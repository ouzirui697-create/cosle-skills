---
name: cosle-content
description: >
  生成 Cosle 跨境卖家实验室公众号长文 / 小红书图文 / 封面图,统一品牌调性、视觉系统、内容结构。
  Use this skill whenever the user asks to write content for the Cosle WeChat public account ("Cosle 跨境卖家实验室"),
  Xiaohongshu (小红书) posts about Amazon AI shopping / Rufus / COSMO / Alexa for Shopping,
  or any external-facing Cosle marketing content.
  触发词:「写一篇 Cosle 公众号」「Cosle 文章」「公众号长文」「小红书图卡」「写一篇关于 Rufus / COSMO / Alexa 的文章」
  「帮我写一篇引流卖家的文章」「Cosle 第 N 篇」「参考 XX 文章再写一篇」「公众号排版」「公众号 HTML」「小红书发布」。
  也触发于「Cosle 封面图」「公众号头图」「小红书图文卡片」。
  本 skill 强制 5 步工作流:Step 0 反问澄清 → Step 1 加载品牌系统 → Step 2 拟定骨架 → Step 3 落稿 → Step 4 生成排版资产。
  绝不允许跳过 Step 0 直接动笔。
---

# Cosle 内容创作 Skill

## 这个 Skill 解决什么问题

Cosle 是「AI 购物时代服务于亚马逊精品卖家的研究团队」。它的对外内容(公众号、小红书、PR、销售材料)有非常强的品牌约束:研究院调性、不立危机叙事、价值主张段落必须照搬、视觉系统统一。

如果每次写文章都重新发明结构和措辞,文章会失去系列感、可能踩品牌雷区(危机词/小编口吻/编造数字),也很难复用上一篇沉淀的视觉资产。

本 skill 把整套流程封装成 5 步:**先反问 → 加载品牌 → 拟骨架 → 落稿 → 生成排版资产(HTML / 图卡 / 封面)**。

---

## 强制工作流(顺序不可跳)

### Step 0 — 反问澄清(MANDATORY)

> **在写任何一个字之前,先按 `kickoff-questions.md` 的清单向用户提问。**
> 不允许跳过此步直接动笔。即使用户已给出主题,也必须确认参考文章/选题方向/字数/引流强度/承接关系五件事。

用 `AskUserQuestion` 工具,一次最多 3-4 个问题。核心要问的:

1. **承接哪一篇 / 第几篇** — 系列文章必须互相承接,文末的「下期预告」要兑现
2. **是否有参考文章** — 用户要照着某篇文章的结构/节奏/钩子来写
3. **选题方向** — 兑现上一篇预告 / 蹭最新行业动向 / 卖家高频问题 / 真实诊断案例反推
4. **字数和引流强度** — 1500 字软引流 / 2500-3000 字干货 / 1200 字短钩子
5. **是否包含真实诊断案例** — 哪个客户、是否脱敏沿用、数字是否允许公开

详见 `kickoff-questions.md`。

**如果用户给了参考文章链接(尤其是 mp.weixin.qq.com 链接),WebFetch 大概率拿不到**(微信反爬验证页)。这种情况必须明确让用户**直接粘贴正文**,不要凭借标题或猜测就动笔。

### Step 1 — 加载品牌系统

读取 `brand-system.md`,把以下内容直接内化(不允许改写):

- **Slogan**:「让你的产品在 AI 推荐里被看见」
- **副标**:「AI 购物时代的卖家研究团队」
- **价值主张段(60 字压舱石)** — 任何对外文章都必须出现,不允许自由改写
- **差异化一句话** — 「我们卖快速变化中的认知,不卖稳定数据指标」
- **品牌签名段** — 文末固定段落,直接复用
- **禁用词清单** — 「天塌、灭顶、出局、杀招、小编、咱们」等绝对不能出现

同时读取 `~/.claude/projects/-Users-apple-Desktop-Rufus/memory/project_cosle_brand_v1.md` 作为权威源(memory 优先级高于本 skill 内的 brand-system.md,若有冲突以 memory 为准)。

### Step 2 — 拟定文章骨架

不论公众号长文还是小红书图卡,都用同一套 5 节式骨架:

| 节 | 作用 | 公众号字数 | 小红书图卡 |
|---|---|---|---|
| 1 · 开篇钩子 | 承接上篇 / 抛出核心问题 / 先说结论 | 200-300 | 第 1 张(封面) |
| 2 · 问题诊断 | 旧逻辑为什么开始失效 / 现象拆解 | 300-400 | 第 2 张 |
| 3 · 核心方法论 | 干货主体,带「错误示范 vs 正确示范」对比 | 1000-1500 | 第 3-8 张 |
| 4 · 真实案例 | 一个脱敏客户的完整诊断闭环 | 400-500 | 第 9 张 |
| 5 · 泼冷水 / 但是 | 用数据(YouGov 等)给冷静判断,避免危机叙事 | 300-400 | 第 10 张 |
| 6 · 行动建议 + 引流 | 3 件今天能动手的事 + 文末 CTA(仅公众号) | 200-300 | 第 11 张(行动 + 签名) |

