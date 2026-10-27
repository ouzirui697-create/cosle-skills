"""Render an offline, escaped HTML evidence report from analyze_ads.py JSON."""
import argparse
import html
import json
from pathlib import Path


def esc(value):
    return html.escape(str(value if value is not None else '待确认'), quote=True)


def fmt(value, percent=False):
    if value is None:
        return '未提供 / 不适用'
    return f'{value:.2%}' if percent else f'{value:,.2f}'.removesuffix('.00')


def table(headers, rows):
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>' + ''.join(f'<th>{esc(h)}</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join(f'<td>{esc(c)}</td>' for c in row)+'</tr>' for row in rows) + '</tbody></table></div>'


REASONS = {
    'free_period': '免费期，不能用ACOS判断付费扩量',
    'billing_unknown': '收费状态待确认',
    'zero_spend_no_paid_evidence': '没有正花费，缺少付费效率证据',
    'spend_incomplete': '花费缺失，不能当作0',
    'row_quality_issues': '原始行存在字段、重复或拆分异常',
    'sheet_quality_issues': '工作表字段存在歧义',
    'action_entity_incomplete': '活动、广告组或ASIN信息不完整',
    'target_acos_unknown': '未提供目标ACOS',
    'sample_policy_unknown': '未定义适用于本次目标的样本门槛',
    'sample_below_user_policy': '点击样本未达到用户设定门槛',
    'attribution_maturity_unknown': '无法确认归因窗口是否完整',
    'attribution_not_mature': '归因窗口尚未完整',
    'currency_unknown': '币种待确认', 'country_unknown': '站点待确认',
    'currency_incomplete': '部分记录的币种待确认', 'country_incomplete': '部分记录的站点待确认',
    'attribution_window_incomplete': '部分表缺少归因窗口',
    'duplicate_daily_entity': '同日同广告实体重复，先核对再汇总',
    'all_rows_have_clicks_coverage_not_proven': '全部记录均有点击；无法证明覆盖零点击曝光，不能当成全账户CTR',
    'row_quality_issues_review_before_using_totals': '总计包含待核查的原始行；请先处理parsed.json中的issues',
}
FIELDS = {'orders':'总订单','sales':'总销售','clicks':'点击','promoted_orders':'本品订单',
          'other_orders':'其他SKU订单','promoted_sales':'本品销售','other_sales':'其他SKU销售'}


def reason(code):
    if code.endswith('_incomplete') and code[:-11] in FIELDS:
        return FIELDS[code[:-11]]+'缺失'
    return REASONS.get(code, code)


