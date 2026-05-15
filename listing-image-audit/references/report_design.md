# HTML Report Design System (Image Audit)

紫色 IMAGE-AUDIT 主题 — 视觉上与诊断报告系列协调，但用紫色 `#c77dff` 作为主标识，与诊断报告（红 `#e63946`）/ 预测报告（橙 `#f4a261`）视觉区分。

## CSS 变量（必须放在 `:root`）

```css
:root{
  --bg:#0a0b0d; --bg2:#111318; --bg3:#181c24; --card:#1a1f2b;
  --border:#252c3a; --red:#e63946; --orange:#f4a261; --yellow:#ffd166;
  --green:#2ec4b6; --blue:#4cc9f0; --purple:#c77dff;
  --text:#e8eaf0; --muted:#7b8299; --brand:#c77dff;
}
```

## 字体

```html
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
```

- Syne 800：H1/H2/H3 / 分数大字
- DM Mono：数据 / 文件名 / 标签徽章
- Noto Sans SC：正文 / 中文

## 全局 reset + Print 颜色保留

```css
*{box-sizing:border-box;margin:0;padding:0;
  -webkit-print-color-adjust:exact !important;
  print-color-adjust:exact !important;
  color-adjust:exact !important}
```

`print-color-adjust:exact` 是导出 PDF 时<strong>必须</strong>的，否则 Chrome 默认会把暗色背景变白。

## Hero Header

```html
<div style="background:linear-gradient(135deg,#0d1117,#1a0d24,#0d1117);
            border-bottom:1px solid #2a1535;padding:60px 40px 50px;
            position:relative;overflow:hidden">
  <div style="position:absolute;top:-60px;right:-60px;width:340px;height:340px;
              border-radius:50%;
              background:radial-gradient(circle,rgba(199,125,255,0.18),transparent 70%)"></div>
  <div class="container" style="position:relative;z-index:1">
    <div style="display:inline-flex;align-items:center;gap:8px;
                background:rgba(199,125,255,0.12);border:1px solid rgba(199,125,255,0.3);
                border-radius:4px;padding:4px 12px;font-family:'DM Mono',monospace;
                font-size:11px;color:#c77dff;letter-spacing:1.5px;text-transform:uppercase">
      🎨 Cosle Image Audit Report v1.0
    </div>
    <h1>[Product Name]<br><span style="color:#c77dff">主图 + A+ 视觉打分诊断报告</span></h1>
  </div>
</div>
```

## image-card 卡片（核心组件）

每张图独立一个 image-card：

```css
.image-card{
  background:#1a1f2b;border:1px solid #252c3a;border-radius:14px;
  padding:20px;margin-bottom:18px;
  display:grid;grid-template-columns:340px 1fr;gap:24px;align-items:start
}
.image-card .img-wrap{
  background:#0a0b0d;border:1px solid #252c3a;border-radius:10px;
  overflow:hidden;display:flex;align-items:center;justify-content:center;
  min-height:280px;position:relative
}
.image-card .img-wrap img{width:100%;height:auto;display:block;border-radius:8px}
.image-card .img-meta{
  font-family:'DM Mono',monospace;font-size:10px;color:var(--muted);
  margin-top:8px;text-align:center
}
.image-card h3{font-family:'Syne',sans-serif;font-size:16px;font-weight:800;margin-bottom:6px}
.image-card .role{
  font-family:'DM Mono',monospace;font-size:10px;color:var(--muted);
  text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px
}
@media (max-width:900px){.image-card{grid-template-columns:1fr}}
```

## SVG 评分环 + 中央数字 div（必须！）

纯 SVG 圆环不显示中央数字。必须用 `position:relative` 包裹 SVG + absolute 居中分数 div：

```html
<div style="position:relative;width:80px;height:80px;flex-shrink:0">
  <svg width="80" height="80" viewBox="0 0 80 80" style="transform:rotate(-90deg)">
    <circle cx="40" cy="40" r="33" fill="none" stroke="#181c24" stroke-width="7"/>
    <circle cx="40" cy="40" r="33" fill="none" stroke="[#color]" stroke-width="7"
      stroke-linecap="round" stroke-dasharray="207.3"
      stroke-dashoffset="[207.3 * (1 - score/100)]"/>
  </svg>
  <div style="position:absolute;top:0;left:0;width:100%;height:100%;
              display:flex;align-items:center;justify-content:center;
              font-family:'Syne',sans-serif;font-size:22px;font-weight:800;
              color:[#color]">[score]</div>
</div>
```

