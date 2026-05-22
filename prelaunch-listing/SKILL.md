---
name: prelaunch-listing
description: >
  Generate a Rufus-optimized listing and COSMO pre-launch report for a new Amazon product that
  has NOT yet launched (no SP Prompts data exists). Use this skill whenever a seller asks for
  help writing a listing for a new product, generating pre-launch copy, creating a COSMO report
  for an unlaunched product, or optimizing a new product's listing before going live on Amazon.
  Also trigger when the user says things like "新品listing", "新产品文案", "上市前listing",
  "pre-launch listing", "帮我写listing", "新品COSMO报告", "还没上架的产品怎么写listing",
  or any request involving writing Amazon listing copy from scratch using COSMO/Rufus methodology.
  This skill uses competitor proxy analysis + product specs to predict the Prompt universe and
  generate listing copy that maximizes Rufus friendliness BEFORE the product goes live.
  Do NOT use the cosmo-report skill for pre-launch products — that skill requires real SP Prompts
  data. This skill is the correct choice when no advertising data exists yet.
---

# Pre-Launch Listing Generator (COSMO × Rufus)

## What this skill does

Generates a complete, Rufus-optimized Amazon listing and predictive COSMO report for a product
that has NOT yet launched. Unlike the cosmo-report skill (which diagnoses existing campaigns),
this skill works from competitor data and product specs to **predict** what Rufus will ask and
**generate** listing copy that answers those questions with high typicality.

Output is a **single HTML file** containing:
1. **Predicted Prompt Universe** — what Rufus will likely ask about this product, classified L1/L2/L3
2. **Competitor Benchmark** — how competitors cover each predicted prompt, where the gaps are
3. **Generated Listing Copy** — Title, 5 Bullet Points, A+ content outline, Backend keywords
4. **Predicted Rufus Friendliness Score** — scored per dimension (clearly labeled as prediction)
5. **Cross-Model Substitution Risk** — if the seller has other SKUs, assess cannibalization risk
6. **Post-Launch Verification Roadmap** — D+30/D+60/D+90 action plan

---

## Core Methodology Difference

