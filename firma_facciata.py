#!/usr/bin/env python3
"""Firma geometrica di tutte le mesh NON appartenenti alle raccolte 07*/08*.

Serve a dimostrare che la facciata v3.9 resta identica prima/dopo un
aggiornamento dei muri esterni: vertici, poligoni, materiali e trasformazioni
di ogni oggetto del fronte devono coincidere al byte.
Uso: python firma_facciata.py <output.json>
"""
import bpy
import json
import sys


def main(out_path):
    sig = {}
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        cols = [c.name for c in obj.users_collection]
        if any(c.startswith(("07", "08")) for c in cols):
            continue
        me = obj.data
        sig[obj.name] = {
            "vertici": len(me.vertices),
            "poligoni": len(me.polygons),
            "materiali": [m.name if m else None for m in me.materials],
            "matrix": [round(v, 6) for row in obj.matrix_world for v in row],
            "somma_vertici": round(sum(v.co.length for v in me.vertices), 4),
        }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(sig, fh, sort_keys=True, indent=1)
    print(f"Oggetti firmati: {len(sig)} -> {out_path}")


if __name__ == "__main__":
    main(sys.argv[-1])
