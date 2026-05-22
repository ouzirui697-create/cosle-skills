---
name: listing-image-audit
description: >
  对 Amazon listing 的主图序列和 A+ 图片做 Rufus 视觉打分诊断。读取图片目录、用多模态视觉
  逐张评分（主图 6 维度 / A+ 5 维度）、识别重复 / 命名冲突 / Amazon 主图合规问题、输出包含
  缩略图预览的暗色 HTML 报告 + 可选 PDF。
  Use this skill whenever a seller asks for visual scoring of Amazon main images or A+ content,
  image audit, evaluating product image quality, identifying image duplication, or assessing
  whether visuals cover the differentiation points called out in a prelaunch-listing text report.
  触发词：「主图打分」「主图诊断」「主图评分」「A+ 图片诊断」「A+ 图片打分」「A+ 图片分析」
  「listing 视觉评分」「listing 视觉诊断」「图片审核」「图片报告」「主图重排建议」
  「A+ 补全路线图」「image audit」「evaluate main images」「score A+ content」
  「Amazon main image review」「listing visual report」。
  与 cosmo-report / prelaunch-listing 互补——这两个 skill 处理文字 listing（Title / Bullet /
  Backend），本 skill 专门处理视觉素材（主图序列 + A+ 模块图）。建议先用 prelaunch-listing
  做文字优化报告（识别 N 个独家差异化点），再用本 skill 评估图片是否充分覆盖这些差异化点。
  Do NOT use this skill for text-only listing optimization — use prelaunch-listing for that.
  Do NOT use this skill to evaluate product videos / Brand Store / Posts — those are separate.
---

# Listing Image Audit (主图 + A+ 打分诊断)

## What this skill does

对 Amazon 产品的<strong>主图序列（最多 9 张）+ A+ 图片模块</strong>做<strong>逐张视觉打分诊断</strong>。
输出一份单文件 HTML 报告（暗色紫色主题），可选导出 PDF。报告内容：

1. **执行摘要** — 总图数 / 主图均分 / A+ 均分 / 关键问题数
2. **评分方法论** — 主图 6 维度 / A+ 5 维度 / 4 级色阶
3. **主图整体诊断** — 角色分类 + 4 类结构性问题（重复 / 命名 / 合规 / 路径）
4. **逐张主图打分诊断**（核心 N 张评分卡）— 每张含缩略图 + 评分环 + 6 维度横条 + 4 类诊断 box
5. **A+ 整体诊断 + 已做 vs 计划缺口**
6. **逐张 A+ 打分诊断**（5 维度）
7. **主图序列重排建议**（N 张取 9，推荐 #1-9 排序 + 删除 / 降级理由）
8. **A+ 补全路线图**（对照上游差异化点，推荐缺失模块设计草案）
9. **图片 ↔ Listing 一致性矩阵**（独家差异化点 × Bullet × 主图 × A+ 三维度覆盖对照）
10. **D+30 / D+60 验证路径**（Amazon Ads Console 拉点击热图 + Brand Analytics）
11. **报告局限 + Footer**

---

## Skill 间协作关系

| Skill | 输入 | 输出 | 何时用 |
|-------|------|------|--------|
| `cosmo-report` | 真实 SP Prompts xlsx | 诊断性文字 listing 报告 | 已上架产品的广告数据诊断 |
| `prelaunch-listing` | Excel 模板 + 竞品 ASIN | 预测性文字 listing 报告 | 未上市产品的 Title / Bullet / Backend / A+ 文案优化 |
| <strong>`listing-image-audit`（本 skill）</strong> | <strong>主图目录 + A+ 图片目录</strong> | <strong>视觉打分诊断 HTML/PDF 报告</strong> | <strong>评估图片素材质量 / 主图序列 / A+ 视觉</strong> |

**推荐工作流**：先用 `prelaunch-listing` 做文字优化报告（其中会识别 N 个独家差异化点），
再用本 skill 评估图片是否充分视觉化这些差异化点。本 skill 的"差异化呈现"维度评分依赖
上游报告识别的差异化清单。