def render(data, annotations=None):
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported analysis schema')
    notes = {}
    ids = {u['unit_id'] for u in data['units']}
    for item in annotations or []:
        key = item.get('unit_id')
        if key not in ids or key in notes:
            raise ValueError('Unknown or repeated annotation unit_id')
        if item.get('intent') not in ('L1','L2','L3','unknown') or not item.get('rationale'):
            raise ValueError('Annotations need intent and rationale')
        notes[key] = item
    context, summary = data['context'], data['summary']
    m = summary['metrics']
    billing = {'free':'免费期','paid':'收费期','unknown':'收费状态待确认'}[context['billing']]
    scope = '—'.join(data['date_range_observed']) if data['date_range_observed'] else '日期未明确'
    content = f'<header><p class="eyebrow">COSLE · 广告证据报告</p><h1>SP Prompts 广告诊断</h1><p>{esc(billing)} · {esc(context["country"])} · 币种 {esc(context["currency"])} · 实际日期 {esc(scope)}</p><p>{summary["record_count"]} 条记录 / {summary["unique_prompt_count"]} 个不同问题 / {data["campaign_count"]} 个活动 / {data["asin_count"]} 个广告ASIN</p></header>'
    content += '<nav><a href="#summary">数据总览</a><a href="#decisions">投放判断</a><a href="#responses">回答证据</a><a href="#sources">数据来源</a></nav><main>'
    content += '<section id="summary"><h2>先看订单买了什么</h2><div class="cards">'
    for title, field in [('曝光（文件内）','impressions'),('点击','clicks'),('归因总订单','orders'),('本品订单','promoted_orders'),('其他SKU订单','other_orders'),('花费','spend')]:
        content += f'<article><span>{title}</span><strong>{fmt(m[field])}</strong></article>'
    content += '</div>'
    content += table(['总销售','本品销售','其他SKU销售','CTR（文件内）','订单/点击','CPC','ACOS','ROAS'],[[fmt(m[k], k in ('ctr','purchase_rate','acos')) for k in ('sales','promoted_sales','other_sales','ctr','purchase_rate','cpc','acos','roas')]])
    content += '<p class="notice">总订单不等于本品订单；其他SKU订单不等于回答错误或销售损失。归因不等于净增量。免费期或零花费不能证明收费后有加价空间。缺失值不填0，ROAS分母为0时不定义。</p>'
    warnings = list(data['warnings'])
    if data.get('missing_date_rows'):
        content += f'<p>有 {data["missing_date_rows"]} 条记录缺少可解析的单日日期。</p>'
    if warnings:
        content += '<ul>'+''.join(f'<li>{esc(reason(w))}</li>' for w in warnings)+'</ul>'
    missing = [(FIELDS.get(k,k),v['present'],v['missing'],fmt(v['observed_sum'])) for k,v in summary['coverage'].items() if v['missing']]
    if missing:
        content += '<details><summary>缺失字段覆盖率（已知部分之和不能当完整总计）</summary>'+table(['字段','已提供行','缺失行','已知部分之和'],missing)+'</details>'
    content += '</section><section id="decisions"><h2>投放判断</h2><p>按活动 × 广告组 × ASIN × SKU × 原文问题核算。通过检查只代表可以进一步评估，不自动生成加价百分比，也不授权执行。L3不自动暂停。</p>'
    units = sorted(data['units'], key=lambda u: -(u['metrics']['clicks'] or 0))
    rows=[]
    for u in units:
        note=notes.get(u['unit_id'],{})
        gate=u['gate']
        status='观察/核查：'+'；'.join(reason(r) for r in gate['reasons']) if gate['reasons'] else '可评估：仍需核对相关性、利润、预算与近期稳定性'
        evidence='；'.join(f"{s['sheet']}!行{s['row']}" for s in u['sources'])
        metric=u['metrics']
        rows.append([u['campaign'] or u.get('campaign_id') or '缺活动名',u['ad_group'] or u.get('ad_group_id') or '缺广告组',u['asin'],u['sku'],u['prompt'],note.get('intent','未分类'),note.get('rationale','待模型语义判断'),fmt(metric['clicks']),fmt(metric['orders']),fmt(metric['promoted_orders']),fmt(metric['other_orders']),fmt(metric['spend']),fmt(metric['sales']),status,evidence])
    content += table(['活动','广告组','ASIN','SKU','问题','意图','分类依据','点击','总单','本品单','其他SKU单','花费','销售','判断','来源'],rows)+'</section>'
    content += '<section id="responses"><h2>回答证据：独立核对，不重复计入总额</h2><p>附表可能与主表重叠。没有日期、活动与广告身份的精确关联时，不把示例回答套用到每次展示。型号一致也不代表规格已核验。</p>'
    if not data['response_records']:
        content += '<p>未提供回答原文，回答与产品的匹配状态为未知。</p>'
    for rec in data['response_records']:
        src=rec['source']
        content+=f'<details><summary>{esc(src["sheet"])} · 行{src["row"]} · {esc(rec.get("sku") or rec.get("asin"))} · {esc(rec["prompt"])}</summary><p>{esc(rec["response"])}</p></details>'
    content+='</section><section id="sources"><h2>工作表与来源</h2>'
    content+=table(['工作表','角色','保留记录','排除记录','计入总额'],[[s['name'],s['role'],s['records'],s['excluded'],'是' if s['name'] in data['selected_sheets'] else '否'] for s in data['sheet_inventory']])
    content+=f'<p>文件：{esc(Path(data["source_file"]).name)}<br>SHA-256：<code>{esc(data["sha256"])}</code></p><p>诊断依据已提供的历史样本；当前调整须结合最新收费期报表。建议与实际广告变更是不同步骤。</p></section></main>'
    css='''*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:#0a0b0d;color:#e8eaf0;font:15px/1.7 -apple-system,BlinkMacSystemFont,"Noto Sans SC",sans-serif}header,main,nav{max-width:1280px;margin:auto;padding:24px}header{border-bottom:1px solid #252c3a}h1{font-size:32px}.eyebrow{color:#e63946;letter-spacing:2px}nav{display:flex;gap:20px;flex-wrap:wrap}a{color:#2ec4b6}section{margin:0 0 36px;min-width:0}h2{border-left:4px solid #e63946;padding-left:12px}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}article{background:#181c24;border:1px solid #252c3a;border-radius:10px;padding:16px}article span{color:#aab2c4}article strong{display:block;font-size:30px}.table-wrap{overflow:auto;max-width:100%;border:1px solid #252c3a;margin:16px 0}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;vertical-align:top;padding:10px;min-width:95px;max-width:380px;overflow-wrap:anywhere;border-bottom:1px solid #252c3a}th{background:#181c24;color:#aab2c4}td{white-space:normal}.notice{border-left:3px solid #ffd166;background:#181c24;padding:16px}details{background:#111318;padding:12px;margin:8px 0;border:1px solid #252c3a;border-radius:6px}summary{cursor:pointer}p,code{overflow-wrap:anywhere}@media(max-width:640px){header,main,nav{padding:16px}.cards{grid-template-columns:repeat(2,minmax(0,1fr))}h1{font-size:26px}article strong{font-size:24px}}@media print{@page{size:A4 landscape;margin:12mm}body{background:white;color:#111;font-size:10pt}header,main{padding:0}nav{display:none}.cards{grid-template-columns:repeat(3,1fr)}article,details,th,.notice{background:white;color:#111}.table-wrap{overflow:visible}table{table-layout:fixed;font-size:6pt}th,td{min-width:0;max-width:none;padding:3px;color:#111;overflow-wrap:anywhere}thead{display:table-header-group}tr,article{break-inside:avoid}a{color:#111}details{display:block}details::details-content{content-visibility:visible}details>*{display:block!important}}'''
    return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cosle SP Prompts 广告证据报告</title><style>'+css+'</style><body>'+content+'</body></html>'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('input',type=Path)
    ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--annotations',type=Path,help='Optional model-reviewed unit_id/intent/rationale list')
    args=ap.parse_args()
    notes=json.loads(args.annotations.read_text(encoding='utf-8')) if args.annotations else None
    output=render(json.loads(args.input.read_text(encoding='utf-8')),notes)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(output,encoding='utf-8')
    print(args.out)


if __name__=='__main__':
    main()
