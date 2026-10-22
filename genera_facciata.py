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
Larghezza totale ~30 m, altezza all'angelo ~34 m (proporzioni della facciata reale).
Tutto il modello viene poi riscalato di "scala_globale" (default 3.0) -> ~90 x ~102 m.

MIGLIORAMENTI v1.1:
  1. Configurazione JSON esterna (config_facciata.json)
  2. UV unwrapping automatico per tutti i mesh (pronti per texture)
  3. Esportazione glTF/GLB (formato standard web/game engine)

MIGLIORAMENTI v1.2 (fedelta' alla fotografia di riferimento):
  1. Al posto del rosone gotico a raggiera: il vero OCULO di Camaino di Crescentino,
     con la corona di 34 nicchie gotiche (mezzi busti degli Antenati di Cristo) e la
     Madonna col Bambino nella nicchia centrale superiore.
  2. Silhouette "tricuspidale" corretta: le due guglie sottili spostate a ridosso del
     timpano centrale (x = +-5.2 m e non +-6.9 m, cosi' fra guglia e settore laterale
     torna il vuoto verso il cielo), cuspidi laterali con i mosaici della
     Presentazione e della Nativita' alzate a coronare i settori laterali (con i due
     ordini di loggette), torrioni laterali tozzi con edicole cuspidate e pinnacoli.
  3. Portali di Giovanni Pisano: colonne ritorte, archivolti ritorti con chiave di
     volta a testa di satiro, ghimberghe cuspidate con foglie rampanti e, in sommita',
     la Vergine (al centro) e gli Angeli (ai lati).
  + Il modello viene ingrandito di 3 volte (scala_globale nel JSON).
"""

import bpy
import math
import os
import json
from mathutils import Vector

# -----------------------------------------------------------------------------
# Configurazione
# -----------------------------------------------------------------------------
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(OUT_DIR, "config_facciata.json")
BLEND_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend")
PNG_PATH = os.path.join(OUT_DIR, "anteprima_facciata.png")
GLB_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.glb")


def load_config():
    """Carica configurazione da JSON, con fallback ai default hardcoded."""
    default = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠ Errore lettura config: {e}. Uso default.")
    return default


CFG = load_config()

# -----------------------------------------------------------------------------
# Pulizia scena
# -----------------------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
# rimuovi datablock orfani
for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights, bpy.data.materials):
    for item in block:
        if item.users == 0:
            block.remove(item)

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene["titolo"] = "Duomo di Siena — solo facciata ovest"
scene["nota"] = "Modello procedurale stilizzato da fotografia: solo la facciata, spessore ridotto, retro piatto."

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

# -----------------------------------------------------------------------------
# Materiali da config
# -----------------------------------------------------------------------------
def mat_from_cfg(name, cfg):
    """Crea materiale Principled BSDF da dict config."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    bsdf = nodes.get("Principled BSDF")
    if not bsdf:
        bsdf = nodes.new("ShaderNodeBsdfPrincipled")
        out = nodes.get("Material Output") or nodes.new("ShaderNodeOutputMaterial")
        links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    c = cfg.get("color", [0.8, 0.8, 0.8])
    bsdf.inputs["Base Color"].default_value = (*c, 1.0)
    bsdf.inputs["Roughness"].default_value = cfg.get("roughness", 0.5)
    bsdf.inputs["Metallic"].default_value = cfg.get("metallic", 0.0)

    if "emission" in cfg:
        bsdf.inputs["Emission Color"].default_value = (*cfg["emission"], 1.0)
        bsdf.inputs["Emission Strength"].default_value = cfg.get("emission_strength", 1.0)

    # Trasparenza per vetri
    if cfg.get("transmission", 0) > 0:
        bsdf.inputs["Transmission Weight"].default_value = cfg["transmission"]
        bsdf.inputs["Alpha"].default_value = cfg.get("alpha", 1.0)
        m.blend_method = "BLEND"
        m.shadow_method = "HASHED"

    return m


MAT_CFG = CFG.get("materiali", {})
MATS = {name: mat_from_cfg(name, cfg) for name, cfg in MAT_CFG.items()}

# Shortcut per compatibilità con codice esistente
BIANCO = MATS.get("Marmo_Bianco")
BIANCO2 = MATS.get("Marmo_Bianco_Caldo")
ROSA = MATS.get("Marmo_Rosa")
ROSA_C = MATS.get("Marmo_Rosato_Chiaro")
VERDE = MATS.get("Marmo_Verde_Scuro")
ORO = MATS.get("Mosaico_Oro")
ORO_C = MATS.get("Mosaico_Chiaro")
BRONZO = MATS.get("Bronzo_Portale")
LEGNO = MATS.get("Legno_Portali")
LEGNO_S = MATS.get("Legno_Scuro")
VETRO = MATS.get("Vetro_Rosone")
VETRO_C = MATS.get("Vetro_Chiaro")
PIETRA = MATS.get("Pietra_Statue")
SCURO = MATS.get("Vano_Scuro")
BLU = MATS.get("Mosaico_Blu")
ROSSO = MATS.get("Mosaico_Rosso")

# -----------------------------------------------------------------------------
# UV Unwrapping helper
# -----------------------------------------------------------------------------
def unwrap_uv(obj, method="SMART", margin=0.001):
    """Applica UV unwrap al mesh dell'oggetto."""
    if not obj or obj.type != "MESH":
        return
    # Seleziona solo questo oggetto
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    # NB: in Blender 4.2 gli operatori si chiamano *_project (non *_projection)
    try:
        if method == "SMART":
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=margin, correct_aspect=True)
        elif method == "CUBE":
            bpy.ops.uv.cube_project()
        elif method == "SPHERE":
            bpy.ops.uv.sphere_project()
        elif method == "CYLINDER":
            bpy.ops.uv.cylinder_project()
    except Exception as e:
        # un UV qualsiasi e' meglio di niente: lo script non deve interrompersi
        print(f"⚠ UV unwrap '{method}' non riuscito su {obj.name}: {e}")
    bpy.ops.object.mode_set(mode="OBJECT")
    bpy.ops.object.select_all(action="DESELECT")


