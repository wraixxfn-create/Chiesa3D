#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facciata del Duomo di Siena (fronte ovest) — modello 3D procedurale.
SOLO la facciata: nessun interno, nessuna navata, nessun edificio laterale.

Uso:
  - con Blender:   blender --background --python genera_facciata.py
  - con il modulo bpy (pip):  python genera_facciata.py

Output (nella stessa cartella dello script):
  - Facciata_Duomo_Siena.blend
  - anteprima_facciata.png
  - Facciata_Duomo_Siena.glb (se abilitato in config)

Coordinate: X = larghezza (m), Y = profondita' (fronte verso -Y), Z = altezza (m).
Larghezza totale ~30 m, altezza all'angelo ~35 m (proporzioni della facciata reale).
Tutto il modello viene poi riscalato di "scala_globale" (default 3.0) -> ~90 x ~105 m.

MIGLIORAMENTI v1.4 (altri 3, e solo 3, miglioramenti di fedelta' all'originale):
  1. Oculo finalmente CIRCOLARE (raggi X e Z uguali: 2.80 m) come nella foto, con
     griglia della vetrata 3x3 a barre sottili, e nicchie della cornice quadrata non
     piu' "buchi neri": vani in ombra calda poco profondi, con busti piu' grandi che
     riempiono l'edicola come gli altorilievi reali di Patriarchi e Profeti.
  2. Policromia marmorea attenuata come nell'originale: contrafforti angolari con
     5 FASCE SOTTILI di serpentino (non piu' zebratura a bande nere spesse), fondo e
     specchiature fra le ghimberghe in marmo chiaro/rosato con piccolo intarsio verde
     centrale (non piu' lastre nere a "domino"), campo rosa delle ghimberghe ridotto
     a una cornice sottile in marmo rosato chiaro.
  3. Apparato scultoreo Giovanni Pisano: statue non piu' "pedine" (cono + sfera) ma figure
     panneggiate con pieghe verticali, spalle, maniche e testa proporzionata, in pietra
     calda consumata piu' scura del marmo di fondo; doccioni come draghi orizzontali
     con testa, muso e ala (non piu' pioli conici) e angelo apicale con 2 ali per lato.
"""

import bpy
import bmesh
import math
import os
import sys
import json
import tempfile
import numpy as np
from mathutils import Vector, Matrix

# -----------------------------------------------------------------------------
# Configurazione
# -----------------------------------------------------------------------------
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(OUT_DIR, "config_facciata.json")
REF_PATH = os.path.join(OUT_DIR, "riferimento_facciata.jpg")
BLEND_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend")
PNG_PATH = os.path.join(OUT_DIR, "anteprima_facciata.png")
GLB_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.glb")


def load_config():
    """Carica configurazione da JSON, con fallback ai default hardcoded."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Attenzione: errore lettura config ({e}). Uso default.")
    return {}


CFG = load_config()

# -----------------------------------------------------------------------------
# Pulizia scena
# -----------------------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
for block in (
    bpy.data.meshes,
    bpy.data.curves,
    bpy.data.cameras,
    bpy.data.lights,
    bpy.data.materials,
    bpy.data.images,
):
    for item in list(block):
        if item.users == 0:
            block.remove(item)

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene["titolo"] = "Duomo di Siena — solo facciata ovest"
scene["nota"] = "Modello procedurale v1.4 fedele alla fotografia di riferimento: solo facciata, retro piatto."


# -----------------------------------------------------------------------------
# Collezioni
# -----------------------------------------------------------------------------
def make_collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or scene.collection).children.link(c)
    return c


COL_NAMES = CFG.get("collezioni", {
    "struttura": "01_Struttura",
    "portali": "02_Portali",
    "rosone_e_logge": "03_Rosone_e_logge",
    "guglie_e_pinnacoli": "04_Guglie_e_pinnacoli",
    "statue": "05_Statue",
    "dettagli": "06_Dettagli",
})
COL = {k: make_collection(v) for k, v in COL_NAMES.items()}
S = COL["struttura"]
P = COL["portali"]
R = COL["rosone_e_logge"]
G = COL["guglie_e_pinnacoli"]
ST = COL["statue"]
D = COL["dettagli"]


# -----------------------------------------------------------------------------
# Generatore texture PBR incorporate (.pack()) per marmi, portoni e mosaici
# -----------------------------------------------------------------------------
def _save_packed_image(name, rgb_bottom_up):
    """Converte un array float [H, W, 3] in [0..1] (riga 0 = basso) in una
    bpy.types.Image PNG compressa e impacchettata dentro il file .blend."""
    h, w, _ = rgb_bottom_up.shape
    rgba = np.ones((h, w, 4), dtype=np.float32)
    rgba[:, :, :3] = np.clip(rgb_bottom_up, 0.0, 1.0)
    img = bpy.data.images.new(name=name, width=w, height=h, alpha=False)
    img.pixels.foreach_set(rgba.ravel())
    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        img.filepath_raw = tmp_path
        img.file_format = "PNG"
        img.save()
        img.pack()
        img.filepath = ""
        img.filepath_raw = ""
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
    return img


def _fbm2d(size, seed=0, octaves=4):
    """Rumore frattale morbido periodico [0..1] con solo numpy."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((size, size), dtype=np.float32)
    amp = 1.0
    norm = 0.0
    y_idx = np.linspace(0, 1, size, endpoint=False, dtype=np.float32)
    x_idx = np.linspace(0, 1, size, endpoint=False, dtype=np.float32)
    yy, xx = np.meshgrid(y_idx, x_idx, indexing="ij")
    for o in range(octaves):
        freq = 2 ** (o + 1)
        ph1 = rng.uniform(0, 2 * math.pi, (freq, freq))
        am1 = rng.uniform(0.3, 1.0, (freq, freq))
        field = np.zeros((size, size), dtype=np.float32)
        for ky in range(min(freq, 6)):
            for kx in range(min(freq, 6)):
                field += am1[ky, kx] * np.sin(
                    2 * math.pi * ((kx + 1) * xx + (ky + 1) * yy) + ph1[ky, kx]
                )
        field = (field - field.min()) / max(float(field.max() - field.min()), 1e-5)
        acc += amp * field
        norm += amp
        amp *= 0.5
    return acc / norm


def _make_marble_tex(name, base_srgb, vein_srgb, courses=8, seed=1, contrast=0.14):
    """Lastra marmorea a conci con venature senesi sottili."""
    sz = 256
    n1 = _fbm2d(sz, seed=seed, octaves=4)
    n2 = _fbm2d(sz, seed=seed + 17, octaves=3)
    yy, xx = np.meshgrid(
        np.linspace(0, 1, sz, endpoint=False),
        np.linspace(0, 1, sz, endpoint=False),
        indexing="ij",
    )
    veins = 0.5 + 0.5 * np.sin(2.0 * math.pi * (3.0 * yy + 1.15 * n1 + 0.35 * n2))
    veins = veins ** 2.2

    # Leggera variazione di tono fra un concio lapideo e l'altro + giunti sottili
    row_id = np.floor(yy * courses).astype(np.int32)
    stagger = (row_id % 2) * 0.5
    col_id = np.floor((xx * (courses // 2) + stagger) % (courses // 2)).astype(np.int32)
    rng = np.random.default_rng(seed + 99)
    block_lut = rng.uniform(1.0 - contrast * 0.55, 1.0 + contrast * 0.45, (courses + 1, courses + 1))
    block_tone = block_lut[row_id, col_id]

    fy = np.abs((yy * courses) % 1.0 - 0.5)
    fx = np.abs(((xx * (courses // 2) + stagger)) % 1.0 - 0.5)
    mortar = np.where((fy > 0.475) | (fx > 0.482), 0.86, 1.0)

    base = np.array(base_srgb, dtype=np.float32)[None, None, :]
    vein = np.array(vein_srgb, dtype=np.float32)[None, None, :]
    col = base * (1.0 - 0.30 * veins[:, :, None]) + vein * (0.30 * veins[:, :, None])
    col = col * block_tone[:, :, None] * mortar[:, :, None]
    return _save_packed_image(name, col)


def _bilinear_sample(topdown_rgb, x_coords, y_coords):
    """Campionamento bilineare vettoriale su immagine [H, W, 3] top-down."""
    h, w, _ = topdown_rgb.shape
    x = np.clip(x_coords, 0.0, w - 1.001)
    y = np.clip(y_coords, 0.0, h - 1.001)
    x0 = np.floor(x).astype(np.int32)
    y0 = np.floor(y).astype(np.int32)
    x1 = np.minimum(x0 + 1, w - 1)
    y1 = np.minimum(y0 + 1, h - 1)
    wx = (x - x0)[:, :, None]
    wy = (y - y0)[:, :, None]
    c00 = topdown_rgb[y0, x0]
    c10 = topdown_rgb[y0, x1]
    c01 = topdown_rgb[y1, x0]
    c11 = topdown_rgb[y1, x1]
    return (1 - wy) * ((1 - wx) * c00 + wx * c10) + wy * ((1 - wx) * c01 + wx * c11)


def _extract_triangle_tex(name, topdown_rgb, p_bl, p_br, p_top, size=512, boost=1.10):
    """Rettifica baricentrica di un mosaico triangolare verso UV (0,0)-(1,0)-(0.5,1)."""
    # Riga 0 in Blender = v=0 (base del triangolo), riga size-1 = v=1 (vertice alto)
    v_lin = np.linspace(0.0, 1.0, size, dtype=np.float32)
    u_lin = np.linspace(0.0, 1.0, size, dtype=np.float32)
    vv, uu = np.meshgrid(v_lin, u_lin, indexing="ij")
    denom = np.maximum(1.0 - vv, 1e-3)
    s = np.clip((uu - 0.5 * vv) / denom, 0.0, 1.0)
    px = (1.0 - vv) * ((1.0 - s) * p_bl[0] + s * p_br[0]) + vv * p_top[0]
    py = (1.0 - vv) * ((1.0 - s) * p_bl[1] + s * p_br[1]) + vv * p_top[1]
    sampled = _bilinear_sample(topdown_rgb, px, py)
    # Leggera compensazione per evitare doppia attenuazione d'illuminazione in Cycles
    sampled = np.clip(sampled * boost, 0.0, 1.0)
    return _save_packed_image(name, sampled)


def _extract_rect_tex(name, topdown_rgb, x0, y0_top, x1, y1_bot, w_out=256, h_out=384, boost=1.08):
    """Estrae una regione rettangolare (portone/vetrata) orientata bottom-up per Blender."""
    v_lin = np.linspace(1.0, 0.0, h_out, dtype=np.float32)  # riga 0 -> y1_bot (basso)
    u_lin = np.linspace(0.0, 1.0, w_out, dtype=np.float32)
    vv, uu = np.meshgrid(v_lin, u_lin, indexing="ij")
    px = x0 + uu * (x1 - x0)
    py = y0_top + vv * (y1_bot - y0_top)
    sampled = np.clip(_bilinear_sample(topdown_rgb, px, py) * boost, 0.0, 1.0)
    return _save_packed_image(name, sampled)


def build_all_textures():
    tex = {}
    tex["marmo_bianco"] = _make_marble_tex(
        "Tex_Marmo_Bianco", (0.75, 0.70, 0.62), (0.60, 0.54, 0.46), courses=8, seed=3, contrast=0.12
    )
    tex["marmo_caldo"] = _make_marble_tex(
        "Tex_Marmo_Caldo", (0.70, 0.63, 0.53), (0.54, 0.47, 0.39), courses=8, seed=11, contrast=0.14
    )
    tex["pietra_statue"] = _make_marble_tex(
        "Tex_Pietra_Statue", (0.63, 0.56, 0.47), (0.46, 0.40, 0.33), courses=4, seed=21, contrast=0.08
    )
    tex["gradinata"] = _make_marble_tex(
        "Tex_Gradinata", (0.58, 0.59, 0.63), (0.44, 0.46, 0.50), courses=12, seed=31, contrast=0.16
    )
    tex["marmo_rosa"] = _make_marble_tex(
        "Tex_Marmo_Rosa", (0.58, 0.41, 0.37), (0.42, 0.28, 0.24), courses=6, seed=41, contrast=0.15
    )
    tex["marmo_rosa_chiaro"] = _make_marble_tex(
        "Tex_Marmo_Rosa_Chiaro", (0.67, 0.53, 0.47), (0.52, 0.39, 0.34), courses=6, seed=51, contrast=0.12
    )
    tex["serpentino"] = _make_marble_tex(
        "Tex_Serpentino_Prato", (0.17, 0.19, 0.19), (0.10, 0.13, 0.12), courses=6, seed=61, contrast=0.12
    )

    if os.path.exists(REF_PATH):
        ref_img = bpy.data.images.load(REF_PATH)
        rw, rh = ref_img.size
        buf = np.empty(rw * rh * 4, dtype=np.float32)
        ref_img.pixels.foreach_get(buf)
        bpy.data.images.remove(ref_img)
        # In Blender riga 0 = basso -> invertiamo per avere y=0 in alto come nella foto
        topdown = buf.reshape((rh, rw, 4))[::-1, :, :3].copy()
        sx = rw / 2560.0
        sy = rh / 2438.0
        tex["mosaico_centrale"] = _extract_triangle_tex(
            "Tex_Mosaico_Incoronazione",
            topdown,
            (1102 * sx, 780 * sy),
            (1564 * sx, 770 * sy),
            (1332 * sx, 478 * sy),
            size=512,
            boost=1.18,
        )
        tex["mosaico_sx"] = _extract_triangle_tex(
            "Tex_Mosaico_Presentazione",
            topdown,
            (724 * sx, 1146 * sy),
            (914 * sx, 1143 * sy),
            (822 * sx, 1016 * sy),
            size=256,
            boost=1.20,
        )
        tex["mosaico_dx"] = _extract_triangle_tex(
            "Tex_Mosaico_Nativita",
            topdown,
            (1750 * sx, 1110 * sy),
            (1944 * sx, 1102 * sy),
            (1850 * sx, 972 * sy),
            size=256,
            boost=1.20,
        )
        tex["bronzo_porta"] = _extract_rect_tex(
            "Tex_Porta_Bronzo", topdown, 1232 * sx, 1887 * sy, 1454 * sx, 2252 * sy, 256, 384, boost=1.22
        )
        tex["legno_porta"] = _extract_rect_tex(
            "Tex_Porta_Legno", topdown, 836 * sx, 1974 * sy, 972 * sx, 2245 * sy, 256, 384, boost=1.18
        )
        tex["oculo_vetro"] = _extract_rect_tex(
            "Tex_Oculo_Vetro", topdown, 1126 * sx, 952 * sy, 1560 * sx, 1314 * sy, 256, 256, boost=1.12
        )
    else:
        # Fallback procedurale autonomo
        oro = _make_marble_tex("Tex_Mosaico_Fallback", (0.72, 0.58, 0.28), (0.45, 0.28, 0.16), courses=16, seed=7)
        for k in ("mosaico_centrale", "mosaico_sx", "mosaico_dx"):
            tex[k] = oro
        tex["bronzo_porta"] = _make_marble_tex("Tex_Bronzo_Fb", (0.18, 0.19, 0.19), (0.11, 0.12, 0.11), courses=6, seed=8)
        tex["legno_porta"] = _make_marble_tex("Tex_Legno_Fb", (0.30, 0.21, 0.15), (0.20, 0.13, 0.09), courses=6, seed=9)
        tex["oculo_vetro"] = _make_marble_tex("Tex_Vetro_Fb", (0.22, 0.27, 0.34), (0.15, 0.19, 0.25), courses=4, seed=10)
    return tex


TEXTURES = build_all_textures()


# -----------------------------------------------------------------------------
# Materiali PBR da config + texture incorporate
# -----------------------------------------------------------------------------
def mat_from_cfg(name, cfg):
    """Crea materiale Principled BSDF compatibile sia con Cycles che con export GLB."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (420, 0)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (120, 0)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    c = cfg.get("color", [0.4, 0.4, 0.4])
    bsdf.inputs["Base Color"].default_value = (*c, 1.0)
    bsdf.inputs["Roughness"].default_value = cfg.get("roughness", 0.55)
    bsdf.inputs["Metallic"].default_value = cfg.get("metallic", 0.0)

    tex_key = cfg.get("tex")
    if tex_key and tex_key in TEXTURES:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.location = (-260, 0)
        tex_node.image = TEXTURES[tex_key]
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        if cfg.get("emission_strength", 0.0) > 0.0:
            links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = cfg["emission_strength"]

    if "emission" in cfg and not tex_key:
        bsdf.inputs["Emission Color"].default_value = (*cfg["emission"], 1.0)
        bsdf.inputs["Emission Strength"].default_value = cfg.get("emission_strength", 0.2)

    return m


MAT_CFG = CFG.get("materiali", {})
MATS = {name: mat_from_cfg(name, cfg) for name, cfg in MAT_CFG.items()}

BIANCO = MATS.get("Marmo_Bianco")
BIANCO2 = MATS.get("Marmo_Bianco_Caldo")
GRADINATA_MAT = MATS.get("Marmo_Gradinata", BIANCO2)
ROSA = MATS.get("Marmo_Rosa")
ROSA_C = MATS.get("Marmo_Rosato_Chiaro")
VERDE = MATS.get("Marmo_Verde_Scuro")
MOS_C = MATS.get("Mosaico_Centrale_Mat")
MOS_SX = MATS.get("Mosaico_Sx_Mat")
MOS_DX = MATS.get("Mosaico_Dx_Mat")
ORO = MATS.get("Mosaico_Oro")
ORO_C = MATS.get("Mosaico_Chiaro")
BRONZO = MATS.get("Bronzo_Portale")
BRONZO_D = MATS.get("Bronzo_Dorato", ORO)
LEGNO = MATS.get("Legno_Portali")
LEGNO_S = MATS.get("Legno_Scuro")
VETRO = MATS.get("Vetro_Rosone")
FERRO = MATS.get("Ferro_Griglia")
PIETRA = MATS.get("Pietra_Statue")
SCURO = MATS.get("Vano_Scuro")
NICCHIA = MATS.get("Vano_Nicchia", PIETRA)


# -----------------------------------------------------------------------------
# Helper di costruzione rapidi con UV analitici privi di distorsione e triangolati
# -----------------------------------------------------------------------------
def _finish_bmesh(bm, mesh, uv_scale=(1.0, 1.0), planar_uv=False):
    """Calcola normali esterne, coordinate UV pulite e triangola eventuali n-gon."""
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uv_layer = bm.loops.layers.uv.verify()
    if planar_uv:
        xs = [v.co.x for v in bm.verts]
        zs = [v.co.z for v in bm.verts]
        x0, dx = min(xs), max(max(xs) - min(xs), 1e-4)
        z0, dz = min(zs), max(max(zs) - min(zs), 1e-4)
        for f in bm.faces:
            for loop in f.loops:
                loop[uv_layer].uv = ((loop.vert.co.x - x0) / dx, (loop.vert.co.z - z0) / dz)
    else:
        su, sv = uv_scale
        for f in bm.faces:
            n = f.normal
            ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
            for loop in f.loops:
                co = loop.vert.co
                if ay >= ax and ay >= az:
                    u, v = (co.x + 0.5) * su, (co.z + 0.5) * sv
                elif ax >= az:
                    u, v = (co.y + 0.5) * su, (co.z + 0.5) * sv
                else:
                    u, v = (co.x + 0.5) * su, (co.y + 0.5) * sv
                loop[uv_layer].uv = (u, v)
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        bmesh.ops.triangulate(bm, faces=ngons)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def _create_mesh_object(name, mesh, col, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), material=None):
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj.scale = scale
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    return obj


