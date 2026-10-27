---
name: cosmo-report
description: >
  Analyze Amazon SP Prompts XLSX/CSV reports with traceable ad metrics, semantic intent
  classification, response checks, and evidence-based action plans. Use for SP Prompts
  分析、COSMO 报告、Rufus 广告诊断或已有广告数据的 Listing 优化。
  Supports advertising-only analysis without Listing input; use prelaunch-listing for
  unlaunched products without ad data and listing-image-audit for image-only reviews.
---

# COSMO × Rufus 广告诊断

先回答卖家「保留什么、核查什么、是否已有调整依据」，再提供来源和计算过程。
脚本负责读取、核算和展示；模型负责语义分类、证据解释与建议。分类不是购买意图真值，
报告也不是账户操作授权。

## 按请求选范围

- **只做广告**：分析报表、归因、活动和问题表现；无需索取五点描述，不生成 Listing 分数或改写。
- **广告 + Listing**：先完成可做的广告分析；需要诊断或改写具体文案时，才按
  [listing-review.md](references/listing-review.md) 核验 Title/Bullets。
- 没有明确请求改写时给修改方向；用户需要完整文案时保留原有交付能力，以已核实事实为依据。

先读取 [data-contract.md](references/data-contract.md) 和 [ad-decisions.md](references/ad-decisions.md)。
只确认影响结论的缺口，已知信息不重复询问。目标、利润或收费状态缺失时，先完成事实分析，
依赖这些信息的建议标为观察/核查，不猜默认值。

## 1. 读取与核算

Python 3.10+；XLSX读取需要 `scripts/requirements.txt` 中的openpyxl，CSV/TSV不需要。
从skill目录运行，输出放用户工作目录或临时目录，不写入skill的脚本/参考目录：

```bash
python3 scripts/parse_prompts.py /path/report.xlsx --out /path/work/parsed.json
python3 scripts/analyze_ads.py /path/work/parsed.json --sheet '主表名称' --out /path/work/analysis.json
```

- 解析器扫描**全部**工作表。检查 `sheet_inventory`、`issues`、`excluded` 和真实日期，
  不把文件名当已验证周期，不把备注、缺名汇总行当普通问题。
- 只有一个纯指标表时可省略 `--sheet`；有多个候选时必须明确选择。附表回答单独保留。
  多表合并须核实无重叠、同币种/站点/归因窗口，再传多个 `--sheet` 和 `--confirmed-disjoint`。
- Spend与CPC分别读取；Campaign/Ad Group不是Title；Ad Name也仅是未核实标签。
- 原始行数、不同问题文本数、广告ASIN数、活动数分别显示。同一问题跨活动不共享调整建议。
- 总/本品/其他SKU订单和销售额并列；缺失为未知，不补0；拆分不一致时核查。
  ACOS/CTR/CPC用总和重算，不平均行级百分比；花费为0时ROAS不定义。
- 重复或字段歧义未处理前，不将总计视为最终可信结果；脚本不擅自删除重复。

用户确认免费期后传 `--billing free`；未知保持默认 `unknown`。付费评估可传：

```bash
python3 scripts/analyze_ads.py /path/work/parsed.json --sheet '主表名称' \
  --billing paid --currency USD --target-acos 0.25 --min-clicks 30 \
  --as-of 2026-04-30 --out /path/work/analysis.json
```

目标和样本是**命令参数示例，不是推荐阈值**，须使用卖家目标与适用样本规则。
`--as-of` 是原始报表已回补归因至哪天，不填今天来使旧数据「成熟」。窗口优先读表头；
有证据时才用 `--attribution-days` 补充。币种/站点缺失可用明确来源的 `--currency` / `--country`。

## 2. 语义分类与回答核查

按 [cosmo_framework.md](references/cosmo_framework.md) 阅读原文，输出
`intent: L1/L2/L3/unknown`、关系、判读依据和歧义；不按有没有数字或问句开头做正则分类。
同一文字可复用语义标签，但广告动作保留活动、广告组、ASIN/SKU和周期。

`response_records` 是独立证据。区分：缺回答、未明确型号、型号一致、明确提及其他型号、
与已核实规格冲突。缺回答不填Irrelevant；同品牌其他型号不等于竞品。
示例回答不证明每次曝光都这样回答，其他SKU订单也不证明回答错误。
没有购买SKU与会话证据，不把二者连接成因果链。

## 3. 形成广告建议

按 [ad-decisions.md](references/ad-decisions.md) 给出「事实 → 判断 → 动作 → 验证」。
每项动作保留源表/行号和广告实体，说明适用目标、证据限制和下一步。

- L3不自动暂停；出单不自动加价；免费期0%ACOS不代表付费效率。
- `observe_or_verify` 表示有缺口；`review_candidate` 仅表示可以进一步评估，
  仍须核查相关性、利润、预算、当前状态与稳定性，不能直接下发固定百分比。
- 不把Prompt子集解释为整个活动或账户表现，不据此调整整个活动预算。
- 小样本洞察注明点击/订单样本量与品类范围；不把单案例变成跨品类常数。
- 前后期保持站点、窗口、长度与指标口径；列出其他变化因素，不直接宣称因果提升。

## 4. 交付

普通问答先给可执行结论，不强制生成长报告。正式广告报告可用：

```bash
python3 scripts/render_ads.py /path/work/analysis.json --out /path/work/广告诊断.html
```

模型分类可通过 `--annotations /path/work/annotations.json` 输入：

```json
[{"unit_id":"复制analysis.json中的真实unit_id","intent":"L3","rationale":"品牌选择泛问；标签本身不决定暂停"}]
```

未分类项显示「未分类」，不要伪装已完成分析。广告报告含：范围/缺口、指标与归因拆分、
具体活动/问题建议、回答证据、来源与复查条件。人工撰写完整报告也使用同一份analysis.json数值，
参考 [report_design.md](references/report_design.md) 的样式；广告-only略去评分、文案和营销章节。

交付前核对源数据不变、无跨表重复累加、拆分与总计一致、建议可追溯、免费期无付费扩量结论；
HTML桌面/窄屏/打印无关键信息丢失，原始文本转义。任何自定义评分必须标为启发式，
不叫「亚马逊官方评分」或「真实Rufus分」。

## 维护与验证

```bash
python3 -m unittest discover -s tests -v
```

测试使用合成数据，真实卖家文件与报告只留本地工作区，不纳入仓库。
新规则写明来源、条件与例外，不把个案CPC、ACOS、点击量或品类当作永久阈值。