引流话术(仅公众号,小红书禁用):
- 公众号后台回复关键词「自查」领取
- 或扫码加微信(放 `qr_personal.jpg`)
- 免费 30 分钟速看 ASIN 邀请(对齐 `自查清单_卖家咨询话术_v1.txt`)

**小红书绝对不能出现**:二维码 / 微信号 / 加我 / 扫码 / 私信 / 公众号引导。

### Step 3 — 落稿

按骨架写 markdown 主稿,落在:
```
/Users/apple/Desktop/Rufus/对外内容（小红书+公众号）/<主题文件夹>/公众号长文_v<版本>_<选题>.md
```

落稿后立即按 `content-verification.md` 做内容核查:
- 所有 listing 诊断数字必须 100% 真实,未确认用 `[X]` 占位
- 价值主张段一字不差
- 无危机词、无个人化口吻
- 引用文献完整(YouGov / Amazon Science / TechCrunch / SIGMOD 等)
- 字数控制达标

### Step 4 — 生成排版资产

根据用户的发布渠道,生成对应资产:

| 渠道 | 资产 | 模板路径 |
|---|---|---|
| 公众号 · 复制粘贴版 | 纯文本 markdown,带 `━━━━━` 分隔线 | `templates/wechat-plain.md` |
| 公众号 · HTML 排版版 | 直接粘进公众号编辑器的 HTML | `templates/wechat-html.html` |
| 公众号 · 封面图 | 900×383(首条)+ 800×800(次条) | `templates/cover-generator.py` |
| 小红书 · 图文卡 | 11 张 1080×1440 / 3:4 | `templates/xhs-cards-generator.py` |
| 小红书 · 发布文案 | 标题 3 选 1 + 正文 + 标签 + 规则自查 | 生成在图卡同目录的 txt |

**视觉系统强约束**(三套资产必须一致):
- 主色 `#1F1F1F` 深灰底
- 强调 `#E63946` 警示红
- 中文字体 PingFang SC,英文字体 Helvetica Neue Thin(品牌名)/ SF Mono(代码示范)
- 章节标题左侧 6px 红色竖条
- 「错误示范」灰底深灰边条,「正确示范」暗红底亮红边条

---

## 不允许的操作

- ❌ 跳过 Step 0 直接动笔
- ❌ 改写价值主张段或差异化一句话
- ❌ 出现危机词 / 小编口吻 / 个人戏谑("这玩意""神经病""复读机")
- ❌ 编造未确认的 listing 数字 / 改写效果数字
- ❌ 小红书图卡里出现二维码 / 微信号 / 加微引导
- ❌ 公众号 CTA 用「立即下单」「错过血亏」等焦虑词
- ❌ 对友商(H10 / 卖家精灵 / 千问 / 豆包)做轻佻调侃

---

## 文件索引

| 文件 | 用途 |
|---|---|
| `brand-system.md` | 品牌定位、口号矩阵、视觉系统、禁用词清单(本 skill 自带,memory 优先) |
| `kickoff-questions.md` | Step 0 反问问题清单(中英双语模板) |
| `article-structure.md` | 5 节骨架详细说明 + 每节写作要点 |
| `content-verification.md` | 内容核查铁律(数字 / 调性 / 引用 / 字数) |
| `templates/wechat-html.html` | 公众号 HTML 排版骨架,可直接 fork 改文字 |
| `templates/xhs-cards-generator.py` | 小红书 11 张图卡 Python 生成脚本 |
| `templates/cover-generator.py` | 公众号封面图 + 小红书封面 Python 生成脚本 |
| `reference-examples/` | 已发布标杆文章 markdown 备份,用作 few-shot 参考 |

---

## 典型对话模板(Step 0)

```
用户:「帮我写一篇 Cosle 公众号文章,主题是 XXX」

Claude(本 skill 触发后):
「在我开始动笔之前,需要先把 5 件事和你对齐。我用 AskUserQuestion 一次问 3 个。」

[AskUserQuestion 第一轮]
1. 这是 Cosle 公众号第几篇?有没有上一篇要承接的「下期预告」?
2. 有没有参考文章?(粘贴正文给我,或描述结构要点)
3. 想要的字数和引流强度?(1500 软引流 / 2500-3000 干货 / 1200 短钩子)

[收到答复后,如有缺口,问第二轮]
4. 用不用真实诊断案例?哪个客户,是否脱敏沿用,数字是否能公开?
5. 文末引流方式?(关键词回复 + 扫码 / 仅扫码 / 不引流仅品牌曝光)

[全部对齐后才进入 Step 1]
```

---

## 维护建议

- 每发布 1 篇正式文章,把 markdown 主稿存到 `reference-examples/`,作为下次写作的 few-shot 素材
- 品牌系统变更时,先更新 memory `project_cosle_brand_v1.md`,再同步 `brand-system.md`
- 视觉系统调整时,先更新 `templates/` 下的脚本,再回填到 `brand-system.md` 的「视觉系统」段

```
最后更新:2026-05-20
基于:公众号 v3 首发版(Alexa for Shopping)+ v2.0 第二篇(Listing 5 类信息)的真实落地经验
```
