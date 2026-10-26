#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MURI ESTERNI DEL CORPO DELLA CHIESA — Duomo di Siena (v4.0)
============================================================

Il progetto nasce come SOLA facciata ovest.  Questo modulo aggiunge il resto
dei muri esterni della struttura, volutamente SEMPLICI (prismi e polilinee
estruse, senza decorazioni), ma con PROPORZIONI misurate sulla pianta allegata
`riferimento_pianta.jpg` ("Plan of Siena Cath.", 487 x 431 px).

Coordinate del modello (come in `genera_facciata.py`):
    X = larghezza, Y = profondita' (facciata verso -Y), Z = altezza.
    Il retro della facciata e' a Y = +1.3 m (non scalato), il corpo si
    sviluppa verso +Y: navata -> transetto/esagono -> coro -> abside.

TARATURA DELLA PIANTA
---------------------
La scala grafica in alto a destra da' 10 m = 30 px (e 50 ft = ~46 px):

    PX_PER_M = 3.0        -> 1 px = 0.333 m reali

Siccome il modello usa `scala_globale = 3.0` (1 m reale = 3 unita' modello),
per la scala di default 1 px della pianta = 1 unita' modello: coincide, ma
qui la conversione e' scritta per esteso, cosi' le proporzioni restano esatte
anche cambiando `scala_globale`.

Riferimenti planimetrici (pixel dell'immagine, origine in alto a sinistra):

    X0_PX = 166.5   asse longitudinale = centro della facciata
                     (muri esterni della navata a x = 121 e x = 212)
    Y0_PX = 333     filo interno del muro di facciata; la facciata occupa
                     y = 333..341 (= ~2.7 m, come i 7.08 u.m. del modello)

Punti principali (px -> metri reali, arrotondati):

    facciata (ovest)          y = 333   -> Y =  1.3 m
    navata, larghezza esterna x = 121..212 -> 30.3 m (facciata: 30 m)
    navata, lunghezza         y = 333..210 -> 41.0 m
    transetto, larghezza      x = 76..253  -> 59.0 m
    transetto, profondita'    y = 128..210 -> 27.3 m
    coro, larghezza           x = 121..212 -> 30.3 m
    coro, profondita'         y = 47..128  -> 27.0 m
    testata orientale         y = 47    -> Y = 96.6 m
    lunghezza totale esterna  y = 341..47  -> ~98.0 m (interno reale: 89.4 m)
    centro esagono/cupola     (166, 178) -> Y = 53.0 m
    campanile (ruotato 45°)   ( 84,  62) -> X = -27.5 m, Y = 91.6 m
    Duomo Nuovo (incompiuto)  x = 250..444, y = 128..241

Le misure reali note (89.4 m di lunghezza interna, 54 m al transetto, 24 m
di navata) confermano la taratura: la pianta del libro e' una semplificazione
in cui i muri esterni sono circa il 5-10% piu' generosi degli interni.

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
# 1. TARATURA (pixel -> metri reali -> unita' modello)
# -----------------------------------------------------------------------------
PX_PER_M = 3.0          # 10 m = 30 px sulla scala grafica MTRS
X0_PX = 166.5           # asse della facciata
Y0_PX = 333.0           # retro del muro di facciata
Y_BACK_M = 1.3          # Y (m reali, NON scalati) del retro della facciata

SCALA_DEFAULT = 3.0     # `scala_globale` di config_facciata.json

# Altezze in metri REALI (vengono moltiplicate per `scala`).
# 24.0 m = 72 u.m. = colmo del Corpo_Superiore_Centrale della facciata:
# i muri del corpo si allineano cosi' alle cornici del fronte esistente.
H_PLINTO = 1.9          # = 5.7 u.m. = sommita' di Basamento_Pietra
H_MURO = 24.0           # = 72 u.m. = sommita' del corpo superiore centrale
H_COPING = 0.40         # coronamento semplice sopra il filo dei muri
H_FASCIA = 12.0         # unica fascia scura a mezza altezza (ricordo senese)
SPESSORE_FASCIA = 0.55
H_TAMBURO = 34.0        # sommita' del tamburo esagonale
H_CUPOLA = 40.0         # colmo della semplice cupola piramidale
H_CAMPANILE = 52.0      # torre campanaria semplice (77 m reali / 1.4)
H_CAMPANILE_PUNTA = 57.0
H_ANNESSI = 12.0
H_BATTISTERO = 6.0
H_CAPPELLE = 16.0
H_DUOMO_NUOVO = 12.0    # muri superstiti del Duomo Nuovo, mai completato

SPESSORE_MURO = 1.5     # spessore dei muri perimetrali (m reali)
SPESSORE_ANNESSE = 1.2
SPESSORE_INCOMPIUTO = 1.8
AGGETTO_PL = 0.18       # plinto e cornice sporgono di poco dal filo muro
R_TAMBURO = 14.0        # raggio del tamburo esagonale (28 m fra i vertici)
R_CAPPELLA = 3.6        # cappelle circolari alle teste del transetto
LATO_CAMPANILE = 14.0
TILE_UV = 3.2           # modulo delle texture di marmo della facciata


def P(x_px, y_px, scala=SCALA_DEFAULT):
    """Converte un punto della pianta (px) in (X, Y) del modello."""
    xm = (x_px - X0_PX) / PX_PER_M
    ym = Y_BACK_M + (Y0_PX - y_px) / PX_PER_M
    return (xm * scala, ym * scala)


def M(val_m, scala=SCALA_DEFAULT):
    """Metri reali -> unita' modello."""
    return val_m * scala


# -----------------------------------------------------------------------------
# 2. PIANTA DIGITALIZZATA (tutte le coordinate sono in pixel dell'immagine)
# -----------------------------------------------------------------------------

# Poligono chiuso del perimetro esterno del corpo della chiesa.  Parte dallo
# spigolo ovest sinistro (retro facciata), gira in senso antiorario e torna
# allo spigolo ovest destro.  L'ultimo lato (la facciata) NON viene costruito:
# e' gia' il fronte modellato.
PERIMETRO_PX = [
    (124, 333),   # spigolo ovest sinistro (retro facciata)
    (124, 210),   # muro sinistro della navata
    (76, 210),   # testata ovest del braccio sinistro del transetto
    (76, 128),   # fianco esterno del braccio sinistro
    (121, 128),   # testata nord del braccio sinistro
    (121, 47),    # muro sinistro del coro
    (212, 47),    # testata orientale (abside)
    (212, 128),   # muro destro del coro
    (253, 128),   # testata nord del braccio destro
    (253, 210),   # fianco esterno del braccio destro
    (209, 210),   # testata ovest del braccio destro
    (209, 333),   # muro destro della navata -> spigolo ovest destro
]

# Il perimetro e' spezzato in tratti nominali: ogni tratto diventa un oggetto
# con nome leggibile, cosi' in seguito si puo' dettagliare una zona alla volta.
TRATTI_MURO = [
    ("Muro_Navata_Sx", "07a_Muri_Nave", [(124, 333), (124, 210)]),
    ("Muro_Navata_Dx", "07a_Muri_Nave", [(209, 210), (209, 333)]),
    ("Muro_Transetto_Sx", "07b_Muri_Transetto",
     [(124, 210), (76, 210), (76, 128)]),
    ("Muro_Transetto_Dx", "07b_Muri_Transetto",
     [(253, 128), (253, 210), (209, 210)]),
    ("Muro_TestaTransetto_Sx", "07b_Muri_Transetto", [(76, 128), (121, 128)]),
    ("Muro_TestaTransetto_Dx", "07b_Muri_Transetto", [(212, 128), (253, 128)]),
    ("Muro_Coro_Sx", "07c_Muri_Coro", [(121, 128), (121, 47)]),
    ("Muro_Coro_Dx", "07c_Muri_Coro", [(212, 47), (212, 128)]),
    ("Muro_Abside", "07c_Muri_Coro", [(121, 47), (212, 47)]),
]

# Annessi: poligoni chiusi (px) estrusi come volumi pieni.
ANNESSI = [
    ("Sacrestia_Sx", "07f_Annessi", H_ANNESSI,
     [(68, 208), (124, 208), (124, 238), (68, 238)]),
    ("Sacrestia_Dx", "07f_Annessi", H_ANNESSI,
     [(212, 205), (235, 205), (235, 235), (212, 235)]),
    ("Blocco_Battistero", "07f_Annessi", H_BATTISTERO,
     [(50, 238), (124, 238), (124, 270), (50, 270)]),
]

# Cappelle circolari alle teste del transetto (centro px, raggio m reali).
CAPPELLE_TONDE = [
    ("Cappella_Tonda_Sx", 90, 197),
    ("Cappella_Tonda_Dx", 232, 197),
]

# Torre campanaria: quadrato ruotato di 45° come nella pianta (px del centro).
CAMPANILE_PX = (84, 62)

# Esagono della cupola (centro px).  Orientato con due vertici sull'asse X.
ESAGONO_PX = (166, 178)

# Duomo Nuovo: i muri superstiti del progetto mai completato.  Raccolta a
# parte, disattivabile da config (`includi_duomo_nuovo`).
TRATTI_DUOMO_NUOVO = [
    ("DuomoNuovo_Parete_Nord", [(250, 128), (444, 128)]),
    ("DuomoNuovo_Facciatone_Est", [(444, 128), (444, 241)]),
    ("DuomoNuovo_Parete_Sud", [(335, 241), (444, 241)]),
    ("DuomoNuovo_Attacco_Transetto", [(250, 160), (250, 128)]),
]


# -----------------------------------------------------------------------------
# 3. MATERIALI SEMPLICI (riutilizzano i marmi PBR della facciata se presenti)
# -----------------------------------------------------------------------------
NOMI_MAT = {
    "muro": "Marmo_Bianco_Caldo",
    "plinto": "Marmo_Verde_Scuro",
    "cornice": "Marmo_Bianco",
    "tetto": "Muro_Esterno_Tetto_Semplice",
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


def _muro(nome, punti_px, spessore_m, z0_m, z1_m, materiale, col, scala):
    pts = [P(x, y, scala) for x, y in punti_px]
    poly = _offset_polilinea(pts, spessore_m * scala)
    return _estrudi_poligono(nome, poly, z0_m * scala, z1_m * scala,
                             materiale, col, scala)


def _poligono_da_px(punti_px, scala):
    return [P(x, y, scala) for x, y in punti_px]


def _esagono(cx, cy, raggio, scala, rotazione=0.0):
    out = []
    for i in range(6):
        a = rotazione + i * math.pi / 3.0
        out.append((cx * scala + raggio * scala * math.cos(a),
                    cy * scala + raggio * scala * math.sin(a)))
    return out


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
    h_plinto = float(opt.get("altezza_plinto", H_PLINTO))
    h_tamburo = float(opt.get("altezza_tamburo", H_TAMBURO))
    h_cupola = float(opt.get("altezza_cupola", H_CUPOLA))
    h_campanile = float(opt.get("altezza_campanile", H_CAMPANILE))
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

    # --- 5.1 muri perimetrici: plinto scuro + paramento + coronamento -----
    for nome, col_key, punti_px in TRATTI_MURO:
        col = cols[col_key]
        _muro(nome + "_Plinto", punti_px, sp + AGGETTO_PL * 2, 0.0,
              h_plinto, mats["plinto"], col, scala)
        _muro(nome, punti_px, sp, h_plinto, h_muro,
              mats["muro"], col, scala)
        # Unica fascia orizzontale scura a mezz'altezza: e' l'unica
        # concessione alla bicromia senese, tutto il resto e' liscio.
        _muro(nome + "_Fascia", punti_px, sp + AGGETTO_PL,
              H_FASCIA, H_FASCIA + SPESSORE_FASCIA,
              mats["plinto"], col, scala)
        _muro(nome + "_Coronamento", punti_px, sp + AGGETTO_PL * 2,
              h_muro, h_muro + H_COPING, mats["cornice"], col, scala)
        conteggio += 4

    # --- 5.2 tamburo esagonale + cupola piramidale semplice ---------------
    cx = (ESAGONO_PX[0] - X0_PX) / PX_PER_M
    cy = Y_BACK_M + (Y0_PX - ESAGONO_PX[1]) / PX_PER_M
    hex_poly = _esagono(cx, cy, R_TAMBURO, scala)
    ct = cols["07d_Tiburio_e_Cupola"]
    _estrudi_poligono("Tamburo_Esagonale", hex_poly,
                      h_muro * scala, h_tamburo * scala,
                      mats["muro"], ct, scala)
    _estrudi_poligono("Tamburo_Esagonale_Cornice",
                      _esagono(cx, cy, R_TAMBURO + AGGETTO_PL, scala),
                      h_tamburo * scala, (h_tamburo + H_COPING) * scala,
                      mats["cornice"], ct, scala)
    _piramide("Cupola_Semplice_Esagonale", hex_poly,
              (h_tamburo + H_COPING) * scala, h_cupola * scala,
              mats["tetto"], ct, scala)
    conteggio += 3

    # --- 5.3 campanile semplice (quadrato ruotato come in pianta) ---------
    cx_c = (CAMPANILE_PX[0] - X0_PX) / PX_PER_M
    cy_c = Y_BACK_M + (Y0_PX - CAMPANILE_PX[1]) / PX_PER_M
    # Quadrato ruotato di 45°: i vertici cadono sugli assi, come nella pianta.
    r = LATO_CAMPANILE / 2.0
    quad = [(cx_c * scala + dx * scala, cy_c * scala + dy * scala)
            for dx, dy in ((-r * math.sqrt(2.0), 0.0),
                           (0.0, -r * math.sqrt(2.0)),
                           (r * math.sqrt(2.0), 0.0),
                           (0.0, r * math.sqrt(2.0)))]
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
              H_CAMPANILE_PUNTA * scala, mats["tetto"], cc, scala)
    conteggio += 4

    # --- 5.4 annessi e cappelle circolari --------------------------------
    ca = cols["07f_Annessi"]
    for nome, _col_key, altezza, poly_px in ANNESSI:
        poly = _poligono_da_px(poly_px, scala)
        _estrudi_poligono(nome + "_Plinto", poly, 0.0,
                          min(H_PLINTO, altezza) * scala,
                          mats["plinto"], ca, scala)
        _estrudi_poligono(nome, poly, min(H_PLINTO, altezza) * scala,
                          altezza * scala, mats["muro"], ca, scala)
        conteggio += 2
    for nome, x_px, y_px in CAPPELLE_TONDE:
        cx_k = (x_px - X0_PX) / PX_PER_M
        cy_k = Y_BACK_M + (Y0_PX - y_px) / PX_PER_M
        # dodecagono per una cappella tonda leggibile anche da lontano
        poly = [(cx_k * scala + R_CAPPELLA * scala * math.cos(2 * math.pi * i / 12),
                 cy_k * scala + R_CAPPELLA * scala * math.sin(2 * math.pi * i / 12))
                for i in range(12)]
        _estrudi_poligono(nome, poly, 0.0, H_CAPPELLE * scala,
                          mats["muro"], ca, scala)
        _piramide(nome + "_Cupolino", poly, H_CAPPELLE * scala,
                  (H_CAPPELLE + 2.0) * scala, mats["tetto"], ca, scala)
        conteggio += 2

    # --- 5.5 tetto piano semplice (raccolta separata, disattivabile) -----
    # La croce latina e' decomposta in TRE lastre rettangolari: nessun
    # poligono concavo, nessuna triangolazione visibile in vista dall'alto.
    if tetti:
        z_r0 = (h_muro + H_COPING) * scala
        z_r1 = (h_muro + H_COPING + 0.45) * scala
        for nome, rect in (
            ("Tetto_Navata", [(124, 333), (209, 333), (209, 210), (124, 210)]),
            ("Tetto_Transetto", [(76, 210), (253, 210), (253, 128), (76, 128)]),
            ("Tetto_Coro", [(121, 128), (212, 128), (212, 47), (121, 47)]),
        ):
            _estrudi_poligono(nome, _poligono_da_px(rect, scala),
                              z_r0, z_r1, mats["tetto"],
                              cols["07h_Tetti_Semplici"], scala)
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
    print("=" * 72)
    print("MURI ESTERNI v4.0 — proporzioni dalla pianta (3 px = 1 m reale)")
    print("=" * 72)
    for k, v in dims.items():
        print(f"  {k:<38s} {v:>10.2f} m reali  = {v * SCALA_DEFAULT:>8.1f} u.m.")
    print(f"  oggetti creati: {conteggio}")
    print("=" * 72)

    return {"oggetti": conteggio, "collezione": root.name,
            "dimensioni_m": dims}


def riepilogo_dimensioni():
    """Tabella delle quote principali, in metri reali (NON scalati)."""
    def d(a, b):
        return abs(a - b) / PX_PER_M
    return {
        "Larghezza esterna navata": d(121, 212),
        "Lunghezza navata (facciata->transetto)": d(333, 210),
        "Larghezza esterna transetto": d(76, 253),
        "Profondita' transetto": d(128, 210),
        "Larghezza coro": d(121, 212),
        "Profondita' coro": d(47, 128),
        "Lunghezza totale esterna": d(341, 47),
        "Distanza facciata->centro cupola": d(333, ESAGONO_PX[1]),
        "Diametro tamburo esagonale": 2 * R_TAMBURO,
        "Altezza muri (semplice)": H_MURO,
        "Altezza colmo cupola (semplice)": H_CUPOLA,
        "Altezza campanile (semplice)": H_CAMPANILE,
        "Lato campanile": LATO_CAMPANILE,
    }
