# Examples · 真实案例样本

本目录包含 Cosle Skills 输出的<strong>真实报告样本</strong>（产品名 / 价格 / 竞品 ASIN 等已脱敏处理），用于演示三个 skill 的输出格式与质量。

## 文件清单

| 文件 | 来源 Skill | 说明 |
|------|-----------|------|
| [`example-prelaunch-listing-report.html`](./example-prelaunch-listing-report.html) | `prelaunch-listing` | 新品文字 listing 预测报告 v2.0 · 完整 12 章节 · 含 v2.0 经验教训反馈循环 |
| [`example-image-audit-report.html`](./example-image-audit-report.html) | `listing-image-audit` | 主图 + A+ 视觉打分诊断报告 · 13 主图 + 3 A+ 逐张评分 · 16 评分卡 |

## 如何查看

直接在浏览器中打开 `.html` 文件即可。报告自带暗色主题 + 完整 CSS，无需额外依赖。

```bash
# macOS
open example-prelaunch-listing-report.html

# Linux
xdg-open example-prelaunch-listing-report.html
```

## 注意

- **图片报告需要原图才能完整渲染**：`example-image-audit-report.html` 中的 `<img src>` 用的是相对路径（指向 `E5800/E5800主图/` 等目录），独立查看时图片会显示为破图占位符 — 这是<strong>正常的</strong>，仅说明卖家在实际使用时该把图片目录与 HTML 报告放在同一项目根下。

- **报告本身设计为可独立交付**：暗色主题 / 字体 / SVG 评分环 / 印刷友好的 print CSS 都已内嵌，可以直接打印为 PDF 或 PNG 分享。

- **作为 PDF 也可以**：参见 [`../listing-image-audit/references/pdf_export.md`](../listing-image-audit/references/pdf_export.md) 的 Chrome headless 命令。

## 案例脱敏说明

样本中保留的 GL.iNet Mudi 7 (GL-E5800) 是公开发售的产品（Parent ASIN B0GTNPSJ5Q），所有技术参数 / 价格 / 竞品 ASIN 均来自卖家提供的公开 Excel 输入模板，无敏感信息。
