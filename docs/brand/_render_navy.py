"""Navy lockups: SVG (transparent) + PNG preview."""
from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SCREENS = ROOT.parent / "screens"
FONT = Path(r"C:\Windows\Fonts\segoeuib.ttf")

PRIMARY = (52, 143, 253, 255)
NAVY = (18, 59, 110, 255)
WHITE = (255, 255, 255, 255)
HEX = "#123B6E"
PRI = "#348FFD"


def hexagon(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    k = r / 208.0
    return [
        (cx, cy + (48 - 256) * k),
        (cx + (429.2 - 256) * k, cy + (148 - 256) * k),
        (cx + (429.2 - 256) * k, cy + (364 - 256) * k),
        (cx, cy + (464 - 256) * k),
        (cx + (82.8 - 256) * k, cy + (364 - 256) * k),
        (cx + (82.8 - 256) * k, cy + (148 - 256) * k),
    ]


def draw_y(d: ImageDraw.ImageDraw, cx: float, cy: float, s: float) -> None:
    pts = [
        (cx, cy),
        (cx, cy + 96 * s),
        (cx - 83.1 * s, cy - 48 * s),
        (cx + 83.1 * s, cy - 48 * s),
    ]
    w = max(2, int(14 * s))
    r = max(2, int(18 * s))
    for p in pts[1:]:
        d.line([pts[0], p], fill=WHITE, width=w)
    for x, y in pts:
        d.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)


def draw_mark(size: int, pad: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = size / 2
    r = (size - 2 * pad) / 2
    d.polygon(hexagon(cx, cy, r), fill=NAVY)
    draw_y(d, cx, cy, r / 208.0)
    return img


def crop_pad(img: Image.Image, pad: int) -> Image.Image:
    bbox = img.getbbox()
    cropped = img.crop(bbox)
    out = Image.new("RGBA", (cropped.width + pad * 2, cropped.height + pad * 2), (0, 0, 0, 0))
    out.alpha_composite(cropped, (pad, pad))
    return out


def draw_horizontal() -> Image.Image:
    h = 560
    mark_h = int(h * 0.72)
    mark = draw_mark(mark_h, pad=int(mark_h * 0.04))
    font = ImageFont.truetype(str(FONT), size=int(h * 0.34))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    gap = int(h * 0.10)
    group_w = mark_h + gap + probe.textlength("Asset ", font=font) + probe.textlength("Pro", font=font)
    w = int(group_w + h * 0.4)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    mx = int((w - group_w) / 2)
    my = (h - mark_h) // 2
    img.alpha_composite(mark, (mx, my))
    d = ImageDraw.Draw(img)
    tx = mx + mark_h + gap
    ty = h * 0.50
    d.text((tx, ty), "Asset ", font=font, fill=NAVY, anchor="lm")
    d.text((tx + d.textlength("Asset ", font=font), ty), "Pro", font=font, fill=PRIMARY, anchor="lm")
    return crop_pad(img, int(h * 0.12))


def draw_stacked() -> Image.Image:
    mark = draw_mark(640, pad=28)
    font = ImageFont.truetype(str(FONT), size=96)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    asset_w = probe.textlength("Asset ", font=font)
    pro_w = probe.textlength("Pro", font=font)
    tw = asset_w + pro_w
    gap = 36
    w = max(mark.width, int(tw)) + 80
    h = mark.height + gap + 120 + 40
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    img.alpha_composite(mark, ((w - mark.width) // 2, 20))
    d = ImageDraw.Draw(img)
    tx = (w - tw) / 2
    ty = mark.height + 20 + gap
    d.text((tx, ty), "Asset ", font=font, fill=NAVY, anchor="la")
    d.text((tx + asset_w, ty), "Pro", font=font, fill=PRIMARY, anchor="la")
    return crop_pad(img, 48)


def on_paper(src: Image.Image) -> Image.Image:
    out = Image.new("RGB", (src.width + 80, src.height + 80), (247, 248, 250))
    canvas = Image.new("RGBA", out.size, (247, 248, 250, 255))
    canvas.alpha_composite(src, (40, 40))
    return canvas.convert("RGB")


def save(img: Image.Image, name: str) -> None:
    for folder in (ROOT, SCREENS):
        path = folder / name
        img.save(path, "PNG")
        print(path)


def copy_svgs() -> None:
    for name in (
        "assetpro-logo-nome.svg",
        "assetpro-logo-nome-empilhado.svg",
        "assetpro-logo-marca.svg",
    ):
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, SCREENS / name)
            print(SCREENS / name)


def main() -> None:
    mark = crop_pad(draw_mark(1024, pad=48), 48)
    horiz = draw_horizontal()
    stacked = draw_stacked()
    save(mark, "assetpro-logo-marca.png")
    save(horiz, "assetpro-logo-nome-navy.png")
    save(stacked, "assetpro-logo-nome-empilhado.png")
    save(on_paper(mark), "assetpro-logo-marca-preview.png")
    save(on_paper(horiz), "assetpro-logo-nome-navy-preview.png")
    save(on_paper(stacked), "assetpro-logo-nome-empilhado-preview.png")
    copy_svgs()


if __name__ == "__main__":
    main()