def box(name, col, x, y, z, sx, sy, sz, material, rot_z=0.0, rot_x=0.0, rot_y=0.0, fit_uv=False):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix())
    uv_scale = (1.0, 1.0) if fit_uv else (max(sx / 3.2, 0.25), max(sz / 3.2, 0.25))
    _finish_bmesh(bm, mesh, uv_scale=uv_scale)
    return _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, rot_y, rot_z), (sx, sy, sz), material)


def cyl(name, col, x, y, z, radius, depth, material, vertices=20,
        rot_x=0.0, rot_y=0.0, rot_z=0.0, scale_x=1.0, scale_y=1.0, fit_uv=False):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=True, segments=vertices,
        radius1=radius, radius2=radius, depth=depth, calc_uvs=True
    )
    if fit_uv:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        uv_layer = bm.loops.layers.uv.verify()
        for f in bm.faces:
            for loop in f.loops:
                co = loop.vert.co
                loop[uv_layer].uv = (
                    0.5 + co.x / max(2.0 * radius, 1e-4),
                    0.5 + co.y / max(2.0 * radius, 1e-4),
                )
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
    else:
        _finish_bmesh(bm, mesh, uv_scale=(max(radius * 1.5, 0.3), max(depth / 3.0, 0.3)))
    return _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, rot_y, rot_z), (scale_x, scale_y, 1.0), material)


def cone(name, col, x, y, z, r1, r2, depth, material, vertices=12, rot_x=0.0, rot_y=0.0, rot_z=0.0):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=True, segments=vertices,
        radius1=r1, radius2=r2, depth=depth, calc_uvs=True
    )
    _finish_bmesh(bm, mesh, uv_scale=(0.6, max(depth / 3.0, 0.4)))
    return _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, rot_y, rot_z), (1.0, 1.0, 1.0), material)


def sphere(name, col, x, y, z, radius, material, sx=1.0, sy=1.0, sz=1.0):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=10, radius=radius, calc_uvs=True)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    ngons = [f for f in bm.faces if len(f.verts) > 4]
    if ngons:
        bmesh.ops.triangulate(bm, faces=ngons)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (x, y, z), (0, 0, 0), (sx, sy, sz), material)


