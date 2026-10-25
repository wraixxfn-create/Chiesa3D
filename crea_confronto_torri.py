#!/usr/bin/env python3
"""Confronto fotografia / modello delle due torri-pinnacolo (v3.3).

Ritaglia dalla nuova fotografia frontale `riferimento_torri.jpg` le due
torri, le affianca ai render dedicati `model_sx.png` / `model_dx.png`
(rigenerati da `genera_facciata.py`) e ritaglia il cielo attorno al modello.
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


def cella(path, box, size):
    im = Image.open(path).convert("RGB")
    if box:
        im = im.crop(box)
    im.thumbnail(size, Image.LANCZOS)
    return im


def cella_modello(path, size):
    """Render della torre: tiene la banda centrale con la torre, poi
    ritaglia il cielo restante."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    im = im.crop((int(w * 0.20), int(h * 0.01), int(w * 0.84), int(h * 0.99)))
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

    # torri nella fotografia allegata (1997x3043): statua compresa
    sx_ph = cella("riferimento_torri.jpg", (18, 85, 352, 2420), (col_w, cell_h))
    dx_ph = cella("riferimento_torri.jpg", (1642, 85, 1976, 2420), (col_w, cell_h))
    sx_md = cella_modello("model_sx.png", (col_w, cell_h))
    dx_md = cella_modello("model_dx.png", (col_w, cell_h))

    caselle = [sx_ph, sx_md, dx_ph, dx_md]
    etichette = ["FOTOGRAFIA\ntorre sinistra", "MODELLO v3.3\ntorre sinistra",
                 "FOTOGRAFIA\ntorre destra", "MODELLO v3.3\ntorre destra"]
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
              "LE DUE TORRI-PINNACOLO — fusto, lancette, fasce e coronamento",
              font=f_title, fill=(255, 255, 255))
    draw.text((18, 50),
              "v3.3 — fusto a lastre di marmo bianco con tre lesene piatte e due vene salmone; "
              "registro grande di due lancette con ghimberghe piene;",
              font=f_sub, fill=(214, 219, 228))
    draw.text((18, 72),
              "tre fasce a dente di cane; doccioni diagonali agli spigoli; coronamento pieno: "
              "pinnacoletti a bocciolo, guglia fogliata con figure, statua sommitale.",
              font=f_sub, fill=(214, 219, 228))
    draw.text((18, 100),
              "Prima della v3.3: fusto a colonnine su pannelli rosa a righe e lanterna traforata "
              "con vani neri, che nella fotografia non esiste.",
              font=f_sub, fill=(150, 165, 190))

    canvas.save("confronto_torri.png")
    print("confronto_torri.png scritto", canvas.size)


if __name__ == "__main__":
    main()
