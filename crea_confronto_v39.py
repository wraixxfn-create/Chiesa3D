#!/usr/bin/env python3
"""Confronto fotografia / modello v3.9 della facciata d'insieme.

Affianca la fotografia frontale di riferimento (`riferimento_facciata.jpg`)
al render d'insieme `anteprima_facciata.png` rigenerato da
`genera_facciata.py`, alla stessa altezza, con intestazione didattica.
Serve a leggere una accanto all'altra le tre migliorie della v3.9, tutte
sotto la parte centrale superiore (cuspide, rosone e frontoni dei mosaici):

  1. torrioni angolari con archivolti bicromi a cunei su ogni apertura,
     corona ad arco acuto unico con traforo a quatrifoglio e tiburio a
     specchiature modanate, corsi bicromi del basamento intarsiati a filo;
  2. ordine dei portali con raggiera bicroma a pieno campo nelle lunette,
     fregio su fondo scuro, cornici delle porte aggettanti, medaglioni e
     rosoni delle specchiature a rilievo profondo;
  3. gradinata del sagrato a gradoni con naso aggettante e alzata
     rientrante in marmo patinato: le bande si contano una a una.
"""
import os

from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FOTO_PATH = os.path.join(OUT_DIR, "riferimento_facciata.jpg")
RENDER_PATH = os.path.join(OUT_DIR, "anteprima_facciata.png")
OUT_PATH = os.path.join(OUT_DIR, "confronto_v39.png")

H_OUT = 1150
HEADER = 96
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def auto_crop_sky(im, pad=8):
    """Ritaglia il cielo uniforme attorno al modello nel render."""
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
    x0, x1 = max(0, min(xs) - pad), min(w, max(xs) + pad)
    y0, y1 = max(0, min(ys) - pad), min(h, max(ys) + pad)
    return rgb.crop((x0, y0, x1, y1))


def main():
    foto = Image.open(FOTO_PATH).convert("RGB")
    render = auto_crop_sky(Image.open(RENDER_PATH))

    hf = H_OUT
    foto = foto.resize((int(foto.width * hf / foto.height), hf))
    render = render.resize((int(render.width * hf / render.height), hf))

    canvas = Image.new("RGB", (foto.width + render.width + 24,
                               H_OUT + HEADER), (24, 24, 28))
    canvas.paste(foto, (0, HEADER))
    canvas.paste(render, (foto.width + 24, HEADER))

    draw = ImageDraw.Draw(canvas)
    try:
        fb = ImageFont.truetype(FONT_B, 40)
        fr = ImageFont.truetype(FONT_R, 26)
    except OSError:
        fb = fr = ImageFont.load_default()
    draw.text((24, 14), "Duomo di Siena — facciata", font=fb,
              fill=(245, 240, 230))
    draw.text((24, 60), "fotografia di riferimento / modello v3.9 "
                        "(torrioni, portali e gradinata)", font=fr,
              fill=(200, 195, 185))
    draw.text((foto.width + 40, HEADER + 8), "MODELLO v3.9", font=fr,
              fill=(245, 240, 230))
    draw.text((16, HEADER + 8), "FOTOGRAFIA", font=fr,
              fill=(245, 240, 230))
    canvas.save(OUT_PATH)
    print(f"Confronto salvato: {OUT_PATH} ({canvas.width}x{canvas.height})")


if __name__ == "__main__":
    main()