def torus_ellipse(name, col, cx, y, cz, rx, rz, minor, material, seg_u=48, seg_v=12):
    """Anello toroidale ellittico/circolare nel piano XZ (per oculo e cornici)."""
    bm = bmesh.new()
    grid = []
    for i in range(seg_u):
        a = 2.0 * math.pi * i / seg_u
        ca, sa = math.cos(a), math.sin(a)
        row = []
        for j in range(seg_v):
            b = 2.0 * math.pi * j / seg_v
            cb, sb = math.cos(b), math.sin(b)
            px = (rx + minor * cb) * ca
            py = minor * sb
            pz = (rz + minor * cb) * sa
            row.append(bm.verts.new((px, py, pz)))
        grid.append(row)
    uv_layer = bm.loops.layers.uv.verify()
    for i in range(seg_u):
        i2 = (i + 1) % seg_u
        for j in range(seg_v):
            j2 = (j + 1) % seg_v
            f = bm.faces.new((grid[i][j], grid[i2][j], grid[i2][j2], grid[i][j2]))
            uvs = ((i / seg_u * 4, j / seg_v), ((i + 1) / seg_u * 4, j / seg_v),
                   ((i + 1) / seg_u * 4, (j + 1) / seg_v), (i / seg_u * 4, (j + 1) / seg_v))
            for loop, uv in zip(f.loops, uvs):
                loop[uv_layer].uv = uv
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, cz), (0, 0, 0), (1, 1, 1), material)


def torus(name, col, x, y, z, major, minor, material):
    return torus_ellipse(name, col, x, y, z, major, major, minor, material, seg_u=36, seg_v=10)


def arch(name, col, cx, y, cz, major, minor, material, seg_u=32, seg_v=10, pointed=0.0):
    """Archivolto nel piano XZ: a tutto sesto (pointed=0) o acuto gotico (pointed>0)."""
    bm = bmesh.new()
    grid = []
    for i in range(seg_u + 1):
        t = i / seg_u
        a = math.pi * (1.0 - t)  # da sinistra (pi) a destra (0)
        base_x = major * math.cos(a)
        base_z = major * math.sin(a) + pointed * major * (1.0 - abs(2.0 * t - 1.0)) ** 0.85
        row = []
        for j in range(seg_v):
            b = 2.0 * math.pi * j / seg_v
            cb, sb = math.cos(b), math.sin(b)
            nx, nz = math.cos(a), math.sin(a)
            row.append(bm.verts.new((base_x + minor * cb * nx, minor * sb, base_z + minor * cb * nz)))
        grid.append(row)
    uv_layer = bm.loops.layers.uv.verify()
    for i in range(seg_u):
        for j in range(seg_v):
            j2 = (j + 1) % seg_v
            f = bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j2], grid[i][j2]))
            for k, loop in enumerate(f.loops):
                loop[uv_layer].uv = ((i + (1 if k in (1, 2) else 0)) / seg_u * 3.0, (j + (1 if k in (2, 3) else 0)) / seg_v)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, cz), (0, 0, 0), (1, 1, 1), material)


def prism(name, col, cx, y, z_base, width, height, depth, material, mosaic_uv=False):
    """Prisma triangolare con faccia frontale mappata esattamente su (0,0)-(1,0)-(0.5,1)."""
    w, h, d = width / 2.0, height, depth / 2.0
    bm = bmesh.new()
    v0 = bm.verts.new((-w, -d, 0.0))
    v1 = bm.verts.new((w, -d, 0.0))
    v2 = bm.verts.new((0.0, -d, h))
    v3 = bm.verts.new((-w, d, 0.0))
    v4 = bm.verts.new((w, d, 0.0))
    v5 = bm.verts.new((0.0, d, h))
    f_front = bm.faces.new((v0, v1, v2))
    f_back = bm.faces.new((v5, v4, v3))
    f_bot = bm.faces.new((v0, v3, v4, v1))
    f_r = bm.faces.new((v1, v4, v5, v2))
    f_l = bm.faces.new((v2, v5, v3, v0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uv_layer = bm.loops.layers.uv.verify()
    if mosaic_uv:
        tri_map = {v0: (0.0, 0.0), v1: (1.0, 0.0), v2: (0.5, 1.0),
                   v3: (0.0, 0.0), v4: (1.0, 0.0), v5: (0.5, 1.0)}
        for f in bm.faces:
            for loop in f.loops:
                loop[uv_layer].uv = tri_map[loop.vert]
    else:
        for f in (f_front, f_back, f_bot, f_r, f_l):
            for loop in f.loops:
                co = loop.vert.co
                loop[uv_layer].uv = ((co.x + w) / 3.2, co.z / 3.2)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, z_base), (0, 0, 0), (1, 1, 1), material)


def spioventi_modanati(name, col, cx, y, z_base, width, height, thickness, depth, material):
    """Doppia cornice inclinata aggettante lungo i due spioventi di un timpano/ghimberga."""
    half = width / 2.0
    slope_len = math.hypot(half, height) + thickness * 0.6
    ang = math.atan2(height, half)
    for s in (-1, 1):
        mx = cx + s * half * 0.5
        mz = z_base + height * 0.5 + thickness * 0.32
        box(
            f"{name}_Spiov_{s}", col, mx, y, mz,
            slope_len, depth, thickness, material, rot_y=s * ang
        )


def colonna_ritorta(name, col, x, y, z, radius, height, material, turns=3.2,
                    segments=14, rings=26, ridges=3, ridge_amp=0.16, taper=0.05):
    """Colonna tortile ('a vite') di Giovanni Pisano."""
    bm = bmesh.new()
    grid = []
    for i in range(rings + 1):
        t = i / float(rings)
        zz = -height / 2.0 + t * height
        ang0 = t * turns * 2.0 * math.pi
        rad = radius * (1.0 - taper * t)
        row = []
        for j in range(segments):
            a = ang0 + 2.0 * math.pi * j / segments
            rr = rad * (1.0 + ridge_amp * math.cos(ridges * (a - ang0)))
            row.append(bm.verts.new((rr * math.cos(a), rr * math.sin(a), zz)))
        grid.append(row)
    uv_layer = bm.loops.layers.uv.verify()
    for i in range(rings):
        for j in range(segments):
            j2 = (j + 1) % segments
            f = bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
            for k, loop in enumerate(f.loops):
                loop[uv_layer].uv = (j / segments, (i + (1 if k >= 2 else 0)) / rings * 2.0)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (x, y, z), (0, 0, 0), (1, 1, 1), material)


def arco_ritorto(name, col, cx, y, cz, major, minor, material,
                 seg_u=34, seg_v=12, ribs=7, turns=2.2, amp=0.22):
    """Archivolto tortile scolpito di Giovanni Pisano."""
    bm = bmesh.new()
    grid = []
    for i in range(seg_u + 1):
        a = math.pi * (1.0 - i / seg_u)
        helix = 2.0 * math.pi * turns * i / seg_u
        row = []
        for j in range(seg_v):
            b = 2.0 * math.pi * j / seg_v
            m = minor * (1.0 + amp * math.cos(ribs * b + helix))
            r = major + m * math.cos(b)
            row.append(bm.verts.new((r * math.cos(a), m * math.sin(b), r * math.sin(a))))
        grid.append(row)
    uv_layer = bm.loops.layers.uv.verify()
    for i in range(seg_u):
        for j in range(seg_v):
            j2 = (j + 1) % seg_v
            f = bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j2], grid[i][j2]))
            for k, loop in enumerate(f.loops):
                loop[uv_layer].uv = (i / seg_u * 4.0, j / seg_v)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, cz), (0, 0, 0), (1, 1, 1), material)


def foglie_rampanti(name, col, cx, y, z_base, width, height, material=PIETRA, n=9, size=0.28):
    """Foglie rampanti gotiche (crockets) lungo entrambi gli spioventi."""
    for s in (-1, 1):
        for i in range(n):
            t = 0.08 + 0.85 * i / max(1, n - 1)
            x = cx + s * (width / 2.0) * (1.0 - t)
            z = z_base + height * t
            cone(
                f"{name}_Foglia_{s}_{i}", col, x, y - 0.04, z + size * 0.42,
                size * 0.28, 0.02, size * 0.92, material, vertices=7,
                rot_y=-s * math.radians(32)
            )
            sphere(
                f"{name}_Bocciolo_{s}_{i}", col, x - s * size * 0.14, y - 0.05,
                z + size * 0.82, size * 0.14, material
            )


def statue(name, col, x, y, z, h=1.5, material=PIETRA):
    """Statua gotica panneggiata: plinto, manto con pieghe, spalle, maniche e testa.

    Silhouette stretta e verticale come le figure di Giovanni Pisano, non piu'
    il cono largo con sfera che nel render v1.3 leggeva come una "pedina".
    """
    s = h / 1.5
    box(name + "_base", col, x, y, z + 0.09, 0.36 * s, 0.32, 0.18, BIANCO2)
    # Manto rastremato (base molto meno larga della vecchia toga conica)
    cone(name + "_toga", col, x, y, z + 0.18 + h * 0.30, 0.165 * s, 0.105 * s,
         h * 0.60, material, vertices=10)
    # Tre pieghe verticali del panneggio sul fronte del manto
    for fx in (-0.085, 0.0, 0.085):
        box(f"{name}_piega_{fx:+.3f}", col, x + fx * s, y - 0.125 * s,
            z + 0.18 + h * 0.29, 0.034 * s, 0.045, h * 0.50, material)
    # Spalle arrotondate e maniche cadenti lungo i fianchi (niente barra orizzontale)
    sphere(name + "_spalle", col, x, y - 0.01, z + 0.18 + h * 0.615, 0.125 * s,
           material, sx=1.35, sy=0.85, sz=0.78)
    for sa in (-1, 1):
        cone(f"{name}_manica_{sa}", col, x + sa * 0.155 * s, y - 0.02,
             z + 0.18 + h * 0.47, 0.058 * s, 0.042 * s, h * 0.32, material,
             vertices=8, rot_z=sa * math.radians(14))
    # Collo e testa proporzionata (piu' piccola della vecchia sfera)
    cyl(name + "_collo", col, x, y - 0.01, z + 0.18 + h * 0.70, 0.045 * s, 0.10 * s,
        material, vertices=8)
    sphere(name + "_testa", col, x, y - 0.01, z + 0.18 + h * 0.775, 0.092 * s, material)


def statua_angelo(name, col, x, y, z, h=1.35, material=PIETRA, con_tromba=False):
    statue(name, col, x, y, z, h, material)
    for s in (-1, 1):
        # Solo 2 ali per lato, raccolte e slanciate a V come sull'apice del Duomo
        # (le 4 penne per lato della v1.3 formavano una "stella" dorata innaturale)
        for f_k in range(2):
            ang_w = s * math.radians(13 + f_k * 9)
            len_w = h * (0.70 - f_k * 0.10)
            cone(
                f"{name}_Penna_{s}_{f_k}", col,
                x + s * (0.17 + f_k * 0.07) * (h / 1.35), y + 0.05,
                z + 0.34 + h * (0.88 - f_k * 0.07),
                0.088 * (h / 1.35), 0.015, len_w, material, vertices=8,
                rot_x=math.radians(-10), rot_y=ang_w
            )
    if con_tromba:
        cyl(
            f"{name}_Tromba", col, x - 0.30, y - 0.08, z + h * 1.22,
            0.030, h * 0.92, BRONZO_D, vertices=8, rot_y=math.radians(-15)
        )


