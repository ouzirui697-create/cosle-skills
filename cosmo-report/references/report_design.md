# Report Design System

The COSMO report uses a consistent dark-theme design system. This file defines the exact CSS variables, components, and layout patterns to use when generating the HTML report.

---

## Core Design Principles

- **Dark background** — #0a0b0d base, layered with #111318 and #181c24
- **Red accent** — #e63946 (Cosle brand color), used for urgency and emphasis
- **Teal accent** — #2ec4b6 (positive / green signals)
- **Typography** — DM Mono (data/code), Syne (headers), Noto Sans SC (body, supports Chinese)
- **Card-based layout** — all data sections inside bordered cards with subtle backgrounds
- **Priority color system**: 🔴 #e63946 | 🟡 #f4a261 / #ffd166 | 🟢 #2ec4b6 | ⚪ muted

---

## CSS Variables (always include in `<style>`)

```css
:root {
  --bg: #0a0b0d;
  --bg2: #111318;
  --bg3: #181c24;
  --card: #1a1f2b;
  --border: #252c3a;
  --red: #e63946;
  --orange: #f4a261;
  --yellow: #ffd166;
  --green: #2ec4b6;
  --blue: #4cc9f0;
  --purple: #c77dff;
  --text: #e8eaf0;
  --muted: #7b8299;
  --brand: #e63946;
}
```

## Font Loading

Always load these three fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
```

Usage:
- Section titles, score numbers → `font-family: 'Syne', sans-serif; font-weight: 800`
- Data, code snippets, ASIN numbers, metrics → `font-family: 'DM Mono', monospace`
- Body text, descriptions (Chinese + English) → `font-family: 'Noto Sans SC', sans-serif`

---

## Key Component Patterns

### Hero Header
```html
<div style="background:linear-gradient(135deg,#0d1117,#1a0a12,#0d1117); border-bottom:1px solid #2a1520; padding:60px 40px 50px; position:relative; overflow:hidden;">
  <!-- Red radial glow: position:absolute, top:-60px, right:-60px, 340px circle -->
  <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(230,57,70,0.12); border:1px solid rgba(230,57,70,0.3); border-radius:4px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:11px; color:#e63946; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:20px;">
    🔬 Cosle × COSMO 诊断报告 v1.0
  </div>
  <h1 style="font-family:'Syne',sans-serif; font-size:36px; font-weight:800;">
    [BRAND NAME]<br><span style="color:#e63946">Rufus × COSMO 优化报告</span>
  </h1>
  <!-- Meta row with: 品牌, 产品线, 数据期间, Prompt数, 报告日期 -->
</div>
```

### Score Ring (SVG)

**CRITICAL**: The wrapper `div` MUST have `position:relative`. Without it, the score number (`position:absolute`) won't center correctly — it will overflow or disappear inside a flex container.

Circumference formula: `2π × r = 2π × 33 ≈ 207.35`
Dash offset formula: `207.35 × (1 - SCORE/100)`

```html
<!-- CORRECT: position:relative on wrapper is mandatory -->
<div style="position:relative; width:80px; height:80px; flex-shrink:0;">
  <svg width="80" height="80" viewBox="0 0 80 80" style="transform:rotate(-90deg)">
    <circle cx="40" cy="40" r="33" fill="none" stroke="#181c24" stroke-width="7"/>
    <circle cx="40" cy="40" r="33" fill="none"
      stroke="[COLOR]" stroke-width="7" stroke-linecap="round"
      stroke-dasharray="207.3"
      stroke-dashoffset="[207.3 × (1 - SCORE/100)]"/>
  </svg>
  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
              font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:[COLOR]">
    [SCORE]
  </div>
</div>
```

Score ring color: red (`#e63946`) for < 40, orange (`#f4a261`) for 40–60, yellow (`#ffd166`) for 60–65, teal (`#2ec4b6`) for 65+.

For the **overall brand score ring** (larger, displayed prominently in the hero/stat area), use `width:90px; height:90px` and `font-size:28px`.

