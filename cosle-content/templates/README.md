# Templates 使用说明

> 这三个文件是 v2.0「Listing 5 类信息」那篇文章落地时的真实脚本快照,作为后续文章的可执行模板。
> 写新一篇 Cosle 文章时,**复制到新目录、改文字内容、运行**即可,不要直接在 templates/ 里改。

## 三个模板

| 文件 | 输出 | 怎么改 |
|---|---|---|
| `cover-generator.py` | 公众号头图 900×383 + 小封面 800×800 | 改顶部常量 + 函数里的文字。封面有「品牌通用版」(只放 Cosle)和「内容封面版」(主标 + 信息维度)两种,默认用品牌通用版 |
| `wechat-html.html` | 公众号 HTML 排版,可直接 Ctrl+A 复制粘贴到公众号编辑器 | 这是 v2.0 实例。改章节标题 + 段落正文 + 错误/正确示范文本即可。视觉系统(颜色/字体/盒子样式)不要动 |
| `xhs-cards-generator.py` | 小红书 11 张 1080×1440 图卡 + 发布文案 txt | 改各 `card_XX()` 函数里的文字内容,卡片框架(顶部红条/底部品牌签名/卡片背景色)不要动 |

## 推荐工作流

```bash
# 1. 在 Rufus 项目里建本次文章的目录
mkdir -p "/Users/apple/Desktop/Rufus/对外内容（小红书+公众号）/<本期主题>"

# 2. 复制三个模板
cp templates/cover-generator.py <目标目录>/gen_cover.py
cp templates/wechat-html.html <目标目录>/公众号-排版_<版本>.html
cp templates/xhs-cards-generator.py <目标目录>/gen_xhs_cards.py

# 3. 改 cover-generator.py / xhs-cards-generator.py 里的 OUT_DIR 路径

# 4. 改内容文字,运行
python3 gen_cover.py
python3 gen_xhs_cards.py

# 5. wechat-html.html 直接双击浏览器打开 → Cmd+A → Cmd+C → 粘贴到公众号
```

## 视觉系统强约束

不允许在 templates 之外的脚本里改这些值,所有 Cosle 内容必须保持视觉统一:

```python
BG = (31, 31, 31)         # #1F1F1F 主色深灰
RED = (230, 57, 70)       # #E63946 警示红
WHITE = (255, 255, 255)
GREY_TEXT = (220, 220, 220)
GREY_MID = (160, 160, 160)
GREY_DARK = (110, 110, 110)
GREY_BG_2 = (48, 48, 48)  # 错误示范深灰底
RED_BG = (60, 30, 35)     # 正确示范暗红底

PINGFANG = "/System/Library/Fonts/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/HelveticaNeue.ttc"
SFMONO = "/System/Library/Fonts/SFNSMono.ttf"
```

字体索引(PIL `ImageFont.truetype(path, size, index=N)`):

| 字体 | index | 用途 |
|---|---|---|
| PingFang Regular | 3 | 正文 |
| PingFang Medium | 4 | 副标 / 强调 |
| PingFang Semibold | 5 | 标题 |
| Helvetica Neue Thin | 12 | 品牌名「Cosle」、大数字 |
| Helvetica Neue Regular | 0 | 英文小字 |

## 文字内容改写时的核查 checklist

每次改完模板,运行前必查:
- [ ] 品牌签名段一字不差(`关于 Cosle` 那段)
- [ ] 价值主张段(60 字)一字不差
- [ ] 没有「天塌、灭顶、出局、小编、咱们」等禁用词
- [ ] 所有 listing 数字都是真实可公开的(否则用 `[X]` 占位)
- [ ] 系列编号正确(`#00X`),和 reference-examples 续号
- [ ] 文末「下期预告」必须明确,下一期要兑现

## 修复历史(踩过的坑)

| 现象 | 原因 | 修复 |
|---|---|---|
| Cosle 出成斜体 | HelveticaNeue.ttc index=2 是 Italic | 改用 index=12 (Thin) |
| 错误示范盒只显示一个逗号 | SFMono 不支持中文,中文按空格 split 后丢失 | 判断 bad/good 是否含 ASCII,中文走 PingFang + wrap_chinese |
| 标题压在大数字上 | 居中坐标算错 | 改成上下三段式布局,数字 + 红线 + 标题各占一段 |
