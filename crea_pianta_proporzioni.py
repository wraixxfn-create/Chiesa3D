#!/usr/bin/env python3
"""Tavola di controllo v4.2: pianta e altezze riferite alla facciata."""
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

    def draw(points, color, closed=False, width=4):
        pts = [(25 + 215 + (x - 124) / m.RAPPORTO_PIANTE,
                105 + 820 + (y - 333) / m.RAPPORTO_PIANTE)
               for x, y in points]
        d.line(pts + ([pts[0]] if closed else []), fill=color, width=width)

    draw(m.PERIMETRO_PX, "#ed5547")
    for _, _, _, poly in m.ANNESSI:
        draw(poly, "#329bdb", True)
    x, y = m.CAMPANILE_PX
    r = m.LATO_CAMPANILE * m.PX_PER_M / 2
    draw([(x-r, y-r), (x+r, y-r), (x+r, y+r), (x-r, y+r)],
         "#e99116", True)
    xd, yd = m.ESAGONO_PX
    rd = m.R_TAMBURO * m.PX_PER_M
    esagono = [(xd + rd * math.cos(i*math.pi/3),
                yd + rd * math.sin(i*math.pi/3)) for i in range(6)]
    draw(esagono, "#9b59b6", True)

    d.text((25, 24), "SIENA / Corpo della chiesa — controllo proporzioni v4.2",
           font=title, fill="#252a31")
    d.text((25, 62), "Facciata v3.9 invariata: larghezza 30 m, altezza 37,5 m",
           font=subtitle, fill="#525860")
    d.text((650, 108),
           "Rosso: perimetro\nBlu: sacrestia e annessi\n"
           "Arancio: campanile\nViola: tamburo / cupola",
           font=small, fill="#252a31", spacing=6)

    d.text((650, 260), "PIANTA — metri reali", font=subtitle, fill="#252a31")
    yy = 305
    for label, value in m.riepilogo_dimensioni().items():
        d.text((650, yy), f"{label}\n{value:.2f} m", font=small,
               fill="#252a31", spacing=3)
        yy += 72

    d.text((1110, 260), "ALTEZZE — metri reali", font=subtitle, fill="#252a31")
    yy = 305
    for label, value in m.riepilogo_altezze().items():
        d.text((1110, yy), f"{label}\n{value:.2f} m", font=small,
               fill="#252a31", spacing=3)
        yy += 72
    d.text((1110, yy + 8),
           "Rapporti con la facciata\nCupola: 1,280 ×\nCampanile: 2,053 ×",
           font=small, fill="#525860", spacing=6)

    d.text((25, 1005),
           "Una sola scala uniforme agganciata alla facciata; nessuno stiramento indipendente degli assi X/Y.",
           font=small, fill="#252a31")
    canvas.save(ROOT / "pianta_proporzioni.png")


if __name__ == "__main__":
    main()