### Alert Boxes
```html
<!-- Red alert (urgent) -->
<div style="background:rgba(230,57,70,0.08); border:1px solid rgba(230,57,70,0.25); border-radius:8px; padding:14px 18px; margin-bottom:10px; display:flex; align-items:flex-start; gap:12px; font-size:13px;">
  <span style="font-size:16px; flex-shrink:0">🚨</span>
  <div><strong style="display:block; font-weight:700; margin-bottom:2px">Alert title</strong>Description text</div>
</div>

<!-- Orange alert (warning) -->
<!-- Use rgba(244,162,97,0.08) and rgba(244,162,97,0.25) -->

<!-- Yellow alert (info) -->
<!-- Use rgba(255,209,102,0.08) and rgba(255,209,102,0.25) -->

<!-- Green alert (positive) -->
<!-- Use rgba(46,196,182,0.08) and rgba(46,196,182,0.25) -->
```

### Tags/Badges
```html
<!-- L1 tag (green) -->
<span style="display:inline-flex; align-items:center; padding:2px 8px; border-radius:3px; font-family:'DM Mono',monospace; font-size:10px; font-weight:500; text-transform:uppercase; letter-spacing:0.5px; background:rgba(46,196,182,0.15); color:#2ec4b6; border:1px solid rgba(46,196,182,0.3); white-space:nowrap;">L1 capable_of</span>

<!-- L2 tag (yellow) -->
<!-- rgba(255,209,102,0.15), color:#ffd166, border rgba(255,209,102,0.3) -->

<!-- L3 tag (red) -->
<!-- rgba(230,57,70,0.15), color:#e63946, border rgba(230,57,70,0.3) -->

<!-- Priority badges -->
<span style="padding:3px 10px; border-radius:4px; font-family:'DM Mono',monospace; font-size:10px; font-weight:500; text-transform:uppercase; white-space:nowrap; background:rgba(230,57,70,0.2); color:#e63946; border:1px solid rgba(230,57,70,0.4);">🔴 URGENT</span>
```

### COSMO Analysis Table (11 columns)

The COSMO analysis table must include all sales data columns from the xlsx. Use color-coding for CPC and CTR to make high-cost / high-performance prompts immediately visible.

**11 columns (in order):**
`#` | `Prompt` | `产品` | `COSMO关系` | `层级` | `曝光` | `点击` | `CTR` | `花费` | `CPC` | `标记`

**Color rules for data cells:**
- CPC ≥ $5.00 → red `#e63946`
- CPC ≥ $3.00 → orange `#f4a261`
- CPC < $3.00 → default color
- CTR ≥ 10% → teal `#2ec4b6` (high engagement signal)

```html
<div style="overflow-x:auto; border-radius:10px; border:1px solid #252c3a;">
  <table style="width:100%; border-collapse:collapse; font-size:12px;">
    <thead>
      <tr style="background:#181c24;">
        <th style="font-family:'DM Mono',monospace; font-size:10px; text-transform:uppercase; letter-spacing:0.8px; color:#7b8299; padding:10px 14px; text-align:left; border-bottom:1px solid #252c3a; white-space:nowrap;">#</th>
        <th style="...">Prompt</th>
        <th style="...">产品</th>
        <th style="...">COSMO关系</th>
        <th style="...">层级</th>
        <th style="...">曝光</th>
        <th style="...">点击</th>
        <th style="...">CTR</th>
        <th style="...">花费</th>
        <th style="...">CPC</th>
        <th style="...">标记</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid rgba(37,44,58,0.5);">
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; color:#7b8299;">[N]</td>
        <td style="padding:10px 14px; font-size:12px;">[Prompt text]</td>
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; font-size:11px;">[Product]</td>
        <td style="padding:10px 14px;">[COSMO badge]</td>
        <td style="padding:10px 14px;">[L1/L2/L3 badge]</td>
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; text-align:right;">[impressions]</td>
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; text-align:right;">[clicks]</td>
        <!-- CTR ≥10% → color:#2ec4b6 -->
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; text-align:right; color:[CTR_COLOR];">[ctr%]</td>
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; text-align:right;">$[cost]</td>
        <!-- CPC ≥$5 → #e63946, ≥$3 → #f4a261 -->
        <td style="padding:10px 14px; font-family:'DM Mono',monospace; text-align:right; font-weight:700; color:[CPC_COLOR];">$[cpc]</td>
        <td style="padding:10px 14px;">[flags/badges]</td>
      </tr>
    </tbody>
  </table>
</div>
```

