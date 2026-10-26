#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Disegno quotato di controllo: la pianta allegata con sopra la tracciatura
dei muri esterni generati da `muri_esterni.py` e le quote in metri reali.

Serve a verificare a colpo d'occhio che le PROPORZIONI del modello 3D
corrispondano alla pianta:

    python crea_pianta_proporzioni.py     -> pianta_proporzioni.png

Richiede solo Pillow (come gli altri script di confronto del progetto).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

import muri_esterni as ME

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
PIANTA = os.path.join(OUT_DIR, "riferimento_pianta.jpg")
OUT = os.path.join(OUT_DIR, "pianta_proporzioni.png")

S = 2                      # ingrandimento della pianta
OX, OY = 150, 120          # origine della pianta nel canvas
W, H = 1780, 1030
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
F_TITLE = ImageFont.truetype(FONT_B, 27)
F_SUB = ImageFont.truetype(FONT_R, 17)
F_DIM = ImageFont.truetype(FONT_B, 15)
F_TAB = ImageFont.truetype(FONT_R, 17)
F_TABB = ImageFont.truetype(FONT_B, 17)
F_LEG = ImageFont.truetype(FONT_R, 16)

ROSSO = (215, 45, 45)
BLU = (35, 90, 205)
ARANCIO = (235, 140, 30)
VIOLA = (145, 60, 170)
VERDE = (30, 145, 90)
GRIGIO = (95, 115, 140)
NERO = (35, 38, 42)
BIANCO = (255, 255, 255)


def X(px):
    return OX + px * S


def Y(px):
    return OY + px * S


def freccia(d, p, q, colore=NERO, larg=2):
    """Linea con due punte di freccia."""
    d.line([p, q], fill=colore, width=larg)
    ang = math.atan2(q[1] - p[1], q[0] - p[0])
    for estremita, verso in ((p, ang), (q, ang + math.pi)):
        for delta in (-0.42, 0.42):
            a = verso + math.pi + delta
            tip = (estremita[0] + 11 * math.cos(a),
                   estremita[1] + 11 * math.sin(a))
            d.line([estremita, tip], fill=colore, width=larg)