---

## 铁律（必读 · 不可违反）

1. **必须读完所有图片**：用 Read 工具逐张读（Read 支持图片，是 multimodal）。<strong>不能凭文件名编内容</strong>。即使图很多（>15 张）也要全读完。
2. **零编造**：所有诊断只引用<strong>实际看到的视觉元素</strong>（"屏幕显示 11:40"是因为图中确实显示，不是猜测）。
3. **重复检测必须给证据**：声明"主图 A 与 A+ B 重复"时，必须列出两者重复的具体维度（同样 9 宫格 / 同样数字 / 仅排版差异），不能空口断言。
4. **独家差异化引用上游**：如果用户有上游 `prelaunch-listing` 文字报告，本 skill 的"差异化呈现"维度必须引用其中识别的 N 个独家差异化点作为评分基准，<strong>不重新自己定义</strong>。
5. **路径校验**：HTML 写完后<strong>必须用脚本验证所有 `<img src>` 路径文件确实存在</strong>（参见 §Workflow Step 9 末尾）。
6. **文件名 URL 编码**：主图文件名含空格 / 特殊字符时，`<img src>` 必须做 URL 编码（空格 → `%20`），否则浏览器加载破图。
7. **SVG 评分环必须叠加中央数字 div**：纯 SVG 不显示中央数字。模板见 `references/report_design.md`。
8. **主图与 A+ 图命名全程区分（HARD RULE）**：报告正文、诊断 box、交叉引用、矩阵表格、HTML 卡片标题，凡引用图片必须带类型前缀：
   - 主图序列统一用：`主图 #1`、`主图 #2` … `主图 #9`
   - A+ 图片统一用：`A+ 图 #1`、`A+ 图 #2`（或 `A+ 模块 #1`）
   - ❌ 禁止裸写 `#1`、`Image #1`、`图片 #1`、仅文件名——这些表达在主图与 A+ 混排后无法区分指向
   - 跨层引用时必须两者都写全：`主图 #5（9宫格）与 A+ 图 #2 内容重复，建议删除其中一张`

---

## Workflow

### Step 0 — Gather Inputs

| Input | 必需 / 可选 | 内容 |
|-------|-------------|------|
| 1. 主图目录路径 | 必需 | 通常含 ≤ 9 张（Amazon 上限），可能含 10-15 张候选 |
| 2. A+ 图片目录路径 | 必需（可为空） | 通常 0-10 张；不完整时本 skill 给出补全建议 |
| 3. 上游 prelaunch-listing 报告 | 可选但强烈推荐 | HTML 或 Markdown，提取 N 个独家差异化点 |
| 4. 卖家自填的 Excel 输入模板 | 可选 | 含产品 spec / Tier 用户表 / 竞品列表，用于场景代入感评分 |

如果用户没提供路径，向用户索取（参考"主图打分"或"A+ 诊断"触发场景）。

### Step 1 — Read All Images (multimodal 必需)

```
# 用 Read 工具逐张读图（Read 支持 jpg/png/webp/jpeg）
Read /path/to/main_images/主图-01.jpg
Read /path/to/main_images/主图-02.png
... (全部读完)
Read /path/to/a_plus_images/1-KV.jpg
... (全部读完)
```

并行调用多个 Read 可以加速。读图后内容会以多模态形式呈现在上下文中。

### Step 2 — 按角色分类主图

把所有主图按角色归类（适用于 Amazon 通用品类，根据具体产品可能有变体）：

