#!/usr/bin/env python3
"""Confronto fotografia / modello delle due torri-pinnacolo (v3.2).

Ritaglia dalla fotografia di riferimento `riferimento_apice.jpg` le due torri,
le affianca ai render dedicati `model_sx.png` / `model_dx.png` e ritaglia
automaticamente il cielo attorno al modello.
"""
from PIL import Image, ImageChops, ImageDraw, ImageFont

W_OUT, H_OUT = 1560, 1460
HEADER = 130
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def auto_crop_sky(im, pad=10):
    """Toglie il cielo uniforme attorno alla torre in un render."""
    rgb = im.convert("RGB")
    px = rgb.load()
    w, h = rgb.size
    bg = px[2, 2]

    def sky(p):
        return (abs(p[0] - bg[0]) < 26 and abs(p[1] - bg[1]) < 26
                and abs(p[2] - bg[2]) < 26)

    xs, ys = [], []
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if not sky(px[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        return rgb
    x0 = max(0, min(xs) - pad)
    x1 = min(w, max(xs) + pad)
    y0 = max(0, min(ys) - pad)
    y1 = min(h, max(ys) + pad)
    return rgb.crop((x0, y0, x1, y1))


def cella(path, box, size, crop_sky=False):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    if crop_sky:
        im = auto_crop_sky(im)
    im.thumbnail(size, Image.LANCZOS)
    return im


def main():
    canvas = Image.new("RGB", (W_OUT, H_OUT), (14, 14, 16))
    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT_B, 34)
    f_lab = ImageFont.truetype(FONT_B, 21)
    f_sub = ImageFont.truetype(FONT_R, 19)

    col_w = (W_OUT - 50) // 4
    pad = 10
    cell_h = H_OUT - HEADER - 76

    sx_ph = cella("riferimento_apice.jpg", (30, 830, 390, 2160), (col_w, cell_h))
    dx_ph = cella("riferimento_apice.jpg", (1785, 830, 2145, 2160), (col_w, cell_h))
    sx_md = cella("model_sx.png", None, (col_w, cell_h))
    dx_md = cella("model_dx.png", None, (col_w, cell_h))

    caselle = [sx_ph, sx_md, dx_ph, dx_md]
    etichette = ["FOTOGRAFIA\ntorre sinistra", "MODELLO v3.2\ntorre sinistra",
                 "FOTOGRAFIA\ntorre destra", "MODELLO v3.2\ntorre destra"]
    for i, (im, lab) in enumerate(zip(caselle, etichette)):
        x0 = 18 + i * (col_w + pad)
        y0 = HEADER + 6
        sfondo = Image.new("RGB", (col_w, cell_h),
                           (150, 182, 222) if i % 2 == 0 else (108, 138, 180))
        sfondo.paste(im, ((col_w - im.width) // 2, (cell_h - im.height) // 2))
        canvas.paste(sfondo, (x0, y0))
        draw.multiline_text((x0 + 4, HEADER + cell_h - 4), lab, font=f_lab,
                            fill=(255, 255, 255), spacing=2)

    draw.text((18, 6),
              "LE DUE TORRI-PINNACOLO — fusto, lancette, carellature e coronamento",
              font=f_title, fill=(255, 255, 255))
    draw.text((18, 50),
              "v3.2 — cinque colonnine scanalate con capitelli fogliati e specchiature in marmo rigato rosa; "
              "due registri di lancette cieche; tre fasce di carellature;",
              font=f_sub, fill=(214, 219, 228))
    draw.text((18, 72),
              "otto doccioni zoomorfi; cornice a tre fili; otto pinnacoli; lanterna traforata col santo; "
              "guglia crochettata con nodo; statua sommitale a figura intera.",
              font=f_sub, fill=(214, 219, 228))
    draw.text((18, 100),
              "Prima della v3.2: prisma con cinque costoloni piatti, due stecche al posto dei doccioni, "
              "tabernacolo a cono e figurina tozza.",
              font=f_sub, fill=(150, 165, 190))

    canvas.save("confronto_torri.png")
    print("confronto_torri.png scritto", canvas.size)


if __name__ == "__main__":
    main()
