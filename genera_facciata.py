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
  - anteprima_apice.png e anteprima_galleria.png
  - Facciata_Duomo_Siena.glb (se abilitato in config)

Coordinate: X = larghezza (m), Y = profondita' (fronte verso -Y), Z = altezza (m).
Larghezza totale ~30 m, altezza all'angelo ~35 m (proporzioni della facciata reale).
Tutto il modello viene poi riscalato di "scala_globale" (default 3.0) -> ~90 x ~111 m.

RICOSTRUZIONE v2.4 — galleria dei Profeti (sopra lo specchio del rosone,
sotto il triangolo centrale), sviluppata sulla fotografia di dettaglio:

  1. Quindici figure scolpite con torso continuo, spalle larghe, pose
     individuali, maniche curve e mani articolate; il grande profeta
     sporgente ha scala e torsione proprie, la Madonna regge il Bambino.
  2. Volti con mascella, zigomi, naso, orbite, palpebre, labbra, orecchie,
     capelli a ciocche, barbe scanalate e copricapi distinti. Niente piu'
     teste sferiche o busti formati da cilindri giuntati.
  3. Panneggi modellati nella mesh con grandi pieghe a U, manto diagonale
     aderente al corpo e lembi continui oltre il parapetto.
  4. Nicchie piu' luminose e piedritti piu' sottili; frontoni a chevron
     con gigli scolpiti, perlinature fitte e campo grigio-azzurro soltanto
     nel registro alto, come nella fotografia.
  5. Coronamento dell'oculo con perle e dentelli fogliati minuti, pannelli
     rosa nei pennacchi e un solo fregio di grandi cherubini alternati ai
     gigli sotto il mosaico.
  6. Camera dedicata ricalibrata per comprendere fregio, galleria, sommita'
     del rosone e i due profeti dei pennacchi nello stesso dettaglio.

