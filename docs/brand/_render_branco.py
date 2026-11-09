"""Render Asset Pro white logos as true RGBA PNGs + navy preview."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
SCREENS = ROOT.parent / "screens"
FONT = Path(r"C:\Windows\Fonts\segoeuib.ttf")

PRIMARY = (52, 143, 253, 255)  # #348FFD
NAVY = (18, 59, 110, 255)  # #123B6E
WHITE = (255, 255, 255, 255)


def hexagon(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    # same proportions as the color SVG (pointy top, R≈208 in 512 viewBox)
    k = r / 208.0
    return [
        (cx + (256 - 256) * k, cy + (48 - 256) * k),
        (cx + (429.2 - 256) * k, cy + (148 - 256) * k),
        (cx + (429.2 - 256) * k, cy + (364 - 256) * k),
        (cx + (256 - 256) * k, cy + (464 - 256) * k),
        (cx + (82.8 - 256) * k, cy + (364 - 256) * k),
        (cx + (82.8 - 256) * k, cy + (148 - 256) * k),
    ]


def punch_y(img: Image.Image, cx: float, cy: float, scale: float) -> None:
    """Cut the Y-network out of a white hexagon (transparent holes)."""
    hole = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(hole)
    s = scale
    pts = [
        (cx, cy),
        (cx, cy + 96 * s),
        (cx - 83.1 * s, cy - 48 * s),
        (cx + 83.1 * s, cy - 48 * s),
    ]
    w = max(2, int(14 * s))
    r = max(2, int(18 * s))
    d.line([pts[0], pts[1]], fill=255, width=w)
    d.line([pts[0], pts[2]], fill=255, width=w)
    d.line([pts[0], pts[3]], fill=255, width=w)
    for x, y in pts:
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    img.putalpha(
        Image.composite(
            Image.new("L", img.size, 0),
            img.getchannel("A"),
            hole,
        )
    )


def draw_mark(size: int, pad: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = cy = size / 2
    r = (size - 2 * pad) / 2
    d.polygon(hexagon(cx, cy, r), fill=WHITE)
    punch_y(img, cx, cy, r / 208.0)
    return img


def draw_lockup(w: int, h: int) -> Image.Image:
    mark_h = int(h * 0.72)
    mark = draw_mark(mark_h, pad=int(mark_h * 0.04))
    font = ImageFont.truetype(str(FONT), size=int(h * 0.34))
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    gap = int(h * 0.10)
    group_w = mark_h + gap + probe.textlength("Asset ", font=font) + probe.textlength("Pro", font=font)

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    mx = int((w - group_w) / 2)
    my = (h - mark_h) // 2
    img.alpha_composite(mark, (mx, my))
    d = ImageDraw.Draw(img)
    text_x = mx + mark_h + gap
    text_y = h * 0.50
    d.text((text_x, text_y), "Asset ", font=font, fill=WHITE, anchor="lm")
    aw = d.textlength("Asset ", font=font)
    d.text((text_x + aw, text_y), "Pro", font=font, fill=PRIMARY, anchor="lm")

    bbox = img.getbbox()
    cropped = img.crop(bbox)
    pad = int(h * 0.14)
    out = Image.new("RGBA", (cropped.width + pad * 2, cropped.height + pad * 2), (0, 0, 0, 0))
    out.alpha_composite(cropped, (pad, pad))
    return out


def on_navy(src: Image.Image, pad: int = 64) -> Image.Image:
    out = Image.new("RGBA", (src.width + pad * 2, src.height + pad * 2), NAVY)
    out.alpha_composite(src, (pad, pad))
    return out.convert("RGB")


def save(img: Image.Image, name: str) -> None:
    for folder in (ROOT, SCREENS):
        path = folder / name
        img.save(path, "PNG")
        print(path)


def main() -> None:
    mark = draw_mark(1024, pad=64)
    lockup = draw_lockup(2000, 560)
    save(mark, "assetpro-logo-marca-branco.png")
    save(lockup, "assetpro-logo-nome-branco.png")
    save(on_navy(mark, 80), "assetpro-logo-marca-branco-preview.png")
    save(on_navy(lockup, 80), "assetpro-logo-nome-branco-preview.png")

    sheet = Image.new("RGB", (2000, 1100), NAVY)
    m = mark.resize((420, 420), Image.Resampling.LANCZOS)
    l = lockup.resize((1680, 470), Image.Resampling.LANCZOS)
    tmp = Image.new("RGBA", sheet.size, NAVY)
    tmp.alpha_composite(m, (790, 80))
    tmp.alpha_composite(l, (160, 560))
    save(tmp.convert("RGB"), "assetpro-logo-branco-preview.png")


if __name__ == "__main__":
    main()
