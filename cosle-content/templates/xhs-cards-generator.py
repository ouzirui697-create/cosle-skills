"""
生成小红书图文卡(11 张, 1080x1440 / 3:4)
基于公众号长文 v2.0(Listing 该怎么写)
规则:不含二维码 / 微信号 / 扫码引导,纯知识分享
设计:沿用 Cosle 品牌视觉(深灰 #1F1F1F + 警示红 #E63946)
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path(__file__).parent / "小红书图卡_v2.0_listing写法"
OUT_DIR.mkdir(exist_ok=True)

# 品牌色
BG = (31, 31, 31)              # 深灰主色
RED = (230, 57, 70)            # 警示红
WHITE = (255, 255, 255)
GREY_TEXT = (220, 220, 220)
GREY_MID = (160, 160, 160)
GREY_DARK = (110, 110, 110)
GREY_BG = (45, 45, 45)         # 卡片内浅色块
RED_BG = (60, 30, 35)          # 正确示范暗红底
GREY_BG_2 = (48, 48, 48)       # 错误示范深灰底

PINGFANG = "/System/Library/Fonts/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/HelveticaNeue.ttc"
SFMONO = "/System/Library/Fonts/SFNSMono.ttf"

W, H = 1080, 1440


def load(font_path, size, index=0):
    try:
        return ImageFont.truetype(font_path, size, index=index)
    except Exception:
        return ImageFont.truetype(font_path, size)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def wrap_chinese(text, font, max_w, draw):
    """中文按字符宽度换行"""
    lines = []
    cur = ""
    for ch in text:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        test = cur + ch
        w, _ = measure(draw, test, font)
        if w > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def wrap_english(text, font, max_w, draw):
    """英文按单词换行"""
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        test = (cur + " " + w).strip()
        tw, _ = measure(draw, test, font)
        if tw > max_w and cur:
            lines.append(cur)
            cur = w
        else:
            cur = test
    if cur:
        lines.append(cur)
    return lines


def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    return img, draw


def draw_header(draw, label):
    """顶部品牌标识 — 红条 + 系列标签"""
    draw.rectangle([80, 80, 200, 86], fill=RED)
    f = load(PINGFANG, 26, index=3)
    draw.text((80, 110), label, font=f, fill=GREY_MID)


def draw_footer(draw, page_num, total=11):
    """底部品牌签名 + 页码"""
    f = load(PINGFANG, 24, index=3)
    f_page = load(SFMONO, 22)
    brand_text = "Cosle 跨境卖家实验室  ·  AI 购物时代的研究团队"
    draw.text((80, H - 100), brand_text, font=f, fill=GREY_DARK)
    page_text = f"{page_num:02d} / {total:02d}"
    pw, _ = measure(draw, page_text, f_page)
    draw.text((W - pw - 80, H - 100), page_text, font=f_page, fill=GREY_DARK)


def save(img, name):
    out = OUT_DIR / name
    img.save(out, "PNG", optimize=True)
    return out


# ─────────────────────────────────────────
# 图 01 · 封面
# ─────────────────────────────────────────
def card_01():
    img, draw = new_canvas()
    draw_header(draw, "Cosle 研究笔记 · #002")

    # 主标
    f_main = load(PINGFANG, 84, index=5)  # Semibold
    title_lines = ["AI 购物时代", "你的 Listing", "到底要改什么"]
    y = 360
    for line in title_lines:
        lw, lh = measure(draw, line, f_main)
        draw.text((80, y), line, font=f_main, fill=WHITE)
        y += 110

    # 红色短线
    draw.rectangle([80, y + 20, 220, y + 28], fill=RED)

    # 副标
    f_sub = load(PINGFANG, 38, index=3)
    sub = "写给亚马逊精品卖家的 5 类信息清单"
    draw.text((80, y + 70), sub, font=f_sub, fill=GREY_TEXT)

    # 右侧小字提示
    f_hint = load(SFMONO, 22)
    hints = ["WHO", "WHERE", "WHY", "VS", "NOT"]
    hy = 360
    for i, h in enumerate(hints):
        f_num = load(SFMONO, 16)
        draw.text((W - 220, hy + 4), f"0{i+1}", font=f_num, fill=GREY_DARK)
        draw.text((W - 165, hy), h, font=f_hint, fill=GREY_MID)
        hy += 46

    draw_footer(draw, 1)
    return save(img, "01_封面.png")


# ─────────────────────────────────────────
# 图 02 · 旧公式 vs 新公式
# ─────────────────────────────────────────
def card_02():
    img, draw = new_canvas()
    draw_header(draw, "01 · 为什么要改 Listing")

    f_h2 = load(PINGFANG, 64, index=5)
    draw.text((80, 200), "旧 Listing 写法", font=f_h2, fill=WHITE)
    draw.text((80, 280), "为什么开始失效", font=f_h2, fill=WHITE)

    # 旧公式块
    f_label = load(PINGFANG, 26, index=5)
    f_formula = load(PINGFANG, 30, index=4)
    f_body = load(PINGFANG, 28, index=3)

    box_y = 460
    draw.rectangle([80, box_y, W - 80, box_y + 200], fill=GREY_BG_2)
    draw.text((110, box_y + 30), "A9 时代", font=f_label, fill=GREY_MID)
    f1 = load(PINGFANG, 26, index=4)
    f1_lines = wrap_chinese(
        "自然流量 ≈ 关键词覆盖 × 点击率 × 转化率 × 排名权重",
        f1, W - 220, draw
    )
    yy = box_y + 80
    for line in f1_lines:
        draw.text((110, yy), line, font=f1, fill=WHITE)
        yy += 42

    # 新公式块
    box_y2 = 720
    draw.rectangle([80, box_y2, W - 80, box_y2 + 280], fill=RED_BG)
    draw.rectangle([80, box_y2, 86, box_y2 + 280], fill=RED)
    draw.text((110, box_y2 + 30), "AI 推荐时代", font=f_label, fill=RED)
    formula2 = [
        "能不能被推荐 ≈",
        "COSMO 理解你的场景",
        "+ Rufus 找到能回答 prompt 的素材",
        "+ Alexa+ 认不认你的下单信号"
    ]
    yy = box_y2 + 80
    for line in formula2:
        draw.text((110, yy), line, font=f1, fill=WHITE)
        yy += 44

    # 总结
    f_quote = load(PINGFANG, 30, index=5)
    quote = "A9 看你「写了什么关键词」"
    quote2 = "COSMO 看你「能被归到哪个生活场景」"
    draw.text((80, 1080), quote, font=f_quote, fill=GREY_TEXT)
    draw.text((80, 1130), quote2, font=f_quote, fill=GREY_TEXT)

    draw_footer(draw, 2)
    return save(img, "02_新旧公式对比.png")


# ─────────────────────────────────────────
# 图 03 · 5 类信息总览
# ─────────────────────────────────────────
def card_03():
    img, draw = new_canvas()
    draw_header(draw, "02 · 5 类信息总览")

    f_h2 = load(PINGFANG, 64, index=5)
    draw.text((80, 200), "AI 能读懂的 Listing =", font=f_h2, fill=WHITE)
    draw.text((80, 280), "把这 5 类信息写清楚", font=f_h2, fill=WHITE)

    # 5 类列表
    items = [
        ("01", "WHO", "人群信息", "产品适合谁、写 6 个以上具体人群标签"),
        ("02", "WHERE", "场景信息", "物理场景、时间、使用方式"),
        ("03", "WHY", "决策信息", "可被量化的对比体验点"),
        ("04", "VS", "差异信息", "和 Top 3 竞品到底哪里不一样"),
        ("05", "NOT", "反对信息", "主动说明不适合谁 ★ 90% 卖家漏的"),
    ]

    f_num = load(SFMONO, 28)
    f_en = load(SFMONO, 32)
    f_cn = load(PINGFANG, 32, index=5)
    f_desc = load(PINGFANG, 22, index=3)

    yy = 460
    for num, en, cn, desc in items:
        # 高亮 NOT
        is_special = en == "NOT"
        text_color = RED if is_special else WHITE
        if is_special:
            draw.rectangle([80, yy - 10, W - 80, yy + 130], fill=RED_BG)
            draw.rectangle([80, yy - 10, 86, yy + 130], fill=RED)

        draw.text((110, yy + 6), num, font=f_num, fill=GREY_DARK)
        draw.text((200, yy), en, font=f_en, fill=text_color)
        draw.text((380, yy + 4), cn, font=f_cn, fill=text_color)
        draw.text((110, yy + 70), desc, font=f_desc, fill=GREY_TEXT if not is_special else GREY_TEXT)
        yy += 150

    draw_footer(draw, 3)
    return save(img, "03_5类信息总览.png")


# ─────────────────────────────────────────
# 图 04-08 · 5 类信息详解(通用模板)
# ─────────────────────────────────────────
def card_dim(page_num, num, en, cn, what, why, bad, good, extra=None, is_special=False):
    img, draw = new_canvas()
    draw_header(draw, f"{num} · {en}  {cn}")

    # 大标
    f_num = load(SFMONO, 56)
    f_en = load(SFMONO, 56)
    f_cn = load(PINGFANG, 64, index=5)

    draw.text((80, 180), num, font=f_num, fill=GREY_DARK)
    draw.text((80, 260), en, font=f_en, fill=RED if is_special else WHITE)
    draw.text((80, 340), cn, font=f_cn, fill=WHITE)

    if is_special:
        f_tag = load(PINGFANG, 24, index=5)
        draw.text((80, 420), "★ 这一维 90% 的卖家都漏了", font=f_tag, fill=RED)

    # 它是什么
    f_label = load(PINGFANG, 24, index=5)
    f_body = load(PINGFANG, 28, index=3)

    top_y = 490 if not is_special else 480
    draw.text((80, top_y), "它是什么", font=f_label, fill=RED)
    body_lines = wrap_chinese(what, f_body, W - 160, draw)
    yy = top_y + 42
    for line in body_lines:
        draw.text((80, yy), line, font=f_body, fill=GREY_TEXT)
        yy += 42

    # 为什么需要
    yy += 16
    draw.text((80, yy), "为什么 AI 需要它", font=f_label, fill=RED)
    yy += 42
    why_lines = wrap_chinese(why, f_body, W - 160, draw)
    for line in why_lines:
        draw.text((80, yy), line, font=f_body, fill=GREY_TEXT)
        yy += 42

    # 错误示范
    yy += 20
    box_y = yy
    f_demo_label = load(PINGFANG, 22, index=5)
    f_demo_en = load(SFMONO, 22)
    f_demo_cn = load(PINGFANG, 24, index=3)

    # 判断中英文,选合适的字体和换行函数
    is_chinese_bad = not any(c.isalpha() and ord(c) < 128 for c in bad)
    f_bad = f_demo_cn if is_chinese_bad else f_demo_en
    bad_lines = wrap_chinese(bad, f_bad, W - 200, draw) if is_chinese_bad else wrap_english(bad, f_bad, W - 200, draw)
    bad_h = 60 + len(bad_lines) * 32 + 20
    draw.rectangle([80, box_y, W - 80, box_y + bad_h], fill=GREY_BG_2)
    draw.rectangle([80, box_y, 86, box_y + bad_h], fill=GREY_DARK)
    draw.text((110, box_y + 18), "✗ 错误示范", font=f_demo_label, fill=GREY_MID)
    dy = box_y + 56
    for line in bad_lines:
        draw.text((110, dy), line, font=f_bad, fill=GREY_TEXT)
        dy += 32

    # 正确示范
    yy = box_y + bad_h + 20
    is_chinese_good = not any(c.isalpha() and ord(c) < 128 for c in good)
    f_good = f_demo_cn if is_chinese_good else f_demo_en
    good_lines = wrap_chinese(good, f_good, W - 200, draw) if is_chinese_good else wrap_english(good, f_good, W - 200, draw)
    good_h = 60 + len(good_lines) * 32 + 20
    draw.rectangle([80, yy, W - 80, yy + good_h], fill=RED_BG)
    draw.rectangle([80, yy, 86, yy + good_h], fill=RED)
    draw.text((110, yy + 18), "✓ 正确示范", font=f_demo_label, fill=RED)
    dy = yy + 56
    for line in good_lines:
        draw.text((110, dy), line, font=f_good, fill=WHITE)
        dy += 32

    draw_footer(draw, page_num)
    return img


def card_04():
    img = card_dim(
        page_num=4, num="01", en="WHO", cn="人群信息",
        what="这个产品到底是给谁用的、写明白 6 个以上具体人群标签。",
        why="COSMO 的常识图谱是从「谁搜了什么 → 谁买了什么」推理出来的,人群是它最基础的节点维度。",
        bad="Heavy duty queen bed frame, easy to assemble, noise free.",
        good="Heavy duty queen bed frame for renters, college students, first apartment, guest room, budget family, and easy moving."
    )
    return save(img, "04_01_人群信息.png")


def card_05():
    img = card_dim(
        page_num=5, num="02", en="WHERE", cn="场景信息",
        what="产品在什么物理场景、什么时间、什么使用方式下被用到。",
        why="Rufus 走的是 RAG(检索增强生成),先翻商品库 + 评论 + Q&A,你 Listing 里有没有「能回答场景化 prompt」的素材直接决定它能不能用你做答案。",
        bad="Compact design, suitable for small spaces.",
        good="12-inch under-bed clearance, fits standard 11-inch storage bins—ideal for studio apartments, kids rooms with no closet, and dorm rooms."
    )
    return save(img, "05_02_场景信息.png")


def card_06():
    img = card_dim(
        page_num=6, num="03", en="WHY", cn="决策信息",
        what="AI 替买家做产品对比时会抓哪些可对比的体验点——稳定性、安装难度、承重、噪音、退货风险。",
        why="AI 做对比时抓的不是「heavy duty」这种空词,而是可被量化、可被复述给买家的细节。写得越具体,AI 越敢把你拎出来对比。",
        bad="Sturdy and noise-free.",
        good="12 reinforced steel bars with a center support leg, tested up to 1200 lbs static load. Rubber-padded contact points eliminate squeaking."
    )
    return save(img, "06_03_决策信息.png")


def card_07():
    img = card_dim(
        page_num=7, num="04", en="VS", cn="差异信息",
        what="你和 Top 3 竞品到底哪里不一样。",
        why="Cosle 在诊断里反复看到:一个卖家的 8 条五点有 5、6 条是 Top 3 竞品的同义改写——COSMO 看不出区别,Rufus 也就没法把你单独拎出来推荐。",
        bad="Easy 30-minute assembly, no tools required.",
        good="Unlike most queen bed frames that require 2 people and 45+ minutes, our pre-threaded connector system lets one person assemble it in under 20 minutes."
    )
    return save(img, "07_04_差异信息.png")


def card_08():
    img = card_dim(
        page_num=8, num="05", en="NOT", cn="反对信息",
        what="主动声明「我不适合谁、不适合什么场景」。",
        why="差评里高频「不适合 XXX」会被 Rufus 当成产品负信号。主动写清楚反而能提高推荐精度:错的买家被劝退、对的买家被吸引。",
        bad="留白,什么都不写。",
        good="Not designed for use with box spring (mattress sits directly on slats). Not recommended for ceilings under 7 feet.",
        is_special=True
    )
    return save(img, "08_05_反对信息.png")


# ─────────────────────────────────────────
# 图 09 · 真实案例
# ─────────────────────────────────────────
def card_09():
    img, draw = new_canvas()
    draw_header(draw, "03 · 真实案例")

    f_h2 = load(PINGFANG, 60, index=5)
    draw.text((80, 200), "一个客户的 5 类信息改写", font=f_h2, fill=WHITE)

    f_sub = load(PINGFANG, 28, index=3)
    sub = "家居安全类卖家(脱敏)· 浴室扶手"
    draw.text((80, 290), sub, font=f_sub, fill=GREY_MID)

    # 痛点
    draw.rectangle([80, 360, W - 80, 470], fill=GREY_BG_2)
    draw.rectangle([80, 360, 86, 470], fill=RED)
    f_label = load(PINGFANG, 24, index=5)
    f_body = load(PINGFANG, 28, index=3)
    draw.text((110, 380), "诊断发现", font=f_label, fill=RED)
    draw.text((110, 420), "88.9% 购买发生在 Rufus 答错的 prompt 上", font=f_body, fill=WHITE)

    # 5 类改写
    items = [
        ("人群", "加 elderly / post-surgery / pregnant women"),
        ("场景", "升级为 suction-cup / ideal for renters / no drilling"),
        ("决策", "改为 dual vacuum-lock / 10,000 pull cycles tested"),
        ("差异", "加 Unlike wall-mounted bars that require drilling..."),
        ("反对", "加 Not suitable for textured tile, mosaic, wallpaper"),
    ]

    yy = 510
    f_num = load(SFMONO, 24)
    f_cn = load(PINGFANG, 30, index=5)
    f_en = load(SFMONO, 20)
    for i, (cn, en) in enumerate(items):
        draw.text((110, yy + 6), f"0{i+1}", font=f_num, fill=RED)
        draw.text((180, yy), cn, font=f_cn, fill=WHITE)
        en_lines = wrap_english(en, f_en, W - 380, draw)
        ey = yy + 6
        for line in en_lines:
            draw.text((360, ey), line, font=f_en, fill=GREY_TEXT)
            ey += 28
        yy += 90

    # 结果
    draw.rectangle([80, 1000, W - 80, 1180], fill=RED_BG)
    draw.rectangle([80, 1000, 86, 1180], fill=RED)
    draw.text((110, 1020), "改写后两周", font=f_label, fill=RED)
    f_result = load(PINGFANG, 28, index=5)
    draw.text((110, 1060), "浴室柜误归类消失", font=f_result, fill=WHITE)
    draw.text((110, 1100), "正确场景下推荐频次显著上升", font=f_result, fill=WHITE)
    draw.text((110, 1140), "改写耗时 = 1 个工作日 · 广告预算 = 0", font=f_result, fill=WHITE)

    draw_footer(draw, 9)
    return save(img, "09_真实案例.png")


# ─────────────────────────────────────────
# 图 10 · 但是先别恐慌
# ─────────────────────────────────────────
def card_10():
    img, draw = new_canvas()
    draw_header(draw, "04 · 一份冷静判断")

    f_h2 = load(PINGFANG, 64, index=5)
    draw.text((80, 200), "但是,", font=f_h2, fill=WHITE)
    draw.text((80, 280), "先别恐慌性大改", font=f_h2, fill=WHITE)

    # YouGov 数据
    f_src = load(PINGFANG, 22, index=4)
    draw.text((80, 400), "YouGov · 2026.01 调研", font=f_src, fill=GREY_MID)

    data_items = [
        ("26%", "美国消费者信任零售场景里的 AI"),
        ("14%", "接受自动下单(Buy for Me)"),
        ("43%", "知道 AI 购物助手,但只 14% 用过"),
    ]

    f_big = load(HELVETICA, 110, index=12)  # Thin
    f_desc = load(PINGFANG, 26, index=3)
    yy = 450
    for num, desc in data_items:
        draw.text((80, yy), num, font=f_big, fill=RED)
        # 文字描述
        desc_lines = wrap_chinese(desc, f_desc, W - 380, draw)
        dy = yy + 30
        for line in desc_lines:
            draw.text((360, dy), line, font=f_desc, fill=GREY_TEXT)
            dy += 38
        yy += 150

    # 结论
    draw.rectangle([80, 950, W - 80, 1060], fill=GREY_BG_2)
    f_quote = load(PINGFANG, 32, index=5)
    draw.text((110, 970), "AI 购物助手现在还在", font=f_quote, fill=WHITE)
    draw.text((110, 1010), "「工具」阶段 · 不是「管家」阶段", font=f_quote, fill=RED)

    # 但是
    f_but = load(PINGFANG, 26, index=4)
    draw.text((80, 1110), "但产品比较 / 评论摘要 / 长尾需求匹配", font=f_but, fill=GREY_TEXT)
    draw.text((80, 1150), "这三件事已经开始 100% 依赖 Listing 语义", font=f_but, fill=GREY_TEXT)

    draw_footer(draw, 10)
    return save(img, "10_先别恐慌.png")


# ─────────────────────────────────────────
# 图 11 · 行动建议 + 品牌签名
# ─────────────────────────────────────────
def card_11():
    img, draw = new_canvas()
    draw_header(draw, "05 · 今天就能动手")

    f_h2 = load(PINGFANG, 64, index=5)
    draw.text((80, 200), "从今天开始小改", font=f_h2, fill=WHITE)
    draw.text((80, 280), "三件最便宜的事", font=f_h2, fill=WHITE)

    actions = [
        ("01", "找出 Listing 里最空洞的 3 条五点", "heavy duty / premium quality / easy to use 这种"),
        ("02", "每条补「场景 + 决策 + 差异」", "把参数语言改成场景语言"),
        ("03", "在描述里加一段反对信息", "主动说明不适合谁/什么场景"),
    ]

    f_num = load(SFMONO, 36)
    f_act = load(PINGFANG, 30, index=5)
    f_note = load(PINGFANG, 22, index=3)

    yy = 460
    for num, act, note in actions:
        # 卡片背景
        draw.rectangle([80, yy, W - 80, yy + 160], fill=GREY_BG_2)
        draw.rectangle([80, yy, 86, yy + 160], fill=RED)
        draw.text((110, yy + 30), num, font=f_num, fill=RED)
        draw.text((220, yy + 36), act, font=f_act, fill=WHITE)
        # 备注
        note_lines = wrap_chinese(note, f_note, W - 260, draw)
        ny = yy + 90
        for line in note_lines:
            draw.text((220, ny), line, font=f_note, fill=GREY_MID)
            ny += 30
        yy += 190

    # 品牌签名段
    sig_y = 1080
    draw.rectangle([80, sig_y, W - 80, sig_y + 200], fill=GREY_BG)
    f_sig_label = load(PINGFANG, 22, index=4)
    f_sig_main = load(PINGFANG, 32, index=5)
    f_sig_body = load(PINGFANG, 22, index=3)
    draw.text((110, sig_y + 30), "关于 Cosle", font=f_sig_label, fill=RED)
    draw.text((110, sig_y + 70), "AI 购物时代服务于卖家的研究团队", font=f_sig_main, fill=WHITE)
    draw.text((110, sig_y + 120), "持续追踪 Rufus / Alexa / COSMO 的变化", font=f_sig_body, fill=GREY_TEXT)
    draw.text((110, sig_y + 154), "把 AI 推荐机制对卖家的影响讲清楚", font=f_sig_body, fill=GREY_TEXT)

    draw_footer(draw, 11)
    return save(img, "11_行动+签名.png")


if __name__ == "__main__":
    funcs = [card_01, card_02, card_03, card_04, card_05,
             card_06, card_07, card_08, card_09, card_10, card_11]
    for f in funcs:
        p = f()
        print(f"生成: {p.name}")
    print(f"\n输出目录: {OUT_DIR}")
