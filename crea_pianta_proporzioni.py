#!/usr/bin/env python3
"""Controllo della tracciatura v4.1 sulla pianta moderna. Richiede Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import muri_esterni as m
ROOT = Path(__file__).resolve().parent

def main():
    base = Image.open(ROOT / 'riferimento_perimetro.png').convert('RGB')
    canvas = Image.new('RGB', (1150, 1000), '#eeeae2')
    canvas.paste(base, (25, 90))
    d = ImageDraw.Draw(canvas)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 17)
    def draw(points, color, closed=False):
        pts = [(25 + 215 + (x-124)/m.RAPPORTO_PIANTE,
                90 + 820 + (y-333)/m.RAPPORTO_PIANTE) for x,y in points]
        d.line(pts + ([pts[0]] if closed else []), fill=color, width=4)
    draw(m.PERIMETRO_PX, '#ed5547')
    for _,_,_,poly in m.ANNESSI:
        draw(poly, '#329bdb', True)
    x,y=m.CAMPANILE_PX
    r=m.LATO_CAMPANILE*m.PX_PER_M/2
    draw([(x-r,y-r),(x+r,y-r),(x+r,y+r),(x-r,y+r)], '#e99116', True)
    d.text((25,25), 'SIENA / Muri esterni semplici — controllo proporzioni', font=font, fill='#252a31')
    d.text((650,110), 'Rosso: corpo della chiesa\nBlu: sacrestia e annessi\nArancio: campanile', font=font, fill='#252a31', spacing=10)
    y=240
    for label,value in m.riepilogo_dimensioni().items():
        d.text((650,y), f'{label}\n{value:.2f} m', font=font, fill='#252a31', spacing=5)
        y+=65
    d.text((25,960), 'Scala agganciata alla facciata esistente; altezze indicative, non da rilievo.', font=font, fill='#252a31')
    canvas.save(ROOT/'pianta_proporzioni.png')
if __name__ == '__main__':
    main()