| 角色 | 典型特征 |
|------|----------|
| 白底主图 #1 候选 | 纯白底 / 产品 3/4 主视图 / 无文字道具 / Amazon 主图 #1 政策强制要求 |
| 副角度 / 正反对应 | 产品其他角度（背面 / 俯视 / 立面） |
| 尺寸 / 接口标注图 | 深色底 + 产品悬浮 + 标注三维尺寸 + 各接口名 |
| 9 宫格特性总览 | 3×3 等分九宫 / 4×2 行布局 / 集中呈现核心 spec + 数字 |
| 概念图 | 卖点抽象视觉化（连接 / 速度 / 全球覆盖） |
| 场景图 | 真实人物 / 环境 / lifestyle（Tier 1-3 用户对应） |
| Inside the Box 包装清单 | 白底 + 包装内所有附件展示 + "1 x" 数量标注 |
| 技术性图（频段表 / spec 表） | 表格 / 爆炸图 / 频段列表 |

### Step 3 — 检测 4 类结构性问题

逐图扫描后，必须显式列出以下 4 类问题（即使 0 个也要说"未发现"）：

1. **主图间内容重复**：是否有两张主图角度 / 屏幕显示 / 文字标注几乎完全一样？
2. **主图与 A+ 内容重复**：是否有 A+ 模块的信息与某张主图<strong>近乎完全一致</strong>（典型：9 宫格特性总览同时出现在主图和 A+）？引用时必须用带前缀的全称，例如"主图 #5（9宫格）与 A+ 图 #2 内容重复"，不得只写 "#5 与 #2 重复"。
3. **文件命名冲突**：是否有多个文件以同一编号开头（如 `主图-09.jpg` + `9.-NA frequency band.jpg`）？
4. **白底主图合规性**：主图 #1 候选的背景是否真的接近 RGB 255/255/255？是否有不应出现的灰底 / 渐变 / 阴影？

### Step 4 — 主图 6 维度评分（每张图）

详见 `references/scoring_rubric.md`。摘要：

| 维度 | 权重 |
|------|------|
| Amazon 主图政策合规度 | 25% |
| Rufus 多模态视觉典型性 | 25% |
| 视觉清晰度 & 信息层级 | 20% |
| 差异化卖点呈现 | 15% |
| 场景 / 人群代入感 | 10% |
| 品牌一致性 | 5% |

每张图必须给出<strong>具体分数 + 该分数的理由</strong>（不是泛泛"看起来不错"）。重复 / 命名冲突 / 不合规等问题直接扣 8-15 分。

### Step 5 — A+ 5 维度评分（每张图）

详见 `references/scoring_rubric.md`。摘要：

| 维度 | 权重 |
|------|------|
| 信息层级 & 版式 | 25% |
| Rufus 抓取友好度（OCR + 视觉） | 25% |
| 文字密度 & 移动端可读性 | 20% |
| 场景连贯性 & Tagline 一致性 | 15% |
| 品牌一致性 & 设计质感 | 15% |

A+ 评分特别注意"是否与主图重复" —— 如果重复，<strong>扣 10-15 分</strong>并明确写在"⚠ 关键问题"中。

### Step 6 — 主图序列重排建议

把<strong>所有主图（即使 13 张 / 15 张）按角色重排为推荐的 Amazon 主图 #1-#9 序列</strong>。
逻辑：白底主图 → 副角度 / 正反对应 → 尺寸 / 接口图 → 9 宫格功能总览 → 独家差异化（VPN / 触屏 / 电池） → 场景图 → Inside the Box。

输出格式：

```
| 新位置 | 使用的图 | 角色 | 关键 prompt 命中 |
| #1 | 主图-01.jpg | 白底 3/4 主图 | ... |
| #2 | 主图-11.jpg | 白底背面图 | ... |
| ... |
| 删除 | 主图-10.jpg | 与主图-01 重复 | n/a |
| 降级 | 主图-05.jpg | 移到 A+ 模块 / listing 详情 | n/a |
| 重命名 | 9.-NA frequency band.jpg → 辅图-NA频段表.jpg | 不进主图序列 | n/a |
```

### Step 7 — A+ 补全路线图

对照上游 `prelaunch-listing` 报告的独家差异化点（如果有），<strong>识别哪些差异化点在已做 A+ 模块中未充分体现</strong>。
为每个缺口给出<strong>设计草案</strong>：