def add_uv_map(obj, name="UVMap"):
    """Assicura che esista una UV map."""
    if obj.type == "MESH" and not obj.data.uv_layers:
        obj.data.uv_layers.new(name=name)


# -----------------------------------------------------------------------------
# Helper di costruzione con UV
# -----------------------------------------------------------------------------
def link(obj, col):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def _create_mesh_object(name, mesh, col, location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), material=None):
    """Crea oggetto da mesh data (più veloce di bpy.ops)."""
    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    obj.scale = scale
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    return obj


def box(name, col, x, y, z, sx, sy, sz, material, rot_z=0.0, rot_x=0.0, rot_y=0.0, uv_method="CUBE"):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    # NB: create_cube(size=1) è GIÀ centrato sull'origine (vertici a ±0.5):
    # una ulteriore traslazione di -0.5 sfalserebbe ogni blocco di metà dimensione.
    bmesh.ops.create_cube(bm, size=1.0, matrix=Matrix())
    bm.to_mesh(mesh)
    bm.free()
    obj = _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, rot_y, rot_z), (sx, sy, sz), material)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def cyl(name, col, x, y, z, radius, depth, material, vertices=20,
        rot_x=0.0, rot_y=0.0, rot_z=0.0, scale_y=1.0, uv_method="CYLINDER"):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=vertices,
                          radius1=radius, radius2=radius, depth=depth)
    bm.to_mesh(mesh)
    bm.free()
    obj = _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, rot_y, rot_z), (1.0, scale_y, 1.0), material)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def cone(name, col, x, y, z, r1, r2, depth, material, vertices=12, rot_x=0.0, rot_z=0.0, uv_method="CONE"):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=False, segments=vertices,
                          radius1=r1, radius2=r2, depth=depth)
    # create_cone(depth=d) è già centrato su z=0 (da -d/2 a +d/2)
    bm.to_mesh(mesh)
    bm.free()
    obj = _create_mesh_object(name, mesh, col, (x, y, z), (rot_x, 0.0, rot_z), (1.0, 1.0, 1.0), material)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def sphere(name, col, x, y, z, radius, material, sy=1.0, uv_method="SPHERE"):
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=radius)
    bm.to_mesh(mesh)
    bm.free()
    obj = _create_mesh_object(name, mesh, col, (x, y, z), (0, 0, 0), (1.0, sy, 1.0), material)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def torus(name, col, x, y, z, major, minor, material, rot_x=math.radians(90), rot_y=0.0, uv_method="SMART"):
    """Toro (ghiera, anello, aureola). Costruito a mano: in Blender 4.2
    bmesh non ha piu' l'operatore 'create_torus'."""
    seg_u, seg_v = 40, 10
    verts, faces = [], []
    for i in range(seg_u + 1):
        a = 2.0 * math.pi * i / seg_u
        for j in range(seg_v + 1):
            b = 2.0 * math.pi * j / seg_v
            r = major + minor * math.cos(b)
            verts.append((r * math.cos(a), r * math.sin(a), minor * math.sin(b)))
    for i in range(seg_u):
        for j in range(seg_v):
            v0 = i * (seg_v + 1) + j
            faces.append((v0, v0 + seg_v + 1, v0 + seg_v + 2, v0 + 1))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = (x, y, z)
    obj.rotation_euler = (rot_x, rot_y, 0.0)
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def arch(name, col, cx, y, cz, major, minor, material, uv_method="SMART"):
    """Archivolto a tutto sesto: mezzo toro nel piano XZ (solo meta' superiore)."""
    seg_u, seg_v = 28, 10
    verts, faces = [], []
    for i in range(seg_u + 1):
        a = math.pi * i / seg_u
        for j in range(seg_v + 1):
            b = 2 * math.pi * j / seg_v
            r = major + minor * math.cos(b)
            verts.append((cx + r * math.cos(a), y + minor * math.sin(b), cz + r * math.sin(a)))
    for i in range(seg_u):
        for j in range(seg_v):
            a = i * (seg_v + 1) + j
            faces.append((a, a + seg_v + 1, a + seg_v + 2, a + 1))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def prism(name, col, cx, y, z_base, width, height, depth, material, front_only_depth=None, uv_method="SMART"):
    """Prisma triangolare (timpano): base orizzontale, apice centrato, estruso in Y."""
    w, h, d = width / 2.0, height, depth / 2.0
    verts = [(-w, -d, 0), (w, -d, 0), (0, -d, h),
             (-w,  d, 0), (w,  d, 0), (0,  d, h)]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    obj.location = (cx, y, z_base)
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    add_uv_map(obj)
    unwrap_uv(obj, uv_method)
    return obj


def statue(name, col, x, y, z, h=1.5, material=PIETRA):
    """Statua stilizzata: basamento, corpo a cono/cilindro, testa."""
    box(name + "_base", col, x, y, z + 0.12, 0.42, 0.34, 0.24, BIANCO2)
    cone(name + "_corpo", col, x, y, z + 0.24 + h * 0.36, 0.20, 0.11, h * 0.72, material, vertices=10)
    sphere(name + "_testa", col, x, y, z + 0.24 + h * 0.82, 0.13, material)
    box(name + "_braccia", col, x, y - 0.03, z + 0.24 + h * 0.52, 0.44, 0.16, 0.14, material)


