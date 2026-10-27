# COSMO相关语义框架与工具标签

参考：Yu et al. (2024), COSMO: A Large-Scale E-commerce Common Sense Knowledge Generation
and Serving System at Amazon, https://doi.org/10.1145/3626246.3653398 。
关系词汇用于组织语义；本工具的L1/L2/L3、运营建议与评分不是亚马逊官方规则。
引用具体论文结论须核验原文，不把案例转化占比、关键词句式或缓存时间说成平台事实。

## 先读问题，不看转化给标签

| 标签 | 原文表达 | 示例 | 边界 |
|---|---|---|---|
| L1 功能/能力 | 命名功能、标准、协议、容量等 | dual band、Wi-Fi 6、WireGuard | 不要求数字或Does开头 |
| L2 场景/人群/泛功能 | 受众、场景或泛问有哪些功能 | suitable for travelers、what features | 场景+功能混合时说明主意图 |
| L3 品牌/品类浏览 | 泛品牌选择、纯品类发现 | Why choose Brand routers? | 不表示没有购买价值或应停投 |
| unknown | 缺失、歧义过大 | 无法识别的文字片段 | 不默认L3 |

「How fast is its VPN throughput?」是具体性能问题，可判L1，不因How fast句式判L3。
「Wi-Fi 6 for fast gaming」同时含标准与场景，可按主意图判L1或L2，写明理由并保持批次一致。
「easy setup」为泛化易用性，说明L1/L2边界，不强行等同量化规格。
「portable router」可能仅是品类，不自动判具体能力。
成交、是否该投放是独立判断，不改变问题语义标签。

## 关系词汇

| 关系 | 用途 |
|---|---|
| capable_of | 具体能力 |
| used_for_func | 功能用途 |
| used_to | 完成动作 |
| xWant | 买家希望的结果 |
| used_for_eve | 事件/场合 |
| used_for_aud | 受众 |
| used_as | 用作某角色 |
| used_on | 时间/情境 |
| used_in_loc | 使用地点 |
| used_with | 兼容/搭配 |
| used_by | 使用者 |
| xIs_a | 买家身份 |
| used_in_body | 身体部位 |
| is_a | 商品类型 |
| xInterested_in | 兴趣主题 |

关系与意图不是强制一对一映射，不合适时用unknown；示例不是转化排名。

## 回答与商品匹配

- missing_response：未提供/空白，不当Irrelevant。
- model_unspecified：只有品牌/品类，无法确认具体ASIN。
- model_consistent_specs_unverified：型号一致但规格未核实，不代表全面准确。
- different_model：明确提及其他型号，记录原文、广告型号、回答型号。
- verified_spec_conflict：与已核实产品事实冲突，必须附事实来源。

如需ESCI（Exact/Substitute/Complement/Irrelevant），必须有足够产品与问题证据。
ESCI相关性与「回答换型号」是不同维度；同品牌其他SKU不等于跨品牌竞品，
其他SKU归因也不能替代回答证据。

## 文案启发

具体事实、可理解功能与买家场景可帮助表达；更多数字不自动更好，capable of不是必需关键词。
不能为分数编造性能、认证或倍数。文案模块见[listing-review.md](listing-review.md)，广告-only不加载。