- **主标题** + **副文案**
- **视觉布局描述**（左右双栏 / 4 列方格 / 网络拓扑图 等）
- **命中的 L1/L2 Prompt** 编号
- **数字 / 关键词清单**

典型 A+ 补全模块（按上游差异化点反推，每个产品具体不同）：
- 独家差异化 #1 单点放大图
- Tier 1 / Tier 2 / Tier 3 场景模块
- "What's New vs 上一代" 升级对照
- vs 主要竞品 4 列对比表
- Brand Story（化解 L3 brand-level prompt）

### Step 8 — 图片 ↔ Listing 一致性矩阵

构造矩阵：

| 独家差异化点 | Bullet 覆盖 | 主图覆盖 | A+ 覆盖 | 一致性诊断 |
|---|---|---|---|---|
| 点 1 | ✓ Bullet N | ✓ 主图-X | ✓ A+ N | ✓ 三处一致 |
| 点 2 | ✓ Bullet N | ✗ 0 张 | ✗ 0 张 | 🔴 Bullet 独家但完全没视觉化 |
| ... | | | | |

输出"必须补 X 个 mismatch"清单，明确指向 §Step 7 的具体设计草案。

### Step 9 — 写 HTML 报告

设计系统：紫色 IMAGE-AUDIT 主题（详见 `references/report_design.md`）。
关键技术点：

- 每张图嵌入缩略图预览（`<img src="..." style="max-width:300px"/>`，相对路径）
- SVG 评分环必须用 `position:relative` 包裹 + absolute 居中分数 div（纯 SVG 不显示数字）
- 4 类诊断 box 用图标区分：🔍 借鉴自 / 🚀 差异化 / ⚠ 必改 / 📝 In-place 建议
- @media print CSS（page-break-inside:avoid / @page A4 / print-color-adjust:exact）

输出文件命名约定：`[Brand]_[Product]_主图+A+打分诊断报告_v[N].0.html`

**写完后必须验证**（直接 Bash 执行）：

```bash
python3 -c "
import re, os
with open('[output.html]', 'r', encoding='utf-8') as f: s = f.read()
imgs = re.findall(r'<img src=\"([^\"]+)\"', s)
base = os.path.dirname('[output.html]')
for img in imgs:
    decoded = img.replace('%20', ' ')
    full = os.path.join(base, decoded)
    print(('✓' if os.path.exists(full) else '✗'), img)
"
```

如有 ✗，必须修正路径或文件名 URL 编码。

### Step 10 (可选) — 导出 PDF

仅当用户明确要求 PDF 时执行。详见 `references/pdf_export.md`。
要点：必须在 HTML 加 print CSS（`-webkit-print-color-adjust:exact` 等），否则 Chrome 默认会把暗色背景变白 + 把卡片切断到两页。

---

## Image Card 标准 HTML 模板（实施时直接 copy）