def finial(name, col, x, y, z):
    cyl(name + "_fusto", col, x, y, z + 0.25, 0.07, 0.5, BIANCO, vertices=8)
    sphere(name + "_palla", col, x, y, z + 0.6, 0.12, PIETRA)
    cone(name + "_punta", col, x, y, z + 0.85, 0.09, 0.0, 0.4, PIETRA, vertices=8)


# -----------------------------------------------------------------------------
# MIGLIORAMENTO 3 — elementi di Giovanni Pisano: colonne ritorte, archivolti
# ritorti, foglie rampanti, statue (Vergine / Angeli)
# -----------------------------------------------------------------------------
def colonna_ritorta(name, col, x, y, z, radius, height, material, turns=3.0,
                    segments=12, rings=24, ridges=2, ridge_amp=0.17, taper=0.08):
    """Colonna ritorta ('a vite'): costoloni elicoidali, come negli sguanci dei
    tre portali della facciata inferiore."""
    verts, faces = [], []
    for i in range(rings + 1):
        t = i / float(rings)
        zz = -height / 2.0 + t * height
        ang0 = t * turns * 2.0 * math.pi
        rad = radius * (1.0 - taper * t)
        for j in range(segments):
            a = ang0 + 2.0 * math.pi * j / segments
            rr = rad * (1.0 + ridge_amp * math.cos(ridges * (a - ang0)))
            verts.append((rr * math.cos(a), rr * math.sin(a), zz))
    for i in range(rings):
        for j in range(segments):
            j2 = (j + 1) % segments
            v0 = i * segments + j
            v1 = i * segments + j2
            v2 = (i + 1) * segments + j2
            v3 = (i + 1) * segments + j
            faces.append((v0, v1, v2, v3))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if material:
        obj.data.materials.append(material)
    obj.location = (x, y, z)
    col.objects.link(obj)
    add_uv_map(obj)
    unwrap_uv(obj, "SMART")
    return obj


def arco_ritorto(name, col, cx, y, cz, major, minor, material,
                 seg_u=30, seg_v=14, ribs=8, turns=1.8, amp=0.24):
    """Archivolto ritorto: i costoloni della ghiera girano a elica attorno
    all'arco (come negli archivolti dei portali della facciata)."""
    verts, faces = [], []
    for i in range(seg_u + 1):
        a = math.pi * i / seg_u
        helix = 2.0 * math.pi * turns * i / seg_u
        for j in range(seg_v + 1):
            b = 2.0 * math.pi * j / seg_v
            m = minor * (1.0 + amp * math.cos(ribs * b + helix))
            r = major + m * math.cos(b)
            verts.append((cx + r * math.cos(a), y + m * math.sin(b), cz + r * math.sin(a)))
    for i in range(seg_u):
        for j in range(seg_v):
            v0 = i * (seg_v + 1) + j
            faces.append((v0, v0 + seg_v + 1, v0 + seg_v + 2, v0 + 1))
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if material:
        obj.data.materials.append(material)
    col.objects.link(obj)
    add_uv_map(obj)
    unwrap_uv(obj, "SMART")
    return obj


def testa_satiro(name, col, x, y, z, s=1.0):
    """Chiave di volta degli archivolti: testa di satiro (con corna)."""
    sphere(name + "_testa", col, x, y, z, 0.17 * s, PIETRA)
    cone(name + "_muso", col, x, y - 0.12 * s, z - 0.04 * s, 0.07 * s, 0.04 * s, 0.16 * s,
         PIETRA, vertices=8, rot_x=math.radians(90))
    for s2 in (-1, 1):
        cone(name + f"_corno_{s2}", col, x + s2 * 0.12 * s, y - 0.02 * s, z + 0.10 * s,
             0.035 * s, 0.01 * s, 0.20 * s, PIETRA, vertices=6, rot_z=-s2 * math.radians(35))


def foglie_rampanti(name, col, cx, y, z_base, width, height, material=PIETRA,
                    n=6, size=0.30):
    """Foglie rampanti (crocket) che corrono sulle due pendenze di una ghimberga."""
    for s in (-1, 1):
        for i in range(n):
            t = 0.14 + 0.78 * i / max(1, n - 1)
            x = cx + s * (width / 2.0) * (1.0 - t)
            z = z_base + height * t
            cone(f"{name}_Foglia_{s}_{i}", col, x, y - 0.05, z + size * 0.45,
                 size * 0.30, 0.015, size, material, vertices=6,
                 rot_z=-s * math.radians(40))
            sphere(f"{name}_Bocciolo_{s}_{i}", col, x, y - 0.05, z + size * 1.0,
                   size * 0.15, material)


def statua_angelo(name, col, x, y, z, h=1.30, material=PIETRA):
    """Statua d'angelo: corpo stilizzato + due ali spiegate."""
    statue(name, col, x, y, z, h, material)
    for s in (-1, 1):
        box(f"{name}_Ala_{s}", col, x + s * 0.24, y - 0.06, z + 0.24 + h * 0.58,
            0.13, 0.44, 0.16, material, rot_z=-s * 0.55, rot_y=s * 0.30)


def statua_vergine(name, col, x, y, z, h=1.45, material=PIETRA):
    """Statua della Vergine col Bambino e aureola (ghimberga centrale)."""
    statue(name, col, x, y, z, h, material)
    sphere(f"{name}_Bambino", col, x + 0.17, y - 0.12, z + 0.24 + h * 0.52, 0.12, material)
    torus(f"{name}_Aureola", col, x, y + 0.03, z + 0.24 + h * 0.88, 0.24, 0.05, ORO)


# Import bmesh e Matrix per i primitive helper
import bmesh
from mathutils import Matrix

