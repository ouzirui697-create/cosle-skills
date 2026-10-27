# 广告数据契约

## 来源与范围

parse_prompts.py输出schema_version=1，含文件路径、SHA-256和全部工作表。
每张表含角色、表头行、映射列、归因天数、币种、records、excluded、issues。
角色为metrics / response_detail / unrecognized，仅帮助选表，不证明无重叠。
被跳过的缺名、合计与备注行保留原始内容供核查，不自动分摊其数字。

源文件不会改写。记录含record_id、source.sheet/source.row、原始单元格raw。
CSV按UTF-8（可带BOM）读取，TSV按制表符；Excel读缓存值，缺公式缓存仍是缺失。
未支持的表头只有明确加入别名后才识别，不模糊猜列。

## 精确字段

- 身份：campaign/campaign_id、ad_group/ad_group_id、asin、sku、prompt。
- 文字：response、ad_name、title（仅Product Title/Listing Title等明确列）。
- 基础：impressions、clicks、spend；cpc/ctr/acos/roas保留原值，汇总重新计算。
- 归因：orders/units/sales及promoted_* / other_*；保留表头7 Day等归因窗口。
- 范围：date、period_text、country、currency。

表头忽略大小写、空格及已定义币种/(#)装饰后**完整匹配**，不会让Cost Per Click抢占Spend。
同时出现7天与14天同名指标等多重映射时，该字段置为缺失并记录歧义，不选第一个。
数字百分比按Excel原值保存：1.5=150%；文本0.5%=0.005；不靠大于1猜单位。
`1,234.56`可读，`1.234,56`等歧义格式报异常；负数、非有限值和非整数计数标记核查。
没有明确币种时，不只凭`$`猜USD。Spend缺失阻断成本结论；CPC/CTR可由基础字段重算。

## 汇总与检查

analyze_ads.py只累计选中表，回答表作为独立证据。默认选唯一非空metrics表，否则需--sheet。
多个表须确认无重叠后显式选择；不同已知站点、币种、归因窗口拒绝合并。
完全重复行标记duplicate_row；同日期、同广告实体重复时阻断评估。存在隐含维度的可能，
不能静默删重复，必须核查。不同文字默认不归一化。

总计只有所有选中行都有值时才求和，否则为null；coverage同时显示已知/缺失行及已知部分之和。
总=本品+其他逐行核对允许金额舍入误差0.011，异常定位原行；缺失拆分不补0。
其他SKU不是已确定购买型号，需要购买商品报告才可识别。

操作单元：country/currency + campaign_id/name + ad_group_id/name + ASIN + SKU + 原文问题。
保留名称与ID避免空ID误合并；原始行数、不同问题数独立报告，后者也不是独立用户数。

## 收费、日期与统计边界

billing取用户或账单确认的free/paid/unknown，不凭日期或0成本推断。
as_of是报表回补截止日，不是分析日；窗口来自表头或有来源的参数。
只有范围文字而无单日date时，脚本不判定成熟，仍能完成事实分析。
全部行有点击时提示可能有选择性覆盖，CTR仅代表文件内样本。

target_acos是用户比例（0.25=25%），无品类默认值。min_clicks是本次选择的样本政策，
只检查下限，不代表统计显著性、足够订单或可加价证明。缺失参数不阻止读取与解释事实。

官方参考（读取于2026-10-27，操作时核对当前站点界面）：
- https://advertising.amazon.com/resources/whats-new/unboxed-2025-sponsored-products-and-sponsored-brands-prompts
- https://advertising.amazon.com/help/GYNVHW8R4QPYUS9H

平台资料解释Prompts与归因，不为本工具分类、竞价阈值或评分背书。
