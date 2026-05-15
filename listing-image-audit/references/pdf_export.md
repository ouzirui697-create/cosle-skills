# PDF Export Guide

把 HTML 报告转为 PDF。默认用 Chrome headless（macOS 上几乎都已装 Chrome），渲染质量最高（保留 CSS / 字体 / 暗色主题 / SVG / 中文字体）。

## 前置条件（必查）

HTML 必须包含以下 print CSS（在 `<style>` 内），否则 Chrome 默认会：
- 把暗色背景变白（节省墨水）
- 把 image-card 切断到两页
- 把 section-title 单独留页脚

```css
*{... -webkit-print-color-adjust:exact !important;
       print-color-adjust:exact !important;
       color-adjust:exact !important}

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

如 HTML 还没有这些 CSS，先用 Edit 工具加上再转 PDF。

## 主要方案 · Chrome Headless（推荐 · macOS）

```bash
HTML_PATH="/绝对路径/to/report.html"
PDF_PATH="/绝对路径/to/report.pdf"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --virtual-time-budget=15000 \
  --run-all-compositor-stages-before-draw \
  --hide-scrollbars \
  --no-sandbox \
  --print-to-pdf="$PDF_PATH" \
  "file://$HTML_PATH"
```

参数说明：

| 参数 | 作用 |
|------|------|
| `--headless=new` | 新版 headless 模式（Chrome 109+） |
| `--disable-gpu` | macOS headless 兼容性 |
| `--no-pdf-header-footer` `--print-to-pdf-no-header` | 不要 Chrome 默认的页眉页脚（URL / 时间戳） |
| `--virtual-time-budget=15000` | 给 15 秒让 Google Fonts 加载（中文字体不可缺） |
| `--run-all-compositor-stages-before-draw` | 等所有渲染层合成完成 |
| `--hide-scrollbars` | 不要滚动条遮挡内容 |

输出会看到：`N bytes written to file /path/to/report.pdf`

## 验证 PDF

```bash
mdls -name kMDItemNumberOfPages \
     -name kMDItemPageHeight \
     -name kMDItemPageWidth \
     "$PDF_PATH"
```

预期输出（A4）：
- `kMDItemNumberOfPages = [页数]`
- `kMDItemPageHeight = 841.92`
- `kMDItemPageWidth = 594.96`

## 替代方案 1 · Linux / Ubuntu

```bash
google-chrome --headless=new --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PDF_PATH" \
  "file://$HTML_PATH"
```

或：
```bash
chromium --headless=new --disable-gpu \
  --print-to-pdf="$PDF_PATH" \
  "file://$HTML_PATH"
```

## 替代方案 2 · wkhtmltopdf

```bash
brew install wkhtmltopdf  # macOS
sudo apt install wkhtmltopdf  # Ubuntu

wkhtmltopdf \
  --enable-local-file-access \
  --print-media-type \
  --page-size A4 \
  --margin-top 10mm --margin-bottom 10mm \
  --margin-left 8mm --margin-right 8mm \
  "$HTML_PATH" "$PDF_PATH"
```

注：wkhtmltopdf 基于旧版 WebKit，CSS `print-color-adjust` 可能不完美，<strong>建议优先用 Chrome</strong>。

## 替代方案 3 · WeasyPrint（Python）

```bash
pip install weasyprint
weasyprint "$HTML_PATH" "$PDF_PATH"
```

WeasyPrint 对中文字体处理较好，但<strong>不支持本 skill 用的 Google Fonts 远程加载</strong>，需把字体下载到本地。

## 常见问题

### 1. 图片不显示在 PDF
原因：相对路径找不到。  
解决：用<strong>绝对路径</strong>或<strong>确保 HTML 所在目录与图片目录关系正确</strong>。Chrome 用 `file://` 协议时，相对路径 base 是 HTML 所在目录。

### 2. 中文字符变成豆腐方块
原因：Google Fonts 没加载完。  
解决：增加 `--virtual-time-budget=20000`（20 秒），或在 HTML 中改为本地字体。

### 3. PDF 太大（> 20 MB）
原因：图片原始分辨率高。  
解决：用 `--enable-features=PdfImageDownsampling` 或先压缩图片再转 PDF。

### 4. SVG 评分环不显示数字
原因：HTML 中没用 `position:relative` 包裹 SVG + absolute 分数 div（参考 `report_design.md`）。  
解决：先修复 HTML 再重新转 PDF。

### 5. image-card 被拦腰切断
原因：缺 print CSS `page-break-inside:avoid`。  
解决：在 HTML `<style>` 内补上完整 `@media print { ... }` 块。

### 6. 暗色背景变白
原因：缺 `print-color-adjust:exact`。  
解决：在 `*{}` 全局规则里加上三种前缀的 `*-print-color-adjust:exact !important`。

## 完整封装脚本（建议附在交付时）

```bash
#!/bin/bash
# 将 HTML 报告转为 A4 PDF
# 用法: ./html2pdf.sh report.html report.pdf

HTML="$1"
PDF="$2"

if [ -z "$HTML" ] || [ -z "$PDF" ]; then
  echo "用法: $0 input.html output.pdf"
  exit 1
fi

HTML_ABS="$(cd "$(dirname "$HTML")"; pwd)/$(basename "$HTML")"
PDF_ABS="$(cd "$(dirname "$PDF")"; pwd)/$(basename "$PDF")"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf-no-header \
  --virtual-time-budget=15000 \
  --run-all-compositor-stages-before-draw \
  --hide-scrollbars --no-sandbox \
  --print-to-pdf="$PDF_ABS" \
  "file://$HTML_ABS"

echo "PDF: $PDF_ABS"
mdls -name kMDItemNumberOfPages "$PDF_ABS"
```

## 何时不需要 PDF

- 仅在 Mac / Windows 桌面浏览器查看 → HTML 已经够好，PDF 反而失去交互
- 报告需要继续编辑 / 反馈 → 保留 HTML
- 嵌入其他文档 / 邮件附件 / 打印 → 转 PDF
- 客户希望"看着方便" / 分享给团队 → 转 PDF（统一阅读体验）

询问用户后再决定。