S = COL["struttura"]; P = COL["portali"]; R = COL["rosone_e_logge"]
G = COL["guglie_e_pinnacoli"]; ST = COL["statue"]; D = COL["dettagli"]

# -----------------------------------------------------------------------------
# Parametri da config
# -----------------------------------------------------------------------------
DIM = CFG.get("dimensioni", {})
W_TOT = DIM.get("larghezza_totale", 30.0)
H_ANGELO = DIM.get("altezza_angelo", 34.0)
THICK = DIM.get("spessore_facciata", 2.6)
H_BASE = DIM.get("altezza_basamento", 1.5)
H_PORTALI = DIM.get("altezza_portali", 5.6)
W_PORT_C = DIM.get("larghezza_portale_centrale", 3.7)
W_PORT_L = DIM.get("larghezza_portali_laterali", 3.1)
R_OCULO = DIM.get("raggio_oculo", 2.0)
Z_OCULO = DIM.get("altezza_centro_oculo", 19.2)
R_CORONA = DIM.get("raggio_corona_nicchie", 2.95)
N_NICCHIE = int(DIM.get("numero_nicchie_oculo", 34))
X_GUGLIE = DIM.get("x_guglie_centrali", 5.2)
W_GUGLIA = DIM.get("larghezza_guglia_centrale", 1.25)
Z0_GUGLIA = DIM.get("base_guglia_centrale", 20.6)
Z1_GUGLIA = DIM.get("colmo_guglia_centrale", 26.2)
Z_CUSP_LAT = DIM.get("base_cuspidi_laterali", 20.5)
H_CUSP_LAT = DIM.get("altezza_cuspidi_laterali", 4.6)

# Fattore di ingrandimento globale del modello (richiesto: almeno il triplo)
SCALA = float(DIM.get("scala_globale", 3.0))

# -----------------------------------------------------------------------------
# 1. Gradinata e basamento (sagrato, parte integrante della facciata)
# -----------------------------------------------------------------------------
for i in range(6):
    box(f"Gradino_{i+1}", S, 0, -3.4 - i * 0.85, 0.55 - i * 0.18,
        36 - i * 0.6, 1.0, 0.19, BIANCO2)
box("Basamento", S, 0, 0, 0.75, 32, 4.6, 1.5, ROSA_C)
box("Zoccolo", S, 0, -0.4, 1.65, 30.5, 3.4, 0.5, BIANCO)

# -----------------------------------------------------------------------------
# 2. Corpo principale — SOLO facciata (spessore 2.6 m, retro piatto)
# -----------------------------------------------------------------------------
box("Corpo_Inferiore", S, 0, 0, 7.0, 30, THICK, 10.2, BIANCO)
box("Corpo_Superiore", S, 0, 0.15, 16.2, 19.5, 2.3, 8.6, BIANCO)
box("Attico", S, 0, 0.15, 21.6, 13.5, 2.3, 2.6, BIANCO2)

# Torri laterali
for side in (-1, 1):
    x = 13.6 * side
    box(f"Torre_Laterale_{side}", S, x, 0, 7.5, 3.0, 2.9, 11.2, BIANCO)
    box(f"Torre_Media_{side}", S, x, 0, 15.2, 2.7, 2.7, 4.6, BIANCO2)
    box(f"Torre_Alta_{side}", S, x, 0, 19.9, 2.3, 2.4, 4.8, BIANCO)
    # fasce bicrome
    for i in range(9):
        m = VERDE if i % 2 == 0 else BIANCO
        box(f"Fascia_Bicroma_{side}_{i}", D, x, -1.52, 2.6 + i * 0.62, 3.06, 0.10, 0.5, m)
    # pannello a losanghe
    for r in range(5):
        for c in range(2):
            box(f"Losanga_{side}_{r}_{c}", D, 11.15 * side + (c - 0.5) * 0.62, -1.36,
                3.2 + r * 0.85, 0.36, 0.08, 0.36,
                ROSA if (r + c) % 2 else BIANCO2, rot_y=math.radians(45))

# Cornicioni orizzontali
for z, w, m in [(2.0, 30.6, VERDE), (8.1, 30.4, BIANCO2), (12.15, 30.6, ROSA_C),
                (22.95, 14.2, BIANCO2)]:
    box(f"Cornicione_{z}", S, 0, -0.55, z, w, 3.3, 0.42, m)
for z, m in [(13.55, BIANCO2), (21.05, ROSA_C)]:
    for s in (-1, 1):
        box(f"Cornicione_Rosone_{z}_{s}", S, s * 7.3, -0.55, z, 5.4, 3.3, 0.38, m)