def etichetta(d, testo, x, y, font=F_DIM, colore=NERO, sfondo=BIANCO):
    box = d.textbbox((0, 0), testo, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.rectangle([x - tw / 2 - 5, y - th / 2 - 4,
                 x + tw / 2 + 5, y + th / 2 + 4], fill=sfondo)
    d.text((x - tw / 2, y - th / 2 - 2), testo, font=font, fill=colore)


def quota_h(d, x0, x1, y, testo, colore=NERO):
    freccia(d, (X(x0), y), (X(x1), y), colore)
    d.line([(X(x0), y - 10), (X(x0), y + 10)], fill=colore, width=1)
    d.line([(X(x1), y - 10), (X(x1), y + 10)], fill=colore, width=1)
    etichetta(d, testo, (X(x0) + X(x1)) / 2, y - 14)


def quota_v(d, y0, y1, x, testo, colore=NERO):
    freccia(d, (x, Y(y0)), (x, Y(y1)), colore)
    d.line([(x - 10, Y(y0)), (x + 10, Y(y0))], fill=colore, width=1)
    d.line([(x - 10, Y(y1)), (x + 10, Y(y1))], fill=colore, width=1)
    # testo ruotato di 90° per non coprire il disegno
    tmp = Image.new("RGBA", (340, 34), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    box = td.textbbox((0, 0), testo, font=F_DIM)
    tw = box[2] - box[0]
    td.rectangle([0, 0, tw + 10, 30], fill=(*BIANCO, 235))
    td.text((5 - box[0], 3 - box[1]), testo, font=F_DIM, fill=colore)
    rot = tmp.rotate(90, expand=True)
    canvas.paste(rot, (int(x - rot.width / 2),
                       int((Y(y0) + Y(y1)) / 2 - rot.height / 2)), rot)


def polilinea(d, punti, colore, larg=3, tratteggio=False, chiuso=False):
    pts = [(X(a), Y(b)) for a, b in punti]
    if chiuso:
        pts.append(pts[0])
    if not tratteggio:
        d.line(pts, fill=colore, width=larg, joint="curve")
    else:
        for p, q in zip(pts[:-1], pts[1:]):
            lung = math.dist(p, q)
            n = max(1, int(lung // 12))
            for i in range(n):
                if i % 2 == 0:
                    t0, t1 = i / n, min(1.0, (i + 0.6) / n)
                    d.line([(p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0),
                            (p[0] + (q[0] - p[0]) * t1, p[1] + (q[1] - p[1]) * t1)],
                           fill=colore, width=larg)
    for p in pts:
        d.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=colore)


def cerchio(d, cx_px, cy_px, r_px, colore, larg=3):
    d.ellipse([X(cx_px - r_px), Y(cy_px - r_px),
               X(cx_px + r_px), Y(cy_px + r_px)],
              outline=colore, width=larg)


# -----------------------------------------------------------------------------
# Canvas e pianta di riferimento
# -----------------------------------------------------------------------------
canvas = Image.new("RGB", (W, H), (247, 246, 242))
d = ImageDraw.Draw(canvas)
pianta = Image.open(PIANTA).convert("RGB").resize(
    (487 * S, 431 * S), Image.LANCZOS)
canvas.paste(pianta, (OX, OY))
d = ImageDraw.Draw(canvas)
d.rectangle([OX, OY, OX + 487 * S, OY + 431 * S], outline=(190, 190, 185), width=2)

d.text((OX, 24), "DUOMO DI SIENA — taratura dei muri esterni (v4.0)",
       font=F_TITLE, fill=NERO)
d.text((OX, 62), "Pianta allegata con la tracciatura usata dal generatore: "
       "3 px = 1 m reale  •  1 m reale = 3 unità modello (scala_globale = 3.0)",
       font=F_SUB, fill=(80, 84, 90))

# -----------------------------------------------------------------------------
# Tracciatura
# -----------------------------------------------------------------------------
polilinea(d, ME.PERIMETRO_PX, ROSSO, larg=3, chiuso=False)
# il lato ovest (facciata) e' il modello esistente: tratteggio blu
d.line([(X(124), Y(333)), (X(209), Y(333))], fill=BLU, width=4)
polilinea(d, [(124, 341), (209, 341)], BLU, larg=3)

for _nome, _col, _altezza, poly in ME.ANNESSI:
    polilinea(d, poly, ARANCIO, larg=3, chiuso=True)

for _nome, x, y in ME.CAPPELLE_TONDE:
    cerchio(d, x, y, ME.R_CAPPELLA * ME.PX_PER_M, VERDE)

# campanile: quadrato ruotato di 45° (come nella pianta)
cx_c, cy_c = ME.CAMPANILE_PX
r = ME.LATO_CAMPANILE * ME.PX_PER_M / math.sqrt(2.0)
polilinea(d, [(cx_c - r, cy_c), (cx_c, cy_c - r),
              (cx_c + r, cy_c), (cx_c, cy_c + r)], VIOLA, larg=3, chiuso=True)

# tamburo esagonale della cupola
cx_e, cy_e = ME.ESAGONO_PX
raggio_px = ME.R_TAMBURO * ME.PX_PER_M
hex_pts = [(cx_e + raggio_px * math.cos(i * math.pi / 3),
            cy_e + raggio_px * math.sin(i * math.pi / 3))
           for i in range(6)]
polilinea(d, hex_pts, VERDE, larg=3, chiuso=True)

# Duomo Nuovo (incompiuto)
for _nome, pts in ME.TRATTI_DUOMO_NUOVO:
    polilinea(d, pts, GRIGIO, larg=3)

# -----------------------------------------------------------------------------
# Quote (metri reali, dalla scala grafica della pianta)
# -----------------------------------------------------------------------------
quota_h(d, 121, 212, Y(47) - 34, "30,3 m  navata = facciata", colore=ROSSO)
quota_h(d, 76, 253, Y(210) + 48, "59,0 m  larghezza transetto", colore=ROSSO)
# Le quote verticali stanno tutte nel margine sinistro: non coprono il
# disegno né la tabella a destra.
quota_v(d, 341, 47, X(18), "98,0 m  lunghezza totale esterna")
quota_v(d, 333, 210, X(43), "41,0 m  navata")
quota_v(d, 333, 178, X(68), "51,7 m  facciata → cupola")
quota_v(d, 128, 47, X(93), "27,0 m  coro")

# -----------------------------------------------------------------------------
# Legenda + tabella quote
# -----------------------------------------------------------------------------
LX = OX + 487 * S + 36
LY = OY + 10
d.text((LX, LY - 46), "LEGENDA", font=F_TABB, fill=NERO)
voci = [
    (ROSSO, "Perimetro dei muri esterni (navata, transetto, coro)"),
    (BLU, "Facciata ovest già modellata (non ricostruita)"),
    (ARANCIO, "Annessi / sacrestie / blocco battistero"),
    (VERDE, "Tamburo esagonale e cappelle tonde"),
    (VIOLA, "Campanile, quadrato ruotato di 45°"),
    (GRIGIO, "Duomo Nuovo: progetto mai completato"),
]
for i, (col, txt) in enumerate(voci):
    yy = LY + i * 30
    d.line([(LX, yy + 9), (LX + 34, yy + 9)], fill=col, width=5)
    d.text((LX + 44, yy), txt, font=F_LEG, fill=NERO)

TY = LY + len(voci) * 30 + 40
d.text((LX, TY), "QUOTE IN METRI REALI", font=F_TABB, fill=NERO)
dim = ME.riepilogo_dimensioni()
righe = [
    ("Larghezza esterna navata", dim["Larghezza esterna navata"]),
    ("Lunghezza navata", dim["Lunghezza navata (facciata->transetto)"]),
    ("Larghezza esterna transetto", dim["Larghezza esterna transetto"]),
    ("Profondità transetto", dim["Profondita' transetto"]),
    ("Profondità coro", dim["Profondita' coro"]),
    ("Lunghezza totale esterna", dim["Lunghezza totale esterna"]),
    ("Distanza facciata → cupola", dim["Distanza facciata->centro cupola"]),
    ("Diametro tamburo esagonale", dim["Diametro tamburo esagonale"]),
    ("Altezza muri (semplice)", dim["Altezza muri (semplice)"]),
    ("Altezza colmo cupola", dim["Altezza colmo cupola (semplice)"]),
    ("Altezza campanile", dim["Altezza campanile (semplice)"]),
]
d.text((LX, TY + 32), "misura", font=F_TABB, fill=(90, 94, 100))
d.text((LX + 320, TY + 32), "m reali", font=F_TABB, fill=(90, 94, 100))
d.text((LX + 430, TY + 32), "u. modello", font=F_TABB, fill=(90, 94, 100))
d.line([(LX, TY + 56), (LX + 540, TY + 56)], fill=(190, 190, 185), width=1)
for i, (nome, val) in enumerate(righe):
    yy = TY + 66 + i * 30
    d.text((LX, yy), nome, font=F_TAB, fill=NERO)
    d.text((LX + 320, yy), f"{val:.1f}", font=F_TABB, fill=ROSSO)
    d.text((LX + 430, yy), f"{val * 3.0:.0f}", font=F_TAB, fill=BLU)

NY = TY + 72 + len(righe) * 30 + 18
note = [
    "Verifica: la facciata del modello è larga 30 m reali",
    "(90 u.m.): coincide con i 30,3 m dei muri della navata.",
    "L'interno reale è 89,4 m; i ~98 m qui sono esterni,",
    "muro compreso, come nella pianta del libro.",
]
for i, t in enumerate(note):
    d.text((LX, NY + i * 25), t, font=F_LEG, fill=(80, 84, 90))

canvas.save(OUT)
print(f"Salvato: {OUT} ({canvas.width}x{canvas.height})")