### V1→V2 Comparison Banner

Use this component when the seller has data from a previous reporting period. Place it after the stat row, before the health score section.

```html
<div style="background:linear-gradient(135deg,rgba(46,196,182,0.06),rgba(76,201,240,0.04));
            border:1px solid rgba(46,196,182,0.2); border-radius:12px; padding:20px 24px; margin-bottom:24px;">
  <div style="font-family:'DM Mono',monospace; font-size:10px; color:#2ec4b6;
              text-transform:uppercase; letter-spacing:1.5px; margin-bottom:10px;">
    📈 两期对比
  </div>
  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap; margin-bottom:16px;">
    <span style="font-size:13px; color:#7b8299;">第1期（[中文日期范围]）</span>
    <span style="font-size:18px; color:#4cc9f0;">→</span>
    <span style="font-size:13px; color:#e8eaf0; font-weight:600;">第2期（[中文日期范围]）</span>
  </div>
  <!-- Score change grid: one card per product with delta -->
  <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px;">
    <div style="background:rgba(46,196,182,0.08); border:1px solid rgba(46,196,182,0.2); border-radius:8px; padding:12px; text-align:center;">
      <div style="font-size:11px; color:#7b8299; margin-bottom:4px;">[Product]</div>
      <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:#2ec4b6;">
        [v1_score] → [v2_score]
      </div>
      <div style="font-size:11px; color:#2ec4b6; margin-top:2px;">▲ +[delta]</div>
    </div>
    <!-- Red delta for regressions: color:#e63946, ▼ prefix -->
  </div>
  <!-- Key mechanism callout -->
  <div style="margin-top:14px; font-size:12.5px; color:#a0c8c8; line-height:1.7; border-left:2px solid #2ec4b6; padding-left:12px;">
    <strong>典型改善机制：</strong>[Describe the specific COSMO fix that worked, e.g., "U8PRO Bullet 3 新增 capable_of + ADA 17.375" 精确规格 → Rufus 在 14 天内停止推荐竞品 iX7-MT"]
  </div>
</div>
```

**Date format rule**: All dates must be in Chinese format. Example: `3月10日–4月9日`, `2026年4月27日`. Never use `Mar 10–Apr 9` or any English month names.

### Complete Listing Reference Template (`<details>/<summary>`)

Use this collapsible pattern after each partial fix card. No JavaScript required.