# -----------------------------------------------------------------------------
# 3. I tre portali
# -----------------------------------------------------------------------------
def portal(cx, door_w, door_h, door_mat, central=False):
    tag = "Centrale" if central else f"Laterale_{int(cx)}"
    front = -1.42
    # vano e porta
    box(f"Vano_{tag}", P, cx, front + 0.25, 1.9 + door_h / 2, door_w + 0.5, 0.5, door_h, SCURO)
    door = box(f"Porta_{tag}", P, cx, front, 1.9 + door_h / 2, door_w, 0.18, door_h, door_mat)
    # pannelli porta
    for px in (-door_w / 4, door_w / 4):
        for pz in range(3):
            box(f"Pannello_{tag}_{px}_{pz}", P, cx + px, front - 0.11,
                2.6 + pz * (door_h / 3.2), door_w / 2.4, 0.05, door_h / 4.2,
                LEGNO_S if door_mat is LEGNO else BRONZO)
    box(f"Soglia_{tag}", P, cx, front - 0.2, 1.95, door_w + 0.6, 0.7, 0.14, BIANCO2)
    # lunetta
    lun_z = 1.9 + door_h
    cyl(f"Lunetta_{tag}", P, cx, front + 0.05, lun_z, door_w / 2 + 0.25, 0.22,
        ORO if central else ROSA_C, vertices=28, rot_x=math.radians(90))
    cyl(f"Lunetta_Vetro_{tag}", P, cx, front - 0.08, lun_z, door_w / 2 - 0.25, 0.10,
        VETRO_C if central else SCURO, vertices=28, rot_x=math.radians(90))
    if central:
        # trigramma bronzeo del nome di Cristo sulla lunetta del portale centrale
        sphere("Stemma_Sole", P, cx, front - 0.2, lun_z + 0.15, 0.42, BRONZO)
        for a in range(12):
            ang = a * math.pi / 6
            box(f"Raggio_{a}", P, cx + math.cos(ang) * 0.72, front - 0.18,
                lun_z + 0.15 + math.sin(ang) * 0.72, 0.42, 0.06, 0.09, BRONZO, rot_y=-ang)
    # archivolto RITORTO + conci bicromi + chiave di volta a testa di satiro
    arco_ritorto(f"Arco_{tag}", P, cx, front - 0.05, lun_z, door_w / 2 + 0.35, 0.30, BIANCO2,
                 ribs=8, turns=1.8, amp=0.24)
    for i in range(9):
        ang = math.pi * (0.08 + 0.84 * i / 8)
        box(f"Concio_{tag}_{i}", P,
            cx + math.cos(ang) * (door_w / 2 + 0.72), front - 0.05,
            lun_z + math.sin(ang) * (door_w / 2 + 0.72),
            0.55, 0.28, 0.55, VERDE if i % 2 == 0 else BIANCO, rot_y=-ang)
    # chiave di volta: testa di satiro
    testa_satiro(f"Chiave_{tag}", P, cx, front - 0.12,
                 lun_z + door_w / 2 + 0.70, 1.0 if central else 0.85)
    # COLONNE RITORTE con capitelli a fogliame
    for s in (-1, 1):
        for k in range(3):
            xx = cx + s * (door_w / 2 + 0.55 + k * 0.42)
            colonna_ritorta(f"Colonna_{tag}_{s}_{k}", P,
                            xx, front - 0.05 - (0.12 if k == 1 else 0),
                            1.9 + door_h / 2, 0.16, door_h,
                            BIANCO if k != 1 else ROSA,
                            turns=3.0, ridges=2)
            # collarino / base attorcigliata
            cyl(f"Collarino_{tag}_{s}_{k}", P, xx, front - 0.05 - (0.12 if k == 1 else 0),
                1.9 + door_h / 2, 0.19, 0.22, BIANCO2, vertices=12)
            box(f"Capitello_{tag}_{s}_{k}", P, xx, front - 0.05, 1.9 + door_h + 0.05,
                0.42, 0.42, 0.3, BIANCO2)
            sphere(f"Fogliame_{tag}_{s}_{k}", P, xx, front - 0.05, 1.9 + door_h + 0.02,
                   0.17, PIETRA, sy=0.6)
            box(f"BaseCol_{tag}_{s}_{k}", P, xx, front - 0.05, 2.05, 0.42, 0.42, 0.3, BIANCO2)
    # GHIMBERGA cuspidata: foglie rampanti sulle pendenze, busto nel medaglione
    # (i busti dei beati senesi furono aggiunti nel XVII secolo) e, in sommita',
    # la Vergine su quella centrale e gli Angeli su quelle laterali.
    gz = 1.9 + door_h + door_w / 2 + 0.55
    gw = door_w + 2.6          # larghezza della ghimberga
    gh = 2.6                   # altezza della ghimberga
    prism(f"Timpano_{tag}", P, cx, -0.85, gz, gw, gh, 1.1, BIANCO)
    prism(f"Mosaico_Timpano_{tag}", P, cx, -1.48, gz + 0.35, door_w + 1.5, 1.8, 0.12, ORO_C)
    foglie_rampanti(f"Ghimberga_{tag}", P, cx, -1.42, gz, gw, gh, PIETRA, n=6, size=0.30)
    # cuspide sommitale della ghimberga
    cone(f"Cuspide_Ghimberga_{tag}", P, cx, -1.30, gz + gh + 0.18, 0.16, 0.0, 0.55, PIETRA, vertices=8)
    # medaglione con busto (beziers)
    torus(f"Medaglione_{tag}", P, cx, front - 0.15, gz + 1.05, 0.48, 0.12, ROSA)
    cyl(f"Medaglione_Centro_{tag}", P, cx, front - 0.12, gz + 1.05, 0.42, 0.1,
        ORO, vertices=20, rot_x=math.radians(90))
    sphere(f"Busto_Medaglione_{tag}", P, cx, front - 0.20, gz + 1.22, 0.20, PIETRA)
    if central:
        statua_vergine("Statua_Vergine_Ghimberga", ST, cx, front - 0.1, gz + 2.45, 1.40)
    else:
        statua_angelo(f"Statua_Angelo_Ghimberga_{tag}", ST, cx, front - 0.1, gz + 2.45, 1.25)
    for s in (-1, 1):
        statua_angelo(f"Statua_Porta_{tag}_{s}", ST, cx + s * (door_w / 2 + 1.15),
                      front - 0.15, gz - 0.15, 1.30)


portal(-7.6, W_PORT_L, 5.0, LEGNO)
portal(0.0, W_PORT_C, H_PORTALI, BRONZO, central=True)
portal(7.6, W_PORT_L, 5.0, LEGNO)