def lastra_forata_oculo(name, col, cx, y, cz, half_w, half_h, rx, rz, depth, material, seg=64):
    """Pannello rettangolare con vero foro ellittico passante per l'oculo."""
    bm = bmesh.new()
    hd = depth * 0.5
    inner_f, outer_f, inner_b, outer_b = [], [], [], []
    for i in range(seg):
        a = 2.0 * math.pi * i / seg
        ca, sa = math.cos(a), math.sin(a)
        ix, iz = rx * ca, rz * sa
        # Proiezione del raggio sul bordo rettangolare [-half_w, half_w] x [-half_h, half_h]
        tx = half_w / max(abs(ca), 1e-4)
        tz = half_h / max(abs(sa), 1e-4)
        t = min(tx, tz)
        ox, oz = t * ca, t * sa
        inner_f.append(bm.verts.new((ix, -hd, iz)))
        outer_f.append(bm.verts.new((ox, -hd, oz)))
        inner_b.append(bm.verts.new((ix, hd, iz)))
        outer_b.append(bm.verts.new((ox, hd, oz)))
    uv_layer = bm.loops.layers.uv.verify()
    for i in range(seg):
        i2 = (i + 1) % seg
        faces = [
            bm.faces.new((inner_f[i], outer_f[i], outer_f[i2], inner_f[i2])),
            bm.faces.new((inner_b[i2], outer_b[i2], outer_b[i], inner_b[i])),
            bm.faces.new((inner_f[i2], inner_b[i2], inner_b[i], inner_f[i])),
        ]
        for f in faces:
            for loop in f.loops:
                co = loop.vert.co
                loop[uv_layer].uv = ((co.x + half_w) / 3.2, (co.z + half_h) / 3.2)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, cz), (0, 0, 0), (1, 1, 1), material)


def statua_vergine(name, col, x, y, z, h=1.55, material=PIETRA):
    statue(name, col, x, y, z, h, material)
    sphere(f"{name}_Bambino", col, x + 0.13, y - 0.11, z + 0.22 + h * 0.56, 0.11, material)
    cone(f"{name}_Bambino_Veste", col, x + 0.13, y - 0.10, z + 0.22 + h * 0.44, 0.10, 0.06, 0.22, material, vertices=8)


def gargolla(name, col, x, y, z, side, length, radius, material=PIETRA):
    """Doccione a drago sporgente in orizzontale: corpo, testa col muso e ala.

    Sostituisce il cono con sfera della v1.3, che nel render leggeva come un
    "piolo" piantato nel torrione invece della gargolla monumentale della foto.
    """
    # Corpo orizzontale proteso verso l'esterno (asse inclinato sui lati)
    cone(f"{name}_Corpo", col, x, y, z, radius, radius * 0.52, length, material,
         vertices=8, rot_y=side * math.radians(80))
    # Testa allungata all'estremita' esterna, col muso rivolto in fuori
    hx = x + side * length * 0.52
    sphere(f"{name}_Testa", col, hx, y, z + radius * 0.35, radius * 0.82, material,
           sx=1.45, sy=0.9, sz=0.9)
    cone(f"{name}_Muso", col, hx + side * radius * 1.15, y, z + radius * 0.22,
         radius * 0.42, radius * 0.14, radius * 1.7, material, vertices=7,
         rot_y=side * math.radians(84))
    # Ala ripiegata verso l'alto alla radice del corpo
    cone(f"{name}_Ala", col, x - side * length * 0.16, y, z + radius * 1.55,
         radius * 0.55, 0.015, radius * 3.4, material, vertices=7,
         rot_z=-side * math.radians(24))


def finial(name, col, x, y, z, s=1.0):
    cyl(name + "_fusto", col, x, y, z + 0.22 * s, 0.065 * s, 0.44 * s, BIANCO, vertices=8)
    sphere(name + "_nodo", col, x, y, z + 0.50 * s, 0.10 * s, PIETRA)
    cone(name + "_punta", col, x, y, z + 0.82 * s, 0.085 * s, 0.01, 0.52 * s, PIETRA, vertices=8)


def edicola_gotica_busto(name, col, cx, y, z0, w, h, con_busto=True):
    """Singola nicchia gotica cuspidata con archetto trilobo, ghimberga e mezzo busto."""
    arch_h = h * 0.34
    body_h = h - arch_h
    # Fondo in ombra calda e poco profondo (non il "buco nero" piatto della v1.3):
    # nella foto le nicchie sono altorilievi chiari in edicole appena incassate
    box(f"{name}_Vano", col, cx, y + 0.06, z0 + body_h * 0.5, w * 0.74, 0.14, body_h, NICCHIA)
    prism(f"{name}_VanoCima", col, cx, y + 0.06, z0 + body_h, w * 0.74, arch_h * 0.9, 0.14, NICCHIA)
    # Colonnine divisorie e ghimberga acuta
    for s in (-1, 1):
        box(f"{name}_Stip_{s}", col, cx + s * w * 0.46, y - 0.02, z0 + body_h * 0.5,
            w * 0.11, 0.16, body_h, BIANCO2)
    spioventi_modanati(f"{name}_Ghim", col, cx, y - 0.05, z0 + body_h * 0.86,
                       w * 0.96, arch_h * 1.12, 0.075, 0.16, BIANCO)
    cone(f"{name}_Fiorone", col, cx, y - 0.05, z0 + h + 0.09, 0.055, 0.01, 0.18, PIETRA, vertices=6)
    if con_busto:
        # Busto piu' grande, che riempie l'edicola come gli altorilievi reali
        cone(f"{name}_Busto", col, cx, y - 0.07, z0 + body_h * 0.34,
             w * 0.31, w * 0.19, body_h * 0.52, PIETRA, vertices=9)
        sphere(f"{name}_Testa", col, cx, y - 0.08, z0 + body_h * 0.72, w * 0.19, PIETRA)


# -----------------------------------------------------------------------------
# Lettura quote e parametri principali
# -----------------------------------------------------------------------------
DIM = CFG.get("dimensioni", {})
W_TOT = DIM.get("larghezza_totale", 30.0)
H_ANGELO = DIM.get("altezza_angelo", 35.2)
THICK = DIM.get("spessore_facciata", 2.6)
H_BASE = DIM.get("altezza_basamento", 1.9)
H_PORTALI = DIM.get("altezza_portali", 5.65)
W_PORT_C = DIM.get("larghezza_portale_centrale", 3.5)
W_PORT_L = DIM.get("larghezza_portali_laterali", 2.35)
X_PORT_L = DIM.get("asse_portali_laterali", 7.15)
Z_IMPOSTA = DIM.get("quota_imposta_portali", 8.45)
Z_GALLERIA = DIM.get("quota_cornicione_galleria", 15.35)
Z_OCULO = DIM.get("altezza_centro_oculo", 19.75)
RX_OCULO = DIM.get("raggio_oculo_x", 3.08)
RZ_OCULO = DIM.get("raggio_oculo_z", 2.66)
HALF_SQ = DIM.get("semilato_quadrato_oculo", 4.45)
Z_TIMPANO = DIM.get("quota_base_timpano_centrale", 24.45)
X_PIL_C = DIM.get("x_pilastri_centrali", 5.0)
W_PIL_C = DIM.get("larghezza_pilastro_centrale", 1.15)
Z_PIL_TOP = DIM.get("colmo_pilastro_centrale", 27.0)
X_LAT = DIM.get("x_settori_laterali", 8.05)
Z_CUSP_LAT = DIM.get("base_cuspidi_laterali", 19.75)
H_CUSP_LAT = DIM.get("altezza_cuspidi_laterali", 4.6)
X_TORRI = DIM.get("x_torrioni_angolari", 12.7)
SCALA = float(DIM.get("scala_globale", 3.0))

# =============================================================================
# 1. GRADINATA DEL SAGRATO E BASAMENTO ORIZZONTALE
# =============================================================================
for i in range(13):
    box(
        f"Gradino_{i+1}", S, 0.0, -2.1 - i * 0.65, 1.82 - i * 0.25,
        42.0, 0.88, 0.28, GRADINATA_MAT
    )
box("Basamento_Pietra", S, 0.0, -0.35, 0.95, 31.2, 3.6, 1.9, BIANCO2)
box("Zoccolo_Modanato", S, 0.0, -0.55, 1.92, 30.6, 3.3, 0.24, BIANCO)

# =============================================================================
# 2. STRUTTURA DI FONDO — SOLO FACCIATA (retro piatto a Y = +1.30)
# =============================================================================
# Ordine inferiore in marmo bianco senese (retro compatto, spessore 2.6 m)
box("Corpo_Inferiore", S, 0.0, 0.12, 8.55, 29.6, THICK - 0.24, 13.30, BIANCO)
# Fondo chiaro rosato nella fascia dei timpani (nella foto non c'e' alcuna
# lastra nera continua dietro le ghimberghe: il fondo e' marmo chiaro senese)
box("Specchiatura_Fondo_Prato", S, 0.0, -1.25, 12.80, 21.4, 0.14, 4.55, ROSA_C)
# Corpo superiore centrale arretrato (faccia anteriore a Y = -0.55, dietro la vetrata dell'oculo!)
box("Corpo_Superiore_Centrale", S, 0.0, 0.38, 19.60, 10.8, 1.85, 8.95, BIANCO)
# Muri di spalla dietro le loggette laterali
for side in (-1, 1):
    box(f"Corpo_Settore_Lat_{side}", S, side * X_LAT, 0.35, 16.95, 5.2, 1.90, 3.75, BIANCO2)

