"""Aggregate explicitly selected reports; emit evidence gates, never bid changes."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import date
from pathlib import Path

ADDITIVE = ('impressions', 'clicks', 'spend', 'orders', 'units', 'sales',
            'promoted_orders', 'other_orders', 'promoted_units', 'other_units',
            'promoted_sales', 'other_sales')


def summarize(rows):
    result, coverage = {}, {}
    for field in ADDITIVE:
        present = [r[field] for r in rows if r.get(field) is not None]
        coverage[field] = {'present': len(present), 'missing': len(rows)-len(present),
                           'observed_sum': round(sum(present), 6) if present else None}
        # Unknown data stays unknown. Never present partial spend as complete spend.
        result[field] = round(sum(present), 6) if len(present) == len(rows) and rows else None
    for field, num, den in [('ctr', 'clicks', 'impressions'), ('cpc', 'spend', 'clicks'),
                             ('purchase_rate', 'orders', 'clicks'), ('acos', 'spend', 'sales'),
                             ('roas', 'sales', 'spend'), ('promoted_purchase_rate', 'promoted_orders', 'clicks')]:
        result[field] = result[num] / result[den] if result[num] is not None and result[den] else None
    return {'metrics': result, 'coverage': coverage, 'record_count': len(rows),
            'unique_prompt_count': len({r['prompt'] for r in rows})}


def unit_key(row):
    # Include both identifiers and labels; missing IDs never merge unlike names.
    return tuple(row.get(k) or '' for k in ('country', 'currency', 'campaign_id', 'campaign',
                  'ad_group_id', 'ad_group', 'asin', 'sku', 'prompt'))


def evaluate_gate(rows, summary, context, global_blockers):
    reasons = list(global_blockers)
    metrics = summary['metrics']
    if context['billing'] != 'paid':
        reasons.append('free_period' if context['billing'] == 'free' else 'billing_unknown')
    if metrics['spend'] is None:
        reasons.append('spend_incomplete')
    elif metrics['spend'] == 0:
        reasons.append('zero_spend_no_paid_evidence')
    for field in ('clicks', 'orders', 'sales', 'promoted_orders', 'other_orders', 'promoted_sales', 'other_sales'):
        if metrics[field] is None:
            reasons.append(f'{field}_incomplete')
    if any(r.get('issues') for r in rows):
        reasons.append('row_quality_issues')
    if not all(r.get('asin') and (r.get('campaign') or r.get('campaign_id')) and
               (r.get('ad_group') or r.get('ad_group_id')) for r in rows):
        reasons.append('action_entity_incomplete')
    if not context.get('target_acos'):
        reasons.append('target_acos_unknown')
    if not context.get('min_clicks'):
        reasons.append('sample_policy_unknown')
    elif metrics['clicks'] is None or metrics['clicks'] < context['min_clicks']:
        reasons.append('sample_below_user_policy')
    dates = [r.get('date') for r in rows]
    if not context.get('as_of') or not context.get('attribution_days') or not all(dates):
        reasons.append('attribution_maturity_unknown')
    else:
        elapsed = (date.fromisoformat(context['as_of']) - date.fromisoformat(max(dates))).days
        if elapsed < context['attribution_days']:
            reasons.append('attribution_not_mature')
    if reasons:
        return {'status': 'observe_or_verify', 'reasons': sorted(set(reasons)), 'bid_change_percent': None}
    # Passing a data gate is not permission to mutate an account, nor proof of causality.
    if not metrics['orders'] or not metrics['sales']:
        comparison = 'zero_orders_or_sales_review_relevance_and_user_loss_limit'
    else:
        comparison = 'below_target' if metrics['acos'] < context['target_acos'] else 'at_or_above_target'
    return {'status': 'review_candidate', 'reasons': [], 'target_comparison': comparison,
            'bid_change_percent': None}


def analyze(parsed, sheet_names=None, billing='unknown', target_acos=None, min_clicks=None,
            as_of=None, attribution_days=None, currency=None, country=None, confirmed_disjoint=False):
    if parsed.get('schema_version') != 1:
        raise ValueError('Unsupported parsed schema')
    if billing not in ('free', 'paid', 'unknown'):
        raise ValueError('billing must be free, paid, or unknown')
    if target_acos is not None and (not 0 < target_acos < float('inf')):
        raise ValueError('target_acos must be a positive finite ratio, e.g. 0.25')
    if min_clicks is not None and min_clicks < 1:
        raise ValueError('min_clicks must be positive')
    if attribution_days is not None and attribution_days < 1:
        raise ValueError('attribution_days must be positive')
    if as_of:
        date.fromisoformat(as_of)
    available = {s['name']: s for s in parsed['sheets']}
    if not sheet_names:
        candidates = [s['name'] for s in parsed['sheets'] if s['role'] == 'metrics' and s['records']]
        if len(candidates) != 1:
            raise ValueError('Select one main report using --sheet. Multiple sheets are never automatically summed.')
        sheet_names = candidates
    if len(set(sheet_names)) != len(sheet_names):
        raise ValueError('Repeated sheet selection')
    if len(sheet_names) > 1 and not confirmed_disjoint:
        raise ValueError('Multiple reports require --confirmed-disjoint after checking overlap, scope and attribution.')
    selected = []
    for name in sheet_names:
        if name not in available or available[name]['role'] == 'unrecognized':
            raise ValueError(f'Not a recognized prompt report: {name}')
        selected.append(available[name])
    rows = [r for s in selected for r in s['records']]
    if not rows:
        raise ValueError('No prompt records selected')
    windows = {v for s in selected for v in s['attribution_days']}
    countries = {r['country'] for r in rows if r.get('country')}
    currencies = {r['currency'].upper() for r in rows if r.get('currency')}
    currencies.update(c for s in selected for c in s['header_currencies'])
    for supplied, observed, label in [(attribution_days, windows, 'attribution window'),
                                       (currency.upper() if currency else None, currencies, 'currency'),
                                       (country, countries, 'country')]:
        if supplied and observed and supplied not in observed:
            raise ValueError(f'Provided {label} conflicts with source')
        if supplied:
            observed.add(supplied)
        if len(observed) > 1:
            raise ValueError(f'Mixed {label}: analyze scopes separately')
    global_blockers = []
    if any(s['issues'] for s in selected):
        global_blockers.append('sheet_quality_issues')
    if not currencies:
        global_blockers.append('currency_unknown')
    if not countries:
        global_blockers.append('country_unknown')
    # A known label on one row does not establish the scope of unlabeled rows.
    if not country and countries and any(not r.get('country') for r in rows):
        global_blockers.append('country_incomplete')
    if not currency and any(not s['header_currencies'] and any(not r.get('currency') for r in s['records']) for s in selected):
        global_blockers.append('currency_incomplete')
    if not attribution_days and any(not s['attribution_days'] for s in selected):
        global_blockers.append('attribution_window_incomplete')
    # Detect potentially overlapping daily cells even across different selected sheets.
    daily = set()
    for row in rows:
        if row.get('date'):
            key = (*unit_key(row), row['date'])
            if key in daily:
                global_blockers.append('duplicate_daily_entity')
            daily.add(key)
    context = {'billing': billing, 'target_acos': target_acos, 'min_clicks': min_clicks,
               'as_of': as_of, 'attribution_days': next(iter(windows), None),
               'currency': next(iter(currencies), None), 'country': next(iter(countries), None)}
    groups = defaultdict(list)
    for row in rows:
        groups[unit_key(row)].append(row)
    units = []
    for key, group in groups.items():
        summary = summarize(group)
        unit = {'unit_id': hashlib.sha256(json.dumps(key, ensure_ascii=False).encode()).hexdigest()[:20],
                'campaign': group[0].get('campaign'), 'ad_group': group[0].get('ad_group'),
                'campaign_id': group[0].get('campaign_id'), 'ad_group_id': group[0].get('ad_group_id'),
                'asin': group[0].get('asin'), 'sku': group[0].get('sku'), 'prompt': group[0]['prompt'],
                **summary, 'sources': [dict(r['source'], record_id=r['record_id']) for r in group]}
        unit['gate'] = evaluate_gate(group, summary, context, global_blockers)
        units.append(unit)
    dates = sorted(r['date'] for r in rows if r.get('date'))
    warnings = sorted(set(global_blockers))
    if all(r.get('clicks') and r['clicks'] > 0 for r in rows):
        warnings.append('all_rows_have_clicks_coverage_not_proven')
    if any(r['issues'] for r in rows):
        warnings.append('row_quality_issues_review_before_using_totals')
    excluded_sheets = [s for s in parsed['sheets'] if s['name'] not in sheet_names]
    return {'schema_version': 1, 'source_file': parsed['source_file'], 'sha256': parsed['sha256'],
            'selected_sheets': sheet_names, 'context': context, 'summary': summarize(rows),
            'date_range_observed': [dates[0], dates[-1]] if dates else None,
            'period_texts': sorted({r['period_text'] for r in rows if r.get('period_text')}),
            'missing_date_rows': sum(not r.get('date') for r in rows),
            'campaign_count': len({r.get('campaign_id') or r.get('campaign') for r in rows if r.get('campaign_id') or r.get('campaign')}),
            'asin_count': len({r['asin'] for r in rows if r.get('asin')}),
            'warnings': warnings, 'units': units,
            'sheet_inventory': [{'name': s['name'], 'role': s['role'], 'records': len(s['records']),
                                  'excluded': len(s['excluded']), 'issues': s['issues']} for s in parsed['sheets']],
            'response_records': [r for s in parsed['sheets'] for r in s['records'] if r.get('response')],
            'not_summed_sheets': [s['name'] for s in excluded_sheets]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input', type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--sheet', action='append', dest='sheet_names')
    ap.add_argument('--confirmed-disjoint', action='store_true')
    ap.add_argument('--billing', choices=['free', 'paid', 'unknown'], default='unknown')
    ap.add_argument('--target-acos', type=float)
    ap.add_argument('--min-clicks', type=int)
    ap.add_argument('--as-of', help='Date through which the source was refreshed, NOT the date of this analysis')
    ap.add_argument('--attribution-days', type=int)
    ap.add_argument('--currency')
    ap.add_argument('--country')
    args = vars(ap.parse_args())
    path, out = args.pop('input'), args.pop('out')
    try:
        result = analyze(json.loads(path.read_text(encoding='utf-8')), **args)
    except ValueError as error:
        ap.error(str(error))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"{result['summary']['record_count']} rows / {result['summary']['unique_prompt_count']} distinct prompts / {len(result['units'])} action units")


if __name__ == '__main__':
    main()