```html
<details style="margin-bottom:14px;">
  <summary style="
    background:rgba(76,201,240,.06); border:1px solid rgba(76,201,240,.2);
    border-radius:10px; padding:14px 18px; cursor:pointer; list-style:none;
    display:flex; align-items:center; justify-content:space-between;
    font-size:13px; font-weight:600; color:#4cc9f0;
    font-family:'Syne',sans-serif;">
    <span>
      📄 <span style="background:rgba(76,201,240,.15); border:1px solid rgba(76,201,240,.3);
                      border-radius:4px; padding:2px 8px; font-size:11px; margin-right:8px;">[PRODUCT]</span>
      完整 Listing 参考模板 · 点击展开 ▼
    </span>
  </summary>

  <div style="background:#0c1018; border:1px solid rgba(76,201,240,.15);
              border-top:none; border-radius:0 0 10px 10px; padding:20px 24px;">

    <!-- COSMO Constraint Note -->
    <div style="background:rgba(230,57,70,.06); border:1px solid rgba(230,57,70,.2);
                border-radius:8px; padding:12px 16px; margin-bottom:20px;
                font-size:12px; color:#e8eaf0; line-height:1.7;">
      <strong style="color:#e63946;">⚠️ COSMO 约束说明：</strong>
      [Explain any critical rules, e.g., "G20 标题和所有 Bullet 中不得出现 MaP 字样——G20 无 MaP 认证，这是跨型号串扰的根本原因"]
    </div>

    <!-- TITLE SECTION -->
    <div style="margin-bottom:24px;">
      <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4cc9f0;
                  text-transform:uppercase; letter-spacing:1.2px; margin-bottom:10px;">
        🏷️ 优化标题
      </div>
      <code style="display:block; background:#0a0b0d; border:1px solid rgba(76,201,240,.2);
                   border-radius:8px; padding:14px 16px; font-family:'DM Mono',monospace;
                   font-size:12px; color:#e8eaf0; line-height:1.6; white-space:pre-wrap;">
[Complete optimized title here]
      </code>
      <div style="margin-top:8px; display:flex; gap:12px; font-size:11px; color:#7b8299;">
        <span>字符数：<strong style="color:#4cc9f0;">[N]/200</strong></span>
        <span>核心关键词密度：<strong style="color:#2ec4b6;">✓ 品牌 · 型号 · 功能 · 认证</strong></span>
      </div>
    </div>

    <!-- BULLETS SECTION -->
    <div style="margin-bottom:24px;">
      <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4cc9f0;
                  text-transform:uppercase; letter-spacing:1.2px; margin-bottom:10px;">
        📋 五点描述（COSMO capable_of 格式）
      </div>
      <!-- One card per bullet -->
      <div style="background:#111318; border:1px solid #252c3a; border-radius:8px;
                  padding:14px 16px; margin-bottom:8px;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
          <span style="font-family:'Syne',sans-serif; font-size:13px; font-weight:800;
                       color:#4cc9f0;">B[N]</span>
          <!-- COSMO relation badge -->
          <span style="background:rgba(46,196,182,.15); border:1px solid rgba(46,196,182,.3);
                       border-radius:3px; padding:2px 7px; font-family:'DM Mono',monospace;
                       font-size:9px; color:#2ec4b6; text-transform:uppercase;">capable_of</span>
          <!-- Typicality rating -->
          <span style="font-family:'DM Mono',monospace; font-size:10px; color:#ffd166;">
            典型性 ★★★★★
          </span>
        </div>
        <div style="font-size:12.5px; line-height:1.7; color:#e8eaf0;">
          [Bullet text in COSMO triple format]
        </div>
        <!-- Warn about [X] placeholders -->
        <!-- <div style="margin-top:6px; font-size:11px; color:#f4a261;">⚠️ [X] 需卖家确认实际规格后填写</div> -->
      </div>
    </div>

    <!-- IMAGES SECTION -->
    <div style="margin-bottom:24px;">
      <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4cc9f0;
                  text-transform:uppercase; letter-spacing:1.2px; margin-bottom:10px;">
        📷 图片建议
      </div>
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
        <!-- Main image card (highlighted with ⭐) -->
        <div style="background:rgba(255,209,102,.06); border:1px solid rgba(255,209,102,.25);
                    border-radius:8px; padding:14px 16px; grid-column:1/-1;">
          <div style="font-size:11px; font-weight:700; color:#ffd166; margin-bottom:6px;">
            ⭐ 主图（最高优先级）
          </div>
          <div style="font-size:12px; color:#e8eaf0; line-height:1.7;">[Main image recommendations]</div>
        </div>
        <!-- Supporting image cards -->
        <div style="background:#111318; border:1px solid #252c3a; border-radius:8px; padding:12px 14px;">
          <div style="font-size:10px; color:#7b8299; margin-bottom:4px;">图2</div>
          <div style="font-size:12px; color:#e8eaf0; line-height:1.6;">[Description]</div>
        </div>
        <!-- Repeat for 图3, 图4, 图5 -->
      </div>
    </div>

    <!-- Q&A SECTION -->
    <div style="margin-bottom:16px;">
      <div style="font-family:'DM Mono',monospace; font-size:10px; color:#4cc9f0;
                  text-transform:uppercase; letter-spacing:1.2px; margin-bottom:10px;">
        ❓ Q&A 建议（对应当前 Rufus Prompts）
      </div>
      <div style="overflow-x:auto; border-radius:8px; border:1px solid #252c3a;">
        <table style="width:100%; border-collapse:collapse; font-size:12px;">
          <thead>
            <tr style="background:#181c24;">
              <th style="...padding:10px 14px; color:#7b8299; font-family:'DM Mono',monospace;
                         font-size:10px; text-transform:uppercase; letter-spacing:.8px;
                         border-bottom:1px solid #252c3a; text-align:left; width:40%;">
                买家问题 (Prompt #[N])
              </th>
              <th style="...同上...">建议答案模板</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid rgba(37,44,58,.5);">
              <td style="padding:10px 14px; color:#ffd166;">[Buyer question from actual Prompt]</td>
              <td style="padding:10px 14px; color:#e8eaf0; line-height:1.6;">[Answer template]</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Placeholder warning footer -->
    <div style="background:rgba(244,162,97,.06); border:1px solid rgba(244,162,97,.2);
                border-radius:6px; padding:10px 14px; font-size:11px;
                color:#f4a261; line-height:1.7;">
      ⚠️ 所有标注 <code style="background:#181c24; padding:1px 5px; border-radius:3px;">[X]</code>
      的占位符均需卖家根据实际规格填写，请勿直接上传含占位符的版本。
    </div>
  </div>
</details>
```

