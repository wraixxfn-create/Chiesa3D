#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MURI ESTERNI DEL CORPO DELLA CHIESA — Duomo di Siena (v4.3)
============================================================

Il progetto nasce come SOLA facciata ovest. Questo modulo aggiunge il resto
dei muri esterni con geometria volutamente SEMPLICE, ma con pianta e altezze
proporzionate alla facciata esistente e alle fotografie allegate. La facciata
non viene mai modificata: gli oggetti creati qui stanno solo nelle raccolte
07*.

Coordinate del modello (come in `genera_facciata.py`):
    X = larghezza, Y = profondita' (facciata verso -Y), Z = altezza.
    Il retro della facciata e' a Y = +1.3 m (non scalato), il corpo si
    sviluppa verso +Y: navata -> transetto/esagono -> coro -> abside.

TARATURA DELLA PIANTA E DELLE ALTEZZE (v4.3)
-------------------------------------------
La facciata v3.9 (larga 30 m e alta 37,5 m) e' il RIFERIMENTO FISSO: tutte
le quote nascono da lei o dalle dimensioni interne ufficiali (Touring /
Wikipedia): 89,4 m di lunghezza, 24,37 m di larghezza alle navate e 54,48 m
alla crociera.  Con muri da 1,5 m il perimetro esterno vale quindi 90,9 m
dal retro della facciata all'abside, 27,37 m alle navate e 57,48 m al
transetto.  La facciata resta piu' larga del corpo navata (30 m contro
27,37 m): nelle fotografie aeree, nel modello di carta e nei rilievi il
fronte aggetta infatti sulle fiancate, quindi il perimetro parte con due
spalline di raccordo sul retro della facciata invece di esserne a filo.
La pianta moderna `riferimento_perimetro.png` fornisce soltanto la FORMA
dei risalti secondari (scalette del transetto, sacrestia, libreria,
posizione di campanile ed esagono), con un'unica scala K_PIANTA; le tre
quote principali sono invece imposte dai valori ufficiali.  Il campanile e'
addossato al fianco destro della navata appena prima del transetto.  Le
altezze distinguono navate laterali, cleristorio, colmi dei tetti, cupola
con lanterna e campanile: cupola 48 m e campanile 77 m, cioe' 1,28 e 2,053
volte la facciata di riferimento.