# -----------------------------------------------------------------------------
# 4. Settori laterali (DUE ORDINI DI LOGGETTE + cuspidi dorate) e OCULO centrale
# -----------------------------------------------------------------------------
for side in (-1, 1):
    cx = 11.3 * side
    # --- primo ordine di loggette (inferiore) ---
    box(f"Loggia1_Fondo_{side}", R, cx, -0.95, 15.6, 5.6, 0.3, 3.4, SCURO)
    for i in range(5):
        cyl(f"Colonnina_Loggia1_{side}_{i}", R, cx - 2.2 + i * 1.1, -1.55, 15.9, 0.11, 2.6, BIANCO, vertices=10)
    box(f"Loggia1_Trave_{side}", R, cx, -1.5, 17.35, 5.6, 0.35, 0.4, BIANCO2)
    # --- secondo ordine di loggette (superiore) ---
    box(f"Loggia2_Fondo_{side}", R, cx, -0.95, 18.95, 5.6, 0.3, 2.9, SCURO)
    for i in range(7):
        cyl(f"Colonnina_Loggia2_{side}_{i}", R, cx - 2.4 + i * 0.8, -1.55, 19.0, 0.09, 2.2, BIANCO, vertices=10)
    box(f"Loggia2_Trave_{side}", R, cx, -1.5, 20.35, 5.6, 0.35, 0.35, BIANCO2)
    # --- cuspide laterale dorata: Presentazione di Maria al Tempio / Nativita' ---
    prism(f"Timpano_Laterale_{side}", R, cx, -0.75, Z_CUSP_LAT, 5.4, H_CUSP_LAT, 1.2, BIANCO)
    prism(f"Mosaico_Laterale_{side}", R, cx, -1.42, Z_CUSP_LAT + 0.45, 4.2, H_CUSP_LAT - 1.4, 0.12, ORO)
    cyl(f"Figura_Mosaico_{side}", R, cx - 0.7 * side, -1.50, Z_CUSP_LAT + 1.6, 0.40, 0.08, BLU, vertices=20, rot_x=math.radians(90))
    cyl(f"Figura2_Mosaico_{side}", R, cx + 0.8 * side, -1.50, Z_CUSP_LAT + 1.3, 0.34, 0.08, ROSSO, vertices=20, rot_x=math.radians(90))
    cyl(f"Figura3_Mosaico_{side}", R, cx, -1.50, Z_CUSP_LAT + 2.1, 0.30, 0.08, ORO_C, vertices=20, rot_x=math.radians(90))
    foglie_rampanti(f"Cuspide_Lat_{side}", D, cx, -1.44, Z_CUSP_LAT, 5.4, H_CUSP_LAT, PIETRA, n=5, size=0.26)
    finial(f"Pinnacolino_Cuspide_{side}", G, cx, -1.1, Z_CUSP_LAT + H_CUSP_LAT)

# --- OCULO centrale (al posto del rosone) con la corona di nicchie gotiche ---
RX, RZ, RR = 0.0, Z_OCULO, R_OCULO
# vetrata dell'oculo (l'Ultima Cena di Pastorino dei Pastorini)
cyl("Oculo_Vetro", R, RX, -1.30, RZ, RR, 0.16, VETRO, vertices=48, rot_x=math.radians(90))
# ghiera marmorea dell'oculo
torus("Oculo_Cornice", R, RX, -1.46, RZ, RR + 0.22, 0.30, BIANCO2)
torus("Oculo_Anello_Rosa", R, RX, -1.50, RZ, RR + 0.60, 0.13, ROSA)
# corona di nicchie gotiche con i 34 mezzi busti degli Antenati di Cristo
for i in range(N_NICCHIE):
    a = math.pi / 2.0 + 2.0 * math.pi * i / N_NICCHIE      # i = 0 -> nicchia in alto
    nx = RX + math.cos(a) * R_CORONA
    nz = RZ + math.sin(a) * R_CORONA
    box(f"Nicchia_Ant_{i}_Fondo", R, nx, -1.30, nz, 0.46, 0.22, 0.60, SCURO)
    prism(f"Nicchia_Ant_{i}_Arco", R, nx, -1.36, nz + 0.30, 0.46, 0.34, 0.24, SCURO)
    box(f"Nicchia_Ant_{i}_Edicola", R, nx, -1.24, nz + 0.05, 0.62, 0.10, 0.72, BIANCO2)
    cone(f"Nicchia_Ant_{i}_Busto", R, nx, -1.38, nz + 0.02, 0.15, 0.09, 0.34, PIETRA, vertices=10)
    sphere(f"Nicchia_Ant_{i}_Testa", R, nx, -1.38, nz + 0.34, 0.12, PIETRA)
    if i == 0:
        # nicchia centrale superiore: la Madonna col Bambino
        sphere("Madonna_Bambino", R, nx + 0.15, -1.44, nz + 0.22, 0.10, ORO_C)
        torus("Madonna_Aureola", R, nx, -1.32, nz + 0.42, 0.20, 0.045, ORO)
statue("Statua_Sotto_Oculo", ST, RX, -1.55, RZ - R_CORONA - 1.15, 1.2)

for side in (-1, 1):
    for i in range(3):
        statue(f"Statua_Galleria_{side}_{i}", ST, side * (4.6 + i * 1.7), -1.5, 12.35, 1.45)

# -----------------------------------------------------------------------------
# 5. Timpano centrale, mosaico dell'Incoronazione e angelo apicale
# -----------------------------------------------------------------------------
prism("Timpano_Centrale", S, 0, 0.0, 22.9, 12.4, 8.4, 2.5, BIANCO)
prism("Mosaico_Centrale", S, 0, -1.32, 23.7, 9.6, 6.2, 0.14, ORO)
prism("Mosaico_Centrale_Interno", S, 0, -1.42, 24.3, 7.2, 4.4, 0.10, ORO_C)
cyl("Figura_Cristo", D, 0.5, -1.50, 27.6, 0.48, 0.08, BLU, vertices=20, rot_x=math.radians(90))
cyl("Figura_Madonna", D, -0.9, -1.50, 27.2, 0.42, 0.08, ROSSO, vertices=20, rot_x=math.radians(90))
for i, dx in enumerate((-2.6, -1.8, 1.9, 2.7, -0.2)):
    cyl(f"Angelo_Mosaico_{i}", D, dx, -1.50, 25.6 + abs(dx) * 0.12, 0.26, 0.08, BIANCO2, vertices=16, rot_x=math.radians(90))
