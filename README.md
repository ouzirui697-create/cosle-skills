<div align="center">

# Cosle Skills

**Amazon Listing × Rufus 优化工具集 · 三个 Claude Code Skill**

文字 · 预测 · 视觉 — 覆盖 Amazon 卖家从<strong>新品上市前</strong>到<strong>已上架优化</strong>的完整 Rufus 友好度闭环。

[![Skills](https://img.shields.io/badge/Claude_Code_Skills-3-c77dff)](https://docs.claude.com/en/docs/claude-code)
[![License](https://img.shields.io/badge/license-MIT-2ec4b6)](LICENSE)
[![COSMO Method](https://img.shields.io/badge/methodology-COSMO_15_relations-4cc9f0)](https://www.amazon.science/publications/cosmo)

</div>

---

## 为什么需要这套工具

Amazon Rufus 上线后，<strong>"Listing 怎么写"已经从 SEO 关键词游戏变成了 AI 友好度博弈</strong>。Rufus 是 multimodal LLM，它会：

- 读你的 Title / Bullet / Backend → 决定要不要把你的产品<strong>呈现给问 X 的买家</strong>
- 读你的主图 / A+ 图片 → 决定<strong>买家点进来后多久流失</strong>
- 拿你的 SP Prompts 实测数据 → 反馈给亚马逊的 ranking 算法

但卖家在三个阶段都缺工具：

| 阶段 | 痛点 | Cosle 解决方案 |
|------|------|---------------|
| ① 新品上市前 | 没有广告数据，不知道 Rufus 会怎么问 | **prelaunch-listing** — 用竞品代理 + COSMO 框架预测 Prompt 宇宙 |
| ② 视觉素材审查 | 主图重复 / A+ 模块和主图打架 / 不知道是否合规 | **listing-image-audit** — 多模态视觉打分 + Amazon 政策对照 |
| ③ 上架后诊断 | SP Prompts 数据看不懂 / 不知道哪些该关 | **cosmo-report** — 用 COSMO 15 关系框架做 L1/L2/L3 分级诊断 |

---

## 三 Skill 闭环

```
   ┌───────────────────────┐                ┌───────────────────────┐
   │   产品 spec + 竞品     │                │   主图 + A+ 图片目录   │
   │       ↓                │                │       ↓                │
   │  prelaunch-listing    │ ── 识别 N 个 ──→│  listing-image-audit  │
   │  （文字 listing）      │   独家差异化点    │  （视觉打分诊断）       │
   │       ↓                │                │       ↓                │
   │  ✍ Title / Bullets /   │                │  📸 主图 6 维度评分    │
   │     A+ / Backend       │                │  🎨 A+ 5 维度评分      │
   │  📊 预测 Prompt 宇宙   │                │  🔀 主图重排建议       │
   └───────────┬───────────┘                └───────────┬───────────┘
               │                                         │
               ↓     ━━━━━━ 产品上市（W+0） ━━━━━━     ↓
                              │
                              ↓
               ┌──────────────────────────────┐
               │   真实 SP Prompts xlsx        │
               │   （W+1 / W+2 / W+4 / W+8 / W+12）│
               │              ↓                │
               │       cosmo-report           │
               │       （真实诊断）             │
               │              ↓                │
               │  🎯 L1 加码 / L3 关闭清单      │
               │  📈 Rufus 友好度真实分        │
               │  ✏ 字符级 Listing 微调建议     │
               └──────────────────────────────┘
```

---

## 三个 Skill 概览

### 1. `prelaunch-listing` · 新品文字 Listing 预测报告

> 没上架的新品也能写出 Rufus 友好的 listing — 用竞品做代理 + COSMO 框架推演。

**输入**：产品 spec（参数 / USP / 人群 / 价格）+ 3-5 个竞品 ASIN
**输出**：单文件 HTML 报告，含：
- 📊 **Predicted Prompt Universe** —— 30-50 条预测 Prompt，按 L1/L2/L3 分级
- 🎯 **Competitor Benchmark** —— 竞品在每条 Prompt 上的覆盖度热图
- ✍ **Generated Listing** —— Title / 5-7 Bullets / A+ 大纲 / Backend Keywords
- 💯 **Predicted Rufus Friendliness Score** —— 5 维度评分（明确标注 PREDICTED）
- ⚠ **Cross-Model Substitution Risk** —— 同品牌 SKU 互相抢量分析
- 🔁 **验证路线图** —— W+1 / W+2 / W+4 / W+8 / W+12 周颗粒度

**典型触发词**："新品 listing"、"上市前 listing"、"pre-launch listing"、"新产品 COSMO 报告"

### 2. `listing-image-audit` · 主图 + A+ 视觉打分诊断

> 13 张主图 / 10 张 A+ 一张一张打分。Amazon 政策对照 / 重复检测 / 视觉化覆盖差异化点。

**输入**：主图目录 + A+ 图片目录（可选 + 上游 prelaunch-listing 报告）
**输出**：单文件 HTML 报告 + 可选 PDF（A4 暗色主题），含：
- 📸 **每张图独立评分卡** —— 缩略图 + 6/5 维度评分 ring + 4 类诊断 box（🔍 借鉴 / 🚀 差异化 / ⚠ 必改 / 📝 优化建议）
- 🔀 **主图序列重排建议** —— N 张取 9，给出推荐 #1-#9 排序
- 📝 **A+ 补全路线图** —— 缺失模块的设计草案（含主标题 / 副文案 / 视觉布局）
- 🔗 **图片 ↔ Listing 一致性矩阵** —— 找"Bullet 提到但图没画"的 mismatch
- 🛡 **Amazon 主图政策合规** —— 白底 RGB / 占比 / 像素 / 文字禁令逐项核查

**典型触发词**："主图打分"、"A+ 图片诊断"、"listing 视觉评分"、"image audit"

**评分维度**：

| 主图（6 维度） | 权重 | A+ 图片（5 维度） | 权重 |
|------|------|------|------|
| Amazon 主图政策合规度 | 25% | 信息层级 & 版式 | 25% |
| Rufus 多模态视觉典型性 | 25% | Rufus 抓取友好度（OCR + 视觉）| 25% |
| 视觉清晰度 & 信息层级 | 20% | 文字密度 & 移动端可读性 | 20% |
| 差异化卖点呈现 | 15% | 场景连贯性 & Tagline 一致性 | 15% |
| 场景 / 人群代入感 | 10% | 品牌一致性 & 设计质感 | 15% |
| 品牌一致性 | 5% | | |

### 3. `cosmo-report` · 已上架产品 SP Prompts 诊断

> 拿到 SP Prompts xlsx 数据后的真实诊断。L3 关闭清单 + L1 加码清单 + 字符级 Listing 微调。

**输入**：Amazon Ads Console 导出的 SP Prompts xlsx（真实广告数据）
**输出**：单文件 HTML 报告，含：
- 🔬 **COSMO 分析** —— 每条 Prompt 按 L1/L2/L3 分级 + 转化贡献 + 跨型号替代检测
- 💯 **Rufus 友好度真实分** —— 5 维度评分（不再是预测，是真实）
- 🚫 **L3 关闭清单** —— 实测无转化的低典型性 Prompt + 预估省下的广告费
- 📈 **L1 加码清单** —— 真实有转化的 Prompt 建议 +20-30% bid
- ✏ **Listing 字符级微调** —— 基于真实 mismatch 给出精确修改建议
- 🎯 **Ad Action Plan** —— 优先级排序的下一步动作清单

**典型触发词**："帮我分析广告报告"、"做一份 COSMO 报告"、"SP Prompts 分析"、"Rufus 广告优化"

---

## 安装

三个 skill 都是标准 Claude Code Skill 格式，可全局或项目级别安装。

### 全局安装（推荐 · 所有项目都可用）

```bash
git clone https://github.com/ouzirui697-create/cosle-skills.git
cd cosle-skills

# 复制到 ~/.claude/skills/
mkdir -p ~/.claude/skills/cosmo-report
mkdir -p ~/.claude/skills/prelaunch-listing
mkdir -p ~/.claude/skills/listing-image-audit

cp -r cosmo-report/* ~/.claude/skills/cosmo-report/
cp -r prelaunch-listing/* ~/.claude/skills/prelaunch-listing/
cp -r listing-image-audit/* ~/.claude/skills/listing-image-audit/
```

### 项目级安装（仅本项目可用）

```bash
mkdir -p your-project/.claude/skills
cp -r cosle-skills/cosmo-report your-project/.claude/skills/
cp -r cosle-skills/prelaunch-listing your-project/.claude/skills/
cp -r cosle-skills/listing-image-audit your-project/.claude/skills/
```

### 验证安装

```bash
ls ~/.claude/skills/cosmo-report/
ls ~/.claude/skills/prelaunch-listing/
ls ~/.claude/skills/listing-image-audit/
```

每个 skill 目录应该包含 `SKILL.md` + `references/` 子目录。安装后在 Claude Code 中输入 `/<skill-name>` 或用自然语言触发词即可激活。

---

## 完整工作流示例（Mudi 7 为例）

### W-30（上市前 4 周）· 用 `prelaunch-listing` 生成文字 listing

```
我要给 GL.iNet Mudi 7 (GL-E5800) 做一份新品 listing 预测报告。
产品：5G NR Tri-band Wi-Fi 7 Travel Router
价格：$419.99 USD（正式价，预售期 $369.99）
竞品：B0G4XP7JMR, B0F2B6NHSL, B0FQDMQXRW, B0C6XVCM6L
```

→ 输出：<strong>预测 Rufus 友好度 78 分</strong>（应用本报告优化后预估升至 86）+ 9 个独家差异化点 + 7 条 Bullet 优化版 + Backend Keywords。

### W-15（上市前 2 周）· 用 `listing-image-audit` 审查图片素材

```
帮我对 13 张主图和 3 张 A+ 图片做视觉打分诊断。
图片目录：./E5800/E5800主图/ + ./E5800/B5800A+图片/
请对照上一步 prelaunch-listing 报告的 9 个独家差异化点做覆盖度检查。
```

→ 输出：<strong>主图均分 79 / A+ 均分 84</strong> + 4 类结构性问题（主图-04 与 A+ 2-highlight 重复 / 主图-01 与主图-10 角度重复 / 9 号文件命名冲突 / 9 项独家差异化在视觉中的覆盖率）+ 主图 #1-#9 重排建议 + 7 张 A+ 补全模块设计草案。

### W+0 ~ W+12（上市后周颗粒度验证）· 用 `cosmo-report` 做真实诊断

```
我的 Mudi 7 已经上架 4 周了，这是 SP Prompts xlsx 数据。
请帮我做完整的 COSMO 诊断报告。
```

→ 输出：<strong>预测命中率（v0 的 46 条预测中实际触发 N 条）</strong>+ 意外 Prompt 全量 + L3 关闭清单（预估省 $X/月） + L1 加码清单（预估提 +N% 转化） + 字符级 Listing 微调建议 + Rufus 友好度真实分（替代预测分）。

---

## 设计原则（三 Skill 通用）

### 🎨 暗色主题设计系统

三个 skill 输出 HTML 报告共享一套设计系统，主色按场景区分：

| Skill | 主色 | 视觉语义 |
|-------|------|----------|
| cosmo-report | <span style="color:#e63946">●</span> 红 `#e63946` | 诊断（哪里有问题） |
| prelaunch-listing | <span style="color:#f4a261">●</span> 橙 `#f4a261` | 预测（待 W+1 起验证） |
| listing-image-audit | <span style="color:#c77dff">●</span> 紫 `#c77dff` | 视觉审查 |

通用字体：`Syne`（标题）/ `DM Mono`（数据）/ `Noto Sans SC`（正文）

### 🔬 COSMO 15 关系框架

prelaunch-listing 和 cosmo-report 共用 [Yu et al. (2024). COSMO](https://www.amazon.science/publications/cosmo) 论文的 15 关系类型，把 Prompt 按典型性分为三级：

- **L1 高典型性**（`capable_of` / `used_for_func` / `used_to` / `xWant`）— 占 75% 真实购买转化
- **L2 中典型性**（`used_for_aud` / `used_for_eve` / `used_in_loc` / `used_with` / `used_by`）— 场景类
- **L3 低典型性**（`is_a` / `xInterested_in`）— 品牌泛化，建议 PAUSED

### ⚡ 周颗粒度验证（v2.0+）

D+30 / D+60 / D+90 月颗粒度太粗，错过 W+1 / W+2 的"意外 Prompt"早期信号。新版本默认推荐：

| 时间点 | 类型 | 交付 |
|--------|------|------|
| W+1 | Quick Read | 24h 内短报，找完全没预测到的高频 Prompt |
| W+2 | Trend Check | 短报，识别 L3 候选 PAUSED |
| W+4 | Validation Report v1 | 完整报告，预测命中率 + 意外 Prompt 全量 |
| W+8 | Optimization Report v1 | 完整诊断 + Listing 字符级微调 |
| W+12 | Calibration Report | 长期方案 + ROI 测算 |

---

## 内置经验教训（从真实卖家反馈沉淀）

`prelaunch-listing` skill 内置了 6 条来自真实卖家评审循环的经验教训，未来生成报告会自动避开这些坑：

1. **SIM 硬件描述真实性 > 营销简化**：eSIM + Dual Nano-SIM 路由器中，eSIM 启用通常占一个物理槽位，不能说"3 槽同时活跃"。
2. **数字可证伪原则**：避免"140+ countries"等不可验证的具体数字，改用"global carriers"模糊化。
3. **避免绝对化措辞**："No App, No Admin Panel" 等绝对化卖点容易被解读为"完全不需要"，软化为"日常任务不需要"+ 明示高级功能仍依赖软件。
4. **预售价 vs 正式价**：Comparison Chart 必须用正式价做锚点，预售价单独标注。
5. **周颗粒度验证**：W+1 / W+2 短报抓"意外 Prompt"，比 D+30 月颗粒度有效得多。
6. **跨型号风险监控**：W+1 起就监控老 SKU 抢量，不能等到 W+4。

详见各 skill 的 `SKILL.md` 末尾的 "Lessons learned" 章节。

---

## 项目结构

```
cosle-skills/
├── README.md                          # 本文件
├── LICENSE
│
├── cosmo-report/                      # Skill 1 · 真实数据诊断
│   ├── SKILL.md
│   └── references/
│       ├── cosmo_framework.md         # COSMO 15 关系详细定义
│       └── report_design.md           # 红色诊断主题 HTML 设计系统
│
├── prelaunch-listing/                 # Skill 2 · 预测性文字报告
│   ├── SKILL.md                       # 含 Lessons learned 6 条
│   └── references/
│       ├── cosmo_framework.md         # （与 cosmo-report 共用）
│       └── report_design.md           # 橙色预测主题
│
├── listing-image-audit/               # Skill 3 · 视觉打分诊断
│   ├── SKILL.md
│   └── references/
│       ├── scoring_rubric.md          # 主图 6 维度 / A+ 5 维度评分锚点
│       ├── amazon_image_policy.md     # Amazon 主图政策摘要
│       ├── report_design.md           # 紫色 IMAGE-AUDIT 主题
│       └── pdf_export.md              # Chrome headless PDF 导出指南
│
└── examples/                          # 真实案例（脱敏）
    ├── mudi7-prelaunch-v2.html        # Mudi 7 prelaunch-listing 报告样本
    └── mudi7-image-audit-v1.html      # Mudi 7 listing-image-audit 报告样本
```

---

## 常见问题

### Q：必须三个 skill 都装吗？

不必。每个 skill 都可独立使用：
- 只有 SP Prompts 数据 → 装 `cosmo-report`
- 新品要写 listing → 装 `prelaunch-listing`
- 只想审查图片 → 装 `listing-image-audit`

但<strong>三者协作</strong>时价值最大化（如 image-audit 引用 prelaunch-listing 识别的差异化点做覆盖检查）。

### Q：报告导出 PDF 怎么做？

`listing-image-audit` 的 PDF 导出已内置 Chrome headless 命令（见 `references/pdf_export.md`）。其他 skill 同理，但需在 HTML 加 print CSS（`page-break-inside:avoid` + `print-color-adjust:exact`）。

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf-no-header \
  --virtual-time-budget=15000 \
  --run-all-compositor-stages-before-draw \
  --print-to-pdf="$OUT.pdf" "file://$IN.html"
```

### Q：Rufus 模型每月更新，skill 也要每月改吗？

模型更新主要影响"具体 Prompt 形态"，但<strong>方法论框架（L1/L2/L3 + 15 关系）是稳定的</strong>。skill 本身不需要月度更新；只有发现新的真实卖家反馈坑点时才迭代 Lessons learned。

### Q：可以加 cosmo-report 之外的其他评分维度吗？

可以。每个 skill 的 `references/scoring_rubric.md`（或同等文件）都是可编辑的。自定义维度后，记得同步更新 `SKILL.md` 中的工作流描述。

### Q：支持哪些国家的 Amazon 站点？

主要针对 amazon.com（US）做了优化。UK / DE / JP 等站点的频段表、认证 logo、营销 tagline 需要按区域单独本地化（`listing-image-audit/references/amazon_image_policy.md` 有说明）。

---

## 方法论引用

本工具集的核心方法论来自：

- Yu et al. (2024). <em>COSMO: A Large-Scale E-commerce Common Sense Knowledge Generation and Serving System at Amazon</em>. SIGMOD-Companion '24.
- Amazon Rufus 公开技术博客与 product detail page 视觉规范

---

## 贡献

欢迎提 issue / PR：

- 🐛 Bug 修复（HTML 渲染 / 评分逻辑 / 触发词覆盖）
- 📐 新增评分维度（请在 PR 中说明数据支撑）
- 🎨 新增主题色 / 设计系统变体
- 🌍 多语言本地化（README 翻译 / SKILL.md 触发词扩展）

---

## License

MIT License — 详见 [LICENSE](LICENSE)

---

## 联系方式

- 📧 zouak@connect.ust.hk · Ray（Cosle Founder）
- 📧 zyuanay@connect.ust.hk · Jack（Cosle Co-Founder）
- 🏫 香港科技大学 AI 创业团队

<div align="center">

<strong>Built for Amazon sellers in the Rufus era · 由 Cosle 团队制作</strong>

</div>