# =============================================================================
# 3. ORDINE INFERIORE DI GIOVANNI PISANO: CONTRAFFORTI BICROMI, 4 PILONI A
#    FASCIO, 3 PORTALI CONTIGUI STROMBATI E SPECCHIATURE CON ROSONI
# =============================================================================
# --- Contrafforti angolari inferiori a fasce bicrome + fascia a losanghe ---
for side in (-1, 1):
    # Campata esterna sporgente (fasce bicrome nette bianco / verde-nero di Prato)
    xe = side * 13.85
    box(f"Contrafforte_Base_Est_{side}", S, xe, -0.15, 5.15, 2.25, 2.95, 6.45, BIANCO)
    # Solo 5 fasce SOTTILI di serpentino molto distanziate, come nella foto
    # (la v1.3 alternava bande nere spesse e marmo: effetto "zebratura" assente
    # nell'originale, dove i corsi scuri sono listelli di ~15 cm)
    for k in range(5):
        zk = 2.95 + k * 1.02
        box(f"Fascia_Est_{side}_{k}", D, xe, -0.22, zk, 2.30, 2.92, 0.15, VERDE)
    # Feritoia stretta sul contrafforte destro/sinistro
    box(f"Feritoia_Base_{side}", D, xe, -1.70, 5.05, 0.18, 0.10, 0.72, SCURO)

    # Campata interna arretrata con fasce bicrome + fascia a losanghe rosa/bianche
    xi = side * 11.82
    box(f"Contrafforte_Base_Int_{side}", S, xi, -0.05, 5.15, 1.90, 2.75, 6.45, BIANCO)
    # Stesso ritmo sottile della campata esterna, evitando la fascia a losanghe
    for zk in (2.60, 3.62, 6.05, 7.07):
        box(f"Fascia_Int_{side}_{zk:.2f}", D, xi, -1.45, zk, 1.92, 0.12, 0.13, VERDE)
    # Fascia a 3 riquadri con losanghe intarsiate (come nella foto a quota ~4.8 m)
    box(f"Cornice_Losanghe_{side}", D, xi, -1.44, 4.85, 1.88, 0.12, 1.05, BIANCO2)
    for c in range(3):
        lx = xi + (c - 1) * 0.58
        box(f"Riquadro_Los_{side}_{c}", D, lx, -1.47, 4.85, 0.50, 0.10, 0.62, ROSA_C)
        box(f"Losanga_{side}_{c}", D, lx, -1.51, 4.85, 0.32, 0.10, 0.32, VERDE, rot_y=math.radians(45))

    # Trabeazione scolpita d'imposta sui contrafforti (z = 8.35 m, NON attraversa gli archi)
    box(f"Trabeazione_Angolo_{side}", S, side * 12.85, -0.25, Z_IMPOSTA, 4.35, 3.05, 0.62, BIANCO2)
    box(f"Cornice_Aggetto_Angolo_{side}", S, side * 12.85, -0.32, Z_IMPOSTA + 0.38, 4.50, 3.20, 0.22, ROSA_C)


# --- 4 grandi piloni strombati a fascio di colonne (x = +-10.45 e +-3.85) ---
def pilone_strombato(cx, central_side=False):
    tag = f"Pilone_{cx:+.2f}"
    y0 = -1.52
    # Zoccolo modanato a gradoni
    box(f"{tag}_Basamento", P, cx, y0 + 0.15, 2.18, 1.55, 0.95, 0.52, BIANCO2)
    # Colonna principale frontale scolpita a candelabro/fogliame + 4 colonne tortili laterali
    cyl(f"{tag}_ColFrontale", P, cx, y0 - 0.18, 5.10, 0.21, 5.30, BIANCO, vertices=16)
    for r_i in range(7):
        torus(f"{tag}_Rilievo_{r_i}", P, cx, y0 - 0.18, 2.85 + r_i * 0.72, 0.19, 0.055, PIETRA)
    for s in (-1, 1):
        colonna_ritorta(
            f"{tag}_Tort1_{s}", P, cx + s * 0.44, y0 - 0.06, 5.10, 0.155, 5.30,
            ROSA if s > 0 else BIANCO, turns=3.5, ridges=3
        )
        colonna_ritorta(
            f"{tag}_Tort2_{s}", P, cx + s * 0.80, y0 + 0.08, 5.10, 0.145, 5.30,
            BIANCO2, turns=-3.0, ridges=4
        )
    # Capitelli compositi a fogliame d'acanto + trabeazione d'imposta spezzata
    box(f"{tag}_Capitelli", P, cx, y0 - 0.02, 7.95, 1.85, 0.88, 0.46, PIETRA)
    box(f"{tag}_Imposta", P, cx, y0 - 0.08, Z_IMPOSTA, 1.98, 1.00, 0.52, BIANCO2)
    box(f"{tag}_ImpostaRosa", P, cx, y0 - 0.12, Z_IMPOSTA + 0.32, 2.06, 1.06, 0.20, ROSA)
    # Leone / grifone stiloforo sporgente di Giovanni Pisano
    box(f"{tag}_LeoneCorpo", ST, cx, y0 - 0.28, Z_IMPOSTA + 0.66, 0.36, 0.62, 0.36, PIETRA)
    sphere(f"{tag}_LeoneTesta", ST, cx, y0 - 0.58, Z_IMPOSTA + 0.82, 0.20, PIETRA)
    # Pilastrino e grande statua di Profeta/Sibilla nel pennacchio fra le ghimberghe
    box(f"{tag}_ Contrafforte Alto", P, cx, -1.42, 12.15, 0.62, 0.44, 5.80, BIANCO)
    statue(f"{tag}_StatuaProfeta", ST, cx, y0 - 0.18, 9.85, 1.85 if central_side else 1.70, PIETRA)
    spioventi_modanati(f"{tag}_Baldacchino", P, cx, y0 - 0.20, 12.10, 0.86, 0.85, 0.09, 0.44, BIANCO)
    finial(f"{tag}_Pinnacolo", G, cx, y0 - 0.10, 14.95, 0.95)


for px_pier, is_c in [(-10.45, False), (-3.85, True), (3.85, True), (10.45, False)]:
    pilone_strombato(px_pier, central_side=is_c)


# --- I 3 grandi portali contigui (centrale + due laterali) ---
def portale_pisano(cx, door_w, door_h, r_ext, gh_base, gh_apex, door_mat, central=False):
    tag = "Centrale" if central else ("Sinistro" if cx < 0 else "Destro")
    front = -1.32

    # 1. Mostra marmorea aperta attorno al vano (2 stipiti + sopraluce, SENZA coprire la porta!)
    show_w = door_w + (0.85 if central else 1.40)
    jamb_w = (show_w - door_w) * 0.5
    for s_j in (-1, 1):
        box(
            f"Stipite_Mostra_{tag}_{s_j}", P,
            cx + s_j * (door_w * 0.5 + jamb_w * 0.5), front - 0.14, 1.95 + door_h * 0.5,
            jamb_w, 0.24, door_h, BIANCO
        )
    # Vano ombroso e portone ben visibile con texture ad alta risoluzione
    box(f"Vano_Porta_{tag}", P, cx, front + 0.08, 1.95 + door_h * 0.5, door_w + 0.10, 0.20, door_h + 0.06, SCURO)
    box(f"Porta_{tag}", P, cx, front - 0.08, 1.95 + door_h * 0.5, door_w, 0.10, door_h, door_mat, fit_uv=True)
    # Battente centrale sottile in rilievo
    box(f"Battente_{tag}", P, cx, front - 0.14, 1.95 + door_h * 0.5, 0.06, 0.04, door_h,
        BRONZO if central else LEGNO_S)

    # Architrave scolpito e fregio a mensole sopra il portone (sotto la lunetta!)
    z_lint = 2.02 + door_h + 0.24
    box(f"Architrave_{tag}", P, cx, front - 0.16, z_lint, show_w + 0.15, 0.30, 0.44, PIETRA)
    if not central:
        # Nei portali laterali, fascia marmorea bianca e fregio scolpito fra porta e imposta
        box(f"Sopraluce_Marmo_{tag}", P, cx, front - 0.12, 7.38, show_w, 0.24, 1.48, BIANCO)
        for m_i in range(5):
            box(f"Metopa_{tag}_{m_i}", P, cx + (m_i - 2) * 0.62, front - 0.20, 7.62, 0.44, 0.08, 0.48, PIETRA)
    for d_i in range(9):
        box(f"Mensolina_{tag}_{d_i}", P, cx + (d_i - 4) * (show_w / 9.0), front - 0.22,
            Z_IMPOSTA - 0.16, 0.18, 0.18, 0.20, BIANCO)

    # 2. Lunetta sopra la quota d'imposta Z_IMPOSTA (mai tagliata da alcun cornicione!)
    r_in = r_ext - 1.52
    cyl(f"Lunetta_Fondo_{tag}", P, cx, front + 0.04, Z_IMPOSTA + 0.12, r_in + 0.15, 0.20,
        BIANCO2, vertices=36, rot_x=math.radians(90))
    if central:
        # Raggiera bicroma bianco / verde-nero + Sole raggiante bronzeo di San Bernardino
        n_rays_bg = 15
        for k in range(n_rays_bg):
            a = math.pi * (0.06 + 0.88 * k / (n_rays_bg - 1))
            box(
                f"Spicchio_Lunetta_{k}", P,
                cx + math.cos(a) * (r_in * 0.62), front - 0.07,
                Z_IMPOSTA + 0.15 + math.sin(a) * (r_in * 0.62),
                0.24, 0.06, r_in * 0.95,
                VERDE if k % 2 == 1 else BIANCO,
                rot_y=(math.pi / 2.0 - a)
            )
        arch("Cornice_Interna_Sole", P, cx, front - 0.09, Z_IMPOSTA + 0.20, r_in * 0.92, 0.09, ROSA)
        cyl("Disco_Sole_IHS", P, cx, front - 0.16, Z_IMPOSTA + 0.78, 0.44, 0.12,
            BRONZO_D, vertices=24, rot_x=math.radians(90))
        for a_i in range(16):
            ang = a_i * 2.0 * math.pi / 16.0
            cone(
                f"Fiamma_Sole_{a_i}", P,
                cx + math.cos(ang) * 0.70, front - 0.16,
                Z_IMPOSTA + 0.78 + math.sin(ang) * 0.70,
                0.085, 0.01, 0.56, BRONZO_D, vertices=6,
                rot_y=math.pi / 2.0 - ang
            )
    else:
        # Ghirlanda circolare scolpita nelle lunette laterali
        arch(f"Lunetta_Rosa_{tag}", P, cx, front - 0.07, Z_IMPOSTA + 0.16, r_in * 0.86, 0.09, ROSA)
        torus(f"Ghirlanda_{tag}", P, cx, front - 0.12, Z_IMPOSTA + 0.78, 0.40, 0.09, PIETRA)

    # 3. Strombatura profonda a 5 ordini concentrici di archivolti bianchi e rosa
    cz_arch = Z_IMPOSTA + 0.15
    rings_spec = [
        (r_in + 0.12, 0.13, -0.08, ROSA, False),
        (r_in + 0.42, 0.15, -0.16, BIANCO, True),
        (r_in + 0.76, 0.16, -0.24, ROSA, False),
        (r_in + 1.12, 0.16, -0.32, PIETRA, True),
        (r_ext - 0.08, 0.17, -0.40, BIANCO2, False),
    ]
    for idx, (rr, min_r, dy, mat_a, twisted) in enumerate(rings_spec):
        if twisted:
            arco_ritorto(f"Archivolto_{tag}_{idx}", P, cx, front + dy, cz_arch, rr, min_r, mat_a)
        else:
            arch(f"Archivolto_{tag}_{idx}", P, cx, front + dy, cz_arch, rr, min_r, mat_a, seg_u=38)
    # Chiave di volta scolpita
    sphere(f"Chiave_Volta_{tag}", P, cx, front - 0.46, cz_arch + r_ext - 0.05, 0.22, PIETRA)

    # 4. Grande ghimberga triangolare ripida svettante oltre Z_GALLERIA
    gh_w = r_ext * 2.0 + 0.15
    gh_h = gh_apex - gh_base
    # Corpo triangolare in marmo bianco; il rosa resta solo una cornice sottile
    # chiara attorno al campo interno (nella foto le ghimberghe sono quasi
    # interamente in marmo bianco scolpito, non campi rosa saturi)
    prism(f"Ghimberga_Corpo_{tag}", P, cx, -1.42, gh_base, gh_w, gh_h, 0.46, BIANCO)
    prism(f"Ghimberga_CampoRosa_{tag}", P, cx, -1.66, gh_base + 0.42, gh_w * 0.66, gh_h * 0.66, 0.10, ROSA_C)
    prism(f"Ghimberga_CampoInterno_{tag}", P, cx, -1.72, gh_base + 0.62, gh_w * 0.56, gh_h * 0.54, 0.08, BIANCO2)
    spioventi_modanati(f"Ghimberga_Cornice_{tag}", P, cx, -1.72, gh_base, gh_w, gh_h, 0.26, 0.36, BIANCO)
    foglie_rampanti(f"Ghimberga_Foglie_{tag}", P, cx, -1.76, gh_base, gh_w, gh_h, PIETRA, n=11, size=0.30)

    # Medaglione circolare scolpito col busto a mezz'altezza della ghimberga
    z_med = gh_base + gh_h * 0.56
    torus(f"Medaglione_Cornice_{tag}", P, cx, -1.78, z_med, 0.56, 0.11, BIANCO)
    cyl(f"Medaglione_Fondo_{tag}", P, cx, -1.76, z_med, 0.50, 0.08, ROSA_C, vertices=24, rot_x=math.radians(90))
    cone(f"Medaglione_Busto_{tag}", P, cx, -1.83, z_med - 0.12, 0.24, 0.14, 0.38, PIETRA, vertices=10)
    sphere(f"Medaglione_Testa_{tag}", P, cx, -1.84, z_med + 0.16, 0.15, PIETRA)

    # Statua di coronamento sul vertice della ghimberga
    if central:
        statua_vergine("Statua_Madonna_Oculo", ST, cx, -1.72, gh_apex + 0.05, 1.62, PIETRA)
    else:
        statue(f"Statua_Apice_Ghimberga_{tag}", ST, cx, -1.70, gh_apex + 0.02, 1.36, PIETRA)


