#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tavola fotografia / v5.1 / v5.2: cupola, lanterna e fastigio.

Eseguire dalla radice del progetto: python crea_confronto_cupola.py
Richiede Pillow e le quattro anteprime generate da aggiorna_cupola.py.
"""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W_OUT, H_OUT = 1560, 1910
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
try:
    RESAMPLE = Image.Resampling.LANCZOS
except AttributeError:
    RESAMPLE = Image.LANCZOS

FOTO_CUPOLA = (0.14, 0.10, 0.94, 0.80)
FOTO_LANTERNA = (0.05, 0.31, 0.95, 0.88)
FOTO_FASTIGIO = (0.30, 0.10, 0.70, 0.40)
V51_FASTIGIO = (0.36, 0.24, 0.64, 0.46)


def cella(percorso, size, frazioni=None):
    with Image.open(percorso) as sorgente:
        im = ImageOps.exif_transpose(sorgente).convert("RGB")
    if frazioni is not None:
        w, h = im.size
        x0, y0, x1, y1 = frazioni
        im = im.crop((int(w*x0), int(h*y0), int(w*x1), int(h*y1)))
    im.thumbnail(size, RESAMPLE)
    return im


def main():
    canvas = Image.new("RGB", (W_OUT, H_OUT), (14, 14, 16))
    draw = ImageDraw.Draw(canvas)
    title = ImageFont.truetype(FONT_B, 32)
    label = ImageFont.truetype(FONT_B, 20)
    sub = ImageFont.truetype(FONT_R, 18)
    draw.text((14, 10), "LA CUPOLA DEL DUOMO DI SIENA — v5.2", font=title, fill="white")
    draw.text((14, 54), "Calotta ogivale, 768 lastre e 16 costoloni; lanterna con finestre traforate e tetto a otto lobi.", font=sub, fill=(212, 218, 226))
    draw.text((14, 80), "Confronto fotografico e vista precedente: le quote ufficiali e la facciata restano invariate.", font=sub, fill=(212, 218, 226))
    larg = 500
    rows = [
        ("CUPOLA", 120, 760, [("riferimento_cupola.jpg", FOTO_CUPOLA), ("v51_cupola.png", None), ("anteprima_cupola.png", None)]),
        ("LANTERNA", 925, 530, [("riferimento_cupola_lanterna.jpg", FOTO_LANTERNA), ("v51_cupola_lanterna.png", None), ("anteprima_cupola_lanterna.png", None)]),
        ("FASTIGIO", 1500, 350, [("riferimento_cupola_lanterna.jpg", FOTO_FASTIGIO), ("v51_cupola_lanterna.png", V51_FASTIGIO), ("anteprima_cupola_fastigio.png", None)]),
    ]
    for descr, y, h, files in rows:
        for i, (name, crop) in enumerate(files):
            x = 14 + i*516
            bg = (150, 181, 222) if i == 0 else (86, 112, 148)
            panel = Image.new("RGB", (larg, h), bg)
            im = cella(name, (larg, h), crop)
            panel.paste(im, ((larg-im.width)//2, (h-im.height)//2))
            canvas.paste(panel, (x, y))
            draw.text((x+5, y+h+6), f"{('FOTOGRAFIA', 'MODELLO v5.1', 'MODELLO v5.2')[i]} — {descr}", font=label, fill="white")
    canvas.save("confronto_cupola.png")
    print("confronto_cupola.png scritto", canvas.size)


if __name__ == "__main__":
    main()
