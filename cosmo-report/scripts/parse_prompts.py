"""Read every XLSX/CSV/TSV sheet without combining overlapping reports.

Requires openpyxl for XLSX only. No network access and no source-file writes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from datetime import date, datetime
from pathlib import Path

SCHEMA_VERSION = 1
METRICS = (
    'impressions', 'clicks', 'spend', 'orders', 'units', 'sales',
    'promoted_orders', 'other_orders', 'promoted_units', 'other_units',
    'promoted_sales', 'other_sales', 'cpc', 'ctr', 'acos', 'roas',
)
COUNTS = {'impressions', 'clicks', 'orders', 'units', 'promoted_orders',
          'other_orders', 'promoted_units', 'other_units'}


def norm(value):
    return re.sub(r'\s+', ' ', str(value if value is not None else '').strip().casefold())


ALIASES = {
    'prompt': ['prompt', 'prompt detail', 'prompt details', '提示词', '提示详细', '提示详细信息'],
    'response': ['sample response', 'rufus response', '示例回答', '回答示例', '示例响应'],
    'campaign': ['campaign name', '广告活动名称'],
    'campaign_id': ['campaign id', '广告活动编号'],
    'ad_group': ['ad group name', '广告组名称'],
    'ad_group_id': ['ad group id', '广告组编号'],
    # Keep these separate. Neither a campaign nor an ad group is a product title.
    'ad_name': ['ad name', '广告名称'],
    'title': ['product title', 'listing title', '商品标题', '产品标题'],
    'asin': ['asin', 'advertised asin', '广告asin', '广告 asin'],
    'sku': ['sku', 'advertised sku', '广告sku', '广告 sku'],
    'date': ['date', '日期'],
    'period_text': ['time', 'period', 'report period', '时间', '周期'],
    'country': ['country', 'marketplace', '国家', '站点'],
    'currency': ['currency', 'currency code', '货币', '币种'],
    'impressions': ['impressions', '曝光', '展示量', '展示'],
    'clicks': ['clicks', '点击量', '点击'],
    'spend': ['spend', 'cost', 'total cost', '花费', '支出', '总花费'],
    'cpc': ['cpc', 'cost per click', 'cost per click (cpc)', '平均点击成本', '单次点击成本'],
    'ctr': ['ctr', 'click-thru rate (ctr)', 'click through rate (ctr)', '点击率'],
    'acos': ['acos', 'total advertising cost of sales (acos)', '广告销售成本'],
    'roas': ['roas', 'total return on advertising spend (roas)'],
    'orders': ['purchases', 'orders', 'total orders', '订单', '购买'],
    'units': ['units', 'total units', 'units sold'],
    'sales': ['sales', 'total sales', 'revenue', '销售额'],
    'promoted_orders': ['advertised sku orders', 'purchases (promoted)'],
    'other_orders': ['other sku orders', 'purchases (halo)'],
    'promoted_units': ['advertised sku units', 'units sold (promoted)'],
    'other_units': ['other sku units', 'units sold (halo)'],
    'promoted_sales': ['advertised sku sales', 'sales (promoted)'],
    'other_sales': ['other sku sales', 'sales (halo)'],
}
LOOKUP = {norm(alias): field for field, aliases in ALIASES.items() for alias in aliases}


def identify_header(value):
    """Exact aliases after removing ONLY documented units/window decorations."""
    text = norm(value)
    currency_match = re.search(r'\((USD|CAD|GBP|EUR|JPY|AUD|CNY|MXN)\)', text, re.I)
    currency = currency_match.group(1).upper() if currency_match else None
    text = re.sub(r'\s*\((?:usd|cad|gbp|eur|jpy|aud|cny|mxn|#)\)', '', text).strip()
    match = re.match(r'^(\d+)\s*day\s+', text)
    window = int(match.group(1)) if match else None
    if match:
        text = text[match.end():]
    field = LOOKUP.get(text)
    return field, window, currency


def number(value, field):
    if value is None or norm(value) in ('', '-', '—', 'n/a', 'na', 'null'):
        return None
    if isinstance(value, bool):
        raise ValueError('boolean is not a numeric metric')
    if isinstance(value, (int, float)):
        result = float(value)
    else:
        text = str(value).strip()
        percent = text.endswith('%')
        if percent and field not in {'ctr', 'acos'}:
            raise ValueError('unexpected percent sign')
        text = text.removesuffix('%').strip()
        text = re.sub(r'^(?:USD|CAD|GBP|EUR|JPY|AUD|CNY|MXN|[$€£¥])\s*', '', text, flags=re.I)
        # Accept 1,234.56; reject locale-ambiguous 1.234,56 / 1,23.
        if not re.fullmatch(r'-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?', text):
            raise ValueError('unsupported numeric format')
        result = float(text.replace(',', '')) / (100 if percent else 1)
    if not math.isfinite(result) or result < 0:
        raise ValueError('non-finite or negative metric; reconcile source first')
    if field in COUNTS:
        if not result.is_integer():
            raise ValueError('fractional count')
        return int(result)
    # Numeric Excel percentages are already ratios. ACOS can legitimately exceed 1.
    return result


def date_text(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()[:10]
    text = str(value or '').strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}(?:$|[ T])', text):
        try:
            return date.fromisoformat(text[:10]).isoformat()
        except ValueError:
            pass
    return None


def parse_sheet(name, rows, source_hash):
    best = None
    for index, row in enumerate(rows[:20]):
        found = {}
        for col, header in enumerate(row):
            field, window, currency = identify_header(header)
            if field:
                found.setdefault(field, []).append((col, window, currency))
        score = len(found)
        if best is None or score > best[0]:
            best = (score, index, found)
    result = {'name': name, 'role': 'unrecognized', 'header_row': None,
              'columns': {}, 'issues': [], 'records': [], 'excluded': []}
    if not best or 'prompt' not in best[2]:
        return result
    _, header_index, found = best
    headers = rows[header_index]
    result['header_row'] = header_index + 1
    windows, currencies = set(), set()
    for field, matches in found.items():
        if len(matches) > 1:
            result['issues'].append({'code': 'ambiguous_column', 'field': field,
                                     'headers': [str(headers[m[0]]) for m in matches]})
            continue  # Never silently choose one of two competing attribution windows.
        col, window, currency = matches[0]
        result['columns'][field] = {'index': col, 'header': str(headers[col]),
                                    'attribution_days': window}
        if window:
            windows.add(window)
        if currency:
            currencies.add(currency)
    result['attribution_days'] = sorted(windows)
    result['header_currencies'] = sorted(currencies)
    if not all(k in result['columns'] for k in ('prompt', 'impressions', 'clicks')):
        result['issues'].append({'code': 'missing_required_columns'})
        return result
    result['role'] = 'response_detail' if 'response' in result['columns'] else 'metrics'
    seen = {}
    for rownum, row in enumerate(rows[header_index+1:], header_index+2):
        if all(v is None or v == '' for v in row):
            continue
        raw = {f'{i+1}:{h}': row[i] for i, h in enumerate(headers) if h is not None and i < len(row)}
        values = {field: row[info['index']] if info['index'] < len(row) else None
                  for field, info in result['columns'].items()}
        prompt = str(values.get('prompt') or '').strip()
        if prompt in ('', '-', '—', 'ASIN HERE', 'Prompt HERE', '[Prompt]') or prompt.casefold() in ('total', 'grand total', '合计', '总计'):
            result['excluded'].append({'row': rownum, 'reason': 'missing_prompt_or_summary', 'raw': raw})
            continue
        rec = {'record_id': hashlib.sha256(f'{source_hash}:{name}:{rownum}'.encode()).hexdigest()[:20],
               'source': {'sheet': name, 'row': rownum}, 'raw': raw, 'issues': []}
        for field, value in values.items():
            if field in METRICS:
                try:
                    rec[field] = number(value, field)
                except ValueError as error:
                    rec[field] = None
                    rec['issues'].append({'code': 'invalid_number', 'field': field, 'value': str(value), 'reason': str(error)})
            elif field == 'date':
                rec[field] = date_text(value)
                if value and rec[field] is None:
                    rec['issues'].append({'code': 'unparsed_date', 'value': str(value)})
            else:
                text = str(value).strip() if value is not None else None
                rec[field] = None if norm(text) in ('', '-', '—', 'n/a', 'null') else text
        # No fallback from campaign/ad_group/ad_name to product title.
        rec['ad_name_kind'] = 'unverified_ad_label' if rec.get('ad_name') else None
        for field in METRICS:
            rec.setdefault(field, None)
        for total, own, other in [('orders', 'promoted_orders', 'other_orders'),
                                  ('units', 'promoted_units', 'other_units'),
                                  ('sales', 'promoted_sales', 'other_sales')]:
            if all(rec[f] is not None for f in (total, own, other)):
                if abs(rec[total] - rec[own] - rec[other]) > 0.011:
                    rec['issues'].append({'code': 'attribution_split_mismatch', 'field': total})
        fingerprint = json.dumps(raw, sort_keys=True, default=str, ensure_ascii=False)
        if fingerprint in seen:
            rec['issues'].append({'code': 'duplicate_row', 'first_row': seen[fingerprint]})
        else:
            seen[fingerprint] = rownum
        result['records'].append(rec)
    return result


def parse_file(path):
    path = Path(path)
    source_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    sheets = []
    if path.suffix.lower() == '.xlsx':
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        try:
            for ws in wb:
                sheets.append(parse_sheet(ws.title, list(ws.iter_rows(values_only=True)), source_hash))
        finally:
            wb.close()
    elif path.suffix.lower() in ('.csv', '.tsv'):
        with path.open(encoding='utf-8-sig', newline='') as handle:
            rows = list(csv.reader(handle, delimiter='\t' if path.suffix.lower() == '.tsv' else ','))
        sheets.append(parse_sheet(path.name, rows, source_hash))
    else:
        raise ValueError('Supported formats: .xlsx, .csv, .tsv')
    return {'schema_version': SCHEMA_VERSION, 'source_file': str(path.resolve()),
            'sha256': source_hash, 'sheets': sheets}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args()
    result = parse_file(args.input)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str), encoding='utf-8')
    for sheet in result['sheets']:
        print(f"{sheet['name']}: {sheet['role']} / {len(sheet['records'])} records / {len(sheet['excluded'])} excluded / {len(sheet['issues'])} sheet issues")


if __name__ == '__main__':
    main()