portale_pisano(-X_PORT_L, W_PORT_L, 4.55, 3.30, 10.25, 15.90, LEGNO, central=False)
portale_pisano(0.0, W_PORT_C, H_PORTALI, 3.85, 10.55, 16.40, BRONZO, central=True)
portale_pisano(X_PORT_L, W_PORT_L, 4.55, 3.30, 10.25, 15.90, LEGNO, central=False)

# --- Specchiature marmoree incorniciate e rosoni scolpiti nei 6 timpani murari ---
spandrel_positions = [
    (-9.35, 13.75, 1.75, 2.05),
    (-4.95, 13.75, 1.75, 2.05),
    (-2.65, 13.85, 1.55, 1.90),
    (2.65, 13.85, 1.55, 1.90),
    (4.95, 13.75, 1.75, 2.05),
    (9.35, 13.75, 1.75, 2.05),
]
for idx_s, (sx_pos, sz_pos, sw, sh) in enumerate(spandrel_positions):
    # Specchiatura chiara incorniciata come nella foto (marmo bianco/rosato con
    # rosone fogliato); il verde di Prato resta solo nel piccolo intarsio centrale
    box(f"Specch_CorniceEst_{idx_s}", D, sx_pos, -1.30, sz_pos, sw, 0.10, sh, BIANCO)
    box(f"Specch_CorniceRosa_{idx_s}", D, sx_pos, -1.33, sz_pos, sw - 0.24, 0.10, sh - 0.24, ROSA_C)
    box(f"Specch_LastraPrato_{idx_s}", D, sx_pos, -1.36, sz_pos, sw - 0.44, 0.10, sh - 0.44, BIANCO)
    # Rosone fogliato scolpito al centro, con piccolo intarsio verde romboidale
    torus(f"Specch_Rosone_{idx_s}", D, sx_pos, -1.41, sz_pos + 0.12, 0.34, 0.08, ROSA_C)
    box(f"Specch_Intarsio_{idx_s}", D, sx_pos, -1.43, sz_pos + 0.12, 0.20, 0.08, 0.20, VERDE, rot_y=math.radians(45))
    for leaf_i in range(6):
        la = leaf_i * math.pi / 3.0
        cone(
            f"Specch_Petalo_{idx_s}_{leaf_i}", D,
            sx_pos + math.cos(la) * 0.26, -1.42, sz_pos + 0.12 + math.sin(la) * 0.26,
            0.10, 0.02, 0.34, PIETRA, vertices=6, rot_y=math.pi / 2.0 - la
        )

# --- Cornicione orizzontale principale della galleria a mensole (z = 15.35 m) ---
box("Cornicione_Galleria", S, 0.0, -0.35, Z_GALLERIA, 30.6, 3.05, 0.44, BIANCO2)
box("Fregio_Sotto_Galleria", S, 0.0, -1.46, Z_GALLERIA - 0.34, 29.8, 0.26, 0.30, ROSA_C)
for m_k in range(38):
    mx = -14.4 + m_k * (28.8 / 37.0)
    box(f"Mensola_Galleria_{m_k}", D, mx, -1.62, Z_GALLERIA - 0.18, 0.22, 0.32, 0.24, PIETRA)

# =============================================================================
# 4. REGISTRO SUPERIORE CENTRALE: CORNICE QUADRATA DELL'OCULO DI CAMAINO
# =============================================================================
# Pannello quadrato interno FORATO attorno all'oculo CIRCOLARE (pennacchi dei 4 Evangelisti)
IN_W, IN_H = 3.44, 2.95
lastra_forata_oculo(
    "Oculo_Quadro_Pennacchi", R, 0.0, -1.36, Z_OCULO,
    IN_W, IN_H, RX_OCULO + 0.02, RZ_OCULO + 0.02, 0.44, ROSA_C
)

# Vetrata profonda incassata dell'oculo circolare + griglia metallica sottile
cyl(
    "Oculo_Vetro", R, 0.0, -0.82, Z_OCULO, 1.0, 0.14, VETRO,
    vertices=64, rot_x=math.radians(90), scale_x=RX_OCULO + 0.04, scale_y=RZ_OCULO + 0.04, fit_uv=True
)
# Griglia 3x3 a barre sottili come nella vetrata reale (non il reticolo spesso 5x4)
for gx in (-0.50, 0.0, 0.50):
    bar_x = gx * RX_OCULO
    bar_h = 2.0 * RZ_OCULO * math.sqrt(max(0.0, 1.0 - gx * gx))
    box(f"Griglia_Oculo_V_{gx:+.2f}", R, bar_x, -0.92, Z_OCULO, 0.045, 0.06, bar_h, FERRO)
for gz in (-0.50, 0.0, 0.50):
    bar_z = Z_OCULO + gz * RZ_OCULO
    bar_w = 2.0 * RX_OCULO * math.sqrt(max(0.0, 1.0 - gz * gz))
    box(f"Griglia_Oculo_O_{gz:+.2f}", R, 0.0, -0.92, bar_z, bar_w, 0.06, 0.045, FERRO)

# Strombatura profonda dell'oculo a 4 anelli concentrici scolpiti bianco/rosa
oculo_rings = [
    (RX_OCULO + 0.02, RZ_OCULO + 0.02, 0.13, -1.04, BIANCO2),
    (RX_OCULO + 0.12, RZ_OCULO + 0.12, 0.13, -1.20, ROSA),
    (RX_OCULO + 0.22, RZ_OCULO + 0.22, 0.13, -1.34, PIETRA),
    (RX_OCULO + 0.32, RZ_OCULO + 0.32, 0.12, -1.48, BIANCO),
]
for idx_o, (orx, orz, omin, oy, omat) in enumerate(oculo_rings):
    torus_ellipse(f"Oculo_Anello_{idx_o}", R, 0.0, oy, Z_OCULO, orx, orz, omin, omat, seg_u=56, seg_v=12)

# I Quattro Evangelisti ad altorilievo nei 4 pennacchi angolari del quadrato
for sx_e in (-1, 1):
    for sz_e in (-1, 1):
        ex = sx_e * 2.82
        ez = Z_OCULO + sz_e * 2.15
        statue(f"Evangelista_{sx_e}_{sz_e}", ST, ex, -1.52, ez - 0.52, 1.02, PIETRA)

# LA VERA CORONA QUADRATA DI NICCHIE GOTICHE CUSPIDATE (non un cerchio!)
# 14 nicchie nella fila orizzontale superiore
n_top = 14
w_ntop = (HALF_SQ * 2.0) / n_top
for i in range(n_top):
    nx = -HALF_SQ + w_ntop * (i + 0.5)
    edicola_gotica_busto(f"Nicchia_Sup_{i}", R, nx, -1.44, 22.42, w_ntop * 0.98, 1.32, con_busto=True)

# 12 nicchie nella fila orizzontale inferiore (interrotta al centro dalla Madonna col Bambino)
n_bot = 14
w_nbot = (HALF_SQ * 2.0) / n_bot
for i in range(n_bot):
    nx = -HALF_SQ + w_nbot * (i + 0.5)
    if abs(nx) > 0.72:
        edicola_gotica_busto(f"Nicchia_Inf_{i}", R, nx, -1.44, 15.32, w_nbot * 0.98, 1.22, con_busto=True)

# 5 + 5 nicchie sovrapposte nelle due colonne verticali laterali + fregio cosmatesco esterno
n_side = 5
z_v0, z_v1 = 16.58, 22.38
h_nside = (z_v1 - z_v0) / n_side
for side in (-1, 1):
    box(f"Fregio_Est_Oculo_{side}", D, side * 4.30, -1.40, (z_v0 + z_v1) * 0.5, 0.34, 0.14, z_v1 - z_v0, ROSA_C)
    for k_r in range(12):
        sphere(f"Rosetta_Oculo_{side}_{k_r}", D, side * 4.30, -1.48, z_v0 + 0.24 + k_r * 0.47, 0.095, BIANCO)
    for j in range(n_side):
        edicola_gotica_busto(
            f"Nicchia_Lat_{side}_{j}", R, side * 3.84, -1.44,
            z_v0 + j * h_nside, 0.68, h_nside * 0.97, con_busto=True
        )

# Simboli tetramorfi / statue lungo il ballatoio inferiore dell'oculo
for sx_b in (-3.6, 3.6):
    statue(f"Simbolo_Ballatoio_{sx_b:+.1f}", ST, sx_b, -1.68, Z_GALLERIA + 0.20, 1.15, PIETRA)