USO
---
Da solo (apre un .blend gia' generato e aggiunge i muri):

    python aggiorna_muri_esterni.py
    blender --background --python aggiorna_muri_esterni.py

Da `genera_facciata.py` (prima della scala globale):

    from muri_esterni import costruisci_muri_esterni
    costruisci_muri_esterni(scala=1.0, cfg=CFG)   # la scala 3x arriva dopo

La funzione e' idempotente: rimuove le raccolte `07*` prima di ricostruire.
"""

import math

try:
    # Il modulo e' pensato per Blender, ma i DATI PLANIMETRICI (costanti e
    # funzione P) devono essere importabili anche da script 2D senza bpy
    # (es. `crea_pianta_proporzioni.py`, che usa solo Pillow).
    import bpy
    from mathutils import Vector
except ImportError:  # pragma: no cover - solo per gli script di disegno 2D
    bpy = None
    Vector = None


# -----------------------------------------------------------------------------
# 1. TARATURA (metri reali -> unita' modello) e quote ufficiali
# -----------------------------------------------------------------------------
SCALA_DEFAULT = 3.0     # `scala_globale` di config_facciata.json

# Riferimento fisso: la facciata v3.9, NON modificata da questo modulo.
LARGHEZZA_FACCIATA = 30.0
ALTEZZA_FACCIATA = 37.5

# Quote interne ufficiali del Duomo di Siena (Touring / Wikipedia).
LUNGHEZZA_INTERNA = 89.4     # dall'intradosso facciata all'intradosso abside
LARGHEZZA_INTERNA_NAVATA = 24.37
LARGHEZZA_INTERNA_CROCIERA = 54.48

SPESSORE_MURO = 1.5     # spessore dei muri perimetrali (m reali)

# Altezze in metri REALI (vengono moltiplicate per `scala`).
H_PLINTO = 1.9          # = 5,7 u.m. = sommita' di Basamento_Pietra
H_MURO = 15.2           # muri esterni delle navate laterali
H_CLERISTORIO = 21.8    # filo superiore del corpo centrale rialzato
H_COLMO_NAVATA = 24.0   # allineato alla base del timpano centrale (23,95 m)
H_COPING = 0.40
H_FASCIA = 7.6          # unica fascia scura a mezza altezza dei muri bassi
SPESSORE_FASCIA = 0.55
H_TAMBURO_BASE = 23.6
H_TAMBURO = 32.8        # sommita' delle due gallerie del tamburo
H_CALOTTA = 42.0        # imposta della lanterna
H_CUPOLA = 48.0         # croce compresa: 48 / 37,5 = 1,28 volte la facciata
H_CAMPANILE = 68.0      # filo superiore del fusto
H_CAMPANILE_PUNTA = 77.0# 77 / 37,5 = 2,053 volte la facciata
H_ANNESSI = 12.0
H_BATTISTERO = 6.0
H_CAPPELLE = 16.0
H_DUOMO_NUOVO = 15.2    # allineato alla cornice delle navate laterali

LARGHEZZA_CLERISTORIO = 13.2   # setti del cleristorio sopra le arcate maggiori
PASSO_FASCE_CAMPANILE = 2.65
SPESSORE_FASCE_CAMPANILE = 0.32

SPESSORE_ANNESSE = 1.2
SPESSORE_INCOMPIUTO = 1.8
AGGETTO_PL = 0.18       # plinto e cornice sporgono di poco dal filo muro
R_TAMBURO = 11.335      # raggio del tamburo esagonale (22,67 m fra i vertici)
LATO_CAMPANILE = 7.5
TILE_UV = 3.2           # modulo delle texture di marmo della facciata


def M(val_m, scala=SCALA_DEFAULT):
    """Metri reali -> unita' modello."""
    return val_m * scala


# -----------------------------------------------------------------------------
# 2. PIANTA QUOTATA v4.3 (tutte le coordinate sono METRI REALI, assi dei muri)
# -----------------------------------------------------------------------------
# Le tre quote principali derivano dai valori ufficiali + spessore muro;
# Y_BACK_M e' il retro della facciata nel modello esistente.
Y_BACK_M = 1.3
X_NAVATA_SX = -(LARGHEZZA_INTERNA_NAVATA / 2 + SPESSORE_MURO / 2)   # -12,935
X_NAVATA_DX = -X_NAVATA_SX
X_TRANSETTO_SX = -(LARGHEZZA_INTERNA_CROCIERA / 2 + SPESSORE_MURO / 2)  # -27,99
X_TRANSETTO_DX = -X_TRANSETTO_SX
X_SPALLA = LARGHEZZA_FACCIATA / 2 - SPESSORE_MURO / 2   # spalline sul retro
Y_ABSIDE = Y_BACK_M + LUNGHEZZA_INTERNA + SPESSORE_MURO / 2   # asse: 91,45

# Scala UNIFORME della pianta moderna `riferimento_perimetro.png` (595x842 px):
# 763 px (facciata y=820 -> abside y=57) corrispondono ai 90,9 m esterni
# ufficiali; serve solo per i risalti secondari e gli annessi.
K_PIANTA = (SPESSORE_MURO / 2 + LUNGHEZZA_INTERNA) / 763.0
PIANTA_ASSE_X = 327.5   # asse della facciata in pixel della pianta moderna
PIANTA_FACCIATA_Y = 820.0


def dalla_pianta_m(x_px, y_px):
    """Pixel della pianta moderna -> metri reali (assi dei muri)."""
    return ((x_px - PIANTA_ASSE_X) * K_PIANTA,
            Y_BACK_M + (PIANTA_FACCIATA_Y - y_px) * K_PIANTA)


# Quote orizzontali secondarie lette sulla pianta moderna con K_PIANTA.
Y_NAVATA_FINE = dalla_pianta_m(215, 478)[1]      # filo sud del transetto
Y_TRANSETTO_SX_TOP = dalla_pianta_m(101, 263)[1]
Y_TRANSETTO_DX_TOP = dalla_pianta_m(553, 249)[1]
Y_CORO_INIZIO = dalla_pianta_m(211, 195)[1]
Y_CORO_INIZIO_DX = dalla_pianta_m(440, 190)[1]
Y_CORO_FINE = Y_ABSIDE
X_STEP_SX = dalla_pianta_m(164, 263)[0]          # risalti fra transetto e coro
X_STEP_DX = dalla_pianta_m(495, 190)[0]

# Poligono aperto del perimetro esterno (assi dei muri).  Parte dallo spigolo
# ovest sinistro sul retro della facciata, gira in senso antiorario e torna
# allo spigolo ovest destro.  L'ultimo lato (la facciata) NON viene costruito:
# e' gia' il fronte modellato.  Le due spalline iniziali/finali raccordano il
# fronte largo 30 m con le fiancate da 27,37 m, come nelle fotografie.
PERIMETRO = [
    (-X_SPALLA, Y_BACK_M), (X_NAVATA_SX, Y_BACK_M),
    (X_NAVATA_SX, Y_NAVATA_FINE),
    (X_TRANSETTO_SX, Y_NAVATA_FINE), (X_TRANSETTO_SX, Y_TRANSETTO_SX_TOP),
    (X_STEP_SX, Y_TRANSETTO_SX_TOP), (X_STEP_SX, Y_CORO_INIZIO),
    (X_NAVATA_SX, Y_CORO_INIZIO), (X_NAVATA_SX, Y_ABSIDE),
    (X_NAVATA_DX, Y_ABSIDE), (X_NAVATA_DX, Y_CORO_INIZIO_DX),
    (X_STEP_DX, Y_CORO_INIZIO_DX), (X_STEP_DX, Y_TRANSETTO_DX_TOP),
    (X_TRANSETTO_DX, Y_TRANSETTO_DX_TOP), (X_TRANSETTO_DX, Y_NAVATA_FINE),
    (X_NAVATA_DX, Y_NAVATA_FINE), (X_NAVATA_DX, Y_BACK_M),
    (X_SPALLA, Y_BACK_M),
]
TRATTI_MURO = [
    ("Muro_Navata_Sx", "07a_Muri_Nave", PERIMETRO[0:3]),
    ("Muro_Navata_Dx", "07a_Muri_Nave", PERIMETRO[16:18]),
    ("Muro_Transetto_Sx", "07b_Muri_Transetto", PERIMETRO[2:8]),
    ("Muro_Coro_Sx", "07c_Muri_Coro", PERIMETRO[7:9]),
    ("Muro_Abside", "07c_Muri_Coro", PERIMETRO[8:10]),
    ("Muro_Coro_Dx", "07c_Muri_Coro", PERIMETRO[9:12]),
    ("Muro_Transetto_Dx", "07b_Muri_Transetto", PERIMETRO[11:17]),
]
ANNESSI = [
    ("Sacrestia_Obliqua", "07f_Annessi", H_ANNESSI,
     [dalla_pianta_m(x, y) for x, y in
      [(211, 119), (101, 9), (13, 101), (100, 174), (150, 195), (211, 174)]]),
    ("Libreria_Piccolomini", "07f_Annessi", H_ANNESSI,
     [dalla_pianta_m(x, y) for x, y in
      [(215, 485), (57, 490), (57, 562), (215, 562)]]),
    ("Annessi_Libreria", "07f_Annessi", 8.0,
     [dalla_pianta_m(x, y) for x, y in
      [(215, 568), (42, 575), (35, 617), (25, 625), (32, 658), (215, 638)]]),
]
# Campanile addossato al fianco DESTRO della navata, a cavallo del filo del
# transetto: posizione letta sulla pianta moderna, lato 7,5 m come nel rilievo.
CAMPANILE_M = dalla_pianta_m(458, 501)
# Baricentro dei SEI pilastri maggiori della crociera (vertici della pianta
# moderna circa (275,325),(370,325),(415,400),(370,475),(275,475),(230,400)).
ESAGONO_M = dalla_pianta_m(322.5, 400)

# Duomo Nuovo: i muri superstiti del progetto mai completato (quota est
# ~92,5 m dall'asse, come nella pianta Baedeker e in quella Touring).
# Raccolta a parte, disattivabile da config (`includi_duomo_nuovo`).
TRATTI_DUOMO_NUOVO = [
    ("DuomoNuovo_Parete_Nord", [(27.833, 69.633), (92.500, 69.633)]),
    ("DuomoNuovo_Facciatone_Est", [(92.500, 69.633), (92.500, 31.967)]),
    ("DuomoNuovo_Parete_Sud", [(56.167, 31.967), (92.500, 31.967)]),
    ("DuomoNuovo_Attacco_Transetto", [(27.833, 58.967), (27.833, 69.633)]),
]


# -----------------------------------------------------------------------------
# 3. MATERIALI SEMPLICI (riutilizzano i marmi PBR della facciata se presenti)
# -----------------------------------------------------------------------------
NOMI_MAT = {
    "muro": "Marmo_Bianco_Caldo",
    "plinto": "Marmo_Verde_Scuro",
    "cornice": "Marmo_Bianco",
    "tetto": "Muro_Esterno_Tetto_Semplice",
    "piombo": "Muro_Esterno_Piombo_Semplice",
    "incompiuto": "Muro_Esterno_Incompiuto",
}


def _materiale(nome, colore, scala, roughness=0.72, noise=0.0):
    """Restituisce un materiale esistente o ne crea uno piatto/leggermente
    granuloso (nessuna texture esterna, nessuna UV obbligatoria)."""
    m = bpy.data.materials.get(nome)
    if m is not None:
        return m
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (420, 60)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (120, 60)
    bsdf.inputs["Base Color"].default_value = (*colore, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    if noise > 0.0:
        # Il noise usa coordinate OGGETTO: con i vertici in coord. mondo e
        # oggetti a trasformazione identica, la grana resta costante in metri.
        coord = nodes.new("ShaderNodeTexCoord")
        coord.location = (-700, -120)
        scale = nodes.new("ShaderNodeVectorMath")
        scale.operation = "SCALE"
        scale.inputs["Scale"].default_value = 0.34 / max(scala, 1e-6)
        scale.location = (-500, -120)
        ntx = nodes.new("ShaderNodeTexNoise")
        ntx.inputs["Scale"].default_value = 1.0
        ntx.inputs["Detail"].default_value = 3.0
        ntx.location = (-300, -120)
        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.location = (-80, -120)
        k = noise
        ramp.color_ramp.elements[0].color = (
            max(0.0, colore[0] * (1 - k)), max(0.0, colore[1] * (1 - k)),
            max(0.0, colore[2] * (1 - k)), 1.0)
        ramp.color_ramp.elements[1].color = (
            min(1.0, colore[0] * (1 + k)), min(1.0, colore[1] * (1 + k)),
            min(1.0, colore[2] * (1 + k)), 1.0)
        links.new(coord.outputs["Object"], scale.inputs[0])
        links.new(scale.outputs["Vector"], ntx.inputs["Vector"])
        links.new(ntx.outputs["Fac"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return m


def _materiali(scala):
    return {
        "muro": _materiale(NOMI_MAT["muro"], (0.79, 0.75, 0.68), scala,
                           noise=0.10),
        "plinto": _materiale(NOMI_MAT["plinto"], (0.15, 0.18, 0.17), scala,
                             roughness=0.55, noise=0.06),
        "cornice": _materiale(NOMI_MAT["cornice"], (0.86, 0.82, 0.75), scala),
        "tetto": _materiale(NOMI_MAT["tetto"], (0.41, 0.24, 0.18), scala,
                            roughness=0.85, noise=0.08),
        "piombo": _materiale(NOMI_MAT["piombo"], (0.43, 0.49, 0.53), scala,
                             roughness=0.68, noise=0.05),
        "incompiuto": _materiale(NOMI_MAT["incompiuto"], (0.60, 0.57, 0.51),
                                 scala, roughness=0.82, noise=0.10),
    }


# -----------------------------------------------------------------------------
# 4. COSTRUZIONE GEOMETRIA
# -----------------------------------------------------------------------------
def _collezione(nome, parent=None):
    c = bpy.data.collections.get(nome)
    if c is None:
        c = bpy.data.collections.new(nome)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def _uv_box(mesh, scala):
    """UV world-box per le texture dei marmi: proiezione sull'asse dominante
    per le facce verticali, pianta XY per i cieli delle estrusioni."""
    uv = mesh.uv_layers.new(name="UVMap")
    k = 1.0 / (TILE_UV * max(scala, 1e-6))
    for poly in mesh.polygons:
        vs = [mesh.vertices[mesh.loops[li].vertex_index].co
              for li in poly.loop_indices]
        xs = [v.x for v in vs]
        ys = [v.y for v in vs]
        zs = [v.z for v in vs]
        verticale = (max(zs) - min(zs)) > 1e-6 and (
            (max(xs) - min(xs)) > 1e-6 or (max(ys) - min(ys)) > 1e-6)
        asse_x = (max(xs) - min(xs)) >= (max(ys) - min(ys))
        for li in poly.loop_indices:
            v = mesh.vertices[mesh.loops[li].vertex_index].co
            if verticale and asse_x:
                uv.data[li].uv = (v.x * k, v.z * k)
            elif verticale:
                uv.data[li].uv = (v.y * k, v.z * k)
            else:
                uv.data[li].uv = (v.x * k, v.y * k)


def _estrudi_poligono(nome, poligono, z0, z1, materiale, col, scala):
    """Estrude un poligono 2D (coordinate gia' in unita' modello)."""
    n = len(poligono)
    if n < 3 or z1 - z0 < 1e-6:
        return None
    # garantisce verso antiorario (area positiva)
    area = sum(poligono[i][0] * poligono[(i + 1) % n][1] -
               poligono[(i + 1) % n][0] * poligono[i][1] for i in range(n))
    if area < 0:
        poligono = list(reversed(poligono))
    verts = [(p[0], p[1], z0) for p in poligono] + \
            [(p[0], p[1], z1) for p in poligono]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    mesh = bpy.data.meshes.new(nome + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    _uv_box(mesh, scala)
    obj = bpy.data.objects.new(nome, mesh)
    col.objects.link(obj)
    mesh.materials.append(materiale)
    return obj


def _offset_polilinea(punti, spessore):
    """Crea il poligono di una polilinea APERTA con giunti a mitra.
    `punti` sono (x, y) in unita' modello; ritorna il poligono chiuso."""
    pts = [Vector((p[0], p[1])) for p in punti]
    half = spessore / 2.0
    dirs = []
    for i in range(len(pts) - 1):
        d = pts[i + 1] - pts[i]
        d.normalize()
        dirs.append(d)
    normals = [Vector((-d.y, d.x)) for d in dirs]

    def miter(i):
        """Punto sinistro/destro del giunto i (intersezione dei due offset)."""
        a, b = normals[max(0, i - 1)], normals[min(len(normals) - 1, i)]
        n = a + b
        if n.length < 1e-6:
            n = a
        n.normalize()
        coseno = max(0.35, n.dot(a))  # limita le mitre troppo acute
        return n * (half / coseno)

    left = [pts[i] + miter(i) for i in range(len(pts))]
    right = [pts[i] - miter(i) for i in range(len(pts))]
    return [(p.x, p.y) for p in left] + [(p.x, p.y) for p in reversed(right)]


def _muro(nome, punti_m, spessore_m, z0_m, z1_m, materiale, col, scala):
    pts = [(x * scala, y * scala) for x, y in punti_m]
    poly = _offset_polilinea(pts, spessore_m * scala)
    return _estrudi_poligono(nome, poly, z0_m * scala, z1_m * scala,
                             materiale, col, scala)


def _poligono_da_m(punti_m, scala):
    return [(x * scala, y * scala) for x, y in punti_m]


def _poligono_regolare(cx, cy, raggio, lati, scala, rotazione=0.0):
    return [(cx * scala + raggio * scala * math.cos(rotazione + 2 * math.pi * i / lati),
             cy * scala + raggio * scala * math.sin(rotazione + 2 * math.pi * i / lati))
            for i in range(lati)]


def _esagono(cx, cy, raggio, scala, rotazione=0.0):
    return _poligono_regolare(cx, cy, raggio, 6, scala, rotazione)


def _rettangolo(cx, cy, larghezza, profondita, scala):
    hx, hy = larghezza * scala / 2.0, profondita * scala / 2.0
    return [(cx * scala - hx, cy * scala - hy),
            (cx * scala + hx, cy * scala - hy),
            (cx * scala + hx, cy * scala + hy),
            (cx * scala - hx, cy * scala + hy)]


def _mesh(nome, verts, faces, materiale, col, scala):
    mesh = bpy.data.meshes.new(nome + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    _uv_box(mesh, scala)
    obj = bpy.data.objects.new(nome, mesh)
    col.objects.link(obj)
    mesh.materials.append(materiale)
    return obj


def _tetto_capanna(nome, x0, x1, y0, y1, z_gronda, z_colmo,
                   asse, materiale, col, scala):
    """Tetto semplice a due falde; coordinate e quote in metri reali."""
    if asse == "Y":
        xc = (x0 + x1) / 2.0
        pts = [(x0,y0,z_gronda), (x1,y0,z_gronda),
               (x1,y1,z_gronda), (x0,y1,z_gronda),
               (xc,y0,z_colmo), (xc,y1,z_colmo)]
        faces = [(0,4,5,3), (1,2,5,4), (0,1,4), (3,5,2)]
    else:
        yc = (y0 + y1) / 2.0
        pts = [(x0,y0,z_gronda), (x1,y0,z_gronda),
               (x1,y1,z_gronda), (x0,y1,z_gronda),
               (x0,yc,z_colmo), (x1,yc,z_colmo)]
        faces = [(0,1,5,4), (3,4,5,2), (0,4,3), (1,2,5)]
    verts = [(x*scala, y*scala, z*scala) for x,y,z in pts]
    return _mesh(nome, verts, faces, materiale, col, scala)


def _falda_navata_laterale(nome, x_esterno, x_interno, y0, y1,
                           z_esterno, z_interno, materiale, col, scala):
    pts = [(x_esterno,y0,z_esterno), (x_interno,y0,z_interno),
           (x_interno,y1,z_interno), (x_esterno,y1,z_esterno)]
    if x_esterno < x_interno:
        pts.reverse()
    verts = [(x*scala, y*scala, z*scala) for x,y,z in pts]
    return _mesh(nome, verts, [(0,1,2,3)], materiale, col, scala)


def _calotta(nome, cx, cy, raggio, z_base, z_colmo,
             materiale, col, scala, lati=48, anelli=14):
    """Calotta emisferica regolare, non una piramide: la silhouette e' una
    delle proporzioni principali delle fotografie allegate."""
    verts = []
    for j in range(anelli):
        theta = (j / anelli) * math.pi / 2.0
        r = raggio * math.cos(theta)
        z = z_base + (z_colmo - z_base) * math.sin(theta)
        for i in range(lati):
            a = 2 * math.pi * i / lati
            verts.append(((cx + r * math.cos(a)) * scala,
                          (cy + r * math.sin(a)) * scala, z * scala))
    apex = len(verts)
    verts.append((cx * scala, cy * scala, z_colmo * scala))
    faces = []
    for j in range(anelli - 1):
        for i in range(lati):
            ni = (i + 1) % lati
            a, b = j * lati + i, j * lati + ni
            faces.append((a, b, b + lati, a + lati))
    last = (anelli - 1) * lati
    for i in range(lati):
        faces.append((last + i, last + (i + 1) % lati, apex))
    return _mesh(nome, verts, faces, materiale, col, scala)


def _piramide(nome, base, z_base, z_colmo, materiale, col, scala):
    """Piramide (o cono poligonale) su base poligonale, senza la faccia di base."""
    n = len(base)
    verts = [(p[0], p[1], z_base) for p in base] + \
            [(sum(p[0] for p in base) / n, sum(p[1] for p in base) / n, z_colmo)]
    faces = [(i, (i + 1) % n, n) for i in range(n)]
    mesh = bpy.data.meshes.new(nome + "Mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    _uv_box(mesh, scala)
    obj = bpy.data.objects.new(nome, mesh)
    col.objects.link(obj)
    mesh.materials.append(materiale)
    return obj


# -----------------------------------------------------------------------------
# 5. API PRINCIPALE
# -----------------------------------------------------------------------------
def rimuovi_muri_esterni():
    """Rende la funzione idempotente: cancella raccolte/oggetti 07*."""
    for c in list(bpy.data.collections):
        if not c.name.startswith("07"):
            continue
        for o in list(c.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c, do_unlink=True)


def costruisci_muri_esterni(scala=SCALA_DEFAULT, cfg=None,
                            includi_duomo_nuovo=True, tetti=True,
                            rimuovi_esistenti=True):
    """Aggiunge i muri esterni semplici alla scena corrente.

    `scala` = fattore da applicare alle misure in metri reali.
      - 1.0 se chiamata da `genera_facciata.py` PRIMA della scala globale 3x;
      - 3.0 (default) se chiamata su un .blend gia' salvato.
    `cfg` = dizionario `muri_esterni` di config_facciata.json (opzionale).
    """
    if rimuovi_esistenti:
        rimuovi_muri_esterni()

    opt = dict(cfg or {})
    sp = float(opt.get("spessore_muri", SPESSORE_MURO))
    h_muro = float(opt.get("altezza_muri", H_MURO))
    h_cleristorio = float(opt.get("altezza_cleristorio", H_CLERISTORIO))
    h_colmo = float(opt.get("altezza_colmo_navata", H_COLMO_NAVATA))
    h_plinto = float(opt.get("altezza_plinto", H_PLINTO))
    h_tamburo_base = float(opt.get("altezza_tamburo_base", H_TAMBURO_BASE))
    h_tamburo = float(opt.get("altezza_tamburo", H_TAMBURO))
    h_calotta = float(opt.get("altezza_calotta", H_CALOTTA))
    h_cupola = float(opt.get("altezza_cupola", H_CUPOLA))
    h_campanile = float(opt.get("altezza_campanile", H_CAMPANILE))
    h_campanile_punta = float(opt.get("altezza_campanile_punta",
                                      H_CAMPANILE_PUNTA))
    h_incompiuto = float(opt.get("altezza_duomo_nuovo", H_DUOMO_NUOVO))
    includi_duomo_nuovo = bool(opt.get("includi_duomo_nuovo",
                                       includi_duomo_nuovo))
    tetti = bool(opt.get("tetti", tetti))
    mats = _materiali(scala)

    root = _collezione("07_Corpo_Chiesa")
    cols = {k: _collezione(k, root) for k in (
        "07a_Muri_Nave", "07b_Muri_Transetto", "07c_Muri_Coro",
        "07d_Tiburio_e_Cupola", "07e_Campanile", "07f_Annessi",
        "07g_Duomo_Nuovo_Incompiuto", "07h_Tetti_Semplici")}

    conteggio = 0

    # --- 5.1 muri perimetrici: navate basse e transetto rialzato ----------
    for nome, col_key, punti_px in TRATTI_MURO:
        col = cols[col_key]
        # Nelle foto il muro delle navate laterali e' molto piu' basso del
        # corpo centrale. Il transetto, invece, arriva alla gronda alta.
        h_tratto = h_cleristorio if col_key == "07b_Muri_Transetto" else h_muro
        _muro(nome + "_Plinto", punti_px, sp + AGGETTO_PL * 2, 0.0,
              h_plinto, mats["plinto"], col, scala)
        _muro(nome, punti_px, sp, h_plinto, h_tratto,
              mats["muro"], col, scala)
        _muro(nome + "_Fascia", punti_px, sp + AGGETTO_PL,
              H_FASCIA, H_FASCIA + SPESSORE_FASCIA,
              mats["plinto"], col, scala)
        _muro(nome + "_Coronamento", punti_px, sp + AGGETTO_PL * 2,
              h_tratto, h_tratto + H_COPING, mats["cornice"], col, scala)
        conteggio += 4

    # Cleristorio: due setti semplici per navata e coro, raccolti in raccolte
    # proprie ma senza modificare il perimetro ne' la facciata.
    mezzo_cl = LARGHEZZA_CLERISTORIO / 2.0
    for nome, col_key, y0, y1 in (
        ("Navata", "07a_Muri_Nave", Y_BACK_M, Y_NAVATA_FINE),
        ("Coro", "07c_Muri_Coro", Y_CORO_INIZIO, Y_CORO_FINE),
    ):
        for lato, x in (("Sx", -mezzo_cl), ("Dx", mezzo_cl)):
            punti = [(x, y0), (x, y1)]
            _muro(f"Cleristorio_{nome}_{lato}", punti, 1.0,
                  h_muro, h_cleristorio, mats["muro"], cols[col_key], scala)
            _muro(f"Cleristorio_{nome}_{lato}_Cornice", punti, 1.15,
                  h_cleristorio, h_cleristorio + H_COPING,
                  mats["cornice"], cols[col_key], scala)
            conteggio += 2

    # --- 5.2 tamburo, calotta e lanterna (48 m complessivi) ---------------
    cx, cy = ESAGONO_M
    hex_poly = _esagono(cx, cy, R_TAMBURO, scala)
    ct = cols["07d_Tiburio_e_Cupola"]
    h_galleria = h_tamburo_base + (h_tamburo - h_tamburo_base) * 0.52
    _estrudi_poligono("Tamburo_Esagonale", hex_poly,
                      h_tamburo_base * scala, h_galleria * scala,
                      mats["muro"], ct, scala)
    dodec = _poligono_regolare(cx, cy, R_TAMBURO * 0.94, 12, scala,
                               math.pi / 12.0)
    _estrudi_poligono("Tamburo_Dodecagonale", dodec,
                      h_galleria * scala, h_tamburo * scala,
                      mats["muro"], ct, scala)
    for nome, z in (("Tamburo_Cornice_Inferiore", h_galleria),
                    ("Tamburo_Cornice_Superiore", h_tamburo)):
        _estrudi_poligono(nome,
                          _poligono_regolare(cx, cy, R_TAMBURO + AGGETTO_PL,
                                             12, scala, math.pi / 12.0),
                          z * scala, (z + H_COPING) * scala,
                          mats["cornice"], ct, scala)
    _calotta("Cupola_Calotta", cx, cy, R_TAMBURO * 0.90,
             h_tamburo + H_COPING, h_calotta,
             mats["piombo"], ct, scala)

    # Lanterna e croce: semplici, ma incluse nel colmo complessivo di 48 m.
    r_lanterna = max(1.65, R_TAMBURO * 0.17)
    z_cupoletta = h_cupola - 2.25
    z_croce = h_cupola - 0.85
    lanterna = _poligono_regolare(cx, cy, r_lanterna, 12, scala)
    _estrudi_poligono("Lanterna_Tamburo", lanterna,
                      h_calotta * scala, z_cupoletta * scala,
                      mats["muro"], ct, scala)
    _estrudi_poligono("Lanterna_Cornice",
                      _poligono_regolare(cx, cy, r_lanterna + 0.16, 12, scala),
                      z_cupoletta * scala, (z_cupoletta + 0.22) * scala,
                      mats["cornice"], ct, scala)
    _piramide("Lanterna_Cupoletta", lanterna,
              (z_cupoletta + 0.22) * scala, z_croce * scala,
              mats["piombo"], ct, scala)
    _estrudi_poligono("Lanterna_Croce_Stelo",
                      _rettangolo(cx, cy, 0.13, 0.13, scala),
                      z_croce * scala, h_cupola * scala,
                      mats["cornice"], ct, scala)
    _estrudi_poligono("Lanterna_Croce_Braccio",
                      _rettangolo(cx, cy, 0.72, 0.13, scala),
                      (h_cupola - 0.34) * scala, (h_cupola - 0.20) * scala,
                      mats["cornice"], ct, scala)
    conteggio += 11

    # --- 5.3 campanile sul fianco DESTRO, prima del transetto -------------
    cx_c, cy_c = CAMPANILE_M
    r = LATO_CAMPANILE / 2.0
    quad = _rettangolo(cx_c, cy_c, LATO_CAMPANILE, LATO_CAMPANILE, scala)
    cc = cols["07e_Campanile"]
    _estrudi_poligono("Campanile_Plinto", quad, 0.0, h_plinto * scala,
                      mats["plinto"], cc, scala)
    _estrudi_poligono("Campanile_Fusto", quad, h_plinto * scala,
                      h_campanile * scala, mats["muro"], cc, scala)
    _estrudi_poligono("Campanile_Cornice", quad, h_campanile * scala,
                      (h_campanile + H_COPING) * scala,
                      mats["cornice"], cc, scala)
    _piramide("Campanile_Punta_Semplice", quad,
              (h_campanile + H_COPING) * scala,
              h_campanile_punta * scala, mats["muro"], cc, scala)
    conteggio += 4

    # Bicromia ridotta a semplici fasce geometriche: aiuta a leggere la
    # corretta altezza senza introdurre il dettaglio architettonico delle
    # sei monofore/esafore, che resta fuori da questa versione dei muri.
    z_fascia = PASSO_FASCE_CAMPANILE
    while z_fascia + SPESSORE_FASCE_CAMPANILE < h_campanile:
        _estrudi_poligono(
            f"Campanile_Fascia_{z_fascia:05.2f}",
            _rettangolo(cx_c, cy_c, LATO_CAMPANILE + 0.055,
                        LATO_CAMPANILE + 0.055, scala),
            z_fascia * scala,
            (z_fascia + SPESSORE_FASCE_CAMPANILE) * scala,
            mats["plinto"], cc, scala)
        conteggio += 1
        z_fascia += PASSO_FASCE_CAMPANILE

    # Quattro pinnacoli secondari; il colmo centrale resta a 77 m.
    for i, (sx, sy) in enumerate(((-1,-1), (1,-1), (1,1), (-1,1)), 1):
        px = cx_c + sx * (r - 0.38)
        py = cy_c + sy * (r - 0.38)
        base = _rettangolo(px, py, 0.76, 0.76, scala)
        _piramide(f"Campanile_Pinnacolo_{i}", base,
                  (h_campanile + H_COPING) * scala,
                  (h_campanile + 4.25) * scala, mats["cornice"], cc, scala)
        conteggio += 1

    # --- 5.4 annessi e cappelle circolari --------------------------------
    ca = cols["07f_Annessi"]
    for nome, _col_key, altezza, poly_m in ANNESSI:
        # Guscio vuoto: nessun volume pieno che riempia gli interni.
        _muro(nome + "_Plinto", poly_m + [poly_m[0]],
              SPESSORE_ANNESSE, 0, H_PLINTO, mats["plinto"], ca, scala)
        _muro(nome, poly_m + [poly_m[0]], SPESSORE_ANNESSE,
              H_PLINTO, altezza, mats["muro"], ca, scala)
        conteggio += 2
        if tetti:
            _estrusi = _poligono_da_m(poly_m, scala)
            _estrudi_poligono(nome + "_Copertura", _estrusi,
                              altezza * scala, (altezza + 0.24) * scala,
                              mats["tetto"], cols["07h_Tetti_Semplici"], scala)
            conteggio += 1

    # --- 5.5 tetti semplici a falde, su DUE livelli ----------------------
    if tetti:
        cr = cols["07h_Tetti_Semplici"]
        z_gronda_alta = h_cleristorio + H_COPING
        for nome, y0, y1 in (("Navata", Y_BACK_M, Y_NAVATA_FINE),
                             ("Coro", Y_CORO_INIZIO, Y_CORO_FINE)):
            _tetto_capanna(f"Tetto_{nome}_Centrale",
                           -mezzo_cl, mezzo_cl, y0, y1,
                           z_gronda_alta, h_colmo, "Y",
                           mats["piombo"], cr, scala)
            for lato, x_esterno, x_interno in (
                ("Sx", X_NAVATA_SX, -mezzo_cl),
                ("Dx", X_NAVATA_DX, mezzo_cl),
            ):
                _falda_navata_laterale(
                    f"Tetto_{nome}_Laterale_{lato}",
                    x_esterno, x_interno, y0, y1,
                    h_muro + H_COPING, h_muro + 2.0,
                    mats["tetto"], cr, scala)
                conteggio += 1
            conteggio += 1
        _tetto_capanna("Tetto_Transetto", X_TRANSETTO_SX, X_TRANSETTO_DX,
                       Y_NAVATA_FINE, Y_CORO_INIZIO,
                       z_gronda_alta, h_colmo, "X",
                       mats["piombo"], cr, scala)
        conteggio += 1

    # --- 5.6 Duomo Nuovo (incompiuto), raccolta propria ------------------
    if includi_duomo_nuovo:
        cn = cols["07g_Duomo_Nuovo_Incompiuto"]
        for nome, punti_px in TRATTI_DUOMO_NUOVO:
            _muro(nome + "_Plinto", punti_px,
                  SPESSORE_INCOMPIUTO + AGGETTO_PL * 2, 0.0, h_plinto,
                  mats["plinto"], cn, scala)
            _muro(nome, punti_px, SPESSORE_INCOMPIUTO, h_plinto,
                  h_incompiuto, mats["incompiuto"], cn, scala)
            conteggio += 2

    # --- 5.7 riepilogo a console ----------------------------------------
    dims = riepilogo_dimensioni()
    altezze = riepilogo_altezze(opt)
    print("=" * 72)
    print("MURI ESTERNI v4.3 — facciata invariata, perimetro sulle quote ufficiali")
    print("=" * 72)
    for k, v in {**dims, **altezze}.items():
        print(f"  {k:<42s} {v:>10.2f} m reali  = {v * SCALA_DEFAULT:>8.1f} u.m.")
    print(f"  oggetti creati: {conteggio}")
    print("=" * 72)

    return {"oggetti": conteggio, "collezione": root.name,
            "dimensioni_m": dims, "altezze_m": altezze}


def riepilogo_dimensioni():
    """Quote planimetriche in metri reali (NON scalati)."""
    cx_c, cy_c = CAMPANILE_M
    cx_d, cy_d = ESAGONO_M
    return {
        "Larghezza esterna navata": LARGHEZZA_INTERNA_NAVATA + 2 * SPESSORE_MURO,
        "Lunghezza navata (facciata->transetto)": Y_NAVATA_FINE - Y_BACK_M,
        "Larghezza esterna transetto": LARGHEZZA_INTERNA_CROCIERA + 2 * SPESSORE_MURO,
        "Larghezza coro": LARGHEZZA_INTERNA_NAVATA + 2 * SPESSORE_MURO,
        "Lunghezza corpo (retro facciata->abside)":
            (Y_ABSIDE + SPESSORE_MURO / 2) - Y_BACK_M,
        "Aggetto facciata sulle fiancate":
            LARGHEZZA_FACCIATA / 2 - (LARGHEZZA_INTERNA_NAVATA / 2 + SPESSORE_MURO),
        "Distanza facciata->centro cupola": cy_d - Y_BACK_M,
        "Distanza campanile->centro cupola": math.hypot(cx_d-cx_c, cy_d-cy_c),
        "Diametro tamburo esagonale": 2 * R_TAMBURO,
        "Lato campanile": LATO_CAMPANILE,
    }


def riepilogo_altezze(cfg=None):
    """Altezze reali usate dal generatore; facciata di riferimento 37,5 m."""
    opt = dict(cfg or {})
    return {
        "Muri navate laterali": float(opt.get("altezza_muri", H_MURO)),
        "Filo superiore cleristorio": float(opt.get("altezza_cleristorio", H_CLERISTORIO)),
        "Colmo tetti principali": float(opt.get("altezza_colmo_navata", H_COLMO_NAVATA)),
        "Sommita tamburo": float(opt.get("altezza_tamburo", H_TAMBURO)),
        "Imposta lanterna": float(opt.get("altezza_calotta", H_CALOTTA)),
        "Cupola (croce compresa)": float(opt.get("altezza_cupola", H_CUPOLA)),
        "Campanile (fusto)": float(opt.get("altezza_campanile", H_CAMPANILE)),
        "Campanile (punta centrale)": float(opt.get("altezza_campanile_punta", H_CAMPANILE_PUNTA)),
    }
