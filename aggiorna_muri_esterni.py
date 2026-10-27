#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aggiunge i MURI ESTERNI SEMPLICI del corpo della chiesa a un .blend esistente.

Uso (Blender 4.2+ oppure modulo pip `bpy`):

    python aggiorna_muri_esterni.py
    blender --background --python aggiorna_muri_esterni.py

Variabili d'ambiente:

    CHIESA_MURI_BLEND=...       .blend di partenza (default Facciata_Duomo_Siena.blend)
    CHIESA_MURI_OUT=...         .blend di destinazione (default: sovrascrive)
    CHIESA_MURI_BACKUP=1        salva una copia .bak prima di sovrascrivere
    CHIESA_MURI_NO_RENDER=1     non generare le anteprime
    CHIESA_MURI_SAMPLES=16      campioni Cycles delle anteprime
    CHIESA_MURI_RES=1100x760    risoluzione della vista d'insieme
    CHIESA_MURI_PIANTA_RES=1000x1000  risoluzione della vista dall'alto

Lo script e' idempotente: le raccolte `07*` vengono ricostruite da zero.
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

from muri_esterni import (  # noqa: E402
    SCALA_DEFAULT, costruisci_muri_esterni,
)

CFG_PATH = os.path.join(OUT_DIR, "config_facciata.json")
BLEND_PATH = os.environ.get(
    "CHIESA_MURI_BLEND", os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend"))
OUT_PATH = os.environ.get("CHIESA_MURI_OUT", BLEND_PATH)

with open(CFG_PATH, "r", encoding="utf-8") as fh:
    CFG = json.load(fh)

SCALA = float(CFG.get("dimensioni", {}).get(
    "scala_globale", CFG.get("meta", {}).get("scala_finale", SCALA_DEFAULT)))
MURI_CFG = CFG.get("muri_esterni", {})

print(f"Carico: {BLEND_PATH}")
bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
print(f"Oggetti prima: {len(bpy.data.objects)} | scala globale: {SCALA}")

# -----------------------------------------------------------------------------
# Costruzione muri (il .blend e' gia' in unita' 3x -> scala=SCALA)
# -----------------------------------------------------------------------------
risultato = costruisci_muri_esterni(scala=SCALA, cfg=MURI_CFG)
print(f"Oggetti dopo: {len(bpy.data.objects)}")

# -----------------------------------------------------------------------------
# Camera di servizio per le anteprime (aggiunta al .blend, scena invariata)
# -----------------------------------------------------------------------------
def _collezione(nome):
    c = bpy.data.collections.get(nome)
    if c is None:
        c = bpy.data.collections.new(nome)
        bpy.context.scene.collection.children.link(c)
    return c


# Rimuove eventuali camere di servizio di una run precedente (idempotente).
_cam_col = bpy.data.collections.get("08_Camere_Anteprima")
if _cam_col is not None:
    for _o in list(_cam_col.objects):
        bpy.data.objects.remove(_o, do_unlink=True)
    bpy.data.collections.remove(_cam_col, do_unlink=True)


def _bbox_muri(escludi=()):
    """Bounding box dei soli muri esterni (per inquadrare le anteprime)."""
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for c in bpy.data.collections:
        if not c.name.startswith("07") or c.name in escludi:
            continue
        for o in c.objects:
            if o.type != "MESH":
                continue
            for corner in o.bound_box:
                p = o.matrix_world @ Vector(corner)
                for i in range(3):
                    mn[i] = min(mn[i], p[i])
                    mx[i] = max(mx[i], p[i])
    return mn, mx


def _camera(nome, loc, target, ortho):
    cam_data = bpy.data.cameras.new(nome)
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = ortho
    cam_data.clip_end = 5000.0
    cam = bpy.data.objects.new(nome, cam_data)
    _collezione("08_Camere_Anteprima").objects.link(cam)
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat(
        "-Z", "Y").to_euler()
    return cam


def _luce_ripieno():
    """Due soli deboli sui fianchi: il sole del .blend e' calibrato sul
    fronte e lascerebbe i muri laterali in controluce.  Vengono creati DOPO
    il salvataggio: il .blend non cambia illuminazione."""
    out = []
    for nome, energia, rz in (
        ("Luce_Riempimento_Sx", 1.25, 128.0),
        ("Luce_Riempimento_Dx", 0.95, -118.0),
    ):
        data = bpy.data.lights.new(nome, type="SUN")
        data.energy = energia
        data.angle = math.radians(26.0)
        data.color = (0.88, 0.91, 1.0)
        obj = bpy.data.objects.new(nome, data)
        _collezione("08_Camere_Anteprima").objects.link(obj)
        obj.rotation_euler = (math.radians(52.0), 0.0, math.radians(rz))
        out.append(obj)
    return out


DUOMO_NUOVO_COL = "07g_Duomo_Nuovo_Incompiuto"

# Vista dall'alto: pianta COMPLETA (Duomo Nuovo compreso).
mn, mx = _bbox_muri()
centro_top = (mn + mx) * 0.5
estensione = max(mx.x - mn.x, mx.y - mn.y, mx.z - mn.z)
print("BBox muri:", tuple(round(v, 1) for v in mn),
      tuple(round(v, 1) for v in mx))

# Vista 3/4: solo il corpo della chiesa, inquadratura piu' stretta.
mn_c, mx_c = _bbox_muri(escludi=(DUOMO_NUOVO_COL,))
centro = (mn_c + mx_c) * 0.5
# Il fronte e' a Y negativo; inquadriamo il fianco DESTRO, come nelle
# fotografie allegate, cosi' campanile e cupola sono entrambi leggibili.
centro.y -= (mx_c.y - mn_c.y) * 0.10
centro.z = mx_c.z * 0.30  # il campanile non deve spostare il target in cielo
ext_c = max(mx_c.x - mn_c.x, mx_c.y - mn_c.y, mx_c.z - mn_c.z)
cam_3q = _camera(
    "Camera_Struttura_3Q",
    (centro.x + ext_c * 0.50, centro.y - ext_c * 1.20,
     centro.z + ext_c * 0.72),
    centro,
    ext_c * 1.38,
)
cam_pianta = _camera(
    "Camera_Pianta_Alto",
    (centro_top.x, centro_top.y, mx.z + estensione * 1.4),
    centro_top,
    estensione * 1.18,
)
# Convenzione della pianta: facciata in basso, campanile a destra.
cam_pianta.rotation_euler = (0.0, 0.0, 0.0)

scene = bpy.context.scene
camera_originale = scene.camera
res_originale = (scene.render.resolution_x, scene.render.resolution_y)
samples_originali = scene.cycles.samples
filepath_originale = scene.render.filepath

# -----------------------------------------------------------------------------
# Salvataggio: il .blend resta sulla camera frontale originale
# -----------------------------------------------------------------------------
if os.environ.get("CHIESA_MURI_BACKUP") and os.path.abspath(OUT_PATH) == os.path.abspath(BLEND_PATH):
    import shutil
    shutil.copy2(BLEND_PATH, BLEND_PATH + ".bak")
    print(f"Backup: {BLEND_PATH}.bak")

scene.camera = camera_originale
scene["titolo"] = "Duomo di Siena — facciata ovest e corpo della chiesa"
scene["nota"] = ("Modello procedurale v4.2: facciata v3.9 invariata + corpo "
                 "semplice proporzionato sulle fotografie allegate. Navate "
                 "laterali a 15,2 m, cleristorio a 21,8 m, cupola con lanterna "
                 "a 48 m e campanile a 77 m sul fianco destro. Raccolte 07*.")
bpy.ops.wm.save_as_mainfile(filepath=OUT_PATH, compress=True)
print(f"Salvato: {OUT_PATH}")

# -----------------------------------------------------------------------------
# Anteprime (dopo il salvataggio: non alterano la camera del .blend)
# -----------------------------------------------------------------------------
if not os.environ.get("CHIESA_MURI_NO_RENDER"):
    _luce_ripieno()  # solo in memoria: il .blend salvato resta invariato
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = int(os.environ.get("CHIESA_MURI_SAMPLES", 16))
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
        print(f"Render {nome_file} ({rx}x{ry}, {scene.cycles.samples} campioni)...")
        try:
            bpy.ops.render.render(write_still=True)
        finally:
            for c in nascosti:
                c.hide_render = False

    rx, ry = (int(v) for v in os.environ.get(
        "CHIESA_MURI_RES", "1100x760").split("x"))
    # Nel render d'insieme si nasconde il Duomo Nuovo (raccolta 07g): e' il
    # progetto MAI COMPLETATO e le sue lunghe pareti vuote distraggono dalla
    # lettura del corpo della chiesa.  La vista dall'alto lo mostra invece
    # per intero, esattamente come nella pianta di riferimento.
    _rendi(cam_3q, "anteprima_struttura.png", rx, ry,
           nascondi=(DUOMO_NUOVO_COL,))

    rx2, ry2 = (int(v) for v in os.environ.get(
        "CHIESA_MURI_PIANTA_RES", "1000x1000").split("x"))
    _rendi(cam_pianta, "anteprima_pianta.png", rx2, ry2)

    scene.camera = camera_originale
    scene.render.resolution_x, scene.render.resolution_y = res_originale
    scene.cycles.samples = samples_originali
    scene.render.filepath = filepath_originale

print("Aggiornamento muri esterni completato.")