```html
<div class="image-card">
  <div>
    <div class="img-wrap"><img src="[相对路径，注意 URL 编码]" alt="[文件名]"/></div>
    <!-- img-meta 必须写明类型前缀：主图 #N 或 A+ 图 #N，不能只写文件名 -->
    <div class="img-meta">[主图 #N | A+ 图 #N] · [文件名] · [文件大小]</div>
  </div>
  <div>
    <!-- h3 必须以 "主图 #N —" 或 "A+ 图 #N —" 开头，区分层级 -->
    <h3>[主图 #N | A+ 图 #N] — [文件名] · [角色描述]</h3>
    <div class="role">[等级标签] · 总分 [N] [Critical/Needs Work/Good/Excellent]</div>
    <div class="score-ring-wrap">
      <div style="position:relative;width:80px;height:80px;flex-shrink:0">
        <svg width="80" height="80" viewBox="0 0 80 80" style="transform:rotate(-90deg)">
          <circle cx="40" cy="40" r="33" fill="none" stroke="#181c24" stroke-width="7"/>
          <circle cx="40" cy="40" r="33" fill="none" stroke="[#color]" stroke-width="7"
            stroke-linecap="round" stroke-dasharray="207.3"
            stroke-dashoffset="[207.3 * (1 - score/100)]"/>
        </svg>
        <div style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;
                    align-items:center;justify-content:center;font-family:'Syne',sans-serif;
                    font-size:22px;font-weight:800;color:[#color]">[N]</div>
      </div>
      <div style="flex:1">
        <!-- 6 / 5 维度横条评分 -->
        <div class="dim-bar">
          <div class="dim-bar-head">
            <span>[维度名]（[权重]%）</span><strong style="color:[#color]">[分]</strong>
          </div>
          <div class="dim-bar-fill"><div style="width:[分]%;background:[#color]"></div></div>
        </div>
        <!-- ... 重复其他维度 -->
      </div>
    </div>
    <div class="diag-box diag-borrow"><strong>🔍 做得好的地方</strong> [具体引用图中视觉元素，不空话]</div>
    <div class="diag-box diag-diff"><strong>🚀 差异化机会</strong> [点名 1-2 个竞品的相似呈现或空白]</div>
    <div class="diag-box diag-warn"><strong>⚠ 关键问题</strong> [Amazon 合规 / 重复 / 命名冲突等必改项]</div>
    <div class="diag-box diag-fix"><strong>📝 In-place 优化建议</strong> [不改图本身，给出文字 overlay / 重命名 / 重排建议]</div>
  </div>
</div>
```

颜色对应分数级别：
- 0-40 → `#e63946` 🔴 Critical
- 41-60 → `#f4a261` 🟡 Needs Work
- 61-80 → `#2ec4b6` 🟢 Good
- 81-100 → `#c77dff` ✨ Excellent

---

## Output

保存到与图片目录相对路径合理的位置（推荐与图片目录同层）。
文件命名：`[Brand]_[Product]_主图+A+打分诊断报告_v[N].0.html`

告诉用户：「报告已生成。直接用浏览器打开（图片会通过相对路径加载）。如需 PDF 版本，告诉我一声。」

---

## Brand Profiles

在开始图片审核前，**先识别品牌**。若品牌匹配下方档案，在通用评分规则之上叠加品牌特有规范。品牌规范覆盖通用格式检查，但永远不豁免真正的质量问题。

### GL.iNet (GL Technologies)

**触发条件**：品牌为 GL.iNet，或产品名含 Mudi / Beryl / Slate / Brume / Opal / Flint / Spitz / Convexa，或图片文件名含 `MP1`–`MP9` 前缀，或用户明确说明是 GL.iNet 产品。

---

#### 主图命名规范

GL.iNet 内部用 `MPX` 作为图片编号代码（MP1–MP9），对应 Amazon 主图 #1–#9 的上传位置。在报告中引用时，同时写出两套编号：

```
主图 #1（GL: MP1）— 陰影白底正面圖
主图 #2（GL: MP2）— Touchscreen
...
```

---

#### 主图序列参考（E5800 及同代产品标准结构）

| Amazon 位置 | GL 代码 | 图片类型 | 关键评分注意 |
|------------|---------|---------|------------|
| 主图 #1 | MP1 | 陰影白底正面圖 | ⚠️ 见下方"MP1 白底例外"说明 |
| 主图 #2 | MP2 | Touchscreen UI 演示 | 触屏操作界面实拍 |
| 主图 #3 | MP3 | VPN Speed | 速率数字 + 服务商品牌 |
| 主图 #4 | MP4 | Stay Connected / 多路 WAN | 连接可靠性卖点 |
| 主图 #5 | MP5 | Battery | 续航时长 + 充电速率 |
| 主图 #6 | MP6 | Scenario / 使用场景 | 真实人物 / 旅行环境 |
| 主图 #7 | MP8 | 尺寸細節圖（接口标注） | **注意：MP8 在 MP7 之前上传** |
| 主图 #8 | MP7 | Frequency Band（频段表） | **地区分版，见下方说明** |
| 主图 #9 | MP9 | Inside the Box | 附件清单 |