- `stroke-dasharray="207.3"` = 2π × r = 2 × 3.14159 × 33 ≈ 207.3（圆周长）
- `stroke-dashoffset="33.17"` 对应分数 84（207.3 × (1 - 84/100) = 33.17）
- 颜色按分数级别选：≤40 红 / 41-60 橙 / 61-80 绿 / 81-100 紫

## 维度横条（dim-bar）

```css
.dim-bar{background:#0a0b0d;border:1px solid var(--border);border-radius:6px;
         padding:8px 12px;margin-bottom:6px}
.dim-bar-head{display:flex;justify-content:space-between;font-size:11.5px;margin-bottom:3px}
.dim-bar-fill{height:3px;background:#181c24;border-radius:2px;overflow:hidden}
.dim-bar-fill > div{height:100%;border-radius:2px}
```

模板：
```html
<div class="dim-bar">
  <div class="dim-bar-head">
    <span>[维度名]（[权重]%）</span><strong style="color:[#color]">[分]</strong>
  </div>
  <div class="dim-bar-fill"><div style="width:[分]%;background:[#color]"></div></div>
</div>
```

## 4 种诊断 box（核心信息载体）

```css
.diag-box{border-radius:6px;padding:10px 14px;margin-top:8px;
          font-size:11.5px;color:#9eb4c5;line-height:1.75}
.diag-borrow{background:rgba(46,196,182,0.06);border:1px solid rgba(46,196,182,0.2)}
.diag-borrow strong{color:#2ec4b6}
.diag-diff{background:rgba(244,162,97,0.06);border:1px solid rgba(244,162,97,0.2)}
.diag-diff strong{color:#f4a261}
.diag-warn{background:rgba(230,57,70,0.06);border:1px solid rgba(230,57,70,0.2)}
.diag-warn strong{color:#e63946}
.diag-fix{background:rgba(76,201,240,0.06);border:1px solid rgba(76,201,240,0.2)}
.diag-fix strong{color:#4cc9f0}
```

用法：
```html
<div class="diag-box diag-borrow"><strong>🔍 做得好的地方</strong> [具体引用图中视觉元素]</div>
<div class="diag-box diag-diff"><strong>🚀 差异化机会</strong> [点名 1-2 个竞品]</div>
<div class="diag-box diag-warn"><strong>⚠ 关键问题</strong> [Amazon 合规 / 重复 / 命名]</div>
<div class="diag-box diag-fix"><strong>📝 In-place 优化建议</strong> [文字 overlay / 重命名 / 重排]</div>
```

## Section Title

```css
.section-title{
  font-family:'Syne',sans-serif;font-size:18px;font-weight:700;
  letter-spacing:.5px;margin:56px 0 20px;display:flex;align-items:center;gap:10px
}
.section-title .icon{
  width:28px;height:28px;border-radius:6px;display:flex;align-items:center;
  justify-content:center;font-size:14px;flex-shrink:0;
  background:rgba(199,125,255,0.15)
}
```

## Stat Row（4 列摘要）

```html
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:32px">
  <div class="card" style="text-align:center;padding:18px 14px">
    <div style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;
                color:#c77dff;line-height:1;margin-bottom:6px">[N]</div>
    <div style="font-size:11px;color:var(--muted)">[Label]</div>
  </div>
  ...
</div>
```

## Alert Boxes

```css
.alert{border-radius:8px;padding:14px 18px;margin-bottom:10px;
       display:flex;align-items:flex-start;gap:12px;font-size:13px;line-height:1.6}
.alert-red{background:rgba(230,57,70,0.08);border:1px solid rgba(230,57,70,0.25)}
.alert-orange{background:rgba(244,162,97,0.08);border:1px solid rgba(244,162,97,0.25)}
.alert-yellow{background:rgba(255,209,102,0.08);border:1px solid rgba(255,209,102,0.25)}
.alert-green{background:rgba(46,196,182,0.08);border:1px solid rgba(46,196,182,0.25)}
.alert-blue{background:rgba(76,201,240,0.08);border:1px solid rgba(76,201,240,0.25)}
.alert-purple{background:rgba(199,125,255,0.08);border:1px solid rgba(199,125,255,0.25)}
```

