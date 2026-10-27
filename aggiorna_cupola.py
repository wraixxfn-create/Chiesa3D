#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rigenera soltanto il gruppo TIBURIO + CALOTTA + LANTERNA (v5.1).

Apre `Facciata_Duomo_Siena.blend`, cancella gli oggetti della raccolta
`07d_Tiburio_e_Cupola` e li ricostruisce con `cupola.py`; opzionalmente
salva il .blend e produce le anteprime dedicate.

Uso (Blender 4.2+ oppure modulo pip `bpy`):

    python aggiorna_cupola.py
    blender --background --python aggiorna_cupola.py

Variabili d'ambiente:

    CHIESA_CUPOLA_BLEND=...    .blend di partenza (default Facciata_Duomo_Siena.blend)
    CHIESA_CUPOLA_OUT=...      .blend di destinazione (default: sovrascrive)
    CHIESA_CUPOLA_BACKUP=1     salva una copia .bak prima di sovrascrivere
    CHIESA_CUPOLA_NO_RENDER=1  non generare le anteprime
    CHIESA_CUPOLA_SAMPLES=24   campioni Cycles delle anteprime
    CHIESA_CUPOLA_RES=900x1150 risoluzione delle viste della cupola

La facciata e il resto del corpo non vengono toccati: tutto il lavoro avviene
dentro la raccolta `07d*`.
"""

import json
import math
import os
import sys

import bpy
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
if OUT_DIR not in sys.path:
    sys.path.insert(0, OUT_DIR)

from cupola import costruisci_cupola  # noqa: E402

CFG_PATH = os.path.join(OUT_DIR, "config_facciata.json")
BLEND_PATH = os.environ.get(
    "CHIESA_CUPOLA_BLEND", os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend"))
OUT_PATH = os.environ.get("CHIESA_CUPOLA_OUT", BLEND_PATH)

with open(CFG_PATH, "r", encoding="utf-8") as fh:
    CFG = json.load(fh)

SCALA = float(CFG.get("dimensioni", {}).get(
    "scala_globale", CFG.get("meta", {}).get("scala_finale", 3.0)))
CUPOLA_CFG = dict(CFG.get("muri_esterni", {}))
CUPOLA_CFG.update(CFG.get("cupola", {}))

print(f"Carico: {BLEND_PATH}")
bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
print(f"Oggetti prima: {len(bpy.data.objects)} | scala globale: {SCALA}")


# -----------------------------------------------------------------------------
# Ricostruzione del gruppo cupola
# -----------------------------------------------------------------------------
def _collezione(nome, parent=None):
    c = bpy.data.collections.get(nome)
    if c is None:
        c = bpy.data.collections.new(nome)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


root = _collezione("07_Corpo_Chiesa")
col = _collezione("07d_Tiburio_e_Cupola", root)

# idempotenza: via i vecchi oggetti del tiburio (calotta "a campana" v4.4)
for _o in list(col.objects):
    bpy.data.objects.remove(_o, do_unlink=True)

risultato = costruisci_cupola(scala=SCALA, cfg=CUPOLA_CFG, col=col)
print(f"Oggetti dopo: {len(bpy.data.objects)} | "
      f"vertici cupola: {risultato['vertici']}")

# -----------------------------------------------------------------------------
# Camere di servizio per le anteprime (non toccano la camera della scena)
# -----------------------------------------------------------------------------
CAM_COL = "08b_Camere_Cupola"
_cam_col = bpy.data.collections.get(CAM_COL)
if _cam_col is not None:
    for _o in list(_cam_col.objects):
        bpy.data.objects.remove(_o, do_unlink=True)
    bpy.data.collections.remove(_cam_col, do_unlink=True)


def _camera(nome, target, distanza, azimuth, elevazione, lens):
    """Camera prospettica a distanza fissa dal centro del tiburio."""
    dati = bpy.data.cameras.new(nome)
    dati.lens = lens
    dati.clip_start = 0.5
    dati.clip_end = 6000.0
    cam = bpy.data.objects.new(nome, dati)
    _collezione(CAM_COL).objects.link(cam)
    az, el = math.radians(azimuth), math.radians(elevazione)
    loc = Vector(target) + Vector((
        math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el),
        math.sin(el))) * distanza
    cam.location = loc
    cam.rotation_euler = (Vector(target) - loc).to_track_quat(
        "-Z", "Y").to_euler()
    return cam


# centro del tiburio: lo stesso esagono della crociera
from muri_esterni import ESAGONO_M  # noqa: E402

cx, cy = ESAGONO_M
centro = (cx * SCALA, cy * SCALA, 0.0)


def _bersaglio(z_m):
    return (centro[0], centro[1], z_m * SCALA)


cam_cupola = _camera("Camera_Cupola_3Q", _bersaglio(36.0), 205.0, 20.0, 9.0,
                     85.0)
# Il sole del .blend arriva da destra (rotazione Z 52,7): le camere della
# cupola stanno dallo stesso lato, cosi' la calotta e la lanterna sono in luce
# come nelle fotografie allegate invece che in controluce.
cam_lanterna = _camera("Camera_Cupola_Lanterna", _bersaglio(45.2), 82.0, 18.0,
                       8.0, 85.0)
cam_tamburo = _camera("Camera_Cupola_Tamburo", _bersaglio(27.6), 148.0, 12.0,
                      8.0, 85.0)

def _luce_riempimento_cupola():
    """Due soli deboli di riempimento per le anteprime.

    Il sole del .blend e' basso (19,6 gradi): con quella luce il tetto in
    piombo della lanterna tiene in ombra tutto il colonnato sottostante e la
    cupola si legge male.  Queste luci vengono create DOPO il salvataggio,
    quindi il .blend resta con l'illuminazione calibrata sulla facciata.
    """
    out = []
    for nome, energia, rz, rx in (
            ("Luce_Riempimento_Cupola_A", 1.6, 52.0, 34.0),
            ("Luce_Riempimento_Cupola_B", 0.9, -60.0, 46.0)):
        dati = bpy.data.lights.new(nome, type="SUN")
        dati.energy = energia
        dati.angle = math.radians(18.0)
        dati.color = (0.92, 0.94, 1.0)
        obj = bpy.data.objects.new(nome, dati)
        _collezione(CAM_COL).objects.link(obj)
        obj.rotation_euler = (math.radians(rx), 0.0, math.radians(rz))
        out.append(obj)
    return out


scene = bpy.context.scene
camera_originale = scene.camera
res_originale = (scene.render.resolution_x, scene.render.resolution_y)
samples_originali = scene.cycles.samples
filepath_originale = scene.render.filepath

# -----------------------------------------------------------------------------
# Salvataggio (il .blend resta sulla camera frontale originale)
# -----------------------------------------------------------------------------
if os.environ.get("CHIESA_CUPOLA_BACKUP") and \
        os.path.abspath(OUT_PATH) == os.path.abspath(BLEND_PATH):
    import shutil
    shutil.copy2(BLEND_PATH, BLEND_PATH + ".bak")
    print(f"Backup: {BLEND_PATH}.bak")

scene.camera = camera_originale
scene["nota_cupola"] = (
    "v5.1: tiburio con due ordini di logge (colonne binate e archi acuti "
    "sotto, colonne binate e archetti a tutto sesto sopra), calotta fatta di "
    "768 LASTRE di piombo vere con pieghe di giunzione e otto costoloni a "
    "nastro, lanterna del Bernini ad otto lati con finestre a sesto acuto e "
    "grate, fascia in piombo con gli oculi, tetto a otto falde, vaso lapideo, "
    "mela dorata a coste, stella a dodici punte e croce; punta della croce "
    "a 48 m.")
bpy.ops.wm.save_as_mainfile(filepath=OUT_PATH, compress=True)
print(f"Salvato: {OUT_PATH}")

# -----------------------------------------------------------------------------
# Anteprime (dopo il salvataggio: non alterano camera e luci del .blend)
# -----------------------------------------------------------------------------
if not os.environ.get("CHIESA_CUPOLA_NO_RENDER"):
    _luce_riempimento_cupola()   # solo in memoria: non entra nel .blend
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = int(os.environ.get("CHIESA_CUPOLA_SAMPLES", 24))
    scene.cycles.use_denoising = True

    def _rendi(cam, nome_file, rx, ry, nascondi=()):
        nascosti = []
        for c in bpy.data.collections:
            if c.name in nascondi and not c.hide_render:
                c.hide_render = True
                nascosti.append(c)
        scene.camera = cam
        scene.render.resolution_x = rx
        scene.render.resolution_y = ry
        scene.render.resolution_percentage = 100
        scene.render.filepath = os.path.join(OUT_DIR, nome_file)
        print(f"Render {nome_file} ({rx}x{ry}, {scene.cycles.samples} campioni)")
        try:
            bpy.ops.render.render(write_still=True)
        finally:
            for c in nascosti:
                c.hide_render = False

    rx, ry = (int(v) for v in os.environ.get(
        "CHIESA_CUPOLA_RES", "900x1150").split("x"))
    # Nel render d'insieme il Duomo Nuovo resta nascosto: le sue pareti vuote
    # toglierebbero leggibilita' alla cupola (come nelle altre anteprime).
    _rendi(cam_cupola, "anteprima_cupola.png", rx, ry,
           nascondi=("07g_Duomo_Nuovo_Incompiuto",))
    _rendi(cam_lanterna, "anteprima_cupola_lanterna.png", rx, ry,
           nascondi=("07g_Duomo_Nuovo_Incompiuto",))
    _rendi(cam_tamburo, "anteprima_cupola_tamburo.png", 1200, 800,
           nascondi=("07g_Duomo_Nuovo_Incompiuto",))

    scene.camera = camera_originale
    scene.render.resolution_x, scene.render.resolution_y = res_originale
    scene.cycles.samples = samples_originali
    scene.render.filepath = filepath_originale

print("Aggiornamento cupola completato.")