**Usage rules:**
- Always place immediately after the corresponding partial fix card
- Q&A questions must come from actual running Rufus Prompts (not invented)
- All `[X]` placeholders must have the ⚠️ footer warning
- Never fabricate specs — missing data → `[X]` placeholder

### Data Tables (generic)
```html
<div style="overflow-x:auto; border-radius:10px; border:1px solid #252c3a;">
  <table style="width:100%; border-collapse:collapse;">
    <thead>
      <tr style="background:#181c24;">
        <th style="font-family:'DM Mono',monospace; font-size:10px; text-transform:uppercase; letter-spacing:0.8px; color:#7b8299; padding:10px 14px; text-align:left; border-bottom:1px solid #252c3a; white-space:nowrap;">[HEADER]</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid rgba(37,44,58,0.5);">
        <td style="padding:10px 14px; font-size:12.5px;">[CELL]</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Step Cards (for seller guide)
```html
<div style="background:#1a1f2b; border:1px solid #252c3a; border-radius:10px; padding:20px; margin-bottom:12px;">
  <div style="display:flex; align-items:center; gap:12px; margin-bottom:12px;">
    <div style="width:32px; height:32px; background:#e63946; border-radius:8px; display:flex; align-items:center; justify-content:center; font-family:'Syne',sans-serif; font-size:14px; font-weight:800; flex-shrink:0;">[N]</div>
    <div>
      <div style="font-size:14px; font-weight:700;">[Step Title]</div>
      <div style="font-size:11px; color:#7b8299;">[Subtitle]</div>
    </div>
  </div>
  <div style="font-size:12.5px; color:#7b8299; line-height:1.8;">
    <!-- Step content here -->
    <code style="display:block; background:#0a0b0d; border:1px solid #252c3a; border-radius:6px; padding:10px 14px; font-family:'DM Mono',monospace; font-size:11.5px; color:#4cc9f0; margin:8px 0; line-height:1.7;">[Code/instructions]</code>
  </div>
</div>
```

### Action Items
```html
<div style="background:#1a1f2b; border:1px solid #252c3a; border-radius:8px; padding:16px 18px; display:grid; grid-template-columns:28px 80px 1fr auto; gap:14px; align-items:start; margin-bottom:10px;">
  <div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:#252c3a; line-height:1;">01</div>
  <span class="badge urgent">[PRIORITY BADGE]</span>
  <div>
    <div style="font-size:13px; font-weight:700; margin-bottom:4px;">[Action Title]</div>
    <div style="font-size:12px; color:#7b8299; line-height:1.6;">[Description]
      <div style="background:#0a0b0d; border:1px solid #252c3a; border-radius:6px; padding:8px 12px; font-family:'DM Mono',monospace; font-size:11px; color:#4cc9f0; margin-top:8px; line-height:1.8;">[Steps]</div>
    </div>
  </div>
</div>
```

---

## Section Title Pattern

```html
<div style="font-family:'Syne',sans-serif; font-size:18px; font-weight:700; letter-spacing:0.5px; margin-bottom:20px; display:flex; align-items:center; gap:10px; margin-top:56px;">
  <span style="width:28px; height:28px; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0; background:rgba(230,57,70,0.15);">💯</span>
  [Section Title]