## Tags（L1/L2/L3/Predictive）

```css
.tag{display:inline-flex;align-items:center;padding:2px 8px;border-radius:3px;
     font-family:'DM Mono',monospace;font-size:10px;font-weight:500;
     text-transform:uppercase;letter-spacing:.5px;white-space:nowrap}
.tag-l1{background:rgba(46,196,182,0.15);color:#2ec4b6;border:1px solid rgba(46,196,182,0.3)}
.tag-l2{background:rgba(255,209,102,0.15);color:#ffd166;border:1px solid rgba(255,209,102,0.3)}
.tag-l3{background:rgba(230,57,70,0.15);color:#e63946;border:1px solid rgba(230,57,70,0.3)}
.tag-purple{background:rgba(199,125,255,0.15);color:#c77dff;border:1px solid rgba(199,125,255,0.3)}
.tag-blue{background:rgba(76,201,240,0.15);color:#4cc9f0;border:1px solid rgba(76,201,240,0.3)}
.tag-green{background:rgba(46,196,182,0.15);color:#2ec4b6;border:1px solid rgba(46,196,182,0.3)}
.tag-orange{background:rgba(244,162,97,0.15);color:#f4a261;border:1px solid rgba(244,162,97,0.3)}
```

## @media print（PDF 导出必需）

```css
@media print{
  @page{size:A4;margin:10mm 8mm}
  body{padding:0 !important}
  .container{max-width:none !important;padding:0 16px !important}
  .image-card{page-break-inside:avoid;break-inside:avoid}
  .card{page-break-inside:avoid;break-inside:avoid}
  tr{page-break-inside:avoid;break-inside:avoid}
  .section-title{page-break-after:avoid;break-after:avoid;margin-top:24px !important}
  h1,h2,h3{page-break-after:avoid;break-after:avoid}
  .alert{page-break-inside:avoid;break-inside:avoid}
  img{max-width:100% !important;page-break-inside:avoid}
}
```

## Footer

```html
<div style="text-align:center;padding:40px;color:var(--muted);font-size:11px;
            border-top:1px solid var(--border);margin-top:60px">
  <div>由 <strong style="color:#e8eaf0">Cosle</strong> 基于 Cosle Rufus 视觉模型生成</div>
  <div style="margin-top:6px">输入：[N] 张主图 + [N] 张 A+ 图片 · 报告日期 [YYYY-MM-DD]</div>
  <div style="margin-top:14px">📧 <a href="mailto:zouak@connect.ust.hk" style="color:#c77dff">zouak@connect.ust.hk</a></div>
</div>
```

## Container

```css
.container{max-width:1200px;margin:0 auto;padding:0 40px}
```

主图 + A+ 报告由于图片卡片宽（grid 340 + 1fr），用 1200 max-width 比常规 1100 更舒展。

## Image src 路径规则

1. <strong>相对路径</strong>：从 HTML 所在目录出发的相对路径
   - HTML 在 `xxx/E5800/` → `<img src="E5800主图/...">`（去掉 E5800 前缀）
   - HTML 在 `xxx/新品listing/` → `<img src="E5800/E5800主图/...">`（加 E5800 前缀）

2. <strong>URL 编码</strong>：文件名含空格 / 特殊字符必须编码
   - `9.-NA frequency band.jpg` → `9.-NA%20frequency%20band.jpg`
   - 否则浏览器加载破图

3. <strong>路径校验</strong>：HTML 写完后用脚本验证（详见 SKILL.md Step 9 末尾）

## 颜色快速参考

| 用途 | 颜色 | RGBA |
|------|------|------|
| 主标识（紫） | `#c77dff` | rgba(199,125,255,0.x) |
| Critical 红 | `#e63946` | rgba(230,57,70,0.x) |
| Needs Work 橙 | `#f4a261` | rgba(244,162,97,0.x) |
| Yellow | `#ffd166` | rgba(255,209,102,0.x) |
| Good 绿 | `#2ec4b6` | rgba(46,196,182,0.x) |
| Info 蓝 | `#4cc9f0` | rgba(76,201,240,0.x) |
| Muted 灰 | `#7b8299` | n/a |
