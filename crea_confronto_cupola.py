#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronto fotografia / v4.4 / v5.0 del gruppo tiburio-cupola-lanterna.

Affianca tre celle alla stessa altezza:

    riferimento_cupola.jpg   fotografia allegata (ritaglio sulla cupola)
    v44_cupola.png           render della v4.4 (calotta "a campana", cilindro)
    anteprima_cupola.png     render della v5.0 (due ordini di logge, lastre,
                             lanterna del Bernini con mela dorata)

E in una seconda fascia il primo piano della lanterna: fotografia e modello.

Uso:  python crea_confronto_cupola.py
"""

from PIL import Image, ImageDraw, ImageFont, ImageOps

W_OUT, H_OUT = 1620, 1560
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# ritaglio della fotografia: la cupola dal tamburo alla punta della croce
FOTO_CUPOLA = (0.14, 0.10, 0.94, 0.80)      # frazioni di larghezza/altezza
FOTO_LANTERNA = (0.30, 0.06, 0.74, 0.28)


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
    cell_h = 900
    y0 = 132
    cella = (col_w - 10, cell_h)

    foto = cella_foto("riferimento_cupola.jpg", FOTO_CUPOLA, cella)
    vecchia = cella_render("/tmp/v44_cupola.png", cella) \
        if __import__("os").path.exists("/tmp/v44_cupola.png") \
        else cella_render("v44_cupola.png", cella)
    nuova = cella_render("anteprima_cupola.png", cella)

    for i, (im, lab) in enumerate(zip(
            (foto, vecchia, nuova),
            ("FOTOGRAFIA ALLEGATA", "MODELLO v4.4", "MODELLO v5.0"))):
        x = 14 + i * (col_w + 6)
        incolla(canvas, im, x, y0, col_w - 10, cell_h,
                (150, 181, 222) if i == 0 else (86, 112, 148))
        draw.text((x + 6, y0 + cell_h + 8), lab, font=f_lab,
                  fill=(255, 255, 255))

    # --- seconda fascia: la lanterna -------------------------------------
    y1 = y0 + cell_h + 52
    h2 = H_OUT - y1 - 16
    larg = (W_OUT - 40) // 2
    foto_l = cella_foto("riferimento_cupola_lanterna.jpg", FOTO_LANTERNA,
                        (larg - 10, h2 - 40))
    mod_l = cella_render("anteprima_cupola_lanterna.png", (larg - 10, h2 - 40))
    for i, (im, lab) in enumerate(((foto_l, "FOTOGRAFIA — lanterna e mela"),
                                   (mod_l, "MODELLO v5.0 — lanterna"))):
        x = 14 + i * (larg + 6)
        incolla(canvas, im, x, y1, larg - 10, h2 - 40,
                (150, 181, 222) if i == 0 else (86, 112, 148))
        draw.text((x + 6, y1 + h2 - 34), lab, font=f_lab, fill=(255, 255, 255))

    # --- testi ------------------------------------------------------------
    draw.text((14, 8), "LA CUPOLA DEL DUOMO DI SIENA — v5.0",
              font=f_title, fill=(255, 255, 255))
    draw.text((14, 48),
              "v5.0 — tamburo a DUE ordini di logge (colonne binate e archi acuti "
              "sotto, colonne singole e archi a tutto sesto sopra), attico bicromo, "
              "fascia bicroma a rombi, dentelli.",
              font=f_sub, fill=(212, 218, 226))
    draw.text((14, 72),
              "Calotta in LASTRE di piombo con otto costoloni e giunti veri, lanterna "
              "del Bernini con bifore, tetto a padiglione e mela dorata; punta della "
              "croce a 48 m.",
              font=f_sub, fill=(212, 218, 226))
    draw.text((14, 96),
              "v4.4 — una calotta emisferica liscia con un cilindro e una crocetta "
              "sopra: nessuna loggia, nessuna lanterna, nessuna lastra.",
              font=f_sub, fill=(150, 165, 190))

    canvas.save("confronto_cupola.png")
    print("confronto_cupola.png scritto", canvas.size)


if __name__ == "__main__":
    main()