AGGIORNAMENTO v2.5 — la stessa fascia riletta sul dettaglio fotografico:

  1. Via la banda grigio-azzurra sopra i frontoni: il fondo dietro le
     punte e' marmo rosa rigato continuo fino al filetto verde (e chiusa
     la fessura da cui traspariva il cielo sotto la trabeazione).
  2. Frontoni a chevron piu' bassi e fitti (sei gattoni uncinati per
     falda), seconda cornice a chevron in rilievo e ogivetta con giglio,
     rosetta e volute al posto del motivo a "X"; pannellini cosmateschi
     delle V piu' ampi e leggibili.
  3. Profeti piu' stretti nella luce (il rosa respira ai lati) e avanzati
     in altorilievo; lembi dei manti piu' lunghi sul parapetto, fasce
     cosmatesche di parapetto e piedritti piu' ampie.
  4. I due profeti dei pennacchi sono ora mezze figure grandi sdraiate in
     diagonale sui pannelli rosa (testa all'angolo alto esterno, braccio
     teso verso il rosone): nella v2.4 restava visibile solo la testa.
  5. Trabeazione completata: scacchiera cosmatesca a due ordini sotto il
     fregio e fascia a ovoli e dardi fra toro e dentelli; cherubini del
     fregio ingranditi e abbassati sulla soglia, gigli piu' grandi.
  6. Corona dell'oculo: 172 dentelli fogliati e 172 perle (prima 112) e
     nuovo anello interno a losanghe oro/verde sullo sguincio; strisce
     laterali del quadrato ridisegnate come pannelli bianchi a
     quatrifogli con cornice verde (niente piu' sfere).
  7. Camera della galleria ri-inquadrata sul taglio della fotografia di
     riferimento: dentro fregio, galleria, arco e pennacchi completi.

AGGIORNAMENTO v2.6 — IL ROSONE E LE STATUE CHE LO CIRCONDANO, rifatti sulla
nuova fotografia di dettaglio `riferimento_vetrata.jpg`:

  1. Vetrata cattedrale vera: la lastra e' un disco con UV proprie, letta da
     quattro riquadri puliti della fotografia (azzurro-verde lattiginoso,
     nuvolature e bollicine) e composta 2x2 senza specchiature: niente piu'
     ritaglio stirato ne' ripetizione visibile. Fondo opaco dietro il vetro.
  2. Piombatura sottile: due montanti verticali a un terzo del raggio, cinque
     traversi, filo perimetrale; sezione piatta di ferro, non tubi neri.
  3. Ghiera ricostruita come nell'intaglio originale: orlo modanato doppio,
     gola in ombra, perlinatura fitta, due ordini di fogliame d'acanto che
     CORRE lungo l'arco (telaio locale tangente, non foglie a raggiera),
     corda intrecciata oro/avorio e mosaico aureo a tessere sul bordo vetro.
  4. Strombatura troncoconica in ombra fra ghiera e vetro: la profondita'
     nasce dalla geometria, non da un anello disegnato.
  5. Quattro profeti sui pennacchi (prima due): i superiori sdraiati in
     diagonale col braccio teso verso l'oculo, gli inferiori ritti e rivolti
     al centro, tutti su pannelli di marmo rigato con cornice.
  6. Nicchie laterali rifatte (`edicola_v26`): quattro per lato con statue a
     FIGURA INTERA (`statua_gotica_v26`) — corpo a sezioni con pieghe lunghe,
     manto a cordoni, cintola, mani articolate e volto di
     `_bm_testa_profeta24`; via i vani neri delle vecchie nicchiette.
  7. Al centro, davanti al vetro, il Redentore benedicente a figura intera
     (prima una statuina di sfere e coni).
  8. Nuova inquadratura `anteprima_rosone.png` e nuovo riferimento
     `riferimento_vetrata.jpg`; `CHIESA_SOLO_ROSone=1` renderizza solo il
     rosone per le prove rapide.

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
APICE_PATH = os.path.join(OUT_DIR, "riferimento_apice.jpg")
BLEND_PATH = os.path.join(OUT_DIR, "Facciata_Duomo_Siena.blend")
PNG_PATH = os.path.join(OUT_DIR, "anteprima_facciata.png")
APICE_PNG_PATH = os.path.join(OUT_DIR, "anteprima_apice.png")
GALLERIA_PNG_PATH = os.path.join(OUT_DIR, "anteprima_galleria.png")
ROSONE_PNG_PATH = os.path.join(OUT_DIR, "anteprima_rosone.png")
VETRATA_PATH = os.path.join(OUT_DIR, "riferimento_vetrata.jpg")
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
scene["nota"] = "Modello procedurale v2.6: galleria superiore in 15 campate con Madonna col Bambino sull'asse, busti in altorilievo con pose dalla fotografia e profeti sui pennacchi del rosone; retro piatto."


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


def _make_marble_tex(name, base_srgb, vein_srgb, courses=8, seed=1, contrast=0.12, blocks=True):
    """Lastra marmorea senese con venature morbide; opzionalmente senza giunti per statue."""
    sz = 512 if not blocks or courses >= 8 else 256
    n1 = _fbm2d(sz, seed=seed, octaves=5)
    n2 = _fbm2d(sz, seed=seed + 17, octaves=4)
    yy, xx = np.meshgrid(
        np.linspace(0, 1, sz, endpoint=False),
        np.linspace(0, 1, sz, endpoint=False),
        indexing="ij",
    )
    veins = 0.5 + 0.5 * np.sin(2.0 * math.pi * (2.6 * yy + 0.4 * xx + 1.25 * n1 + 0.40 * n2))
    veins = veins ** 2.6
    fine = (n2 - 0.5) * 0.06

    base = np.array(base_srgb, dtype=np.float32)[None, None, :]
    vein = np.array(vein_srgb, dtype=np.float32)[None, None, :]
    col = base * (1.0 - 0.26 * veins[:, :, None]) + vein * (0.26 * veins[:, :, None]) + fine[:, :, None]

    if blocks:
        row_id = np.floor(yy * courses).astype(np.int32)
        stagger = (row_id % 2) * 0.5
        col_id = np.floor((xx * (courses // 2) + stagger) % max(1, courses // 2)).astype(np.int32)
        rng = np.random.default_rng(seed + 99)
        block_lut = rng.uniform(1.0 - contrast * 0.42, 1.0 + contrast * 0.35, (courses + 1, courses + 1))
        block_tone = block_lut[row_id, col_id]
        fy = np.abs((yy * courses) % 1.0 - 0.5)
        fx = np.abs(((xx * max(1, courses // 2) + stagger)) % 1.0 - 0.5)
        mortar = np.where((fy > 0.484) | (fx > 0.488), 0.90, 1.0)
        col = col * block_tone[:, :, None] * mortar[:, :, None]

    return _save_packed_image(name, np.clip(col, 0.0, 1.0))


def _make_verdigris_tex(name, seed=77):
    """Lastra di rame ossidato (verderame senese con screziature turchesi e bronzee)."""
    sz = 512
    n1 = _fbm2d(sz, seed=seed, octaves=5)
    n2 = _fbm2d(sz, seed=seed + 31, octaves=4)
    yy, xx = np.meshgrid(
        np.linspace(0, 1, sz, endpoint=False),
        np.linspace(0, 1, sz, endpoint=False),
        indexing="ij",
    )
    striations = 0.5 + 0.5 * np.sin(2.0 * math.pi * (14.0 * xx + 0.85 * n2))
    patina = np.clip(0.30 + 0.62 * n1 + 0.16 * striations, 0.0, 1.0)
    dark_bronze = np.array((0.20, 0.33, 0.35), dtype=np.float32)[None, None, :]
    bright_verd = np.array((0.46, 0.63, 0.61), dtype=np.float32)[None, None, :]
    col = dark_bronze * (1.0 - patina[:, :, None]) + bright_verd * patina[:, :, None]
    return _save_packed_image(name, np.clip(col, 0.0, 1.0))


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


def _affina_textura(rgb, lo=1.5, hi=99.0, contrasto=1.0, unsharp=0.7,
                    raggio=1, saturazione=1.0, gamma=1.0):
    """Stira i livelli, aumenta il contrasto locale e la saturazione.

    Le fotografie dei mosaici sono velate dalla luce d'ambiente: senza questo
    passaggio la texture resta slavata e "sporca" di grigio, mentre nel
    mosaico originale l'oro è pieno e le figure hanno contorni netti.
    """
    out = np.asarray(rgb, dtype=np.float32)
    # 1) stiramento per canale sui percentili
    for c in range(3):
        ch = out[:, :, c]
        a, b = np.percentile(ch, lo), np.percentile(ch, hi)
        if b - a > 1e-4:
            out[:, :, c] = np.clip((ch - a) / (b - a), 0.0, 1.0)
    # 2) contrasto attorno alla mediana
    if abs(contrasto - 1.0) > 1e-4:
        out = np.clip((out - 0.5) * contrasto + 0.5, 0.0, 1.0)
    # 3) maschera di contrasto (unsharp) su un nucleo 3x3
    if unsharp > 0.0:
        acc = np.zeros_like(out)
        for dy in (-raggio, 0, raggio):
            for dx in (-raggio, 0, raggio):
                acc += np.roll(np.roll(out, dy, axis=0), dx, axis=1)
        acc /= 9.0
        out = np.clip(out * (1.0 + unsharp) - acc * unsharp, 0.0, 1.0)
    # 4) saturazione e gamma
    if abs(saturazione - 1.0) > 1e-4:
        lum = out.mean(axis=2, keepdims=True)
        out = np.clip(lum + (out - lum) * saturazione, 0.0, 1.0)
    if abs(gamma - 1.0) > 1e-4:
        out = np.clip(out, 0.0, 1.0) ** gamma
    return out


def _extract_triangle_tex(name, topdown_rgb, p_bl, p_br, p_top, size=512, boost=1.10,
                          saturazione=1.0):
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
    # Il mosaico dorato, sotto il sole forte del render, tende a sbiancarsi e
    # la fotografia è velata: si riportano livelli, contrasto e saturazione.
    sampled = _affina_textura(sampled, lo=1.0, hi=99.0, contrasto=1.05,
                              unsharp=0.55, raggio=1,
                              saturazione=saturazione, gamma=0.96)
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


def _box_blur_mask(mask, r=2):
    acc = np.zeros_like(mask, dtype=np.float32)
    cnt = 0
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            acc += np.roll(np.roll(mask, dy, axis=0), dx, axis=1)
            cnt += 1
    return acc / float(cnt)


def _extract_mosaic_apice_clean(name, apice_rgb, p_bl, p_br, p_top, size=1536):
    """Estrae il mosaico dell'Incoronazione lungo l'intero triangolo della cornice
    interna, ripristinando il fondo aureo a tessere lungo il margine esterno dove
    nella fotografia compaiono i rilievi lapidei dei cherubini (ricostruiti qui in 3D)."""
    v_lin = np.linspace(0.0, 1.0, size, dtype=np.float32)
    u_lin = np.linspace(0.0, 1.0, size, dtype=np.float32)
    vv, uu = np.meshgrid(v_lin, u_lin, indexing="ij")
    denom = np.maximum(1.0 - vv, 1e-4)
    s = np.clip((uu - 0.5 * vv) / denom, 0.0, 1.0)
    px = (1.0 - vv) * ((1.0 - s) * p_bl[0] + s * p_br[0]) + vv * p_top[0]
    py = (1.0 - vv) * ((1.0 - s) * p_bl[1] + s * p_br[1]) + vv * p_top[1]
    sampled = _bilinear_sample(apice_rgb, px, py)

    w_side = 0.088 + 0.048 * vv
    d_bot = np.clip((vv - 0.058) / 0.042, 0.0, 1.0)
    d_left = np.clip((((1.0 - vv) * s) - w_side * 0.62) / (w_side * 0.42), 0.0, 1.0)
    d_right = np.clip((((1.0 - vv) * (1.0 - s)) - w_side * 0.62) / (w_side * 0.42), 0.0, 1.0)
    d_top = np.clip(((1.0 - vv) - 0.145) / 0.065, 0.0, 1.0)
    core = np.minimum(np.minimum(d_bot, d_top), np.minimum(d_left, d_right))
    edge_mask = 1.0 - core
    edge_mask = edge_mask * edge_mask * (3.0 - 2.0 * edge_mask)

    max_c = sampled.max(axis=2)
    min_c = sampled.min(axis=2)
    sat = (max_c - min_c) / np.maximum(max_c, 1e-3)
    in_outer_rim = (
        (vv < 0.046)
        | (((1.0 - vv) * s) < 0.054)
        | (((1.0 - vv) * (1.0 - s)) < 0.054)
        | (vv > 0.875)
    )
    hue_garment = (
        ((sampled[:, :, 2] > sampled[:, :, 1] * 0.94) & (sat > 0.11))
        | ((sampled[:, :, 1] > sampled[:, :, 0] * 0.94) & (sat > 0.13))
        | ((sampled[:, :, 0] - sampled[:, :, 1] > 0.07) & (sat > 0.24))
    )
    protect = _box_blur_mask(
        np.where((~in_outer_rim) & hue_garment & (vv < 0.56), 1.0, 0.0).astype(np.float32),
        r=3,
    )
    clean_w = edge_mask * (1.0 - np.clip(protect * 1.25, 0.0, 1.0))

    rng = np.random.default_rng(42)
    fine_tess = np.kron(
        rng.normal(0.0, 0.017, (512, 512)).astype(np.float32),
        np.ones((size // 512, size // 512), dtype=np.float32),
    )
    soft_glow = (
        0.026 * np.sin(2.0 * math.pi * (2.3 * uu + 1.7 * vv))
        + 0.018 * np.cos(2.0 * math.pi * (3.9 * uu - 2.6 * vv))
    )
    gold_base = (
        np.array([0.962, 0.910, 0.742], dtype=np.float32)[None, None, :] * (1.0 - 0.30 * vv[:, :, None])
        + np.array([0.952, 0.885, 0.688], dtype=np.float32)[None, None, :] * (0.30 * vv[:, :, None])
    )
    gold_tex = np.clip(
        gold_base + (fine_tess + soft_glow)[:, :, None] * np.array([1.0, 0.94, 0.78], dtype=np.float32),
        0.0,
        1.0,
    )
    merged = sampled * (1.0 - clean_w[:, :, None]) + gold_tex * clean_w[:, :, None]
    merged = _affina_textura(
        merged, lo=0.5, hi=99.4, contrasto=1.08, unsharp=0.50, raggio=1, saturazione=1.22, gamma=1.18
    )
    # Calibrazione fotometrica per Cycles + Sole diretto: la foto contiene già
    # l'illuminazione diurna; attenuando lievemente l'albedo ed esaltando la
    # componente ambra dell'oro musivo, sotto il sole 4.45 non sbianca in giallo pallido
    # ma brilla d'oro bizantino caldo e saturo identico all'originale!
    merged = np.clip(merged * np.array([0.80, 0.75, 0.64], dtype=np.float32)[None, None, :], 0.0, 1.0)
    return _save_packed_image(name, merged)


def _make_striped_marble_tex(name, base_srgb, stripe_srgb, n_strisce=26, seed=91):
    """Lastra di marmo rosa a righe orizzontali chiare (fondo delle nicchie della
    galleria dei Profeti, come nella fotografia del coronamento senese)."""
    sz = 256
    n1 = _fbm2d(sz, seed=seed, octaves=4)
    yy, xx = np.meshgrid(
        np.linspace(0, 1, sz, endpoint=False),
        np.linspace(0, 1, sz, endpoint=False),
        indexing="ij",
    )
    riga = np.floor(yy * n_strisce)
    chiaro = (riga % 2).astype(np.float32)
    # righe chiare sottili rispetto al fondo rosa
    col = (np.array(base_srgb, dtype=np.float32)[None, None, :] * (1.0 - chiaro[:, :, None] * 0.26)
           + np.array(stripe_srgb, dtype=np.float32)[None, None, :] * (chiaro[:, :, None] * 0.26))
    # venatura e giunti verticali sfalsati
    ven = 0.5 + 0.5 * np.sin(2.0 * math.pi * (3.0 * n1 + 0.6 * xx))
    col *= (0.94 + 0.10 * ven)[:, :, None]
    fy = np.abs((yy * n_strisce) % 1.0 - 0.5)
    giunto = np.where(fy > 0.484, 0.93, 1.0)
    stagger = (riga % 2) * 0.5
    fx = np.abs(((xx * 3.0 + stagger)) % 1.0 - 0.5)
    giunto *= np.where(fx > 0.492, 0.95, 1.0)
    col *= giunto[:, :, None]
    return _save_packed_image(name, np.clip(col, 0.0, 1.0))


def _make_cosmatesco_tex(name, seed=93):
    """Fondo cosmatesco senese discretissimo: lastre scure con sottili
    incorniciature chiare, borchie rosse e dorate (fondo dei pinnacoli)."""
    sz = 256
    yy, xx = np.meshgrid(
        np.linspace(0, 1, sz, endpoint=False),
        np.linspace(0, 1, sz, endpoint=False),
        indexing="ij",
    )
    n1 = _fbm2d(sz, seed=seed, octaves=4)
    fondo = np.array((0.685, 0.625, 0.535), dtype=np.float32)
    chiaro = np.array((0.600, 0.555, 0.480), dtype=np.float32)
    rosso = np.array((0.540, 0.290, 0.240), dtype=np.float32)
    oro = np.array((0.180, 0.240, 0.400), dtype=np.float32)
    col = np.ones((sz, sz, 3), dtype=np.float32) * fondo
    # quattro pannelli per lato: cornice chiara sottile attorno al campo scuro
    nx, ny = 2, 2
    ix, iy = (xx * nx) % 1.0, (yy * ny) % 1.0
    bord = np.maximum(np.abs(ix - 0.5), np.abs(iy - 0.5))
    cornice = ((bord >= 0.400) & (bord < 0.452))[:, :, None]
    col = col * (1.0 - cornice) + chiaro[None, None, :] * cornice
    filo = ((bord >= 0.452) & (bord < 0.472))[:, :, None]
    col = col * (1.0 - filo) + rosso[None, None, :] * filo
    # piccola borchia dorata al centro e quattro borchie rosse ai quarti
    r = np.hypot(ix - 0.5, iy - 0.5)
    borchia = (r < 0.060)[:, :, None]
    col = col * (1.0 - borchia) + oro[None, None, :] * borchia
    for cx_b, cy_b in ((0.30, 0.30), (0.70, 0.30), (0.30, 0.70), (0.70, 0.70)):
        rr = np.hypot(ix - cx_b, iy - cy_b)
        bor = ((rr < 0.034))[:, :, None]
        col = col * (1.0 - bor) + rosso[None, None, :] * bor
    col *= (0.94 + 0.10 * n1)[:, :, None]
    return _save_packed_image(name, np.clip(col, 0.0, 1.0))


def _make_vetro_cattedrale_tex(name, seed=131):
    """Vetro cattedrale procedurale: lastra azzurro-verde lattiginosa con
    nuvolature chiare e bolle, come i vetri antichi del rosone senese."""
    size = 512
    base = np.empty((size, size, 3), dtype=np.float32)
    lum = _fbm2d(size, seed=seed, octaves=5)
    medio = _fbm2d(size, seed=seed + 7, octaves=3)
    fine = _fbm2d(size, seed=seed + 21, octaves=2)
    v = 0.52 + 0.30 * lum + 0.10 * medio
    # nuvolette bianche (le lastre sono lattiginose, non trasparenti)
    nuvola = np.clip((lum - 0.56) / 0.30, 0.0, 1.0) ** 1.3
    v = v * (1.0 - 0.55 * nuvola) + 0.92 * nuvola * 0.55
    # pagliuzze e bollicine luminose
    rng = np.random.default_rng(seed)
    punte = rng.random((size, size)).astype(np.float32)
    v = v + np.where(fine > 0.70, 0.16, 0.0) + np.where(punte > 0.9975, 0.42, 0.0)
    v = np.clip(v, 0.0, 1.0)
    base[:, :, 0] = v * 0.78
    base[:, :, 1] = v * 0.93
    base[:, :, 2] = v * 1.00
    base = np.clip(base * np.array([0.94, 1.0, 1.02], dtype=np.float32), 0.0, 1.0)
    return _save_packed_image(name, base)


def _vetro_da_foto(name, topdown_rgb, riquadri, size=1024):
    """Compone la lastra di vetro cattedrale da quattro riquadri DIVERSI letti
    dalla fotografia del rosone, disposti 2x2: nessuna ripetizione a specchio,
    nessuna cucitura. Ogni riquadro e' preso all'interno di un riquadro di
    vetro pulito, lontano dai montanti di piombo.
    """
    img_h, img_w = topdown_rgb.shape[:2]
    half = size // 2
    tile = np.zeros((size, size, 3), dtype=np.float32)
    pesi = np.zeros((size, size, 1), dtype=np.float32)
    for idx, (x0, y0, x1, y1) in enumerate(riquadri):
        if max(x1, y1) <= 1.5:
            x0, y0, x1, y1 = x0 * img_w, y0 * img_h, x1 * img_w, y1 * img_h
        u_lin = np.linspace(x0, x1, half, dtype=np.float32)
        v_lin = np.linspace(y0, y1, half, dtype=np.float32)
        vv, uu = np.meshgrid(v_lin, u_lin, indexing="ij")
        pezzo = _bilinear_sample(topdown_rgb, uu, vv)
        # sfuma i bordi del riquadro verso il vicino (fusione morbida)
        fy = np.linspace(-1.0, 1.0, half, dtype=np.float32)[:, None]
        fx = np.linspace(-1.0, 1.0, half, dtype=np.float32)[None, :]
        w = np.clip(1.6 - 0.9 * (fx ** 2 + fy ** 2), 0.05, 1.0)[:, :, None]
        cx0 = (idx % 2) * half
        cy0 = (idx // 2) * half
        tile[cy0:cy0 + half, cx0:cx0 + half, :] = pezzo
        pesi[cy0:cy0 + half, cx0:cx0 + half, :] = w
    # la lastra deve restare chiara e lattiginosa, ma azzurro-verde:
    # riportata in un intervallo stretto e ritinta come il vetro originale
    tile = _affina_textura(tile, lo=1.0, hi=99.0, contrasto=0.72,
                           unsharp=0.30, raggio=1, saturazione=0.80, gamma=0.95)
    lum = tile.mean(axis=2, keepdims=True)
    lum = 0.52 + (lum - lum.mean()) * 0.62
    tinta = np.array([0.74, 0.94, 1.00], dtype=np.float32)[None, None, :]
    tile = np.clip(lum * tinta * 0.98, 0.0, 1.0)
    return _save_packed_image(name, tile)


def build_all_textures():
    tex = {}
    tex["marmo_bianco"] = _make_marble_tex(
        "Tex_Marmo_Bianco", (0.88, 0.84, 0.77), (0.76, 0.71, 0.63), courses=8, seed=3, contrast=0.09
    )
    tex["marmo_caldo"] = _make_marble_tex(
        "Tex_Marmo_Caldo", (0.83, 0.78, 0.69), (0.70, 0.64, 0.55), courses=8, seed=11, contrast=0.10
    )
    tex["pietra_statue"] = _make_marble_tex(
        "Tex_Pietra_Statue", (0.84, 0.79, 0.71), (0.71, 0.65, 0.56), courses=6, seed=21, contrast=0.06, blocks=False
    )
    tex["gradinata"] = _make_marble_tex(
        "Tex_Gradinata", (0.62, 0.63, 0.67), (0.48, 0.50, 0.54), courses=12, seed=31, contrast=0.14
    )
    tex["marmo_rosa"] = _make_marble_tex(
        "Tex_Marmo_Rosa", (0.64, 0.46, 0.41), (0.48, 0.33, 0.29), courses=6, seed=41, contrast=0.13
    )
    tex["marmo_rosa_chiaro"] = _make_marble_tex(
        "Tex_Marmo_Rosa_Chiaro", (0.76, 0.62, 0.55), (0.61, 0.47, 0.41), courses=6, seed=51, contrast=0.10
    )
    tex["serpentino"] = _make_marble_tex(
        "Tex_Serpentino_Prato", (0.17, 0.19, 0.19), (0.10, 0.13, 0.12), courses=6, seed=61, contrast=0.12
    )
    tex["marmo_rigato"] = _make_striped_marble_tex(
        "Tex_Marmo_Rigato", (0.665, 0.470, 0.420), (0.845, 0.775, 0.700), n_strisce=52, seed=91
    )
    tex["cosmatesco"] = _make_cosmatesco_tex("Tex_Cosmatesco", seed=93)
    tex["rame_verde"] = _make_verdigris_tex("Tex_Rame_Verde", seed=77)

    if os.path.exists(REF_PATH):
        ref_img = bpy.data.images.load(REF_PATH)
        rw, rh = ref_img.size
        buf = np.empty(rw * rh * 4, dtype=np.float32)
        ref_img.pixels.foreach_get(buf)
        bpy.data.images.remove(ref_img)
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
        # v2.6: il vetro ha una texture dedicata (lastra cattedrale), non piu'
        # un ritaglio stirato della foto d'insieme.
        tex["oculo_vetro"] = _make_vetro_cattedrale_tex("Tex_Vetro_Cattedrale")

    if os.path.exists(APICE_PATH):
        apice_img = bpy.data.images.load(APICE_PATH)
        aw, ah = apice_img.size
        abuf = np.empty(aw * ah * 4, dtype=np.float32)
        apice_img.pixels.foreach_get(abuf)
        bpy.data.images.remove(apice_img)
        apice = abuf.reshape((ah, aw, 4))[::-1, :, :3].copy()
        if ah / max(aw, 1) > 1.07:
            ax_s, ay_s = aw / 2176.0, ah / 2472.0
            p_bl = (520.0 * ax_s, 2108.0 * ay_s)
            p_br = (1718.0 * ax_s, 2108.0 * ay_s)
            p_top = (1119.0 * ax_s, 1002.0 * ay_s)
        else:
            ax_s, ay_s = aw / 2067.0, ah / 2092.0
            p_bl = (478.0 * ax_s, 2036.0 * ay_s)
            p_br = (1598.0 * ax_s, 2036.0 * ay_s)
            p_top = (1038.0 * ax_s, 1020.0 * ay_s)
        tex["mosaico_centrale"] = _extract_mosaic_apice_clean(
            "Tex_Mosaico_Incoronazione", apice, p_bl, p_br, p_top, size=1536
        )

    if not os.path.exists(REF_PATH):
        oro = _make_marble_tex("Tex_Mosaico_Fallback", (0.72, 0.58, 0.28), (0.45, 0.28, 0.16), courses=16, seed=7)
        for k in ("mosaico_centrale", "mosaico_sx", "mosaico_dx"):
            tex[k] = oro
        tex["bronzo_porta"] = _make_marble_tex("Tex_Bronzo_Fb", (0.18, 0.19, 0.19), (0.11, 0.12, 0.11), courses=6, seed=8)
        tex["legno_porta"] = _make_marble_tex("Tex_Legno_Fb", (0.30, 0.21, 0.15), (0.20, 0.13, 0.09), courses=6, seed=9)
        tex["oculo_vetro"] = _make_vetro_cattedrale_tex("Tex_Vetro_Cattedrale")
    # v2.6 — la lastra di vetro cattedrale viene letta dalla fotografia del
    # rosone (riferimento_vetrata.jpg): colore azzurro-verde lattiginoso,
    # nuvolature bianche e bollicine, esattamente come l'originale.
    if os.path.exists(VETRATA_PATH):
        try:
            vimg = bpy.data.images.load(VETRATA_PATH)
            vw, vh = vimg.size
            vbuf = np.empty(vw * vh * 4, dtype=np.float32)
            vimg.pixels.foreach_get(vbuf)
            bpy.data.images.remove(vimg)
            vtop = vbuf.reshape((vh, vw, 4))[::-1, :, :3].copy()
            # coordinate nel sistema della foto 1453x1582: una lastra pulita
            # fra due montanti, sotto la fascia superiore del telaio
            kx, ky = vw / 1453.0, vh / 1582.0
            # quattro riquadri di vetro pulito (fra i montanti di piombo)
            tex["oculo_vetro"] = _vetro_da_foto(
                "Tex_Vetro_Cattedrale", vtop,
                ((478 * kx, 600 * ky, 604 * kx, 712 * ky),
                 (640 * kx, 600 * ky, 838 * kx, 712 * ky),
                 (478 * kx, 745 * ky, 604 * kx, 856 * ky),
                 (640 * kx, 745 * ky, 838 * kx, 856 * ky)),
                size=1024,
            )
        except Exception as e:
            print(f"Vetrata di riferimento non leggibile ({e}); uso il vetro procedurale.")
    return tex


TEXTURES = build_all_textures()


# -----------------------------------------------------------------------------
# Materiali PBR da config + texture incorporate + patina di cavità per Cycles
# -----------------------------------------------------------------------------
def mat_from_cfg(name, cfg):
    """Crea materiale Principled BSDF compatibile sia con export GLB che con Cycles
    (con patina d'ombra naturale nelle cavità scolpite tramite Ambient Occlusion)."""
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    nodes = m.node_tree.nodes
    links = m.node_tree.links
    nodes.clear()

    out = nodes.new("ShaderNodeOutputMaterial")
    out.target = "ALL"
    out.location = (520, 120)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (180, 120)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    c = cfg.get("color", [0.4, 0.4, 0.4])[:3]
    bsdf.inputs["Base Color"].default_value = (*c, 1.0)
    bsdf.inputs["Roughness"].default_value = cfg.get("roughness", 0.55)
    bsdf.inputs["Metallic"].default_value = cfg.get("metallic", 0.0)

    tex_key = cfg.get("tex")
    base_color_socket = None
    if tex_key and tex_key in TEXTURES:
        tex_node = nodes.new("ShaderNodeTexImage")
        tex_node.location = (-340, 60)
        tex_node.image = TEXTURES[tex_key]
        links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
        base_color_socket = tex_node.outputs["Color"]
        if cfg.get("emission_strength", 0.0) > 0.0:
            links.new(tex_node.outputs["Color"], bsdf.inputs["Emission Color"])
            bsdf.inputs["Emission Strength"].default_value = cfg["emission_strength"]

    if "emission" in cfg and not tex_key:
        bsdf.inputs["Emission Color"].default_value = (*cfg["emission"], 1.0)
        bsdf.inputs["Emission Strength"].default_value = cfg.get("emission_strength", 0.2)

    ao_strength = cfg.get("ao_strength", 0.0)
    if ao_strength > 0.0:
        out_c = nodes.new("ShaderNodeOutputMaterial")
        out_c.target = "CYCLES"
        out_c.location = (520, -220)
        bsdf_c = nodes.new("ShaderNodeBsdfPrincipled")
        bsdf_c.location = (180, -220)
        bsdf_c.inputs["Roughness"].default_value = cfg.get("roughness", 0.55)
        bsdf_c.inputs["Metallic"].default_value = cfg.get("metallic", 0.0)
        links.new(bsdf_c.outputs["BSDF"], out_c.inputs["Surface"])

        ao = nodes.new("ShaderNodeAmbientOcclusion")
        ao.location = (-420, -220)
        ao.samples = 8
        ao.inputs["Distance"].default_value = 0.32

        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.location = (-200, -220)
        ramp.color_ramp.elements[0].position = 0.08
        ramp.color_ramp.elements[1].position = 0.94

        # Rilevamento geometrico fine delle pieghe, cavità scolpite, riccioli e orbite
        # (indipendente dalla scala 3x e visibile anche in pieno sole diretto!)
        geom = nodes.new("ShaderNodeNewGeometry")
        geom.location = (-420, -430)
        p_ramp = nodes.new("ShaderNodeValToRGB")
        p_ramp.location = (-200, -430)
        p_ramp.color_ramp.elements[0].position = 0.455
        p_ramp.color_ramp.elements[0].color = (1.0, 1.0, 1.0, 1.0)
        p_ramp.color_ramp.elements[1].position = 0.515
        p_ramp.color_ramp.elements[1].color = (0.0, 0.0, 0.0, 1.0)
        links.new(geom.outputs["Pointiness"], p_ramp.inputs["Fac"])

        # Combina AO d'occlusione e concavità fine Pointiness in patina bruno-senese
        cav_mix = nodes.new("ShaderNodeMixRGB")
        cav_mix.blend_type = "MULTIPLY"
        cav_mix.inputs["Fac"].default_value = min(1.0, ao_strength * 0.85)
        cav_mix.location = (-20, -280)

        patina_col = nodes.new("ShaderNodeMixRGB")
        patina_col.blend_type = "MIX"
        patina_col.location = (-20, -460)
        patina_col.inputs["Color1"].default_value = (1.0, 1.0, 1.0, 1.0)
        patina_col.inputs["Color2"].default_value = (0.24, 0.19, 0.145, 1.0)
        links.new(p_ramp.outputs["Color"], patina_col.inputs["Fac"])

        mix_ao = nodes.new("ShaderNodeMixRGB")
        mix_ao.blend_type = "MULTIPLY"
        mix_ao.location = (30, -180)
        mix_ao.inputs["Fac"].default_value = ao_strength
        if base_color_socket is not None:
            links.new(base_color_socket, mix_ao.inputs["Color1"])
            bump = nodes.new("ShaderNodeBump")
            bump.location = (-40, -380)
            bump.inputs["Strength"].default_value = 0.08
            bump.inputs["Distance"].default_value = 0.02
            links.new(base_color_socket, bump.inputs["Height"])
            links.new(bump.outputs["Normal"], bsdf_c.inputs["Normal"])
        else:
            mix_ao.inputs["Color1"].default_value = (*c, 1.0)

        patina_tint = (0.28, 0.23, 0.18, 1.0) if "Verde" not in name else (0.12, 0.20, 0.26, 1.0)
        ramp.color_ramp.elements[0].color = patina_tint
        ramp.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
        links.new(ao.outputs["AO"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], cav_mix.inputs["Color1"])
        links.new(patina_col.outputs["Color"], cav_mix.inputs["Color2"])
        links.new(cav_mix.outputs["Color"], mix_ao.inputs["Color2"])
        links.new(mix_ao.outputs["Color"], bsdf_c.inputs["Base Color"])

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
BRONZO_A = MATS.get("Bronzo_Angelico", BRONZO_D)
LEGNO = MATS.get("Legno_Portali")
LEGNO_S = MATS.get("Legno_Scuro")
VETRO = MATS.get("Vetro_Rosone")
FERRO = MATS.get("Ferro_Griglia")
PIETRA = MATS.get("Pietra_Statue")
PIETRA_RIL = MATS.get("Pietra_Rilievi", PIETRA)
PATINA = MATS.get("Patina_Scolpita", SCURO if "SCURO" in globals() else PIETRA)
SCURO = MATS.get("Vano_Scuro")
PATINA = MATS.get("Patina_Scolpita", SCURO)
PATINA_BR = MATS.get("Patina_Bronzo", SCURO)
NICCHIA = MATS.get("Vano_Nicchia", PIETRA)
VERDE_RAME = MATS.get("Bronzo_Verde", PIETRA)
RIGATO = MATS.get("Marmo_Rigato", ROSA_C)
COSMATE = MATS.get("Cosmatesco_Blu", ROSA_C)
CAMPO = MATS.get("Marmo_Grigio_Azzurro", VERDE)


# -----------------------------------------------------------------------------
# Helper di costruzione rapidi con UV analitici privi di distorsione e triangolati
# -----------------------------------------------------------------------------
def _finish_bmesh(bm, mesh, uv_scale=(1.0, 1.0), planar_uv=False,
                  smooth=True, angolo_spigolo=32.0):
    """Calcola normali esterne, coordinate UV pulite e triangola eventuali n-gon.

    Con `smooth` attivo le facce sono ombreggiate morbide e gli spigoli con
    angolo maggiore di `angolo_spigolo` restano vivi: è ciò che fa leggere
    come scultura le modanature tonde e le foglie, senza ammorbidire gli
    spigoli delle cornici.
    """
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    if smooth:
        soglia = math.radians(angolo_spigolo)
        for f in bm.faces:
            f.smooth = True
        for e in bm.edges:
            if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > soglia:
                e.smooth = False
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


def rosetta_rilievo(name, col, x, y, z, radius, petals=6):
    """Rosetta lapidea a petali lanceolati, poco sporgente nel piano XZ."""
    sphere(name + "_Cuore", col, x, y - 0.025, z, radius * 0.22,
           PIETRA, sy=0.45)
    for k in range(petals):
        a = math.tau * k / petals
        leaf = sphere(f"{name}_Petalo_{k}", col,
                      x + math.sin(a) * radius * 0.52, y,
                      z + math.cos(a) * radius * 0.52,
                      radius, BIANCO2, sx=0.22, sy=0.10, sz=0.52)
        leaf.rotation_euler.y = a


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


PROFILO_FOGLIA = (
    (0.00, 0.24), (0.12, 0.44), (0.24, 0.38), (0.36, 0.52),
    (0.50, 0.40), (0.64, 0.40), (0.76, 0.26), (0.90, 0.13), (1.00, 0.01),
)
PROFILO_PENNA = (
    (0.00, 0.16), (0.14, 0.42), (0.30, 0.48), (0.46, 0.46),
    (0.62, 0.40), (0.78, 0.29), (0.90, 0.16), (1.00, 0.01),
)


def _bm_foglia(bm, lung, larg, spess, mat4, profilo=None, piega=0.0, gonfia=1.0):
    """Aggiunge al bmesh una foglia lanceolata a rilievo (lunghezza +Z locale)."""
    profilo = profilo or PROFILO_FOGLIA
    lf, rf, lb, rb = [], [], [], []
    for t, hw in profilo:
        w = hw * larg
        zz = t * lung
        bulge = spess * gonfia * (0.34 + 0.66 * math.sin(math.pi * min(1.0, t * 1.05)))
        curv = piega * (t ** 2) * lung
        for lst, xx, yy in ((lf, -w, -bulge), (rf, w, -bulge),
                            (lb, -w * 0.90, 0.0), (rb, w * 0.90, 0.0)):
            lst.append(bm.verts.new(mat4 @ Vector((xx + curv, yy, zz))))
    n = len(profilo)
    for i in range(n - 1):
        bm.faces.new((lf[i], rf[i], rf[i + 1], lf[i + 1]))
        bm.faces.new((lb[i + 1], rb[i + 1], rb[i], lb[i]))
        bm.faces.new((lf[i + 1], lf[i], lb[i], lb[i + 1]))
        bm.faces.new((rf[i], rf[i + 1], rb[i + 1], rb[i]))
    bm.faces.new((lf[0], lb[0], rb[0], rf[0]))
    bm.faces.new((rf[-1], rb[-1], lb[-1], lf[-1]))


def _bm_sfera(bm, mat4, x, y, z, r, sx=1.0, sy=1.0, sz=1.0, u=10, v=6):
    m = mat4 @ Matrix.Translation((x, y, z)) @ Matrix.Diagonal((r * sx, r * sy, r * sz, 1.0))
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=1.0, matrix=m)


def _bm_cono(bm, mat4, x, y, z, r1, r2, h, rot=None, seg=8, sy=1.0):
    m = mat4 @ Matrix.Translation((x, y, z))
    if rot is not None:
        m = m @ rot
    m = m @ Matrix.Diagonal((1.0, sy, 1.0, 1.0))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=seg,
                          radius1=r1, radius2=r2, depth=h, matrix=m)


def _bm_lathe(bm, mat4, profile, seg=24, sy=0.76, rib=0.0, rib_n=9, cap=True):
    """Solido di rotazione dentro un bmesh (profilo = sequenza di (z, raggio))."""
    grid = []
    for k, (zz, rr) in enumerate(profile):
        row = []
        for j in range(seg):
            a = 2.0 * math.pi * j / seg
            f = 1.0 + rib * math.cos(rib_n * a + k * 0.45)
            row.append(bm.verts.new(mat4 @ Vector((rr * f * math.cos(a),
                                                   rr * f * math.sin(a) * sy, zz))))
        grid.append(row)
    for k in range(len(profile) - 1):
        for j in range(seg):
            j2 = (j + 1) % seg
            bm.faces.new((grid[k][j], grid[k][j2], grid[k + 1][j2], grid[k + 1][j]))
    if cap:
        bm.faces.new(list(reversed(grid[0])))
        bm.faces.new(grid[-1])


def _bm_segmento(bm, mat4, p0, p1, r0, r1, seg=8, sy=1.0):
    """Tronco di cono orientato da p0 a p1 (braccia, aste, panneggi)."""
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    ln = max(d.length, 1e-4)
    q = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    m = mat4 @ Matrix.Translation((p0 + p1) * 0.5) @ q @ Matrix.Diagonal((1.0, sy, 1.0, 1.0))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=seg,
                          radius1=r0, radius2=r1, depth=ln, matrix=m)


def _mesh_da_bmesh(name, col, bm, material, uv_scale=(0.31, 0.31)):
    mesh = bpy.data.meshes.new(name + "Mesh")
    _finish_bmesh(bm, mesh, uv_scale=uv_scale)
    return _create_mesh_object(name, mesh, col, (0, 0, 0), (0, 0, 0), (1, 1, 1), material)


def _bm_box(bm, mat4, x, y, z, sx, sy, sz, rot=None):
    m = mat4 @ Matrix.Translation((x, y, z))
    if rot is not None:
        m = m @ rot
    m = m @ Matrix.Diagonal((sx, sy, sz, 1.0))
    bmesh.ops.create_cube(bm, size=1.0, matrix=m)


def _bm_arco_acuto(bm, mat4, cx, y, cz, span, rise, minor, seg_u=18, seg_v=7):
    """Arco gotico acuto nel piano XZ dentro un bmesh condiviso."""
    hw = span * 0.5
    grid = []
    for i in range(seg_u + 1):
        t = i / seg_u
        if t <= 0.5:
            u = t * 2.0
            a = math.pi * 0.5 * u
            bx = -hw * math.cos(a)
            bz = rise * math.sin(a)
            nx, nz = -math.cos(a), math.sin(a) * (hw / max(rise, 1e-3))
        else:
            u = (t - 0.5) * 2.0
            a = math.pi * 0.5 * (1.0 - u)
            bx = hw * math.cos(a)
            bz = rise * math.sin(a)
            nx, nz = math.cos(a), math.sin(a) * (hw / max(rise, 1e-3))
        nl = max(math.hypot(nx, nz), 1e-4)
        nx, nz = nx / nl, nz / nl
        row = []
        for j in range(seg_v):
            b = math.tau * j / seg_v
            cb, sb = math.cos(b), math.sin(b)
            row.append(
                bm.verts.new(
                    mat4 @ Vector((cx + bx + minor * cb * nx, y + minor * sb, cz + bz + minor * cb * nz))
                )
            )
        grid.append(row)
    for i in range(seg_u):
        for j in range(seg_v):
            j2 = (j + 1) % seg_v
            bm.faces.new((grid[i][j], grid[i + 1][j], grid[i + 1][j2], grid[i][j2]))


def gargolla(name, col, x, y, z, side, length, radius, material=PIETRA, pitch_deg=0.0):
    """Doccione gotico scolpito (drago/chimera senese proteso nel vuoto)."""
    bm = bmesh.new()
    pitch = math.radians(pitch_deg)
    M = (
        Matrix.Translation((x, y, z))
        @ Matrix.Rotation(-side * pitch, 4, "Y")
    )
    # Mensola modanata d'innesto contro il contrafforte
    _bm_box(bm, M, -side * length * 0.42, 0.0, -radius * 0.35, length * 0.28, radius * 2.1, radius * 1.9)
    # Dorso inarcato muscoloso e collo teso in avanti
    p0 = (-side * length * 0.36, 0.0, -radius * 0.10)
    p1 = (side * length * 0.14, -radius * 0.10, radius * 0.12)
    p2 = (side * length * 0.50, -radius * 0.14, radius * 0.06)
    _bm_segmento(bm, M, p0, p1, radius * 1.05, radius * 0.72, seg=10, sy=0.88)
    _bm_segmento(bm, M, p1, p2, radius * 0.74, radius * 0.56, seg=10, sy=0.86)
    # Zampe anteriori artigliate ripiegate sotto il petto
    for sy_z in (-0.42, 0.42):
        _bm_segmento(
            bm, M,
            (side * length * 0.04, sy_z * radius, -radius * 0.15),
            (side * length * 0.32, sy_z * radius * 0.8, -radius * 0.62),
            radius * 0.34, radius * 0.22, seg=7,
        )
    # Testa allungata con fauci spalancate e orecchie/cresta gotica
    hx = side * length * 0.58
    _bm_sfera(bm, M, hx, -radius * 0.14, radius * 0.14, radius * 0.76, sx=1.35, sy=0.84, sz=0.82, u=12, v=8)
    _bm_segmento(
        bm, M,
        (hx, -radius * 0.14, radius * 0.22),
        (hx + side * radius * 1.55, -radius * 0.15, radius * 0.12),
        radius * 0.46, radius * 0.20, seg=8, sy=0.80,
    )
    _bm_segmento(
        bm, M,
        (hx, -radius * 0.14, -radius * 0.08),
        (hx + side * radius * 1.35, -radius * 0.15, -radius * 0.38),
        radius * 0.34, radius * 0.14, seg=7, sy=0.75,
    )
    # Ali membranose ripiegate lungo i fianchi e orecchie appuntite
    for sy_a in (-0.48, 0.48):
        _bm_foglia(
            bm, radius * 2.9, radius * 1.05, radius * 0.26,
            M @ Matrix.Translation((-side * length * 0.05, sy_a * radius, radius * 0.35))
              @ Matrix.Rotation(-side * math.radians(52), 4, "Y"),
            piega=-0.12,
        )
    return _mesh_da_bmesh(name, col, bm, material)


def finial(name, col, x, y, z, s=1.0):
    bm = bmesh.new()
    M = Matrix.Translation((x, y, z))
    _bm_lathe(
        bm, M,
        ((0.0, 0.095 * s), (0.14 * s, 0.070 * s), (0.38 * s, 0.062 * s),
         (0.48 * s, 0.115 * s), (0.58 * s, 0.065 * s), (0.98 * s, 0.018 * s)),
        seg=10, sy=1.0,
    )
    for k in range(4):
        a = math.pi * 0.5 * k + 0.4
        _bm_foglia(
            bm, 0.24 * s, 0.11 * s, 0.045 * s,
            M @ Matrix.Translation((0.06 * s * math.cos(a), 0.06 * s * math.sin(a), 0.44 * s))
              @ Matrix.Rotation(a, 4, "Z") @ Matrix.Rotation(0.55, 4, "X"),
            piega=0.14,
        )
    return _mesh_da_bmesh(name, col, bm, PIETRA)


def busto_profeta_scolpito(name, col, cx, y, z0, w, body_h, variant=0, material=None):
    """Altorilievo espressivo di Profeta / Patriarca senese (Giovanni Pisano / Camaino):
    pose variate, barbe scolpite, cappucci o mitre, panneggi obliqui e cartigli/codici."""
    material = material or PIETRA
    bm = bmesh.new()
    s = w
    M = Matrix.Translation((cx, y, z0))
    turn = ((variant * 37) % 11 - 5) * 0.065
    tilt_x = ((variant * 19) % 5 - 2) * 0.035

    # Mensoletta e basamento del busto
    _bm_box(bm, M, 0.0, 0.02, body_h * 0.07, w * 0.62, 0.14, body_h * 0.13)

    # Torso panneggiato ad altorilievo con pieghe diagonali scavate
    _bm_lathe(
        bm, M @ Matrix.Translation((0.0, 0.02, body_h * 0.12)),
        ((0.00, w * 0.30), (body_h * 0.16, w * 0.33), (body_h * 0.34, w * 0.34), (body_h * 0.46, w * 0.24)),
        seg=16, sy=0.58, rib=0.06, rib_n=7,
    )
    _bm_sfera(bm, M, 0.0, -0.01, body_h * 0.54, w * 0.22, sx=1.52, sy=0.62, sz=0.62, u=14, v=8)

    # Pieghe del manto obliquo sul petto
    for pf in (-1, 0, 1):
        _bm_segmento(
            bm, M,
            (-w * 0.20 + pf * w * 0.09, -w * 0.12, body_h * 0.52),
            (w * 0.14 + pf * w * 0.07, -w * 0.13, body_h * 0.16),
            w * 0.038, w * 0.030, seg=7, sy=0.7,
        )

    # Braccia piegate e attributo profetico (cartiglio srotolato o libro sacro)
    side_hand = 1 if variant % 2 == 0 else -1
    _bm_segmento(
        bm, M,
        (-side_hand * w * 0.27, -0.01, body_h * 0.52),
        (-side_hand * w * 0.24, -w * 0.13, body_h * 0.30),
        w * 0.068, w * 0.052, seg=8,
    )
    _bm_segmento(
        bm, M,
        (side_hand * w * 0.27, -0.01, body_h * 0.52),
        (side_hand * w * 0.14, -w * 0.16, body_h * 0.36),
        w * 0.068, w * 0.052, seg=8,
    )
    if variant % 3 != 2:
        # Cartiglio profetico in marmo ricurvo
        _bm_segmento(
            bm, M,
            (-w * 0.17, -w * 0.165, body_h * 0.34 + side_hand * 0.03),
            (w * 0.18, -w * 0.175, body_h * 0.25 - side_hand * 0.02),
            w * 0.042, w * 0.038, seg=8, sy=0.38,
        )
    else:
        # Codice / tavola della Legge
        _bm_box(
            bm, M, side_hand * w * 0.06, -w * 0.16, body_h * 0.32,
            w * 0.22, w * 0.06, body_h * 0.20,
            rot=Matrix.Rotation(side_hand * 0.18, 4, "Y"),
        )

    # Testa scolpita con rotazione individuale, barba e copricapo gotico
    Mh = (
        M
        @ Matrix.Translation((turn * w * 0.18, -w * 0.04, body_h * 0.72))
        @ Matrix.Rotation(turn, 4, "Z")
        @ Matrix.Rotation(tilt_x, 4, "X")
    )
    r_h = w * 0.155
    _bm_segmento(bm, Mh, (0.0, 0.01, -r_h * 1.15), (0.0, 0.0, -r_h * 0.35), r_h * 0.52, r_h * 0.46, seg=8)
    _bm_sfera(bm, Mh, 0.0, 0.0, 0.0, r_h, sx=0.84, sy=0.88, sz=1.06, u=14, v=10)
    # Arcata sopracciliare, orbite patinate, naso e zigomi per espressività gotica
    bm_pat = bmesh.new()
    for es in (-1, 1):
        _bm_sfera(bm, Mh, es * r_h * 0.30, -r_h * 0.80, r_h * 0.16, r_h * 0.20, sx=1.1, sy=0.45, sz=0.32, u=8, v=5)
        _bm_sfera(bm_pat, Mh, es * r_h * 0.30, -r_h * 0.85, r_h * 0.02, r_h * 0.14, sx=1.15, sy=0.38, sz=0.55, u=7, v=5)
        _bm_sfera(bm, Mh, es * r_h * 0.36, -r_h * 0.70, -r_h * 0.12, r_h * 0.22, sx=0.8, sy=0.5, sz=0.6, u=8, v=5)
    _bm_segmento(bm, Mh, (0.0, -r_h * 0.82, r_h * 0.18), (0.0, -r_h * 0.98, -r_h * 0.20), r_h * 0.15, r_h * 0.19, seg=6)
    # Solchi d'ombra patinati sotto il cappuccio, nella barba e nelle pieghe del manto
    _bm_sfera(bm_pat, Mh, 0.0, -r_h * 0.86, -r_h * 0.36, r_h * 0.13, sx=1.35, sy=0.35, sz=0.32, u=7, v=5)
    for pf in (-1, 1):
        _bm_segmento(
            bm_pat, M,
            (-w * 0.16 + pf * w * 0.08, -w * 0.128, body_h * 0.49),
            (w * 0.12 + pf * w * 0.06, -w * 0.136, body_h * 0.18),
            w * 0.020, w * 0.016, seg=6,
        )
    _mesh_da_bmesh(f"{name}_ProfetaPatina", col, bm_pat, PATINA)

    # Barba fluente (lunga bipartita, media riccia o corta)
    beard_len = (1.55, 1.05, 0.55, 1.35)[variant % 4]
    if beard_len > 0.7:
        for bs in (-1, 1):
            _bm_segmento(
                bm, Mh,
                (bs * r_h * 0.22, -r_h * 0.66, -r_h * 0.42),
                (bs * r_h * 0.16, -r_h * 0.74, -r_h * (0.55 + beard_len)),
                r_h * 0.30, r_h * 0.13, seg=7, sy=0.62,
            )
    else:
        _bm_sfera(bm, Mh, 0.0, -r_h * 0.62, -r_h * 0.62, r_h * 0.42, sx=0.85, sy=0.62, sz=0.75, u=8, v=6)

    # Copricapo / chioma (cappuccio drappeggiato, berretto profetico, mitra o chioma fluente)
    hat = variant % 4
    if hat == 0:
        _bm_sfera(bm, Mh, 0.0, r_h * 0.04, r_h * 0.28, r_h * 1.06, sx=0.98, sy=0.96, sz=0.92, u=12, v=8)
    elif hat == 1:
        _bm_lathe(
            bm, Mh @ Matrix.Translation((0.0, 0.0, r_h * 0.32)),
            ((0.0, r_h * 0.96), (r_h * 0.45, r_h * 1.04), (r_h * 0.85, r_h * 0.62)),
            seg=12, sy=0.92,
        )
    elif hat == 2:
        for hs in (-1, 1):
            _bm_segmento(
                bm, Mh,
                (hs * r_h * 0.68, 0.0, r_h * 0.35),
                (hs * r_h * 0.82, -r_h * 0.10, -r_h * 0.85),
                r_h * 0.26, r_h * 0.16, seg=7,
            )
        _bm_sfera(bm, Mh, 0.0, r_h * 0.06, r_h * 0.34, r_h * 0.94, sx=0.95, sy=0.95, sz=0.78, u=10, v=7)
    else:
        _bm_cono(bm, Mh, 0.0, 0.0, r_h * 0.92, r_h * 0.88, r_h * 0.14, r_h * 1.15, seg=10, sy=0.85)

    return _mesh_da_bmesh(f"{name}_Profeta", col, bm, material)


_BUST_COUNTER = 0


def edicola_gotica_busto(name, col, cx, y, z0, w, h, con_busto=True):
    """Nicchia gotica senese con fondo scanalato in marmo rosato, colonnine con capitello,
    arco acuto trilobato inscritto, ghimberga modanata con gattoni, fiorone e profeta scolpito."""
    global _BUST_COUNTER
    variant = _BUST_COUNTER
    _BUST_COUNTER += 1

    arch_h = h * 0.36
    body_h = h - arch_h
    # Fondo profondo in ombra nella parte superiore + specchiatura rosata scanalata inferiore
    # (fa risaltare nitidamente in 3D ogni volto, barba e cartiglio dei Profeti!)
    box(f"{name}_Vano", col, cx, y + 0.075, z0 + body_h * 0.34, w * 0.78, 0.12, body_h * 0.66, NICCHIA)
    box(f"{name}_OmbraBusto", col, cx, y + 0.065, z0 + body_h * 0.78, w * 0.76, 0.10, body_h * 0.44, SCURO)
    prism(f"{name}_OmbraArco", col, cx, y + 0.055, z0 + body_h * 0.94, w * 0.76, arch_h * 0.90, 0.10, SCURO)

    # Architettura marmorea dell'edicola (colonnine, capitelli, arco acuto trilobato, ghimberga e gattoni)
    bm = bmesh.new()
    M = Matrix.Identity(4)
    # Soglia inferiore modanata
    _bm_box(bm, M, cx, y - 0.03, z0 + 0.035, w * 0.98, 0.18, 0.07)
    # Colonnine laterali e capitelli fogliati
    for s in (-1, 1):
        kx = cx + s * w * 0.455
        _bm_lathe(
            bm, Matrix.Translation((kx, y - 0.045, z0 + 0.07)),
            ((0.0, w * 0.075), (0.07, w * 0.052), (body_h * 0.80, w * 0.048),
             (body_h * 0.88, w * 0.088), (body_h * 0.95, w * 0.098)),
            seg=10, sy=0.92,
        )
    # Arco gotico acuto + archetti trilobi interni sotto la ghimberga
    _bm_arco_acuto(bm, M, cx, y - 0.055, z0 + body_h * 0.92, w * 0.84, arch_h * 0.72, w * 0.046, seg_u=16, seg_v=7)
    _bm_arco_acuto(bm, M, cx, y - 0.035, z0 + body_h * 0.89, w * 0.72, arch_h * 0.58, w * 0.032, seg_u=14, seg_v=6)
    # Spioventi acuti della ghimberga con taglio pulito e gattoni rampanti
    gh_z0 = z0 + body_h * 0.86
    gh_h = arch_h * 1.18
    gh_hw = w * 0.50
    ang = math.atan2(gh_h, gh_hw)
    sl_len = math.hypot(gh_hw, gh_h) + 0.05
    for s in (-1, 1):
        _bm_box(
            bm, M, cx + s * gh_hw * 0.5, y - 0.075, gh_z0 + gh_h * 0.5,
            sl_len, 0.15, 0.068, rot=Matrix.Rotation(s * ang, 4, "Y"),
        )
        _bm_box(
            bm, M, cx + s * gh_hw * 0.46, y - 0.055, gh_z0 + gh_h * 0.46 - 0.03,
            sl_len * 0.88, 0.12, 0.036, rot=Matrix.Rotation(s * ang, 4, "Y"),
        )
        for kc in range(3):
            tc = 0.24 + 0.56 * kc / 2.0
            gx = cx + s * gh_hw * (1.0 - tc)
            gz = gh_z0 + gh_h * tc
            _bm_foglia(
                bm, 0.13, 0.07, 0.04,
                Matrix.Translation((gx, y - 0.085, gz + 0.03)) @ Matrix.Rotation(s * 0.42, 4, "Y"),
                piega=-0.14 * s,
            )
    # Fiorone apicale trilobato
    fz = gh_z0 + gh_h
    _bm_lathe(
        bm, Matrix.Translation((cx, y - 0.075, fz - 0.01)),
        ((0.0, 0.045), (0.08, 0.062), (0.19, 0.024), (0.25, 0.008)),
        seg=8, sy=0.85,
    )
    for fs in (-1, 1):
        _bm_foglia(
            bm, 0.11, 0.065, 0.035,
            Matrix.Translation((cx, y - 0.08, fz + 0.05)) @ Matrix.Rotation(fs * 0.68, 4, "Y"),
            piega=-0.10 * fs,
        )
    _mesh_da_bmesh(f"{name}_Architettura", col, bm, BIANCO)

    if con_busto:
        busto_profeta_scolpito(name, col, cx, y - 0.025, z0 + 0.06, w, body_h, variant=variant, material=PIETRA)


def profeta_galleria_scolpito(name, col, cx, y, z0, w, h, variant=0):
    """Mezzobusto profetico a tutto tondo, con volto, panneggio e gesto variati."""
    bm = bmesh.new()
    bm_pat = bmesh.new()
    M = Matrix.Translation((cx, y, z0))
    r_h = w * 0.17
    z_head = h * 0.82
    turn = ((variant * 37) % 9 - 4) * 0.045

    # Tunica e manto sovrapposto: silhouette piena, ma contenuta nella campata.
    _bm_lathe(
        bm, M @ Matrix.Translation((0.0, 0.015, h * 0.075)),
        ((0.00, w * 0.27), (h * 0.10, w * 0.32), (h * 0.28, w * 0.31),
         (h * 0.47, w * 0.25), (h * 0.61, w * 0.20)),
        seg=18, sy=0.62, rib=0.055, rib_n=9,
    )
    _bm_sfera(bm, M, 0.0, -w * 0.035, h * 0.57, w * 0.30,
              sx=1.20, sy=0.62, sz=0.34, u=14, v=8)
    _bm_segmento(bm, M, (0.0, -w * 0.045, h * 0.60),
                 (0.0, -w * 0.06, h * 0.72), w * 0.075, w * 0.064, seg=9)

    # Piega del mantello e risvolto incrociato sul petto.
    for k_fold in range(4):
        t = k_fold / 3.0
        _bm_segmento(
            bm, M,
            (-w * (0.28 - 0.06 * t), -w * 0.17, h * (0.57 - 0.07 * t)),
            (w * (0.22 - 0.04 * t), -w * 0.18, h * (0.29 + 0.05 * t)),
            w * 0.026, w * 0.018, seg=6, sy=0.55,
        )
        _bm_segmento(
            bm_pat, M,
            (-w * 0.20 + k_fold * w * 0.035, -w * 0.196, h * 0.43),
            (w * 0.17 + k_fold * w * 0.018, -w * 0.198, h * 0.24),
            w * 0.010, w * 0.008, seg=5,
        )

    # Braccia e mani con sei gesti diversi: rotolo, libro, benedizione e ascolto.
    gesto = variant % 6
    mano_alta = -1 if variant % 2 == 0 else 1
    for arm in (-1, 1):
        shoulder = (arm * w * 0.25, -w * 0.055, h * 0.61)
        if arm == mano_alta and gesto in (0, 2, 3, 5):
            elbow = (arm * w * 0.34, -w * 0.14, h * 0.69)
            wrist = (arm * w * 0.39, -w * 0.18, h * (0.84 if gesto in (2, 5) else 0.77))
        elif gesto == 4:
            elbow = (arm * w * 0.19, -w * 0.14, h * 0.51)
            wrist = (arm * w * 0.06, -w * 0.20, h * 0.45)
        else:
            elbow = (arm * w * 0.30, -w * 0.13, h * 0.48)
            wrist = (arm * w * 0.15, -w * 0.19, h * 0.43)
        _bm_segmento(bm, M, shoulder, elbow, w * 0.092, w * 0.067, seg=8, sy=0.78)
        _bm_segmento(bm, M, elbow, wrist, w * 0.065, w * 0.043, seg=8, sy=0.72)
        _bm_sfera(bm, M, *wrist, w * 0.052, sx=0.90, sy=0.66, sz=0.80, u=9, v=6)
        # Dita raccolte, appena separate, per evitare l'effetto di braccia a tubo.
        for finger in (-1, 0, 1):
            px = wrist[0] + finger * w * 0.025
            _bm_segmento(
                bm, M, (px, wrist[1] - w * 0.025, wrist[2]),
                (px + finger * w * 0.006, wrist[1] - w * 0.029, wrist[2] - h * 0.045),
                w * 0.012, w * 0.008, seg=5,
            )

    if gesto in (0, 3, 5):
        # Libro profetico con costa, dorso e due pagine in rilievo.
        rot_book = Matrix.Rotation(-0.16 if variant % 2 else 0.16, 4, "Y")
        _bm_box(bm, M, -w * 0.045, -w * 0.235, h * 0.43,
                w * 0.27, w * 0.075, h * 0.20, rot=rot_book)
        _bm_box(bm_pat, M, -w * 0.045, -w * 0.278, h * 0.43,
                w * 0.012, w * 0.008, h * 0.16, rot=rot_book)
    elif gesto in (1, 4):
        # Cartiglio srotolato, incurvato fra le mani.
        _bm_segmento(bm, M, (-w * 0.21, -w * 0.22, h * 0.43),
                     (w * 0.20, -w * 0.22, h * 0.39), w * 0.046, w * 0.043, seg=9, sy=0.48)
        for end in (-1, 1):
            _bm_sfera(bm, M, end * w * 0.21, -w * 0.23, h * (0.43 - 0.02 * end),
                      w * 0.052, sx=0.82, sy=0.55, sz=0.82, u=8, v=5)
    else:
        # Piccola tavola della Legge, portata verticalmente sul petto.
        _bm_box(bm, M, w * 0.045, -w * 0.215, h * 0.43,
                w * 0.19, w * 0.055, h * 0.23,
                rot=Matrix.Rotation(0.12 * mano_alta, 4, "Y"))

    # Collo, testa inclinata e tratti del volto rivolti verso la piazza.
    Mh = (
        M @ Matrix.Translation((turn * w * 0.16, -w * 0.015, z_head))
          @ Matrix.Rotation(turn, 4, "Z")
    )
    _bm_sfera(bm, M, 0.0, -w * 0.025, h * 0.69, w * 0.075,
              sx=0.78, sy=0.68, sz=0.95, u=10, v=7)
    _bm_sfera(bm, Mh, 0.0, 0.0, 0.0, r_h, sx=0.82, sy=0.80, sz=1.08, u=16, v=11)
    # Arcate sopracciliari, occhi incassati, zigomi, naso e bocca in ombra.
    for es in (-1, 1):
        _bm_sfera(bm, Mh, es * r_h * 0.30, -r_h * 0.73, r_h * 0.20,
                  r_h * 0.18, sx=1.30, sy=0.42, sz=0.34, u=8, v=5)
        _bm_sfera(bm_pat, Mh, es * r_h * 0.30, -r_h * 0.79, r_h * 0.055,
                  r_h * 0.105, sx=1.20, sy=0.34, sz=0.58, u=7, v=5)
        _bm_sfera(bm, Mh, es * r_h * 0.39, -r_h * 0.66, -r_h * 0.12,
                  r_h * 0.22, sx=0.82, sy=0.55, sz=0.62, u=8, v=5)
    _bm_segmento(bm, Mh, (0.0, -r_h * 0.76, r_h * 0.19),
                 (0.0, -r_h * 0.98, -r_h * 0.17), r_h * 0.14, r_h * 0.17, seg=7)
    _bm_segmento(bm_pat, Mh, (-r_h * 0.15, -r_h * 0.79, -r_h * 0.38),
                 (r_h * 0.15, -r_h * 0.79, -r_h * 0.38), r_h * 0.035, r_h * 0.025, seg=6)

    # Barbe scolpite a ciocche, capigliature / mitrie alternate in modo individuale.
    if variant % 4 in (0, 1, 3):
        beard = (0.92, 0.64, 0.0, 0.78)[variant % 4]
        if beard > 0.0:
            for bs in (-1, 1):
                _bm_segmento(
                    bm, Mh,
                    (bs * r_h * 0.20, -r_h * 0.58, -r_h * 0.32),
                    (bs * r_h * 0.15, -r_h * 0.70, -r_h * (0.55 + beard * 0.46)),
                    r_h * 0.27, r_h * 0.12, seg=7, sy=0.62,
                )
                _bm_segmento(
                    bm_pat, Mh,
                    (bs * r_h * 0.20, -r_h * 0.79, -r_h * 0.54),
                    (bs * r_h * 0.15, -r_h * 0.80, -r_h * (0.82 + beard * 0.22)),
                    r_h * 0.020, r_h * 0.012, seg=5,
                )
    copricapo = variant % 4
    if copricapo == 0:
        _bm_sfera(bm, Mh, 0.0, r_h * 0.05, r_h * 0.30, r_h * 0.84,
                  sx=1.08, sy=0.95, sz=0.66, u=12, v=8)
        for ciocca in (-1, 0, 1):
            _bm_sfera(bm, Mh, ciocca * r_h * 0.46, -r_h * 0.10, r_h * 0.20,
                      r_h * 0.27, sx=0.84, sy=0.65, sz=0.70, u=8, v=6)
    elif copricapo == 1:
        _bm_cono(bm, Mh, 0.0, r_h * 0.02, r_h * 0.72,
                 r_h * 0.78, r_h * 0.12, r_h * 1.15, seg=10, sy=0.82)
        _bm_box(bm, Mh, 0.0, -r_h * 0.74, r_h * 0.34,
                r_h * 1.12, r_h * 0.12, r_h * 0.11)
    elif copricapo == 2:
        _bm_lathe(
            bm, Mh @ Matrix.Translation((0.0, 0.0, r_h * 0.30)),
            ((0.0, r_h * 0.92), (r_h * 0.24, r_h * 1.02), (r_h * 0.48, r_h * 0.72)),
            seg=14, sy=0.86, rib=0.045, rib_n=8,
        )
    else:
        _bm_sfera(bm, Mh, 0.0, r_h * 0.10, r_h * 0.24, r_h * 0.88,
                  sx=1.03, sy=0.95, sz=0.74, u=12, v=8)
        for hs in (-1, 1):
            _bm_segmento(bm, Mh, (hs * r_h * 0.72, 0.0, r_h * 0.20),
                         (hs * r_h * 0.88, -r_h * 0.08, -r_h * 0.50),
                         r_h * 0.20, r_h * 0.13, seg=7, sy=0.72)

    _mesh_da_bmesh(f"{name}_Scultura", col, bm, PIETRA_RIL)
    _mesh_da_bmesh(f"{name}_Patina", col, bm_pat, PATINA)


# -----------------------------------------------------------------------------
# GALLERIA SUPERIORE DEI PROFETI — ricostruzione v2.4
# -----------------------------------------------------------------------------
# Fascia sopra lo specchio del rosone e sotto il triangolo centrale, rifatta
# sulla fotografia `riferimento_galleria.jpg`: 15 campate a tutto sesto poco
# profonde con Madonna col Bambino sull'asse, busti grandi in altorilievo con
# pose individuali (`_POSE_PROFETI`), frontoni triangolari pieni a chevron,
# pinnacolini nella V fra i frontoni, parapetto e specchiature cosmatesche.
# -----------------------------------------------------------------------------


def _bm_lastra(bm, mat4, punti, spess, y0=0.0):
    """Estrude una polilinea chiusa del piano XZ in una lastra piana di
    spessore `spess` lungo +Y (fronte verso -Y)."""
    fronte = [bm.verts.new(mat4 @ Vector((x, y0, z))) for x, z in punti]
    dietro = [bm.verts.new(mat4 @ Vector((x, y0 + spess, z))) for x, z in punti]
    bm.faces.new(fronte)
    bm.faces.new(list(reversed(dietro)))
    n = len(punti)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((fronte[i], fronte[j], dietro[j], dietro[i]))


def _bm_trave(bm, mat4, p0, p1, y, profondita, spessore, extra=0.0):
    """Trave/cornice retta fra due punti del piano XZ (usata per spioventi)."""
    dx, dz = p1[0] - p0[0], p1[1] - p0[1]
    lung = math.hypot(dx, dz) + extra
    ang = math.atan2(dz, dx)
    mx, mz = (p0[0] + p1[0]) * 0.5, (p0[1] + p1[1]) * 0.5
    _bm_box(bm, mat4, mx, y, mz, lung, profondita, spessore,
            rot=Matrix.Rotation(-ang, 4, "Y"))


def _bm_ghimberga(bm, mat4, cx, hw, z_base, z_top, y, spess, profondita,
                  crockets=None, n_croc=4, croc_size=0.03):
    """Ghimberga gotica piena: due spioventi modanati che si incontrano in punta.

    `spess` è lo spessore della modanatura misurato perpendicolarmente allo
    spiovente, `profondita` l'aggetto verso l'osservatore.
    """
    ang = math.atan2(z_top - z_base, hw)
    for s in (-1, 1):
        _bm_trave(bm, mat4, (cx + s * hw, z_base), (cx, z_top), y,
                  profondita, spess, extra=spess * 0.5)
        # gola interna arretrata: legge come modanatura, non come stecca
        _bm_trave(bm, mat4,
                  (cx + s * hw * 0.960, z_base + (z_top - z_base) * 0.020),
                  (cx, z_top - spess * 0.60), y + profondita * 0.58,
                  profondita * 0.42, spess * 0.52)
        if crockets is not None and n_croc > 0:
            for k in range(n_croc):
                t = 0.22 + 0.62 * k / max(1, n_croc - 1)
                gx = cx + s * hw * (1.0 - t)
                gz = z_base + (z_top - z_base) * t
                Mg = (mat4 @ Matrix.Translation((gx, y - spess * 0.30, gz))
                      @ Matrix.Rotation(-s * ang * 0.92, 4, "Y"))
                _bm_foglia(crockets, croc_size * (1.12 - 0.32 * t),
                           croc_size * 0.46, croc_size * 0.30, Mg,
                           piega=-0.10 * s, gonfia=1.22)


def _bm_rosetta(bm, mat4, x, y, z, r, petali=8, spess=0.6, guscio=None):
    """Rosetta a bassorilievo: bottone centrale e petali embricati."""
    _bm_sfera(bm, mat4, x, y - r * 0.30, z, r * 0.42, sx=1.0, sy=spess, sz=1.0, u=10, v=6)
    for k in range(petali):
        a = math.tau * k / petali
        M = (mat4 @ Matrix.Translation((x + r * 0.52 * math.cos(a), y, z + r * 0.52 * math.sin(a)))
             @ Matrix.Rotation(a + math.pi * 0.5, 4, "Y"))
        _bm_foglia(bm, r * 0.62, r * 0.30, r * 0.16,
                   M, profilo=((0.00, 0.30), (0.35, 0.50), (0.70, 0.42), (1.00, 0.04)),
                   piega=0.10, gonfia=1.10)


def _bm_pinnacolo(bm_w, bm_r, mat4, x, y, z0, alt, larg, ghiere=True):
    """Pinnacolo gotico snello: zoccolo, fusto sfaccettato, ghimberghe e fiorone."""
    # Zoccolo e base modanata
    _bm_box(bm_w, mat4, x, y + 0.01, z0 + 0.020, larg * 1.62, 0.085, 0.040)
    _bm_box(bm_w, mat4, x, y, z0 + 0.048, larg * 1.30, 0.078, 0.026)
    # Fusto a fascio sfaccettato che rastrema verso l'alto
    h_fusto = alt * 0.52
    _bm_lathe(bm_w, mat4 @ Matrix.Translation((x, y, z0 + 0.060)),
              ((0.00, larg * 0.60), (h_fusto * 0.30, larg * 0.50),
               (h_fusto * 0.70, larg * 0.41), (h_fusto, larg * 0.34)),
              seg=8, sy=0.92, rib=0.13, rib_n=4)
    # Ghiera in marmo rosa sul fusto
    if ghiere:
        _bm_lathe(bm_r, mat4 @ Matrix.Translation((x, y, z0 + 0.060 + h_fusto * 0.44)),
                  ((0.00, larg * 0.52), (0.016, larg * 0.50)), seg=8, sy=0.94)
    z_cor = z0 + 0.060 + h_fusto
    # Coronamento a ghimberga aperta sui quattro lati
    for k in range(4):
        a = math.tau * k / 4.0 + math.pi * 0.25
        nx, ny = math.cos(a), math.sin(a) * 0.92
        hw = larg * 0.46
        punta = (x + nx * hw * 0.5, z_cor + alt * 0.30)
        _bm_trave(bm_w, mat4, (x + nx * hw, z_cor), punta, y + ny * hw, 0.032, 0.030)
        _bm_trave(bm_w, mat4, (x - nx * hw, z_cor), punta, y + ny * hw, 0.026, 0.020)
        for kk in range(2):
            t = 0.32 + 0.36 * kk
            cx_k = x + nx * hw * (1.0 - t)
            cz_k = z_cor + alt * 0.30 * t
            Mk = (mat4 @ Matrix.Translation((cx_k, y + ny * hw, cz_k))
                  @ Matrix.Rotation(-math.atan2(alt * 0.30, hw) * 0.9, 4, "Y"))
            _bm_foglia(bm_w, alt * 0.10, alt * 0.045, alt * 0.030, Mk, gonfia=1.20)
    # Guglia finale a foglie e bottone
    z_fin = z_cor + alt * 0.30
    _bm_lathe(bm_w, mat4 @ Matrix.Translation((x, y, z_fin - alt * 0.02)),
              ((0.00, larg * 0.30), (0.012, larg * 0.24), (alt * 0.30, larg * 0.10),
               (alt * 0.40, 0.004)), seg=8, sy=0.92)
    _bm_sfera(bm_w, mat4, x, y, z_fin + alt * 0.40, larg * 0.075, u=8, v=5)


# Pose dei 15 profeti della galleria superiore, lette una per una dalla
# fotografia di dettaglio `riferimento_galleria.jpg` (da sinistra a destra).
# La campata centrale (indice 7) e' la Madonna col Bambino sull'asse.
_POSE_PROFETI = [
    # 0 - anziano con berretta, libro chiuso al petto
    dict(yaw=-0.12, nod=0.06, gesto="libro_chiuso", barba=0.45,
         copricapo="berretta", drappo=0.0, scala=1.01),
    # 1 - giovane imberbe, testa alzata di tre quarti, braccia incrociate
    dict(yaw=-0.72, nod=-0.20, gesto="incrociate", barba=0.0,
         copricapo="capelli", drappo=0.0, scala=0.95),
    # 2 - patriarca dalla lunga barba che legge
    dict(yaw=0.10, nod=0.24, gesto="libro", barba=1.15,
         copricapo="capelli", drappo=0.0, scala=1.04),
    # 3 - il grande profeta sporgente (Giovanni Pisano): corpo in diagonale,
    #     un braccio scende oltre il davanzale, l'altro si aggrappa in alto
    dict(yaw=0.55, nod=-0.05, gesto="sporgente", barba=0.70,
         copricapo="capelli_lunghi", drappo=0.45, scala=1.12, roll=0.20,
         pitch=0.08, dx=-0.05),
    # 4 - figura seduta di profilo, libro sulle ginocchia
    dict(yaw=0.95, nod=0.28, gesto="libro_basso", barba=0.35,
         copricapo="cappuccio", drappo=0.35),
    # 5 - profeta che legge un libro, lembo del manto oltre il parapetto
    dict(yaw=-0.28, nod=0.32, gesto="libro", barba=1.00,
         copricapo="capelli_lunghi", drappo=0.55),
    # 6 - mano sul petto e tavola sotto l'altro braccio, manto a campana
    dict(yaw=-0.18, nod=0.10, gesto="petto_tavola", barba=0.65,
         copricapo="turbante", drappo=0.85, scala=1.03),
    # 7 - MADONNA COL BAMBINO (asse della facciata)
    dict(yaw=0.16, nod=0.15, gesto="madonna", barba=0.0,
         copricapo="velo", drappo=0.0, scala=1.04),
    # 8 - profeta inchinato verso la Madonna, grande manto a campana
    dict(yaw=-0.92, nod=0.44, gesto="inchino", barba=0.80,
         copricapo="cappuccio", drappo=0.95, pitch=0.16, scala=1.02),
    # 9 - vecchio di profilo con rotolo la cui punta scende sul parapetto
    dict(yaw=-0.85, nod=0.16, gesto="rotolo", barba=1.10,
         copricapo="capelli_lunghi", drappo=0.40),
    # 10 - profeta assorto nella lettura
    dict(yaw=0.22, nod=0.34, gesto="libro", barba=0.50,
         copricapo="zucchetto", drappo=0.30),
    # 11 - profeta severo, frontale, mano alzata a parlare
    dict(yaw=0.15, nod=0.03, gesto="parlante", barba=0.95,
         copricapo="capelli", drappo=0.45),
    # 12 - tre quarti, libro chiuso e grande manto a campana sul parapetto
    dict(yaw=0.42, nod=0.18, gesto="libro_chiuso", barba=0.60,
         copricapo="berretta", drappo=1.00),
    # 13 - il pensatore: mano alla guancia, gomito appoggiato
    dict(yaw=-0.45, nod=0.32, gesto="pensatore", barba=0.55,
         copricapo="cappuccio", drappo=0.0),
    # 14 - giovane orante a mani giunte, sguardo in alto
    dict(yaw=0.04, nod=-0.15, gesto="preghiera", barba=0.0,
         copricapo="capelli", drappo=0.0),
]


def _bm_sweep24(bm, mat4, punti, raggi, lati=12, ellisse=1.0,
                rughe=0.0, campioni=4):
    """Tubo organico smussato lungo una Catmull-Rom, con sezione variabile.

    A differenza di `_bm_segmento` non produce cilindri giuntati: spalle,
    maniche, dita e ciocche hanno una superficie continua e le piccole
    ondulazioni della sezione leggono come stoffa o ricci scolpiti.
    """
    pts = [Vector(p) for p in punti]
    if len(pts) < 2:
        return
    if isinstance(raggi, (int, float)):
        raggi = [float(raggi)] * len(pts)
    samples = []
    for i in range(len(pts) - 1):
        p0 = pts[max(0, i - 1)]
        p1 = pts[i]
        p2 = pts[i + 1]
        p3 = pts[min(len(pts) - 1, i + 2)]
        for j in range(campioni):
            t = j / float(campioni)
            t2, t3 = t * t, t * t * t
            p = 0.5 * ((2.0 * p1) + (-p0 + p2) * t
                       + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t2
                       + (-p0 + 3.0 * p1 - 3.0 * p2 + p3) * t3)
            r = raggi[i] * (1.0 - t) + raggi[i + 1] * t
            samples.append((p, max(r, 0.0005)))
    samples.append((pts[-1], max(raggi[-1], 0.0005)))
    grid = []
    for i, (p, r) in enumerate(samples):
        tangent = samples[min(i + 1, len(samples) - 1)][0] - samples[max(0, i - 1)][0]
        if tangent.length < 1e-7:
            tangent = Vector((0.0, 0.0, 1.0))
        q = tangent.normalized().to_track_quat("Z", "Y")
        ax = q @ Vector((1.0, 0.0, 0.0))
        ay = q @ Vector((0.0, 1.0, 0.0))
        row = []
        t = i / max(1, len(samples) - 1)
        for j in range(lati):
            a = math.tau * j / lati
            # Pieghe trasversali molto leggere; il profilo non diventa una vite.
            onda = 1.0 + rughe * (0.62 * math.sin(a * 3.0 + t * 17.0)
                                  + 0.38 * math.sin(t * 31.0 - a * 2.0))
            v = p + ax * (math.cos(a) * r * onda) + ay * (math.sin(a) * r * ellisse * onda)
            row.append(bm.verts.new(mat4 @ v))
        grid.append(row)
    for i in range(len(grid) - 1):
        for j in range(lati):
            j2 = (j + 1) % lati
            bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
    bm.faces.new(list(reversed(grid[0])))
    bm.faces.new(grid[-1])


def _bm_mano24(bm, mat4, W, polso, direzione=(0.0, 0.0, 1.0), modo="grip", lato=1):
    """Mano scolpita con palmo, quattro dita articolate e pollice opponibile."""
    d = Vector(direzione)
    if d.length < 1e-6:
        d = Vector((0.0, 0.0, 1.0))
    M = mat4 @ Matrix.Translation(Vector(polso)) @ d.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4()
    _bm_sfera(bm, M, 0.0, 0.0, W * 0.035, W * 0.052,
              sx=0.70, sy=0.34, sz=1.00, u=12, v=8)
    for k in range(4):
        fx = (k - 1.5) * W * 0.019
        lun = W * (0.083 - abs(k - 1.4) * 0.007)
        p0 = (fx, -W * 0.002, W * 0.073)
        if modo == "aperta" or (modo == "indice" and k == 2):
            spread = (k - 1.5) * W * 0.013
            p1 = (fx + spread * 0.45, 0.0, W * 0.073 + lun * 0.55)
            p2 = (fx + spread, W * 0.003, W * 0.073 + lun)
        elif modo == "preghiera":
            p1 = (fx * 0.88, 0.0, W * 0.073 + lun * 0.55)
            p2 = (fx * 0.72, 0.0, W * 0.073 + lun)
        else:
            p1 = (fx, -W * 0.010, W * 0.073 + lun * 0.55)
            p2 = (fx, -W * 0.037, W * 0.073 + lun * 0.77)
        _bm_sweep24(bm, M, (p0, p1, p2),
                    (W * 0.0105, W * 0.0090, W * 0.0055), lati=7, campioni=2)
    s = 1 if lato >= 0 else -1
    _bm_sweep24(bm, M,
                ((s * W * 0.036, 0.0, W * 0.030),
                 (s * W * 0.066, -W * 0.009, W * 0.055),
                 (s * W * 0.070, -W * 0.025, W * 0.080)),
                (W * 0.014, W * 0.011, W * 0.006), lati=8, campioni=3)


def _bm_libro24(bm, bm_pat, mat4, W, H, centro, aperto=True, lato=1, piccolo=1.0):
    """Libro sottile con copertine, pagine e dorso; non più una tavola piena."""
    M = (mat4 @ Matrix.Translation(Vector(centro) + Vector((0.0, -W * 0.055, 0.0)))
         @ Matrix.Rotation(lato * 0.13, 4, "Y") @ Matrix.Rotation(-0.24, 4, "X"))
    bw = W * 0.40 * piccolo
    bh = H * 0.215 * piccolo
    if aperto:
        for s in (-1, 1):
            Mp = M @ Matrix.Translation((s * bw * 0.255, 0.0, 0.0)) @ Matrix.Rotation(s * 0.09, 4, "Z")
            _bm_box(bm, Mp, 0.0, 0.0, 0.0, bw * 0.49, W * 0.045, bh)
            _bm_box(bm, Mp, 0.0, -W * 0.026, 0.0, bw * 0.44, W * 0.014, bh * 0.94)
            for riga in (-0.25, 0.0, 0.25):
                _bm_box(bm_pat, Mp, 0.0, -W * 0.035, bh * riga,
                        bw * 0.29, W * 0.004, bh * 0.018)
        _bm_sweep24(bm, M, ((0.0, -W * 0.026, -bh * 0.49),
                            (0.0, -W * 0.034, 0.0),
                            (0.0, -W * 0.026, bh * 0.49)),
                    (W * 0.012, W * 0.015, W * 0.012), lati=7, campioni=2)
    else:
        _bm_box(bm, M, 0.0, 0.0, 0.0, bw * 0.62, W * 0.080, bh * 1.12)
        _bm_box(bm, M, 0.0, -W * 0.047, 0.0, bw * 0.55, W * 0.020, bh * 1.04)
        _bm_box(bm_pat, M, -lato * bw * 0.26, -W * 0.060, 0.0,
                bw * 0.055, W * 0.008, bh * 1.02)


def _bm_testa_profeta24(bm, bm_pat, mat4, r, yaw, nod, barba, copricapo, seed=0):
    """Volto gotico scolpito: anatomia, sguardi e capigliature individuali."""
    Mh = mat4 @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Rotation(nod, 4, "X")
    # Cranio, mascella, zigomi e mento: il volto non e' una sfera vuota.
    _bm_sfera(bm, Mh, 0.0, 0.015 * r, 0.02 * r, r,
              sx=0.77, sy=0.72, sz=1.03, u=28, v=18)
    _bm_sfera(bm, Mh, 0.0, -0.24 * r, -0.49 * r, 0.47 * r,
              sx=0.93, sy=0.67, sz=0.74, u=18, v=12)
    for s in (-1, 1):
        _bm_sfera(bm, Mh, s * 0.36 * r, -0.48 * r, -0.15 * r, 0.27 * r,
                  sx=0.94, sy=0.56, sz=0.74, u=14, v=9)
        # Orecchio con incavo e elice.
        _bm_sfera(bm, Mh, s * 0.75 * r, -0.005 * r, -0.08 * r, 0.17 * r,
                  sx=0.42, sy=0.64, sz=1.00, u=10, v=7)
        _bm_sfera(bm_pat, Mh, s * 0.79 * r, -0.075 * r, -0.08 * r, 0.085 * r,
                  sx=0.30, sy=0.40, sz=0.85, u=8, v=5)

    # Naso a ponte stretto e punta morbida, narici e filtro.
    _bm_sweep24(bm, Mh,
                ((0.0, -0.60 * r, 0.31 * r), (0.0, -0.79 * r, 0.08 * r),
                 (0.0, -0.91 * r, -0.17 * r)),
                (0.070 * r, 0.085 * r, 0.115 * r), lati=10, ellisse=0.78, campioni=4)
    _bm_sfera(bm, Mh, 0.0, -0.91 * r, -0.17 * r, 0.13 * r,
              sx=1.00, sy=0.69, sz=0.66, u=12, v=8)
    for s in (-1, 1):
        _bm_sfera(bm_pat, Mh, s * 0.082 * r, -0.944 * r, -0.225 * r, 0.040 * r,
                  sx=0.92, sy=0.30, sz=0.48, u=7, v=5)

    # Occhi infossati, iridi appena indicate, palpebre e sopracciglia.
    for s in (-1, 1):
        ex = s * 0.275 * r
        _bm_sfera(bm_pat, Mh, ex, -0.655 * r, 0.105 * r, 0.115 * r,
                  sx=1.38, sy=0.30, sz=0.68, u=10, v=6)
        _bm_sfera(bm, Mh, ex, -0.699 * r, 0.095 * r, 0.071 * r,
                  sx=1.20, sy=0.43, sz=0.55, u=10, v=6)
        _bm_sfera(bm_pat, Mh, ex, -0.731 * r, 0.096 * r, 0.025 * r,
                  sx=0.72, sy=0.25, sz=0.85, u=7, v=5)
        for su in (-1, 1):
            punti = []
            for k in range(5):
                t = k / 4.0
                punti.append((ex + (t - 0.5) * 0.30 * r,
                              -0.723 * r + 0.022 * r * abs(2 * t - 1),
                              0.095 * r + su * (0.042 + 0.025 * math.sin(math.pi * t)) * r))
            _bm_sweep24(bm, Mh, punti, [0.020 * r] * len(punti), lati=6, campioni=1)
        _bm_sweep24(bm, Mh,
                    ((ex - 0.17 * r, -0.655 * r, 0.285 * r),
                     (ex, -0.707 * r, 0.325 * r),
                     (ex + 0.17 * r, -0.635 * r, 0.275 * r)),
                    (0.026 * r, 0.042 * r, 0.022 * r), lati=7, ellisse=0.70, campioni=3)

    # Bocca e labbra: sottili, ma con una vera linea d'ombra.
    _bm_sweep24(bm_pat, Mh,
                ((-0.20 * r, -0.684 * r, -0.405 * r),
                 (0.0, -0.755 * r, -0.425 * r),
                 (0.20 * r, -0.684 * r, -0.405 * r)),
                (0.015 * r, 0.022 * r, 0.015 * r), lati=6, campioni=3)
    for sz in (-1, 1):
        _bm_sweep24(bm, Mh,
                    ((-0.18 * r, -0.704 * r, -0.405 * r + sz * 0.025 * r),
                     (0.0, -0.772 * r, -0.405 * r + sz * 0.035 * r),
                     (0.18 * r, -0.704 * r, -0.405 * r + sz * 0.025 * r)),
                    (0.018 * r, 0.027 * r, 0.018 * r), lati=6, ellisse=0.65, campioni=3)
    _bm_sfera(bm, Mh, 0.0, -0.49 * r, -0.69 * r, 0.22 * r,
              sx=1.10, sy=0.64, sz=0.52, u=12, v=8)

    # Massa dei capelli e ciocche ondulate separate sulla fronte.
    _bm_sfera(bm, Mh, 0.0, 0.12 * r, 0.43 * r, 0.86 * r,
              sx=0.96, sy=0.88, sz=0.63, u=22, v=14)
    for k in range(9):
        t = k / 8.0
        x = (t - 0.5) * 1.35 * r
        z = (0.46 + 0.17 * math.sin(math.pi * t)) * r
        verso = -1 if k % 2 else 1
        _bm_sweep24(bm, Mh,
                    ((x - verso * 0.055 * r, -0.56 * r, z + 0.08 * r),
                     (x, -0.665 * r, z),
                     (x + verso * 0.065 * r, -0.58 * r, z - 0.10 * r)),
                    (0.070 * r, 0.082 * r, 0.030 * r), lati=8, ellisse=0.70,
                    rughe=0.08, campioni=3)
    for s in (-1, 1):
        for k in range(3):
            zz = (0.29 - 0.23 * k) * r
            _bm_sweep24(bm, Mh,
                        ((s * 0.68 * r, -0.24 * r, zz + 0.18 * r),
                         (s * 0.77 * r, -0.35 * r, zz),
                         (s * 0.70 * r, -0.26 * r, zz - 0.18 * r)),
                        (0.095 * r, 0.105 * r, 0.040 * r), lati=8,
                        ellisse=0.74, rughe=0.07, campioni=3)

    if copricapo == "capelli_lunghi":
        for s in (-1, 1):
            for k in range(3):
                xx = s * (0.61 + 0.10 * k) * r
                _bm_sweep24(bm, Mh,
                            ((xx, 0.01 * r, 0.34 * r),
                             (xx + s * 0.08 * r, -0.12 * r, -0.35 * r),
                             (xx - s * 0.05 * r, -0.08 * r, -1.12 * r)),
                            (0.12 * r, 0.13 * r, 0.055 * r), lati=9,
                            ellisse=0.72, rughe=0.09, campioni=4)

    # Barba continua e scanalata, con punta irregolare e ciocche sul fronte.
    if barba > 0.05:
        lung = (0.50 + 0.48 * barba) * r
        grid = []
        nr, na = 11, 28
        for i in range(nr):
            t = i / (nr - 1.0)
            rx = (0.54 * (1.0 - t) ** 0.55 + 0.045) * r
            ry = (0.39 * (1.0 - t) ** 0.70 + 0.035) * r
            row = []
            for j in range(na):
                a = math.tau * j / na
                ond = 1.0 + 0.09 * math.sin(7 * a + t * 6.0 + seed)
                x = rx * math.cos(a) * ond
                y = -0.29 * r + ry * math.sin(a) * ond - 0.07 * r * (1.0 - t)
                z = -0.48 * r - lung * t + 0.035 * r * math.sin(5 * a + seed) * t
                row.append(bm.verts.new(Mh @ Vector((x, y, z))))
            grid.append(row)
        for i in range(nr - 1):
            for j in range(na):
                j2 = (j + 1) % na
                bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
        bm.faces.new(grid[-1])
        for k in range(7):
            x0 = (k - 3) * 0.13 * r
            _bm_sweep24(bm, Mh,
                        ((x0, -0.665 * r, -0.51 * r),
                         (x0 * 0.82 + 0.025 * r * math.sin(seed + k), -0.66 * r, -0.65 * r - lung * 0.38),
                         (x0 * 0.34, -0.47 * r, -0.48 * r - lung * 0.94)),
                        (0.045 * r, 0.055 * r, 0.012 * r), lati=7,
                        ellisse=0.62, campioni=4)
        for s in (-1, 1):
            _bm_sweep24(bm, Mh,
                        ((s * 0.035 * r, -0.82 * r, -0.30 * r),
                         (s * 0.19 * r, -0.77 * r, -0.35 * r),
                         (s * 0.32 * r, -0.61 * r, -0.47 * r)),
                        (0.045 * r, 0.055 * r, 0.020 * r), lati=7,
                        ellisse=0.68, campioni=3)

    # Copricapi distinti, con bordi morbidi e non geometrici.
    if copricapo == "berretta":
        _bm_sfera(bm, Mh, -0.05 * r, 0.07 * r, 0.65 * r, 0.83 * r,
                  sx=1.02, sy=0.93, sz=0.45, u=20, v=12)
        _bm_sweep24(bm, Mh,
                    ((-0.72 * r, -0.32 * r, 0.50 * r), (0.0, -0.66 * r, 0.48 * r),
                     (0.72 * r, -0.32 * r, 0.50 * r)),
                    (0.065 * r, 0.075 * r, 0.065 * r), lati=8, ellisse=0.65, campioni=4)
    elif copricapo == "zucchetto":
        _bm_sfera(bm, Mh, 0.0, 0.10 * r, 0.79 * r, 0.55 * r,
                  sx=1.0, sy=0.95, sz=0.37, u=16, v=9)
    elif copricapo == "turbante":
        for k in range(3):
            _bm_lathe(bm, Mh @ Matrix.Translation((0.0, 0.0, (0.30 + 0.18 * k) * r)),
                      ((0.0, (0.94 - 0.08 * k) * r),
                       (0.12 * r, (1.00 - 0.08 * k) * r),
                       (0.22 * r, (0.90 - 0.08 * k) * r)),
                      seg=24, sy=0.91, rib=0.055, rib_n=7)
    elif copricapo in ("cappuccio", "velo"):
        # Calotta arretrata e bordo a ferro di cavallo: il volto resta libero.
        _bm_sfera(bm, Mh, 0.0, 0.30 * r, 0.08 * r, 1.06 * r,
                  sx=0.99, sy=0.72, sz=1.16, u=24, v=15)
        punti = []
        for k in range(13):
            a = math.pi * (0.08 + 0.84 * k / 12.0)
            punti.append((-1.00 * r * math.cos(a), -0.31 * r,
                          -0.18 * r + 1.30 * r * math.sin(a)))
        _bm_sweep24(bm, Mh, punti, [0.12 * r] * len(punti),
                    lati=10, ellisse=0.72, rughe=0.06, campioni=2)
        for s in (-1, 1):
            for k in range(2):
                _bm_sweep24(bm, Mh,
                            ((s * (0.84 + 0.09 * k) * r, -0.13 * r, 0.18 * r),
                             (s * (0.92 + 0.08 * k) * r, -0.16 * r, -0.68 * r),
                             (s * (0.74 + 0.10 * k) * r, -0.08 * r, -1.55 * r)),
                            (0.14 * r, 0.16 * r, 0.08 * r), lati=9,
                            ellisse=0.66, rughe=0.08, campioni=4)


def _bm_drappo_parapetto24(bm, mat4, cx, y, z_top, larg, lun, seed=0):
    """Manto continuo e mosso che ricade oltre il davanzale cosmatesco."""
    nu, nv = 20, 12
    fronte, retro = [], []
    for i in range(nu + 1):
        t = i / nu
        fr, br = [], []
        for j in range(nv + 1):
            u = 2.0 * j / nv - 1.0
            width = larg * (1.0 - 0.16 * t)
            x = cx + u * width * 0.5 + 0.025 * larg * math.sin(t * 5.0 + seed) * t
            z = z_top - lun * t + 0.30 * lun * (u * u) * t
            yf = y - 0.018 * math.cos(u * math.pi * 1.2 + t * 1.4) * (0.35 + 0.65 * t)
            fr.append(bm.verts.new(mat4 @ Vector((x, yf, z))))
            br.append(bm.verts.new(mat4 @ Vector((x, yf + 0.025, z))))
        fronte.append(fr)
        retro.append(br)
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((fronte[i][j], fronte[i][j + 1], fronte[i + 1][j + 1], fronte[i + 1][j]))
            bm.faces.new((retro[i + 1][j], retro[i + 1][j + 1], retro[i][j + 1], retro[i][j]))
    for i in range(nu):
        bm.faces.new((fronte[i][0], fronte[i + 1][0], retro[i + 1][0], retro[i][0]))
        bm.faces.new((fronte[i + 1][-1], fronte[i][-1], retro[i][-1], retro[i + 1][-1]))
    for j in range(nv):
        bm.faces.new((fronte[-1][j], fronte[-1][j + 1], retro[-1][j + 1], retro[-1][j]))


def _bm_busto_profeta24(bm, bm_pat, mat4, W, H, spec):
    """Altorilievo v2.4: figura gotica organica, panneggiata e realmente posata.

    Le superfici del torso e dei manti sono continue e scanalate nella mesh;
    maniche e dita seguono curve anatomiche. Ogni campata conserva la posa
    letta dalla fotografia, ma perde la simmetria e la rigidita' da manichino.
    """
    yaw = spec.get("yaw", 0.0)
    nod = spec.get("nod", 0.10)
    gesto = spec.get("gesto", "libro")
    barba = spec.get("barba", 0.6)
    copricapo = spec.get("copricapo", "capelli")
    lato = spec.get("lato", 1)
    seed = spec.get("seed", 0)
    lean = yaw * W * 0.075 + (0.035 * W if gesto == "sporgente" else 0.0)

    def shift(z):
        return lean * (z / H) + 0.012 * W * math.sin(seed * 1.7 + z / H * 2.2)

    def sezione(z):
        t = max(0.0, min(1.0, z / (H * 0.62)))
        # Vento raccolto sulle ginocchia, ventre, torace e spalle.
        anchors = ((0.00, 0.31, 0.18), (0.18, 0.36, 0.205),
                   (0.48, 0.33, 0.190), (0.78, 0.37, 0.180),
                   (0.92, 0.31, 0.150), (1.00, 0.14, 0.115))
        rx, ry = anchors[-1][1], anchors[-1][2]
        for a, b in zip(anchors, anchors[1:]):
            if a[0] <= t <= b[0]:
                u = (t - a[0]) / (b[0] - a[0])
                u = u * u * (3.0 - 2.0 * u)
                rx = (a[1] * (1 - u) + b[1] * u) * W
                ry = (a[2] * (1 - u) + b[2] * u) * W
                break
        return shift(z), -0.045 * W - 0.035 * W * math.sin(math.pi * t), rx, ry

    # Torso unico, denso e scolpito: niente ellissoidi sovrapposti.
    grid = []
    nz, na = 26, 48
    for i in range(nz + 1):
        t = i / nz
        z = H * 0.62 * t
        cx, cy, rx, ry = sezione(z)
        row = []
        for j in range(na):
            a = math.tau * j / na
            front = max(0.0, -math.sin(a)) ** 1.5
            amp = W * 0.042 * math.sin(math.pi * t) ** 0.65 * (0.30 + 0.70 * front)
            fase = 7.0 * a + 4.6 * t + 0.85 * math.sin(3.0 * a + seed)
            scult = amp * (math.sin(fase) + 0.32 * math.sin(2.0 * fase + 0.7))
            x = cx + (rx + scult) * math.cos(a)
            y = cy + (ry + scult * 0.72) * math.sin(a)
            # Spalle non perfettamente orizzontali.
            zz = z + H * 0.012 * math.cos(a) * math.sin(math.pi * t) * math.sin(seed + 0.8)
            row.append(bm.verts.new(mat4 @ Vector((x, y, zz))))
        grid.append(row)
    for i in range(nz):
        for j in range(na):
            j2 = (j + 1) % na
            bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
    bm.faces.new(list(reversed(grid[0])))
    bm.faces.new(grid[-1])

    # Grandi pieghe a U sul ventre e sulle ginocchia: il rilievo deve leggere
    # anche nella vista d'insieme, non soltanto nel wireframe.
    for k_fold in range(4):
        z_fold = H * (0.085 + 0.105 * k_fold)
        punti_fold = []
        for j_fold in range(11):
            u_fold = -1.0 + 2.0 * j_fold / 10.0
            zf = z_fold + H * (0.040 * u_fold * u_fold - 0.014)
            xf = shift(zf) + u_fold * W * (0.285 - 0.018 * k_fold)
            cx_f, cy_f, rx_f, ry_f = sezione(zf)
            q_fold = max(-0.96, min(0.96, (xf - cx_f) / max(rx_f, 1e-5)))
            yf = cy_f - ry_f * math.sqrt(max(0.0, 1.0 - q_fold * q_fold)) - W * 0.018
            punti_fold.append((xf, yf, zf))
        _bm_sweep24(bm, mat4, punti_fold,
                    [W * (0.010 + 0.004 * math.sin(math.pi * j / 10.0)) for j in range(11)],
                    lati=8, ellisse=0.58, campioni=2)

    # Ampio manto diagonale aderente al torso, con pieghe trasversali vere.
    nu, nv = 24, 10
    drappo_grid = []
    for i in range(nu + 1):
        t = i / nu
        zc = H * (0.575 - 0.50 * t)
        xc = shift(zc) + lato * W * (0.27 - 0.57 * t)
        row = []
        for j in range(nv + 1):
            u = 2.0 * j / nv - 1.0
            z = zc + u * H * 0.042
            x = xc + u * W * (0.095 + 0.018 * math.sin(math.pi * t))
            cx, cy, rx, ry = sezione(max(0.0, min(H * 0.62, z)))
            q = max(-0.97, min(0.97, (x - cx) / max(rx, 1e-5)))
            yf = cy - ry * math.sqrt(max(0.0, 1.0 - q * q))
            yf -= W * (0.022 + 0.014 * math.cos(u * math.pi * 3.0 + t * 4.0))
            row.append(bm.verts.new(mat4 @ Vector((x, yf, z))))
        drappo_grid.append(row)
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((drappo_grid[i][j], drappo_grid[i][j + 1],
                          drappo_grid[i + 1][j + 1], drappo_grid[i + 1][j]))
    # Orli morbidi del manto, non barre cilindriche sul petto.
    for edge in (0, -1):
        punti = []
        for i in range(0, nu + 1, 3):
            # Ricava il punto trasformando l'indice in coordinate gia' note.
            v = drappo_grid[i][edge].co.copy()
            # mat4 e' quasi sempre una trasformazione rigida+scala uniforme:
            # l'inversa riporta il bordo nel sistema locale della figura.
            punti.append(mat4.inverted() @ v)
        _bm_sweep24(bm, mat4, punti, [W * 0.012] * len(punti), lati=7, ellisse=0.70, campioni=2)

    z_sh = H * 0.545
    r_h = H * 0.116
    z_head = H * (0.760 if gesto == "sporgente" else 0.805)
    y_h = -0.105 * W
    x_head = shift(z_head)

    # Collo e trapezio, raccordati al torso.
    _bm_sweep24(bm, mat4,
                ((shift(H * 0.58), -0.045 * W, H * 0.575),
                 (x_head * 0.96, y_h * 0.70, H * 0.655),
                 (x_head, y_h, z_head - r_h * 0.73)),
                (W * 0.115, W * 0.092, r_h * 0.48), lati=16, ellisse=0.84, campioni=4)

    def braccio(s, gomito, polso, r=1.0, mano_modo="grip", direzione=None):
        spalla = (shift(z_sh) + s * W * 0.325, -0.065 * W, z_sh)
        g = Vector(gomito) + Vector((0.0, -W * 0.050, 0.0))
        p = Vector(polso) + Vector((0.0, -W * 0.060, 0.0))
        sp = Vector(spalla)
        upper = sp.lerp(g, 0.52) + Vector((s * W * 0.018, -W * 0.018, H * 0.012))
        lower = g.lerp(p, 0.53) + Vector((0.0, -W * 0.012, 0.0))
        _bm_sweep24(bm, mat4, (spalla, upper, gomito, lower, polso),
                    (W * 0.138 * r, W * 0.128 * r, W * 0.112 * r,
                     W * 0.084 * r, W * 0.052 * r),
                    lati=14, ellisse=0.82, rughe=0.105, campioni=4)
        # Risvolto della manica al polso.
        d = (p - g).normalized()
        _bm_sweep24(bm, mat4, (p - d * W * 0.035, p),
                    (W * 0.057 * r, W * 0.052 * r), lati=12, ellisse=0.80, campioni=2)
        _bm_mano24(bm, mat4, W, polso, direzione if direzione is not None else p - g,
                   modo=mano_modo, lato=s)

    if gesto == "libro":
        for s in (-1, 1):
            braccio(s, (shift(H * 0.25) + s * W * 0.42, -0.245 * W, H * 0.245),
                    (s * W * 0.18, -0.335 * W, H * 0.315), r=0.88)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.305 * W, H * 0.315), True, lato)
    elif gesto == "libro_basso":
        for s in (-1, 1):
            braccio(s, (s * W * 0.40, -0.235 * W, H * 0.155),
                    (s * W * 0.17, -0.325 * W, H * 0.205), r=0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.300 * W, H * 0.205), True, lato, 0.94)
    elif gesto == "libro_chiuso":
        _bm_libro24(bm, bm_pat, mat4, W, H, (lato * W * 0.14, -0.270 * W, H * 0.325), False, lato)
        braccio(lato, (lato * W * 0.41, -0.230 * W, H * 0.190),
                (lato * W * 0.16, -0.315 * W, H * 0.220), r=0.92)
        braccio(-lato, (-lato * W * 0.40, -0.215 * W, H * 0.290),
                (lato * W * 0.035, -0.320 * W, H * 0.410), r=0.88)
    elif gesto == "rotolo":
        _bm_sweep24(bm, mat4,
                    ((lato * W * 0.11, -0.295 * W, H * 0.53),
                     (lato * W * 0.10, -0.310 * W, H * 0.31),
                     (lato * W * 0.15, -0.295 * W, H * 0.075)),
                    (W * 0.041, W * 0.045, W * 0.033), lati=12, ellisse=0.55, campioni=5)
        braccio(lato, (lato * W * 0.41, -0.230 * W, H * 0.350),
                (lato * W * 0.12, -0.335 * W, H * 0.500), r=0.90)
        braccio(-lato, (-lato * W * 0.42, -0.230 * W, H * 0.190),
                (lato * W * 0.095, -0.330 * W, H * 0.235), r=0.90)
    elif gesto == "petto_tavola":
        braccio(lato, (lato * W * 0.40, -0.215 * W, H * 0.320),
                (-lato * W * 0.035, -0.315 * W, H * 0.500), r=0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (-lato * W * 0.20, -0.255 * W, H * 0.240), False, -lato, 0.82)
        braccio(-lato, (-lato * W * 0.42, -0.220 * W, H * 0.170),
                (-lato * W * 0.22, -0.310 * W, H * 0.215), r=0.92)
    elif gesto == "incrociate":
        braccio(1, (W * 0.41, -0.220 * W, H * 0.240),
                (-W * 0.16, -0.330 * W, H * 0.380), r=0.94)
        braccio(-1, (-W * 0.41, -0.250 * W, H * 0.215),
                (W * 0.16, -0.355 * W, H * 0.325), r=0.94)
    elif gesto == "preghiera":
        for s in (-1, 1):
            braccio(s, (s * W * 0.36, -0.165 * W, H * 0.185),
                    (s * W * 0.025, -0.300 * W, H * 0.405), r=0.88,
                    mano_modo="preghiera", direzione=(0.0, 0.0, 1.0))
    elif gesto == "inchino":
        for s in (-1, 1):
            braccio(s, (s * W * 0.36, -0.165 * W, H * 0.155),
                    (s * W * 0.055, -0.300 * W, H * 0.265), r=0.92)
    elif gesto == "pensatore":
        braccio(lato, (lato * W * 0.37, -0.190 * W, H * 0.205),
                (x_head + lato * W * 0.12, -0.265 * W, z_head - r_h * 0.48),
                r=0.87, direzione=(-lato * 0.2, 0.0, 1.0))
        braccio(-lato, (-lato * W * 0.41, -0.230 * W, H * 0.180),
                (lato * W * 0.08, -0.320 * W, H * 0.245), r=0.92)
    elif gesto == "parlante":
        p_mano = (lato * W * 0.32, -0.270 * W, H * 0.610)
        braccio(lato, (lato * W * 0.40, -0.175 * W, H * 0.350), p_mano,
                r=0.86, mano_modo="aperta", direzione=(lato * 0.15, 0.0, 1.0))
        _bm_libro24(bm, bm_pat, mat4, W, H, (-lato * W * 0.15, -0.270 * W, H * 0.260), False, lato, 0.88)
        braccio(-lato, (-lato * W * 0.41, -0.220 * W, H * 0.175),
                (-lato * W * 0.16, -0.310 * W, H * 0.205), r=0.90)
    elif gesto == "sporgente":
        braccio(-1, (-W * 0.44, -0.235 * W, H * 0.300),
                (-W * 0.46, -0.320 * W, H * 0.045), r=0.83,
                mano_modo="aperta", direzione=(-0.25, 0.0, -1.0))
        braccio(1, (W * 0.39, -0.160 * W, H * 0.510),
                (W * 0.31, -0.245 * W, H * 0.735), r=0.82,
                direzione=(-0.2, 0.0, 1.0))
        # Il lembo afferrato sale davvero fino alla mano.
        _bm_sweep24(bm, mat4,
                    ((W * 0.30, -0.225 * W, H * 0.73),
                     (W * 0.25, -0.285 * W, H * 0.54),
                     (W * 0.15, -0.310 * W, H * 0.39)),
                    (W * 0.042, W * 0.060, W * 0.035), lati=10,
                    ellisse=0.52, rughe=0.10, campioni=5)
    elif gesto == "madonna":
        bx = W * 0.225 + shift(H * 0.35)
        # Bambino: corpicino avvolto, testa proporzionata, braccia e gambe.
        _bm_sweep24(bm, mat4,
                    ((bx, -0.270 * W, H * 0.245), (bx - W * 0.025, -0.295 * W, H * 0.390),
                     (bx, -0.275 * W, H * 0.520)),
                    (W * 0.105, W * 0.120, W * 0.065), lati=16,
                    ellisse=0.70, rughe=0.10, campioni=5)
        cr = r_h * 0.49
        _bm_sfera(bm, mat4, bx, -0.285 * W, H * 0.595, cr,
                  sx=0.84, sy=0.78, sz=1.0, u=18, v=12)
        for s in (-1, 1):
            _bm_sweep24(bm, mat4,
                        ((bx + s * W * 0.065, -0.270 * W, H * 0.475),
                         (bx + s * W * 0.125, -0.300 * W, H * 0.425),
                         (bx + s * W * 0.155, -0.305 * W, H * 0.455)),
                        (W * 0.026, W * 0.022, W * 0.012), lati=8, campioni=3)
            _bm_sweep24(bm, mat4,
                        ((bx + s * W * 0.050, -0.255 * W, H * 0.280),
                         (bx + s * W * 0.085, -0.290 * W, H * 0.190)),
                        (W * 0.035, W * 0.018), lati=8, campioni=3)
        for k in range(5):
            a = math.pi * k / 4.0
            _bm_sfera(bm, mat4, bx + math.cos(a) * cr * 0.65,
                      -0.285 * W - cr * 0.35, H * 0.595 + cr * (0.55 + 0.30 * math.sin(a)),
                      cr * 0.25, u=8, v=6)
        braccio(1, (W * 0.41, -0.225 * W, H * 0.260),
                (bx - W * 0.020, -0.340 * W, H * 0.320), r=0.92)
        braccio(-1, (-W * 0.40, -0.220 * W, H * 0.250),
                (bx - W * 0.065, -0.330 * W, H * 0.440), r=0.88)
    elif gesto == "indica":
        p_mano = (lato * W * 0.78, -0.270 * W, H * 0.625)
        braccio(lato, (lato * W * 0.51, -0.215 * W, H * 0.510), p_mano,
                r=0.83, mano_modo="indice", direzione=(lato, 0.0, 0.18))
        braccio(-lato, (-lato * W * 0.41, -0.220 * W, H * 0.200),
                (-lato * W * 0.14, -0.310 * W, H * 0.220), r=0.90)
    elif gesto == "parla":
        p_mano = (lato * W * 0.50, -0.270 * W, H * 0.695)
        braccio(lato, (lato * W * 0.43, -0.185 * W, H * 0.380), p_mano,
                r=0.82, mano_modo="aperta", direzione=(lato * 0.18, 0.0, 1.0))
        braccio(-lato, (-lato * W * 0.41, -0.225 * W, H * 0.300),
                (lato * W * 0.015, -0.320 * W, H * 0.490), r=0.90)

    Mh = Matrix.Translation((x_head, y_h, z_head))
    _bm_testa_profeta24(bm, bm_pat, mat4 @ Mh, r_h, yaw, nod, barba, copricapo, seed)


def _bm_fascia_spiovente(bm, mat4, cx, hw, z_base, z_apex, y, o0, o1, profondita):
    """Fascia modanata parallela a uno spiovente del frontone, tagliata a mitra
    sull'asse (le due falde si incontrano in punta senza sovrapporsi).

    `o0`, `o1` sono gli scostamenti misurati perpendicolarmente allo spiovente:
    la fascia resta così sempre dello stesso spessore visivo, come in fotografia.
    """
    dz = z_apex - z_base
    L = math.hypot(hw, dz)
    nz = hw / L
    nx = dz / L
    for s in (-1, 1):
        p_in = Vector((cx + s * hw + s * nx * o0, z_base + nz * o0))
        p_out = Vector((cx + s * hw + s * nx * o1, z_base + nz * o1))
        a_in = Vector((cx, z_apex + o0 * L / hw))
        a_out = Vector((cx, z_apex + o1 * L / hw))
        poli = [(p_in.x, p_in.y), (p_out.x, p_out.y), (a_out.x, a_out.y), (a_in.x, a_in.y)]
        if s < 0:
            poli = poli[::-1]
        _bm_lastra(bm, mat4 @ Matrix.Translation((0.0, y, 0.0)), poli, profondita)


def _bm_tabernacolo(bm_w, bm_r, bm_f, bm_p, mat4, x, y, z0, h, lar, variant=0):
    """Tabernacolo gotico con statuina, infisso fra due frontoni (come nella
    fotografia del coronamento senese): zoccolo, vano in ombra con colonnine
    angolari, ghimberga compatta e fiorone."""
    # zoccolo a due gradoni
    _bm_box(bm_w, mat4, x, y - 0.008, z0 + h * 0.022, lar * 1.90, 0.120, h * 0.044)
    _bm_box(bm_r, mat4, x, y - 0.028, z0 + h * 0.052, lar * 1.62, 0.095, h * 0.018)
    # vano in ombra e statuina
    _bm_box(bm_p, mat4, x, y + 0.052, z0 + h * 0.300, lar * 1.30, 0.040, h * 0.470)
    _bm_lathe(bm_f, mat4 @ Matrix.Translation((x, y - 0.012, z0 + h * 0.090)),
              ((0.00, lar * 0.420), (h * 0.070, lar * 0.440), (h * 0.200, lar * 0.340),
               (h * 0.300, lar * 0.250)), seg=12, sy=0.68, rib=0.06, rib_n=7)
    _bm_sfera(bm_f, mat4, x, y - 0.036, z0 + h * 0.372, lar * 0.150,
              sx=0.88, sy=0.76, sz=1.04, u=12, v=8)
    _bm_sfera(bm_f, mat4, x, y - 0.030, z0 + h * 0.448, lar * 0.160,
              sx=1.02, sy=0.92, sz=0.58, u=10, v=6)
    # quattro colonnine angolari del vano
    for sx in (-1, 1):
        _bm_lathe(bm_w, mat4 @ Matrix.Translation((x + sx * lar * 0.70, y - 0.010,
                                                   z0 + h * 0.070)),
                  ((0.00, lar * 0.230), (0.012, lar * 0.185), (h * 0.400, lar * 0.175),
                   (h * 0.450, lar * 0.215)), seg=8, sy=0.95, rib=0.08, rib_n=5)
    # coronamento: cimasa, ghimberga e fiorone
    _bm_box(bm_w, mat4, x, y - 0.006, z0 + h * 0.500, lar * 1.92, 0.130, h * 0.026)
    _bm_box(bm_r, mat4, x, y - 0.030, z0 + h * 0.518, lar * 1.70, 0.100, h * 0.012)
    hw_c = lar * 0.86
    _bm_ghimberga(bm_w, mat4, x, hw_c, z0 + h * 0.532, z0 + h * 0.790,
                  y - 0.020, h * 0.022, 0.070, crockets=bm_f, n_croc=2, croc_size=h * 0.030)
    _bm_ghimberga(bm_r, mat4, x, hw_c * 0.66, z0 + h * 0.545, z0 + h * 0.745,
                  y - 0.004, h * 0.012, 0.040)
    _bm_lathe(bm_f, mat4 @ Matrix.Translation((x, y - 0.030, z0 + h * 0.800)),
              ((0.0, lar * 0.34), (h * 0.018, lar * 0.38), (h * 0.052, lar * 0.18),
               (h * 0.085, 0.003)), seg=10, sy=0.90)


def edicola_galleria_profeta(name, col, cx, y, z0, w, h, variant=0):
    """Edicola della galleria dei Profeti, v2.4 — proporzioni misurate sulla
    fotografia `riferimento_galleria.jpg`:

      • nicchia a TUTTO SESTO poco profonda (altorilievo, non un vano buio)
        con fondale continuo in marmo rosa rigato che riempie anche la
        lunetta dietro la testa; triplice ghiera concentrica (bianco/rosa/
        bianco) con perlinatura sulla ghiera esterna;
      • piedritti a parasta con specchiatura cosmatesca verticale, file di
        perle ai lati e capitello a fasce all'imposta dell'arco;
      • frontone triangolare PIENO a chevron (non solo fasce vuote), con
        doppia cornice modanata, triangolo inciso interno, losanga
        cosmatesca verso la punta, gattoni e fiorone;
      • pinnacolino con statuina sull'asse dei piedritti, nella V fra due
        frontoni, davanti a un pannellino cosmatesco incassato;
      • parapetto con specchiatura cosmatesca sotto ogni campata e, per le
        figure che in foto lo mostrano, il lembo del manto che scende
        davanti al parapetto;
      • mezzo busto grande che riempie la nicchia fin dentro l'arco, con
        la posa della tabella `_POSE_PROFETI`.
    """
    spec = dict(_POSE_PROFETI[variant % len(_POSE_PROFETI)])
    spec["lato"] = 1 if variant % 2 == 0 else -1
    spec["seed"] = variant

    z_dav = z0 + 0.055 * h          # piano del davanzale / base del busto
    z_imp = z0 + 0.470 * h          # imposta dell'arco a tutto sesto
    op = 0.675 * w                  # luce della nicchia: figure piu' grandi
    hw_o = op * 0.5
    rise = hw_o                     # semicerchio
    z_top = z_imp + rise            # chiave interna dell'arco
    z_gb = z0 + 0.515 * h           # base del frontone (dietro l'arco)
    z_apice = z0 + 0.822 * h        # punta del frontone (v2.5: chevron piu' ribassato, come in foto)
    hw_g = 0.485 * w

    bm_w = bmesh.new()
    bm_r = bmesh.new()
    bm_f = bmesh.new()
    bm_p = bmesh.new()
    bm_c = bmesh.new()
    Mi = Matrix.Identity(4)

    # ------------------------------------------------------------- piedritti
    def _piedritto(xs):
        z_mid = (z0 + z_imp) * 0.5
        _bm_box(bm_w, Mi, xs, y + 0.005, z_mid, w * 0.225, 0.125,
                z_imp - z0 + 0.030)
        # specchiatura cosmatesca verticale al centro della parasta
        _bm_box(bm_c, Mi, xs, y - 0.060, (z_dav + z_imp) * 0.5,
                w * 0.090, 0.014, (z_imp - z_dav) * 0.82)
        # file di perle ai lati della specchiatura
        n_per = max(6, int((z_imp - z_dav) * 0.80 / 0.048))
        for sl in (-1, 1):
            for k_per in range(n_per):
                _bm_sfera(bm_f, Mi, xs + sl * w * 0.091, y - 0.064,
                          z_dav + (z_imp - z_dav) * 0.10
                          + k_per * ((z_imp - z_dav) * 0.80 / max(1, n_per - 1)),
                          w * 0.0145, sx=1.0, sy=0.55, sz=1.0, u=6, v=4)
        # base e capitello a fasce
        _bm_box(bm_w, Mi, xs, y - 0.012, z_dav + 0.016, w * 0.270, 0.145, 0.055)
        _bm_box(bm_r, Mi, xs, y - 0.020, z_dav + 0.050, w * 0.255, 0.130, 0.016)
        _bm_box(bm_r, Mi, xs, y - 0.018, z_imp - 0.022, w * 0.290, 0.150, 0.034)
        _bm_box(bm_w, Mi, xs, y - 0.024, z_imp + 0.006, w * 0.305, 0.162, 0.024)
        # losanghetta scolpita sulla base
        _bm_box(bm_f, Mi, xs, y - 0.088, z_dav + 0.016, w * 0.052, 0.016,
                w * 0.052, rot=Matrix.Rotation(math.pi * 0.25, 4, "Y"))

    _piedritto(cx + w * 0.5)
    if variant == 0:
        _piedritto(cx - w * 0.5)

    # ----------------------------------------------------- nicchia incassata
    # fondale in marmo rosa rigato: sale fino in chiave, la lunetta dietro
    # la testa e' rosa come in fotografia (niente catino scuro)
    box(f"{name}_Fondo", col, cx, y + 0.125, (z_dav + z_top) * 0.5,
        op + 0.10, 0.070, (z_top - z_dav) + 0.05, RIGATO, fit_uv=True)
    # spallette e soffitto del vano
    for s in (-1, 1):
        _bm_box(bm_w, Mi, cx + s * (hw_o + 0.012), y + 0.055,
                (z_dav + z_imp) * 0.5, 0.024, 0.190, z_imp - z_dav)
    _bm_box(bm_w, Mi, cx, y + 0.055, z_top - 0.012, op + 0.05, 0.190, 0.030)
    # fodera interna dell'arco in marmo rosa, arretrata
    _bm_arco_acuto(bm_r, Mi, cx, y + 0.082, z_imp, op + 0.030,
                   (op + 0.030) * 0.5, 0.020, seg_u=22, seg_v=7)

    # ------------------------------------------------------------ arcata
    y_arco = y - 0.040
    _bm_arco_acuto(bm_w, Mi, cx, y_arco, z_imp, op + 0.105,
                   (op + 0.105) * 0.5, 0.030, seg_u=26, seg_v=8)
    _bm_arco_acuto(bm_r, Mi, cx, y_arco - 0.008, z_imp, op + 0.052,
                   (op + 0.052) * 0.5, 0.016, seg_u=26, seg_v=7)
    _bm_arco_acuto(bm_w, Mi, cx, y_arco + 0.014, z_imp, op + 0.008,
                   (op + 0.008) * 0.5, 0.013, seg_u=24, seg_v=6)
    # perlinatura sulla ghiera esterna + chiave di volta scolpita
    for k in range(23):
        a_b = math.pi * k / 22.0
        _bm_sfera(bm_f, Mi, cx - (hw_o + 0.052) * math.cos(a_b),
                  y_arco - 0.028, z_imp + (hw_o + 0.052) * math.sin(a_b),
                  0.0075, u=7, v=5)
    _bm_box(bm_f, Mi, cx, y_arco - 0.012, z_top + 0.045, 0.046, 0.052, 0.095)

    # -------------------------------------------------------------- parapetto
    _bm_box(bm_w, Mi, cx, y - 0.020, z_dav - 0.012, w * 1.005, 0.240, 0.045)
    _bm_box(bm_r, Mi, cx, y - 0.058, z_dav - 0.041, w * 0.990, 0.170, 0.018)
    _bm_box(bm_w, Mi, cx, y - 0.005, (z0 + z_dav) * 0.5 - 0.010,
            w * 0.990, 0.190, (z_dav - z0) + 0.012)
    # specchiatura cosmatesca sotto la campata, come sullo zoccolo senese
    # (v2.5: piu' ampia — in foto la fascia musiva corre quasi continua
    # sotto i profeti, interrotta solo dai lembi dei manti)
    _bm_box(bm_c, Mi, cx, y - 0.103, (z0 + z_dav) * 0.5 - 0.010,
            w * 0.815, 0.014, (z_dav - z0) * 0.80)

    # --------------------------------------------------- frontone a chevron
    # pannello triangolare pieno dietro l'arco
    _bm_lastra(bm_w, Mi, [(cx - hw_g, z_gb), (cx + hw_g, z_gb), (cx, z_apice)],
               0.055, y0=y + 0.018)
    # triangolo inciso interno (linea d'ombra)
    _bm_fascia_spiovente(bm_p, Mi, cx, hw_g, z_gb, z_apice, y + 0.010,
                         -0.060, -0.048, 0.012)
    # cornici modanate sugli spioventi
    _bm_fascia_spiovente(bm_w, Mi, cx, hw_g, z_gb, z_apice, y - 0.030,
                         -0.006, 0.020, 0.055)
    _bm_fascia_spiovente(bm_r, Mi, cx, hw_g, z_gb, z_apice, y - 0.022,
                         0.020, 0.034, 0.034)
    _bm_fascia_spiovente(bm_w, Mi, cx, hw_g, z_gb, z_apice, y - 0.032,
                         0.034, 0.062, 0.060)
    # Motivo interno del frontone (v2.5): nella fotografia ogni timpano ha
    # una seconda cornice a chevron in rilievo e, dentro, una piccola ogiva
    # traforata con giglio e rosetta. La vecchia losanga + foglie incrociate
    # leggeva nel render come una "X" estranea.
    H_gh = z_apice - z_gb
    # seconda cornice a chevron in rilievo, interna alle modanature
    _bm_fascia_spiovente(bm_w, Mi, cx, hw_g, z_gb, z_apice, y - 0.004,
                         -0.080, -0.066, 0.028)
    # ogivetta centrale con colonnine ai piedi (in parte celata dall'arco,
    # come il traforo reale che nasce dietro la chiave)
    span_og = w * 0.205
    z_ogb = z_gb + H_gh * 0.26
    rise_og = H_gh * 0.40
    _bm_arco_acuto(bm_f, Mi, cx, y - 0.024, z_ogb, span_og, rise_og, 0.0085,
                   seg_u=18, seg_v=6)
    for sl in (-1, 1):
        _bm_segmento(bm_f, Mi,
                     (cx + sl * span_og * 0.5, y - 0.024, z_ogb - H_gh * 0.16),
                     (cx + sl * span_og * 0.5, y - 0.024, z_ogb),
                     0.0085, 0.0085, seg=8)
        _bm_sfera(bm_f, Mi, cx + sl * span_og * 0.5, y - 0.026,
                  z_ogb - H_gh * 0.005, 0.0110, sx=1.15, sy=0.8, sz=0.75, u=8, v=5)
    # giglio senese a tre petali dentro l'ogiva
    z_gi = z_ogb + rise_og * 0.10
    _bm_sweep24(bm_f, Mi,
                ((cx, y - 0.020, z_gi - h * 0.030),
                 (cx, y - 0.030, z_gi + h * 0.020)),
                (h * 0.008, h * 0.006), lati=7, campioni=2)
    _bm_foglia(bm_f, h * 0.092, h * 0.030, h * 0.014,
               Mi @ Matrix.Translation((cx, y - 0.024, z_gi)),
               gonfia=1.20)
    for sl in (-1, 1):
        _bm_foglia(bm_f, h * 0.072, h * 0.027, h * 0.013,
                   Mi @ Matrix.Translation((cx + sl * h * 0.008, y - 0.023,
                                            z_gi - h * 0.004))
                   @ Matrix.Rotation(sl * 0.66, 4, "Y"),
                   piega=sl * 0.10, gonfia=1.18)
        # volutina fogliata alla base dell'ogiva, sui due lati
        _bm_foglia(bm_f, h * 0.055, h * 0.022, h * 0.011,
                   Mi @ Matrix.Translation((cx + sl * span_og * 0.62,
                                            y - 0.016, z_ogb - H_gh * 0.13))
                   @ Matrix.Rotation(sl * 0.95, 4, "Y"),
                   piega=-sl * 0.12, gonfia=1.15)
    # rosetta nella punta dell'ogiva, sotto il vertice del timpano
    _bm_rosetta(bm_f, Mi, cx, y - 0.018,
                z_ogb + rise_og * 0.80, h * 0.018, petali=6, spess=0.45)
    # gattoni rampanti digradanti + fiorone in punta (v2.5: sei per falda,
    # piu' grandi e uncinati — in foto la cresta del chevron e' fitta)
    ang_gh = math.atan2(z_apice - z_gb, hw_g)
    for s in (-1, 1):
        for k in range(6):
            t = 0.13 + 0.74 * k / 5.0
            gx = cx + s * hw_g * (1.0 - t) + s * math.sin(ang_gh) * 0.072
            gz = z_gb + (z_apice - z_gb) * t + math.cos(ang_gh) * 0.072
            Mg = (Mi @ Matrix.Translation((gx, y - 0.048, gz))
                  @ Matrix.Rotation(-s * ang_gh * 0.95, 4, "Y"))
            _bm_foglia(bm_f, h * 0.045 * (1.08 - 0.30 * t), h * 0.021,
                       h * 0.013, Mg, piega=-0.16 * s, gonfia=1.28)
    _bm_lathe(bm_f, Mi @ Matrix.Translation((cx, y - 0.048, z_apice + h * 0.018)),
              ((0.0, 0.021), (h * 0.020, 0.027), (h * 0.052, 0.014),
               (h * 0.080, 0.004)), seg=10, sy=0.88)

    # ------------------------------ pinnacolino fra i frontoni (sui piedritti)
    def _pinnacolino(xs):
        z_b = z_gb
        # mensolina, fustino con statuina e fiorone a foglie: resta sotto la
        # punta dei frontoni, come i piccoli finiali della fotografia
        _bm_box(bm_w, Mi, xs, y - 0.008, z_b + h * 0.012, w * 0.140, 0.105, h * 0.030)
        _bm_box(bm_p, Mi, xs, y - 0.004, z_b + h * 0.078, w * 0.058, 0.050, h * 0.095)
        _bm_lathe(bm_f, Mi @ Matrix.Translation((xs, y - 0.036, z_b + h * 0.038)),
                  ((0.0, w * 0.027), (h * 0.042, w * 0.022), (h * 0.068, w * 0.015)),
                  seg=8, sy=0.80)
        _bm_sfera(bm_f, Mi, xs, y - 0.036, z_b + h * 0.118, w * 0.016,
                  sx=0.9, sy=0.8, sz=1.05, u=8, v=6)
        for sl in (-1, 1):
            _bm_box(bm_w, Mi, xs + sl * w * 0.050, y - 0.008, z_b + h * 0.072,
                    w * 0.021, 0.080, h * 0.115)
        _bm_box(bm_r, Mi, xs, y - 0.010, z_b + h * 0.136, w * 0.150, 0.092, h * 0.013)
        # cupolino a foglie + bottone
        for sl in (-1, 1):
            Ml = (Mi @ Matrix.Translation((xs + sl * w * 0.028, y - 0.034,
                                           z_b + h * 0.148))
                  @ Matrix.Rotation(-sl * 0.38, 4, "Y"))
            _bm_foglia(bm_f, h * 0.085, h * 0.034, h * 0.016, Ml,
                       piega=-0.08 * sl, gonfia=1.25)
        _bm_lathe(bm_f, Mi @ Matrix.Translation((xs, y - 0.034, z_b + h * 0.150)),
                  ((0.0, w * 0.026), (h * 0.035, w * 0.030), (h * 0.075, w * 0.015),
                   (h * 0.110, 0.003)), seg=9, sy=0.88)
        # pannellino cosmatesco nella V fra i due frontoni (v2.5: piu'
        # grande e avanzato, cosi' le tessere del mosaico si leggono fra
        # le punte come le macchie chiare della fotografia)
        _bm_box(bm_c, Mi, xs, y + 0.030, z_b + h * 0.105, w * 0.285, 0.034, h * 0.215)
        _bm_box(bm_w, Mi, xs, y + 0.040, z_b + h * 0.219, w * 0.330, 0.026, h * 0.014)
        _bm_box(bm_w, Mi, xs, y + 0.040, z_b - h * 0.009, w * 0.330, 0.026, h * 0.014)

    _pinnacolino(cx + w * 0.5)
    if variant == 0:
        _pinnacolino(cx - w * 0.5)

    # i due angiolini sdraiati sul frontone centrale, sopra la Madonna
    if spec.get("gesto") == "madonna":
        for s in (-1, 1):
            p0a = (cx + s * hw_g * 0.055, y - 0.055,
                   z_apice - (z_apice - z_gb) * 0.055 + 0.030)
            p1a = (cx + s * hw_g * 0.340, y - 0.060,
                   z_apice - (z_apice - z_gb) * 0.340 + 0.034)
            _bm_segmento(bm_f, Mi, p0a, p1a, h * 0.020, h * 0.014, seg=7, sy=0.85)
            _bm_sfera(bm_f, Mi, p0a[0] + s * h * 0.006, y - 0.062, p0a[2] + h * 0.012,
                      h * 0.019, sx=0.9, sy=0.8, sz=1.0, u=9, v=6)
            Mw = (Mi @ Matrix.Translation((cx + s * hw_g * 0.13, y - 0.032,
                                           z_apice - (z_apice - z_gb) * 0.13 + 0.038))
                  @ Matrix.Rotation(-s * ang_gh, 4, "Y")
                  @ Matrix.Rotation(s * 0.7, 4, "Z"))
            _bm_foglia(bm_f, h * 0.075, h * 0.032, h * 0.012, Mw,
                       piega=0.10 * s, gonfia=1.15)

    _mesh_da_bmesh(f"{name}_Marmo_Bianco", col, bm_w, BIANCO, uv_scale=(1.1, 1.1))
    _mesh_da_bmesh(f"{name}_Marmo_Rosa", col, bm_r, ROSA, uv_scale=(1.1, 1.1))
    _mesh_da_bmesh(f"{name}_Scultura", col, bm_f, PIETRA_RIL, uv_scale=(1.4, 1.4))
    _mesh_da_bmesh(f"{name}_Incavi", col, bm_p, PATINA, uv_scale=(1.0, 1.0))
    _mesh_da_bmesh(f"{name}_Cosmatesco", col, bm_c, COSMATE, uv_scale=(2.4, 2.4))

    # ------------------------------------------------------------------- busto
    bm_b = bmesh.new()
    bm_bp = bmesh.new()
    scala_b = spec.get("scala", 1.0)
    # v2.5: in fotografia le mezze figure sono piu' strette della luce (il
    # fondale rosa si vede ai lati) ma emergono di piu' dal fondo: busto
    # ridotto in larghezza e avanzato verso la ghiera, in altorilievo.
    M_busto = (Matrix.Translation((cx + spec.get("dx", 0.0) * w, y - 0.028, z_dav - 0.004))
               @ Matrix.Rotation(spec.get("pitch", 0.0), 4, "X")
               @ Matrix.Rotation(spec.get("roll", 0.0), 4, "Y")
               @ Matrix.Diagonal((scala_b, scala_b, scala_b, 1.0)))
    _bm_busto_profeta24(bm_b, bm_bp, M_busto, op * 1.07, z_top - z_dav, spec)
    _mesh_da_bmesh(f"{name}_Busto", col, bm_b, PIETRA, uv_scale=(1.6, 1.6))
    _mesh_da_bmesh(f"{name}_Busto_Incavi", col, bm_bp, PATINA, uv_scale=(1.6, 1.6))

    # lembo del manto che scende davanti al parapetto (come in fotografia)
    drappo = spec.get("drappo", 0.0)
    if drappo > 0.05:
        bm_d = bmesh.new()
        lun = min(0.100 + 0.140 * drappo, 0.205)  # v2.5: lembi piu' lunghi sul parapetto
        lar_d = w * (0.18 + 0.28 * drappo)
        dx_d = ((variant * 37) % 5 - 2) * w * 0.045
        z_top_d = z_dav + 0.014
        # Superficie continua con due pieghe ampie e punta mossa: il tessuto
        # resta un unico lembo scolpito, senza effetto frangia.
        _bm_drappo_parapetto24(
            bm_d, Mi, cx + dx_d, y - 0.205,
            z_top_d, lar_d, lun, seed=variant,
        )
        _bm_sweep24(
            bm_d, Mi,
            ((cx + dx_d - lar_d * 0.34, y - 0.105, z_dav + 0.010),
             (cx + dx_d, y - 0.168, z_top_d + 0.006),
             (cx + dx_d + lar_d * 0.34, y - 0.105, z_dav + 0.010)),
            (0.018, 0.025, 0.018), lati=9, ellisse=0.70, campioni=4,
        )
        _mesh_da_bmesh(f"{name}_Manto_Sul_Parapetto", col, bm_d, PIETRA,
                       uv_scale=(1.6, 1.6))


def profeta_pennacchio_oculo(name, col, side, x, y, z0, h=1.55):
    """Profeta in altorilievo sul pennacchio superiore dell'oculo (v2.5: mezza
    figura grande sdraiata in diagonale sul pannello).

    Nella fotografia ai lati dell'arco del rosone NON ci sono angeli alati:
    i due pennacchi superiori sono pannelli rettangolari di marmo rosa
    venato con cornice scura, dai quali emerge un profeta a mezza figura —
    a sinistra indica il rosone col braccio teso, a destra parla con la
    mano alzata aperta e l'altra sul petto.
    """
    s = h / 1.55
    lato = -side  # il gesto e' rivolto verso il centro (il rosone)

    # pannello di marmo rosa rigato con cornice in marmo verde scuro
    # (v2.5: pannello piu' alto — in fotografia occupa quasi tutto il
    # rettangolo fra cornice della galleria ed estradosso dell'oculo)
    pan_w, pan_h = 1.58 * s, 1.58 * s
    pan_cz = z0 + 0.74 * s
    box(f"{name}_Pannello_Rosa", col, x, y + 0.145, pan_cz,
        pan_w, 0.075, pan_h, RIGATO, fit_uv=True)
    box(f"{name}_Cornice_Top", col, x, y + 0.098, pan_cz + pan_h * 0.5 + 0.021 * s,
        pan_w + 0.09 * s, 0.045, 0.045 * s, VERDE)
    box(f"{name}_Cornice_Bot", col, x, y + 0.098, pan_cz - pan_h * 0.5 - 0.021 * s,
        pan_w + 0.09 * s, 0.045, 0.045 * s, VERDE)
    for sf in (-1, 1):
        box(f"{name}_Cornice_Lat_{sf}", col, x + sf * (pan_w * 0.5 + 0.021 * s),
            y + 0.098, pan_cz, 0.045 * s, 0.045, pan_h, VERDE)

    bm = bmesh.new()
    bm_pat = bmesh.new()
    spec = dict(
        yaw=lato * 0.50,
        nod=0.14 if side < 0 else -0.02,
        gesto="indica" if side < 0 else "parla",
        barba=0.85 if side < 0 else 1.05,
        copricapo="capelli_lunghi" if side < 0 else "capelli",
        lato=lato,
        seed=3 if side < 0 else 5,
    )
    # v2.5: mezza figura GRANDE e sdraiata in diagonale sul pannello, come
    # in fotografia — testa verso l'angolo alto esterno, corpo inclinato e
    # sporto in avanti sopra la ghiera del rosone. Nella v2.4 la figura era
    # piccola, verticale e semisepolta dietro l'arco: si vedeva solo la testa.
    M = (Matrix.Translation((x - lato * 0.06 * s, y - 0.02, z0))
         @ Matrix.Rotation(0.085, 4, "X")
         @ Matrix.Rotation(side * 0.27, 4, "Y")
         @ Matrix.Diagonal((s, s, s, 1.0)))
    _bm_busto_profeta24(bm, bm_pat, M, 0.97, 1.44, spec)
    _mesh_da_bmesh(f"{name}_Marmo", col, bm, PIETRA_RIL, uv_scale=(1.3, 1.3))
    _mesh_da_bmesh(f"{name}_Incavi", col, bm_pat, PATINA, uv_scale=(1.3, 1.3))


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
# =============================================================================
# 4.4 FIGURA GOTICA A TUTTO TONDO (statue delle nicchie e del ballatoio)
# =============================================================================
def _bm_figura_gotica(bm, bm_pat, mat4, H, spec):
    """Figura gotica a figura intera: panneggio continuo, manto, braccia e volto.

    Corpo costruito a sezioni ellittiche (piede, ginocchia, bacino, cintola,
    petto, spalle) con pieghe lunghe e morbide; spalle raccordate, collo e
    testa con il volto scolpito di `_bm_testa_profeta24`.
    """
    gesto = spec.get("gesto", "libro")
    barba = spec.get("barba", 0.75)
    copricapo = spec.get("copricapo", "capelli")
    yaw = spec.get("yaw", 0.0)
    nod = spec.get("nod", 0.05)
    seed = spec.get("seed", 0)
    lato = spec.get("lato", 1)

    Z_TOP_CORPO = 0.825           # il busto si ferma alla base del collo
    Z_TESTA = 0.893
    R_TESTA = 0.068

    # profilo verticale (t, raggio_x, raggio_y) — proporzioni di statua gotica
    prof = ((0.000, 0.128, 0.100), (0.040, 0.146, 0.113), (0.140, 0.142, 0.110),
            (0.260, 0.131, 0.103), (0.400, 0.126, 0.100), (0.520, 0.128, 0.098),
            (0.610, 0.118, 0.092), (0.690, 0.130, 0.094), (0.750, 0.138, 0.092),
            (0.790, 0.118, 0.082), (0.825, 0.078, 0.070))

    def sez(t):
        t = max(prof[0][0], min(prof[-1][0], t))
        for a_, b_ in zip(prof, prof[1:]):
            if a_[0] <= t <= b_[0]:
                u = (t - a_[0]) / max(1e-6, b_[0] - a_[0])
                u = u * u * (3.0 - 2.0 * u)
                return (a_[1] * (1 - u) + b_[1] * u, a_[2] * (1 - u) + b_[2] * u)
        return (prof[-1][1], prof[-1][2])

    def spost(z_rel):
        t = max(0.0, min(1.0, z_rel / H))
        return H * (0.013 * math.sin(math.pi * t * 1.15) + 0.008 * t)

    nz, na = 40, 48
    grid = []
    for i in range(nz + 1):
        t = Z_TOP_CORPO * i / nz
        rx, ry = sez(t)
        row = []
        for j in range(na):
            a = math.tau * j / na
            piega = 0.0
            if 0.03 < t < 0.80:
                # pieghe lunghe e profonde, non una fisarmonica a passo corto
                piega = H * 0.0175 * (0.72 * math.sin(7.0 * a + 1.7 + 1.4 * t + seed)
                                      + 0.28 * math.sin(13.0 * a - 1.9 * t + 0.4 * seed))
                piega *= min(1.0, (t - 0.03) / 0.14)
            x = spost(H * t) + (rx * H + piega) * math.cos(a)
            y = -H * 0.008 * math.sin(math.pi * t * 0.85) + (ry * H + piega * 0.70) * math.sin(a)
            row.append(bm.verts.new(mat4 @ Vector((x, y, H * t))))
        grid.append(row)
    for i in range(nz):
        for j in range(na):
            j2 = (j + 1) % na
            bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
    bm.faces.new(list(reversed(grid[0])))
    bm.faces.new(grid[-1])

    # spalle raccordate al busto (niente bracci che sbucano dal tubo)
    for s_sh in (-1, 1):
        _bm_sfera(bm, mat4, spost(H * 0.772) + s_sh * 0.108 * H, 0.0, H * 0.772,
                  H * 0.050, sx=1.10, sy=0.95, sz=0.92, u=16, v=10)

    # pieghe profonde del panno: cordoni verticali sul davanti
    for k in range(7):
        a = -math.pi * 0.5 + math.pi * (0.14 + 0.72 * k / 6.0)
        punti, raggi = [], []
        for s_ in range(8):
            t = 0.05 + 0.70 * s_ / 7.0
            rx, ry = sez(t)
            piega = H * 0.0095
            x = spost(H * t) + (rx * H + piega) * math.cos(a)
            y = (ry * H + piega * 0.70) * math.sin(a)
            punti.append((x, y, H * t))
            raggi.append(H * (0.0125 - 0.005 * t))
        _bm_sweep24(bm, mat4, punti, raggi, lati=8, ellisse=0.60, campioni=2)

    # solchi d'ombra patinati fra le pieghe: e' cio' che fa leggere il panno
    for k in range(6):
        a = -math.pi * 0.5 + math.pi * (0.20 + 0.62 * k / 5.0)
        punti = []
        for s_ in range(8):
            t = 0.04 + 0.72 * s_ / 7.0
            rx, ry = sez(t)
            piega = -H * 0.0075 * min(1.0, max(0.0, (abs(math.sin(5.0 * a + 1.7 + 1.4 * t + seed)) - 0.4)))
            punti.append((spost(H * t) + (rx * H + piega) * math.cos(a),
                          (ry * H + piega * 0.70) * math.sin(a), H * t))
        _bm_sweep24(bm_pat, mat4, punti, [H * 0.0075] * len(punti),
                    lati=6, ellisse=0.55, campioni=2)

    # --- PANNO: il mantello e' una seconda pelle che si appoggia al corpo e
    # si fonde con esso ai bordi (niente lastre sporgenti): il rilievo nasce
    # dalle onde del tessuto e dallo spessore che va a zero sugli orli.
    # due pieghe-cordone del manto che scendono di traverso sul petto
    for k_m, (a_s, a_e, t_s, t_e, sp) in enumerate((
        (-0.45, 1.95, 0.800, 0.410, 0.016),
        (0.55, 2.75, 0.795, 0.140, 0.019),
    )):
        pts, rad = [], []
        for i in range(9):
            u = i / 8.0
            t = t_s + (t_e - t_s) * u
            a = (a_s + (a_e - a_s) * u) * lato
            rx, ry = sez(t)
            pts.append((spost(H * t) + (rx * H + sp * H) * math.cos(a),
                        (ry * H + sp * H * 0.8) * math.sin(a), H * t))
            rad.append(H * 0.0175 * (0.55 + 0.60 * math.sin(math.pi * (0.15 + 0.85 * u))))
        _bm_sweep24(bm, mat4, pts, rad, lati=10, ellisse=0.55, campioni=2)

    # cintola con nodo
    rx_c, ry_c = sez(0.415)
    _bm_sweep24(bm, mat4,
                [(spost(H * 0.415) + (rx_c * H + 0.006 * H) * math.cos(math.tau * k / 22),
                  (ry_c * H + 0.005 * H) * math.sin(math.tau * k / 22), H * 0.415) for k in range(23)],
                [H * 0.0115] * 23, lati=9, ellisse=0.60, campioni=1)
    _bm_sfera(bm, mat4, spost(H * 0.415) + 0.010 * H, -ry_c * H - 0.004 * H, H * 0.412,
              H * 0.018, sx=1.10, sy=0.55, sz=0.70, u=12, v=8)
    # due lembi che scendono dal nodo (mosci, non rigidi)
    for s_l in (-1, 1):
        _bm_sweep24(bm, mat4,
                    ((spost(H * 0.412) + 0.012 * H, -ry_c * H - 0.010 * H, H * 0.405),
                     (spost(H * 0.36) + s_l * 0.026 * H, -ry_c * H - 0.016 * H, H * 0.345),
                     (spost(H * 0.30) + s_l * 0.034 * H, -ry_c * H - 0.010 * H, H * 0.275),
                     (spost(H * 0.25) + s_l * 0.020 * H, -ry_c * H - 0.018 * H, H * 0.225)),
                    (H * 0.020, H * 0.022, H * 0.018, H * 0.010), lati=9,
                    ellisse=0.45, rughe=0.06, campioni=3)

    # ---- braccia ----
    W = 0.46 * H                    # larghezza di riferimento per mani e libro
    z_sh = 0.775 * H
    y_sh = -0.004 * H

    def braccio(s, gomito, polso, r=1.0, modo="grip", direzione=None):
        spalla = (spost(z_sh) + s * 0.140 * H, y_sh, z_sh)
        g = (gomito[0], gomito[1], gomito[2])
        p = (polso[0], polso[1], polso[2])
        medio = (0.5 * (spalla[0] + g[0]), 0.5 * (spalla[1] + g[1]) - 0.006 * H,
                 0.5 * (spalla[2] + g[2]))
        _bm_sweep24(bm, mat4, (spalla, medio, g, p),
                    (0.054 * H * r, 0.046 * H * r, 0.036 * H * r, 0.021 * H * r),
                    lati=14, ellisse=0.86, rughe=0.040, campioni=4)
        # polsino rovesciato della manica: raccorda il braccio alla mano
        d_p = (Vector(p) - Vector(g)).normalized()
        _bm_sweep24(bm, mat4, (tuple(Vector(p) - d_p * 0.030 * H), tuple(Vector(p) + d_p * 0.006 * H)),
                    (0.030 * H * r, 0.024 * H * r), lati=12, ellisse=0.86, campioni=2)
        d = (Vector(p) - Vector(g))
        _bm_mano24(bm, mat4, W, p,
                   direzione if direzione is not None else (d.x, d.y, d.z),
                   modo=modo, lato=s)

    z_mano = 0.600 * H
    if gesto == "libro":
        braccio(1, (0.150 * H, -0.055 * H, z_mano + 0.02 * H), (0.052 * H, -0.108 * H, z_mano), 0.90)
        braccio(-1, (-0.150 * H, -0.055 * H, z_mano + 0.02 * H), (-0.052 * H, -0.108 * H, z_mano), 0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.108 * H, z_mano), True, lato, 1.15)
    elif gesto == "leggi":
        z_mano = 0.655 * H
        braccio(1, (0.150 * H, -0.060 * H, z_mano - 0.02 * H), (0.040 * H, -0.112 * H, z_mano), 0.90)
        braccio(-1, (-0.150 * H, -0.060 * H, z_mano - 0.02 * H), (-0.040 * H, -0.112 * H, z_mano), 0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.112 * H, z_mano), True, lato, 1.15)
    elif gesto == "croce":
        braccio(lato, (lato * 0.155 * H, -0.045 * H, 0.660 * H),
                (lato * 0.130 * H, -0.092 * H, 0.745 * H), 0.88)
        braccio(-lato, (-lato * 0.150 * H, -0.055 * H, 0.590 * H),
                (-lato * 0.045 * H, -0.108 * H, 0.545 * H), 0.90)
        _bm_sweep24(bm, mat4, ((lato * 0.130 * H, -0.100 * H, 0.690 * H),
                               (lato * 0.130 * H, -0.104 * H, 0.905 * H)),
                    (0.010 * H, 0.008 * H), lati=8, campioni=2)
        _bm_box(bm, mat4 @ Matrix.Translation((lato * 0.130 * H, -0.106 * H, 0.875 * H)),
                0.0, 0.0, 0.0, 0.086 * H, 0.011 * H, 0.020 * H)
        _bm_libro24(bm, bm_pat, mat4, W, H, (-lato * 0.030 * H, -0.100 * H, 0.545 * H), False, lato, 0.85)
    elif gesto == "benedicente":
        braccio(lato, (lato * 0.160 * H, -0.040 * H, 0.660 * H),
                (lato * 0.180 * H, -0.080 * H, 0.845 * H), 0.86,
                modo="aperta", direzione=(lato * 0.32, -0.10, 1.0))
        braccio(-lato, (-lato * 0.150 * H, -0.055 * H, 0.585 * H),
                (-lato * 0.048 * H, -0.105 * H, 0.545 * H), 0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (-lato * 0.020 * H, -0.125 * H, 0.545 * H),
                    False, lato, 0.80)
    else:  # "petto"
        braccio(lato, (lato * 0.155 * H, -0.040 * H, 0.630 * H),
                (0.0, -0.100 * H, 0.700 * H), 0.88, modo="aperta",
                direzione=(-lato * 0.5, -0.2, 0.9))
        braccio(-lato, (-lato * 0.150 * H, -0.055 * H, 0.580 * H),
                (-lato * 0.050 * H, -0.105 * H, 0.520 * H), 0.90)

    # ---- collo, testa e volto ----
    z_head = Z_TESTA * H
    r_h = R_TESTA * H
    x_h = spost(z_head)
    _bm_sweep24(bm, mat4,
                ((spost(0.80 * H), -0.006 * H, 0.795 * H),
                 (x_h * 0.85, -0.014 * H, 0.845 * H),
                 (x_h, -0.020 * H, z_head - r_h * 0.80)),
                (0.050 * H, 0.042 * H, r_h * 0.72), lati=16, ellisse=0.88, campioni=4)
    Mh = (mat4 @ Matrix.Translation((x_h, -0.018 * H, z_head))
          @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Rotation(nod, 4, "X"))
    _bm_testa_profeta24(bm, bm_pat, Mh, r_h, yaw * 0.35, nod * 0.5, barba, copricapo, seed)


def statua_gotica_v26(name, col, x, y, z, h, spec=None, material=None):
    """Statua gotica completa (piedistallo, figura, incavi patinati)."""
    spec = spec or {}
    bm = bmesh.new()
    bm_pat = bmesh.new()
    M = (Matrix.Translation((x, y, z))
         @ Matrix.Rotation(spec.get("rot_z", 0.0), 4, "Z")
         @ Matrix.Diagonal((h, h, h, 1.0)))
    # piedistallo
    _bm_box(bm, Matrix.Translation((x, y + 0.01, z + 0.022 * h)),
            0.0, 0.0, 0.0, 0.30 * h, 0.24 * h, 0.045 * h)
    _bm_figura_gotica(bm, bm_pat,
                      Matrix.Translation((x, y, z)) @ Matrix.Rotation(spec.get("rot_z", 0.0), 4, "Z")
                      @ Matrix.Diagonal((h, h, h, 1.0)),
                      1.0, spec)
    _mesh_da_bmesh(f"{name}_Marmo", col, bm, material or PIETRA_RIL, uv_scale=(0.9, 0.9))
    _mesh_da_bmesh(f"{name}_Incavi", col, bm_pat, PATINA, uv_scale=(0.9, 0.9))



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
            arco_ritorto(f"Archivolto_{tag}_{idx}", P, cx, front + dy - 0.42, cz_arch, rr, min_r, mat_a)
        else:
            arch(f"Archivolto_{tag}_{idx}", P, cx, front + dy - 0.42, cz_arch, rr, min_r, mat_a, seg_u=38)
    # Fasce scolpite: rosette separate, non una superficie liscia continua.
    for band, rr in enumerate((r_in + 0.42, r_in + 1.12)):
        for k in range(29):
            a = math.pi * (k + 0.5) / 29
            rosetta_rilievo(f"Fogliame_Archivolto_{tag}_{band}_{k}", P,
                           cx + rr * math.cos(a), front - 0.94,
                           cz_arch + rr * math.sin(a), 0.115, petals=5)
    # Chiave di volta scolpita
    sphere(f"Chiave_Volta_{tag}", P, cx, front - 0.94, cz_arch + r_ext - 0.05, 0.22, PIETRA)

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

    # Tralci nei due pennacchi, sopra l'estradosso e dentro gli spioventi.
    for side in (-1, 1):
        for row in range(4):
            t = 0.38 + row * 0.12
            xx = cx + side * gh_w * 0.32 * (1.0 - t)
            zz = gh_base + gh_h * t
            if math.hypot(xx - cx, zz - cz_arch) > r_ext + 0.16:
                rosetta_rilievo(f"Tralcio_Ghimberga_{tag}_{side}_{row}",
                               P, xx, -1.91, zz, 0.25)
    spioventi_modanati(f"Ghimberga_ListelloInterno_{tag}", P, cx, -1.94,
                       gh_base + 0.30, gh_w * 0.85, gh_h * 0.85,
                       0.065, 0.10, PIETRA)

    # Medaglione circolare scolpito col busto a mezz'altezza della ghimberga
    z_med = gh_base + gh_h * 0.56
    torus(f"Medaglione_Cornice_{tag}", P, cx, -1.78, z_med, 0.56, 0.11, BIANCO)
    cyl(f"Medaglione_Fondo_{tag}", P, cx, -1.76, z_med, 0.50, 0.08, ROSA_C, vertices=24, rot_x=math.radians(90))
    cone(f"Medaglione_Busto_{tag}", P, cx, -1.83, z_med - 0.12, 0.24, 0.14, 0.38, PIETRA, vertices=10)
    sphere(f"Medaglione_Testa_{tag}", P, cx, -1.84, z_med + 0.16, 0.15, PIETRA)

    # Statua di coronamento sul vertice della ghimberga.
    # v2.6: al centro e' il Redentore che si staglia davanti al vetro del rosone,
    # come in fotografia — figura intera panneggiata, benedizione con la destra,
    # libro nella sinistra.
    if central:
        box("Piedistallo_Redentore", ST, cx, -1.66, gh_apex + 0.10, 0.46, 0.34, 0.20, BIANCO2)
        statua_gotica_v26(
            "Statua_Redentore_Oculo", ST, cx, -1.70, gh_apex + 0.20, 1.78,
            spec=dict(gesto="benedicente", barba=0.95, copricapo="capelli_lunghi",
                      yaw=0.0, nod=0.02, seed=11, lato=1, rot_z=0.0),
        )
    else:
        statua_gotica_v26(
            f"Statua_Apice_Ghimberga_{tag}", ST, cx, -1.70, gh_apex + 0.02, 1.42,
            spec=dict(gesto="libro", barba=0.7, copricapo="capelli",
                      yaw=0.0, nod=0.04,
                      seed=13, lato=1),
        )


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
# 4. REGISTRO SUPERIORE CENTRALE — IL ROSONE DI CAMAINO (v2.6)
#
#   Rilettura integrale della zona della vetrata sulla fotografia di dettaglio
#   `riferimento_vetrata.jpg`:
#
#   1. Vetrata cattedrale vera: lastra lattiginosa azzurro-verde con
#      nuvolature, letta dalla fotografia; piombatura sottile con due montanti
#      per lato e cinque traversi, giusto il reticolo dell'originale (prima era
#      un disco scuro con una griglia grossolana e un anello dorato sbagliato
#      che girava *dentro* il vetro).
#   2. Strombatura profonda in ombra e ghiera larga quasi il doppio: girali
#      d'acanto alternati, corda intrecciata oro/avorio, fili modanati e
#      mosaico aureo al bordo del vetro — la corona scolpita che in fotografia
#      occupa un terzo del raggio.
#   3. Quattro profeti sui pennacchi: i due in alto sdraiati in diagonale con
#      il braccio teso verso l'oculo, i due in basso ritti e rivolti al centro.
#   4. Quattro nicchie gotiche per lato con statue a figura intera (prima
#      cinque nicchiette con statuine-pedina), e la fascia di quatrifogli
#      riportata sui pilastri dove sta davvero.
# =============================================================================

# --- 4.0 Parametri del rosone ------------------------------------------------
Z_PAN = Z_OCULO - 0.45                 # centro del pannello quadrato
PAN_HW, PAN_HH = 4.30, 3.55            # semiassi del pannello
GH_OUT_RX = RX_OCULO + 0.62            # filo esterno della ghiera
GH_OUT_RZ = RZ_OCULO + 0.50
Y_PARETE = -1.58                       # piano del pannello di marmo rigato
Y_GHIERA = -1.72                       # risalto massimo della ghiera
Y_VETRO = -1.10                        # fondo della strombatura
SGUINCIO = MATS.get("Sguincio_Oculo", ROSA)
ORO_MOS = MATS.get("Braccio_Oro_Mosaico", ORO)


def disco_vetro(name, col, cx, y, cz, rx, rz, material, seg=128, anelli=9, tile=2.3):
    """Vetro piano con UV ripetute: la texture cattedrale si affaccia in lastre."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.verify()
    centro = bm.verts.new((0.0, 0.0, 0.0))
    fasce = []
    for i in range(1, anelli + 1):
        f = i / anelli
        row = []
        for j in range(seg):
            a = math.tau * j / seg
            row.append(bm.verts.new((rx * f * math.cos(a), 0.0, rz * f * math.sin(a))))
        fasce.append(row)

    def _uv(co):
        return (0.5 + 0.5 * tile * (co.x / rx), 0.5 + 0.5 * tile * (co.z / rz))

    facce = []
    r0 = fasce[0]
    for j in range(seg):
        facce.append(bm.faces.new((centro, r0[j], r0[(j + 1) % seg])))
    for i in range(anelli - 1):
        ra, rb = fasce[i], fasce[i + 1]
        for j in range(seg):
            j2 = (j + 1) % seg
            facce.append(bm.faces.new((ra[j], rb[j], rb[j2], ra[j2])))
    for f in facce:
        for loop in f.loops:
            loop[uv].uv = _uv(loop.vert.co)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (cx, y, cz), (0, 0, 0), (1, 1, 1), material)


def anello_strombato(name, col, cz, y_out, y_in, rx_out, rz_out, rx_in, rz_in,
                     material, seg=128):
    """Superficie troncoconica della strombatura (sguincio) del rosone."""
    bm = bmesh.new()
    uv = bm.loops.layers.uv.verify()
    ext, inn = [], []
    for j in range(seg):
        a = math.tau * j / seg
        ext.append(bm.verts.new((rx_out * math.cos(a), y_out, cz + rz_out * math.sin(a))))
        inn.append(bm.verts.new((rx_in * math.cos(a), y_in, cz + rz_in * math.sin(a))))
    for j in range(seg):
        j2 = (j + 1) % seg
        f = bm.faces.new((ext[j], ext[j2], inn[j2], inn[j]))
        for k, loop in enumerate(f.loops):
            loop[uv].uv = ((j + (1 if k in (1, 2) else 0)) / seg * 7.0,
                           0.0 if k < 2 else 0.55)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (0.0, 0.0, 0.0), (0, 0, 0), (1, 1, 1), material)


def _mat_arco(a, rx, rz, cz, y):
    """Matrice di un elemento appoggiato sull'ellisse del rosone: +Z = normale."""
    return (Matrix.Translation((rx * math.cos(a), y, cz + rz * math.sin(a)))
            @ Matrix.Rotation(math.pi / 2 - a, 4, "Y"))


# =============================================================================
# 4.1 PANNELLO QUADRATO IN MARMO RIGATO + CORNICE VERDE
# =============================================================================
IN_W, IN_H = PAN_HW, PAN_HH
lastra_forata_oculo(
    "Oculo_Quadro_Pennacchi", R, 0.0, -1.36, Z_PAN,
    PAN_HW, PAN_HH, RX_OCULO + 0.02, RZ_OCULO + 0.02, 0.44, RIGATO
)
# Cornice di marmo verde con filo bianco attorno al quadro (in fotografia il
# pannello rosa e' chiuso da una fascia scura continua su tutti e quattro i lati).
for _s in (-1, 1):
    box(f"Cornice_Quadro_Orizz_{_s:+d}", R, 0.0, -1.575,
        Z_PAN + _s * (PAN_HH + 0.085), PAN_HW * 2.0 + 0.42, 0.115, 0.17, VERDE)
    box(f"Cornice_Quadro_Vert_{_s:+d}", R, _s * (PAN_HW + 0.085), -1.575,
        Z_PAN, 0.17, 0.115, PAN_HH * 2.0 + 0.42, VERDE)
    box(f"Cornice_Quadro_Filo_Orizz_{_s:+d}", R, 0.0, -1.625,
        Z_PAN + _s * (PAN_HH + 0.185), PAN_HW * 2.0 + 0.34, 0.075, 0.045, BIANCO)
    box(f"Cornice_Quadro_Filo_Vert_{_s:+d}", R, _s * (PAN_HW + 0.185), -1.625,
        Z_PAN, 0.045, 0.075, PAN_HH * 2.0 + 0.34, BIANCO)

# =============================================================================
# 4.2 VETRATA: LA LASTRA, LA PIOMBATURA E IL TELAIO
# =============================================================================
disco_vetro("Oculo_Vetro", R, 0.0, Y_VETRO, Z_OCULO,
            RX_OCULO, RZ_OCULO, VETRO, seg=132, anelli=10, tile=1.0)
# Fondo opaco dietro il vetro: nessun cielo che filtra dalle fughe.
box("Oculo_Fondo_Opaco", R, 0.0, -0.62, Z_OCULO, RX_OCULO * 2.05, 0.10,
    RZ_OCULO * 2.05, SCURO)

# Piombatura: due montanti per lato e cinque traversi, sezione sottile come
# nell'originale (barre di ferro piatto, non tubi neri spessi).
BARRA_HW = 0.042
# due soli montanti verticali interni (a un terzo del raggio), come in fotografia
for _x in (-RX_OCULO * 0.335, RX_OCULO * 0.335):
    _hh = RZ_OCULO * math.sqrt(max(0.0, 1.0 - (_x / RX_OCULO) ** 2)) - 0.02
    box(f"Piombo_Vert_{_x:+.2f}", R, _x, -1.068, Z_OCULO,
        BARRA_HW * 2.0, 0.050, 2.0 * _hh, FERRO)
    box(f"Piombo_Vert_Filo_{_x:+.2f}", R, _x + BARRA_HW * 2.4, -1.085, Z_OCULO,
        BARRA_HW * 0.55, 0.030, 2.0 * _hh * 0.995, FERRO)
# cinque traversi orizzontali, equidistanti
for _k in range(-2, 3):
    _dz = _k * RZ_OCULO * 0.335
    _ww = RX_OCULO * math.sqrt(max(0.0, 1.0 - (_dz / RZ_OCULO) ** 2)) - 0.02
    box(f"Piombo_Orizz_{_k:+d}", R, 0.0, -1.068, Z_OCULO + _dz,
        2.0 * _ww, 0.050, BARRA_HW * 2.0, FERRO)
    box(f"Piombo_Orizz_Filo_{_k:+d}", R, 0.0, -1.085, Z_OCULO + _dz + BARRA_HW * 2.4,
        2.0 * _ww * 0.995, 0.030, BARRA_HW * 0.55, FERRO)
# Telaio di piombo perimetrale (la ghiera del vetro, sottile e scura)
torus_ellipse("Piombo_Filo_Perimetrale", R, 0.0, -1.083, Z_OCULO,
              RX_OCULO - 0.02, RZ_OCULO - 0.02, 0.036, FERRO, seg_u=120, seg_v=8)

# Strombatura in ombra fra il filo della ghiera e il vetro
anello_strombato("Oculo_Strombatura", R, Z_OCULO, -1.545, Y_VETRO + 0.02,
                 RX_OCULO + 0.085, RZ_OCULO + 0.085,
                 RX_OCULO + 0.005, RZ_OCULO + 0.005, SGUINCIO, seg=128)

# =============================================================================
# 4.3 GHIERA SCOLPITA: ORLO MODANATO, PERLE, FOGLIAME D'ACANTO CORRENTE,
#     CORDA INTRECCIATA ORO/AVORIO E MOSAICO AUREO SUL BORDO DEL VETRO
#
#     In fotografia la ghiera non e' un anello di borchie: e' una fascia larga
#     con fogliame d'acanto che CORRE lungo la circonferenza (non sporge a
#     raggiera), una corda intrecciata oro/avorio e un orlo modanato esterno.
# =============================================================================
def _telaio_arco(a, rx, rz, cz, y, tilt=0.0, incl=0.0):
    """Matrice locale su un punto dell'ellisse del rosone.

    Z locale = direzione della foglia (tangente all'arco, inclinata di `incl`
    verso l'esterno); Y locale = normale uscente (spessore del rilievo);
    X locale = larghezza della foglia. Cosi' il fogliame giace SULLA fascia e
    corre lungo di essa, come nell'intaglio originale.
    """
    ca, sa = math.cos(a), math.sin(a)
    P = Vector((rx * ca, y, cz + rz * sa))
    n = Vector((ca / max(rx, 1e-5), 0.0, sa / max(rz, 1e-5))).normalized()
    t = Vector((-sa * rx, 0.0, ca * rz)).normalized()
    d = (t * math.cos(tilt) + n * math.sin(incl)).normalized()
    yc = n
    xc = yc.cross(d).normalized()
    yc = d.cross(xc).normalized()
    M = Matrix(((xc.x, yc.x, d.x, P.x),
                (xc.y, yc.y, d.y, P.y),
                (xc.z, yc.z, d.z, P.z),
                (0.0, 0.0, 0.0, 1.0)))
    return M


# Mosaico aureo sul bordo del vetro: tessere d'oro e d'avorio alternate
_bm_oro_a = bmesh.new()
_bm_oro_b = bmesh.new()
for k in range(184):
    a = math.tau * (k + 0.5) / 184
    M_o = _telaio_arco(a, RX_OCULO + 0.050, RZ_OCULO + 0.050, Z_OCULO, -1.152)
    bm_t = _bm_oro_a if k % 2 == 0 else _bm_oro_b
    _bm_box(bm_t, M_o @ Matrix.Translation((0.0, 0.016, 0.0))
            @ Matrix.Rotation(0.55 if k % 4 < 2 else -0.55, 4, "Z"),
            0.0, 0.0, 0.0, 0.064, 0.032, 0.042)
_mesh_da_bmesh("Oculo_Mosaico_Oro", R, _bm_oro_a, ORO_MOS)
_mesh_da_bmesh("Oculo_Mosaico_Avorio", R, _bm_oro_b, BIANCO2)

# orlo esterno modanato (grosso toro) e fondo rosa della fascia
torus_ellipse("Ghiera_Filo_Esterno", R, 0.0, Y_GHIERA + 0.030, Z_OCULO,
              GH_OUT_RX, GH_OUT_RZ, 0.105, BIANCO, seg_u=132, seg_v=14)
torus_ellipse("Ghiera_Filo_Esterno_Interno", R, 0.0, Y_GHIERA - 0.020, Z_OCULO,
              GH_OUT_RX - 0.108, GH_OUT_RZ - 0.095, 0.036, BIANCO2, seg_u=132, seg_v=8)
torus_ellipse("Ghiera_Fondo_Rosa", R, 0.0, Y_PARETE - 0.045, Z_OCULO,
              GH_OUT_RX - 0.075, GH_OUT_RZ - 0.065, 0.150, ROSA, seg_u=132, seg_v=10)
# gola in ombra subito dentro l'orlo (da' profondita' alla fascia)
torus_ellipse("Ghiera_Gola_Ombra", R, 0.0, Y_PARETE + 0.02, Z_OCULO,
              GH_OUT_RX - 0.150, GH_OUT_RZ - 0.130, 0.055, SGUINCIO, seg_u=132, seg_v=8)

# filo di perle appoggiato sul fondo rosa, sotto l'orlo
_bm_gh_perle = bmesh.new()
for k in range(196):
    a = math.tau * (k + 0.5) / 196
    Mp = _telaio_arco(a, GH_OUT_RX - 0.205, GH_OUT_RZ - 0.178, Z_OCULO, Y_PARETE - 0.055)
    _bm_sfera(_bm_gh_perle, Mp @ Matrix.Translation((0.0, 0.055, 0.0)),
              0.0, 0.0, 0.0, 0.032, sx=1.0, sy=0.75, sz=1.0, u=8, v=5)
_mesh_da_bmesh("Ghiera_Perlinatura", R, _bm_gh_perle, BIANCO, uv_scale=(1.0, 1.0))

# --- fogliame d'acanto corrente: due ordini sfalsati che corrono lungo l'arco
N_FOGLIE = 112
_bm_foglie_a = bmesh.new()
_bm_foglie_b = bmesh.new()
_bm_volute = bmesh.new()
for k in range(N_FOGLIE):
    a = math.tau * (k + 0.5) / N_FOGLIE
    tilt = 0.42 if k % 2 == 0 else -0.42
    for riga, (dr_r, dr_z, lun, lar, bm_t, incl) in enumerate((
        (0.520, 0.462, 0.300, 0.160, _bm_foglie_a, 0.30),
        (0.355, 0.315, 0.250, 0.140, _bm_foglie_b, 0.34),
    )):
        aa = a + (0.5 * math.tau / N_FOGLIE if riga else 0.0)
        M_g = _telaio_arco(aa, GH_OUT_RX - dr_r, GH_OUT_RZ - dr_z, Z_OCULO,
                           Y_PARETE - 0.02, tilt=tilt, incl=incl)
        _bm_foglia(
            bm_t, lun, lar, 0.080,
            M_g @ Matrix.Translation((0.0, 0.014, -lun * 0.42)),
            profilo=((0.0, 0.16), (0.14, 0.42), (0.32, 0.52), (0.52, 0.50),
                     (0.72, 0.38), (0.88, 0.22), (1.0, 0.04)),
            piega=0.22 * (1 if tilt > 0 else -1), gonfia=1.15,
        )
        # occhio della voluta all'attacco della foglia
        _bm_sfera(_bm_volute, M_g @ Matrix.Translation((0.0, 0.045, -lun * 0.40)),
                  0.0, 0.0, 0.0, 0.048, sx=1.15, sy=0.60, sz=1.15, u=10, v=6)
_mesh_da_bmesh("Ghiera_Fogliame_Esterno", R, _bm_foglie_a, PIETRA_RIL)
_mesh_da_bmesh("Ghiera_Fogliame_Interno", R, _bm_foglie_b, PIETRA_RIL)
_mesh_da_bmesh("Ghiera_Occhi_Volute", R, _bm_volute, BIANCO2)

# --- seconda fascia: corda intrecciata oro/avorio (treccia fitta a due capi)
torus_ellipse("Ghiera_Filo_Rosa_Interno", R, 0.0, Y_GHIERA + 0.055, Z_OCULO,
              RX_OCULO + 0.360, RZ_OCULO + 0.318, 0.070, ROSA, seg_u=132, seg_v=10)
_bm_corda_avorio = bmesh.new()
_bm_corda_oro = bmesh.new()
N_CORDA = 132
for k in range(N_CORDA):
    a = math.tau * (k + 0.5) / N_CORDA
    tilt = 0.70 if k % 2 == 0 else -0.70
    Mc = _telaio_arco(a, RX_OCULO + 0.262, RZ_OCULO + 0.232, Z_OCULO,
                      Y_GHIERA + 0.030, tilt=tilt, incl=0.16)
    _bm_box(_bm_corda_avorio if k % 2 == 0 else _bm_corda_oro,
            Mc @ Matrix.Translation((0.0, 0.012, 0.0)),
            0.0, 0.0, 0.0, 0.120, 0.072, 0.040)
_mesh_da_bmesh("Ghiera_Corda_Avorio", R, _bm_corda_avorio, BIANCO2)
_mesh_da_bmesh("Ghiera_Corda_Oro", R, _bm_corda_oro, ORO_MOS)

# --- orli modanati interno ed esterno della corda
torus_ellipse("Ghiera_Filo_Sopra_Corda", R, 0.0, Y_GHIERA + 0.085, Z_OCULO,
              RX_OCULO + 0.352, RZ_OCULO + 0.312, 0.030, BIANCO, seg_u=132, seg_v=8)
torus_ellipse("Ghiera_Filo_Interno", R, 0.0, Y_GHIERA + 0.085, Z_OCULO,
              RX_OCULO + 0.170, RZ_OCULO + 0.152, 0.044, BIANCO2, seg_u=132, seg_v=8)
# mosaico aureo a tessere sul bordo del vetro + filo di raccordo alla strombatura
torus_ellipse("Ghiera_Filo_Sotto_Strombatura", R, 0.0, -1.545, Z_OCULO,
              RX_OCULO + 0.105, RZ_OCULO + 0.100, 0.030, BIANCO2, seg_u=132, seg_v=8)

def edicola_v26(name, col, cx, y, z0, w, h, material_statua=None):
    """Edicola gotica senese: incasso in marmo rigato, pilastrini, arco acuto
    con ghiera, ghimberga a gattoni e fiorone. Nessun pannello nero: il vano
    e' chiaro e la profondita' nasce dalla geometria."""
    z_fondo = y + 0.12
    # vano: fondale rigato, spallette e catino
    box(f"{name}_Fondo", R, cx, z_fondo, z0 + h * 0.48, w * 0.90, 0.10, h * 0.92, RIGATO, fit_uv=True)
    box(f"{name}_Soglia", R, cx, y - 0.02, z0 + 0.028, w * 1.02, 0.20, 0.056, BIANCO2)
    # pilastrini laterali con capitello a fasce
    for sd in (-1, 1):
        box(f"{name}_Piedritto_{sd:+d}", R, cx + sd * w * 0.475, y - 0.05,
            z0 + h * 0.46, w * 0.095, 0.16, h * 0.90, BIANCO2)
        box(f"{name}_Capitello_{sd:+d}", R, cx + sd * w * 0.475, y - 0.075,
            z0 + h * 0.615, w * 0.145, 0.20, 0.062, BIANCO)
        for k_c in range(2):
            box(f"{name}_Collarino_{sd:+d}_{k_c}", R, cx + sd * w * 0.475, y - 0.085,
                z0 + h * (0.645 + 0.028 * k_c), w * 0.125, 0.19, 0.018, PIETRA_RIL)
    # arco acuto a due ghiere
    _bm_n = bmesh.new()
    _bm_arco_acuto(_bm_n, Matrix.Identity(4), cx, y - 0.055, z0 + h * 0.60,
                   w * 0.86, h * 0.30, w * 0.052, seg_u=18, seg_v=7)
    _bm_arco_acuto(_bm_n, Matrix.Identity(4), cx, y - 0.030, z0 + h * 0.605,
                   w * 0.72, h * 0.245, w * 0.030, seg_u=16, seg_v=6)
    _mesh_da_bmesh(f"{name}_Arco", R, _bm_n, BIANCO)

    # ghimberga con gattoni e fiorone
    gh_w, gh_h = w * 1.04, h * 0.34
    gh_z0 = z0 + h * 0.70
    prism(f"{name}_Ghimberga", R, cx, y - 0.10, gh_z0, gh_w * 0.86, gh_h, 0.15, BIANCO2)
    bm_g = bmesh.new()
    ang = math.atan2(gh_h, gh_w * 0.5)
    sl = math.hypot(gh_w * 0.5, gh_h) + 0.03
    for sd in (-1, 1):
        _bm_box(bm_g, Matrix.Identity(4), cx + sd * gh_w * 0.25, y - 0.12,
                gh_z0 + gh_h * 0.5, sl, 0.13, 0.055, rot=Matrix.Rotation(sd * ang, 4, "Y"))
        for k_c in range(4):
            tc = 0.18 + 0.62 * k_c / 3.0
            _bm_foglia(
                bm_g, 0.125, 0.062, 0.036,
                Matrix.Translation((cx + sd * gh_w * 0.5 * (1.0 - tc), y - 0.135,
                                    gh_z0 + gh_h * tc + 0.02))
                @ Matrix.Rotation(sd * 0.45, 4, "Y"),
                piega=-0.12 * sd,
            )
    _bm_lathe(bm_g, Matrix.Translation((cx, y - 0.13, gh_z0 + gh_h)),
              ((0.0, 0.040), (0.075, 0.055), (0.17, 0.018)), seg=8, sy=0.85)
    _mesh_da_bmesh(f"{name}_Ghimberga_Dettagli", R, bm_g, PIETRA_RIL)

    # specchietto con quatrifoglio alla base, fra i piedritti
    torus(f"{name}_Rosetta", R, cx, y - 0.145, z0 + h * 0.055, 0.055, 0.014, BIANCO)


# =============================================================================
# 4.5 I QUATTRO PROFETI DEI PENNACCHI
# =============================================================================
def profeta_pennacchio_v26(name, col, side, x, z_centro, w=1.30, h=1.72, alto=True):
    """Profeta in altorilievo sul pennacchio del rosone.

    In fotografia i due pennacchi superiori hanno mezze figure sdraiate in
    diagonale col braccio teso verso l'oculo; i due inferiori figure ritte,
    rivolte al centro. Tutti emergono da un pannello di marmo rigato con
    cornice verde.
    """
    y_pan = Y_PARETE - 0.045
    box(f"{name}_Pannello", col, x, y_pan + 0.085, z_centro, w, 0.09, h, RIGATO, fit_uv=True)
    # cornice in marmo verde con filo bianco, come i pannelli della fotografia
    for _s in (-1, 1):
        box(f"{name}_Cornice_H_{_s:+d}", col, x, y_pan + 0.030,
            z_centro + _s * (h * 0.5 + 0.040), w + 0.14, 0.075, 0.062, PIETRA_RIL)
        box(f"{name}_Cornice_V_{_s:+d}", col, x + _s * (w * 0.5 + 0.040), y_pan + 0.030,
            z_centro, 0.062, 0.075, h + 0.02, PIETRA_RIL)
        box(f"{name}_Filo_H_{_s:+d}", col, x, y_pan + 0.010,
            z_centro + _s * (h * 0.5 + 0.078), w + 0.09, 0.045, 0.020, VERDE)
        box(f"{name}_Filo_V_{_s:+d}", col, x + _s * (w * 0.5 + 0.078), y_pan + 0.010,
            z_centro, 0.020, 0.045, h + 0.02, VERDE)

    bm = bmesh.new()
    bm_pat = bmesh.new()
    if alto:
        lato = -side  # gesto verso il centro (il rosone)
        spec = dict(yaw=lato * 0.52, nod=0.16, gesto="indica",
                    barba=0.9, copricapo="capelli_lunghi", lato=lato,
                    seed=3 if side < 0 else 5)
        s = h / 1.72
        M = (Matrix.Translation((x - lato * 0.03 * s, y_pan + 0.02, z_centro - h * 0.40))
             @ Matrix.Rotation(0.12, 4, "X")
             @ Matrix.Rotation(side * 0.22, 4, "Y")
             @ Matrix.Diagonal((0.78 * s, 0.78 * s, 0.78 * s, 1.0)))
        _bm_busto_profeta24(bm, bm_pat, M, 1.00, 1.50, spec)
    else:
        lato = -side
        spec = dict(yaw=lato * 0.22, nod=0.06,
                    gesto="libro" if side < 0 else "leggi",
                    barba=1.05, copricapo="capelli", lato=lato,
                    seed=7 if side < 0 else 9)
        s = h / 1.72
        M = (Matrix.Translation((x, y_pan + 0.02, z_centro - h * 0.42))
             @ Matrix.Rotation(side * 0.08, 4, "Y")
             @ Matrix.Diagonal((0.80 * s, 0.80 * s, 0.80 * s, 1.0)))
        _bm_busto_profeta24(bm, bm_pat, M, 1.00, 1.52, spec)
    _mesh_da_bmesh(f"{name}_Marmo", col, bm, PIETRA_RIL, uv_scale=(1.2, 1.2))
    _mesh_da_bmesh(f"{name}_Incavi", col, bm_pat, PATINA, uv_scale=(1.2, 1.2))


for _sx in (-1, 1):
    _tag = "Sx" if _sx < 0 else "Dx"
    profeta_pennacchio_v26(f"Profeta_Pennacchio_Alto_{_tag}", ST, _sx,
                           _sx * 2.62, Z_PAN + 2.42, 1.24, 1.86, alto=True)
    profeta_pennacchio_v26(f"Profeta_Pennacchio_Basso_{_tag}", ST, _sx,
                           _sx * 2.62, Z_PAN - 2.08, 1.24, 1.84, alto=False)

# =============================================================================
# 4.6 GALLERIA SUPERIORE DEI 15 PROFETI (sopra il rosone)
# =============================================================================
n_top = 15
w_ntop = (HALF_SQ * 2.0) / n_top
z_galleria_profeti = Z_PAN + PAN_HH + 0.10
h_galleria_profeti = Z_TIMPANO - z_galleria_profeti - 0.13
z_cornice_base_profeti = z_galleria_profeti - 0.035
z_cornice_cima_profeti = z_galleria_profeti + h_galleria_profeti + 0.045
box(
    "Fondo_Galleria_Profeti", R, 0.0, -1.335,
    z_galleria_profeti + h_galleria_profeti * 0.50,
    HALF_SQ * 2.0, 0.12, h_galleria_profeti * 0.99, ROSA_C,
)
box(
    "Fondo_Rosa_Fra_I_Frontoni", R, 0.0, -1.408,
    z_galleria_profeti + h_galleria_profeti * 0.755,
    HALF_SQ * 2.0, 0.035, h_galleria_profeti * 0.470, RIGATO,
)
_bm_cosmate = bmesh.new()
_bm_box(_bm_cosmate, Matrix.Identity(4), 0.0, -1.405,
        z_galleria_profeti + h_galleria_profeti * 0.985,
        HALF_SQ * 2.0, 0.05, h_galleria_profeti * 0.075)
_mesh_da_bmesh("Fascia_Verde_Sotto_Trabeazione", R, _bm_cosmate, VERDE, uv_scale=(0.600, 0.600))

box("Cornice_Base_Galleria_Profeti", R, 0.0, -1.58,
    z_cornice_base_profeti, HALF_SQ * 2.0 + 0.26, 0.31, 0.12, BIANCO2)
box("Filo_Rosa_Base_Profeti", R, 0.0, -1.740,
    z_cornice_base_profeti + 0.062, HALF_SQ * 2.0 + 0.20, 0.055, 0.024, ROSA)
_bm_perle_base = bmesh.new()
for k_pb in range(int((HALF_SQ * 2.0 + 0.16) / 0.062)):
    _bm_sfera(_bm_perle_base, Matrix.Identity(4),
              -(HALF_SQ + 0.08) + k_pb * 0.062, -1.735,
              z_cornice_base_profeti - 0.020, 0.016, sy=0.7, u=6, v=4)
_mesh_da_bmesh("Perlinatura_Base_Galleria_Profeti", R, _bm_perle_base, BIANCO, uv_scale=(1.0, 1.0))

for i in range(n_top):
    nx = -HALF_SQ + w_ntop * (i + 0.5)
    edicola_galleria_profeta(
        f"Nicchia_Sup_{i:02d}", R, nx, -1.560,
        z_galleria_profeti, w_ntop * 1.005, h_galleria_profeti, variant=i,
    )
box("Cornice_Cima_Galleria_Profeti", R, 0.0, -1.60,
    z_cornice_cima_profeti, HALF_SQ * 2.0 + 0.28, 0.28, 0.075, BIANCO2)
box("Filetto_Rosa_Cima_Profeti", R, 0.0, -1.750,
    z_cornice_cima_profeti + 0.010, HALF_SQ * 2.0 + 0.22, 0.06, 0.024, ROSA)

# =============================================================================
# 4.7 FILA INFERIORE DI NICCHIE (sotto il rosone, ai lati della statua centrale)
# =============================================================================
n_bot = 14
w_nbot = (HALF_SQ * 2.0) / n_bot
for i in range(n_bot):
    nx = -HALF_SQ + w_nbot * (i + 0.5)
    if abs(nx) > 0.72:
        edicola_gotica_busto(f"Nicchia_Inf_{i}", R, nx, -1.44, 15.32,
                             w_nbot * 0.98, 1.22, con_busto=True)

# =============================================================================
# 4.8 QUATTRO NICCHIE PER LATO CON STATUE A FIGURA INTERA + FASCIA DI QUATRIFOGLI
# =============================================================================
n_side = 4
z_v0 = Z_PAN - PAN_HH + 0.42
z_v1 = Z_PAN + PAN_HH - 0.20
h_nside = (z_v1 - z_v0) / n_side
_GESTI_LAT = ("libro", "leggi", "croce", "petto", "benedicente", "libro", "leggi", "croce")
for side in (-1, 1):
    tag = "Sx" if side < 0 else "Dx"
    # fascia di quatrifogli scolpiti sul pilastro, dove in fotografia sta davvero
    box(f"Fregio_Quatrifogli_{tag}", D, side * 4.52, -1.575,
        (z_v0 + z_v1) * 0.5, 0.36, 0.10, z_v1 - z_v0 + 0.10, BIANCO2)
    for _s in (-1, 1):
        box(f"Fregio_Quatrifogli_Filo_{tag}_{_s:+d}", D,
            side * 4.52 + _s * 0.185, -1.61, (z_v0 + z_v1) * 0.5,
            0.045, 0.055, z_v1 - z_v0 + 0.10, VERDE)
    for k_r in range(8):
        rosetta_rilievo(f"Quatrifoglio_{tag}_{k_r}", D, side * 4.52, -1.645,
                        z_v0 + (z_v1 - z_v0) * (k_r + 0.5) / 8.0, 0.115, petals=4)
    for j in range(n_side):
        z_n = z_v0 + j * h_nside
        edicola_v26(
            f"Nicchia_Lat_{tag}_{j}", R, side * 3.93, -1.52,
            z_n, 0.94, h_nside * 0.99,
        )
        gesto = _GESTI_LAT[(j + (0 if side < 0 else 3)) % len(_GESTI_LAT)]
        statua_gotica_v26(
            f"Statua_Lat_{tag}_{j}", ST, side * 3.93, -1.50,
            z_n + 0.085, h_nside * 0.585,
            spec=dict(gesto=gesto, barba=0.55 + 0.18 * (j % 3),
                      copricapo=("capelli", "berretta", "capelli_lunghi")[j % 3],
                      yaw=-side * 0.12, nod=0.05, seed=j * 3 + (0 if side < 0 else 1),
                      lato=-side),
        )

# =============================================================================
# 5. PILASTRI CONTRAFFORTI CENTRALI POLISTILI + GUGLIE GOTICHE CON TABERNACOLI
#    E STATUE (x = +-5.00 m, ricostruiti fedelmente sulla foto ravvicinata)
# =============================================================================
def _statua_santa_guglia(name, col, x, y, z, h=1.18, turn=0.14, material=None):
    """Statua gotica panneggiata sommitale dei due pinnacoli affiancanti la cuspide."""
    material = material or BIANCO
    bm = bmesh.new()
    M = Matrix.Translation((x, y, z)) @ Matrix.Rotation(turn, 4, "Z") @ Matrix.Diagonal((h, h, h, 1.0))
    _bm_lathe(bm, M, ((0.0, 0.13), (0.04, 0.14), (0.08, 0.115)), seg=16, sy=0.88)
    _bm_lathe(
        bm, M,
        ((0.07, 0.115), (0.18, 0.135), (0.36, 0.128), (0.54, 0.112), (0.68, 0.098), (0.76, 0.105)),
        seg=22, sy=0.80, rib=0.055, rib_n=11,
    )
    # Pieghe verticali scavate e manto avvolgente
    for i in range(10):
        a = math.tau * i / 10
        _bm_segmento(
            bm, M,
            (0.115 * math.cos(a), 0.092 * math.sin(a), 0.10),
            (0.092 * math.cos(a), 0.074 * math.sin(a), 0.64),
            0.015, 0.011, seg=6,
        )
    _bm_sfera(bm, M, 0.0, -0.005, 0.77, 0.082, sx=1.55, sy=0.82, sz=0.72, u=14, v=8)
    # Braccia piegate sul petto con codice / rotolo
    for sa in (-1, 1):
        _bm_segmento(bm, M, (sa * 0.11, 0.0, 0.75), (sa * 0.13, -0.05, 0.61), 0.036, 0.030, seg=8)
        _bm_segmento(bm, M, (sa * 0.13, -0.05, 0.61), (sa * 0.05, -0.10, 0.63), 0.030, 0.025, seg=8)
    _bm_box(bm, M, -0.03, -0.115, 0.64, 0.11, 0.045, 0.13, rot=Matrix.Rotation(0.20, 4, "Y"))
    # Testa velata / chioma scolpita
    _bm_segmento(bm, M, (0.0, 0.0, 0.79), (0.0, -0.005, 0.85), 0.036, 0.032, seg=10)
    _bm_sfera(bm, M, 0.0, -0.01, 0.905, 0.072, sx=0.86, sy=0.96, sz=1.08, u=16, v=10)
    _bm_sfera(bm, M, 0.0, 0.015, 0.925, 0.076, sx=0.96, sy=1.02, sz=1.05, u=14, v=9)
    return _mesh_da_bmesh(name, col, bm, material)


def pilastro_centrale_completo(side):
    cx = side * X_PIL_C
    tag = "Sx" if side < 0 else "Dx"
    h_shaft = Z_PIL_TOP - Z_GALLERIA
    z_mid = Z_GALLERIA + h_shaft * 0.5

    # Nucleo del contrafforte polistilo in marmo senese
    box(f"Pilastro_Centrale_{tag}", G, cx, -0.62, z_mid, W_PIL_C, 1.86, h_shaft, BIANCO)

    # Specchiature verticali in marmo rosa senese e bianco caldo (pieno marmo luminoso come in cmp_pier.jpg, ZERO fessure nere!)
    for s2 in (-0.31, 0.31):
        box(f"Specchio_Rosa_Pil_{tag}_{s2:+.2f}", G, cx + s2, -1.565, z_mid, 0.30, 0.08, h_shaft - 0.20, ROSA_C)
    for s2 in (-0.58, -0.22, 0.0, 0.22, 0.58):
        w_rib = 0.135 if abs(s2) > 0.5 else (0.115 if s2 == 0 else 0.095)
        y_rib = -1.625 if abs(s2) in (0.0, 0.58) else -1.59
        mat_rib = BIANCO if abs(s2) > 0.1 else BIANCO2
        box(f"Costolone_Pil_{tag}_{s2:+.2f}", G, cx + s2, y_rib, z_mid, w_rib, 0.20, h_shaft, mat_rib)

    # Statue inferiori nei tabernacoli del registro dell'oculo
    for s2 in (-1, 1):
        sx_st = cx + s2 * 0.30
        statue(f"Statua_PilCent_{tag}_{s2}", ST, sx_st, -1.68, Z_GALLERIA + 0.30, 1.65, PIETRA)
        spioventi_modanati(f"Ghim_PilBase_{tag}_{s2}", G, sx_st, -1.68, Z_GALLERIA + 2.35, 0.58, 0.72, 0.07, 0.26, BIANCO)

    # Costruzione gotica scolpita ad alta definizione del registro alto + guglia (bmesh consolidati)
    bm_w = bmesh.new()   # elementi in Marmo_Bianco
    bm_p = bmesh.new()   # elementi scolpiti / gattoni / capitelli in Pietra_Statue
    Mi = Matrix.Identity(4)

    # 1) Doppie arcate ogivali cieche strombate + ghimberghe acute + doppie cornici marcapiano patinate (cmp_pier.jpg!)
    bm_pat_pil = bmesh.new()
    for z_band in (22.36, 23.02, 24.48, 25.92, 26.52, Z_PIL_TOP):
        _bm_box(bm_w, Mi, cx, -0.64, z_band, W_PIL_C + 0.15, 1.96, 0.10)
        _bm_box(bm_pat_pil, Mi, cx, -0.65, z_band - 0.068, W_PIL_C + 0.11, 1.93, 0.048)
    _mesh_da_bmesh(f"Patina_Marcapiani_Pil_{tag}", G, bm_pat_pil, PATINA)

    for z_gable, h_gable, has_lancet in ((22.98, 1.38, True), (27.06, 1.30, True)):
        for s2 in (-1, 1):
            gx0 = cx + s2 * 0.305
            gw0 = 0.60
            # Triplo ordine di archetti acuti concentrici incassati (come nella foto 3_left_pinnacle.jpg!)
            if has_lancet:
                for ord_k, (sp_k, rs_k, y_k, min_k) in enumerate((
                    (gw0 * 0.88, h_gable * 0.64, -1.63, 0.030),
                    (gw0 * 0.68, h_gable * 0.52, -1.60, 0.025),
                    (gw0 * 0.48, h_gable * 0.40, -1.57, 0.020),
                )):
                    _bm_arco_acuto(bm_w if ord_k % 2 == 0 else bm_p, Mi, gx0, y_k, z_gable - 0.32, sp_k, rs_k, min_k, seg_u=14, seg_v=6)
            ang_g = math.atan2(h_gable, gw0 * 0.5)
            sl_g = math.hypot(gw0 * 0.5, h_gable) + 0.06
            for gs in (-1, 1):
                _bm_box(
                    bm_w, Mi, gx0 + gs * gw0 * 0.25, -1.66, z_gable + h_gable * 0.5,
                    sl_g, 0.18, 0.068, rot=Matrix.Rotation(gs * ang_g, 4, "Y"),
                )
                for kc in range(4):
                    tc = 0.18 + 0.68 * kc / 3.0
                    _bm_foglia(
                        bm_p, 0.14, 0.075, 0.042,
                        Matrix.Translation((gx0 + gs * gw0 * 0.5 * (1.0 - tc), -1.68, z_gable + h_gable * tc + 0.03))
                        @ Matrix.Rotation(gs * 0.42, 4, "Y"),
                        piega=-0.14 * gs,
                    )
            _bm_lathe(
                bm_p, Matrix.Translation((gx0, -1.67, z_gable + h_gable)),
                ((0.0, 0.048), (0.09, 0.064), (0.24, 0.020)), seg=8, sy=0.85,
            )

    # 2) Doccioni gotici scolpiti sui fianchi dei contrafforti (coppia esterna + doccione interno)
    gargolla(f"Gargolla_Pil_Inf_{tag}", D, cx + side * 0.80, -1.48, 26.52, side, 0.72, 0.088, PIETRA, pitch_deg=4.0)
    gargolla(f"Gargolla_Pil_Med_{tag}", D, cx + side * 0.82, -1.52, 27.14, side, 0.86, 0.098, PIETRA, pitch_deg=34.0)
    gargolla(f"Gargolla_Pil_Int_{tag}", D, cx - side * 0.76, -1.50, 27.10, -side, 0.68, 0.086, PIETRA, pitch_deg=32.0)

    # 3) Tabernacolo / Edicola gotica traforata in marmo bianco (ZERO riquadro nero piatto!)
    z_tab = Z_PIL_TOP + 0.06
    h_tab = 1.48
    y_tab = -0.98
    # Basamento a gradoni modanati del tabernacolo
    _bm_box(bm_w, Mi, cx, y_tab, z_tab + 0.08, 1.06, 1.06, 0.16)
    _bm_box(bm_p, Mi, cx, y_tab, z_tab + 0.21, 0.94, 0.94, 0.10)
    _bm_box(bm_w, Mi, cx, y_tab, z_tab + 0.30, 0.88, 0.88, 0.09)

    # Nucleo gotico poligonale scolpito in marmo bianco-avorio + statua frontale in nicchia!
    # Esattamente come in cmp_pier.jpg (ZERO caverna nera: è un tabernacolo marmoreo scolpito con statua!)
    _bm_lathe(
        bm_p, Matrix.Translation((cx, y_tab, z_tab + 0.30)),
        ((0.0, 0.27), (0.45, 0.24), (0.95, 0.23), (1.18, 0.25)),
        seg=8, sy=1.0, rib=0.10, rib_n=8,
    )
    _statua_santa_guglia(f"Statuetta_Ciborio_{tag}", ST, cx, y_tab - 0.27, z_tab + 0.36, h=0.76, turn=side * 0.18, material=PIETRA_RIL)
    # 4 pilastrini angolari polistili + pinnacolini angolari fioriti con gattoni
    for sx2 in (-1, 1):
        for sy2 in (-1, 1):
            px_c = cx + sx2 * 0.37
            py_c = y_tab + sy2 * 0.37
            _bm_box(bm_w, Mi, px_c, py_c, z_tab + 0.34 + 0.52, 0.17, 0.17, 1.04)
            _bm_box(bm_p, Mi, px_c + sx2 * 0.04, py_c + sy2 * 0.04, z_tab + 0.34 + 0.52, 0.11, 0.11, 1.00)
            # Pinnacolino angolare acuto con gattoni e fiorone
            z_pin = z_tab + 1.38
            _bm_box(bm_w, Mi, px_c, py_c, z_pin + 0.05, 0.21, 0.21, 0.10)
            _bm_cono(bm_w, Mi, px_c, py_c, z_pin + 0.44, 0.095, 0.022, 0.68, seg=8)
            for kp in range(3):
                _bm_foglia(
                    bm_p, 0.13, 0.07, 0.04,
                    Matrix.Translation((px_c + sx2 * 0.05, py_c - 0.04, z_pin + 0.14 + kp * 0.17))
                    @ Matrix.Rotation(sx2 * 0.38, 4, "Y"),
                    piega=-0.12 * sx2,
                )
            _bm_sfera(bm_p, Mi, px_c, py_c, z_pin + 0.80, 0.045, sz=1.35, u=8, v=6)

    # Archetti ogivali cuspidati e ghimberghe frontali/laterali del tabernacolo
    for y_face in (-0.38, 0.38):
        _bm_arco_acuto(bm_w, Mi, cx, y_tab + y_face, z_tab + 0.86, 0.62, 0.46, 0.036, seg_u=14, seg_v=6)
        ang_t = math.atan2(0.68, 0.34)
        sl_t = math.hypot(0.34, 0.68) + 0.05
        for gs in (-1, 1):
            _bm_box(
                bm_w, Mi, cx + gs * 0.17, y_tab + y_face - 0.02, z_tab + 0.94 + 0.34,
                sl_t, 0.11, 0.058, rot=Matrix.Rotation(gs * ang_t, 4, "Y"),
            )
            for kc in range(3):
                tc = 0.22 + 0.62 * kc / 2.0
                _bm_foglia(
                    bm_p, 0.13, 0.07, 0.04,
                    Matrix.Translation((cx + gs * 0.34 * (1.0 - tc), y_tab + y_face - 0.04, z_tab + 0.94 + 0.68 * tc))
                    @ Matrix.Rotation(gs * 0.40, 4, "Y"),
                    piega=-0.12 * gs,
                )

    # Doccioni superiori del tabernacolo (visibilissimi nella foto 3_left_pinnacle.jpg!)
    gargolla(f"Gargolla_Tab_Inf_{tag}", D, cx - side * 0.58, y_tab - 0.16, z_tab + 0.68, -side, 0.64, 0.082, PIETRA, pitch_deg=-8.0)
    gargolla(f"Gargolla_Tab_Sup_{tag}", D, cx - side * 0.56, y_tab - 0.14, z_tab + 1.04, -side, 0.66, 0.082, PIETRA, pitch_deg=26.0)
    gargolla(f"Gargolla_Tab_Est_{tag}", D, cx + side * 0.55, y_tab - 0.15, z_tab + 0.96, side, 0.54, 0.076, PIETRA, pitch_deg=18.0)

    # 4) Fusto ottagonale slanciato della guglia tempestate di gattoni rampanti + grande cesto corinzio d'acanto
    h_asym = 0.0 if side < 0 else -0.14  # autentica lieve asimmetria Sx/Dx del Duomo di Siena
    z_sp = z_tab + h_tab
    h_sp = 0.98 + h_asym
    _bm_lathe(
        bm_w, Matrix.Translation((cx, y_tab, z_sp)),
        ((0.0, 0.28), (h_sp * 0.35, 0.22), (h_sp * 0.72, 0.165), (h_sp, 0.135)),
        seg=8, sy=1.0,
    )
    for ring_i in range(5):
        tr = ring_i / 4.0
        rz_i = z_sp + 0.08 + tr * (h_sp - 0.14)
        rr_i = 0.26 * (1.0 - 0.42 * tr)
        sz_i = 0.19 * (1.0 - 0.28 * tr)
        for k8 in range(8):
            a8 = math.tau * k8 / 8.0 + (0.39 if ring_i % 2 else 0.0)
            d8 = Vector((0.68 * math.cos(a8), 0.68 * math.sin(a8), 0.73)).normalized()
            Mp = Matrix.Translation((cx + rr_i * math.cos(a8), y_tab + rr_i * math.sin(a8), rz_i)) @ d8.to_track_quat("Z", "Y").to_matrix().to_4x4()
            _bm_foglia(bm_p, sz_i, sz_i * 0.62, sz_i * 0.30, Mp, piega=0.18, gonfia=1.2)

    # Capitello corinzio compatto e scolpito a due ordini (proporzione snella esatta di cmp_pier.jpg!)
    z_cap = z_sp + h_sp
    _bm_lathe(
        bm_p, Matrix.Translation((cx, y_tab, z_cap)),
        ((0.0, 0.115), (0.12, 0.165), (0.24, 0.185), (0.34, 0.165), (0.40, 0.145)),
        seg=14, sy=1.0,
    )
    for tier_c, (nc, rc, lc, wc, tilt_c) in enumerate(((8, 0.125, 0.22, 0.11, 0.46), (8, 0.145, 0.20, 0.115, 0.30))):
        for kc in range(nc):
            ac = math.tau * kc / nc + (0.39 if tier_c else 0.0)
            dc = Vector((math.sin(tilt_c) * math.cos(ac), math.sin(tilt_c) * math.sin(ac), math.cos(tilt_c)))
            Mcap = Matrix.Translation((cx + rc * math.cos(ac), y_tab + rc * math.sin(ac), z_cap + 0.04 + tier_c * 0.12)) @ dc.to_track_quat("Z", "Y").to_matrix().to_4x4()
            _bm_foglia(bm_p, lc, wc, 0.042, Mcap, piega=0.18, gonfia=1.25)

    _mesh_da_bmesh(f"Guglia_Gotica_Marmo_{tag}", G, bm_w, BIANCO)
    _mesh_da_bmesh(f"Guglia_Gotica_Scolpita_{tag}", G, bm_p, PIETRA_RIL)

    # 5) Statua sommitale panneggiata sul capitello fogliato
    _statua_santa_guglia(
        f"Statua_Sommitale_Guglia_{tag}", ST,
        cx, y_tab, z_cap + 0.40, h=1.14, turn=-side * 0.22, material=PIETRA,
    )


pilastro_centrale_completo(-1)
pilastro_centrale_completo(1)

# -----------------------------------------------------------------------------
# Ornamenti della cuspide: crockets a tre lobi, fregi, ali e statua apicale
# -----------------------------------------------------------------------------
def _normale_spiovente(s, W, H):
    L = math.hypot(W * 0.5, H)
    return (-s * H / L, -(W * 0.5) / L), L


def punto_spiovente(s, W, H, t, offset, z_base):
    """Punto sullo spiovente (t=0 base, t=1 apice) arretrato di `offset` verso l'interno."""
    n, _ = _normale_spiovente(s, W, H)
    return (s * W * 0.5 * (1.0 - t) + n[0] * offset,
            z_base + H * t + n[1] * offset)


def banda_spiovente(name, col, s, W, H, z_base, offset, thickness, depth, material, y,
                    trim_apice=0.0, trim_base=0.0):
    """Modanatura continua parallela allo spiovente, arretrata di `offset` dal bordo.

    `trim_apice` accorcia la modanatura verso la punta così le due falde non si
    incrociano sotto il cappuccio apicale.
    """
    n, L = _normale_spiovente(s, W, H)
    ax, az = n[0] * offset, H + n[1] * offset
    bx, bz = s * W * 0.5 + n[0] * offset, n[1] * offset
    ang = -math.atan2(az - bz, ax - bx)
    # accorcia spostando l'estremità apicale lungo lo spiovente
    ux, uz = (ax - bx) / L, (az - bz) / L
    ax -= ux * trim_apice
    az -= uz * trim_apice
    bx += ux * trim_base
    bz += uz * trim_base
    Ln = math.hypot(ax - bx, az - bz)
    return box(name, col, (ax + bx) * 0.5, y, z_base + (az + bz) * 0.5,
               Ln + thickness * 0.5, depth, thickness, material, rot_y=ang)


def filo_spiovente(name, col, s, W, H, z_base, offset, radius, material, y,
                   trim_apice=0.0):
    """Filo arrotondato (toro) parallelo allo spiovente."""
    n, L = _normale_spiovente(s, W, H)
    ax, az = n[0] * offset, H + n[1] * offset
    bx, bz = s * W * 0.5 + n[0] * offset, n[1] * offset
    ang = math.atan2(-s * W * 0.5, H)   # cilindro con asse Z lungo lo spiovente
    ux, uz = (ax - bx) / L, (az - bz) / L
    ax -= ux * trim_apice
    az -= uz * trim_apice
    Ln = math.hypot(ax - bx, az - bz)
    obj = cyl(name, col, (ax + bx) * 0.5, y, z_base + (az + bz) * 0.5, radius,
              Ln, material, vertices=10, rot_y=ang)
    return obj


def perle_spiovente(name, col, s, W, H, z_base, offset, y, step=0.17, radius=0.052,
                    material=None, fondo=True, fondo_y=None, fondo_depth=0.10,
                    fondo_w=0.26, fondo_material=None):
    """Filo di perle su fondo in ombra: rende il motivo a puntinato della foto."""
    material = material or BIANCO
    fondo_material = fondo_material or PIETRA
    L = math.hypot(W * 0.5, H)
    if fondo:
        banda_spiovente(name + "_fondo", col, s, W, H, z_base, offset,
                        fondo_w, fondo_depth, fondo_material, fondo_y or (y + 0.06))
    n = max(2, int(L / step))
    for i in range(n):
        px, pz = punto_spiovente(s, W, H, (i + 0.5) / n, offset, z_base)
        sphere(f"{name}_{i}", col, px, y, pz, radius, material, sy=0.85)


def foglia_acanto(name, col, x, y, z, lung, larg, spess, ang, material,
                  denti=3, profilo=None):
    """Foglia d'acanto a bassorilievo: punta lanceolata, lobi laterali, spessore in Y.

    Il profilo di semi-larghezza (0..1 della lunghezza) è campionato su una
    serie di ascisse e replicato in modo simmetrico; due pelli parallele
    (fronte e dorso) danno lo spessore che crea l'ombra del rilievo.
    """
    profilo = profilo or (
        (0.00, 0.26), (0.12, 0.46), (0.24, 0.40), (0.36, 0.54),
        (0.50, 0.42), (0.64, 0.42), (0.76, 0.28), (0.90, 0.14), (1.00, 0.01),
    )
    bm = bmesh.new()
    left_f, right_f, left_b, right_b = [], [], [], []
    for t, hw in profilo:
        w = hw * larg
        zz = t * lung
        # il dorso resta piatto contro la muratura, il fronte si solleva
        bulge = spess * (0.35 + 0.65 * math.sin(math.pi * min(1.0, t * 1.08)))
        for lst, yy, scale in ((left_f, -bulge, 1.0), (right_f, -bulge, 1.0),
                               (left_b, 0.0, 0.92), (right_b, 0.0, 0.92)):
            lst.append(( -w * scale if lst in (left_f, left_b) else w * scale, yy, zz))
    lf = [bm.verts.new(p) for p in left_f]
    rf = [bm.verts.new(p) for p in right_f]
    lb = [bm.verts.new(p) for p in left_b]
    rb = [bm.verts.new(p) for p in right_b]
    for i in range(len(profilo) - 1):
        bm.faces.new((lf[i], rf[i], rf[i + 1], lf[i + 1]))
        bm.faces.new((lb[i + 1], rb[i + 1], rb[i], lb[i]))
        bm.faces.new((lf[i + 1], lf[i], lb[i], lb[i + 1]))
        bm.faces.new((rf[i], rf[i + 1], rb[i + 1], rb[i]))
    bm.faces.new((lf[0], lb[0], rb[0], rf[0]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    uv_layer = bm.loops.layers.uv.verify()
    for f in bm.faces:
        for loop in f.loops:
            loop[uv_layer].uv = (0.5 + loop.vert.co.x / max(larg, 1e-3),
                                 0.5 + loop.vert.co.z / max(lung, 1e-3))
    mesh = bpy.data.meshes.new(name + "Mesh")
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    return _create_mesh_object(name, mesh, col, (x, y, z), (0.0, ang, 0.0),
                               (1, 1, 1), material)


# -----------------------------------------------------------------------------
# Geometria ornamentale "monolitica" (molti dettagli in un solo oggetto):
# foglie e penne in un bmesh condiviso, perline fuse in un'unica mesh.
# -----------------------------------------------------------------------------
PROFILO_FOGLIA = (
    (0.00, 0.24), (0.12, 0.44), (0.24, 0.38), (0.36, 0.52),
    (0.50, 0.40), (0.64, 0.40), (0.76, 0.26), (0.90, 0.13), (1.00, 0.01),
)
PROFILO_PENNA = (
    (0.00, 0.16), (0.14, 0.42), (0.30, 0.48), (0.46, 0.46),
    (0.62, 0.40), (0.78, 0.29), (0.90, 0.16), (1.00, 0.01),
)


def _bm_foglia(bm, lung, larg, spess, mat4, profilo=None, piega=0.0, gonfia=1.0):
    """Aggiunge al bmesh una foglia lanceolata a rilievo (lunghezza +Z locale).

    Il dorso resta piatto (appoggiato alla muratura) e il fronte si solleva
    di `spess`; la punta può incurvarsi di `piega` (per i crockets arrotolati).
    """
    profilo = profilo or PROFILO_FOGLIA
    lf, rf, lb, rb = [], [], [], []
    for t, hw in profilo:
        w = hw * larg
        zz = t * lung
        bulge = spess * gonfia * (0.34 + 0.66 * math.sin(math.pi * min(1.0, t * 1.05)))
        curv = piega * (t ** 2) * lung
        for lst, xx, yy, sc in ((lf, -w, -bulge, 1.0), (rf, w, -bulge, 1.0),
                                (lb, -w * 0.90, 0.0, 1.0), (rb, w * 0.90, 0.0, 1.0)):
            lst.append(bm.verts.new(mat4 @ Vector((xx + curv, yy, zz))))
    n = len(profilo)
    for i in range(n - 1):
        bm.faces.new((lf[i], rf[i], rf[i + 1], lf[i + 1]))
        bm.faces.new((lb[i + 1], rb[i + 1], rb[i], lb[i]))
        bm.faces.new((lf[i + 1], lf[i], lb[i], lb[i + 1]))
        bm.faces.new((rf[i], rf[i + 1], rb[i + 1], rb[i]))
    bm.faces.new((lf[0], lb[0], rb[0], rf[0]))
    bm.faces.new((rf[-1], rb[-1], lb[-1], lf[-1]))


def _bm_sfera(bm, mat4, x, y, z, r, sx=1.0, sy=1.0, sz=1.0, u=10, v=6):
    m = mat4 @ Matrix.Translation((x, y, z)) @ Matrix.Diagonal((r * sx, r * sy, r * sz, 1.0))
    bmesh.ops.create_uvsphere(bm, u_segments=u, v_segments=v, radius=1.0, matrix=m)


def _bm_cono(bm, mat4, x, y, z, r1, r2, h, rot=None, seg=8, sy=1.0):
    m = mat4 @ Matrix.Translation((x, y, z))
    if rot is not None:
        m = m @ rot
    m = m @ Matrix.Diagonal((1.0, sy, 1.0, 1.0))
    bmesh.ops.create_cone(bm, cap_ends=True, cap_tris=True, segments=seg,
                          radius1=r1, radius2=r2, depth=h, matrix=m)


def _mesh_da_bmesh(name, col, bm, material, uv_scale=(0.31, 0.31)):
    mesh = bpy.data.meshes.new(name + "Mesh")
    _finish_bmesh(bm, mesh, uv_scale=uv_scale)
    return _create_mesh_object(name, mesh, col, (0, 0, 0), (0, 0, 0), (1, 1, 1), material)


def fila_perle(name, col, punti, r, material, sub=1):
    """Filo di perline fuso in un'unica mesh (le perline v1.6 erano sfere sparse)."""
    bm = bmesh.new()
    ident = Matrix.Identity(4)
    for (x, y, z) in punti:
        _bm_sfera(bm, ident, x, y, z, r, u=8, v=4)
    return _mesh_da_bmesh(name, col, bm, material)


# -----------------------------------------------------------------------------
# Fascia degli spioventi: modanature continue tagliate a mitra sull'asse (x = 0)
# -----------------------------------------------------------------------------
def _angolo_spiovente(W, H):
    """Angolo fra lo spiovente e la verticale: sin(theta) = (W/2)/L."""
    L = math.hypot(W * 0.5, H)
    return math.asin((W * 0.5) / L), L


def punto_fascia(s, W, H, o, u, z_base=0.0):
    """Punto su una modanatura spiovente (o = arretramento dal filo esterno,
    u = 0 alla base del timpano, 1 sul taglio a mitra dell'asse)."""
    sin_t, L = _angolo_spiovente(W, H)
    k = H / (W * 0.5)
    za = H - o / sin_t                       # quota in cui la linea tocca l'asse
    xb = s * (H - o / sin_t) / k             # intersezione con la base
    return (xb * (1.0 - u), z_base + za * u)


def banda_mitrata(name, col, s, W, H, o0, o1, y_front, depth, material, z_base=0.0,
                  uv_scale=(0.31, 0.31), aggetto=0.0):
    """Modanatura dello spiovente con estremità tagliata a mitra sull'asse.

    A differenza delle vecchie scatole ruotate (che si incrociavano formando
    una X con vuoti neri sull'apice) ogni modanatura termina esattamente
    contro il piano x = 0, come il vero taglio a mitra delle cornici.
    """
    bm = bmesh.new()
    y0, y1 = y_front, y_front + depth
    quad = [punto_fascia(s, W, H, o0, 0.0, z_base), punto_fascia(s, W, H, o1, 0.0, z_base),
            punto_fascia(s, W, H, o1, 1.0, z_base), punto_fascia(s, W, H, o0, 1.0, z_base)]
    if aggetto:
        # il filo interno sporge di piu' verso l'osservatore (modanatura obliqua)
        quad = [(px, pz) for (px, pz) in quad]
    ya = (y0 - aggetto, y1 - aggetto, y1 - aggetto, y0 - aggetto)
    vf = [bm.verts.new((px, ya[i], pz)) for i, (px, pz) in enumerate(quad)]
    vb = [bm.verts.new((px, y1 + 0.02, pz)) for (px, pz) in quad]
    bm.faces.new(vf)
    bm.faces.new(list(reversed(vb)))
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((vf[i], vf[j], vb[j], vb[i]))
    return _mesh_da_bmesh(name, col, bm, material, uv_scale=uv_scale)


def crocchi_spiovente(name, col, s, W, H, z_base, y, n=21, size=0.38, offset=0.015,
                      material=None, y_fondo=None, tilt=None, taper=0.84,
                      gonfia=1.28):
    """Autentici gattoni gotici rampanti senesi a foglia d'acanto carnosa e uncinata
    (verificati su cmp_angel.jpg e cmp_lower.jpg: corpo fogliato pieno aderente allo
    spiovente, apice ricurvo a gancio con perla terminale e sottosquadro d'ombra!)."""
    material = material or BIANCO
    sin_t, L = _angolo_spiovente(W, H)
    px_, pz_ = s * H / L, (W * 0.5) / L
    ux_, uz_ = -s * (W * 0.5) / L, H / L
    bm = bmesh.new()
    bm_pat = bmesh.new()
    for i in range(n):
        u = 0.050 + 0.896 * i / max(1, n - 1)
        bx, bz = punto_fascia(s, W, H, offset, u, z_base)
        sz_i = size * (1.0 - (1.0 - taper) * u)
        c0 = Vector((bx - ux_ * sz_i * 0.56, y + 0.01, bz - uz_ * sz_i * 0.56))
        c1 = Vector((bx + px_ * sz_i * 0.28 - ux_ * sz_i * 0.08, y - 0.015, bz + pz_ * sz_i * 0.28 - uz_ * sz_i * 0.08))
        c2 = Vector((bx + px_ * sz_i * 0.60 + ux_ * sz_i * 0.16, y - 0.028, bz + pz_ * sz_i * 0.60 + uz_ * sz_i * 0.16))
        c3 = Vector((bx + px_ * sz_i * 0.68 - ux_ * sz_i * 0.04, y - 0.022, bz + pz_ * sz_i * 0.68 - uz_ * sz_i * 0.04))
        _bm_segmento(bm, Matrix.Identity(4), c0, c1, sz_i * 0.165, sz_i * 0.205, seg=9, sy=0.82)
        _bm_segmento(bm, Matrix.Identity(4), c1, c2, sz_i * 0.205, sz_i * 0.165, seg=9, sy=0.82)
        _bm_sfera(bm, Matrix.Translation(c3), 0.0, 0.0, 0.0, sz_i * 0.175, sx=1.18, sy=0.85, sz=1.08, u=10, v=7)
        # Incavo d'ombra patinato sotto la curvatura del ricciolo (identico alla foto!)
        p_und = Vector((bx + px_ * sz_i * 0.34 - ux_ * sz_i * 0.22, y + 0.005, bz + pz_ * sz_i * 0.34 - uz_ * sz_i * 0.22))
        _bm_sfera(bm_pat, Matrix.Translation(p_und), 0.0, 0.0, 0.0, sz_i * 0.125, sx=1.05, sy=0.72, sz=0.95, u=8, v=6)
        d_climb = (c2 - c0).normalized()
        Mc = Matrix.Translation(c0) @ d_climb.to_track_quat("Z", "Y").to_matrix().to_4x4()
        _bm_foglia(
            bm, (c2 - c0).length * 0.98, sz_i * 0.42, sz_i * 0.18, Mc,
            profilo=((0.00, 0.28), (0.24, 0.50), (0.48, 0.44), (0.72, 0.56), (0.90, 0.38), (1.00, 0.14)),
            piega=0.18 * s, gonfia=gonfia,
        )
    _mesh_da_bmesh(f"{name}_Patina", col, bm_pat, PATINA)
    return _mesh_da_bmesh(name, col, bm, material)


def _bm_ala_rilievo(bm, M, s, a0, a1, r0, r_tip, spess, n_penne=5,
                    larghezza=0.52, scalatura=0.82):
    """Ala di cherubino a bassorilievo: penne lanceolate embricate."""
    for i in range(n_penne):
        t = i / max(1, n_penne - 1)
        a = s * (a0 + (a1 - a0) * t)
        ln = (r_tip - r0) * (1.0 - (1.0 - scalatura) * t)
        Mb = M @ Matrix.Translation((r0 * math.sin(a) * 0.5,
                                     -spess * 0.25 * (1.0 - t),
                                     r0 * math.cos(a) * 0.5)) \
               @ Matrix.Rotation(a, 4, "Y")
        _bm_foglia(bm, ln, ln * larghezza, spess,
                   Mb, profilo=((0.00, 0.30), (0.14, 0.44), (0.32, 0.48),
                                (0.52, 0.44), (0.72, 0.34), (0.88, 0.20), (1.00, 0.01)),
                   piega=0.10 * s)


def _add_testa_cherubino(bm, x, y, z, r, ali=1.0, tilt=0.0, ali_su=False, bm_pat=None):
    """Aggiunge a `bm` una testina di cherubino alata ad altorilievo marmoreo +
    incavi patinati di orbite, bocca, riccioli e penne in `bm_pat` (cmp_lower.jpg!)."""
    M = Matrix.Translation((x, y, z)) @ Matrix.Rotation(tilt, 4, "Y")
    fy = 0.58
    ys = -r * fy * 1.08
    _bm_sfera(bm, M, 0.0, 0.0, 0.0, r, sx=0.82, sy=fy, sz=1.02, u=16, v=10)
    _bm_sfera(bm, M, 0.0, ys * 0.72, -r * 0.58, r * 0.34, sx=0.68, sy=fy * 0.85, sz=0.56, u=10, v=6)
    _bm_sfera(bm, M, 0.0, ys * 0.58, r * 0.24, r * 0.32, sx=0.88, sy=fy * 0.58, sz=0.46, u=10, v=6)
    for s in (-1, 1):
        _bm_sfera(bm, M, s * r * 0.24, ys * 0.96, r * 0.12, r * 0.13, sx=1.55, sy=fy * 0.45, sz=0.28, u=8, v=5)
        _bm_sfera(bm, M, s * r * 0.22, ys * 0.82, -r * 0.03, r * 0.075, sx=1.30, sy=fy * 0.42, sz=0.58, u=8, v=5)
        _bm_sfera(bm, M, s * r * 0.38, ys * 0.76, -r * 0.20, r * 0.27, sx=0.82, sy=fy * 0.68, sz=0.60, u=8, v=5)
        if bm_pat is not None:
            # Orbite oculari e fossette laterali patinate (danno subito vita al volto!)
            _bm_sfera(bm_pat, M, s * r * 0.24, ys * 0.95, r * 0.01, r * 0.095, sx=1.25, sy=fy * 0.35, sz=0.58, u=7, v=5)
            _bm_sfera(bm_pat, M, s * r * 0.58, ys * 0.42, -r * 0.28, r * 0.16, sx=0.75, sy=fy * 0.55, sz=0.85, u=7, v=5)
    _bm_segmento(bm, M, (0.0, ys * 0.88, r * 0.12), (0.0, ys * 1.06, -r * 0.16), r * 0.11, r * 0.14, seg=6)
    _bm_sfera(bm, M, 0.0, ys * 0.94, -r * 0.32, r * 0.08, sx=1.25, sy=fy * 0.35, sz=0.28, u=8, v=5)
    if bm_pat is not None:
        _bm_sfera(bm_pat, M, 0.0, ys * 0.97, -r * 0.31, r * 0.075, sx=1.45, sy=fy * 0.28, sz=0.26, u=7, v=5)
        _bm_sfera(bm_pat, M, 0.0, ys * 0.65, -r * 0.76, r * 0.22, sx=1.25, sy=fy * 0.45, sz=0.38, u=7, v=5)
    for k in range(9):
        a = -1.45 + 2.90 * k / 8.0
        _bm_sfera(bm, M, math.sin(a) * r * 0.76, r * 0.02 - 0.10 * r,
                  r * 0.18 + math.cos(a) * r * 0.68, r * 0.22,
                  sx=1.0, sy=fy * 0.95, sz=0.92, u=8, v=6)
        if bm_pat is not None and k < 8:
            am = -1.45 + 2.90 * (k + 0.5) / 8.0
            _bm_sfera(bm_pat, M, math.sin(am) * r * 0.68, r * 0.02 - 0.13 * r,
                      r * 0.16 + math.cos(am) * r * 0.62, r * 0.14,
                      sx=0.85, sy=fy * 0.80, sz=0.80, u=6, v=5)
    a_start = math.radians(14) if ali_su else math.radians(42)
    a_end = math.radians(136) if ali_su else math.radians(142)
    for s in (-1, 1):
        Ma = M @ Matrix.Translation((s * r * 0.46, 0.02 * r, -r * 0.06))
        _bm_ala_rilievo(bm, Ma, s, a_start, a_end,
                        r * 0.24, r * 1.55 * ali, r * 0.16 * ali,
                        n_penne=7, larghezza=0.58, scalatura=0.76)
        if bm_pat is not None:
            Mp_w = M @ Matrix.Translation((s * r * 0.42, 0.05 * r, -r * 0.08))
            _bm_ala_rilievo(bm_pat, Mp_w, s, a_start + 0.08, a_end - 0.12,
                            r * 0.18, r * 1.15 * ali, r * 0.10 * ali,
                            n_penne=6, larghezza=0.44, scalatura=0.80)
        Mb = M @ Matrix.Translation((s * r * 0.38, -r * 0.07, -r * 0.10))
        _bm_ala_rilievo(bm, Mb, s, a_start + 0.16, a_end - 0.22,
                        r * 0.16, r * 0.92 * ali, r * 0.14 * ali,
                        n_penne=5, larghezza=0.60, scalatura=0.82)


def testa_cherubino(name, col, x, y, z, r, material=None, ali=1.0, tilt=0.0, ali_su=False):
    bm = bmesh.new()
    _add_testa_cherubino(bm, x, y, z, r, ali=ali, tilt=tilt, ali_su=ali_su)
    return _mesh_da_bmesh(name, col, bm, material or BIANCO)


def _add_giglio_rilievo(bm, x, y, z, h=0.34, tilt=0.0):
    """Aggiunge un giglio / palmetta trilobata senese ad altorilievo marmoreo."""
    M = Matrix.Translation((x, y, z)) @ Matrix.Rotation(tilt, 4, "Y")
    # Fascetta d'attacco alla base
    _bm_sfera(bm, M, 0.0, -h * 0.04, h * 0.16, h * 0.15, sx=1.45, sy=0.55, sz=0.45, u=8, v=5)
    # Petalo centrale lanceolato eretto
    _bm_foglia(
        bm, h * 0.86, h * 0.32, h * 0.15,
        M @ Matrix.Translation((0.0, -h * 0.05, h * 0.12)),
        profilo=((0.00, 0.28), (0.20, 0.48), (0.46, 0.52), (0.72, 0.38), (0.90, 0.18), (1.00, 0.02)),
        gonfia=1.25,
    )
    # Due petali laterali arcuati e ricadenti a giglio fiorentino/senese + sepali bassi
    for s in (-1, 1):
        _bm_foglia(
            bm, h * 0.72, h * 0.30, h * 0.14,
            M @ Matrix.Translation((s * h * 0.06, -h * 0.04, h * 0.15)) @ Matrix.Rotation(s * 0.68, 4, "Y"),
            profilo=((0.00, 0.26), (0.24, 0.48), (0.54, 0.50), (0.80, 0.34), (1.00, 0.06)),
            piega=0.28 * s, gonfia=1.20,
        )
        _bm_foglia(
            bm, h * 0.38, h * 0.20, h * 0.10,
            M @ Matrix.Translation((s * h * 0.08, -h * 0.03, h * 0.14)) @ Matrix.Rotation(s * 2.15, 4, "Y"),
            piega=-0.16 * s, gonfia=1.10,
        )


def fila_perle(name, col, punti, r, material, sub=1):
    bm = bmesh.new()
    ident = Matrix.Identity(4)
    for (x, y, z) in punti:
        _bm_sfera(bm, ident, x, y, z, r, u=8, v=5)
    return _mesh_da_bmesh(name, col, bm, material)


def _lathe(name, col, x, y, z0, profile, material, seg=20, sx=1.0, sy=0.74,
           rib=0.0, rib_n=9, cap_top=True, cap_bottom=True):
    bm = bmesh.new()
    _bm_lathe(bm, Matrix.Translation((x, y, z0)) @ Matrix.Diagonal((sx, 1.0, 1.0, 1.0)),
              profile, seg=seg, sy=sy, rib=rib, rib_n=rib_n, cap=cap_top and cap_bottom)
    return _mesh_da_bmesh(name, col, bm, material)


def ala_angelo(name, col, x, y, z, s, h_body, material, rialzata=False):
    """Vera ala d'aquila / Vittoria classica in rame ossidato verderame del Duomo
    di Siena (identica a cmp_angel.jpg LEFT a zoom 200%!):
    - Margine interno superiore: lungo costolone carpale arcuato liscio
    - 10 LARGHE penne remiganti spatolate e arrotondate (larghezza 0.155*h!)
      totalmente sovrapposte fra loro SENZA ALCUNA FESSURA DI CIELO interna,
      con le 10 punte arrotondate che scendono a scalini lungo il profilo esterno
      e solchi ossidati scuri (`PATINA_BR`) fra una penna e l'altra!!"""
    bm = bmesh.new()
    bm_dark = bmesh.new()
    M = Matrix.Translation((x, y, z))
    top_s = 1.08 if rialzata else 0.95
    out_s = 0.85 if rialzata else 1.06

    wrist_pts = [
        Vector((s * 0.03 * h_body, 0.015 * h_body, -0.04 * h_body)),
        Vector((s * 0.11 * out_s * h_body, 0.005 * h_body, 0.12 * top_s * h_body)),
        Vector((s * 0.20 * out_s * h_body, -0.008 * h_body, 0.29 * top_s * h_body)),
        Vector((s * 0.27 * out_s * h_body, -0.015 * h_body, 0.44 * top_s * h_body)),
    ]
    for iw in range(len(wrist_pts) - 1):
        _bm_segmento(
            bm, M, wrist_pts[iw], wrist_pts[iw + 1],
            h_body * (0.038 - 0.008 * iw), h_body * (0.030 - 0.007 * iw), seg=9, sy=0.65,
        )

    n_rem = 10
    roots, mids, tips = [], [], []
    # Profilo spatolato largo a punta arrotondata come le lamine di rame originali!
    prof_spatola = (
        (0.00, 0.40), (0.20, 0.50), (0.50, 0.52),
        (0.76, 0.49), (0.90, 0.40), (0.97, 0.26), (1.00, 0.10),
    )
    for k in range(n_rem):
        t = k / (n_rem - 1)
        rx = s * out_s * h_body * (0.18 * (1.0 - t) + 0.06 * t)
        rz = h_body * (0.27 * top_s * (1.0 - t) - 0.11 * t)
        ry = h_body * (0.010 - 0.004 * k * 0.1)
        p_root = Vector((rx, ry, rz))

        tx = s * out_s * h_body * (0.30 + 0.145 * math.sin(math.pi * 0.62 * t + 0.22) - 0.18 * (t ** 1.65))
        tz = h_body * (0.60 * top_s - 0.87 * (t ** 1.06))
        ty = h_body * (-0.016 + 0.020 * t)
        p_tip = Vector((tx, ty, tz))

        roots.append(p_root)
        mids.append(p_root.lerp(p_tip, 0.86))  # guscio continuo fino all'86%: ZERO fessure di cielo!
        tips.append(p_tip)

        d_f = p_tip - p_root
        ln_f = d_f.length
        y_step = -0.0038 * (n_rem - k) * h_body
        Mf = M @ Matrix.Translation(p_root + Vector((0.0, y_step, 0.0))) @ d_f.to_track_quat("Z", "Y").to_matrix().to_4x4()
        w_plate = h_body * (0.148 - 0.018 * t)
        _bm_foglia(bm, ln_f, w_plate, h_body * 0.020, Mf, profilo=prof_spatola, piega=0.04 * s, gonfia=1.22)
        # Solco ossidato scuro lungo il bordo d'ombra inferiore di ciascuna penna embricata!
        Md = M @ Matrix.Translation(p_root + Vector((0.0, y_step + 0.005 * h_body, -0.016 * h_body))) @ d_f.to_track_quat("Z", "Y").to_matrix().to_4x4()
        _bm_foglia(bm_dark, ln_f * 0.94, w_plate * 0.96, h_body * 0.012, Md, profilo=prof_spatola, piega=0.04 * s, gonfia=1.05)

    for k in range(n_rem - 1):
        for off_y, rev in ((+0.002 * h_body, False), (+0.022 * h_body, True)):
            quad = [
                bm.verts.new(M @ (roots[k] + Vector((0, off_y, 0)))),
                bm.verts.new(M @ (roots[k + 1] + Vector((0, off_y, 0)))),
                bm.verts.new(M @ (mids[k + 1] + Vector((0, off_y, 0)))),
                bm.verts.new(M @ (mids[k] + Vector((0, off_y, 0)))),
            ]
            bm.faces.new(list(reversed(quad)) if rev else quad)

    # Secondo e terzo ordine di larghe copritrici embricate con ombra ossidata scura sotto il bordo!
    for k in range(9):
        p_r = roots[min(n_rem - 1, k)].lerp(Vector((s * 0.045 * h_body, 0.0, 0.02 * h_body)), 0.38)
        p_t = roots[min(n_rem - 1, k)].lerp(tips[min(n_rem - 1, k)], 0.60)
        d_m = p_t - p_r
        Mm = M @ Matrix.Translation(p_r + Vector((0.0, -0.042 * h_body, 0.0))) @ d_m.to_track_quat("Z", "Y").to_matrix().to_4x4()
        _bm_foglia(bm, d_m.length, h_body * 0.125, h_body * 0.019, Mm, profilo=prof_spatola, gonfia=1.28)
        Mm_d = M @ Matrix.Translation(p_r + Vector((0.0, -0.034 * h_body, -0.014 * h_body))) @ d_m.to_track_quat("Z", "Y").to_matrix().to_4x4()
        _bm_foglia(bm_dark, d_m.length * 0.98, h_body * 0.130, h_body * 0.012, Mm_d, profilo=prof_spatola, gonfia=1.08)

    for k in range(7):
        t = k / 6.0
        p_r = Vector((s * 0.042 * h_body, -0.052 * h_body, h_body * (0.12 - 0.18 * t)))
        p_t = roots[min(n_rem - 1, k + 1)].lerp(mids[min(n_rem - 1, k + 1)], 0.44) + Vector((0.0, -0.048 * h_body, 0.0))
        d_s = p_t - p_r
        Ms = M @ Matrix.Translation(p_r) @ d_s.to_track_quat("Z", "Y").to_matrix().to_4x4()
        _bm_foglia(bm, d_s.length, h_body * 0.105, h_body * 0.018, Ms, profilo=prof_spatola, gonfia=1.30)

    _mesh_da_bmesh(f"{name}_patina", col, bm_dark, PATINA_BR)
    return _mesh_da_bmesh(name, col, bm, material)


def statua_angelo_apicale(name, col, x, y, z, h=1.96, corpo=None, ali=None,
                          con_asta=True):
    """Statua apicale dell'Angelo Annunciante / Vittorioso del Duomo di Siena,
    rifinita sui dettagli ad alto contrasto plastico di cmp_angel.jpg:
    - Veste classica profondamente scavata con ombre nette verticali/diagonali e
      solco d'ombra centrale profondo tra la gamba destra avanzata e la sinistra
    - Manto drappeggiato sui fianchi con profonde tasche d'ombra
    - Volto ovale classico con lunghi capelli ondulati ricadenti sulle spalle."""
    corpo = corpo or PIETRA
    ali = ali or VERDE_RAME
    k = h
    bm = bmesh.new()
    M = Matrix.Translation((x, y, z)) @ Matrix.Diagonal((k, k, k, 1.0))

    # Piedi scolpiti sul cuscino fogliato
    for sx_f, dy_f in ((-0.052, -0.048), (0.052, -0.022)):
        _bm_sfera(bm, M, sx_f, dy_f, 0.018, 0.034, sx=0.68, sy=1.35, sz=0.48, u=10, v=6)

    # Superficie continua con PROFONDE pieghe scavate ad ombra netta (ampiezza x2.4!)
    nz_cloth, na_cloth = 30, 48
    cloth_rows = []
    for iz in range(nz_cloth + 1):
        tz = iz / nz_cloth
        zz = 0.008 + 0.785 * tz
        if tz < 0.56:
            r_base = 0.132 - 0.018 * (tz / 0.56) + 0.024 * math.exp(-((tz - 0.45) / 0.12) ** 2)
        elif tz < 0.74:
            r_base = 0.114 - 0.012 * math.sin(math.pi * (tz - 0.56) / 0.18)
        else:
            r_base = 0.112 + 0.018 * math.sin(math.pi * 0.5 * (tz - 0.74) / 0.26)

        cx_shift = -0.012 * math.sin(math.pi * tz)
        row = []
        for ia in range(na_cloth):
            a = math.tau * ia / na_cloth
            # Pieghe profonde scavate (generano le righe scure d'ombra netta viste in cmp_angel.jpg!)
            pleat_deep = 0.026 * (1.0 - 0.32 * tz) * math.cos(11.0 * a + 2.6 * tz)
            pleat_sub = 0.012 * (1.0 - 0.25 * tz) * math.sin(21.0 * a - 1.8 * tz)
            # Profondo solco d'ombra centrale anteriore fra le due gambe (a ~ 3*pi/2 = 4.71 rad)
            center_cleft = -0.032 * math.exp(-(((a - 4.74) % math.tau) ** 2) / 0.035) * (1.0 - 0.45 * tz)
            # Ginocchio destro avanzato luminoso (a ~ 4.35 rad)
            knee_push = 0.030 * math.exp(-(((a - 4.35) % math.tau) ** 2) / 0.12) * math.exp(-((tz - 0.34) / 0.16) ** 2)
            # Balza diagonale scolpita del manto sui fianchi (tz ~ 0.48)
            mantle_fold = 0.032 * math.exp(-((tz - (0.48 + 0.12 * math.sin(a + 0.4))) / 0.075) ** 2) * (0.60 + 0.40 * math.cos(3.0 * a))
            rr = max(0.055, r_base + pleat_deep + pleat_sub + center_cleft + knee_push + mantle_fold)
            px_c = cx_shift + rr * math.cos(a)
            py_c = rr * math.sin(a) * 0.74
            row.append(bm.verts.new(M @ Vector((px_c, py_c, zz))))
        cloth_rows.append(row)

    for iz in range(nz_cloth):
        for ia in range(na_cloth):
            ia2 = (ia + 1) % na_cloth
            bm.faces.new((cloth_rows[iz][ia], cloth_rows[iz][ia2], cloth_rows[iz + 1][ia2], cloth_rows[iz + 1][ia]))
    bm.faces.new(list(reversed(cloth_rows[0])))
    bm.faces.new(cloth_rows[-1])

    # Lembi pendenti laterali e piega obliqua sul torace
    for s_dr, z_dr, rot_dr in ((-1, 0.54, 2.76), (1, 0.52, -2.70)):
        _bm_foglia(
            bm, 0.28, 0.10, 0.038,
            M @ Matrix.Translation((s_dr * 0.120, -0.025, z_dr)) @ Matrix.Rotation(rot_dr, 4, "Y"),
            piega=0.14 * s_dr, gonfia=1.20,
        )

    # Spalle snelle e collo allungato classico
    _bm_sfera(bm, M, 0.0, -0.008, 0.785, 0.082, sx=1.48, sy=0.76, sz=0.52, u=18, v=10)
    _bm_segmento(bm, M, (0.0, -0.008, 0.795), (0.0, -0.016, 0.862), 0.034, 0.031, seg=12)

    # Testa ovale slanciata (NON tonda!), con orbite scavate e lunghi capelli dritti fino alle spalle!
    Mh = M @ Matrix.Translation((-0.005, -0.020, 0.922)) @ Matrix.Rotation(0.14, 4, "X") @ Matrix.Rotation(-0.07, 4, "Z")
    _bm_sfera(bm, Mh, 0.0, 0.0, 0.0, 0.068, sx=0.76, sy=0.92, sz=1.14, u=20, v=14)
    for es in (-1, 1):
        _bm_sfera(bm, Mh, es * 0.021, -0.058, 0.016, 0.014, sx=1.20, sy=0.45, sz=0.35, u=8, v=5)
        _bm_sfera(bm, Mh, es * 0.025, -0.052, -0.010, 0.017, sx=0.80, sy=0.55, sz=0.65, u=8, v=5)
    _bm_segmento(bm, Mh, (0.0, -0.060, 0.016), (0.0, -0.074, -0.014), 0.0085, 0.011, seg=6)
    # Ciocche verticali lunghe ai due lati del volto (creano le due bande scure ai lati del viso in cmp_angel.jpg!)
    _bm_sfera(bm, Mh, 0.0, 0.012, 0.024, 0.071, sx=0.84, sy=0.98, sz=0.98, u=16, v=10)
    for hs in (-1, 1):
        for hk in range(3):
            _bm_segmento(
                bm, Mh,
                (hs * (0.046 + 0.008 * hk), -0.018 + 0.022 * hk, 0.032),
                (hs * (0.052 + 0.010 * hk), -0.014 + 0.022 * hk, -0.092),
                0.015, 0.012, seg=7,
            )

    # Braccio destro levato a impugnare l'asta + braccio sinistro piegato sul fianco
    _bm_segmento(bm, M, (-0.115, -0.016, 0.775), (-0.175, -0.046, 0.935), 0.040, 0.032, seg=10)
    _bm_segmento(bm, M, (-0.175, -0.046, 0.935), (-0.155, -0.060, 1.125), 0.030, 0.024, seg=10)
    _bm_sfera(bm, M, -0.152, -0.064, 1.140, 0.026, sx=0.95, sy=0.90, sz=1.12, u=10, v=7)
    _bm_foglia(
        bm, 0.20, 0.088, 0.035,
        M @ Matrix.Translation((-0.155, -0.030, 0.905)) @ Matrix.Rotation(math.pi * 0.95, 4, "Y"),
        gonfia=1.15,
    )

    _bm_segmento(bm, M, (0.118, -0.015, 0.772), (0.156, -0.038, 0.635), 0.038, 0.030, seg=10)
    _bm_segmento(bm, M, (0.156, -0.038, 0.635), (0.122, -0.070, 0.515), 0.029, 0.022, seg=10)
    _bm_sfera(bm, M, 0.116, -0.076, 0.502, 0.025, sx=0.95, sy=0.90, sz=1.10, u=10, v=7)

    # Sottosquadri patinati profondi su volto, chioma, petto, manto e piega centrale tra le gambe
    # (riproducono esattamente il chiaroscuro scultoreo di cmp_angel.jpg LEFT!)
    bm_ang_pat = bmesh.new()
    for es in (-1, 1):
        _bm_sfera(bm_ang_pat, Mh, es * 0.021, -0.061, 0.008, 0.011, sx=1.15, sy=0.35, sz=0.55, u=7, v=5)
        _bm_segmento(bm_ang_pat, Mh, (es * 0.044, -0.025, 0.025), (es * 0.048, -0.022, -0.090), 0.011, 0.009, seg=6)
    _bm_sfera(bm_ang_pat, Mh, 0.0, -0.062, -0.028, 0.010, sx=1.20, sy=0.35, sz=0.32, u=7, v=5)
    _bm_sfera(bm_ang_pat, M, 0.0, -0.048, 0.840, 0.026, sx=1.25, sy=0.45, sz=0.45, u=8, v=5)
    # Balza arquata sul petto + profonde pieghe a V del manto sui fianchi + solco centrale gambe
    dark_folds = (
        ((-0.072, -0.088, 0.675), (0.0, -0.098, 0.715), 0.011, 0.011),
        ((0.0, -0.098, 0.715), (0.072, -0.086, 0.665), 0.011, 0.011),
        ((-0.092, -0.088, 0.545), (-0.012, -0.105, 0.420), 0.014, 0.011),
        ((0.088, -0.086, 0.535), (-0.008, -0.105, 0.405), 0.013, 0.010),
        ((-0.078, -0.092, 0.455), (-0.048, -0.096, 0.145), 0.013, 0.009),
        ((0.006, -0.084, 0.415), (0.012, -0.088, 0.045), 0.015, 0.012),
        ((0.068, -0.085, 0.445), (0.062, -0.082, 0.085), 0.012, 0.009),
    )
    for pf0, pf1, pr0, pr1 in dark_folds:
        _bm_segmento(bm_ang_pat, M, pf0, pf1, pr0, pr1, seg=7)
    _mesh_da_bmesh(name + "_patina", col, bm_ang_pat, PATINA)

    obj = _mesh_da_bmesh(name + "_corpo", col, bm, corpo)

    # Lancia obliqua con cuspide lanceolata ben visibile nel cielo blu
    if con_asta:
        bm_sp = bmesh.new()
        _bm_segmento(bm_sp, M, (-0.102, -0.062, 0.520), (-0.238, -0.064, 1.660), 0.011, 0.0085, seg=8)
        _bm_lathe(
            bm_sp,
            M @ Matrix.Translation((-0.238, -0.064, 1.660)) @ Matrix.Rotation(-0.112, 4, "Y"),
            ((0.0, 0.011), (0.032, 0.026), (0.088, 0.017), (0.155, 0.003)),
            seg=10, sy=0.55,
        )
        _mesh_da_bmesh(name + "_lancia", col, bm_sp, ali)

    ala_angelo(f"{name}_ala_-1", col, x - 0.042 * k, y + 0.035 * k, z + 0.785 * k, -1, k, ali, rialzata=True)
    ala_angelo(f"{name}_ala_1", col, x + 0.042 * k, y + 0.035 * k, z + 0.775 * k, 1, k, ali, rialzata=False)
    return obj


# =============================================================================
# 6. CUSPIDE CENTRALE: TIMPANO SCOLPITO, MOSAICO DELL'INCORONAZIONE E ANGELO
#    Geometria calibrata fotogrammetricamente su riferimento_apice.jpg:
#    - Cuspide tra i due pilastri polistili: W = 8,80 m x H = 8,12 m (61,1°)
#    - Campo aureo del mosaico dell'Incoronazione: W = 7,18 m x H = 6,62 m
#    - Cornice modanata spiovente a mitra sull'asse x = 0 (dentellatura fitta +
#      gola profonda con mensole/cubetti fogliati d'acanto + toro perlinato +
#      21 gattoni trilobati per falda)
#    - Ghirlanda 3D ad altorilievo marmoreo direttamente sul bordo aureo:
#      cherubino di chiave, angeli superiori, 6 coppie di cherubini e tralci,
#      angeli angolari e alla base 6 cherubini alternati a 7 gigli senesi
#    - Capitello pensile quadrato corinzio-gotico a foglie d'acanto, abaco bianco
#      gradonato, zoccolo scolpito e statua apicale dell'Angelo con ali in rame.
# =============================================================================
W_TIMP = DIM.get("larghezza_timpano_centrale", 8.80)
H_TIMP = DIM.get("altezza_timpano_centrale", 8.12)
W_MOS = DIM.get("larghezza_mosaico_centrale", 7.18)
H_MOS = DIM.get("altezza_mosaico_centrale", 6.62)
Z_TIMP_FRONTE = Z_TIMPANO + 0.56
Z_APICE = Z_TIMP_FRONTE + H_TIMP
Z_MOS_BASE = Z_TIMP_FRONTE + 0.16
Z_MOS_TOP = Z_MOS_BASE + H_MOS
Y_MOS = -1.36

# --- 6.1 Trabeazione orizzontale da pilastro a pilastro: mensoline al sole e dentellatura a tastiera ---
W_TRAB = DIM.get("larghezza_trabeazione_timpano", 8.80)
box("Trabeazione_Timpano_Centrale", S, 0.0, -0.52, Z_TIMPANO + 0.28, W_TRAB + 0.30, 2.26, 0.56, BIANCO2)
box("Ombra_Mensole_Timp", D, 0.0, -1.56, Z_TIMPANO + 0.14, W_TRAB, 0.12, 0.20, SCURO)
box("Ombra_Dentelli_Timp", D, 0.0, -1.58, Z_TIMPANO + 0.41, W_TRAB, 0.12, 0.12, SCURO)

bm_trab_w = bmesh.new()
bm_trab_p = bmesh.new()
Mt = Matrix.Identity(4)
# Architrave inferiore luminoso, toro mediano e cornicione superiore calibrati SENZA gettare ombra sui dentelli!
_bm_box(bm_trab_w, Mt, 0.0, -1.625, Z_TIMPANO + 0.02, W_TRAB, 0.22, 0.075)
_bm_box(bm_trab_w, Mt, 0.0, -1.635, Z_TIMPANO + 0.28, W_TRAB, 0.24, 0.085)
_bm_box(bm_trab_w, Mt, 0.0, -1.655, Z_TIMPANO + 0.51, W_TRAB + 0.06, 0.28, 0.095)
# 48 mensoline scolpite ben esposte al sole (y = -1.645 -> pieno sole sulle fronti, ombra netta fra una e l'altra!)
n_mens = 48
for k_m in range(n_mens):
    mx_t = -(W_TRAB * 0.5 - 0.08) + k_m * ((W_TRAB - 0.16) / (n_mens - 1))
    _bm_box(bm_trab_p, Mt, mx_t, -1.635, Z_TIMPANO + 0.145, 0.088, 0.16, 0.155)
    _bm_sfera(bm_trab_p, Mt, mx_t, -1.665, Z_TIMPANO + 0.175, 0.042, sx=0.95, sy=0.75, sz=0.75, u=8, v=5)
    _bm_foglia(bm_trab_w, 0.115, 0.052, 0.028,
               Mt @ Matrix.Translation((mx_t, -1.724, Z_TIMPANO + 0.085)),
               profilo=((0.0, 0.26), (0.25, 0.48), (0.55, 0.50),
                        (0.78, 0.32), (1.0, 0.03)), gonfia=1.20)
# 96 dentelli bianchi fittissimi in pieno sole (effetto tastiera bianco/nero identico a cmp_lower.jpg!)
n_dent = 96
for k_d in range(n_dent):
    dx_t = -(W_TRAB * 0.5 - 0.04) + k_d * ((W_TRAB - 0.08) / (n_dent - 1))
    _bm_box(bm_trab_w, Mt, dx_t, -1.648, Z_TIMPANO + 0.405, 0.048, 0.14, 0.098)
# Fascia a ovoli e dardi fra toro e dentelli (v2.5: in fotografia un
# fregio a ovuli corre per tutta la trabeazione sopra le mensole).
_bm_box(bm_trab_w, Mt, 0.0, -1.672, Z_TIMPANO + 0.345, W_TRAB, 0.055, 0.078)
n_ov = 92
for k_ov in range(n_ov):
    ox_t = -(W_TRAB * 0.5 - 0.06) + k_ov * ((W_TRAB - 0.12) / (n_ov - 1))
    _bm_sfera(bm_trab_p, Mt, ox_t, -1.705, Z_TIMPANO + 0.348, 0.033,
              sx=0.72, sy=0.58, sz=1.06, u=8, v=6)
    if k_ov < n_ov - 1:
        _bm_cono(bm_trab_p, Mt, ox_t + (W_TRAB - 0.12) / (n_ov - 1) * 0.5,
                 -1.698, Z_TIMPANO + 0.345, 0.004, 0.013, 0.062, seg=6)
# Soglia modanata e perlinata alla base del campo aureo del mosaico
_bm_box(bm_trab_w, Mt, 0.0, -1.52, Z_MOS_BASE - 0.045, W_MOS + 0.50, 0.26, 0.085)
for kp_b in range(96):
    px_b = -(W_MOS * 0.5) + kp_b * (W_MOS / 95.0)
    _bm_sfera(bm_trab_p, Mt, px_b, -1.56, Z_MOS_BASE - 0.095, 0.021, u=7, v=5)
_mesh_da_bmesh("Trabeazione_Modanature_Bianche", D, bm_trab_w, BIANCO)
_mesh_da_bmesh("Trabeazione_Mensole_Scolpite", D, bm_trab_p, PIETRA_RIL)
# Scacchiera cosmatesca a due ordini immediatamente sotto il fregio dei
# cherubini (v2.5): e' la banda bianco/verde-scuro ben visibile in
# fotografia fra cherubini e dentelli, prima assente (la trabeazione
# leggeva come semplice modanatura bianca).
bm_check_chiaro = bmesh.new()
bm_check_scuro = bmesh.new()
z_check0 = Z_TIMPANO + 0.562
quad, alt_q = 0.060, 0.035
n_check = int(W_TRAB / quad)
for riga_q in range(2):
    for k_q in range(n_check):
        bm_q = bm_check_scuro if (k_q + riga_q) % 2 == 0 else bm_check_chiaro
        _bm_box(bm_q, Mt, -W_TRAB * 0.5 + (k_q + 0.5) * quad, -1.662,
                z_check0 + alt_q * (riga_q + 0.5), quad * 0.94, 0.040, alt_q * 0.92)
_mesh_da_bmesh("Trabeazione_Scacchiera_Chiara", D, bm_check_chiaro, BIANCO)
_mesh_da_bmesh("Trabeazione_Scacchiera_Scura", D, bm_check_scuro, VERDE)

# --- 6.2 Corpo murario arretrato della cuspide e Mosaico dell'Incoronazione a pieno campo aureo ---
prism("Timpano_Centrale_Struttura", S, 0.0, 0.05, Z_TIMP_FRONTE - 0.10, W_TIMP + 0.36, H_TIMP + 0.10, 2.30, BIANCO)
prism("Mosaico_Centrale_Reale", S, 0.0, Y_MOS, Z_MOS_BASE, W_MOS, H_MOS, 0.10, MOS_C, mosaic_uv=True)

# --- 6.3 Cornici modanate degli spioventi tagliate a mitra sull'asse x = 0 ---
SIN_T, L_TIMP = _angolo_spiovente(W_TIMP, H_TIMP)
NZ_TIMP = -(W_TIMP * 0.5) / L_TIMP
O_END = (Z_MOS_TOP - Z_APICE) * NZ_TIMP

FASCIA_PROFILO = (
    (0.000, 0.175, -1.67, 0.44, BIANCO),   # cordolo esterno dei gattoni
    (0.175, 0.305, -1.49, 0.24, SCURO),    # canale profondo in ombra dei dentelli
    (0.305, 0.415, -1.64, 0.40, BIANCO),   # toro/listello sporgente luminoso
    (0.415, 0.730, -1.43, 0.20, SCURO),    # grande gola scura dei cubetti d'acanto
    (0.730, 0.855, -1.61, 0.36, BIANCO),   # astragalo e listello interno
    (0.855, 1.015, -1.55, 0.30, BIANCO2),  # battuta interna sul campo aureo del mosaico
)
for s in (-1, 1):
    for k_f, (f0, f1, y_f, dep, mat_f) in enumerate(FASCIA_PROFILO):
        banda_mitrata(
            f"Fascia_Timp_{s}_{k_f}", D, s, W_TIMP, H_TIMP,
            f0 * O_END, f1 * O_END, y_f, dep, mat_f, z_base=Z_TIMP_FRONTE,
        )

    tilt_s = -s * math.atan2(W_TIMP * 0.5, H_TIMP)
    bm_sp_w = bmesh.new()
    bm_sp_p = bmesh.new()

    # 1) Dentellatura obliqua fittissima (108 dentelli netti su fondo scuro per falda!)
    n_sd = 108
    for i in range(n_sd):
        u = 0.008 + 0.984 * i / (n_sd - 1)
        px, pz = punto_fascia(s, W_TIMP, H_TIMP, 0.240 * O_END, u, Z_TIMP_FRONTE)
        _bm_box(bm_sp_w, Mt, px, -1.605, pz, 0.072, 0.14, 0.044, rot=Matrix.Rotation(tilt_s, 4, "Y"))

    # 2) Mensole / cubetti fogliati d'acanto in forte aggetto nella gola scura (36 per falda!)
    n_boss = 36
    for i in range(n_boss):
        u = 0.015 + 0.968 * i / (n_boss - 1)
        px, pz = punto_fascia(s, W_TIMP, H_TIMP, 0.575 * O_END, u, Z_TIMP_FRONTE)
        Mb = Matrix.Translation((px, -1.565, pz)) @ Matrix.Rotation(tilt_s, 4, "Y")
        _bm_box(bm_sp_p, Mb, 0.0, 0.03, 0.0, 0.145, 0.15, 0.115)
        for fl_s in (-1, 0, 1):
            _bm_foglia(
                bm_sp_p, 0.145, 0.075, 0.058,
                Mb @ Matrix.Translation((0.0, -0.045, fl_s * 0.036)) @ Matrix.Rotation(math.pi * 0.5 + s * 0.15, 4, "Y"),
                gonfia=1.30,
            )

    # 3) Perlinatura sull'astragalo interno
    for i in range(118):
        u = 0.010 + 0.980 * i / 117.0
        px, pz = punto_fascia(s, W_TIMP, H_TIMP, 0.800 * O_END, u, Z_TIMP_FRONTE)
        _bm_sfera(bm_sp_w, Mt, px, -1.625, pz, 0.020, u=7, v=5)

    _mesh_da_bmesh(f"Dentelli_Spiovente_{s}", D, bm_sp_w, BIANCO)
    _mesh_da_bmesh(f"Cubetti_Acanto_Spiovente_{s}", D, bm_sp_p, PIETRA)

    # 4) 21 Gattoni rampanti trilobati sul cordolo esterno (nessuna collisione coi pilastri!)
    crocchi_spiovente(
        f"Crocket_Timp_{s}", D, s, W_TIMP, H_TIMP, Z_TIMP_FRONTE,
        -1.67, n=21, size=0.355, offset=0.012, taper=0.80, gonfia=1.22,
    )

# --- 6.4 Ghirlanda 3D ad altorilievo marmoreo lungo tutti e tre i lati del campo aureo ---
bm_garland = bmesh.new()
bm_gar_pat = bmesh.new()
bm_gar_sh = bmesh.new()
Y_GAR = -1.435

def _add_cherub_with_shadow(px, py, pz, r, ali=1.15, tilt=0.0, ali_su=False):
    _add_testa_cherubino(bm_garland, px, py, pz, r, ali=ali, tilt=tilt, ali_su=ali_su, bm_pat=bm_gar_pat)
    Ms = Matrix.Translation((px, Y_MOS - 0.012, pz)) @ Matrix.Rotation(tilt, 4, "Y")
    _bm_sfera(bm_gar_sh, Ms, 0.0, 0.0, 0.0, r * 1.14, sx=1.52 * ali, sy=0.08, sz=1.06, u=12, v=6)

# A) Cherubino monumentale di chiave all'apice interno del mosaico + gigli superiori
_add_cherub_with_shadow(0.0, Y_GAR - 0.02, Z_MOS_TOP - 0.36, 0.180, ali=1.35, ali_su=True)
for s in (-1, 1):
    _add_giglio_rilievo(bm_garland, s * 0.22, Y_GAR, Z_MOS_TOP - 0.68, h=0.33, tilt=-s * 0.45)

# B) Fregio inclinato aderente alla cornice interna (ZERO spazio vuoto all'esterno dei cherubini!):
#    6 coppie di cherubini alati + 5 gigli senesi lungo ciascuno spiovente
O_GAR = O_END + 0.128
for s in (-1, 1):
    tilt_g = -s * math.atan2(W_TIMP * 0.5, H_TIMP)
    n_side_items = 11
    for i in range(n_side_items):
        u = 0.085 + 0.815 * i / (n_side_items - 1)
        px, pz = punto_fascia(s, W_TIMP, H_TIMP, O_GAR, u, Z_TIMP_FRONTE)
        if i % 2 == 0:
            sc_i = 1.14 if i == n_side_items - 1 else 1.0
            _add_cherub_with_shadow(px, Y_GAR - 0.015, pz, 0.168 * sc_i, ali=1.20, tilt=tilt_g)
        else:
            _add_giglio_rilievo(bm_garland, px, Y_GAR, pz - 0.05, h=0.36, tilt=tilt_g)

# C) Grandi rilievi angolari ai due vertici bassi + 6 Cherubini e 7 Gigli senesi aderenti alla soglia!
# (v2.5: teste e ali ingrandite — in fotografia il fregio alla base del
# mosaico e' fitto, le ali dei cherubini quasi si toccano e i gigli
# riempiono gli intervalli; prima le testine leggevano rade e minute)
z_base_gar = Z_MOS_BASE + 0.155
for s in (-1, 1):
    _add_cherub_with_shadow(s * 3.16, Y_GAR - 0.015, z_base_gar + 0.05, 0.196, ali=1.28, tilt=-s * 0.32, ali_su=True)

n_ch_base = 6
span_base_ch = 5.50
step_base_ch = span_base_ch / (n_ch_base - 1)
for k_c in range(n_ch_base):
    xc = -span_base_ch * 0.5 + k_c * step_base_ch
    _add_cherub_with_shadow(xc, Y_GAR - 0.02, z_base_gar, 0.208, ali=1.34, tilt=0.0)
for k_g in range(n_ch_base - 1):
    xg = -span_base_ch * 0.5 + (k_g + 0.5) * step_base_ch
    _add_giglio_rilievo(bm_garland, xg, Y_GAR, z_base_gar - 0.075, h=0.40, tilt=0.0)

_mesh_da_bmesh("Ghirlanda_Mosaico_Cherubini_Gigli", D, bm_garland, PIETRA_RIL)
_mesh_da_bmesh("Ghirlanda_Mosaico_Patina", D, bm_gar_pat, PATINA)
_mesh_da_bmesh("Ghirlanda_Mosaico_Sottosquadro", D, bm_gar_sh, SCURO)

# --- 6.5 Capitello pensile quadrato corinzio-gotico slanciato, abaco bianco e zoccolo scolpito ---
bm_cap_p = bmesh.new()
bm_cap_w = bmesh.new()
Y_AP = -1.24

# Campana corinzio-gotica snella che nasce dal vertice delle cornici (cmp_angel.jpg!)
_bm_lathe(
    bm_cap_p, Matrix.Translation((0.0, Y_AP, Z_APICE - 0.42)),
    ((0.00, 0.19), (0.20, 0.24), (0.42, 0.30), (0.62, 0.34), (0.72, 0.29)),
    seg=16, sy=0.92, rib=0.10, rib_n=8,
)
# Quattro grandi volute/foglie d'acanto angolari verticali + 4 mediane (senza sfere a grappolo!)
for ka in range(8):
    aa = math.tau * ka / 8.0 + math.pi * 0.25
    is_corner = (ka % 2 == 0)
    tilt_a = 0.26 if is_corner else 0.18
    la = 0.58 if is_corner else 0.46
    wa = 0.22 if is_corner else 0.18
    da = Vector((math.sin(tilt_a) * math.cos(aa), math.sin(tilt_a) * math.sin(aa) * 0.92, math.cos(tilt_a)))
    Ma = (
        Matrix.Translation((0.21 * math.cos(aa), Y_AP + 0.20 * math.sin(aa), Z_APICE - 0.32))
        @ da.to_track_quat("Z", "Y").to_matrix().to_4x4()
    )
    _bm_foglia(
        bm_cap_p, la, wa, 0.065, Ma,
        profilo=((0.00, 0.30), (0.25, 0.44), (0.58, 0.50), (0.84, 0.40), (0.96, 0.22), (1.00, 0.05)),
        piega=0.22 if is_corner else 0.12, gonfia=1.35,
    )

# Sottili tiranti in ferro battuto visibili ai fianchi del capitello
for s_ir in (-1, 1):
    box(f"Tirante_Ferro_Capitello_{s_ir}", D, s_ir * 0.36, Y_AP - 0.14, Z_APICE - 0.12, 0.016, 0.016, 0.58, FERRO)

# Abaco e plinto bianco squadrato luminoso con ombra netta sottostante (Z_APICE + 0.28 .. +0.58)
_bm_box(bm_cap_w, Mt, 0.0, Y_AP, Z_APICE + 0.33, 0.88, 0.84, 0.09)
_bm_box(bm_cap_p, Mt, 0.0, Y_AP, Z_APICE + 0.40, 0.74, 0.70, 0.06)
_bm_box(bm_cap_w, Mt, 0.0, Y_AP, Z_APICE + 0.49, 0.68, 0.64, 0.13)

# Cuscino scolpito a foglie d'acanto patinate direttamente sotto i piedi dell'Angelo (Z_APICE + 0.55 .. +0.80)
_bm_box(bm_cap_p, Mt, 0.0, Y_AP, Z_APICE + 0.68, 0.48, 0.46, 0.25)
for kz in range(10):
    az = math.tau * kz / 10.0
    dz = Vector((0.30 * math.cos(az), 0.30 * math.sin(az), 0.95))
    Mz = Matrix.Translation((0.20 * math.cos(az), Y_AP + 0.19 * math.sin(az), Z_APICE + 0.56)) @ dz.to_track_quat("Z", "Y").to_matrix().to_4x4()
    _bm_foglia(bm_cap_p, 0.24, 0.13, 0.048, Mz, piega=0.14, gonfia=1.35)

_mesh_da_bmesh("Capitello_Apice_Scolpito", G, bm_cap_p, PIETRA_RIL)
_mesh_da_bmesh("Abaco_Pedestallo_Angelo", G, bm_cap_w, BIANCO)

statua_angelo_apicale("Angelo_Apicale", ST, 0.0, Y_AP, Z_APICE + 0.80, h=1.96)

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
        box(f"Marcapiano_Torre_{tag}_{zm_t}", G, side * 12.35, -0.35, zm_t, 4.65, 2.65, 0.16, BIANCO2)

    # Tre ordini di finestre gotiche sovrapposte nella campata interna (con ghimberga bicroma!)
    for idx_w, (zw0, wh) in enumerate([(9.35, 3.30), (13.45, 3.55), (17.95, 3.35)]):
        box(f"Finestra_Vano_{tag}_{idx_w}", D, xi, -1.72, zw0 + wh * 0.45, 0.96, 0.24, wh * 0.85, SCURO)
        prism(f"Finestra_ArcoScuro_{tag}_{idx_w}", D, xi, -1.72, zw0 + wh * 0.86, 0.96, 0.68, 0.24, SCURO)
        colonna_ritorta(f"Mullion_Torre_{tag}_{idx_w}", D, xi, -1.92, zw0 + wh * 0.42, 0.075, wh * 0.82, BIANCO, turns=3.0)
        arch(f"Arco_Fin_Bianco_{tag}_{idx_w}", D, xi, -1.96, zw0 + wh * 0.84, 0.54, 0.095, BIANCO, seg_u=18, pointed=0.45)
        arch(f"Arco_Fin_Prato_{tag}_{idx_w}", D, xi, -1.98, zw0 + wh * 0.86, 0.68, 0.085, VERDE, seg_u=18, pointed=0.45)
        spioventi_modanati(f"Ghim_Fin_{tag}_{idx_w}", D, xi, -2.00, zw0 + wh * 0.84, 1.72, 1.25, 0.13, 0.28, BIANCO)

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
    box(f"Cornicione_Torre_{tag}", G, side * 12.70, -0.25, z_top_tower, 4.35, 2.65, 0.20, BIANCO2)
    # Coronamento a ghimberga: la finestra termina con un profilo acuto,
    # non con la grande mensola orizzontale della versione precedente.
    for band, inset in enumerate((0.0, 0.24)):
        spioventi_modanati(f"Coronamento_Ogivale_{tag}_{band}", G,
                           xi, -1.99 - band * 0.04, z_top_tower - 0.85 + inset,
                           2.85 - inset * 2, 2.15 - inset * 1.4,
                           0.13 if band == 0 else 0.075, 0.22, BIANCO)
    foglie_rampanti(f"Coronamento_Foglie_{tag}", G, xi, -2.06,
                    z_top_tower - 0.85, 2.85, 2.15, n=6, size=0.18)
    for dx in (-1.37, 1.37):
        cyl(f"Coronamento_Colonnina_{tag}_{dx}", G,
            xi + dx, -1.90, z_top_tower - 1.20, 0.095, 1.45, BIANCO)
        finial(f"Coronamento_Guglia_{tag}_{dx}", G,
               xi + dx, -1.90, z_top_tower - 0.45, 0.65)
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
w_bg_cam = wnodes.new("ShaderNodeBackground")
w_bg_gi = wnodes.new("ShaderNodeBackground")
w_mix_shader = wnodes.new("ShaderNodeMixShader")
w_lp = wnodes.new("ShaderNodeLightPath")
w_mix = wnodes.new("ShaderNodeMixRGB")
w_sep = wnodes.new("ShaderNodeSeparateXYZ")
w_tc = wnodes.new("ShaderNodeTexCoord")
w_ramp = wnodes.new("ShaderNodeValToRGB")
w_ramp.color_ramp.elements[0].position = 0.04
w_ramp.color_ramp.elements[1].position = 0.42
w_mix.inputs["Color1"].default_value = (*WORLD.get("horizon_color", (0.048, 0.145, 0.340)), 1.0)
w_mix.inputs["Color2"].default_value = (*WORLD.get("sky_color", (0.012, 0.068, 0.215)), 1.0)
w_bg_cam.inputs["Strength"].default_value = WORLD.get("sky_strength", 1.0)
w_bg_gi.inputs["Color"].default_value = (*WORLD.get("bounce_color", (0.310, 0.385, 0.560)), 1.0)
w_bg_gi.inputs["Strength"].default_value = WORLD.get("bounce_strength", 0.55)
wlinks.new(w_tc.outputs["Generated"], w_sep.inputs["Vector"])
wlinks.new(w_sep.outputs["Z"], w_ramp.inputs["Fac"])
wlinks.new(w_ramp.outputs["Color"], w_mix.inputs["Fac"])
wlinks.new(w_mix.outputs["Color"], w_bg_cam.inputs["Color"])
wlinks.new(w_lp.outputs["Is Camera Ray"], w_mix_shader.inputs["Fac"])
wlinks.new(w_bg_gi.outputs["Background"], w_mix_shader.inputs[1])
wlinks.new(w_bg_cam.outputs["Background"], w_mix_shader.inputs[2])
wlinks.new(w_mix_shader.outputs["Shader"], w_out.inputs["Surface"])

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
# Override opzionali da ambiente, utili per prove rapide senza toccare il JSON:
#   CHIESA_SAMPLES=16 CHIESA_RES_X=450 CHIESA_RES_Y=525 CHIESA_NO_GLB=1 python genera_facciata.py
scene.render.engine = RENDER.get("engine", "CYCLES")
# Filmic (invece di AgX) conserva la saturazione dei mosaici dorati: con AgX
# l'oro e i rossi delle vesti si desaturano e il mosaico legge slavato.
try:
    scene.view_settings.view_transform = "Filmic"
except Exception:
    pass
scene.view_settings.exposure = 0.0
scene.cycles.samples = int(os.environ.get("CHIESA_SAMPLES", RENDER.get("samples", 64)))
scene.cycles.device = RENDER.get("device", "CPU")
scene.cycles.use_denoising = bool(RENDER.get("use_denoising", True))
scene.render.resolution_x = int(os.environ.get("CHIESA_RES_X", RENDER.get("resolution_x", 900)))
scene.render.resolution_y = int(os.environ.get("CHIESA_RES_Y", RENDER.get("resolution_y", 1050)))
scene.render.filepath = PNG_PATH

bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH, compress=True)
print(f"Salvato: {BLEND_PATH} | oggetti: {len(scene.objects)} | materiali: {len(bpy.data.materials)}")

if os.environ.get("CHIESA_NO_RENDER"):
    print("Render anteprima saltato (CHIESA_NO_RENDER).")
else:
    try:
        # CHIESA_SOLO_GALLERIA=1 salta le prime due viste (prove rapide
        # sulla fascia dei Profeti senza rifare gli altri render).
        _solo_galleria = bool(os.environ.get("CHIESA_SOLO_GALLERIA"))
        _solo_rosone = bool(os.environ.get("CHIESA_SOLO_ROSone"))
        _salta_tutto = _solo_galleria or _solo_rosone
        if not _salta_tutto:
            bpy.ops.render.render(write_still=True)
            print(f"Anteprima salvata: {PNG_PATH}")
        # Seconda inquadratura teleobiettivo dedicata alla cuspide centrale,
        # calibrata esattamente sul taglio e sulla prospettiva di riferimento_apice.jpg:
        # include la galleria superiore dei Profeti (z ~ 22.0 m), i pilastri gotici con
        # edicole traforate e statue sommitali, il mosaico dell'Incoronazione e l'Angelo.
        camera_loc_main = cam.location.copy()
        camera_rot_main = cam.rotation_euler.copy()
        lens_main = cam.data.lens
        res_main = (scene.render.resolution_x, scene.render.resolution_y)
        if not _salta_tutto:
            target_detail = Vector((-0.12 * SCALA, -1.40 * SCALA, 28.98 * SCALA))
            cam.location = (-0.50 * SCALA, -34.5 * SCALA, 16.5 * SCALA)
            cam.rotation_euler = (target_detail - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 80.5
            scene.render.resolution_x = int(os.environ.get("CHIESA_APICE_RES_X", 900))
            scene.render.resolution_y = int(os.environ.get("CHIESA_APICE_RES_Y", 1022))
            scene.render.filepath = APICE_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Anteprima ravvicinata dell'apice salvata: anteprima_apice.png")

        # Terza inquadratura: fascia esatta richiesta (sotto il timpano, sopra il rosone).
        # v2.5: obiettivo abbassato e camera arretrata per includere anche le
        # mezze figure dei pennacchi, come nel taglio della fotografia
        # `riferimento_galleria.jpg` (nella v2.4 restavano fuori campo).
        if not _solo_rosone:
            target_galleria = Vector((0.0, -1.50 * SCALA, 23.25 * SCALA))
            cam.location = (0.0, -22.00 * SCALA, 23.55 * SCALA)
            cam.rotation_euler = (target_galleria - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 46.5
            scene.render.resolution_x = int(os.environ.get("CHIESA_GALLERIA_RES_X", 1600))
            scene.render.resolution_y = int(os.environ.get("CHIESA_GALLERIA_RES_Y", 520))
            scene.render.filepath = GALLERIA_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Dettaglio della galleria salvato: anteprima_galleria.png")

        # Quarta inquadratura (v2.6): il rosone e le statue che lo circondano,
        # inquadrati come nella fotografia di riferimento `riferimento_vetrata.jpg`.
        target_rosone = Vector((0.0, -1.45 * SCALA, (Z_PAN + 0.55) * SCALA))
        cam.location = (0.0, -15.0 * SCALA, (Z_PAN + 0.55) * SCALA)
        cam.rotation_euler = (target_rosone - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.lens = 56.0
        scene.render.resolution_x = int(os.environ.get("CHIESA_ROSone_RES_X", 1100))
        scene.render.resolution_y = int(os.environ.get("CHIESA_ROSone_RES_Y", 1200))
        scene.render.filepath = ROSONE_PNG_PATH
        bpy.ops.render.render(write_still=True)
        print("Dettaglio del rosone salvato: anteprima_rosone.png")

        # Il .blend resta impostato sull'inquadratura generale.
        cam.location = camera_loc_main
        cam.rotation_euler = camera_rot_main
        cam.data.lens = lens_main
        scene.render.resolution_x, scene.render.resolution_y = res_main
        scene.render.filepath = PNG_PATH
    except Exception as e:
        print(f"Render anteprima non riuscito: {e}")

EXPORT = CFG.get("export", {})
if "gltf" in EXPORT.get("formats", []) and not os.environ.get("CHIESA_NO_GLB"):
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

print("Generazione v2.6 completata!")
sys.stdout.flush()
sys.stderr.flush()
if "bpy" in sys.modules and not bpy.app.binary_path:
    # Evita crash del distruttore C++ TBB in uscita quando bpy gira come modulo pip
    os._exit(0)
