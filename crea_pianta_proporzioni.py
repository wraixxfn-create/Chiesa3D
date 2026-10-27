#!/usr/bin/env python3
"""Tavola di controllo v4.3: pianta e altezze riferite alla facciata."""
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

import muri_esterni as m

ROOT = Path(__file__).resolve().parent


def _font(size):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def main():
    base = Image.open(ROOT / "riferimento_perimetro.png").convert("RGB")
    canvas = Image.new("RGB", (1500, 1050), "#eeeae2")
    canvas.paste(base, (25, 105))
    d = ImageDraw.Draw(canvas)
    title = _font(23)
    subtitle = _font(18)
    small = _font(15)

    def px(punto):
        x, y = punto
        return (25 + m.PIANTA_ASSE_X + x / m.K_PIANTA,
                105 + m.PIANTA_FACCIATA_Y - (y - m.Y_BACK_M) / m.K_PIANTA)

    def draw(points, color, closed=False, width=4):
        pts = [px(p) for p in points]
        d.line(pts + ([pts[0]] if closed else []), fill=color, width=width)

    draw(m.PERIMETRO, "#ed5547")
    for _, _, _, poly in m.ANNESSI:
        draw(poly, "#329bdb", True)
    x, y = m.CAMPANILE_M
    r = m.LATO_CAMPANILE / 2
    draw([(x-r, y-r), (x+r, y-r), (x+r, y+r), (x-r, y+r)],
         "#e99116", True)
    xd, yd = m.ESAGONO_M
    rd = m.R_TAMBURO
    esagono = [(xd + rd * math.cos(i*math.pi/3),
                yd + rd * math.sin(i*math.pi/3)) for i in range(6)]
    draw(esagono, "#9b59b6", True)
    # Il Duomo Nuovo prosegue oltre il taglio destro della pianta moderna:
    # le sue linee vengono ritagliate al bordo del foglio di riferimento.
    x_max = 25 + 593
    for nome, punti in m.TRATTI_DUOMO_NUOVO:
        pts = [px(p) for p in punti]
        pts = [(min(x, x_max), y) for x, y in pts]
        d.line(pts, fill="#7f8c8d", width=4)

    d.text((25, 24), "SIENA / Corpo della chiesa — controllo proporzioni v4.3",
           font=title, fill="#252a31")
    d.text((25, 62), "Facciata v3.9 invariata: larghezza 30 m, altezza 37,5 m",
           font=subtitle, fill="#525860")
    d.text((650, 108),
           "Rosso: perimetro (assi dei muri)\nBlu: sacrestia e annessi\n"
           "Arancio: campanile\nViola: tamburo / cupola\nGrigio: Duomo Nuovo",
           font=small, fill="#252a31", spacing=6)

    d.text((650, 280), "PIANTA — metri reali", font=subtitle, fill="#252a31")
    yy = 325
    for label, value in m.riepilogo_dimensioni().items():
        d.text((650, yy), f"{label}\n{value:.2f} m", font=small,
               fill="#252a31", spacing=3)
        yy += 66

    d.text((1110, 280), "ALTEZZE — metri reali", font=subtitle,
           fill="#252a31")
    yy = 325
    for label, value in m.riepilogo_altezze().items():
        d.text((1110, yy), f"{label}\n{value:.2f} m", font=small,
               fill="#252a31", spacing=3)
        yy += 66
    d.text((1110, yy + 8),
           "Rapporti con la facciata\nCupola: 1,280 ×\nCampanile: 2,053 ×",
           font=small, fill="#525860", spacing=6)

    d.text((25, 1005),
           "Quote principali dai valori ufficiali (89,4 × 24,37 × 54,48 m interni); "
           "forma dei risalti dalla pianta moderna con scala unica K; facciata da 30 m piu' larga delle fiancate.",
           font=small, fill="#252a31")
    canvas.save(ROOT / "pianta_proporzioni.png")


if __name__ == "__main__":
    main()
