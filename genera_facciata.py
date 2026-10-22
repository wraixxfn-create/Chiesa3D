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

Coordinate: X = larghezza (m), Y = profondita' (fronte verso -Y), Z = altezza (m).
Larghezza totale ~30 m, altezza all'angelo ~34 m (proporzioni della facciata reale).
"""

import bpy
import math
import os
from mathutils import Vector

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
BLEND_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend")
PNG_PATH = os.path.join(OUT_DIR, "anteprima_facciata.png")

# ----------------------------------------------------------------------------
# Pulizia scena
# ----------------------------------------------------------------------------
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
for block in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
    pass  # i datablock orfani vengono rimossi al salvataggio

scene = bpy.context.scene
scene.unit_settings.system = "METRIC"
scene.unit_settings.scale_length = 1.0
scene["titolo"] = "Duomo di Siena — solo facciata ovest"
scene["nota"] = "Modello procedurale stilizzato da fotografia: solo la facciata, spessore ridotto, retro piatto."

# ----------------------------------------------------------------------------
# Collezioni
# ----------------------------------------------------------------------------
def make_collection(name, parent=None):
    c = bpy.data.collections.new(name)
    (parent or scene.collection).children.link(c)
    return c

COL = {
    "struttura": make_collection("01_Struttura"),
    "portali":   make_collection("02_Portali"),
    "rosone":    make_collection("03_Rosone_e_logge"),
    "guglie":    make_collection("04_Guglie_e_pinnacoli"),
    "statue":    make_collection("05_Statue"),
    "dettagli":  make_collection("06_Dettagli"),
}

# ----------------------------------------------------------------------------
# Materiali (marmi della facciata: bianco, rosa, verde serpentino, oro)
# ----------------------------------------------------------------------------
def mat(name, color, roughness=0.65, metallic=0.0, emission=None, emission_strength=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    if emission is not None:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    return m

BIANCO = mat("Marmo_Bianco",      (0.87, 0.83, 0.75), 0.55)
BIANCO2 = mat("Marmo_Bianco_Caldo", (0.80, 0.74, 0.63), 0.6)
ROSA   = mat("Marmo_Rosa",        (0.72, 0.52, 0.45), 0.6)
ROSA_C = mat("Marmo_Rosato_Chiaro", (0.82, 0.66, 0.58), 0.6)
VERDE  = mat("Marmo_Verde_Scuro", (0.10, 0.14, 0.12), 0.5)
ORO    = mat("Mosaico_Oro",       (0.83, 0.62, 0.16), 0.35, 0.65, (0.45, 0.30, 0.05), 0.35)
ORO_C  = mat("Mosaico_Chiaro",    (0.90, 0.75, 0.38), 0.4, 0.4)
BRONZO = mat("Bronzo_Portale",    (0.09, 0.07, 0.05), 0.45, 0.75)
LEGNO  = mat("Legno_Portali",     (0.30, 0.17, 0.08), 0.75)
LEGNO_S = mat("Legno_Scuro",      (0.20, 0.11, 0.05), 0.8)
VETRO  = mat("Vetro_Rosone",      (0.04, 0.07, 0.11), 0.12, 0.1, (0.02, 0.04, 0.08), 0.4)
VETRO_C = mat("Vetro_Chiaro",     (0.25, 0.38, 0.48), 0.15, 0.0, (0.05, 0.08, 0.12), 0.4)
PIETRA = mat("Pietra_Statue",     (0.78, 0.75, 0.68), 0.7)
SCURO  = mat("Vano_Scuro",        (0.05, 0.05, 0.05), 0.9)
BLU    = mat("Mosaico_Blu",       (0.15, 0.25, 0.55), 0.4, 0.2)
ROSSO  = mat("Mosaico_Rosso",     (0.55, 0.16, 0.12), 0.4, 0.2)

# ----------------------------------------------------------------------------
# Helper di costruzione
# ----------------------------------------------------------------------------
def link(obj, col):
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)
    return obj

def box(name, col, x, y, z, sx, sy, sz, material, rot_z=0.0, rot_x=0.0, rot_y=0.0):
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.dimensions = (sx, sy, sz)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.rotation_euler = (rot_x, rot_y, rot_z)
    if material:
        o.data.materials.append(material)
    return link(o, col)

def cyl(name, col, x, y, z, radius, depth, material, vertices=20,
        rot_x=0.0, rot_y=0.0, rot_z=0.0, scale_y=1.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth,
                                        location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.rotation_euler = (rot_x, rot_y, rot_z)
    o.scale = (1.0, scale_y, 1.0)
    if material:
        o.data.materials.append(material)
    return link(o, col)

def cone(name, col, x, y, z, r1, r2, depth, material, vertices=12, rot_x=0.0, rot_z=0.0):
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=depth,
                                    location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.rotation_euler = (rot_x, 0.0, rot_z)
    if material:
        o.data.materials.append(material)
    return link(o, col)

def sphere(name, col, x, y, z, radius, material, sy=1.0):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=12, radius=radius,
                                         location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.scale = (1.0, sy, 1.0)
    if material:
        o.data.materials.append(material)
    return link(o, col)

def torus(name, col, x, y, z, major, minor, material, rot_x=math.radians(90), rot_y=0.0):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor,
                                     major_segments=40, minor_segments=10,
                                     location=(x, y, z))
    o = bpy.context.object
    o.name = name
    o.rotation_euler = (rot_x, rot_y, 0.0)
    if material:
        o.data.materials.append(material)
    return link(o, col)

def arch(name, col, cx, y, cz, major, minor, material):
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
    o = bpy.data.objects.new(name, mesh)
    if material:
        o.data.materials.append(material)
    col.objects.link(o)
    return o

def prism(name, col, cx, y, z_base, width, height, depth, material, front_only_depth=None):
    """Prisma triangolare (timpano): base orizzontale, apice centrato, estruso in Y."""
    w, h, d = width / 2.0, height, depth / 2.0
    verts = [(-w, -d, 0), (w, -d, 0), (0, -d, h),
             (-w,  d, 0), (w,  d, 0), (0,  d, h)]
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    mesh = bpy.data.meshes.new(name + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(name, mesh)
    o.location = (cx, y, z_base)
    if material:
        o.data.materials.append(material)
    col.objects.link(o)
    return o

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

S = COL["struttura"]; P = COL["portali"]; R = COL["rosone"]
G = COL["guglie"]; ST = COL["statue"]; D = COL["dettagli"]

# ----------------------------------------------------------------------------
# 1. Gradinata e basamento (sagrato, parte integrante della facciata)
# ----------------------------------------------------------------------------
for i in range(6):
    box(f"Gradino_{i+1}", S, 0, -3.4 - i * 0.85, 0.55 - i * 0.18, 36 - i * 0.6, 1.0, 0.19, BIANCO2)
box("Basamento", S, 0, 0, 0.75, 32, 4.6, 1.5, ROSA_C)
box("Zoccolo", S, 0, -0.4, 1.65, 30.5, 3.4, 0.5, BIANCO)

# ----------------------------------------------------------------------------
# 2. Corpo principale — SOLO facciata (spessore 2.6 m, retro piatto)
# ----------------------------------------------------------------------------
box("Corpo_Inferiore", S, 0, 0, 7.0, 30, 2.6, 10.2, BIANCO)          # z 1.9..12.1
box("Corpo_Superiore", S, 0, 0.15, 16.2, 19.5, 2.3, 8.6, BIANCO)      # blocco del rosone
box("Attico", S, 0, 0.15, 21.6, 13.5, 2.3, 2.6, BIANCO2)              # fascia sopra il rosone

# Torri laterali (angoli della facciata)
for side in (-1, 1):
    x = 13.6 * side
    box(f"Torre_Laterale_{side}", S, x, 0, 7.5, 3.0, 2.9, 11.2, BIANCO)
    box(f"Torre_Media_{side}", S, x, 0, 15.2, 2.7, 2.7, 4.6, BIANCO2)
    box(f"Torre_Alta_{side}", S, x, 0, 19.9, 2.3, 2.4, 4.8, BIANCO)
    # fasce bicrome bianco/verde sulla parte bassa delle torri
    for i in range(9):
        m = VERDE if i % 2 == 0 else BIANCO
        box(f"Fascia_Bicroma_{side}_{i}", D, x, -1.52, 2.6 + i * 0.62, 3.06, 0.10, 0.5, m)
    # pannello a losanghe tra torre e portale laterale
    for r in range(5):
        for c in range(2):
            box(f"Losanga_{side}_{r}_{c}", D, 11.15 * side + (c - 0.5) * 0.62, -1.36,
                3.2 + r * 0.85, 0.36, 0.08, 0.36, ROSA if (r + c) % 2 else BIANCO2, rot_y=math.radians(45))

# Cornicioni orizzontali
for z, w, m in [(2.0, 30.6, VERDE), (8.1, 30.4, BIANCO2), (12.15, 30.6, ROSA_C),
                (22.95, 14.2, BIANCO2)]:
    box(f"Cornicione_{z}", S, 0, -0.55, z, w, 3.3, 0.42, m)
for z, m in [(13.55, BIANCO2), (21.05, ROSA_C)]:
    for s in (-1, 1):
        box(f"Cornicione_Rosone_{z}_{s}", S, s * 7.3, -0.55, z, 5.4, 3.3, 0.38, m)

# ----------------------------------------------------------------------------
# 3. I tre portali
# ----------------------------------------------------------------------------
def portal(cx, door_w, door_h, door_mat, central=False):
    tag = "Centrale" if central else f"Laterale_{int(cx)}"
    front = -1.42
    # vano e porta
    box(f"Vano_{tag}", P, cx, front + 0.25, 1.9 + door_h / 2, door_w + 0.5, 0.5, door_h, SCURO)
    door = box(f"Porta_{tag}", P, cx, front, 1.9 + door_h / 2, door_w, 0.18, door_h, door_mat)
    # pannelli della porta
    for px in (-door_w / 4, door_w / 4):
        for pz in range(3):
            box(f"Pannello_{tag}_{px}_{pz}", P, cx + px, front - 0.11, 2.6 + pz * (door_h / 3.2),
                door_w / 2.4, 0.05, door_h / 4.2, LEGNO_S if door_mat is LEGNO else BRONZO)
    box(f"Soglia_{tag}", P, cx, front - 0.2, 1.95, door_w + 0.6, 0.7, 0.14, BIANCO2)
    # lunetta semicircolare sopra la porta
    lun_z = 1.9 + door_h
    cyl(f"Lunetta_{tag}", P, cx, front + 0.05, lun_z, door_w / 2 + 0.25, 0.22,
        ORO if central else ROSA_C, vertices=28, rot_x=math.radians(90))
    cyl(f"Lunetta_Vetro_{tag}", P, cx, front - 0.08, lun_z, door_w / 2 - 0.25, 0.10,
        VETRO_C if central else SCURO, vertices=28, rot_x=math.radians(90))
    if central:  # sole raggiante (stemma) nella lunetta centrale
        sphere("Stemma_Sole", P, cx, front - 0.2, lun_z + 0.15, 0.42, ORO)
        for a in range(12):
            ang = a * math.pi / 6
            box(f"Raggio_{a}", P, cx + math.cos(ang) * 0.72, front - 0.18,
                lun_z + 0.15 + math.sin(ang) * 0.72, 0.42, 0.06, 0.09, ORO, rot_y=-ang)
    # arco a tutto sesto: archivolto + conci bicromi
    arch(f"Arco_{tag}", P, cx, front - 0.05, lun_z, door_w / 2 + 0.35, 0.30, BIANCO2)
    for i in range(9):  # conci bicromi dell'archivolto
        ang = math.pi * (0.08 + 0.84 * i / 8)
        box(f"Concio_{tag}_{i}", P, cx + math.cos(ang) * (door_w / 2 + 0.72), front - 0.05,
            lun_z + math.sin(ang) * (door_w / 2 + 0.72), 0.55, 0.28, 0.55,
            VERDE if i % 2 == 0 else BIANCO, rot_y=-ang)
    # colonne ai lati (tre per parte, una tortile)
    for s in (-1, 1):
        for k in range(3):
            xx = cx + s * (door_w / 2 + 0.55 + k * 0.42)
            cyl(f"Colonna_{tag}_{s}_{k}", P, xx, front - 0.05 - (0.12 if k == 1 else 0),
                1.9 + door_h / 2, 0.16, door_h, BIANCO if k != 1 else ROSA, vertices=12)
            box(f"Capitello_{tag}_{s}_{k}", P, xx, front - 0.05, 1.9 + door_h + 0.05,
                0.42, 0.42, 0.3, BIANCO2)
            box(f"BaseCol_{tag}_{s}_{k}", P, xx, front - 0.05, 2.05, 0.42, 0.42, 0.3, BIANCO2)
    # timpano triangolare (ghimberga) sopra il portale, con medaglione
    gz = 1.9 + door_h + door_w / 2 + 0.55
    prism(f"Timpano_{tag}", P, cx, -0.85, gz, door_w + 2.6, 2.6, 1.1, BIANCO)
    prism(f"Mosaico_Timpano_{tag}", P, cx, -1.48, gz + 0.35, door_w + 1.5, 1.8, 0.12, ORO_C)
    torus(f"Medaglione_{tag}", P, cx, front - 0.15, gz + 1.05, 0.48, 0.12, ROSA)
    cyl(f"Medaglione_Centro_{tag}", P, cx, front - 0.12, gz + 1.05, 0.42, 0.1,
        ORO, vertices=20, rot_x=math.radians(90))
    statue(f"Statua_Timpano_{tag}", ST, cx, front - 0.1, gz + 2.45, 1.15)
    for s in (-1, 1):  # statue ai piedi del timpano
        statue(f"Statua_Porta_{tag}_{s}", ST, cx + s * (door_w / 2 + 1.15), front - 0.15, gz - 0.15, 1.35)

portal(-7.6, 3.1, 5.0, LEGNO)
portal(0.0, 3.7, 5.6, BRONZO, central=True)
portal(7.6, 3.1, 5.0, LEGNO)

# ----------------------------------------------------------------------------
# 4. Logge laterali e rosone centrale (registro superiore)
# ----------------------------------------------------------------------------
for side in (-1, 1):  # loggette ad archetti beside rosone
    cx = 11.3 * side
    box(f"Loggia_Fondo_{side}", R, cx, -0.95, 15.6, 5.6, 0.3, 3.4, SCURO)
    for i in range(5):
        cyl(f"Colonnina_Loggia_{side}_{i}", R, cx - 2.2 + i * 1.1, -1.55, 15.9, 0.11, 2.6, BIANCO, vertices=10)
    box(f"Loggia_Trave_{side}", R, cx, -1.5, 17.35, 5.6, 0.35, 0.4, BIANCO2)
    # piccolo timpano laterale con mosaico
    prism(f"Timpano_Laterale_{side}", R, cx, -0.75, 17.6, 5.4, 3.0, 1.2, BIANCO)
    prism(f"Mosaico_Laterale_{side}", R, cx, -1.42, 18.0, 4.2, 2.1, 0.12, ORO)
    cyl(f"Figura_Mosaico_{side}", R, cx - 0.5 * side, -1.50, 18.75, 0.38, 0.08, BLU, vertices=20, rot_x=math.radians(90))
    cyl(f"Figura2_Mosaico_{side}", R, cx + 0.6 * side, -1.50, 18.6, 0.32, 0.08, ROSSO, vertices=20, rot_x=math.radians(90))
    finial(f"Pinnacolino_Loggia_{side}", G, cx, -1.1, 20.6)

# --- Rosone ---
RX, RZ, RR = 0.0, 17.3, 3.55
cyl("Vetro_Rosone", R, RX, -1.28, RZ, RR, 0.18, VETRO, vertices=48, rot_x=math.radians(90))
torus("Anello_Rosone_Esterno", R, RX, -1.45, RZ, RR + 0.15, 0.32, BIANCO2)
torus("Anello_Rosone_Rosa", R, RX, -1.5, RZ, RR - 0.45, 0.16, ROSA)
torus("Anello_Rosone_Centro", R, RX, -1.5, RZ, 0.85, 0.18, BIANCO2)
cyl("Occhio_Rosone", R, RX, -1.48, RZ, 0.7, 0.12, VETRO_C, vertices=24, rot_x=math.radians(90))
for i in range(4):  # crociera del rosone
    box(f"Crociera_Rosone_{i}", R, RX, -1.42, RZ, RR * 2 - 0.2, 0.14, 0.26, BIANCO2, rot_y=i * math.pi / 4)
for i in range(12):  # colonnine radiali e piccoli occhi intorno
    ang = i * math.pi / 6
    x, z = RX + math.cos(ang) * (RR - 1.05), RZ + math.sin(ang) * (RR - 1.05)
    cyl(f"Colonnina_Rosone_{i}", R, x, -1.46, z, 0.13, 0.16, BIANCO, vertices=10, rot_x=math.radians(90))
    torus(f"Occhiello_{i}", R, x + math.cos(ang) * 0.55, -1.46, z + math.sin(ang) * 0.55, 0.26, 0.07, ROSA)
statue("Statua_Rosone_Sotto", ST, RX, -1.55, RZ - RR - 0.85, 1.2)

# Galleria di nicchie con statue sopra il rosone e ai lati
for i in range(9):
    x = -7.2 + i * 1.8
    box(f"Nicchia_{i}", R, x, -1.22, 21.35, 1.15, 0.25, 1.9, SCURO)
    statue(f"Statua_Nicchia_{i}", ST, x, -1.42, 20.55, 1.35)
for side in (-1, 1):  # statue della loggia centrale sotto il rosone
    for i in range(3):
        statue(f"Statua_Galleria_{side}_{i}", ST, side * (4.6 + i * 1.7), -1.5, 12.35, 1.45)

# ----------------------------------------------------------------------------
# 5. Timpano centrale, mosaico dell'Incoronazione e angelo apicale
# ----------------------------------------------------------------------------
prism("Timpano_Centrale", S, 0, 0.0, 22.9, 12.4, 8.4, 2.5, BIANCO)
prism("Mosaico_Centrale", S, 0, -1.32, 23.7, 9.6, 6.2, 0.14, ORO)
prism("Mosaico_Centrale_Interno", S, 0, -1.42, 24.3, 7.2, 4.4, 0.10, ORO_C)
# figure stilizzate del mosaico (Madonna, Cristo, angeli): dischi piatti a filo
cyl("Figura_Cristo", D, 0.5, -1.50, 27.6, 0.48, 0.08, BLU, vertices=20, rot_x=math.radians(90))
cyl("Figura_Madonna", D, -0.9, -1.50, 27.2, 0.42, 0.08, ROSSO, vertices=20, rot_x=math.radians(90))
for i, dx in enumerate((-2.6, -1.8, 1.9, 2.7, -0.2)):
    cyl(f"Angelo_Mosaico_{i}", D, dx, -1.50, 25.6 + abs(dx) * 0.12, 0.26, 0.08, BIANCO2, vertices=16, rot_x=math.radians(90))
# fila di archetti sotto il timpano centrale
for i in range(11):
    box(f"Archetto_Timpano_{i}", D, -6.0 + i * 1.2, -1.3, 22.55, 0.7, 0.2, 0.55, ROSA if i % 2 else BIANCO2)
# angelo sulla cuspide
statue("Angelo_Apicale", ST, 0, -0.6, 31.35, 2.0, ORO_C)
for s in (-1, 1):
    box(f"Ala_Angelo_{s}", ST, s * 0.55, -0.55, 33.05, 0.16, 0.5, 1.15, ORO_C, rot_z=s * 0.6, rot_y=s * 0.35)

# ----------------------------------------------------------------------------
# 6. Guglie e pinnacoli
# ----------------------------------------------------------------------------
def pinnacle(cx, z0, z1, w, tag):
    box(f"{tag}_Fusto", G, cx, -0.4, (z0 + z1) / 2, w, 1.7, z1 - z0, BIANCO)
    box(f"{tag}_Cornice", G, cx, -0.4, z1, w + 0.45, 2.0, 0.4, ROSA_C)
    for sx in (-1, 1):
        for sy in (-1, 1):
            finial(f"{tag}_ang{sx}_{sy}", G, cx + sx * w / 2, -0.4 + sy * 0.7, z1 + 0.15)
    cone(f"{tag}_Cuspide", G, cx, -0.4, z1 + 1.5, w * 0.62, 0.02, 3.0, PIETRA, vertices=8)
    sphere(f"{tag}_Palla", G, cx, -0.4, z1 + 3.15, 0.16, ORO)
    statue(f"{tag}_Statua", ST, cx, -1.35, z0 + 1.2, 1.5)
    # finestrella a lancetta sul fusto
    box(f"{tag}_Lancetta", G, cx, -1.32, (z0 + z1) / 2 + 1.0, 0.55, 0.12, 2.2, SCURO)

pinnacle(-6.9, 12.2, 26.5, 1.7, "Guglia_Centrale_Sx")
pinnacle(6.9, 12.2, 26.5, 1.7, "Guglia_Centrale_Dx")
pinnacle(-13.6, 17.6, 24.5, 1.9, "Guglia_Esterna_Sx")
pinnacle(13.6, 17.6, 24.5, 1.9, "Guglia_Esterna_Dx")

# doccioni / gargolle sporgenti ai lati (visibili in foto)
for side in (-1, 1):
    for z, tag in [(9.2, "basso"), (14.8, "alto")]:
        cone(f"Gargolla_{side}_{tag}", D, side * 15.6, -1.6, z, 0.16, 0.34, 1.5,
             PIETRA, vertices=8, rot_x=math.radians(100))
        sphere(f"Testa_Gargolla_{side}_{tag}", D, side * 15.6, -2.25, z - 0.35, 0.2, PIETRA)

# finestre a lancetta sulle torri laterali
for side in (-1, 1):
    for z in (10.6, 15.3, 19.8):
        box(f"Lancetta_Torre_{side}_{z}", D, 13.6 * side, -1.5, z, 0.65, 0.12, 2.0, SCURO)
        prism(f"Lancetta_Cima_{side}_{z}", D, 13.6 * side, -1.52, z + 1.0, 0.65, 0.7, 0.1, SCURO)
        cyl(f"Lancetta_Col_{side}_{z}", D, 13.6 * side, -1.58, z, 0.07, 2.0, BIANCO, vertices=8)

# statue lungo i bordi dei timpani laterali e sulle torri
for side in (-1, 1):
    for i, (dx, z) in enumerate([(2.3, 18.3), (1.2, 19.6), (-1.2, 19.6), (-2.3, 18.3)]):
        statue(f"Statua_Bordo_{side}_{i}", ST, 11.3 * side + dx, -1.35, z - 0.7, 1.15)
    statue(f"Statua_Torre_{side}", ST, 13.6 * side, -1.55, 22.3, 1.5)

# ----------------------------------------------------------------------------
# 7. Luci, camera, mondo — inquadratura frontale come nella foto
# ----------------------------------------------------------------------------
bpy.ops.object.light_add(type="SUN", location=(18, -30, 38))
sun = bpy.context.object
sun.name = "Sole"
sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(-32))
sun.data.energy = 3.2
sun.data.angle = math.radians(4)

bpy.ops.object.light_add(type="AREA", location=(0, -34, 16))
fill = bpy.context.object
fill.name = "Luce_Frontale"
fill.data.energy = 900
fill.data.shape = "DISK"
fill.data.size = 22
fill.rotation_euler = (math.radians(90), 0, 0)

bpy.ops.object.camera_add(location=(7.5, -52, 15.5))
cam = bpy.context.object
cam.name = "Camera_Frontale"
cam.data.lens = 42
direction = Vector((0, 0, 14.5)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

world = bpy.data.worlds["World"]
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs[0].default_value = (0.62, 0.72, 0.86, 1.0)  # cielo azzurro come in foto
bg.inputs[1].default_value = 0.7

# ----------------------------------------------------------------------------
# 8. Salvataggio .blend + anteprima
# ----------------------------------------------------------------------------
for o in scene.objects:
    o.select_set(False)

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print("Salvato:", BLEND_PATH, "| oggetti:", len(scene.objects))

scene.render.engine = "CYCLES"
scene.cycles.samples = 48
scene.cycles.device = "CPU"
scene.render.resolution_x = 900
scene.render.resolution_y = 1050
scene.render.filepath = PNG_PATH
try:
    bpy.ops.render.render(write_still=True)
    print("Anteprima:", PNG_PATH)
except Exception as e:
    print("Render anteprima non riuscito (il .blend e' comunque valido):", e)