</div>
```

---

## Stat Row (4-column key metrics)

```html
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px;">
  <div style="background:#1a1f2b; border:1px solid #252c3a; border-radius:10px; padding:18px 16px; text-align:center;">
    <div style="font-family:'Syne',sans-serif; font-size:28px; font-weight:800; line-height:1; margin-bottom:6px; color:[COLOR];">[VALUE]</div>
    <div style="font-size:11px; color:#7b8299;">[Label]</div>
  </div>
</div>
```

---

## Insight Box

```html
<div style="background:linear-gradient(135deg,rgba(230,57,70,0.06),rgba(76,201,240,0.04)); border:1px solid rgba(230,57,70,0.2); border-radius:10px; padding:20px 24px; margin-bottom:20px;">
  <div style="font-family:'DM Mono',monospace; font-size:10px; color:#e63946; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:8px;">🔍 关键洞察</div>
  <p style="font-size:13px; line-height:1.7;">[Insight text with <strong>bold key points</strong>]</p>
</div>
```

---

## Full Page Structure

```html
<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Brand] × COSMO Rufus 诊断优化报告</title>
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>/* Include all CSS variables and resets here */</style>
</head>
<body style="background:#0a0b0d; color:#e8eaf0; font-family:'Noto Sans SC',sans-serif; font-size:14px; line-height:1.7; padding:0 0 80px;">

  <!-- HERO -->
  <!-- CONTAINER (max-width:1100px, margin:0 auto, padding:0 40px) -->

    <!-- Stat Row (4 key metrics) -->

    <!-- V1→V2 Comparison Banner (returning sellers only) -->

    <!-- Section 1: Health Scores — overall brand ring + 6 product rings -->

    <!-- Section 2: Prior Recommendations Tracking (v2+ only) -->

    <!-- Section 3: COSMO Analysis Table — 11 columns with real sales data -->

    <!-- Section 4: Key Insights -->

    <!-- Section 5: Listing Optimization
         For each product with issues:
           - Partial Fix Card (before/after rewrite)
           - Complete Listing Reference Template (<details>/<summary>) -->

    <!-- Section 6: Ad Action Plan -->

    <!-- Section 7: Plain-language Seller Guide -->

    <!-- Section 8: Summary Table (one-page priority checklist) -->

    <!-- Section 9: Periodic Reports Value -->

    <!-- Section 10: Next Report CTA -->

    <!-- Section 11: Partnership CTA (WeChat ray0117_, no email) -->

  <!-- FOOTER with Cosle attribution + COSMO paper citation -->

</body>
</html>
```

---

## Footer Template

```html
<div style="text-align:center; padding:40px; color:#7b8299; font-size:11px; border-top:1px solid #252c3a; margin-top:60px;">
  <div>由 <strong>Cosle</strong>（香港科技大学 AI 创业团队）基于亚马逊 COSMO 算法论文生成</div>
  <div style="margin-top:6px">数据来源：[Brand] SP Prompts Report · 数据期：[PERIOD] · 报告日期：[DATE]</div>
  <div style="margin-top:6px; font-style:italic">Yu et al. (2024). COSMO: A Large-Scale E-commerce Common Sense Knowledge Generation and Serving System at Amazon. <em>SIGMOD-Companion '24</em></div>
  <div style="margin-top:10px; font-size:10px; color:#4a5068">本报告仅供参考，数据具有时效性。Rufus 知识图谱约每 2–4 周刷新一次，建议定期进行诊断。</div>