for i in range(11):
    box(f"Archetto_Timpano_{i}", D, -6.0 + i * 1.2, -1.3, 22.55, 0.7, 0.2, 0.55, ROSA if i % 2 else BIANCO2)
statue("Angelo_Apicale", ST, 0, -0.6, 31.35, 2.0, ORO_C)
for s in (-1, 1):
    box(f"Ala_Angelo_{s}", ST, s * 0.55, -0.55, 33.05, 0.16, 0.5, 1.15, ORO_C, rot_z=s * 0.6, rot_y=s * 0.35)

# -----------------------------------------------------------------------------
# 6. Guglie e pinnacoli
# -----------------------------------------------------------------------------
def pinnacle(cx, z0, z1, w, tag):
    box(f"{tag}_Fusto", G, cx, -0.4, (z0 + z1) / 2, w, 1.7, z1 - z0, BIANCO)
    box(f"{tag}_Cornice", G, cx, -0.4, z1, w + 0.45, 2.0, 0.4, ROSA_C)
    for sx in (-1, 1):
        for sy in (-1, 1):
            finial(f"{tag}_ang{sx}_{sy}", G, cx + sx * w / 2, -0.4 + sy * 0.7, z1 + 0.15)
    cone(f"{tag}_Cuspide", G, cx, -0.4, z1 + 1.5, w * 0.62, 0.02, 3.0, PIETRA, vertices=8)
    sphere(f"{tag}_Palla", G, cx, -0.4, z1 + 3.15, 0.16, ORO)
    statue(f"{tag}_Statua", ST, cx, -1.35, z0 + 1.2, 1.5)
    box(f"{tag}_Lancetta", G, cx, -1.32, (z0 + z1) / 2 + 1.0, 0.55, 0.12, 2.2, SCURO)


def guglia_sottile(cx, z0, z1, w, tag):
    """Pilastro che incornicia la struttura centrale: termina in pinnacolo e
    quindi in una SOTTILISSIMA guglia (Camaino di Crescentino)."""
    box(f"{tag}_Pilastro", G, cx, -0.55, (z0 + z1) / 2, w, 1.7, z1 - z0, BIANCO)
    box(f"{tag}_Cornice", G, cx, -0.55, z1, w + 0.55, 2.0, 0.45, ROSA_C)
    for sx in (-1, 1):
        for sy in (-1, 1):
            finial(f"{tag}_ang{sx}_{sy}", G, cx + sx * (w / 2 + 0.15), -0.55 + sy * 0.62, z1 + 0.15)
    box(f"{tag}_Lancetta", G, cx, -1.34, (z0 + z1) / 2 + 1.2, 0.42, 0.12, 2.0, SCURO)
    prism(f"{tag}_Lancetta_Cima", G, cx, -1.36, (z0 + z1) / 2 + 2.2, 0.42, 0.55, 0.10, SCURO)
    cone(f"{tag}_Cuspide", G, cx, -0.55, z1 + 1.85, w * 0.5, 0.02, 3.7, PIETRA, vertices=8)
    sphere(f"{tag}_Palla", G, cx, -0.55, z1 + 3.78, 0.15, ORO)
    cone(f"{tag}_Punta", G, cx, -0.55, z1 + 4.10, 0.07, 0.0, 0.6, ORO, vertices=8)


def coronamento_torre(cx, z1, w, tag):
    """Torrione laterale TOZZO e robusto: coronamento gotico con edicole
    cuspidate e statue, pinnacolo basso (niente grandi guglie esterne)."""
    box(f"{tag}_Cornicione", G, cx, -0.4, z1, w + 1.1, 2.7, 0.5, ROSA_C)
    for s in (-1, 1):
        x = cx + s * (w / 2 + 0.55)
        box(f"{tag}_Edicola_{s}", G, x, -1.25, z1 + 0.85, 0.85, 0.35, 1.1, BIANCO2)
        prism(f"{tag}_Edicola_Cuspide_{s}", G, x, -1.42, z1 + 1.40, 0.95, 0.95, 0.35, PIETRA)
        statue(f"{tag}_Statua_{s}", ST, x, -1.50, z1 + 0.52, 1.05)
    box(f"{tag}_Pinnacolo_Fusto", G, cx, -0.4, z1 + 0.65, 0.24, 0.24, 0.8, BIANCO)
    cone(f"{tag}_Pinnacolo_Cuspide", G, cx, -0.4, z1 + 1.55, 0.20, 0.0, 1.0, PIETRA, vertices=8)
    sphere(f"{tag}_Pinnacolo_Palla", G, cx, -0.4, z1 + 2.12, 0.13, ORO)


# le due guglie sottili a ridosso del timpano centrale (x = +-5.2 m)
guglia_sottile(-X_GUGLIE, Z0_GUGLIA, Z1_GUGLIA, W_GUGLIA, "Guglia_Centrale_Sx")
guglia_sottile(X_GUGLIE, Z0_GUGLIA, Z1_GUGLIA, W_GUGLIA, "Guglia_Centrale_Dx")
# i due torrioni laterali: coronamento basso con edicole cuspidate
coronamento_torre(-13.6, 22.3, 2.3, "Torre_Esterna_Sx")
coronamento_torre(13.6, 22.3, 2.3, "Torre_Esterna_Dx")

