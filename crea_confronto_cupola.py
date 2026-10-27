#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronto fotografia / v5.0 / v5.1 della cupola e della lanterna.

Prima fascia, tre celle alla stessa altezza:

    riferimento_cupola.jpg      fotografia dal Facciatone
    v50_cupola.png              render della v5.0 (guscio liscio, lanterna
                                a tempietto schiacciato)
    anteprima_cupola.png        render della v5.1 (768 lastre di piombo,
                                lanterna del Bernini rifatta)

Seconda fascia, primo piano della lanterna: fotografia di fianco, v5.0, v5.1.

Uso:  python crea_confronto_cupola.py
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps

W_OUT, H_OUT = 1560, 1580
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ritaglio della fotografia: la cupola dal tamburo alla punta della croce
FOTO_CUPOLA = (0.14, 0.10, 0.94, 0.80)      # frazioni di larghezza/altezza
FOTO_LANTERNA = (0.05, 0.31, 0.95, 0.88)


def cella_foto(percorso, frazioni, size):
    # Le fotografie hanno l'orientamento nell'EXIF: senza questo passaggio la
    # cupola finirebbe coricata su un fianco.
    im = ImageOps.exif_transpose(Image.open(percorso)).convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = frazioni
    im = im.crop((int(w * x0), int(h * y0), int(w * x1), int(h * y1)))
    im.thumbnail(size, Image.LANCZOS)
    return im


def cella_render(percorso, size):
    im = Image.open(percorso).convert("RGB")
    im.thumbnail(size, Image.LANCZOS)
    return im


def incolla(canvas, im, x0, y0, w, h, sfondo):
    riquadro = Image.new("RGB", (w, h), sfondo)
    riquadro.paste(im, ((w - im.width) // 2, (h - im.height) // 2))
    canvas.paste(riquadro, (x0, y0))


def main():
    canvas = Image.new("RGB", (W_OUT, H_OUT), (14, 14, 16))
    draw = ImageDraw.Draw(canvas)
    f_title = ImageFont.truetype(FONT_B, 32)
    f_lab = ImageFont.truetype(FONT_B, 20)
    f_sub = ImageFont.truetype(FONT_R, 18)

    # --- prima fascia: la cupola intera, tre celle ------------------------
    col_w = (W_OUT - 40) // 3
    cell_h = 800
    y0 = 132
    cella = (col_w - 10, cell_h)

    foto = cella_foto("riferimento_cupola.jpg", FOTO_CUPOLA, cella)
    v50 = cella_render("v50_cupola.png", cella)
    v51 = cella_render("anteprima_cupola.png", cella)

    for i, (im, lab) in enumerate(zip(
            (foto, v50, v51),
            ("FOTOGRAFIA ALLEGATA", "MODELLO v5.0", "MODELLO v5.1"))):
        x = 14 + i * (col_w + 6)
        incolla(canvas, im, x, y0, col_w - 10, cell_h,
                (150, 181, 222) if i == 0 else (86, 112, 148))
        draw.text((x + 6, y0 + cell_h + 8), lab, font=f_lab,
                  fill=(255, 255, 255))

    # --- seconda fascia: la lanterna -------------------------------------
    y1 = y0 + cell_h + 52
    h2 = H_OUT - y1 - 16
    larg = (W_OUT - 40) // 3
    foto_l = cella_foto("riferimento_cupola_lanterna.jpg", FOTO_LANTERNA,
                        (larg - 10, h2 - 40))
    v50_l = cella_render("v50_cupola_lanterna.png", (larg - 10, h2 - 40))
    v51_l = cella_render("anteprima_cupola_lanterna.png",
                         (larg - 10, h2 - 40))
    for i, (im, lab) in enumerate(
            ((foto_l, "FOTOGRAFIA — lanterna e mela"),
             (v50_l, "MODELLO v5.0 — lanterna"),
             (v51_l, "MODELLO v5.1 — lanterna"))):
        x = 14 + i * (larg + 6)
        incolla(canvas, im, x, y1, larg - 10, h2 - 40,
                (150, 181, 222) if i == 0 else (86, 112, 148))
        draw.text((x + 6, y1 + h2 - 34), lab, font=f_lab, fill=(255, 255, 255))

    # --- testi ------------------------------------------------------------
    draw.text((14, 8), "LA CUPOLA DEL DUOMO DI SIENA — v5.1",
              font=f_title, fill=(255, 255, 255))
    draw.text((14, 48),
              "v5.1 — la calotta non è più un guscio liscio con una griglia dipinta: sono "
              "768 lastre di piombo, 12 filari × 8 strisce per spicchio, con le pieghe di",
              font=f_sub, fill=(212, 218, 226))
    draw.text((14, 72),
              "giunzione rilevate, otto costoloni a nastro rastremato e il piombo vecchio "
              "dipinto da tre rumori sovrapposti (patina, velature, colature).",
              font=f_sub, fill=(212, 218, 226))
    draw.text((14, 96),
              "v5.0 — superficie di rotazione unica, lastre solo dipinte, lanterna "
              "schiacciata e tetto a cupoletta.",
              font=f_sub, fill=(150, 165, 190))

    canvas.save("confronto_cupola.png")
    print("confronto_cupola.png scritto", canvas.size)


if __name__ == "__main__":
    main()
