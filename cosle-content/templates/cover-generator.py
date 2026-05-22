"""
生成 Cosle 公众号第二篇封面图(品牌封面通用版)
- 大封面: 900x383
- 小封面: 800x800
风格:沿用 v4 品牌封面,中央 "Cosle" 品牌名 + 副标 "AI 购物时代的卖家研究团队"
本版按用户要求去除左上「文章 #00X」,只保留品牌主视觉
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path(__file__).parent

BG = (31, 31, 31)
RED = (230, 57, 70)
WHITE = (255, 255, 255)
GREY_LIGHT = (200, 200, 200)
GREY_MID = (140, 140, 140)
GREY_DARK = (90, 90, 90)

PINGFANG = "/System/Library/Fonts/PingFang.ttc"
HELVETICA = "/System/Library/Fonts/HelveticaNeue.ttc"


def load(font_path, size, index=0):
    try:
        return ImageFont.truetype(font_path, size, index=index)
    except Exception:
        return ImageFont.truetype(font_path, size)


def measure(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def make_wide():
    """900x383 大封面 — 品牌封面通用版(无文章号)"""
    W, H = 900, 383
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 左上红条(品牌标识保留,无文章号)
    draw.rectangle([45, 38, 130, 42], fill=RED)

    # 中央副标(中文)
    f_subtitle = load(PINGFANG, 22, index=4)  # PingFang Medium
    subtitle = "AI 购物时代的卖家研究团队"
    sw, sh = measure(draw, subtitle, f_subtitle)
    sub_y = 150
    draw.text(((W - sw) // 2, sub_y), subtitle, font=f_subtitle, fill=GREY_LIGHT)

    # 中央主标 Cosle(英文,Helvetica Neue Thin)
    f_brand = load(HELVETICA, 110, index=12)
    brand = "Cosle"
    bw, bh = measure(draw, brand, f_brand)
    draw.text(((W - bw) // 2, sub_y + 40), brand, font=f_brand, fill=WHITE)

    # 右下角
    f_bottom = load(PINGFANG, 13, index=2)
    bottom_text = "Alexa for Shopping  ·  2026.05"
    bw2, bh2 = measure(draw, bottom_text, f_bottom)
    draw.text((W - bw2 - 45, H - 38), bottom_text, font=f_bottom, fill=GREY_DARK)

    out = OUT_DIR / "公众号头图_v2.0_listing写法.png"
    img.save(out, "PNG", optimize=True)
    return out


def make_square():
    """800x800 小封面 — 品牌封面通用版(无文章号)"""
    W, H = 800, 800
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 左上红条(品牌标识保留,无文章号)
    draw.rectangle([55, 70, 175, 76], fill=RED)

    # 中央副标
    f_subtitle = load(PINGFANG, 30, index=4)
    subtitle = "AI 购物时代的卖家研究团队"
    sw, sh = measure(draw, subtitle, f_subtitle)
    sub_y = 320
    draw.text(((W - sw) // 2, sub_y), subtitle, font=f_subtitle, fill=GREY_LIGHT)

    # 中央主标 Cosle (Helvetica Neue Thin)
    f_brand = load(HELVETICA, 170, index=12)
    brand = "Cosle"
    bw, bh = measure(draw, brand, f_brand)
    draw.text(((W - bw) // 2, sub_y + 60), brand, font=f_brand, fill=WHITE)

    # 底部居中
    f_bottom = load(PINGFANG, 16, index=2)
    bottom_text = "Alexa for Shopping  ·  2026.05"
    bw2, bh2 = measure(draw, bottom_text, f_bottom)
    draw.text(((W - bw2) // 2, H - 80), bottom_text, font=f_bottom, fill=GREY_DARK)

    out = OUT_DIR / "公众号小封面_1x1_v2.0_listing写法.png"
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    p1 = make_wide()
    p2 = make_square()
    print(f"生成: {p1}")
    print(f"生成: {p2}")