# Gargolle
for side in (-1, 1):
    for z, tag in [(9.2, "basso"), (14.8, "alto")]:
        cone(f"Gargolla_{side}_{tag}", D, side * 15.6, -1.6, z, 0.16, 0.34, 1.5,
             PIETRA, vertices=8, rot_x=math.radians(100))
        sphere(f"Testa_Gargolla_{side}_{tag}", D, side * 15.6, -2.25, z - 0.35, 0.2, PIETRA)

# Finestre torri
for side in (-1, 1):
    for z in (10.6, 15.3, 19.8):
        box(f"Lancetta_Torre_{side}_{z}", D, 13.6 * side, -1.5, z, 0.65, 0.12, 2.0, SCURO)
        prism(f"Lancetta_Cima_{side}_{z}", D, 13.6 * side, -1.52, z + 1.0, 0.65, 0.7, 0.1, SCURO)
        cyl(f"Lancetta_Col_{side}_{z}", D, 13.6 * side, -1.58, z, 0.07, 2.0, BIANCO, vertices=8)

# Statue bordi
for side in (-1, 1):
    # statue appoggiate alle due travi delle loggette (due ordini)
    for i, (dx, z) in enumerate([(2.3, 18.3), (1.2, 21.3), (-1.2, 21.3), (-2.3, 18.3)]):
        statue(f"Statua_Bordo_{side}_{i}", ST, 11.3 * side + dx, -1.35, z - 0.7, 1.15)

# -----------------------------------------------------------------------------
# 7. Luci, camera, mondo — inquadratura frontale come nella foto
# -----------------------------------------------------------------------------
L_SOLE = CFG.get("luci", {}).get("sole", {})
sole_loc = tuple(v * SCALA for v in L_SOLE.get("location", (18, -30, 38)))
bpy.ops.object.light_add(type="SUN", location=sole_loc)
sun = bpy.context.object
sun.name = "Sole"
sun.rotation_euler = tuple(math.radians(a) for a in L_SOLE.get("rotation", (52, 8, -32)))
sun.data.energy = L_SOLE.get("energy", 3.2)
sun.data.angle = math.radians(L_SOLE.get("angle", 4))

L_FILL = CFG.get("luci", {}).get("fill_frontale", {})
fill_loc = tuple(v * SCALA for v in L_FILL.get("location", (0, -34, 16)))
bpy.ops.object.light_add(type="AREA", location=fill_loc)
fill = bpy.context.object
fill.name = "Luce_Frontale"
# con la scena ingrandita di SCALA, l'area cresce di SCALA^2: la potenza va
# scalata allo stesso modo per mantenere la stessa illuminazione
fill.data.energy = L_FILL.get("energy", 900) * (SCALA ** 2)
fill.data.shape = "DISK"
fill.data.size = L_FILL.get("size", 22) * SCALA
fill.rotation_euler = (math.radians(90), 0, 0)

CAM = CFG.get("camera", {})
cam_loc = Vector(tuple(v * SCALA for v in CAM.get("location", (7.5, -52, 15.5))))
bpy.ops.object.camera_add(location=tuple(cam_loc))
cam = bpy.context.object
cam.name = "Camera_Frontale"
cam.data.lens = CAM.get("lens", 42)
direction = Vector(tuple(v * SCALA for v in CAM.get("look_at", (0, 0, 14.5)))) - cam_loc
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

WORLD = CFG.get("mondo", {})
world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (*WORLD.get("sky_color", (0.62, 0.72, 0.86)), 1.0)
bg.inputs[1].default_value = WORLD.get("sky_strength", 0.7)

# -----------------------------------------------------------------------------
# 8. Ingrandimento globale del modello ("scala_globale", di default 3x)
# -----------------------------------------------------------------------------
if abs(SCALA - 1.0) > 1e-9:
    for o in scene.objects:
        if o.type == "MESH":
            o.location = [v * SCALA for v in o.location]
            o.scale = [v * SCALA for v in o.scale]
    # congela il fattore di scala nei dati mesh: oggetti di nuovo a scale 1:1
    bpy.ops.object.select_all(action="DESELECT")
    meshes = [o for o in scene.objects if o.type == "MESH"]
    for o in meshes:
        o.select_set(True)
    if meshes:
        bpy.context.view_layer.objects.active = meshes[0]
        try:
            bpy.ops.object.transform_apply(location=False, rotation=False,
                                           scale=True, properties=False)
        except Exception as e:
            print(f"⚠ transform_apply non riuscito ({e}): la scala resta sugli oggetti")
    print(f"Ingrandimento x{SCALA}: il modello passa a "
          f"~{W_TOT * SCALA:.0f} m di larghezza x ~{H_ANGELO * SCALA:.0f} m di altezza")

# -----------------------------------------------------------------------------
# 9. Salvataggio .blend + anteprima + export glTF
# -----------------------------------------------------------------------------
for o in scene.objects:
    o.select_set(False)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print(f"Salvato: {BLEND_PATH} | oggetti: {len(scene.objects)}")

# Anteprima render
RENDER = CFG.get("render", {})
scene.render.engine = RENDER.get("engine", "CYCLES")
scene.cycles.samples = RENDER.get("samples", 48)
scene.cycles.device = RENDER.get("device", "CPU")
scene.render.resolution_x = RENDER.get("resolution_x", 900)
scene.render.resolution_y = RENDER.get("resolution_y", 1050)
scene.render.filepath = PNG_PATH
try:
    bpy.ops.render.render(write_still=True)
    print(f"Anteprima: {PNG_PATH}")
except Exception as e:
    print(f"Render anteprima non riuscito (il .blend e' comunque valido): {e}")

# Export glTF/GLB
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

print("✅ Generazione completata!")