# =============================================================================
# 5. PILASTRI CONTRAFFORTI CENTRALI CONTINUI + GUGLIE CON STATUE (x = +-5.0 m)
# =============================================================================
def pilastro_centrale_completo(side):
    cx = side * X_PIL_C
    tag = "Sx" if side < 0 else "Dx"
    h_shaft = Z_PIL_TOP - Z_GALLERIA
    box(f"Pilastro_Centrale_{tag}", G, cx, -0.55, Z_GALLERIA + h_shaft * 0.5, W_PIL_C, 1.85, h_shaft, BIANCO)
    for s2 in (-1, 0, 1):
        box(
            f"Costolone_Pil_{tag}_{s2}", G, cx + s2 * 0.36, -1.52, Z_GALLERIA + h_shaft * 0.5,
            0.16, 0.18, h_shaft, ROSA_C if s2 == 0 else BIANCO2
        )
    for s2 in (-1, 1):
        sx_st = cx + s2 * 0.28
        statue(f"Statua_PilCent_{tag}_{s2}", ST, sx_st, -1.66, Z_GALLERIA + 0.30, 1.65, PIETRA)
        spioventi_modanati(f"Ghim_PilBase_{tag}_{s2}", G, sx_st, -1.66, Z_GALLERIA + 2.35, 0.56, 0.72, 0.07, 0.26, BIANCO)
    for s2 in (-1, 1):
        spioventi_modanati(f"Ghim_PilMed_{tag}_{s2}", G, cx + s2 * 0.28, -1.58, 22.8, 0.56, 0.85, 0.07, 0.22, BIANCO)
    for zg in (22.9, 25.4):
        gargolla(
            f"Gargolla_Pil_{tag}_{zg}", D, cx + side * 0.78, -1.25, zg,
            side, 0.95, 0.10, PIETRA
        )
    box(f"Dado_Guglia_{tag}", G, cx, -0.60, Z_PIL_TOP + 0.85, 0.92, 0.92, 1.65, BIANCO2)
    box(f"Luce_Guglia_{tag}", G, cx, -1.08, Z_PIL_TOP + 0.85, 0.34, 0.14, 1.10, SCURO)
    for sx2 in (-1, 1):
        finial(f"Pin_Ang_Guglia_{tag}_{sx2}", G, cx + sx2 * 0.44, -0.95, Z_PIL_TOP + 1.35, 0.78)
    cone(f"Fusto_Guglia_{tag}", G, cx, -0.60, Z_PIL_TOP + 2.40, 0.35, 0.16, 1.55, PIETRA, vertices=8)
    sphere(f"Capitello_Guglia_{tag}", G, cx, -0.60, Z_PIL_TOP + 3.25, 0.23, PIETRA, sz=0.7)
    statue(f"Statua_Sommitale_Guglia_{tag}", ST, cx, -0.60, Z_PIL_TOP + 3.36, 1.15, PIETRA)


pilastro_centrale_completo(-1)
pilastro_centrale_completo(1)

# =============================================================================
# 6. TIMPANO CENTRALE CON VERO MOSAICO DELL'INCORONAZIONE E ANGELO APICALE
# =============================================================================
W_TIMP = 10.30
H_TIMP = 7.95
box("Trabeazione_Timpano_Centrale", S, 0.0, -0.50, Z_TIMPANO + 0.24, W_TIMP + 0.5, 2.20, 0.50, BIANCO2)
for k_m in range(21):
    box(f"Mensola_Timp_{k_m}", D, -4.8 + k_m * 0.48, -1.58, Z_TIMPANO + 0.05, 0.18, 0.24, 0.20, PIETRA)

prism("Timpano_Centrale_Struttura", S, 0.0, 0.0, Z_TIMPANO + 0.42, W_TIMP, H_TIMP, 2.35, BIANCO)
prism("Mosaico_Centrale_Reale", S, 0.0, -1.24, Z_TIMPANO + 0.88, 8.15, 6.10, 0.10, MOS_C, mosaic_uv=True)
spioventi_modanati("Cornice_Int_Timpano", D, 0.0, -1.36, Z_TIMPANO + 0.70, 8.95, 6.80, 0.24, 0.22, PIETRA)
spioventi_modanati("Cornice_Est_Timpano", S, 0.0, -1.48, Z_TIMPANO + 0.42, W_TIMP + 0.30, H_TIMP + 0.15, 0.36, 0.42, BIANCO)
foglie_rampanti("Foglie_Timpano_Centrale", D, 0.0, -1.56, Z_TIMPANO + 0.48, W_TIMP + 0.45, H_TIMP + 0.20, PIETRA, n=16, size=0.30)
for k_c in range(9):
    sphere(f"Cherubino_Base_{k_c}", D, -3.6 + k_c * 0.90, -1.34, Z_TIMPANO + 0.78, 0.15, PIETRA)

Z_APICE_PIETRA = Z_TIMPANO + 0.42 + H_TIMP
box("Piedistallo_Angelo", G, 0.0, -0.95, Z_APICE_PIETRA + 0.26, 0.90, 0.90, 0.56, PIETRA)
statua_angelo("Angelo_Apicale", ST, 0.0, -0.95, Z_APICE_PIETRA + 0.52, 2.00, BRONZO_D, con_tromba=True)

# =============================================================================
# 7. SETTORI LATERALI INTERNI (cx = +-8.05 m): LOGGETTA GOTICA A 5 ARCHETTI
#    ACUTI SU COLONNINE BINATE + CUSPIDI DORATE CON STATUA
# =============================================================================
for side in (-1, 1):
    cx = side * X_LAT
    tag = "Sx" if side < 0 else "Dx"
    mos_mat = MOS_SX if side < 0 else MOS_DX

    # Vano ombroso profondo della loggia (z = 15.25..18.40 m) ben scuro come nella foto
    w_loggia = 4.25
    box(f"Loggia_Fondo_Scuro_{tag}", R, cx, -0.62, 16.85, w_loggia, 0.24, 3.15, SCURO)
    box(f"Loggia_Parapetto_{tag}", R, cx, -1.46, 15.52, w_loggia, 0.36, 0.46, BIANCO2)

    n_archi = 5
    step_a = w_loggia / n_archi
    for i in range(n_archi + 1):
        col_x = cx - w_loggia * 0.5 + i * step_a
        for dy_c in (-1.48, -1.18):
            cyl(f"Colonnina_Loggia_{tag}_{i}_{dy_c:.2f}", R, col_x, dy_c, 16.58, 0.085, 1.68, BIANCO, vertices=12)
        box(f"Capitello_Loggia_{tag}_{i}", R, col_x, -1.34, 17.45, 0.26, 0.52, 0.18, PIETRA)
        if 0 < i < n_archi:
            finial(f"Pinnacolino_Loggia_{tag}_{i}", G, col_x, -1.48, 17.95, 0.52)

    for i in range(n_archi):
        ax = cx - w_loggia * 0.5 + (i + 0.5) * step_a
        arch(
            f"Archetto_Loggia_{tag}_{i}", R, ax, -1.46, 17.44,
            step_a * 0.48, 0.08, BIANCO, seg_u=20, pointed=0.45
        )
        spioventi_modanati(
            f"Ghim_Loggia_{tag}_{i}", R, ax, -1.50, 17.54,
            step_a * 0.98, 0.78, 0.07, 0.20, BIANCO
        )
        cone(f"Fiorone_Loggia_{tag}_{i}", R, ax, -1.52, 18.40, 0.05, 0.01, 0.18, PIETRA, vertices=6)

    for dx_s in (-1.45, 0.95):
        statue(f"Statua_Loggia_{tag}_{dx_s:+.2f}", ST, cx + side * dx_s, -1.68, Z_GALLERIA + 0.18, 1.34, PIETRA)

    # Trabeazione e Cuspide Laterale Dorata (quota esatta della foto: apice pietra ~22.5 m)
    box(f"Trabeazione_Cuspide_{tag}", R, cx, -0.95, Z_CUSP_LAT, w_loggia + 0.15, 1.35, 0.38, BIANCO2)
    prism(f"Cuspide_Lat_Struttura_{tag}", R, cx, -0.45, Z_CUSP_LAT + 0.16, w_loggia, H_CUSP_LAT, 1.75, BIANCO)
    prism(
        f"Mosaico_Laterale_Reale_{tag}", R, cx, -1.36, Z_CUSP_LAT + 0.44,
        w_loggia * 0.78, H_CUSP_LAT * 0.74, 0.10, mos_mat, mosaic_uv=True
    )
    spioventi_modanati(
        f"Cornice_Cuspide_Lat_{tag}", R, cx, -1.46, Z_CUSP_LAT + 0.16,
        w_loggia + 0.18, H_CUSP_LAT + 0.10, 0.25, 0.34, BIANCO
    )
    foglie_rampanti(
        f"Foglie_Cuspide_Lat_{tag}", D, cx, -1.52, Z_CUSP_LAT + 0.20,
        w_loggia + 0.30, H_CUSP_LAT + 0.12, PIETRA, n=8, size=0.24
    )
    z_top_cusp = Z_CUSP_LAT + 0.16 + H_CUSP_LAT
    box(f"Base_Statua_Cusp_{tag}", G, cx, -1.15, z_top_cusp + 0.16, 0.52, 0.52, 0.32, PIETRA)
    statue(f"Statua_Cuspide_{tag}", ST, cx, -1.15, z_top_cusp + 0.32, 1.25, PIETRA)