</div>
```

---

## Partnership CTA Section (place before footer, after summary table)

Add this section to every report. It contains the Cosle partnership invitation and WeChat contact. **Never include any email addresses or references to "jack".**

```html
<!-- PARTNERSHIP CTA — always include before footer -->
<div style="background:linear-gradient(135deg,#0f1a10,#0a1208); border:1px solid rgba(7,193,96,.25); border-radius:16px; padding:36px; margin-top:20px; position:relative; overflow:hidden;">
  <div style="position:absolute; top:-40px; right:-40px; width:200px; height:200px; background:radial-gradient(circle,rgba(7,193,96,.12) 0%,transparent 70%); pointer-events:none;"></div>

  <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(7,193,96,.12); border:1px solid rgba(7,193,96,.3); border-radius:4px; padding:4px 12px; font-family:'DM Mono',monospace; font-size:10px; color:#07C160; letter-spacing:1px; text-transform:uppercase; margin-bottom:16px;">
    🤝 Cosle 合作伙伴计划
  </div>

  <h3 style="font-family:'Syne',sans-serif; font-size:22px; font-weight:800; margin-bottom:8px; line-height:1.3;">
    开启您的亚马逊 AI 伴侣计划<br>
    <span style="color:#07C160; font-size:18px;">让前沿研究成为您的竞争护城河</span>
  </h3>

  <div style="font-size:13.5px; color:#a0b8a4; line-height:2; margin:16px 0 20px; max-width:680px;">
    本次报告基于您提交的时间节点数据进行精准诊断，数据具有时效性——<strong style="color:#e8eaf0;">Rufus 的底层知识图谱每 2–4 周刷新一次</strong>，今天的诊断结果，下个月可能已发生新变化。<br><br>
    我们诚挚邀请您成为 <strong style="color:#07C160;">Cosle 长期合作伙伴</strong>。作为香港科技大学研究生团队，我们的导师是亚马逊 Rufus AI 领域的前沿研究者，能第一时间掌握算法变动与学术动态，并据此及时更新我们的诊断模型。<br><br>
    <strong style="color:#e8eaf0;">您的信任，是我们早期团队最大的动力。</strong>亚马逊对 AI 的投入正以指数级增长，选择一个能与您同步成长的 AI 诊断伙伴，才是真正持久的竞争优势。
  </div>

  <div style="display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-bottom:24px; max-width:560px;">
    <div style="display:flex; align-items:center; gap:10px; background:rgba(7,193,96,.08); border:1px solid rgba(7,193,96,.2); border-radius:8px; padding:12px 14px;">
      <span>✦</span><span style="font-size:12.5px; color:#c0d8c0;">终身免费报告诊断服务</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; background:rgba(7,193,96,.08); border:1px solid rgba(7,193,96,.2); border-radius:8px; padding:12px 14px;">
      <span>✦</span><span style="font-size:12.5px; color:#c0d8c0;">算法重大变动时主动预警</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; background:rgba(7,193,96,.08); border:1px solid rgba(7,193,96,.2); border-radius:8px; padding:12px 14px;">
      <span>✦</span><span style="font-size:12.5px; color:#c0d8c0;">针对您产品线的定制 COSMO 策略</span>
    </div>
    <div style="display:flex; align-items:center; gap:10px; background:rgba(7,193,96,.08); border:1px solid rgba(7,193,96,.2); border-radius:8px; padding:12px 14px;">
      <span>✦</span><span style="font-size:12.5px; color:#c0d8c0;">优先获取最新亚马逊 AI 研究成果</span>
    </div>
  </div>

  <div style="display:flex; align-items:center; gap:16px; flex-wrap:wrap;">
    <div style="background:#07C160; color:white; padding:12px 24px; border-radius:10px; font-weight:700; font-size:14px;">
      微信联系：ray0117_
    </div>
    <div style="font-size:12px; color:#7b8299;">添加微信后即可获得免费咨询，了解合作详情</div>
  </div>
</div>
```

**Rules for this section:**
- WeChat ID is always `ray0117_`
- Never include email addresses of any kind
- Green theme: `#07C160` (WeChat brand green)
- Place after "Next Report CTA" section, immediately before the footer

---

## Color Quick Reference

| Signal | Background | Border | Text |
|--------|-----------|--------|------|
| Urgent/Red | rgba(230,57,70,0.08) | rgba(230,57,70,0.25) | #e63946 |
| Warning/Orange | rgba(244,162,97,0.08) | rgba(244,162,97,0.25) | #f4a261 |
| Info/Yellow | rgba(255,209,102,0.08) | rgba(255,209,102,0.25) | #ffd166 |
| Good/Green | rgba(46,196,182,0.08) | rgba(46,196,182,0.25) | #2ec4b6 |
| Data/Blue | rgba(76,201,240,0.1) | rgba(76,201,240,0.25) | #4cc9f0 |
| Muted | rgba(120,130,160,0.12) | rgba(120,130,160,0.25) | #7b8299 |