---

#### ⚠️ MP1 白底例外（禁止误判为合规问题）

GL.iNet MP1 使用**带轻微阴影的白底版本**，而非 RGB 255/255/255 纯白底。这是 GL.iNet 的**主动品牌决策**（上传带阴影版本），不是合规失误。

- ❌ 不得写"MP1 背景非纯白，不符合 Amazon 主图政策"
- ✅ 应写"MP1 使用品牌惯例阴影白底，符合 GL.iNet 设计规范；若 Amazon 审核要求纯白，建议备一张纯白版本"

---

#### ⚠️ MP7 地区分版（禁止误判为重复或命名冲突）

GL.iNet 的频段图（MP7）按地区分为 NA 版和 EU 版，各自上传到对应站点。这是**合理的地区合规分版**，不是重复图片。

- ❌ 不得写"频段图出现两个版本，内容重复，建议删除一张"
- ✅ 应写"MP7 NA/EU 分版符合 GL.iNet 地区合规规范；确认 NA 版已上传美国站，EU 版已上传欧洲站"

---

#### ⚠️ MP 编号与上传顺序不一致（禁止误判为顺序错误）

GL.iNet 的内部代号 MP8（尺寸细节图）**上传位置排在 MP7（频段图）之前**（即 Amazon 主图 #7 = GL-MP8，Amazon 主图 #8 = GL-MP7）。这是 GL 的编排决策，不是顺序错误。诊断主图序列时以实际上传顺序为准，不以 MP 数字编号大小排序。

---

#### A+ 模块结构参考

GL.iNet A+ 采用模块编号系统，含子模块后缀（5a/5b、6a/6b 为滑动模组）。报告中引用 A+ 图时必须带模块编号：

| 模块编号 | 类型 | 说明 |
|---------|------|------|
| A+ 模块 1 | 封面 + Teaser Video | 产品大图 + 视频入口 |
| A+ 模块 2 | New Release 推荐位 | E5800 置于第一位（替换旧款） |
| A+ 模块 3–4 | 内容模块 | 产品专属差异化内容 |
| A+ 模块 5a / 5b | 滑动模组（carousel） | 两张图组成一个滑动单元 |
| A+ 模块 6a / 6b | 滑动模组（carousel） | 同上 |
| A+ 模块 7 | Headline 文字模块 | 固定 Tagline："Your Connectivity Companion On the Move" |
| Brand Story | 独立深色区块 | 与主 A+ 模块分离，单独更新 |

**Brand Story 评分注意**：Brand Story 是独立模块，不算在 A+ 模块计数内，需单独列一栏评分。

---

#### GL.iNet 审图禁止事项汇总

| 禁止 | 正确处理 |
|------|---------|
| ❌ 把 MP1 阴影白底判为不合规 | ✅ 注明品牌惯例，建议备纯白版 |
| ❌ 把 MP7 NA/EU 两版判为重复 | ✅ 确认地区分发是否正确 |
| ❌ 按 MP 数字大小排序判顺序对错 | ✅ 按实际上传顺序评估序列逻辑 |
| ❌ 把 5a/5b 当两张独立图评重复 | ✅ 识别为滑动模组组合，整体评分 |
| ❌ Brand Story 漏评或混入 A+ 计数 | ✅ Brand Story 单独列栏评分 |

---

## Reference Files

- `references/scoring_rubric.md` — 主图 6 维度 / A+ 5 维度评分细则 + 锚点举例
- `references/amazon_image_policy.md` — Amazon 主图政策摘要 + 副图自由度 + A+ 模块尺寸
- `references/report_design.md` — 紫色 IMAGE-AUDIT 主题 HTML 设计系统 + image-card 卡片样式 + SVG ring 模板 + print CSS
- `references/pdf_export.md` — Chrome headless PDF 导出命令 + 兼容方案
