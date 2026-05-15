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
```html
<div style="width:80px; height:80px; position:relative;">
  <svg width="80" height="80" viewBox="0 0 80 80" style="transform:rotate(-90deg)">
    <circle cx="40" cy="40" r="33" fill="none" stroke="#181c24" stroke-width="7"/>
    <circle cx="40" cy="40" r="33" fill="none" 
      stroke="[COLOR]" stroke-width="7" stroke-linecap="round"
      stroke-dasharray="207.3"
      stroke-dashoffset="[207.3 * (1 - SCORE/100)]"/>
  </svg>
  <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); font-family:'Syne',sans-serif; font-size:18px; font-weight:800; color:[COLOR]">[SCORE]</div>
</div>
```
Score ring color: red (#e63946) for <50, orange (#f4a261) for 50-65, teal (#2ec4b6) for 65+.

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

### Data Tables
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
    <!-- Section 1: Health Scores -->
    <!-- Section 2: COSMO Analysis Table (per product line) -->
    <!-- Section 3: Key Insights -->
    <!-- Section 4: Listing Optimization -->
    <!-- Section 5: Ad Action Plan -->
    <!-- Section 6: Plain-language Seller Guide -->
    <!-- Section 7: Summary Table -->
  <!-- FOOTER with Cosle attribution + COSMO paper citation -->

</body>
</html>
```

---

## Footer Template

```html
<div style="text-align:center; padding:40px; color:#7b8299; font-size:11px; border-top:1px solid #252c3a; margin-top:60px;">
  <div>由 <strong>Cosle</strong>（香港科技大学 AI 创业团队）基于亚马逊 COSMO 算法论文生成</div>
  <div style="margin-top:6px">数据来源：[Brand] SP Prompts Report · 分析日期：[DATE]</div>
  <div style="margin-top:6px">Yu et al. (2024). COSMO: A Large-Scale E-commerce Common Sense Knowledge Generation and Serving System at Amazon. <em>SIGMOD-Companion '24</em></div>
  <div style="margin-top:10px">📧 <a href="mailto:zouak@connect.ust.hk" style="color:#e63946; text-decoration:none;">zouak@connect.ust.hk</a></div>
</div>
```

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