# =============================================================================
# 8. TORRIONI GOTICI ANGOLARI ESTERNI A DUE CAMPATE (x = +-12.7 m):
#    BIFORE ACUTE BICROME, STATUE IN TABERNACOLO, DOCCIONI E LANTERNA OTTAGONALE
# =============================================================================
for side in (-1, 1):
    tag = "Sx" if side < 0 else "Dx"
    xi = side * 11.15
    xe = side * 13.55
    z_top_tower = 21.65 if side < 0 else 22.35  # leggera asimmetria reale Sx/Dx nella foto!
    h_tower = z_top_tower - Z_IMPOSTA

    # Corpo murario articolato delle due campate fino a z_top_tower
    box(f"Torre_Campata_Int_{tag}", S, xi, -0.05, Z_IMPOSTA + h_tower * 0.5, 2.75, 2.65, h_tower, BIANCO)
    box(f"Torre_Campata_Est_{tag}", S, xe, -0.15, Z_IMPOSTA + (h_tower - 0.5) * 0.5, 2.35, 2.85, h_tower - 0.5, BIANCO2)

    # Fitte lesene e nervature gotiche verticali (elimina ogni parete piatta!)
    for lx_off in (-1.08, -0.50, 0.0, 0.50, 1.08):
        box(
            f"Lesena_Torre_{tag}_{lx_off:+.2f}", G, side * 12.35 + lx_off * 2.05, -1.56,
            Z_IMPOSTA + h_tower * 0.5, 0.22, 0.26, h_tower,
            ROSA_C if abs(lx_off) == 0.50 else BIANCO
        )
    # Marcapiani orizzontali scolpiti sul torrione
    for zm_t in (12.85, 17.65):
        box(f"Marcapiano_Torre_{tag}_{zm_t}", G, side * 12.35, -0.35, zm_t, 5.10, 3.00, 0.30, ROSA_C)

    # Tre ordini di finestre gotiche sovrapposte nella campata interna (con ghimberga bicroma!)
    for idx_w, (zw0, wh) in enumerate([(9.35, 3.30), (13.45, 3.55), (17.95, 3.35)]):
        box(f"Finestra_Vano_{tag}_{idx_w}", D, xi, -1.32, zw0 + wh * 0.45, 0.96, 0.24, wh * 0.85, SCURO)
        prism(f"Finestra_ArcoScuro_{tag}_{idx_w}", D, xi, -1.32, zw0 + wh * 0.86, 0.96, 0.68, 0.24, SCURO)
        colonna_ritorta(f"Mullion_Torre_{tag}_{idx_w}", D, xi, -1.42, zw0 + wh * 0.42, 0.075, wh * 0.82, BIANCO, turns=3.0)
        arch(f"Arco_Fin_Bianco_{tag}_{idx_w}", D, xi, -1.44, zw0 + wh * 0.84, 0.54, 0.095, BIANCO, seg_u=18, pointed=0.45)
        arch(f"Arco_Fin_Prato_{tag}_{idx_w}", D, xi, -1.47, zw0 + wh * 0.86, 0.68, 0.085, VERDE, seg_u=18, pointed=0.45)
        spioventi_modanati(f"Ghim_Fin_{tag}_{idx_w}", D, xi, -1.54, zw0 + wh * 0.84, 1.72, 1.25, 0.13, 0.28, BIANCO)

    # Tre ordini di tabernacoli gotici con grandi statue sul contrafforte d'angolo esterno
    for idx_st, z_st in enumerate((8.95, 13.05, 17.55)):
        box(f"Nicchia_Torre_{tag}_{idx_st}", D, xe, -1.52, z_st + 1.05, 0.88, 0.18, 1.95, NICCHIA)
        statue(f"Statua_Torrione_{tag}_{idx_st}", ST, xe, -1.66, z_st, 1.65, PIETRA)
        spioventi_modanati(f"Baldacch_Torre_{tag}_{idx_st}", G, xe, -1.68, z_st + 1.98, 1.42, 0.98, 0.11, 0.34, BIANCO)

    # 4 doccioni / gargolle sporgenti sul profilo esterno (grande gargolla monumentale a z=13.5 m!)
    gargoyle_specs = [
        (10.2, 1.10, 0.15),
        (13.55, 1.95, 0.22),
        (17.7, 1.20, 0.15),
        (20.9, 1.15, 0.14),
    ]
    for idx_g, (zg, gl, gr) in enumerate(gargoyle_specs):
        gargolla(
            f"Gargolla_Torre_{tag}_{idx_g}", D, xe + side * (0.92 + gl * 0.42), -1.45, zg,
            side, gl, gr, PIETRA
        )

    # Coronamento del torrione: lanterna ottagonale a gradoni piu' alta delle cuspidi laterali (~25.0-25.8 m)
    box(f"Cornicione_Torre_{tag}", G, side * 12.70, -0.25, z_top_tower, 4.65, 3.05, 0.44, BIANCO2)
    cyl(f"Lanterna_Base_{tag}", G, xi, -0.55, z_top_tower + 0.72, 0.90, 1.45, BIANCO2, vertices=8)
    cyl(f"Lanterna_Grado2_{tag}", G, xi, -0.55, z_top_tower + 1.72, 0.65, 0.88, BIANCO, vertices=8)
    cone(f"Lanterna_Cuspide_{tag}", G, xi, -0.55, z_top_tower + 2.52, 0.52, 0.10, 0.92, PIETRA, vertices=8)
    finial(f"Lanterna_Pinnacolo_{tag}", G, xi, -0.55, z_top_tower + 2.90, 0.78)

    for px_off, dz_p, sc_p in [(-0.92, 0.15, 1.18), (0.18, 0.05, 1.32), (0.95, -0.25, 1.08)]:
        px_p = side * (12.70 + px_off * 1.65)
        zp_b = z_top_tower + dz_p
        box(f"Edicola_Sommitale_{tag}_{px_off:+.2f}", G, px_p, -0.95, zp_b + 0.62, 0.60, 0.60, 1.20, BIANCO)
        spioventi_modanati(f"Cusp_Edic_{tag}_{px_off:+.2f}", G, px_p, -1.26, zp_b + 1.18, 0.70, 0.70, 0.08, 0.20, PIETRA)
        finial(f"Pinnacolo_Torre_{tag}_{px_off:+.2f}", G, px_p, -0.95, zp_b + 1.25, sc_p)

# =============================================================================
# 9. LUCI SOLARI POMERIDIANE SENESI, CIELO AZZURRO E CAMERA FRONTALE DAL BASSO
# =============================================================================
L_SOLE = CFG.get("luci", {}).get("sole", {})
sole_loc = tuple(v * SCALA for v in L_SOLE.get("location", (26, -32, 22)))
bpy.ops.object.light_add(type="SUN", location=sole_loc)
sun = bpy.context.object
sun.name = "Sole"
# Direzione reale del sole tardo-pomeridiano da destra (+X, -Y, +Z) come nelle ombre della foto
dir_from = Vector(L_SOLE.get("direction_from", (0.76, -0.58, 0.34))).normalized()
sun.rotation_euler = (-dir_from).to_track_quat("-Z", "Y").to_euler()
sun.data.color = tuple(L_SOLE.get("color", (1.0, 0.87, 0.70)))
sun.data.energy = L_SOLE.get("energy", 3.4)
sun.data.angle = math.radians(L_SOLE.get("angle", 1.2))

L_FILL = CFG.get("luci", {}).get("fill_frontale", {})
fill_loc = tuple(v * SCALA for v in L_FILL.get("location", (-12, -42, 16)))
bpy.ops.object.light_add(type="AREA", location=fill_loc)
fill = bpy.context.object
fill.name = "Luce_Diffusa_Piazza"
fill.data.color = tuple(L_FILL.get("color", (0.74, 0.83, 1.0)))
fill.data.energy = L_FILL.get("energy", 110) * (SCALA ** 2)
fill.data.shape = "DISK"
fill.data.size = L_FILL.get("size", 34) * SCALA
fill_dir = Vector((0, -1.2 * SCALA, 15.0 * SCALA)) - Vector(fill_loc)
fill.rotation_euler = fill_dir.to_track_quat("-Z", "Y").to_euler()

CAM = CFG.get("camera", {})
cam_loc = Vector(tuple(v * SCALA for v in CAM.get("location", (0.35, -54.5, 4.5))))
bpy.ops.object.camera_add(location=tuple(cam_loc))
cam = bpy.context.object
cam.name = "Camera_Frontale"
cam.data.lens = CAM.get("lens", 46.5)
direction = Vector(tuple(v * SCALA for v in CAM.get("look_at", (0.0, -1.4, 16.5)))) - cam_loc
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

# Cielo senese limpido con leggero gradiente verticale verso l'orizzonte
WORLD = CFG.get("mondo", {})
world = bpy.data.worlds["World"]
world.use_nodes = True
wnodes = world.node_tree.nodes
wlinks = world.node_tree.links
wnodes.clear()
w_out = wnodes.new("ShaderNodeOutputWorld")
w_bg = wnodes.new("ShaderNodeBackground")
w_mix = wnodes.new("ShaderNodeMixRGB")
w_sep = wnodes.new("ShaderNodeSeparateXYZ")
w_tc = wnodes.new("ShaderNodeTexCoord")
w_ramp = wnodes.new("ShaderNodeValToRGB")
w_ramp.color_ramp.elements[0].position = 0.02
w_ramp.color_ramp.elements[1].position = 0.35
w_mix.inputs["Color1"].default_value = (*WORLD.get("horizon_color", (0.430, 0.515, 0.735)), 1.0)
w_mix.inputs["Color2"].default_value = (*WORLD.get("sky_color", (0.325, 0.410, 0.630)), 1.0)
w_bg.inputs["Strength"].default_value = WORLD.get("sky_strength", 1.0)
wlinks.new(w_tc.outputs["Generated"], w_sep.inputs["Vector"])
wlinks.new(w_sep.outputs["Z"], w_ramp.inputs["Fac"])
wlinks.new(w_ramp.outputs["Color"], w_mix.inputs["Fac"])
wlinks.new(w_mix.outputs["Color"], w_bg.inputs["Color"])
wlinks.new(w_bg.outputs["Background"], w_out.inputs["Surface"])

# =============================================================================
# 10. SCALA GLOBALE (3x) E CONGELAMENTO TRASFORMAZIONI
# =============================================================================
if abs(SCALA - 1.0) > 1e-9:
    meshes = [o for o in scene.objects if o.type == "MESH"]
    for o in meshes:
        o.location = [v * SCALA for v in o.location]
        o.scale = [v * SCALA for v in o.scale]
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        o.select_set(True)
    if meshes:
        bpy.context.view_layer.objects.active = meshes[0]
        try:
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, properties=False)
        except Exception as e:
            print(f"Attenzione: transform_apply non riuscito ({e})")
    print(f"Ingrandimento x{SCALA}: ~{W_TOT * SCALA:.0f} m x ~{H_ANGELO * SCALA:.0f} m")

# =============================================================================
# 11. SALVATAGGIO .BLEND, RENDER CYCLES CON DENOISE ED EXPORT GLTF/GLB
# =============================================================================
for o in scene.objects:
    o.select_set(False)

RENDER = CFG.get("render", {})
scene.render.engine = RENDER.get("engine", "CYCLES")
scene.cycles.samples = RENDER.get("samples", 64)
scene.cycles.device = RENDER.get("device", "CPU")
scene.cycles.use_denoising = bool(RENDER.get("use_denoising", True))
scene.render.resolution_x = RENDER.get("resolution_x", 900)
scene.render.resolution_y = RENDER.get("resolution_y", 1050)
scene.render.filepath = PNG_PATH

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH, compress=True)
print(f"Salvato: {BLEND_PATH} | oggetti: {len(scene.objects)} | materiali: {len(bpy.data.materials)}")

try:
    bpy.ops.render.render(write_still=True)
    print(f"Anteprima salvata: {PNG_PATH}")
except Exception as e:
    print(f"Render anteprima non riuscito: {e}")

EXPORT = CFG.get("export", {})
if "gltf" in EXPORT.get("formats", []):
    gltf_opts = EXPORT.get("gltf_options", {})
    try:
        bpy.ops.export_scene.gltf(
            filepath=GLB_PATH,
            export_format=gltf_opts.get("export_format", "GLB"),
            export_apply=gltf_opts.get("export_apply", True),
            export_yup=gltf_opts.get("export_yup", True),
            export_draco_mesh_compression_enable=gltf_opts.get("export_draco_mesh_compression_enable", False),
            export_tangents=gltf_opts.get("export_tangents", True),
            export_materials=gltf_opts.get("export_materials", "EXPORT"),
        )
        print(f"Esportato GLB: {GLB_PATH}")
    except Exception as e:
        print(f"Export GLB non riuscito: {e}")

print("Generazione v1.4 completata!")
sys.stdout.flush()
sys.stderr.flush()
if "bpy" in sys.modules and not bpy.app.binary_path:
    # Evita crash del distruttore C++ TBB in uscita quando bpy gira come modulo pip
    os._exit(0)