| Dimension | cosmo-report (existing products) | prelaunch-listing (this skill) |
|-----------|----------------------------------|-------------------------------|
| Core input | SP Prompts xlsx (real ad data) | Competitor ASINs + product specs |
| Data source | Seller's ad console | Competitor listings, reviews, category data |
| COSMO classification | Based on actual Prompt performance | Inferred from competitor proxy |
| Output type | Diagnostic (what's wrong) | Generative (what to write) |
| Language tone | "Listing缺少X" (diagnostic) | "建议listing包含X" (prescriptive) |
| Score label | Rufus Friendliness Score | **Predicted** Rufus Friendliness Score |

**Critical language rule**: This report must NEVER use diagnostic language like "listing缺少X参数".
Everything is prescriptive: "建议listing包含X参数以覆盖L1 Prompt". No verification = no diagnosis
applies even more strongly here, since there is no live listing to verify against.

---

## Workflow

### Step 0 — Gather Inputs

The seller provides (minimum viable input is items 1 and 2):

| Input | Content | Who fills it |
|-------|---------|-------------|
| 1. Product Spec Sheet | Product name, category, key specs (materials, dimensions, capacity, performance numbers), USP, target audience, planned price | Seller |
| 2. Competitor ASINs | 3–5 direct competitors + 1–2 category leaders | Seller |
| 3. Brand Assets (optional) | Brand voice, visual language, existing customer profiles | Seller |
| 4. Same-brand ASINs (optional) | If the seller has other products already on Amazon, list them for cross-model substitution risk analysis | Seller |

If the seller provides an xlsx template (`Cosle_PreLaunch_Input_Template`), parse it with openpyxl.
If they provide info in chat, extract and organize it.

### Step 1 — Pull Competitor Data

For each competitor ASIN:
1. `web_fetch` on `https://www.amazon.com/dp/[ASIN]` with `html_extraction_method: markdown`
2. Extract: Title, Bullet Points, Product Description, A+ content text, key specs
3. If `web_fetch` fails, try `web_search` for `[product name] amazon [ASIN]`
4. Note which COSMO relations each competitor's listing covers well vs poorly

For competitor reviews (if accessible):
1. `web_search` for `[competitor product] amazon reviews` to find review themes
2. Cluster review language by COSMO relation types (what buyers praise = capable_of signals,
   what scenarios they mention = used_for/used_in signals)

### Step 2 — Build Predicted Prompt Universe

Using the COSMO 15-relation framework (read `references/cosmo_framework.md`), generate predicted
Rufus Prompts by:

1. **L1 Prompts (高典型性)**: For each key product spec, generate `capable_of`, `used_for_func`,
   `used_to`, and `xWant` prompts. These are the highest-value prompts.
   - Example: Product has "1800Mbps dual-band" → Predict: "Does [brand] have a router with gigabit speeds?"
   - Example: Product has "pre-installed VPN" → Predict: "Does [brand] have a router with VPN built in?"

2. **L2 Prompts (中典型性)**: For each target scenario, audience, and use location, generate
   `used_for_eve`, `used_for_aud`, `used_in_loc`, `used_with`, `used_by` prompts.
   - Example: Target audience "digital nomads" → Predict: "What router is best for remote workers?"

3. **L3 Prompts (低典型性)**: Generate generic `is_a` and `xInterested_in` prompts.
   - These are low value but will appear. Flag them for monitoring, not investment.

Cross-reference against competitor data to identify:
- **Covered prompts**: Competitors answer well → must match or exceed
- **Gap prompts**: No competitor answers well → opportunity to own
- **Crowded prompts**: Many competitors answer → hard to differentiate

### Step 3 — Generate Listing Copy

Follow COSMO typicality rules strictly. Read `references/cosmo_framework.md` for the full taxonomy.

**Title (≤200 chars, front-load first 80)**:
- First 80 chars: Brand + Product type + #1 differentiating L1 spec (with number)
- Remaining: Secondary L1 specs + primary L2 scenario keyword

**5 Bullet Points** (each maps to a predicted L1 Prompt cluster):
- Use COSMO triple format: `[FEATURE LABEL]: [product] capable of [specific function] – [exact spec with numbers] for [use case]`
- Every bullet must contain at least one specific number/measurement
- Order by predicted Prompt frequency (most common L1 prompt cluster first)

**A+ Content Outline** (each module maps to an L2 scenario):
- Module 1: Hero banner with primary USP + key number
- Module 2–4: Each covers one L2 scenario (event/audience/location)
- Module 5: Comparison chart vs competitors (feature × feature)

**Backend Keywords**:
- All L1 prompt keywords NOT already in Title/Bullets
- L2 scenario terms not covered in A+
- Do NOT stuff L3 terms

**Brand Story (if Brand Registry)**:
- Handle L3 "why choose [brand]" prompts here
- Not high conversion but provides brand context

### Step 4 — Predict Rufus Friendliness Score

Score the generated listing against the predicted Prompt universe. Use the same dimensions
as the cosmo-report skill but clearly label everything as **PREDICTED**:

| Dimension | Weight | How to Score |
|-----------|--------|--------------|
| capable_of 功能覆盖度 | 40% | % of predicted L1 Prompts with specific numbers/specs in listing |
| Typicality 质量 | 30% | Quality of descriptions (vague=30, specific=80, with numbers=100) |
| 前80字符意图密度 | 15% | Do Title's first 80 chars contain key L1 feature words? |
| L2/L3场景覆盖 | 10% | Diversity of scenario/audience coverage in Bullets + A+ |
| Cross-Model Risk | -5% | Deduct if same-brand SKUs have overlapping feature descriptions |

**Rating**: 0–40 = 🔴 Critical, 41–60 = 🟡 Needs Work, 61–80 = 🟢 Good, 81–100 = ✨ Excellent

**MANDATORY caveat** in the report: "本分数为预测值，基于COSMO方法论和竞品数据推演。
COSMO模型持续更新，实际Rufus行为可能与预测存在偏差。建议上市D+30后使用真实SP Prompts数据进行验证。"

### Step 5 — Cross-Model Substitution Risk (if applicable)

If the seller has other ASINs already on Amazon:
1. `web_fetch` each existing ASIN's listing
2. Compare feature descriptions with the new product's generated listing
3. Flag any overlapping descriptions that could cause Rufus to recommend the wrong SKU
4. Suggest differentiation strategies (e.g., "existing SKU emphasizes portability,
   new SKU should emphasize performance/throughput")

### Step 6 — Post-Launch Verification Roadmap

This section is MANDATORY. It's what turns a one-time prediction into a data loop.

| Timeline | Action | Deliverable |
|----------|--------|-------------|
| D+30 | Pull first SP Prompts report | Compare predicted vs actual Prompt universe; calculate hit rate |
| D+60 | Run full cosmo-report skill | First real diagnostic; identify prediction misses |
| D+90 | Review prediction accuracy | Feed back into methodology; adjust listing if needed |

Include exact Amazon console navigation paths for pulling SP Prompts data.

---

## HTML Report Structure

Use the same design system as the cosmo-report (read `references/report_design.md`).
Key visual differences from the diagnostic report:

1. **Hero header**: Include "预测性报告 · Pre-Launch" badge prominently.
   Use a different accent — amber/yellow (#f4a261) instead of red for the badge,
   to visually distinguish from diagnostic reports.

2. **Predicted Prompt Universe table**: Same table format as cosmo-report's COSMO Analysis,
   but columns are: Predicted Prompt | COSMO Relation | Level | Competitor Coverage | Listing Coverage

3. **Competitor Benchmark**: Heat map or coverage matrix showing each competitor's
   coverage of each predicted prompt

4. **Generated Listing**: Display Title, Bullets, A+ outline, Backend in styled code blocks
   with copy-paste formatting

5. **Predicted Score**: Same score ring component but with amber color and "PREDICTED" label

6. **Verification Roadmap**: Timeline visualization with D+30/D+60/D+90 milestones

---

## Output

Save the report as `[ProductName]_PreLaunch_COSMO优化报告.html` in `/mnt/user-data/outputs/`
and call `present_files` to share it with the user.

Tell the user: "这是一份预测性报告。下载后用浏览器打开查看。产品上市后第 1 周（W+1）起，请提供真实 SP Prompts 数据，我们会出具周颗粒度验证报告（W+1 / W+2 / W+4 / W+8 / W+12）。"

---

## Brand Profiles

在生成 listing 文案前，**先识别品牌**。若品牌匹配下方档案，在 COSMO 方法论之上叠加品牌特有规范。品牌规范覆盖通用格式建议，但永远不覆盖 COSMO 典型性规则（Typicality）。

### GL.iNet (GL Technologies)

**触发条件**：品牌为 GL.iNet，或产品名含 Mudi / Beryl / Slate / Brume / Opal / Flint / Spitz / Convexa，或型号以 `GL-` 开头。

---

**品牌写法**：始终写 `GL.iNet` — 不写 `GL`、`GL iNet`、`Glinet`、`glinet`

**产品命名**：`[产品代号] [代际] ([型号])` — 如 `Mudi 7 (GL-E5800)`、`Beryl AX (GL-MT3000)`
- 代号：自然界英文单词（Mudi, Beryl, Slate, Brume, Opal, Flint, Spitz）
- 型号格式：`GL-[字母][数字]`
- Listing 中必须同时出现产品代号和型号

---

**Title 结构**：
```
GL.iNet [产品代号] ([型号]) [主品类] with [Feature 1] & [Feature 2], [Spec 1], [Spec 2] — [使用场景 Tagline]
```
- `—` 破折号分隔参数列表与场景 tagline
- Tagline 简短（< 30 chars）：如 "Mobile Hotspot for Travel, Livestream"
- Title 中数字紧凑写法：`5.76 Gbps`、`700Mbps`、`13.5h`（注意 `13.5h` 连写，不带空格）

---

**Bullet Points 格式**：
- 标题用全角方括号 `【Feature Name】`，**不用** 通用 COSMO 格式 `[LABEL]: product capable of...`
- 右括号后**无冒号**，直接接正文
- 核心芯片/模组必须写全称：`Qualcomm Dragonwing MBB Gen 3 (X72)`
- 速率格式：`688 Mbps (2.4 GHz) + 2882 Mbps (5 GHz) + 5765 Mbps (6 GHz)`
- 句内用 `—` 破折号过渡（不用逗号、不用冒号）
- Bullet 末尾列出使用场景：`for lag-free 4K streaming, gaming, and Zoom/Teams meetings`
- VPN/速率类 Bullet 末尾加免责声明：`*Speeds measured on local network; real-world results vary.*`

**Bullet 顺序（GL.iNet 惯例优先级）**：
1. 主连接速率（5G / Wi-Fi 标准 + 芯片）
2. SIM 灵活性（eSIM + Dual SIM 细节）
3. 有线 I/O（Ethernet + USB-C 规格）
4. 网络可靠性（Multi-WAN Failover）
5. 电池续航
6. 屏幕 / 交互（Touchscreen 快捷操作）
7. VPN（预装服务商 + 速率）

---

**Description 格式**：
- H1 标题：`GL.iNet [产品] ([型号]) — [品类] + [核心卖点]`
- 开篇句：`built for people whose [work / travel / content] depends on [core value]`
- KEY FEATURES 区块用 `•` 列点（不用 `-`）
- 末行固定格式：`Ideal for: business travellers, digital nomads, ...`（逗号分隔受众）
- 全文末尾加 VPN 免责声明

---

**Keywords 风格**：
- 全小写，空格分隔，无逗号无分号
- 必含：产品代号 + 型号（去连字符）— `mudi 7 e5800`
- 必含：芯片名 — `dragonwing x72`
- 美国站必含：运营商关键词 — `at&t t-mobile verizon unlocked`
- 必含：核心使用场景词 — `pop-up retail food truck pos backup digital nomad remote work`

---

**语气 / 受众定位**：
- 技术性强，面向专业用户，不用空洞形容词
- 具名使用场景：`pop-up retail POS, food trucks, trade-show booths, festival vendors`
- 受众列举：business travellers, digital nomads, content creators, livestreamers, remote engineers, expats, campervan users, privacy-conscious families

---

**GL.iNet 禁止事项**：
- ❌ 不用通用 COSMO 格式 `[LABEL]: [product] capable of [function]` — GL 用 `【】` 叙述风格
- ❌ 不写 `GL` 单独出现（必须是 `GL.iNet`）
- ❌ Title 不得省略型号 `(GL-XXXX)`
- ❌ 不用 emoji（✅ ❌ 🔴）作为 Bullet 开头 — GL 用 `【】`
- ❌ 不暗示 eSIM + 双 SIM 三槽同时工作（eSIM 启用时占用一个物理 SIM 位）

---

## Reference Files

- `references/cosmo_framework.md` — Full 15-relation COSMO taxonomy with examples and typicality scoring
- `references/report_design.md` — HTML/CSS design system for the report

These are the same reference files used by the cosmo-report skill. Read them when you need
detail on classification rules or when writing the HTML output.

---

## Lessons learned (from real seller feedback rounds)

These lessons come from real seller review cycles. When generating any pre-launch listing report,
explicitly check each item below — they are the most common failure modes that erode seller
trust when caught by their internal review.

### 1. SIM hardware reality > marketing simplification

eSIM + Dual Nano-SIM 路由器中，<strong>eSIM 启用时通常会占用一个物理 SIM 槽位</strong>（共享逻辑 — 这是行业普遍硬件实现，不是"3 个 SIM 同时活跃"）。生成 Bullet 时：

- ✅ <strong>对</strong>："Two active SIM profiles simultaneously — flexibly combine eSIM with two nano-SIM slots (eSIM uses one SIM position when activated)"
- ❌ <strong>错</strong>："three physical SIM slots running simultaneously" / 暗示三槽同时工作

务必<strong>主动向卖家确认硬件细节</strong>（"是 1 active SIM 还是 2 active SIM？eSIM 启用时是否占物理槽？"）。不要凭"Onboard eSIM Chipset"字面描述就假设 3 槽同时工作。

### 2. Numbers must be auditable, or use fuzzy descriptors

"140+ international carriers" / "支持 N 国家" 等具体数字如果没有<strong>对应官方清单 / 链接背书</strong>，消费者会追问"具体哪些国家"，触发客诉风险。预测报告中：

- ✅ <strong>对</strong>："global carriers" / "carriers worldwide" / "international roaming supported"
- ✅ <strong>对</strong>（如有清单）："140+ carriers (full list at brand.com/coverage)"
- ❌ <strong>错</strong>：纯数字 "140+ countries" 不附验证路径

数字越具体，可证伪压力越大。预测阶段保守使用，把具体数字留给卖家在 A+ Brand Story 或 backend 附完整清单后再放出来。

### 3. Avoid absolute claims ("No X", "Zero X", "Without X")

"No App, No Admin Panel" / "Zero Setup" / "No Cables" 等绝对化措辞容易被消费者解读为"完全不需要 X"。但几乎所有产品都<strong>仍需要软件做高级配置</strong>。修订建议：

- ✅ <strong>对</strong>："no need to open the app <em>for everyday tasks</em>" / "X-free quick controls"
- ✅ <strong>对</strong>：明确"Combined with the [Brand] app for advanced configuration"
- ❌ <strong>错</strong>："No App, No Admin Panel"（让买家以为完全不用 app）/ "Setup-Free"

绝对化卖点放第一句还会触发广告法红线（部分类目）。建议改为"hybrid setup"等中性表达。

### 4. Preorder price vs official price — never anchor on preorder

预售价（preorder/early-bird）通常比正式价低 10-15%。生成 Comparison Chart / 价格对比时<strong>必须用正式价</strong>，不能用预售价做锚点：

- ✅ <strong>对</strong>："Official price $419.99 (preorder closed at $369.99)"
- ❌ <strong>错</strong>：Comparison Chart 只写 $369.99 不标注是预售价

报告生成前主动询问卖家："当前售价是预售价还是正式价？预售期到什么时候？" 并在 footer / 局限章节标注。

### 5. Verification cadence: weekly granularity beats monthly

D+30 / D+60 / D+90 三点位（按月）颗粒度太粗，错过了 W+1、W+2 最有价值的早期 prompt 信号（这两周是<strong>预测命中率最高 / "意外 prompt" 最容易暴露</strong>的窗口）。新版默认推荐：

| 时间点 | 类型 | 交付 |
|--------|------|------|
| W+1 | Quick Read | 24h 内短报，找完全没预测到的高频 prompt |
| W+2 | Trend Check | 短报，识别 L3 候选 PAUSED |
| W+4 | Validation Report v1 | 完整报告，预测命中率 + 意外 Prompt 全量 |
| W+8 | Optimization Report v1 | 完整诊断 + Listing 字符级微调 |
| W+12 | Calibration Report | 长期方案 + ROI 测算 |

D+30/60/90 这种粗粒度已废弃，新生成的报告必须用周颗粒度 5 点位（W+1/2/4/8/12）。

### 6. Cross-model risk verification cadence

跨型号 SKU（如 v2 vs v1）的实际抢流量情况必须在 W+1 起就开始监控（不能等到 W+4）。Old SKU 的 brand-level prompt 早期抢量是<strong>最难逆转</strong>的——一旦 Rufus 学会把"brand X portable router"指向老 SKU，后续要花 4-8 周才能扭转。W+1 / W+2 短报必须明确包含跨型号实测项。
