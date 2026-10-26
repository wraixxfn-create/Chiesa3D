#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Facciata del Duomo di Siena (fronte ovest) — modello 3D procedurale.

NOTA v4.0: di per se' questo script modella SOLTANTO la facciata (nessun
interno, nessuna navata, nessun edificio laterale).  Prima del salvataggio
viene pero' richiamato `muri_esterni.costruisci_muri_esterni()`, che aggiunge
i muri esterni SEMPLICI del corpo della chiesa, tarati sulla pianta allegata.
Impostare `CHIESA_NO_MURI=1` (o `muri_esterni.attivi: false` nel JSON) per
ottenere come un tempo la sola facciata.  Le anteprime di dettaglio del
fronte nascondono i muri durante il render, restando identiche alla v3.9.

Uso:
  - con Blender:   blender --background --python genera_facciata.py
  - con il modulo bpy (pip):  python genera_facciata.py

Output (nella stessa cartella dello script):
  - Facciata_Duomo_Siena.blend
  - anteprima_facciata.png
  - anteprima_apice.png, anteprima_galleria.png e anteprima_rosone.png
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

AGGIORNAMENTO v2.7 — VETRATA E SCULTURE DEL ROSONE:

  1. Apertura circolare e texture 1536 px letta dall'intera vetrata reale;
     piombo e statua rimossi dalla mappa per campionamento locale. Il vetro
     conserva lastre, graffi e bollicine, con micro-bump e riflesso controllato.
  2. Piombatura sottile realmente davanti al vetro: due montanti, cinque
     traversi e filo perimetrale; niente barre impresse nella fotografia.
  3. Telaio della ghiera corretto (larghezza radiale / profondita' frontale),
     288 foglie d'acanto con costa, 180 dentelli e perlinatura concentrica.
  4. Quattro profeti dei pennacchi a figura intera, con contrapposto, manti a
     doppia superficie, piedi separati e pose indica/parla/rotolo/leggi.
  5. Otto nicchie laterali con catino concavo, costole, ghiere circolari,
     ghimberghe non occlusive e busti piu' grandi in posa differente.
  6. Redentore riproporzionato e raccolto nella posa della fotografia;
     inquadratura allargata a 1453x1582 per comprendere tutte le sculture.

AGGIORNAMENTO v2.8 — LE DUE CUSPIDI DEI MOSAICI (Presentazione e Natività):

  1. Proporzioni vere: i due timpani laterali sono larghi e bassi (H/W ~ 0,68,
     non 1,05), centrati sui settori (-8,05 m / +8,05 m) e appoggiati sul
     cornicione della loggia.  Nella v2.7 erano triangoli troppo acuti, con
     l'apice che si perdeva dietro ai pilastri.
  2. Cornice modanata a mitra al posto di due scatole ruotate: filo esterno
     investito dal sole, canalino dei dentelli, toro con perline, gola,
     secondo toro dentellato e battuta sul campo aureo, tutti con y e
     profondita' coerenti.  Niente piu' "X" di scatole sull'apice.
  3. Gattoni rampanti veri (`_bm_gattone_cuspide`): foglia carnosa lobata che
     si arriccia in fuori con perla terminale e seconda fogliolina alla base,
     sedici per falda, rastremati verso la punta.
  4. Mosaici riletti ad alta risoluzione (1024 px, prima 256): triangolo
     letto quasi per intero, bordi lapidei sostituiti da tessere d'oro,
     contrasto/saturazione riportati e calibrazione fotometrica ambrata,
     cosi' sotto il sole il campo aureo resta oro e non sbianca.
  5. Campo del mosaico arretrato rispetto alla cornice (0,17 m): il risalto
     delle modanature nasce dalla profondita' e il bordo aureo non finisce
     piu' dietro al mosaico come nella v2.7.
  6. Base d'imposta a tre fili sottili con dentelli e perline a sbalzo, dado
     apicale con gola fogliata e statua a figura intera (`statua_gotica_v26`)
     di 0,33 h: prima era una figurina di 1,25 m su un piedistallo pesante.
  7. Nuova inquadratura `anteprima_cuspidi.png` (1600x700) sul taglio della
     fotografia d'insieme: rosone al centro e i due timpani ai lati.

AGGIORNAMENTO v2.9 — I DUE FRONTONI DEI MOSAICI, SECONDO PASSAGGIO:

  1. Nuovo riferimento frontale `riferimento_cuspidi.jpg` (3120x1146): i
     triangoli sono piu' alti e proporzionati (H/W ~ 0,93), non schiacciati.
  2. Presentazione e Nativita' rilette sul filo interno corretto a 1536 px;
     eliminata la banda chiara nel mosaico destro e la doppia correzione
     colore che alterava le vesti. Micro-rilievo delle tessere incorporato.
  3. Otto modanature continue a mitra, dentelli, perline lapidee, nastro di
     foglie e dardi; materiali dedicati mantengono le gole leggibili.
  4. Nove gattoni trilobati per falda, piu' carnosi e senza gambi cilindrici;
     corpo nascosto assottigliato per non mostrare un fianco grigio in vista.
  5. Base arricchita con ovoli/foglie, dentelli e perline; eliminate le
     quattro ghimberghe duplicate fra la cuspide e la loggia.
  6. Apice ricomposto con fiore fogliato, volute, dado basso scanalato e
     statua a figura intera con plinto ridotto e pose piu' raccolte.
  7. `CHIESA_SOLO_CUSPIDI=1` per la prova rapida e inquadratura panoramica
     1800x660 calibrata sullo stesso taglio del riferimento.

AGGIORNAMENTO v3.0 — I DUE TRIANGOLI DEI MOSAICI, TERZO PASSAGGIO:

  1. Mosaici riletti con `_extract_mosaic_laterale_v30`: de-velatura della
     Presentazione (il fondo aureo bruciato dal sole torna oro), contrasto
     e saturazione veri da cartone musivo, albedo scurito per il sole
     diretto di Cycles e grana da tessere incorporata nel colore.  Via
     l'emissione che slavava entrambe le scene: ora la luce e' solo quella
     del sole, come nella fotografia.
  2. Gattoni rifatti come gigli senesi (`_bm_giglio_cuspide`): petalo
     centrale alto, due petali laterali arcuati, sepali ricadenti e
     bottone alla base — otto per falda, grandi come in fotografia.
     Non piu' le piccole «colombe» bianche della v2.9.
  3. Cornice con gole d'ombra vere (materiale di patina fra i fili),
     banda a ovoli e dardi scolpita lungo gli spioventi e perlinatura
     piu' grande e fitta sul campo aureo; i marmi delle cuspidi hanno
     di nuovo AO e pointiness, quindi le modanature si leggono in
     pieno sole invece di restare piatti bianchi.
  4. Apice senza il dado a torretta: lastra bassa, capitello di foglie
     e statue femminili piu' alte e snelle (1,52 m), mano al petto a
     sinistra e mano alzata a destra, come le due figure della foto.
  5. Base con fregio a ovoli e dardi a tutto tondo, fila di perle e
     fascia di serpentino scuro sotto la cornice; via il grande
     pannello rosa piatto sotto i frontoni.

AGGIORNAMENTO v3.3 — LE DUE TORRI AI LATI DELLA CUSPIDE, terzo passaggio,
sulla nuova fotografia frontale allegata (`riferimento_torri.jpg`):

  1. Fusto a lastre di marmo bianco con tre lesene piatte per faccia
     (fronte e fianco esterno): via la gabbia di cinque colonnine rotonde
     su pannelli di marmo rigato rosa scuro della v3.2, che da lontano
     leggeva come un palo a righe.  Restano due sole vene salmone sottili
     in marmo rosato chiaro, interrotte da fasce e registri come in foto.
  2. Un registro grande di DUE lancette cieche con ghimberghe crochettate
     (prima quattro miniature per faccia) e un registro piccolo di tre
     lancette strette sotto la cornice; fasce marcapiano a dente di cane
     al posto delle squame a archetti.
  3. Doccioni zoomorfi protesi in diagonale dagli spigoli a due quote,
     piu' due a mezza altezza della guglia: non piu' stecche laterali.
  4. Coronamento PIENO: via la lanterna traforata con i vani neri, che
     nella fotografia non esiste.  Quattro pinnacoletti diagonali a
     cresta fogliata e bocciolo, guglia centrale interamente coperta di
     gattoni con due figure in nicchia, capitello fogliato a coppa e
     statua sommitale piu' alta (1,42 m).
  5. `CHIESA_SOLO_TORRI=1` ora salta davvero le altre viste (ma tiene
     l'apice) e rigenera anche i primi piani `model_sx.png`/`model_dx.png`;
     nuovo confronto `confronto_torri.png` sulla foto allegata.

AGGIORNAMENTO v3.6 — TRE SOLE MIGLIORIE sotto la zona centrale superiore
(che resta intatta), rilette sulla fotografia d'insieme del Duomo vero:

  1. I TRE PORTALI DI GIOVANNI PISANO.  La quota d'imposta in config
     (12,6 m) non era quella su cui e' disegnato tutto l'ordine
     inferiore (8,45 m): lunette e archivolti galleggiavano 4 m sopra i
     portoni e il prisma pieno della ghimberga li copriva, cosi' nel
     render l'arco finiva "dentro" un triangolo piatto e vuoto.
     Ripristinata l'imposta vera, la lunetta e' ora una semiluna libera
     (sole di San Bernardino al centro, ghirlanda ai lati) e il campo
     della ghimberga e' il pennacchio SOPRA l'estradosso
     (`campo_ghimberga`: triangolo meno il disco dell'arco), con il
     medaglione col busto fra estradosso e apice, come in fotografia.
  2. I DUE TORRIONI ANGOLARI ESTERNI (Sez. 8): doccioni corti, spessi
     e inclinati (prima stecche orizzontali lunghe fino a 1,95 m),
     lancette interne strette e incassate con colonnina tortile (la
     bassa cieca con fondo chiaro), statue a figura intera
     `statua_gotica_v26` su mensole aggettanti sotto baldacchini (via
     le statuine-pedina incollate su rettangoli rosa) e coronamento a
     torretta ottagonale con cuspide e pinnacoli pieni (via la
     lanterna cilindrica "a pedina" arretrata e i finali a spillone).
  3. LA GRADINATA DEL SAGRATO: 14 gradoni PIENI larghi 34 m (prima 13
     lastre sottili da 42 m che in prospettiva leggevano come una
     rampa/lastra grigia), con listello chiaro sul naso e filetto
     d'ombra di serpentino sotto ogni alzata, e una lastra di sagrato
     a chiudere la discesa verso la piazza.

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
CUSPIDI_PNG_PATH = os.path.join(OUT_DIR, "anteprima_cuspidi.png")
TORRI_PNG_PATH = os.path.join(OUT_DIR, "anteprima_torri.png")
CUSPIDI_REF_PATH = os.path.join(OUT_DIR, "riferimento_cuspidi.jpg")
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
scene["nota"] = "Modello procedurale v3.9: tre migliorie sotto la parte centrale superiore — torrioni angolari con archivolti bicromi a cunei su ogni apertura, corona ad arco acuto unico con traforo a quatrifoglio e tiburio a specchiature modanate; portali con raggiera bicroma a pieno campo, fregio su fondo scuro, cornici delle porte aggettanti e medaglioni sporgenti; gradinata a gradoni con naso aggettante e alzata rientrante; retro piatto."


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


def _dist_punto_retta(px, py, a, b):
    """Distanza vettoriale dei punti (px, py) dalla retta passante per a e b."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    ln = max(math.hypot(dx, dy), 1e-6)
    nx, ny = -dy / ln, dx / ln
    return np.abs((px - ax) * nx + (py - ay) * ny)


def _extract_mosaic_laterale_v30(name, topdown_rgb, p_bl, p_br, p_top,
                                  size=1536, riscalda_bianchi=False):
    """Rettifica il mosaico laterale dal dettaglio fotografico frontale (v3.1).

    I tre punti sono sul filo interno esatto del campo musivo.  Rispetto
    alla v3.0: preserva l'equilibrio cromatico RGB delle vesti (il blu
    oltremare del manto della Vergine, il cremisi, il verde smeraldo e il
    viola-indaco del sacerdote non vengono piu' ingialliti dal gain B=0.50),
    compensa la sottile ombra portata della cornice lungo lo spiovente
    destro e restituisce l'oro caldo senese sul fondo bruciato della
    Presentazione mantenendo il velo bianco di Anna e le figure ben staccate.
    """
    v_lin = np.linspace(0.0, 1.0, size, dtype=np.float32)
    vv, uu = np.meshgrid(v_lin, v_lin, indexing="ij")
    s = np.clip((uu - 0.5 * vv) / np.maximum(1.0 - vv, 1e-4), 0.0, 1.0)
    px = (1.0 - vv) * ((1.0 - s) * p_bl[0] + s * p_br[0]) + vv * p_top[0]
    py = (1.0 - vv) * ((1.0 - s) * p_bl[1] + s * p_br[1]) + vv * p_top[1]
    sampled = _bilinear_sample(topdown_rgb, px, py)

    # Schiarisce delicatamente il bordo destro dove nella foto cade l'ombra
    # della cornice lapidea, cosi' l'ombra 3D di Cycles non si raddoppia.
    dist_dx = (1.0 - s) * (1.0 - vv)
    ombra_bordo = np.clip((0.055 - dist_dx) / 0.055, 0.0, 1.0)[:, :, None] * np.clip((vv - 0.18) / 0.25, 0.0, 1.0)[:, :, None]
    sampled = np.clip(sampled * (1.0 + 0.22 * ombra_bordo), 0.0, 1.0)

    # De-velatura e nitidezza locale (figure, volti, aureole e gradini).
    merged = np.clip((sampled - 0.028) / 0.945, 0.0, 1.0)
    acc = np.zeros_like(merged)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            acc += np.roll(np.roll(merged, dy, axis=0), dx, axis=1)
    acc /= 9.0
    merged = np.clip(merged * 1.52 - acc * 0.52, 0.0, 1.0)
    merged = np.clip((merged - 0.5) * 1.10 + 0.5, 0.0, 1.0)

    lum0 = merged.mean(axis=2, keepdims=True)
    sat0 = (merged.max(axis=2, keepdims=True) - merged.min(axis=2, keepdims=True))
    if riscalda_bianchi:
        # Protegge il velo/aureola bianca di Anna (s ~ 0.67, vv ~ 0.47) e la
        # veste chiara di Maria bambina (s ~ 0.36, vv ~ 0.46).
        anna_mask = np.exp(-(((s - 0.67) / 0.11) ** 2 + ((vv - 0.47) / 0.09) ** 2))[:, :, None]
        maria_mask = np.exp(-(((s - 0.36) / 0.08) ** 2 + ((vv - 0.46) / 0.11) ** 2))[:, :, None]
        prot = np.clip(anna_mask + 0.65 * maria_mask, 0.0, 1.0)
        oro_mask = (np.clip((lum0 - 0.60) / 0.24, 0.0, 1.0)
                    * np.clip((0.35 - sat0) / 0.25, 0.0, 1.0)
                    * (1.0 - 0.80 * prot))
        oro_col = np.array((0.97, 0.81, 0.46), dtype=np.float32)[None, None, :] \
            * (0.76 + 0.26 * lum0)
        merged = merged * (1.0 - oro_mask * 0.72) + oro_col * (oro_mask * 0.72)
    else:
        oro_mask = (np.clip((lum0 - 0.55) / 0.26, 0.0, 1.0)
                    * np.clip((0.36 - sat0) / 0.24, 0.0, 1.0))
        oro_col = np.array((0.98, 0.81, 0.44), dtype=np.float32)[None, None, :] \
            * (0.75 + 0.27 * lum0)
        merged = merged * (1.0 - oro_mask * 0.58) + oro_col * (oro_mask * 0.58)

    # Saturazione vivida da cartone musivo ottocentesco.
    lum = merged.mean(axis=2, keepdims=True)
    merged = np.clip(lum + (merged - lum) * (1.28 if riscalda_bianchi else 1.32), 0.0, 1.0)
    merged = np.clip(merged, 0.0, 1.0) ** 1.06

    # Grana fine delle tessere musive nel colore.
    rng = np.random.default_rng(300 if riscalda_bianchi else 301)
    cells = 184
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    row = np.floor(yy * cells / size).astype(np.int32)
    shift = (row % 2) * 0.5
    fx = (xx * cells / size + shift) % 1.0
    fy = (yy * cells / size) % 1.0
    bordo = np.minimum(np.minimum(fx, 1.0 - fx), np.minimum(fy, 1.0 - fy))
    fuga = np.clip(bordo / 0.09, 0.0, 1.0)[:, :, None]
    cell_x = np.floor(xx * cells / size + shift).astype(np.int32)
    tono = rng.uniform(-0.042, 0.042, (cells + 2, cells + 2)).astype(np.float32)
    merged *= (0.93 + 0.07 * fuga) * (1.0 + tono[row % (cells + 2), cell_x % (cells + 2)][:, :, None])

    # Calibrazione fotometrica bilanciata: conserva i blu e i rossi delle vesti
    # e scalda solo la componente aurea sotto il sole diretto di Cycles.
    gain_fig = np.array((0.775, 0.745, 0.705), dtype=np.float32)[None, None, :]
    gain_oro = np.array((0.790, 0.720, 0.560), dtype=np.float32)[None, None, :]
    gain = gain_fig * (1.0 - oro_mask) + gain_oro * oro_mask
    merged = np.clip(merged * gain, 0.0, 1.0)
    return _save_packed_image(name, merged)


def _make_tessere_mosaico_tex(name, size=1024, cells=128, seed=290):
    """Mappa di rilievo non-color di piccole tessere leggermente irregolari."""
    rng = np.random.default_rng(seed)
    yy, xx = np.meshgrid(np.arange(size), np.arange(size), indexing="ij")
    row = np.floor(yy * cells / size).astype(np.int32)
    shift = (row % 2) * 0.5
    fx = (xx * cells / size + shift) % 1.0
    fy = (yy * cells / size) % 1.0
    edge = np.minimum(np.minimum(fx, 1.0 - fx), np.minimum(fy, 1.0 - fy))
    rilievo = np.clip(edge / 0.075, 0.0, 1.0)
    rilievo = 0.18 + 0.72 * rilievo
    cell_x = np.floor(xx * cells / size + shift).astype(np.int32)
    tone = rng.uniform(-0.07, 0.07, (cells + 2, cells + 2))
    rilievo += tone[row % (cells + 2), cell_x % (cells + 2)]
    rgb = np.repeat(np.clip(rilievo, 0.0, 1.0)[:, :, None], 3, axis=2)
    img = _save_packed_image(name, rgb.astype(np.float32))
    img.colorspace_settings.name = "Non-Color"
    return img


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


def _vetro_rosone_da_foto(name, topdown_rgb, size=1536):
    """Lastra del rosone riletta integralmente dalla fotografia di dettaglio.

    La mappatura polare conserva le diverse lastre, le nuvolature, i graffi e
    le piccole bolle del vetro vero.  I montanti e il Redentore, che nella
    foto coprono il vetro, vengono rimossi per campionamento locale: le barre
    sono poi geometria 3D e non un'ombra stampata nella texture.
    """
    img_h, img_w = topdown_rgb.shape[:2]
    kx, ky = img_w / 1453.0, img_h / 1582.0
    lin = np.linspace(-1.0, 1.0, size, dtype=np.float32)
    vv, uu = np.meshgrid(lin, lin, indexing="ij")  # riga 0 = basso (UV Blender)

    # Ritaglio leggermente interno al filo del vetro: la ghiera non finisce
    # nella texture nemmeno sugli spicchi perimetrali curvi.
    px = (729.0 + 410.0 * uu) * kx
    py = (854.0 - 410.0 * vv) * ky
    fx, fy = px / kx, py / ky

    vert = (np.abs(fx - 610.0) < 10.0) | (np.abs(fx - 845.0) < 10.0)
    horiz = np.zeros((size, size), dtype=bool)
    for y_bar in (578.0, 720.0, 861.0, 1003.0, 1144.0):
        horiz |= np.abs(fy - y_bar) < 9.0
    half_statue = np.clip(27.0 + 0.095 * (fy - 1170.0), 27.0, 58.0)
    statua = (fy > 1168.0) & (np.abs(fx - 731.0) < half_statue)

    cx = px.copy()
    cy = py.copy()
    cx[vert] += 22.0 * kx
    cy[horiz] += 18.0 * ky
    cx[statua] -= 145.0 * kx
    cy[statua] -= 18.0 * ky
    col = _bilinear_sample(topdown_rgb, cx, cy)

    # Correzione molto contenuta: restano le differenze fra le diciotto
    # lastre e la luce celeste reale, senza l'effetto marmo della v2.6.
    disco = (uu * uu + vv * vv) < 0.96
    if np.any(disco):
        medio = col[disco].mean(axis=0, keepdims=True)
        col = (col - medio) * 0.84 + medio
    col *= np.array([0.90, 0.965, 1.00], dtype=np.float32)[None, None, :]
    col = np.clip(col * 0.94, 0.0, 1.0)
    return _save_packed_image(name, col)


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
    # v3.8 (miglioria 3): la gradinata era grigio-azzurra (0,62/0,63/0,67) e
    # con la luce del cielo leggeva come una rampa di cemento.  I gradoni del
    # sagrato sono in marmo chiaro caldo, appena grigio, come in fotografia.
    # v3.9 (miglioria 3): in fotografia la gradinata e' un marmo chiaro quasi
    # bianco, appena caldo: la tonalita' beige della v3.8 faceva leggere i
    # gradoni come un blocco di travertino.  Schiarita verso il bianco calco.
    tex["gradinata"] = _make_marble_tex(
        "Tex_Gradinata", (0.800, 0.782, 0.752), (0.672, 0.650, 0.618), courses=12, seed=31, contrast=0.10
    )
    tex["marmo_rosa"] = _make_marble_tex(
        "Tex_Marmo_Rosa", (0.64, 0.46, 0.41), (0.48, 0.33, 0.29), courses=6, seed=41, contrast=0.13
    )
    # v3.9 (miglioria 2): il rosato chiaro senese era troppo salmone: sotto il
    # sole del render tutta la fascia dei portali virava al rosa confetto,
    # mentre in fotografia domina il bianco caldo con vene rosate appena
    # accennate.  Desaturato di un passo (resta rosato, non diventa grigio).
    tex["marmo_rosa_chiaro"] = _make_marble_tex(
        "Tex_Marmo_Rosa_Chiaro", (0.78, 0.685, 0.625), (0.655, 0.545, 0.485), courses=6, seed=51, contrast=0.10
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
        # Fallback dalla fotografia d'insieme soltanto se manca il dettaglio
        # v2.9 delle due cuspidi.
        if not os.path.exists(CUSPIDI_REF_PATH):
            tex["mosaico_sx"] = _extract_mosaic_laterale_v30(
                "Tex_Mosaico_Presentazione", topdown,
                (737.0 * sx, 1150.0 * sy), (944.0 * sx, 1146.0 * sy),
                (829.0 * sx, 1012.0 * sy), size=1024, riscalda_bianchi=True,
            )
            tex["mosaico_dx"] = _extract_mosaic_laterale_v30(
                "Tex_Mosaico_Nativita", topdown,
                (1795.0 * sx, 1121.0 * sy), (1993.0 * sx, 1117.0 * sy),
                (1882.0 * sx, 973.0 * sy), size=1024,
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

    # v2.9 — ritaglio frontale ad alta risoluzione allegato per le due cuspidi.
    # Coordinate misurate sul filo interno del mosaico, non sulla cornice.
    if os.path.exists(CUSPIDI_REF_PATH):
        cusp_img = bpy.data.images.load(CUSPIDI_REF_PATH)
        cw, ch = cusp_img.size
        cbuf = np.empty(cw * ch * 4, dtype=np.float32)
        cusp_img.pixels.foreach_get(cbuf)
        bpy.data.images.remove(cusp_img)
        cusp_top = cbuf.reshape((ch, cw, 4))[::-1, :, :3].copy()
        csx, csy = cw / 3120.0, ch / 1146.0
        mos_size = int(CFG.get("texture_reali", {}).get("dimensione_mosaici_laterali_px", 1536))
        tex["mosaico_sx"] = _extract_mosaic_laterale_v30(
            "Tex_Mosaico_Presentazione", cusp_top,
            (114.0 * csx, 906.0 * csy), (566.0 * csx, 906.0 * csy),
            (341.0 * csx, 506.0 * csy), size=mos_size, riscalda_bianchi=True,
        )
        tex["mosaico_dx"] = _extract_mosaic_laterale_v30(
            "Tex_Mosaico_Nativita", cusp_top,
            (2554.0 * csx, 901.0 * csy), (2998.0 * csx, 901.0 * csy),
            (2764.0 * csx, 498.0 * csy), size=mos_size,
        )
    tex["mosaico_tessere"] = _make_tessere_mosaico_tex("Tex_Rilievo_Tessere_Mosaico")

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
            # v2.7: l'intera lastra, non quattro campioni ripetuti.  Il
            # reticolo e la statua sono tolti dalla mappa e rimodellati in 3D.
            tex["oculo_vetro"] = _vetro_rosone_da_foto(
                "Tex_Vetro_Cattedrale_Rosone", vtop, size=1536,
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
    if name == "Vetro_Rosone":
        # Vetro cattedrale opaco sul fondo, ma con una pelle leggermente
        # lucida e ondulata: niente emissione da pannello retroilluminato.
        bsdf.inputs["IOR"].default_value = 1.46
        bsdf.inputs["Specular IOR Level"].default_value = 0.34
        bsdf.inputs["Coat Weight"].default_value = 0.24
        bsdf.inputs["Coat Roughness"].default_value = 0.20

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

    if name == "Vetro_Rosone" and base_color_socket is not None:
        micro = nodes.new("ShaderNodeBump")
        micro.label = "Ondulazione e bollicine del vetro cattedrale"
        micro.location = (-30, -120)
        micro.inputs["Strength"].default_value = cfg.get("bump", 0.10)
        micro.inputs["Distance"].default_value = 0.018
        links.new(base_color_socket, micro.inputs["Height"])
        links.new(micro.outputs["Normal"], bsdf.inputs["Normal"])

    if name in ("Mosaico_Sx_Mat", "Mosaico_Dx_Mat") and "mosaico_tessere" in TEXTURES:
        tess_node = nodes.new("ShaderNodeTexImage")
        tess_node.label = "Fughe reali fra le tessere — rilievo, non disegno"
        tess_node.location = (-340, -210)
        tess_node.image = TEXTURES["mosaico_tessere"]
        micro = nodes.new("ShaderNodeBump")
        micro.location = (-30, -120)
        micro.inputs["Strength"].default_value = 0.42
        micro.inputs["Distance"].default_value = 0.014
        links.new(tess_node.outputs["Color"], micro.inputs["Height"])
        links.new(micro.outputs["Normal"], bsdf.inputs["Normal"])

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
PIETRA_ROS = MATS.get("Pietra_Rosone", PIETRA_RIL)
CUSPIDE_BIANCO = MATS.get("Marmo_Cuspidi_Chiaro", BIANCO2)
CUSPIDE_PIETRA = MATS.get("Pietra_Cuspidi_Rilievi", PIETRA_RIL)
PATINA_ROS = MATS.get("Patina_Rosone", MATS.get("Patina_Scolpita", PIETRA))
PATINA = MATS.get("Patina_Scolpita", SCURO if "SCURO" in globals() else PIETRA)
SCURO = MATS.get("Vano_Scuro")
PATINA = MATS.get("Patina_Scolpita", SCURO)
ALZATA_MAT = MATS.get("Marmo_Alzata_Ombra", PATINA)
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


def _crocchi_falda(name, col, s, cx, y, z_base, width, height, n=8, size=0.22,
                   material=None, piega=0.26, verso_su=True):
    """Crocchette d'acanto ripiegate lungo una falda spiovente (v3.8).

    Sostituisce `foglie_rampanti` (conetti lisci con perlina in punta) dove
    servono crocchette vere: ghimberghe dei portali, timpani, arcs ciechi.
    Tutte le foglie finiscono in un'unica mesh.
    """
    material = material or PIETRA
    L = math.hypot(width * 0.5, height)
    nx, nz = s * height / L, (width * 0.5) / L        # normale esterna alla falda
    bm = bmesh.new()
    for i in range(n):
        t = 0.05 + 0.90 * i / max(1, n - 1)
        bx = cx + s * width * 0.5 * (1.0 - t)
        bz = z_base + height * t
        sz_i = size * (1.0 - 0.34 * t)
        direz = Vector((nx * 0.72, 0.0, nz * 0.72 + (0.62 if verso_su else 0.30)))
        M = (Matrix.Translation((bx + nx * sz_i * 0.10, y, bz + nz * sz_i * 0.10))
             @ direz.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm, sz_i, sz_i * 0.40, sz_i * 0.13, M,
                   piega=piega * s, gonfia=1.25)
    return _mesh_da_bmesh(name, col, bm, material, uv_scale=(1.5, 1.5))


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
            _bm_foglia(bm_p, alt * 0.15, alt * 0.075, alt * 0.040, Mk,
                       piega=0.28, gonfia=1.30)
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
X_PIL_C = DIM.get("x_pilastri_centrali", DIM.get("interasse_pilastri_centrali", 5.20))
W_PIL_C = DIM.get("larghezza_pilastro_centrale", 1.36)
Z_PIL_TOP = DIM.get("colmo_pilastro_centrale", 28.42)
X_LAT = DIM.get("x_settori_laterali", DIM.get("interasse_settori_laterali", 8.01))
Z_CUSP_LAT = DIM.get("base_cuspidi_laterali", DIM.get("quota_cuspidi_laterali", 18.77))
H_CUSP_LAT = DIM.get("altezza_cuspidi_laterali", 3.53)
X_TORRI = DIM.get("x_torrioni_angolari", DIM.get("interasse_torri_esterne", 12.7))
SCALA = float(DIM.get("scala_globale", DIM.get("scala_finale", 3.0)))

# =============================================================================
# 1. GRADINATA DEL SAGRATO E BASAMENTO ORIZZONTALE
# =============================================================================
# v3.6 (miglioria 3): gradoni PIENI fino a terra, non lastre sottili
# sovrapposte: la vecchia rampa da 42 m leggeva come una lastra grigia.
# 14 gradini (alzata 0,23 m, pedata 0,52 m) larghi 34 m — poco piu' della
# facciata — con naso chiaro e filetto d'ombra sotto ogni alzata, cosi'
# le pedate si contano una a una anche in vista frontale come in foto.
GRAD_TOP = 1.96
GRAD_SUOLO = -1.30
# v3.9 (miglioria 3): profilo nuovo dei gradoni.  Prima il naso sporgeva due
# centimetri e l'alzata era a filo: in vista frontale la gradinata leggeva
# come un blocco monolitico con righe sottili (una serranda), non come una
# scala di marmo.  Nella fotografia ogni gradino e' una banda chiara (naso
# illuminato) seguita da una banda scura (alzata in ombra, rientrante).  Ora:
# 11 gradoni (alzata 0,30 m), naso aggettante di 13 cm con bordo arrotondato,
# alzata RIENTRANTE di 5 cm e battuta d'ombra patinata sotto il naso: le
# bande si contano una a una anche in proiezione frontale.
N_GRAD = 11
alzata = (GRAD_TOP - GRAD_SUOLO) / N_GRAD
for i in range(N_GRAD):
    top_i = GRAD_TOP - i * alzata
    cy_i = -2.00 - i * 0.62
    h_i = top_i - GRAD_SUOLO - 0.10
    # corpo del gradone con faccia RIETRANTE di 12 cm: e' l'alzata in ombra
    # della fotografia (marmo patinato), non piu' coperta dal naso
    box(
        f"Gradino_{i+1}", S, 0.0, cy_i + 0.12, GRAD_SUOLO + h_i * 0.5,
        36.0, 0.72, h_i, ALZATA_MAT
    )
    # naso aggettante in marmo chiaro: sporge 26 cm sull'alzata rientrante,
    # cosi' ogni gradino e' una banda chiara + una banda scura, come i
    # gradoni del sagrato nella fotografia (anche in proiezione frontale)
    box(f"Gradino_Naso_{i+1}", S, 0.0, cy_i - 0.37, top_i - 0.055,
        36.0, 0.26, 0.11, BIANCO2)
    # pianerottolo sommitale chiaro fra un naso e l'alzata sottostante
    box(f"Gradino_Pedata_{i+1}", S, 0.0, cy_i - 0.10, top_i - 0.115,
        36.0, 0.62, 0.03, GRADINATA_MAT)
# Lastra di sagrato a quota piazza, a chiudere la discesa
box("Sagrato_Piazza", S, 0.0, -10.65, GRAD_SUOLO - 0.03, 40.0, 3.4, 0.14, GRADINATA_MAT)
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
box("Corpo_Superiore_Centrale", S, 0.0, 0.38, 19.60, 12.10, 1.85, 8.95, BIANCO)
# Muri di spalla continui dietro le loggette e le cuspidi laterali: saldati al
# corpo centrale e ai torrioni esterni fino al retro piatto (Y = +1.30)
for side in (-1, 1):
    # v3.7: il muro di spalla arretra a y = -0,30 per lasciare spazio al
    # vano profondo del loggiato (prima arrivava a -0,90 e il loggiato
    # restava un pannello appiattito sul filo della facciata)
    box(f"Corpo_Settore_Lat_{side}", S, side * 7.85, 0.50, 17.15, 5.70, 1.60, 4.20, BIANCO2)

# =============================================================================
# 3. ORDINE INFERIORE DI GIOVANNI PISANO: CONTRAFFORTI BICROMI, 4 PILONI A
#    FASCIO, 3 PORTALI CONTIGUI STROMBATI E SPECCHIATURE CON ROSONI
# =============================================================================
# --- Contrafforti angolari inferiori a fasce bicrome + fascia a losanghe ---
for side in (-1, 1):
    # Campata esterna sporgente (fasce bicrome nette bianco / verde-nero di Prato)
    xe = side * 13.85
    box(f"Contrafforte_Base_Est_{side}", S, xe, -0.15, 5.15, 2.25, 2.95, 6.45, BIANCO)
    # v3.8 (miglioria 3) — I CORSI BICROMI DEL CONTRAFFORTE.
    # Prima c'erano cinque listelli di serpentino alti 0,15 m distanziati di
    # un metro l'uno dall'altro: sul marmo chiaro leggevano come un codice a
    # barre.  Nel Duomo vero il contrafforte e' fasciato da corsi fitti e
    # regolari (marmo bianco ~0,26 m, serpentino ~0,11 m) per tutta l'altezza:
    # qui si rifa' con quel passo, lasciando libero il solo dado d'imposta.
    n_corsi = 9
    passo_c = 0.72
    for k in range(n_corsi):
        zk = 2.66 + k * passo_c
        # v3.8b — i corsi ora sono INTARSIATI a filo (2 mm di risalto):
        # sporgendo di 5 cm proiettavano un'ombra netta sotto ogni listello
        # e il contrafforte leggeva come una persiana.
        box(f"Fascia_Est_{side}_{k}", D, xe, -0.155, zk, 2.26, 2.945, 0.135, VERDE)
    # Feritoia stretta: in foto e' una piccola monofora sulla campata
    # INTERNA (fra le due fasce scure sopra le losanghe), non un
    # francobollo nero sul contrafforte esterno (v3.6, miglioria 2)
    box(f"Feritoia_Base_{side}", D, side * 11.82, -1.50, 6.54, 0.15, 0.08, 0.54, SCURO)
    prism(f"Feritoia_Arco_{side}", D, side * 11.82, -1.50, 6.81, 0.15, 0.12, 0.08, SCURO)

    # Campata interna arretrata con fasce bicrome + fascia a losanghe rosa/bianche
    xi = side * 11.82
    box(f"Contrafforte_Base_Int_{side}", S, xi, -0.05, 5.15, 1.90, 2.75, 6.45, BIANCO)
    # v3.8 (miglioria 3): la campata interna era un rettangolo di marmo
    # bianco con quattro listelli verdi e tre losanghe rosa — la parte piu'
    # "da plastico" di tutto il basamento.  Ora ha la specchiatura in marmo
    # rosato incorniciata e, a quota 4,85 m, la fascia a LOSANGHE
    # BICROME (cinque tasselli alternati bianco / serpentino), come la
    # fascia intarsiata che gira sui contrafforti del Duomo.
    box(f"Specch_Base_Int_{side}", D, xi, -1.435, 3.12, 1.56, 0.10, 0.96, ROSA_C)
    for zk in (2.60, 3.64):
        box(f"Fascia_Int_{side}_{zk:.2f}", D, xi, -1.45, zk, 1.92, 0.12, 0.11, VERDE)
    for zk in (6.05, 7.07, 8.06):
        box(f"Fascia_Int_{side}_{zk:.2f}", D, xi, -1.45, zk, 1.92, 0.12, 0.11, VERDE)
    # fascia a losanghe bicrome (5 tasselli, fondo alternato)
    box(f"Cornice_Losanghe_{side}", D, xi, -1.44, 4.85, 1.88, 0.12, 0.98, BIANCO2)
    for c in range(5):
        lx = xi + (c - 2) * 0.36
        box(f"Riquadro_Los_{side}_{c}", D, lx, -1.475, 4.85, 0.32, 0.08, 0.62, BIANCO2)
        # v3.8b — losanga ROSATA con cuore di serpentino: prima il contrasto
        # bianco/nero alternato faceva una scacchiera da bagno.
        box(f"Losanga_{side}_{c}", D, lx, -1.505, 4.85, 0.235, 0.08, 0.235, ROSA_C,
            rot_y=math.radians(45))
        box(f"Losanga_Cuore_{side}_{c}", D, lx, -1.525, 4.85, 0.095, 0.08, 0.095,
            VERDE, rot_y=math.radians(45))

    # Trabeazione scolpita d'imposta sui contrafforti (z = 8.35 m, NON attraversa gli archi)
    box(f"Trabeazione_Angolo_{side}", S, side * 12.85, -0.25, Z_IMPOSTA, 4.35, 3.05, 0.62, BIANCO2)
    box(f"Cornice_Aggetto_Angolo_{side}", S, side * 12.85, -0.32, Z_IMPOSTA + 0.38, 4.50, 3.20, 0.22, ROSA_C)


# --- 4 grandi piloni strombati a fascio di colonne (x = +-10.45 e +-3.85) ---
def pilone_strombato(cx, central_side=False):
    """Pilone a fascio di Giovanni Pisano, rifatto per assi verticali (v3.7).

    Nella v3.6 il pilone era quattro colonne tortili dello stesso diametro
    piu' un cilindro centrale, tutte alte fino a 5,30 m, sovrastate da un
    blocco e da un cilindro d'imposta a 8,45 m: davanti alla fotografia
    leggeva come un fascio di tubi, mentre nell'originale il pilone e' un
    *candelabro* di marmo — una lesena centrale coperta di girali, sei
    colonnine PIU' SOTTILI e scalate in profondita', capitello
    corinzio-gotico, cornice d'imposta a tre fili — e sopra l'imposta il
    pilastro riprende snello con la statua sotto il baldacchino.

    Quote (m): zoccolo 0,00-0,90 · fusti 0,90-6,55 · capitelli 6,55-7,15 ·
    abaco 7,15-7,55 · cornice d'imposta 7,55-8,45 (= Z_IMPOSTA, dove
    nascono gli archi dei portali).
    """
    tag = f"Pilone_{cx:+.2f}"
    yf = -2.03                       # filo frontale del candelabro (0,6 m
                                     # davanti agli archivolti: in foto i
                                     # piloni sono l'elemento piu' sporgente)
    # --- zoccolo a due risalti con filo di serpentino
    box(f"{tag}_Zoccolo1", P, cx, yf + 0.40, 0.44, 1.66, 1.26, 0.88, BIANCO2)
    box(f"{tag}_Zoccolo2", P, cx, yf + 0.31, 0.90, 1.50, 1.10, 0.15, BIANCO)
    box(f"{tag}_ZoccoloFilo", D, cx, yf + 0.16, 0.83, 1.56, 0.05, 0.06, VERDE)

    # --- lesena centrale a girali: il "candelabro" vero del pilone
    box(f"{tag}_Lesena", P, cx, yf + 0.11, 3.72, 0.32, 0.22, 5.68, BIANCO)
    box(f"{tag}_LesenaFilo1", D, cx, yf + 0.01, 3.72, 0.05, 0.04, 5.60, ROSA_C)
    box(f"{tag}_LesenaFilo2", D, cx, yf + 0.21, 3.72, 0.05, 0.04, 5.60, ROSA_C)
    bm_gir = bmesh.new()
    # v3.8b — IL CANDELABRO D'ACANTO DELLA LESENA.
    # Prima erano foglie applicate come piastrelle: in pieno sole ogni foglia
    # accendeva una scheggia bianca e la lesena leggeva come una lisca di
    # pesce.  Qui il tralcio e' costruito come nell'intaglio vero: un fusto
    # sottile che sale serpeggiando, e a ogni nodo due VOLUTE (tubi ricurvi
    # che si avvolgono) con il bocciolo in punta e una fogliolina coricata
    # alla base.  Tutto e' dentro un'unica mesh, fusa con la lesena.
    ident_gir = Matrix.Identity(4)
    _bm_segmento(bm_gir, ident_gir, (cx, yf - 0.030, 0.95),
                 (cx, yf - 0.030, 6.40), 0.030, 0.020, seg=8)
    for k in range(9):
        zk = 1.36 + k * 0.60
        for s_f in (-1, 1):
            # voluta: tre tratti di tubo che si arricciano verso l'alto
            p0 = (cx + s_f * 0.030, yf - 0.032, zk)
            p1 = (cx + s_f * 0.140, yf - 0.040, zk + 0.120)
            p2 = (cx + s_f * 0.205, yf - 0.042, zk + 0.300)
            p3 = (cx + s_f * 0.150, yf - 0.044, zk + 0.430)
            p4 = (cx + s_f * 0.075, yf - 0.044, zk + 0.400)
            _bm_segmento(bm_gir, ident_gir, p0, p1, 0.022, 0.019, seg=7)
            _bm_segmento(bm_gir, ident_gir, p1, p2, 0.019, 0.016, seg=7)
            _bm_segmento(bm_gir, ident_gir, p2, p3, 0.016, 0.013, seg=7)
            _bm_segmento(bm_gir, ident_gir, p3, p4, 0.013, 0.010, seg=7)
            _bm_sfera(bm_gir, ident_gir, p4[0], p4[1], p4[2], 0.024,
                      sx=1.1, sy=0.8, sz=1.0, u=8, v=5)
            # fogliolina coricata alla base della voluta (bassorilievo)
            _bm_foglia(
                bm_gir, 0.20, 0.085, 0.020,
                Matrix.Translation((cx + s_f * 0.070, yf - 0.028, zk - 0.10))
                @ Matrix.Rotation(s_f * 1.15, 4, "Y")
                @ Matrix.Rotation(s_f * 0.55, 4, "X"),
                piega=0.0, gonfia=0.55,
            )
    _bm_rosetta(bm_gir, ident_gir, cx, yf - 0.030, 6.55, 0.075, petali=4, spess=0.45)
    _mesh_da_bmesh(f"{tag}_Girali", P, bm_gir, PIETRA, uv_scale=(1.2, 1.2))

    # --- sei colonnine: due lisce, due tortili, due tortili opposte
    _COLONNINE_PILONE = (
        (-0.655, 0.072, -1.86, -1, 2.4),
        (-0.500, 0.086, -1.93, 1, 2.8),
        (-0.300, 0.104, -2.00, 0, 0.0),
        (0.300, 0.104, -2.00, 0, 0.0),
        (0.500, 0.086, -1.93, -1, 2.8),
        (0.655, 0.072, -1.86, 1, 2.4),
    )
    for xo, rr, yy, verso, giri in _COLONNINE_PILONE:
        xc = cx + xo
        # base attica: plinto, toro e listello
        cyl(f"{tag}_BasePlin_{xo:+.3f}", P, xc, yy, 0.965, rr * 1.62, 0.13, BIANCO2, vertices=14)
        cyl(f"{tag}_BaseToro_{xo:+.3f}", P, xc, yy, 1.065, rr * 1.34, 0.075, BIANCO, vertices=14)
        if giri:
            colonna_ritorta(
                f"{tag}_Tort_{xo:+.3f}", P, xc, yy, 3.72, rr, 5.34,
                BIANCO if verso > 0 else ROSA_C, turns=giri, ridges=3,
                ridge_amp=0.20,
            )
        else:
            cyl(f"{tag}_Fusto_{xo:+.3f}", P, xc, yy, 3.72, rr, 5.34, BIANCO, vertices=14)
            cyl(f"{tag}_Collarino_{xo:+.3f}", D, xc, yy, 4.55, rr * 1.10, 0.035, ROSA_C, vertices=14)
        # capitello: collarino, calice fogliato e abaco
        cyl(f"{tag}_Coll_{xo:+.3f}", P, xc, yy, 6.44, rr * 1.06, 0.075, BIANCO2, vertices=14)
        cyl(f"{tag}_Calice_{xo:+.3f}", P, xc, yy, 6.56, rr * 1.26, 0.16, PIETRA, vertices=14)
        for a_c in range(6):
            ang_c = math.tau * a_c / 6.0
            cone(
                f"{tag}_FogliaCap_{xo:+.3f}_{a_c}", P,
                xc + math.cos(ang_c) * rr * 0.98, yy + math.sin(ang_c) * rr * 0.86,
                6.53, rr * 0.42, 0.012, 0.20, PIETRA, vertices=6,
                rot_x=math.pi / 2.0 - ang_c,
            )
        box(f"{tag}_AbacoCol_{xo:+.3f}", P, xc, yy, 6.70, rr * 3.1, 0.20, 0.10, BIANCO2)

    # --- capitello d'insieme, abaco e cornice d'imposta a tre fili
    box(f"{tag}_Capitello", P, cx, yf + 0.16, 7.10, 1.46, 0.42, 0.34, PIETRA)
    box(f"{tag}_Abaco", P, cx, yf + 0.14, 7.36, 1.58, 0.50, 0.16, BIANCO2)
    box(f"{tag}_Imposta_Gola", D, cx, yf + 0.10, 7.62, 1.52, 0.44, 0.20, ROSA_C)
    box(f"{tag}_Imposta_Toro", P, cx, yf + 0.06, 7.90, 1.64, 0.54, 0.24, BIANCO)
    box(f"{tag}_Imposta_Cornice", P, cx, yf + 0.02, 8.26, 1.76, 0.60, 0.28, BIANCO2)
    # dentelli sotto il cornicione d'imposta
    for d_i in range(9):
        box(f"{tag}_Dentello_{d_i}", D, cx - 0.76 + d_i * 0.19, yf - 0.24, 8.30,
            0.10, 0.09, 0.10, BIANCO)

    # --- leone stiloforo all'imposta (Giovanni Pisano), piu' piccolo e disteso
    box(f"{tag}_LeoneCorpo", ST, cx, yf + 0.28, 8.62, 0.62, 0.30, 0.24, PIETRA)
    sphere(f"{tag}_LeoneTesta", ST, cx - 0.02, yf + 0.10, 8.70, 0.13, PIETRA)
    sphere(f"{tag}_LeoneGroppa", ST, cx, yf + 0.42, 8.66, 0.13, PIETRA)

    # --- sopra l'imposta: pilastro snello, statua e baldacchino
    box(f"{tag}_PilastroAlto", P, cx, -1.60, 11.05, 0.72, 0.46, 5.30, BIANCO)
    box(f"{tag}_PilastroFilo", D, cx, -1.84, 11.05, 0.10, 0.05, 5.20, ROSA_C)
    # mensola a tromba e statua a tutto tondo (in foto sta fra le falde ma
    # davanti ad esse, sul leone dell'imposta)
    box(f"{tag}_MensolaStatua", P, cx, -1.90, 8.86, 0.66, 0.52, 0.20, BIANCO2)
    cone(f"{tag}_Mensolone", P, cx, -1.92, 8.62, 0.10, 0.30, 0.34, PIETRA, vertices=8)
    statua_gotica_v26(
        f"{tag}_StatuaProfeta", ST, cx, -1.98, 8.98,
        1.92 if central_side else 1.80,
        spec=dict(gesto="parla" if cx < 0 else "libro", barba=0.70,
                  copricapo="capelli", yaw=(0.14 if cx < 0 else -0.14),
                  nod=0.05, seed=int(abs(cx) * 10), lato=1 if cx > 0 else -1),
        material=PIETRA,
    )
    # baldacchino a ghimberga con gattoni sopra la statua
    spioventi_modanati(f"{tag}_Baldacchino", P, cx, -1.92, 11.02, 1.02, 0.86, 0.10, 0.34, BIANCO)
    foglie_rampanti(f"{tag}_BaldacchinoFoglie", G, cx, -1.96, 11.06, 1.02, 0.86, PIETRA, n=4, size=0.17)
    finial(f"{tag}_BaldacchinoFiore", G, cx, -1.94, 11.90, 0.46)
    # secondo pinnacolo, in cima al pilastro, con gattoni
    box(f"{tag}_Cuspide_Base", P, cx, -1.70, 13.78, 0.60, 0.40, 0.22, BIANCO2)
    cone(f"{tag}_Cuspide", P, cx, -1.70, 14.46, 0.30, 0.03, 1.20, PIETRA, vertices=8)
    for k_c in range(5):
        tc = 0.10 + k_c * 0.18
        for s_c in (-1, 1):
            cone(f"{tag}_CuspideGattone_{k_c}_{s_c}", P,
                 cx + s_c * (0.30 * (1.0 - tc) + 0.02), -1.78, 13.98 + 1.05 * tc,
                 0.055, 0.006, 0.20, PIETRA, vertices=5, rot_y=s_c * math.radians(46))
    finial(f"{tag}_CuspideFiore", G, cx, -1.70, 15.12, 0.50)


# NOTA v3.6: i piloni sono istanziati piu' sotto, subito prima dei
# portali, perche' ora usano `statua_gotica_v26` (definita nella
# sezione 4.4 seguente).


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


def _bm_figura_gotica_v27(bm, bm_pat, mat4, H, spec):
    """Figura a tutto tondo v2.7, con contrapposto e panneggi scolpiti.

    Non e' un fusto cilindrico accessoriato: il volume cambia fra piede,
    ginocchio, bacino, torace e spalle; il manto e' una doppia superficie
    continua con orli e pieghe profonde.  Le braccia hanno polsi e maniche
    raccordate, mentre le pose dei pennacchi sono quelle della fotografia.
    """
    gesto = spec.get("gesto", "libro")
    barba = spec.get("barba", 0.70)
    copricapo = spec.get("copricapo", "capelli")
    yaw = spec.get("yaw", 0.0)
    nod = spec.get("nod", 0.05)
    seed = spec.get("seed", 0)
    lato = spec.get("lato", 1)

    z_embase, z_collo = 0.055, 0.825
    prof = (
        (0.045, 0.136, 0.101), (0.090, 0.151, 0.113),
        (0.190, 0.143, 0.107), (0.310, 0.126, 0.094),
        (0.410, 0.132, 0.098), (0.500, 0.142, 0.105),
        (0.575, 0.123, 0.088), (0.655, 0.119, 0.085),
        (0.720, 0.141, 0.096), (0.775, 0.158, 0.091),
        (0.805, 0.125, 0.077), (0.825, 0.074, 0.062),
    )

    def sez(t):
        t = max(prof[0][0], min(prof[-1][0], t))
        for a_, b_ in zip(prof, prof[1:]):
            if a_[0] <= t <= b_[0]:
                u = (t - a_[0]) / max(1e-7, b_[0] - a_[0])
                u = u * u * (3.0 - 2.0 * u)
                return (a_[1] * (1 - u) + b_[1] * u,
                        a_[2] * (1 - u) + b_[2] * u)
        return prof[-1][1], prof[-1][2]

    def spost(z):
        t = z / max(H, 1e-6)
        # Bacino in appoggio e spalle controspostate: la silhouette non e'
        # piu' simmetrica ne' rigida come un manichino.
        return H * (0.025 * math.sin(0.5 * math.pi * t)
                    - 0.015 * math.sin(math.pi * t))

    def superficie(t, a):
        rx, ry = sez(t)
        front = max(0.0, -math.sin(a)) ** 1.3
        basso = max(0.0, min(1.0, (0.66 - t) / 0.54))
        fase = (8.0 * a + 1.25 * math.sin(t * 7.0 + seed)
                + 0.55 * math.sin(3.0 * a - t * 4.0))
        piega = H * (0.0055 + 0.0070 * basso) * (
            math.sin(fase) + 0.28 * math.sin(2.0 * fase + 0.6))
        piega *= min(1.0, max(0.0, (t - 0.05) / 0.10))
        # Ammasso diagonale sul bacino e grandi curve fra le ginocchia.
        piega += H * 0.0055 * math.sin(25.0 * t + 2.6 * a + seed) \
            * math.exp(-((t - 0.49) / 0.17) ** 2) * front
        piega += H * 0.0045 * math.sin(34.0 * t + 2.0 * math.cos(a)) \
            * math.exp(-((t - 0.25) / 0.14) ** 2) * front
        x = spost(H * t) + (rx * H + piega) * math.cos(a)
        y = -H * 0.006 * math.sin(math.pi * t) + (ry * H + 0.78 * piega) * math.sin(a)
        orlo = max(0.0, 1.0 - (t - z_embase) / 0.105)
        z = H * t + H * 0.006 * math.sin(3.0 * a + seed) * orlo
        z += H * 0.006 * math.cos(a) * math.exp(-((t - 0.775) / 0.055) ** 2)
        return Vector((x, y, z))

    # Tunica continua ad alta densita'.
    nz, na = 54, 64
    grid = []
    for i in range(nz + 1):
        t = z_embase + (z_collo - z_embase) * i / nz
        grid.append([bm.verts.new(mat4 @ superficie(t, math.tau * j / na))
                     for j in range(na)])
    for i in range(nz):
        for j in range(na):
            j2 = (j + 1) % na
            bm.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
    bm.faces.new(list(reversed(grid[0])))
    bm.faces.new(grid[-1])

    # Piedi separati, uno avanzato: appoggio e contrapposto restano leggibili
    # sotto l'orlo invece di terminare in un unico cono.
    for s in (-1, 1):
        avanti = 0.020 * H if s == lato else -0.006 * H
        fx = spost(0.04 * H) + s * 0.064 * H
        _bm_sfera(bm, mat4, fx, -0.044 * H - avanti, 0.035 * H,
                  0.048 * H, sx=0.74, sy=1.34, sz=0.42, u=16, v=10)
        for dito in range(3):
            _bm_sfera(bm, mat4, fx + (dito - 1) * 0.013 * H,
                      -0.102 * H - avanti, 0.029 * H, 0.009 * H,
                      sx=0.85, sy=1.20, sz=0.65, u=8, v=5)

    # Pochi cordoni larghi, non una griglia nera disegnata sul vestito.
    for k, a in enumerate((-2.70, -2.22, -1.72, -1.18, -0.70)):
        pts = []
        for j in range(9):
            t = 0.075 + 0.46 * j / 8.0
            aa = a + 0.075 * math.sin(t * 8.0 + seed + k)
            p = superficie(t, aa)
            p.y -= H * 0.004
            pts.append(p)
        _bm_sweep24(bm, mat4, pts,
                    [H * (0.0055 + 0.0020 * math.sin(math.pi * j / 8.0)) for j in range(9)],
                    lati=7, ellisse=0.52, campioni=2)

    # Manto vero: pelle doppia, larga sul fianco e diagonale sul petto.
    nu, nv = 34, 14
    fronte, retro, local = [], [], []
    for i in range(nu + 1):
        t = i / nu
        zc = 0.785 - 0.655 * t
        xc = spost(zc * H) + lato * H * (0.115 - 0.190 * t)
        larg = H * (0.055 + 0.067 * t)
        fr, br, lr = [], [], []
        for j in range(nv + 1):
            u = 2.0 * j / nv - 1.0
            x = xc + u * larg
            zz = zc + lato * u * 0.024 + 0.006 * math.sin(t * 6.0 + seed) * t
            tt = max(0.06, min(0.80, zz))
            rx, ry = sez(tt)
            q = (x - spost(tt * H)) / max(rx * H, 1e-5)
            qclip = max(-0.995, min(0.995, q))
            yb = -ry * H * math.sqrt(max(0.0, 1.0 - qclip * qclip))
            if abs(q) > 1.0:
                yb = -0.030 * H - 0.025 * H * (abs(q) - 1.0)
            onda = (math.sin(3.0 * math.pi * u + 1.25 * math.sin(t * 5.0 + seed))
                    + 0.30 * math.sin(6.0 * math.pi * u - t * 3.0))
            yb -= H * (0.016 + 0.0085 * onda * math.sin(math.pi * (0.08 + 0.84 * t)))
            p = Vector((x, yb, zz * H))
            fr.append(bm.verts.new(mat4 @ p))
            br.append(bm.verts.new(mat4 @ (p + Vector((0.0, 0.006 * H, 0.0)))))
            lr.append(p)
        fronte.append(fr)
        retro.append(br)
        local.append(lr)
    for i in range(nu):
        for j in range(nv):
            bm.faces.new((fronte[i][j], fronte[i][j + 1], fronte[i + 1][j + 1], fronte[i + 1][j]))
            bm.faces.new((retro[i + 1][j], retro[i + 1][j + 1], retro[i][j + 1], retro[i][j]))
    for i in range(nu):
        bm.faces.new((fronte[i][0], fronte[i + 1][0], retro[i + 1][0], retro[i][0]))
        bm.faces.new((fronte[i + 1][-1], fronte[i][-1], retro[i][-1], retro[i + 1][-1]))
    for j in range(nv):
        bm.faces.new((fronte[-1][j], fronte[-1][j + 1], retro[-1][j + 1], retro[-1][j]))
    for edge in (0, -1):
        pts = [local[i][edge] + Vector((0.0, -0.002 * H, 0.0)) for i in range(0, nu + 1, 2)]
        _bm_sweep24(bm, mat4, pts, [0.0055 * H] * len(pts),
                    lati=7, ellisse=0.65, campioni=2)

    # Cintura sottile e nodo morbido all'altezza del bacino.
    t_c = 0.515
    rx_c, ry_c = sez(t_c)
    cintura = []
    for k in range(37):
        a = math.tau * k / 36.0
        cintura.append((spost(t_c * H) + (rx_c * H + 0.004 * H) * math.cos(a),
                        (ry_c * H + 0.004 * H) * math.sin(a), t_c * H))
    _bm_sweep24(bm, mat4, cintura, [0.0055 * H] * len(cintura),
                lati=8, ellisse=0.62, campioni=1)
    _bm_sfera(bm, mat4, spost(t_c * H), -ry_c * H - 0.008 * H, t_c * H,
              0.013 * H, sx=1.15, sy=0.62, sz=0.80, u=12, v=8)
    for s in (-1, 1):
        _bm_sweep24(bm, mat4,
                    ((spost(t_c * H) + s * 0.007 * H, -ry_c * H - 0.012 * H, 0.507 * H),
                     (spost(0.44 * H) + s * 0.022 * H, -ry_c * H - 0.018 * H, 0.440 * H),
                     (spost(0.36 * H) + s * 0.016 * H, -ry_c * H - 0.010 * H, 0.365 * H)),
                    (0.010 * H, 0.011 * H, 0.004 * H), lati=8,
                    ellisse=0.45, rughe=0.05, campioni=4)

    # Braccia e mani articolate.
    W = 0.42 * H
    z_spalla = 0.770 * H

    def braccio(s, gomito, polso, r=1.0, modo="grip", direzione=None):
        sp = Vector((spost(z_spalla) + s * 0.145 * H, -0.002 * H, z_spalla))
        g, p = Vector(gomito), Vector(polso)
        upper = sp.lerp(g, 0.48) + Vector((s * 0.006 * H, -0.008 * H, 0.006 * H))
        lower = g.lerp(p, 0.52) + Vector((0.0, -0.008 * H, 0.0))
        _bm_sweep24(bm, mat4, (sp, upper, g, lower, p),
                    (0.052 * H * r, 0.047 * H * r, 0.038 * H * r,
                     0.030 * H * r, 0.022 * H * r),
                    lati=16, ellisse=0.86, rughe=0.075, campioni=4)
        d = (p - g).normalized()
        _bm_sweep24(bm, mat4, (p - d * 0.028 * H, p + d * 0.004 * H),
                    (0.030 * H * r, 0.023 * H * r), lati=14,
                    ellisse=0.84, rughe=0.04, campioni=3)
        # Un risvolto segue l'avambraccio e suggerisce la stoffa della manica.
        off = Vector((0.0, -0.020 * H, 0.0))
        _bm_sweep24(bm, mat4, (upper + off, g + off * 0.75, lower + off * 0.45),
                    (0.0045 * H, 0.0050 * H, 0.0030 * H),
                    lati=6, ellisse=0.55, campioni=3)
        _bm_mano24(bm, mat4, W, p,
                   direzione if direzione is not None else p - g,
                   modo=modo, lato=s)

    if gesto == "libro":
        for s in (-1, 1):
            braccio(s, (s * 0.158 * H, -0.048 * H, 0.590 * H),
                    (s * 0.055 * H, -0.112 * H, 0.585 * H), 0.92)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.112 * H, 0.590 * H), True, lato, 0.92)
    elif gesto == "leggi":
        for s in (-1, 1):
            braccio(s, (s * 0.155 * H, -0.050 * H, 0.620 * H),
                    (s * 0.045 * H, -0.116 * H, 0.660 * H), 0.90)
        _bm_libro24(bm, bm_pat, mat4, W, H, (0.0, -0.116 * H, 0.660 * H), True, lato, 0.90)
    elif gesto == "indica":
        braccio(lato, (lato * 0.260 * H, -0.030 * H, 0.735 * H),
                (lato * 0.405 * H, -0.075 * H, 0.790 * H), 1.00,
                modo="aperta", direzione=(lato, -0.05, 0.24))
        braccio(-lato, (-lato * 0.150 * H, -0.035 * H, 0.575 * H),
                (-lato * 0.105 * H, -0.095 * H, 0.480 * H), 0.94)
    elif gesto == "parla":
        braccio(lato, (lato * 0.225 * H, -0.030 * H, 0.655 * H),
                (lato * 0.290 * H, -0.090 * H, 0.850 * H), 0.88,
                modo="aperta", direzione=(lato * 0.15, -0.08, 1.0))
        braccio(-lato, (-lato * 0.150 * H, -0.040 * H, 0.610 * H),
                (-lato * 0.025 * H, -0.112 * H, 0.690 * H), 0.92,
                modo="aperta", direzione=(lato * 0.4, -0.1, 0.8))
    elif gesto == "croce":
        braccio(lato, (lato * 0.160 * H, -0.040 * H, 0.660 * H),
                (lato * 0.130 * H, -0.095 * H, 0.745 * H), 0.90)
        braccio(-lato, (-lato * 0.150 * H, -0.050 * H, 0.575 * H),
                (-lato * 0.045 * H, -0.105 * H, 0.550 * H), 0.92)
        _bm_sweep24(bm, mat4, ((lato * 0.130 * H, -0.102 * H, 0.690 * H),
                               (lato * 0.130 * H, -0.104 * H, 0.905 * H)),
                    (0.008 * H, 0.006 * H), lati=8, campioni=2)
        _bm_box(bm, mat4 @ Matrix.Translation((lato * 0.130 * H, -0.106 * H, 0.875 * H)),
                0.0, 0.0, 0.0, 0.075 * H, 0.010 * H, 0.016 * H)
    elif gesto == "rotolo":
        braccio(lato, (lato * 0.155 * H, -0.040 * H, 0.625 * H),
                (lato * 0.075 * H, -0.110 * H, 0.690 * H), 0.90)
        braccio(-lato, (-lato * 0.150 * H, -0.045 * H, 0.560 * H),
                (lato * 0.020 * H, -0.115 * H, 0.565 * H), 0.92)
        _bm_sweep24(bm, mat4, ((lato * 0.080 * H, -0.125 * H, 0.500 * H),
                               (lato * 0.075 * H, -0.128 * H, 0.650 * H),
                               (lato * 0.078 * H, -0.124 * H, 0.760 * H)),
                    (0.014 * H, 0.016 * H, 0.012 * H), lati=12,
                    ellisse=0.65, campioni=4)
    elif gesto == "benedicente":
        braccio(lato, (lato * 0.165 * H, -0.035 * H, 0.670 * H),
                (lato * 0.180 * H, -0.080 * H, 0.845 * H), 0.88,
                modo="aperta", direzione=(lato * 0.28, -0.08, 1.0))
        braccio(-lato, (-lato * 0.150 * H, -0.050 * H, 0.580 * H),
                (-lato * 0.048 * H, -0.110 * H, 0.550 * H), 0.92)
        _bm_libro24(bm, bm_pat, mat4, W, H, (-lato * 0.020 * H, -0.120 * H, 0.550 * H),
                    False, lato, 0.78)
    else:  # petto / redentore: gesto raccolto, come la statua della foto
        braccio(lato, (lato * 0.155 * H, -0.035 * H, 0.625 * H),
                (lato * 0.020 * H, -0.118 * H, 0.700 * H), 0.90,
                modo="aperta", direzione=(-lato * 0.45, -0.15, 0.85))
        braccio(-lato, (-lato * 0.150 * H, -0.030 * H, 0.555 * H),
                (-lato * 0.120 * H, -0.075 * H, 0.445 * H), 0.94,
                modo="aperta", direzione=(-lato * 0.10, -0.05, -1.0))

    # Collo e testa, con leggere torsioni diverse per ciascuna figura.
    z_head, r_h = 0.895 * H, 0.066 * H
    x_h = spost(z_head)
    _bm_sweep24(bm, mat4,
                ((spost(0.800 * H), -0.003 * H, 0.800 * H),
                 (x_h * 0.92, -0.010 * H, 0.845 * H),
                 (x_h, -0.016 * H, z_head - r_h * 0.78)),
                (0.047 * H, 0.040 * H, r_h * 0.68),
                lati=18, ellisse=0.86, campioni=4)
    Mh = (mat4 @ Matrix.Translation((x_h, -0.017 * H, z_head))
          @ Matrix.Rotation(yaw, 4, "Z") @ Matrix.Rotation(nod, 4, "X"))
    _bm_testa_profeta24(bm, bm_pat, Mh, r_h, yaw * 0.30, nod * 0.45,
                        barba * 0.88, copricapo, seed)


def statua_gotica_v26(name, col, x, y, z, h, spec=None, material=None):
    """Statua v2.7: piedistallo modanato e figura a tutto tondo scolpita."""
    spec = spec or {}
    bm = bmesh.new()
    bm_pat = bmesh.new()
    M = (Matrix.Translation((x, y, z))
         @ Matrix.Rotation(spec.get("rot_z", 0.0), 4, "Z")
         @ Matrix.Diagonal((h, h, h, 1.0)))
    # Tre fili di plinto, con impronta dei piedi; la scala orizzontale puo'
    # essere ridotta per le statue apicali senza alterare la figura.
    plinto = spec.get("scala_plinto", 1.0)
    _bm_box(bm, Matrix.Translation((x, y + 0.012 * h, z - 0.008 * h)),
            0.0, 0.0, 0.0, 0.34 * h * plinto, 0.27 * h * plinto, 0.025 * h)
    _bm_box(bm, Matrix.Translation((x, y + 0.008 * h, z + 0.007 * h)),
            0.0, 0.0, 0.0, 0.305 * h * plinto, 0.245 * h * plinto, 0.020 * h)
    _bm_box(bm, Matrix.Translation((x, y + 0.004 * h, z + 0.020 * h)),
            0.0, 0.0, 0.0, 0.275 * h * plinto, 0.220 * h * plinto, 0.016 * h)
    _bm_figura_gotica_v27(bm, bm_pat, M, 1.0, spec)
    _mesh_da_bmesh(f"{name}_Marmo", col, bm, material or PIETRA_ROS, uv_scale=(0.9, 0.9))
    if len(bm_pat.faces):
        _mesh_da_bmesh(f"{name}_Incavi", col, bm_pat, PATINA_ROS, uv_scale=(0.9, 0.9))
    else:
        bm_pat.free()



def semiluna(name, col, cx, y_front, cz, radius, depth, material, seg=26):
    """Pannello semicircolare pieno della lunetta (v3.6).

    Prima la lunetta era un DISCO intero il cui semicerchio inferiore
    sbucava ai lati dell'architrave; ora il fondo e' una vera semiluna
    con la corda sulla quota d'imposta.
    """
    punti = [(cx + radius, cz)]
    for i in range(1, seg):
        a = math.pi * i / seg
        punti.append((cx + radius * math.cos(a), cz + radius * math.sin(a)))
    punti.append((cx - radius, cz))
    bm = bmesh.new()
    _bm_lastra(bm, Matrix(), punti, depth, y0=y_front)
    return _mesh_da_bmesh(name, col, bm, material)


def campo_ghimberga(name, col, cx, y_front, depth, cz_arco, r_arco,
                    z_base, half_w, z_apex, material, seg=26):
    """Campo triangolare della ghimberga SOPRA l'estradosso (v3.6).

    Il campo reale non e' un triangolo pieno: e' il pennacchio compreso
    fra i due spioventi e la curva dell'archivolto.  Il poligono segue
    quindi la base, sale lungo l'arco (raggio `r_arco` attorno a
    `cz_arco`) che "morde" il triangolo dal basso, e chiude sull'apice.
    Cosi' lunetta e ghiere restano libere davanti al campo, invece di
    finirci incastrate dentro come nella v3.5.
    """
    dz = z_base - cz_arco
    if abs(dz) >= r_arco:
        punti = [(cx - half_w, z_base), (cx + half_w, z_base), (cx, z_apex)]
    else:
        dx = min(math.sqrt(r_arco * r_arco - dz * dz), half_w * 0.98)
        a_sx = math.atan2(dz, -dx)
        a_dx = math.atan2(dz, dx)
        punti = [(cx - half_w, z_base), (cx - dx, z_base)]
        for i in range(1, seg):
            a = a_sx + (a_dx - a_sx) * i / seg
            punti.append((cx + r_arco * math.cos(a),
                          cz_arco + r_arco * math.sin(a)))
        punti += [(cx + dx, z_base), (cx + half_w, z_base), (cx, z_apex)]
    bm = bmesh.new()
    _bm_lastra(bm, Matrix(), punti, depth, y0=y_front)
    return _mesh_da_bmesh(name, col, bm, material)


def portale_pisano(cx, door_w, door_h, r_ext, gh_base, gh_apex, door_mat, central=False):
    """Portale di Giovanni Pisano, rifatto sulla fotografia (v3.7).

    Nella v3.6 il portale era un tubo per ogni ghiera (cinque archivolti
    tondi, lisci e tutti larghi uguali), una semiluna piattissima sopra un
    architrave liscio, e le porte alte 5,65 m che arrivavano a 7,60 m —
    contro i 4,4 m delle porte vere.  Qui:

      1. porte di altezza reale (4,6 m la centrale, 4,1 m le laterali) con
         specchiature in rilievo, cornice bronzea e lastre di marmo con
         quatrefogli ai lati — nella foto fra porta e pilone ci sono
         pannelli chiari con un medaglione a quatrefoglio;
      2. stipiti a tre colonnine binate con basi e capitelli, alternati
         bianco / rosato senese;
      3. architrave modanato + fregio di statuette su fondo d'ombra +
         cornicione a dentelli, il tutto fra la porta e l'imposta;
      4. lunetta emisferica con la raggiera bicroma bianco/serpentino e il
         sole raggiante di San Bernardino (centrale) o la ghirlanda
         (laterali);
      5. sette archivolti sottili e concentrici, alternati lisci, tortili
         e intagliati, ciascuno arretrato rispetto al precedente, cosi'
         la strombatura ha gradini d'ombra veri e non un tubo unico.
    """
    tag = "Centrale" if central else ("Sinistro" if cx < 0 else "Destro")
    front = -1.36
    z0 = 1.95
    z_top = z0 + door_h
    r_lun = max(1.10, 0.56 * door_w)      # raggio interno della lunetta
    hw_d = door_w * 0.5

    # === 1. Porta, cornice bronzea e specchiature ==========================
    box(f"Mostra_Fondo_{tag}", P, cx, front + 0.16, z0 + door_h * 0.5,
        door_w + 0.34, 0.26, door_h + 0.12, NICCHIA)
    box(f"Porta_{tag}", P, cx, front - 0.04, z0 + door_h * 0.5,
        door_w, 0.10, door_h, door_mat, fit_uv=True)
    if central:
        # velo scuro in bronzo brunito DAVANTI alla lastra: nella fotografia
        # il portone centrale e' quasi nero, non verde-oliva come usciva dal
        # solo materiale PBR (il velo deve stare davanti, non dentro la lastra)
        box(f"Porta_Velo_{tag}", P, cx, front - 0.095, z0 + door_h * 0.5,
            door_w * 0.998, 0.015, door_h * 0.996, MATS.get("Bronzo_Portale_Scuro", PATINA))
        for s_b in (-1, 1):
            for riga in range(3):
                box(f"Formella_{tag}_{s_b}_{riga}", P,
                    cx + s_b * door_w * 0.235, front - 0.108,
                    z0 + door_h * (0.20 + riga * 0.28),
                    door_w * 0.32, 0.016, door_h * 0.21,
                    MATS.get("Bronzo_Portale_Scuro", PATINA))
    # due battenti e quattro specchiature in rilievo per battente
    box(f"Battente_{tag}", P, cx, front - 0.10, z0 + door_h * 0.5,
        0.05, 0.035, door_h * 0.99, BRONZO if central else LEGNO_S)
    if not central:
        for s_b in (-1, 1):
            for riga in range(4):
                box(f"Specchiatura_{tag}_{s_b}_{riga}", P,
                    cx + s_b * door_w * 0.235, front - 0.095,
                    z0 + door_h * (0.135 + riga * 0.243),
                    door_w * 0.385, 0.03, door_h * 0.185, LEGNO_S)
    # cornice bronzea attorno alla porta
    # v3.9 (miglioria 2): la cornice era un filo sottile arretrato, e la porta
    # leggeva come una tessera piatta incollata sul muro.  Nella fotografia il
    # battente e' INCASSATO dentro una cornice modanata aggettante (due fili
    # + battuta d'ombra): qui la cornice sporge 16 cm con un filetto rosato e
    # una gola scura, cosi' il vano della porta ha un'ombra vera sul bordo.
    box(f"CornicePorta_Sup_{tag}", P, cx, front - 0.16, z_top + 0.08,
        door_w + 0.34, 0.26, 0.18, BRONZO_D if central else BIANCO)
    box(f"CornicePorta_SupFilo_{tag}", D, cx, front - 0.24, z_top - 0.02,
        door_w + 0.24, 0.10, 0.05, ROSA_C)
    for s_b in (-1, 1):
        box(f"CornicePorta_Lat_{tag}_{s_b}", P, cx + s_b * (hw_d + 0.10),
            front - 0.16, z0 + door_h * 0.5, 0.22, 0.26, door_h + 0.10,
            BRONZO_D if central else BIANCO)
        box(f"CornicePorta_LatFilo_{tag}_{s_b}", D, cx + s_b * (hw_d + 0.02),
            front - 0.24, z0 + door_h * 0.5, 0.05, 0.10, door_h, ROSA_C)
    box(f"CornicePorta_Soglia_{tag}", P, cx, front - 0.14, z0 + 0.05,
        door_w + 0.34, 0.24, 0.10, BIANCO2)

    # === 2. Stipiti: tre colonnine binate per lato ========================
    for s_j in (-1, 1):
        for idx_c, (dxt, rr, yy, mat_c) in enumerate((
            (0.10, 0.078, front - 0.26, BIANCO),
            (0.22, 0.062, front - 0.18, ROSA_C),
            (0.33, 0.052, front - 0.10, BIANCO2),
        )):
            xc = cx + s_j * (hw_d + dxt)
            cyl(f"ColStipite_Plin_{tag}_{s_j}_{idx_c}", P, xc, yy, z0 + 0.05,
                rr * 1.7, 0.10, BIANCO2, vertices=12)
            if idx_c == 0:
                colonna_ritorta(f"ColStipite_{tag}_{s_j}_{idx_c}", P, xc, yy,
                                z0 + 0.10 + (door_h - 0.6) * 0.5, rr, door_h - 0.6,
                                mat_c, turns=2.6, ridges=3, ridge_amp=0.22)
            else:
                cyl(f"ColStipite_{tag}_{s_j}_{idx_c}", P, xc, yy,
                    z0 + 0.10 + (door_h - 0.6) * 0.5, rr, door_h - 0.6, mat_c, vertices=12)
            cyl(f"CapStipite_{tag}_{s_j}_{idx_c}", P, xc, yy, z0 + door_h - 0.44,
                rr * 1.35, 0.11, PIETRA, vertices=12)
            box(f"AbacoStipite_{tag}_{s_j}_{idx_c}", P, xc, yy,
                z0 + door_h - 0.30, rr * 3.0, 0.16, 0.075, BIANCO2)
        # lesena esterna e lastra con quatrefogli (in foto fra porta e pilone)
        box(f"LesenaStipite_{tag}_{s_j}", P, cx + s_j * (hw_d + 0.42), front - 0.02,
            z0 + door_h * 0.52, 0.15, 0.20, door_h + 0.10, BIANCO)
        for k_q in range(6):
            rosetta_rilievo(f"Quatrifoglio_Porta_{tag}_{s_j}_{k_q}", P,
                            cx + s_j * (hw_d + 0.42), front - 0.14,
                            z0 + 0.55 + k_q * (door_h - 0.7) / 5.0, 0.070, petals=4)

    # === 3. Architrave, fregio di statuette e cornicione a dentelli =======
    z_arch = z_top + 0.07
    box(f"Architrave_{tag}", P, cx, front - 0.22, z_arch,
        door_w + 1.02, 0.42, 0.46, PIETRA)
    box(f"Architrave_Filo_{tag}", D, cx, front - 0.40, z_arch - 0.20,
        door_w + 1.02, 0.06, 0.055, ROSA_C)
    # v3.7: fregio basso (0,55 m) con figure fitte su fondo in mezz'ombra,
    # non una fila di sbarre bianche su nero che leggeva come uno steccato
    z_fre0, z_fre1 = z_arch + 0.30, z_arch + 0.85
    # v3.9: il fondo del fregio era in marmo rosato chiaro (NICCHIA) e le
    # figurine chiare vi si confondevano: in vista frontale la fascia sopra
    # le porte leggeva come una striscia candystripe rosa/bianco.  Nella
    # fotografia il fregio e' una teoria di statuette CHIARE su fondo in
    # ombra profonda: il fondo ora e' il vano scuro e le figure, piu' larghe,
    # si stagliano una a una.
    box(f"Fregio_Fondo_{tag}", P, cx, front - 0.08, (z_fre0 + z_fre1) * 0.5,
        door_w + 1.02, 0.20, z_fre1 - z_fre0, SCURO)
    n_fig = 19 if central else 14
    passo_f = (door_w + 0.74) / n_fig
    for k_f in range(n_fig):
        x_f = cx - (n_fig - 1) * 0.5 * passo_f + k_f * passo_f
        box(f"Fregio_Figura_{tag}_{k_f}", P, x_f, front - 0.19,
            z_fre0 + (z_fre1 - z_fre0) * 0.42, passo_f * 0.80, 0.11,
            (z_fre1 - z_fre0) * 0.74, PIETRA)
        sphere(f"Fregio_Testa_{tag}_{k_f}", P, x_f, front - 0.22,
               z_fre0 + (z_fre1 - z_fre0) * 0.88, passo_f * 0.30, PIETRA)
    box(f"Fregio_Cornice_{tag}", P, cx, front - 0.12, z_fre1 + 0.07,
        door_w + 1.06, 0.28, 0.11, BIANCO2)
    for d_i in range(n_fig):
        box(f"Fregio_Dentello_{tag}_{d_i}", D,
            cx - (door_w + 0.86) * 0.5 + (d_i + 0.5) * (door_w + 0.86) / n_fig,
            front - 0.26, z_fre1 + 0.01, 0.055, 0.055, 0.055, BIANCO)
    # fascia d'imposta su cui nascono gli archi (sottile: e' una modanatura)
    box(f"Imposta_Portale_{tag}", P, cx, front + 0.04, Z_IMPOSTA - 0.13,
        door_w + 1.08, 0.46, 0.15, BIANCO2)

    # === 4. Lunetta: raggiera bicroma e sole / ghirlanda ==================
    semiluna(f"Lunetta_Fondo_{tag}", P, cx, front + 0.10, Z_IMPOSTA,
             r_lun + 0.10, 0.18, BIANCO2)
    # v3.9 (miglioria 2): nella fotografia la raggiera bicroma riempie TUTTA
    # la lunetta, dal bordo del tondo/sole fino all'archivolto: gli spicchi
    # bianco/serpentine si contano uno a uno e danno il contrasto che fa
    # leggere i portali da lontano.  Nella v3.8 gli spicchi erano un anello
    # sottile (0,60-1,00 R) su un catino ROSA: in vista frontale la lunetta
    # laterale leggeva come un anello bianco aperto su fondo rosa, e quella
    # centrale come un sole appoggiato su un ventaglio bianco.  Ora gli
    # spicchi corrono da 0,40 R a 1,02 R, il catino e' bianco e un anello
    # d'ombra stacca il tondo/sole dalla raggiera.
    n_rays_bg = 41
    for k in range(n_rays_bg):
        a = math.pi * (0.015 + 0.97 * k / (n_rays_bg - 1))
        box(
            f"Spicchio_Lunetta_{tag}_{k}", P,
            cx + math.cos(a) * (r_lun * 0.71), front + 0.05,
            Z_IMPOSTA + 0.05 + math.sin(a) * (r_lun * 0.71),
            0.075, 0.045, r_lun * 0.62,
            VERDE if k % 2 == 1 else BIANCO,
            rot_y=(math.pi / 2.0 - a)
        )
    cyl(f"Lunetta_Catino_{tag}", P, cx, front + 0.09, Z_IMPOSTA + 0.04,
        r_lun * 0.40, 0.05, BIANCO2, vertices=40, rot_x=math.radians(90))
    torus(f"Lunetta_OmbraAnello_{tag}", P, cx, front + 0.06, Z_IMPOSTA + 0.04,
          r_lun * 0.40, 0.035, PATINA)
    arch(f"Lunetta_Ghiera_{tag}", P, cx, front - 0.02, Z_IMPOSTA + 0.04,
         r_lun * 0.99, 0.075, ROSA_C, seg_u=34)
    arch(f"Lunetta_GhieraInt_{tag}", P, cx, front + 0.04, Z_IMPOSTA + 0.03,
         r_lun * 0.92, 0.045, BIANCO, seg_u=32)
    if central:
        # sole raggiante di San Bernardino con tavoletta IHS
        cyl(f"Disco_Sole_IHS", P, cx, front - 0.06, Z_IMPOSTA + 0.86, 0.42, 0.10,
            BRONZO_D, vertices=28, rot_x=math.radians(90))
        box(f"Tavoletta_IHS", P, cx, front - 0.13, Z_IMPOSTA + 0.86, 0.30, 0.05, 0.24,
            MATS.get("Bronzo_Verde", BRONZO_D))
        for a_i in range(24):
            ang = a_i * math.tau / 24.0
            l_ray = 0.50 if a_i % 2 == 0 else 0.34
            cone(
                f"Fiamma_Sole_{a_i}", P,
                cx + math.cos(ang) * (0.46 + l_ray * 0.5), front - 0.06,
                Z_IMPOSTA + 0.86 + math.sin(ang) * (0.46 + l_ray * 0.5),
                0.055, 0.006, l_ray, BRONZO_D, vertices=5,
                rot_y=math.pi / 2.0 - ang
            )
    else:
        # v3.9: ghirlanda piu' grande e bianca con anello d'ombra dietro: il
        # tondo della lunetta laterale deve leggere come una corona appesa,
        # non come un anello aperto su fondo rosa
        torus(f"Ghirlanda_{tag}", P, cx, front - 0.04, Z_IMPOSTA + r_lun * 0.46,
              r_lun * 0.36, 0.11, BIANCO)
        torus(f"Ghirlanda_Ombra_{tag}", P, cx, front + 0.02, Z_IMPOSTA + r_lun * 0.46,
              r_lun * 0.36, 0.06, PATINA)
        for k_g in range(14):
            ang = math.tau * k_g / 14.0
            sphere(f"Ghirlanda_Foglia_{tag}_{k_g}", P,
                   cx + math.cos(ang) * r_lun * 0.36, front - 0.10,
                   Z_IMPOSTA + r_lun * 0.46 + math.sin(ang) * r_lun * 0.36,
                   0.085, PIETRA, sy=0.8)
        rosetta_rilievo(f"Ghirlanda_Rosetta_{tag}", P, cx, front - 0.06,
                        Z_IMPOSTA + r_lun * 0.46, r_lun * 0.20, petals=8)

    # === 5. Sette archivolti concentrici, arretrati a gradini =============
    cz_arch = Z_IMPOSTA
    n_an = 7
    span_a = max(0.55, r_ext - (r_lun + 0.16))
    y_out, y_in = front - 0.16, front + 0.20
    for k in range(n_an):
        r_k = r_lun + 0.16 + span_a * (k + 0.5) / n_an
        m_k = span_a / n_an * 0.60
        y_k = y_in - (y_in - y_out) * (k / (n_an - 1.0))
        mat_k = (BIANCO, ROSA_C, BIANCO2, PIETRA, BIANCO, BIANCO2, ROSA_C)[k]
        if k in (1, 4):
            arco_ritorto(f"Archivolto_{tag}_{k}", P, cx, y_k - 0.06, cz_arch,
                         r_k, m_k, mat_k, seg_u=40, seg_v=12, ribs=5,
                         turns=2.4, amp=0.26)
        else:
            arch(f"Archivolto_{tag}_{k}", P, cx, y_k - 0.06, cz_arch,
                 r_k, m_k, mat_k, seg_u=44)
        # filetto d'ombra fra un anello e l'altro
        if k < n_an - 1:
            arch(f"Archivolto_Filo_{tag}_{k}", D, cx, y_k - 0.02, cz_arch,
                 r_k + m_k * 1.05, 0.022, PATINA, seg_u=40)
    # v3.8 (miglioria 2): le due fasce portanti degli archivolti erano
    # decorate con 31 rosette a petali ciascuna, che in vista frontale
    # leggevano come asterischi bianchi appoggiati sopra gli archi.  Nella
    # fotografia gli archivolti portano una CORDA INTRECCIATA e un filo di
    # perline, cioe' modanature continue: qui si rifanno cosi'.
    r_corda = r_lun + 0.16 + span_a * 1.5 / n_an
    arco_ritorto(f"Corda_Archivolto_{tag}", P, cx, front - 0.34, cz_arch,
                 r_corda, span_a / n_an * 0.34, PIETRA, seg_u=54, seg_v=10,
                 ribs=6, turns=3.1, amp=0.30)
    r_perle = r_lun + 0.16 + span_a * 5.5 / n_an
    bm_perle = bmesh.new()
    n_perle = 46
    for k in range(n_perle):
        a = math.pi * (k + 0.5) / n_perle
        _bm_sfera(bm_perle, Matrix.Identity(4),
                  cx + r_perle * math.cos(a), front - 0.40,
                  cz_arch + r_perle * math.sin(a), 0.052, u=8, v=5)
    _mesh_da_bmesh(f"Perline_Archivolto_{tag}", P, bm_perle, BIANCO,
                   uv_scale=(1.2, 1.2))
    # piccole foglie d'acanto fra corda e perline (una per volta, fuse)
    bm_fog_arco = bmesh.new()
    n_fog = 26
    for k in range(n_fog):
        a = math.pi * (k + 0.5) / n_fog
        rr = r_lun + 0.16 + span_a * 3.4 / n_an
        base = Vector((cx + rr * math.cos(a), front - 0.38,
                       cz_arch + rr * math.sin(a)))
        direz = Vector((math.cos(a) * 0.55, 0.0, math.sin(a) * 0.55 + 0.55))
        M = (Matrix.Translation(base)
             @ direz.normalized().to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm_fog_arco, 0.20, 0.085, 0.030, M, piega=0.22, gonfia=1.2)
    _mesh_da_bmesh(f"Fogliame_Archivolto_{tag}", P, bm_fog_arco, PIETRA,
                   uv_scale=(1.4, 1.4))
    # chiave di volta e mensole d'imposta
    sphere(f"Chiave_Volta_{tag}", P, cx, front - 0.60, cz_arch + r_ext - 0.02, 0.20, PIETRA)
    for s_m in (-1, 1):
        box(f"Mensola_Imposta_{tag}_{s_m}", P, cx + s_m * (r_ext - 0.10),
            front - 0.42, cz_arch + 0.06, 0.30, 0.34, 0.26, PIETRA)

    # === 6. Ghimberga: pennacchio sopra l'estradosso, cornice e apice =====
    gh_w = r_ext * 2.0 + 0.15
    gh_h = gh_apex - gh_base
    campo_ghimberga(f"Ghimberga_Campo_{tag}", P, cx, -1.60, 0.26,
                    cz_arch, r_ext + 0.06, gh_base, gh_w * 0.5,
                    gh_base + gh_h, BIANCO2)
    arch(f"Ghimberga_FilettoArco_{tag}", P, cx, -1.72, cz_arch,
         r_ext + 0.30, 0.065, ROSA_C, seg_u=38)
    spioventi_modanati(f"Ghimberga_Cornice_{tag}", P, cx, -1.72, gh_base, gh_w, gh_h,
                       0.26, 0.36, BIANCO)
    # v3.8 (miglioria 2): le foglie rampanti erano coni lisci con una perlina
    # in punta, che sulle falde delle tre ghimberghe leggevano come i rebbi
    # di un tridente.  Ora sono crocchette d'acanto ripiegate, come quelle
    # (già giuste) della cuspide centrale.
    for s_g in (-1, 1):
        _crocchi_falda(f"Ghimberga_Foglie_{tag}_{s_g}", P, s_g, cx, -1.76,
                       gh_base + 0.04, gh_w, gh_h, n=13, size=0.26,
                       material=PIETRA)
    # v3.8b — nelle riseghe del campo, al posto delle rosette a raggiera e
    # delle foglie "in piedi" (che leggevano come frecce), tre piccole
    # rosette scolpite coricate sul marmo, come i fregi di Giovanni Pisano.
    for s_f in (-1, 1):
        for row in range(3):
            xx = cx + s_f * gh_w * (0.30 - row * 0.07)
            zz = gh_base + gh_h * (0.44 + row * 0.11)
            if math.hypot(xx - cx, zz - cz_arch) <= r_ext + 0.22:
                continue
            rosetta_rilievo(f"Tralcio_Ghimberga_{tag}_{s_f}_{row}",
                            P, xx, -1.655, zz, 0.155, petals=6)
    spioventi_modanati(f"Ghimberga_ListelloInterno_{tag}", P, cx, -1.66,
                       gh_base + 0.30, gh_w * 0.85, gh_h * 0.85,
                       0.065, 0.10, ROSA_C)
    # medaglione col busto nel pennacchio: cornice, fondo, spalle, testa e
    # capelli (prima cono + sfera leggevano come una campanella)
    z_med = gh_base + gh_h * 0.56
    # v3.9: medaglione piu' grande e piu' sporgente, con un secondo filo
    # modanato esterno: nella fotografia il tondo col busto spicca sul campo
    # della ghimberga con un'ombra netta sotto la cornice; il tondo piccolo e
    # arretrato della v3.8 leggeva come una ciambella stampata.
    torus(f"Medaglione_Cornice_{tag}", P, cx, -1.70, z_med, 0.60, 0.12, BIANCO)
    torus(f"Medaglione_FiloEst_{tag}", P, cx, -1.67, z_med, 0.68, 0.045, BIANCO2)
    torus(f"Medaglione_FiloInterno_{tag}", P, cx, -1.66, z_med, 0.46, 0.035, ROSA_C)
    cyl(f"Medaglione_Fondo_{tag}", P, cx, -1.67, z_med, 0.52, 0.08, ROSA_C,
        vertices=24, rot_x=math.radians(90))
    # v3.8b — il busto era un cilindro con una sfera appoggiata sopra: in
    # vista frontale leggeva come una campanella.  Ora e' un mezzo busto
    # scolpito: petto inclinato, spalle, collo e testa con la chioma.
    bm_med = bmesh.new()
    _bm_lathe(bm_med, Matrix.Translation((cx, -1.74, z_med - 0.38)),
              ((0.0, 0.34), (0.14, 0.30), (0.30, 0.23), (0.44, 0.13)), seg=16,
              sy=0.30)
    _mesh_da_bmesh(f"Medaglione_Busto_{tag}", P, bm_med, PIETRA, uv_scale=(1.4, 1.4))
    sphere(f"Medaglione_Spalle_{tag}", P, cx, -1.76, z_med - 0.14, 0.31,
           PIETRA, sx=1.15, sy=0.34, sz=0.34)
    box(f"Medaglione_Collo_{tag}", P, cx, -1.775, z_med - 0.01, 0.115, 0.0750,
        0.14, PIETRA)
    sphere(f"Medaglione_Testa_{tag}", P, cx, -1.785, z_med + 0.11, 0.128,
           PIETRA, sy=0.86, sz=0.94)
    sphere(f"Medaglione_Chioma_{tag}", P, cx, -1.745, z_med + 0.15, 0.146,
           PIETRA, sy=0.74, sz=0.88)

    # statua di coronamento sul vertice della ghimberga
    if central:
        box("Piedistallo_Redentore", ST, cx, -1.66, gh_apex - 0.32, 0.46, 0.34, 0.16, BIANCO2)
        statua_gotica_v26(
            "Statua_Redentore_Oculo", ST, cx, -1.76, gh_apex - 0.24, 1.72,
            spec=dict(gesto="petto", barba=0.72, copricapo="capelli_lunghi",
                      yaw=-0.18, nod=0.09, seed=11, lato=1, rot_z=-0.08),
        )
    else:
        statua_gotica_v26(
            f"Statua_Apice_Ghimberga_{tag}", ST, cx, -1.70, gh_apex + 0.02, 1.42,
            spec=dict(gesto="libro", barba=0.7, copricapo="capelli",
                      yaw=0.0, nod=0.04,
                      seed=13, lato=1),
        )


for px_pier, is_c in [(-10.45, False), (-4.15, True), (4.15, True), (10.45, False)]:
    pilone_strombato(px_pier, central_side=is_c)

portale_pisano(-X_PORT_L, W_PORT_L, 4.10, 2.48, 10.30, 15.55, LEGNO, central=False)
portale_pisano(0.0, W_PORT_C, H_PORTALI, 3.95, 10.55, 16.40, BRONZO, central=True)
portale_pisano(X_PORT_L, W_PORT_L, 4.10, 2.48, 10.30, 15.55, LEGNO, central=False)



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
    # v3.8 (miglioria 2) — LE SPECCHIATURE FRA LE TRE GHIMBERGHE.
    # Prima erano un quadrato rosa con un anello e sei coni che partivano dal
    # centro: in vista frontale un "fiocco di neve" su una piastrella, e le
    # due losanghe verdi ai lati leggevano come decorazioni da bagno.
    # Nella fotografia questi riquadri sono pannelli cosmateschi: cornice
    # bianca, filo di serpentino, campo in marmo rosato con un ROSONE
    # fogliato a bassorilievo al centro e quattro tasselli verdi agli angoli.
    box(f"Specch_CorniceEst_{idx_s}", D, sx_pos, -1.30, sz_pos, sw, 0.10, sh, BIANCO)
    for k_f, (dx_f, dz_f, sx_f, sz_f) in enumerate((
        (0.0, (sh - 0.20) * 0.5, sw - 0.14, 0.075),
        (0.0, -(sh - 0.20) * 0.5, sw - 0.14, 0.075),
        ((sw - 0.14) * 0.5, 0.0, 0.075, sh - 0.26),
        (-(sw - 0.14) * 0.5, 0.0, 0.075, sh - 0.26),
    )):
        box(f"Specch_Filo_{idx_s}_{k_f}", D, sx_pos + dx_f, -1.335, sz_pos + dz_f,
            sx_f, 0.08, sz_f, VERDE)
    box(f"Specch_Campo_{idx_s}", D, sx_pos, -1.35, sz_pos, sw - 0.26, 0.09,
        sh - 0.26, BIANCO2)
    # rosone fogliato a bassorilievo: anello, otto petali carnosi e bottone
    # v3.9: il rosone era bianco su bianco, tutto alla stessa quota: in vista
    # frontale leggeva come una girandola stampata sulla piastrella.  Ora il
    # disco poggia su un RECESSO scuro (l'ombra del sottosquadro) e petali e
    # bottone sporgono 7 cm in piu', cosi' il fogliame proietta la sua ombra
    # sul campo come i rosoni scolpiti della fotografia.
    r_ros = min(sw, sh) * 0.215
    cyl(f"Specch_OmbraRosone_{idx_s}", D, sx_pos, -1.405, sz_pos + 0.02,
        r_ros * 1.06, 0.04, SCURO, vertices=26, rot_x=math.radians(90))
    cyl(f"Specch_RosoneDisco_{idx_s}", D, sx_pos, -1.42, sz_pos + 0.02, r_ros,
        0.05, BIANCO, vertices=26, rot_x=math.radians(90))
    torus(f"Specch_Rosone_{idx_s}", D, sx_pos, -1.44, sz_pos + 0.02, r_ros * 0.96,
          0.045, ROSA_C)
    bm_ros = bmesh.new()
    for leaf_i in range(8):
        la = math.tau * leaf_i / 8.0
        base = Vector((sx_pos + math.cos(la) * r_ros * 0.42, -1.475,
                       sz_pos + 0.02 + math.sin(la) * r_ros * 0.42))
        direz = Vector((math.cos(la), 0.0, math.sin(la)))
        M = (Matrix.Translation(base)
             @ direz.to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm_ros, r_ros * 0.58, r_ros * 0.24, r_ros * 0.10, M,
                   piega=0.0, gonfia=1.1)
    _mesh_da_bmesh(f"Specch_Petali_{idx_s}", D, bm_ros, PIETRA, uv_scale=(1.8, 1.8))
    sphere(f"Specch_Bottone_{idx_s}", D, sx_pos, -1.49, sz_pos + 0.02,
           r_ros * 0.20, PIETRA, sy=0.45)
    # quattro tasselli verdi di serpentino agli angoli del campo
    for c_i, (cx_i, cz_i) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1))):
        box(f"Specch_Tassello_{idx_s}_{c_i}", D,
            sx_pos + cx_i * (sw * 0.5 - 0.28), -1.395,
            sz_pos + cz_i * (sh * 0.5 - 0.28), 0.15, 0.06, 0.15, ROSA_C,
            rot_y=math.radians(45))

# --- Cornicione orizzontale principale della galleria a mensole (z = 15.35 m) ---
box("Cornicione_Galleria", S, 0.0, -0.35, Z_GALLERIA, 30.6, 3.05, 0.44, BIANCO2)
box("Fregio_Sotto_Galleria", S, 0.0, -1.46, Z_GALLERIA - 0.34, 29.8, 0.26, 0.30, ROSA_C)
for m_k in range(38):
    mx = -14.4 + m_k * (28.8 / 37.0)
    box(f"Mensola_Galleria_{m_k}", D, mx, -1.62, Z_GALLERIA - 0.18, 0.22, 0.32, 0.24, PIETRA)

# =============================================================================
# 4. REGISTRO SUPERIORE CENTRALE — IL ROSONE DI CAMAINO (v2.7)
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
PAN_HW, PAN_HH = 3.55, 3.55            # pannello poco piu' largo della ghiera
GH_OUT_RX = RX_OCULO + 0.62            # filo esterno della ghiera
GH_OUT_RZ = RZ_OCULO + 0.62            # v2.7: apertura e corona circolari
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
            px, pz = rx * f * math.cos(a), rz * f * math.sin(a)
            onda = 0.0035 * math.sin(px * 4.1 + pz * 1.7) * math.sin(pz * 3.3 - px * 0.8)
            row.append(bm.verts.new((px, onda, pz)))
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
        f.smooth = True
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
BARRA_HW = 0.026
Y_PIOMBO = Y_VETRO - 0.035
# due soli montanti verticali interni (a un terzo del raggio), come in fotografia
for _x in (-RX_OCULO * 0.335, RX_OCULO * 0.335):
    _hh = RZ_OCULO * math.sqrt(max(0.0, 1.0 - (_x / RX_OCULO) ** 2)) - 0.02
    box(f"Piombo_Vert_{_x:+.2f}", R, _x, Y_PIOMBO, Z_OCULO,
        BARRA_HW * 2.0, 0.030, 2.0 * _hh, FERRO)
    box(f"Piombo_Vert_Filo_{_x:+.2f}", R, _x + BARRA_HW * 1.45, Y_PIOMBO - 0.018, Z_OCULO,
        BARRA_HW * 0.42, 0.012, 2.0 * _hh * 0.995, FERRO)
# cinque traversi orizzontali, equidistanti
for _k in range(-2, 3):
    _dz = _k * RZ_OCULO * 0.335
    _ww = RX_OCULO * math.sqrt(max(0.0, 1.0 - (_dz / RZ_OCULO) ** 2)) - 0.02
    box(f"Piombo_Orizz_{_k:+d}", R, 0.0, Y_PIOMBO, Z_OCULO + _dz,
        2.0 * _ww, 0.030, BARRA_HW * 2.0, FERRO)
    box(f"Piombo_Orizz_Filo_{_k:+d}", R, 0.0, Y_PIOMBO - 0.018, Z_OCULO + _dz + BARRA_HW * 1.45,
        2.0 * _ww * 0.995, 0.012, BARRA_HW * 0.42, FERRO)
# Telaio di piombo perimetrale (la ghiera del vetro, sottile e scura)
torus_ellipse("Piombo_Filo_Perimetrale", R, 0.0, Y_PIOMBO - 0.005, Z_OCULO,
              RX_OCULO - 0.02, RZ_OCULO - 0.02, 0.024, FERRO, seg_u=160, seg_v=8)

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
    ang = tilt + 0.35 * incl
    d = (t * math.cos(ang) + n * math.sin(ang)).normalized()
    # X = larghezza radiale, Y = profondita' (fronte verso -Y), Z = lunghezza
    # tangente.  Nella v2.6 X e Y erano scambiati e le foglie si disponevano
    # come scaglie piatte invece di riempire la fascia scolpita.
    xc = (n * math.cos(ang) - t * math.sin(ang)).normalized()
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
              GH_OUT_RX - 0.108, GH_OUT_RZ - 0.108, 0.036, BIANCO2, seg_u=160, seg_v=8)
torus_ellipse("Ghiera_Fondo_Rosa", R, 0.0, Y_PARETE - 0.045, Z_OCULO,
              GH_OUT_RX - 0.075, GH_OUT_RZ - 0.075, 0.150, PIETRA_RIL, seg_u=160, seg_v=10)
# gola in ombra subito dentro l'orlo (da' profondita' alla fascia)
torus_ellipse("Ghiera_Gola_Ombra", R, 0.0, Y_PARETE + 0.02, Z_OCULO,
              GH_OUT_RX - 0.150, GH_OUT_RZ - 0.150, 0.055, SGUINCIO, seg_u=160, seg_v=8)

# filo di perle appoggiato sul fondo rosa, sotto l'orlo
_bm_gh_perle = bmesh.new()
for k in range(196):
    a = math.tau * (k + 0.5) / 196
    Mp = _telaio_arco(a, GH_OUT_RX - 0.205, GH_OUT_RZ - 0.205, Z_OCULO, Y_PARETE - 0.055)
    _bm_sfera(_bm_gh_perle, Mp @ Matrix.Translation((0.0, 0.055, 0.0)),
              0.0, 0.0, 0.0, 0.032, sx=1.0, sy=0.75, sz=1.0, u=8, v=5)
_mesh_da_bmesh("Ghiera_Perlinatura", R, _bm_gh_perle, BIANCO, uv_scale=(1.0, 1.0))

# --- fogliame d'acanto corrente: due ordini sfalsati che corrono lungo l'arco
N_FOGLIE = 144
_bm_foglie_a = bmesh.new()
_bm_foglie_b = bmesh.new()
_bm_volute = bmesh.new()
_PROF_ACANTO = ((0.00, 0.15), (0.08, 0.31), (0.16, 0.22), (0.24, 0.48),
                (0.32, 0.30), (0.40, 0.54), (0.48, 0.32), (0.57, 0.48),
                (0.65, 0.27), (0.74, 0.37), (0.83, 0.19), (0.92, 0.15),
                (1.00, 0.015))
for k in range(N_FOGLIE):
    a = math.tau * (k + 0.5) / N_FOGLIE
    tilt = 0.34 if k % 2 == 0 else -0.34
    for riga, (dr_r, dr_z, lun, lar, bm_t, incl) in enumerate((
        (0.520, 0.520, 0.250, 0.138, _bm_foglie_a, 0.24),
        (0.355, 0.355, 0.215, 0.120, _bm_foglie_b, 0.28),
    )):
        aa = a + (0.5 * math.tau / N_FOGLIE if riga else 0.0)
        M_g = _telaio_arco(aa, GH_OUT_RX - dr_r, GH_OUT_RZ - dr_z, Z_OCULO,
                           Y_PARETE - 0.02, tilt=tilt, incl=incl)
        M_leaf = M_g @ Matrix.Translation((0.0, -0.010, -lun * 0.42))
        _bm_foglia(bm_t, lun, lar, 0.072, M_leaf, profilo=_PROF_ACANTO,
                   piega=0.15 * (1 if tilt > 0 else -1), gonfia=1.18)
        # costa centrale e due lobi appena sollevati: il rilievo non e' una
        # silhouette piatta, ma una foglia con una nervatura scolpita.
        _bm_sweep24(bm_t, M_leaf,
                    ((0.0, -0.030, lun * 0.07),
                     (0.0, -0.092, lun * 0.46),
                     (0.0, -0.034, lun * 0.88)),
                    (0.0055, 0.0080, 0.0030), lati=6,
                    ellisse=0.60, campioni=3)
        _bm_sfera(_bm_volute, M_g @ Matrix.Translation((0.0, -0.045, -lun * 0.40)),
                  0.0, 0.0, 0.0, 0.038, sx=1.15, sy=0.60, sz=1.15, u=10, v=6)
_mesh_da_bmesh("Ghiera_Fogliame_Esterno", R, _bm_foglie_a, PIETRA_ROS)
_mesh_da_bmesh("Ghiera_Fogliame_Interno", R, _bm_foglie_b, PIETRA_ROS)
_mesh_da_bmesh("Ghiera_Occhi_Volute", R, _bm_volute, BIANCO2)

# Dentelli minuti fra l'orlo e la perlinatura: una seconda scala di dettaglio
# che resta leggibile nel close-up senza trasformare la corona in borchie.
_bm_dentelli = bmesh.new()
for k in range(180):
    a = math.tau * (k + 0.5) / 180
    Md = _telaio_arco(a, GH_OUT_RX - 0.118, GH_OUT_RZ - 0.118,
                      Z_OCULO, Y_PARETE - 0.090)
    _bm_box(_bm_dentelli, Md @ Matrix.Translation((0.0, -0.022, 0.0)),
            0.0, 0.0, 0.0, 0.052, 0.052, 0.046)
_mesh_da_bmesh("Ghiera_Dentelli_Minuti", R, _bm_dentelli, BIANCO2)

# --- seconda fascia: corda intrecciata oro/avorio (treccia fitta a due capi)
torus_ellipse("Ghiera_Filo_Rosa_Interno", R, 0.0, Y_GHIERA + 0.055, Z_OCULO,
              RX_OCULO + 0.360, RZ_OCULO + 0.360, 0.070, ROSA, seg_u=160, seg_v=10)
_bm_corda_avorio = bmesh.new()
_bm_corda_oro = bmesh.new()
N_CORDA = 132
for k in range(N_CORDA):
    a = math.tau * (k + 0.5) / N_CORDA
    tilt = 0.70 if k % 2 == 0 else -0.70
    Mc = _telaio_arco(a, RX_OCULO + 0.262, RZ_OCULO + 0.262, Z_OCULO,
                      Y_GHIERA + 0.030, tilt=tilt, incl=0.16)
    _bm_box(_bm_corda_avorio if k % 4 else _bm_corda_oro,
            Mc @ Matrix.Translation((0.0, 0.012, 0.0)),
            0.0, 0.0, 0.0, 0.120, 0.072, 0.040)
_mesh_da_bmesh("Ghiera_Corda_Avorio", R, _bm_corda_avorio, BIANCO2)
_mesh_da_bmesh("Ghiera_Corda_Oro", R, _bm_corda_oro, ORO_MOS)

# --- orli modanati interno ed esterno della corda
torus_ellipse("Ghiera_Filo_Sopra_Corda", R, 0.0, Y_GHIERA + 0.085, Z_OCULO,
              RX_OCULO + 0.352, RZ_OCULO + 0.352, 0.030, BIANCO, seg_u=160, seg_v=8)
torus_ellipse("Ghiera_Filo_Interno", R, 0.0, Y_GHIERA + 0.085, Z_OCULO,
              RX_OCULO + 0.170, RZ_OCULO + 0.170, 0.044, BIANCO2, seg_u=160, seg_v=8)
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


def edicola_v27(name, col, cx, y, z0, w, h, variant=0):
    """Edicola laterale del rosone con catino concavo e vero altorilievo."""
    z_dav = z0 + 0.105 * h
    z_imp = z0 + 0.570 * h
    hw = 0.38 * w
    z_top = z_imp + hw

    box(f"{name}_Fondo_Rosa", col, cx, y + 0.205, (z_dav + z_top) * 0.5,
        0.88 * w, 0.075, z_top - z_dav + 0.045, RIGATO, fit_uv=True)
    # Catino semicircolare: il fondo arretra al centro e la luce descrive la
    # concavita'.  Niente parallelepipedo nero dietro la statua.
    bm_shell = bmesh.new()
    seg, rings = 32, 9
    center = bm_shell.verts.new((cx, y + 0.200, z_imp))
    rows = []
    for ir in range(1, rings + 1):
        r = ir / rings
        row = []
        for j in range(seg + 1):
            a = math.pi * j / seg
            row.append(bm_shell.verts.new((cx + hw * r * math.cos(a),
                                            y + 0.200 - 0.155 * r,
                                            z_imp + hw * r * math.sin(a))))
        rows.append(row)
    for j in range(seg):
        bm_shell.faces.new((center, rows[0][j], rows[0][j + 1]))
    for ir in range(rings - 1):
        for j in range(seg):
            bm_shell.faces.new((rows[ir][j], rows[ir + 1][j],
                                rows[ir + 1][j + 1], rows[ir][j + 1]))
    _mesh_da_bmesh(f"{name}_Catino", col, bm_shell, RIGATO, uv_scale=(0.85, 0.85))

    bm_w = bmesh.new()
    bm_r = bmesh.new()
    bm_f = bmesh.new()
    bm_c = bmesh.new()
    Mi = Matrix.Identity(4)
    for sd in (-1, 1):
        xs = cx + sd * w * 0.455
        _bm_box(bm_w, Mi, xs, y - 0.015, (z_dav + z_imp) * 0.5,
                w * 0.085, 0.155, z_imp - z_dav + 0.035)
        _bm_box(bm_r, Mi, xs, y - 0.100, (z_dav + z_imp) * 0.5,
                w * 0.022, 0.018, (z_imp - z_dav) * 0.88)
        for zz, ww, hh in ((z_dav + 0.015, 0.140, 0.040),
                           (z_imp - 0.025, 0.145, 0.045),
                           (z_imp + 0.018, 0.165, 0.028)):
            _bm_box(bm_w, Mi, xs, y - 0.025, zz, w * ww, 0.190, h * hh)
        # fogliolina del capitello
        _bm_foglia(bm_f, h * 0.050, w * 0.040, h * 0.012,
                   Mi @ Matrix.Translation((xs, y - 0.130, z_imp - h * 0.045)),
                   gonfia=1.15)
        # spallette strombate del vano
        _bm_box(bm_w, Mi, cx + sd * (hw + 0.010), y + 0.100,
                (z_dav + z_imp) * 0.5, 0.025, 0.220, z_imp - z_dav)

    arch(f"{name}_Arco_Esterno", col, cx, y - 0.065, z_imp,
         hw + 0.050, 0.030, BIANCO, seg_u=34, seg_v=10)
    arch(f"{name}_Arco_Rosa", col, cx, y - 0.048, z_imp,
         hw + 0.008, 0.018, ROSA, seg_u=32, seg_v=8)
    arch(f"{name}_Arco_Interno", col, cx, y - 0.025, z_imp,
         hw - 0.030, 0.016, BIANCO2, seg_u=30, seg_v=8)
    for k in range(21):
        a = math.pi * k / 20.0
        _bm_sfera(bm_f, Mi, cx - (hw + 0.050) * math.cos(a), y - 0.098,
                  z_imp + (hw + 0.050) * math.sin(a), 0.0085,
                  sy=0.70, u=7, v=5)
    # Costole sottili del catino, appena accennate come nell'originale.
    for k in range(1, 8):
        a = math.pi * k / 8.0
        _bm_sweep24(bm_r, Mi,
                    ((cx, y + 0.192, z_imp + 0.006),
                     (cx + hw * 0.52 * math.cos(a), y + 0.115,
                      z_imp + hw * 0.52 * math.sin(a)),
                     (cx + hw * 0.96 * math.cos(a), y + 0.052,
                      z_imp + hw * 0.96 * math.sin(a))),
                    (0.004, 0.006, 0.008), lati=6, ellisse=0.65, campioni=3)

    # Ghimberga alle spalle dell'arco: solo le modanature avanzano, cosi' la
    # testa non viene tagliata da un triangolo pieno.
    z_gb, z_ap = z0 + 0.735 * h, z0 + 1.025 * h
    hw_g = 0.53 * w
    prism(f"{name}_Campo_Ghimberga", col, cx, y + 0.115, z_gb,
          hw_g * 1.75, z_ap - z_gb, 0.055, BIANCO2)
    _bm_fascia_spiovente(bm_w, Mi, cx, hw_g, z_gb, z_ap, y - 0.050,
                         -0.008, 0.020, 0.065)
    _bm_fascia_spiovente(bm_r, Mi, cx, hw_g, z_gb, z_ap, y - 0.040,
                         0.020, 0.033, 0.045)
    _bm_fascia_spiovente(bm_w, Mi, cx, hw_g, z_gb, z_ap, y - 0.055,
                         0.033, 0.055, 0.055)
    ang = math.atan2(z_ap - z_gb, hw_g)
    for sd in (-1, 1):
        for k in range(5):
            t = 0.16 + 0.68 * k / 4.0
            gx = cx + sd * hw_g * (1.0 - t) + sd * math.sin(ang) * 0.045
            gz = z_gb + (z_ap - z_gb) * t + math.cos(ang) * 0.045
            _bm_foglia(bm_f, h * 0.050 * (1.05 - 0.22 * t), h * 0.022,
                       h * 0.013, Mi @ Matrix.Translation((gx, y - 0.070, gz))
                       @ Matrix.Rotation(-sd * ang * 0.88, 4, "Y"),
                       piega=-0.13 * sd, gonfia=1.22)
    _bm_lathe(bm_f, Mi @ Matrix.Translation((cx, y - 0.070, z_ap)),
              ((0.0, 0.025), (h * 0.025, 0.032), (h * 0.070, 0.012),
               (h * 0.095, 0.003)), seg=10, sy=0.88)

    # Davanzale cosmatesco e mensola a foglia che sostiene il busto.
    _bm_box(bm_w, Mi, cx, y - 0.040, z_dav - 0.018, w * 0.94, 0.225, 0.045)
    _bm_box(bm_c, Mi, cx, y - 0.158, z0 + 0.050 * h,
            w * 0.74, 0.018, h * 0.072)
    _bm_foglia(bm_f, h * 0.105, w * 0.115, h * 0.030,
               Mi @ Matrix.Translation((cx, y - 0.100, z0 + 0.065 * h)),
               piega=0.08, gonfia=1.30)

    _mesh_da_bmesh(f"{name}_Marmo", col, bm_w, BIANCO, uv_scale=(1.0, 1.0))
    _mesh_da_bmesh(f"{name}_Rosa", col, bm_r, ROSA, uv_scale=(1.0, 1.0))
    _mesh_da_bmesh(f"{name}_Scultura", col, bm_f, PIETRA_ROS, uv_scale=(1.1, 1.1))
    _mesh_da_bmesh(f"{name}_Cosmatesco", col, bm_c, COSMATE, uv_scale=(2.2, 2.2))
    return z_dav


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
    lato = -side  # il gesto e lo sguardo sono rivolti verso il rosone
    base_z = z_centro - h * 0.42
    x_fig = x + side * (0.18 if alto else 0.14)
    y_fig = y_pan - (0.16 if alto else 0.10)
    if alto:
        spec = dict(yaw=lato * 0.27, nod=0.07,
                    gesto="indica" if side < 0 else "parla",
                    barba=0.72 if side < 0 else 0.88,
                    copricapo="capelli_lunghi" if side < 0 else "capelli",
                    lato=lato, seed=3 if side < 0 else 5)
        M = (Matrix.Translation((x_fig, y_fig, base_z))
             @ Matrix.Rotation(lato * 0.09, 4, "Z")
             @ Matrix.Rotation(-side * 0.105, 4, "Y")
             @ Matrix.Diagonal((h * 1.02, h * 0.96, h * 0.96, 1.0)))
    else:
        spec = dict(yaw=lato * 0.24, nod=0.08,
                    gesto="rotolo" if side < 0 else "leggi",
                    barba=0.92 if side < 0 else 0.68,
                    copricapo="capelli_lunghi" if side < 0 else "capelli",
                    lato=lato, seed=7 if side < 0 else 9)
        M = (Matrix.Translation((x_fig, y_fig, base_z))
             @ Matrix.Rotation(lato * 0.08, 4, "Z")
             @ Matrix.Rotation(-side * 0.035, 4, "Y")
             @ Matrix.Diagonal((h * 1.02, h * 0.96, h * 0.96, 1.0)))
    _bm_box(bm, Matrix.Translation((x_fig, y_fig + 0.015, base_z + 0.012)),
            0.0, 0.0, 0.0, 0.43, 0.27, 0.050)
    _bm_figura_gotica_v27(bm, bm_pat, M, 1.0, spec)
    _mesh_da_bmesh(f"{name}_Marmo", col, bm, PIETRA_ROS, uv_scale=(1.2, 1.2))
    if len(bm_pat.faces):
        _mesh_da_bmesh(f"{name}_Incavi", col, bm_pat, PATINA_ROS, uv_scale=(1.2, 1.2))
    else:
        bm_pat.free()


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
    for k_r in range(16):
        rosetta_rilievo(f"Quatrifoglio_{tag}_{k_r}", D, side * 4.52, -1.645,
                        z_v0 + (z_v1 - z_v0) * (k_r + 0.5) / 16.0, 0.073, petals=4)
    _POSE_LAT_SX = ("parla", "pensatore", "libro", "petto_tavola")
    _POSE_LAT_DX = ("libro_chiuso", "rotolo", "leggi", "pensatore")
    for j in range(n_side):
        z_n = z_v0 + j * h_nside
        cx_n = side * 3.93
        z_dav = edicola_v27(
            f"Nicchia_Lat_{tag}_{j}", R, cx_n, -1.52,
            z_n, 0.94, h_nside * 0.99, variant=j,
        )
        gesto = (_POSE_LAT_SX if side < 0 else _POSE_LAT_DX)[j]
        if gesto == "leggi":
            gesto = "libro"
        spec = dict(gesto=gesto, barba=(0.05, 0.62, 0.88, 0.52)[j],
                    copricapo=("capelli", "capelli_lunghi", "berretta", "cappuccio")[j],
                    yaw=-side * (0.20 + 0.08 * (j % 2)), nod=0.10 + 0.05 * (j % 2),
                    seed=j * 3 + (0 if side < 0 else 1), lato=-side)
        bm_lat = bmesh.new()
        bm_lat_pat = bmesh.new()
        M_lat = (Matrix.Translation((cx_n, -1.655, z_dav + 0.018))
                 @ Matrix.Rotation(-side * 0.08, 4, "Z"))
        _bm_busto_profeta24(bm_lat, bm_lat_pat, M_lat, 0.68, h_nside * 0.70, spec)
        _mesh_da_bmesh(f"Statua_Lat_{tag}_{j}_Marmo", ST, bm_lat, PIETRA_ROS,
                       uv_scale=(1.3, 1.3))
        if len(bm_lat_pat.faces):
            _mesh_da_bmesh(f"Statua_Lat_{tag}_{j}_Incavi", ST, bm_lat_pat, PATINA_ROS,
                           uv_scale=(1.3, 1.3))
        else:
            bm_lat_pat.free()

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


# =============================================================================
# 5. LE DUE TORRI-PINNACOLO CHE AFFIANCANO LA CUSPIDE CENTRALE
# -----------------------------------------------------------------------------
# v3.3 — Rifatte sulla nuova fotografia frontale `riferimento_torri.jpg`
# (la foto allegata dall'utente, 1997x3043).  La v3.2, riletta su quella
# foto, sbagliava tre cose: il fusto era una gabbia di colonnine rotonde su
# pannelli rosa scuro a righe (nella foto e' una parete di lastre bianche
# con tre lesene piatte e due sole vene salmone sottili), le lancette erano
# quattro miniature per faccia (nella foto sono DUE grandi con ghimberghe,
# piu' tre strette sotto la cornice) e il coronamento era una lanterna
# traforata con vani neri (nella foto e' un grappolo PIENO di fogliame).
#
# Qui c'e' il vero torrione-pinnacolo senese, dalla base al vertice:
#
#   1. fusto a lastre di Marmo_Bianco con tre lesene piatte per faccia
#      (fronte e fianco esterno), due specchiature con una vena centrale
#      in marmo rosato chiaro, interrotta da fasce e registri;
#   2. registro grande di due lancette cieche con fondo rosato, doppia
#      ghiera e ghimberghe crochettate, e registro piccolo di tre lancette
#      strette sotto la cornice;
#   3. tre fasce marcapiano a dente di cane (dentelli a diamante su un filo
#      d'ombra di serpentino), non piu' le squame a archetti;
#   4. doccioni zoomorfi a due quote protesi in DIAGONALE dagli spigoli:
#      mensola, dorso inarcato, collo teso, fauci, orecchie e ali ripiegate;
#   5. coronamento pieno: cornice a tre fili con dentelli, plinto
#      ottagonale, quattro pinnacoletti diagonali a cresta fogliata e
#      bocciolo (senza guglia propria), guglia centrale interamente
#      crochettata con due figure in nicchia e due doccioni a mezza
#      altezza, capitello fogliato a coppa e grande statua sommitale.
# =============================================================================


def _bm_base_colonnina(bm, M, x, y, z0, r):
    """Base attica di colonnina: plinto, gola rovescia e listello d'imposta."""
    _bm_lathe(bm, M @ Matrix.Translation((x, y, z0)),
              ((0.000, r * 1.62), (0.026, r * 1.62), (0.034, r * 1.28),
               (0.052, r * 1.20), (0.078, r * 1.04), (0.104, r * 0.98)),
              seg=14, sy=1.0)


def _bm_capitello_colonnina(bm_w, bm_p, M, x, y, z0, r, lobi=8):
    """Capitello fogliato di colonnina con collarino e abaco."""
    _bm_lathe(bm_p, M @ Matrix.Translation((x, y, z0)),
              ((0.000, r * 0.90), (0.020, r * 1.08), (0.048, r * 1.26), (0.082, r * 1.34)),
              seg=14, sy=1.0)
    for k in range(lobi):
        a = math.tau * k / lobi
        d = Vector((math.cos(a), math.sin(a), 0.62)).normalized()
        Mc = (M @ Matrix.Translation((x + r * 0.96 * math.cos(a),
                                      y + r * 0.96 * math.sin(a), z0 + 0.024))
              @ d.to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm_p, 0.062 + r * 0.52, 0.024 + r * 0.30, 0.013,
                   Mc, piega=0.14, gonfia=1.22)
    _bm_box(bm_w, M, x, y, z0 + 0.094, r * 2.55, r * 2.55, 0.026)


def _bm_colonnina_torre(bm_w, bm_p, M, x, y, z0, z1, r, lobi=8, base=True):
    """Colonnina gotica scanalata: base, fusto a entasi, capitello."""
    if z1 - z0 < 0.30:
        return
    h = z1 - z0
    if base:
        _bm_base_colonnina(bm_w, M, x, y, z0, r)
    zs = z0 + (0.104 if base else 0.0)
    hs = max(0.12, (z1 - 0.11) - zs)
    _bm_lathe(bm_w, M @ Matrix.Translation((x, y, zs)),
              ((0.000, r * 0.995), (hs * 0.08, r * 0.985), (hs * 0.50, r * 0.940),
               (hs * 0.90, r * 0.885), (hs, r * 0.868)),
              seg=16, sy=1.0, rib=0.115, rib_n=lobi)
    _bm_capitello_colonnina(bm_w, bm_p, M, x, y, zs + hs, r, lobi=lobi)


def _bm_pinnacolo_torre(bm_w, bm_p, bm_d, M, x, y, z0, alt, larg, ghimberghe=True):
    """Pinnacolo gotico senese: zoccolo, fusto a nicchie cieche, nodo,
    guglia a quattro costole con gola (sezione a otto punti), gattoni lungo
    gli spigoli e bottone apicale.  E' la sagoma seghettata del colmo della
    torre in `riferimento_apice.jpg`."""
    hw = larg * 0.5
    _bm_box(bm_w, M, x, y, z0 + 0.020, larg * 1.24, larg * 1.24, 0.040)
    _bm_box(bm_p, M, x, y, z0 + 0.056, larg * 1.04, larg * 1.04, 0.030)

    # ---- fusto: quattro facce con nicchia cieca fra quattro spigoli --------
    h_f = alt * 0.30
    for k in range(4):
        R = Matrix.Rotation(k * math.pi * 0.5, 4, "Z")
        _bm_box(bm_d, M @ Matrix.Translation((x, y, z0)) @ R,
                0.0, -hw * 0.560, h_f * 0.44, hw * 1.02, 0.026, h_f * 0.60)
        _bm_arco_acuto(bm_w, M @ Matrix.Translation((x, y, z0)) @ R,
                       0.0, -hw * 0.610, h_f * 0.30, hw * 1.30, h_f * 0.58,
                       0.016, seg_u=10, seg_v=5)
    for sx2 in (-1, 1):
        for sy2 in (-1, 1):
            _bm_box(bm_w, M, x + sx2 * hw * 0.62, y + sy2 * hw * 0.62,
                    z0 + 0.075 + h_f * 0.5, 0.060, 0.060, h_f)

    # ---- nodo a collarino -------------------------------------------------
    z_cor = z0 + 0.075 + h_f
    _bm_box(bm_w, M, x, y, z_cor + 0.020, larg * 0.94, larg * 0.94, 0.042)
    _bm_box(bm_p, M, x, y, z_cor + 0.056, larg * 1.16, larg * 1.16, 0.034)

    # ---- guglia: sezione a otto punti (quattro costole e quattro gole) ----
    z_s0 = z_cor + 0.080
    h_s = alt * 0.56
    prof = ((0.000, 0.980), (0.200, 0.800), (0.440, 0.560),
            (0.680, 0.320), (0.880, 0.120), (1.000, 0.016))
    grid = []
    for t, rf in prof:
        row = []
        for j in range(8):
            a = math.tau * j / 8.0 + math.pi * 0.25
            rr = hw * rf * (1.0 if j % 2 == 0 else 0.66)
            row.append(bm_w.verts.new(
                M @ Vector((x + rr * math.cos(a), y + rr * math.sin(a), z_s0 + h_s * t))))
        grid.append(row)
    for i in range(len(grid) - 1):
        for j in range(8):
            j2 = (j + 1) % 8
            bm_w.faces.new((grid[i][j], grid[i][j2], grid[i + 1][j2], grid[i + 1][j]))
    bm_w.faces.new(list(reversed(grid[0])))

    # ---- gattoni lungo le quattro costole --------------------------------
    for k in range(4):
        a = math.tau * k / 4.0 + math.pi * 0.25
        ca, sa = math.cos(a), math.sin(a)
        for j in range(4):
            t = 0.06 + 0.235 * j
            rf = 0.980 + (0.016 - 0.980) * t
            rr = hw * rf
            Mf = (M @ Matrix.Translation((x + rr * ca, y + rr * sa, z_s0 + h_s * t))
                  @ Vector((ca, sa, 1.55)).normalized()
                  .to_track_quat("Z", "Y").to_matrix().to_4x4())
            _bm_foglia(bm_p, alt * 0.085 * (1.0 - 0.25 * t), alt * 0.060 * (1.0 - 0.2 * t),
                       alt * 0.024, Mf, piega=0.26, gonfia=1.30)

    # ---- bottone apicale -------------------------------------------------
    _bm_lathe(bm_p, M @ Matrix.Translation((x, y, z_s0 + h_s * 0.92)),
              ((0.0, hw * 0.135), (hw * 0.13, hw * 0.180), (hw * 0.26, hw * 0.090)),
              seg=8, sy=1.0)
    _bm_sfera(bm_p, M, x, y, z_s0 + h_s + hw * 0.055, hw * 0.085, sz=1.5, u=8, v=6)


def _bm_doccione_torre(bm, base, dx, dy, lung, r):
    """Doccione zoomorfo proteso in diagonale da uno spigolo della torre.

    Il corpo e' costruito in un telaio locale con +X lungo la direzione di
    proiezione (dx, dy): mensola fogliata d'innesto, dorso inarcato, collo
    teso, testa con fauci e ali ripiegate.  Nella fotografia i doccioni non
    sporgono frontalmente come stecche, ma in diagonale dagli spigoli.
    """
    yaw = math.atan2(dy, dx)
    M = Matrix.Translation(base) @ Matrix.Rotation(yaw, 4, "Z")
    # mensola d'innesto
    _bm_box(bm, M, -lung * 0.06, 0.0, -r * 0.30, lung * 0.30, r * 2.2, r * 2.0)
    # dorso inarcato e collo che ricade: la testa finisce sotto la schiena,
    # protesa in avanti e in basso come i doccioni della fotografia
    _bm_segmento(bm, M, (-lung * 0.10, 0.0, 0.0), (lung * 0.34, 0.0, r * 0.55),
                 r * 1.02, r * 0.70, seg=10, sy=0.88)
    _bm_segmento(bm, M, (lung * 0.34, 0.0, r * 0.55), (lung * 0.72, 0.0, -r * 0.55),
                 r * 0.68, r * 0.46, seg=10, sy=0.86)
    # zampe anteriori ripiegate sotto il petto
    for sz in (-1, 1):
        _bm_segmento(bm, M, (lung * 0.30, sz * r * 0.55, -r * 0.10),
                     (lung * 0.52, sz * r * 0.45, -r * 0.85),
                     r * 0.30, r * 0.18, seg=7)
    # testa allungata, muso aperto e orecchie appuntite
    _bm_sfera(bm, M, lung * 0.80, 0.0, -r * 0.72, r * 0.72,
              sx=1.45, sy=0.82, sz=0.80, u=12, v=8)
    _bm_segmento(bm, M, (lung * 0.86, 0.0, -r * 0.50), (lung * 1.02, 0.0, -r * 0.78),
                 r * 0.40, r * 0.16, seg=8, sy=0.78)
    _bm_segmento(bm, M, (lung * 0.84, 0.0, -r * 0.88), (lung * 0.98, 0.0, -r * 1.28),
                 r * 0.30, r * 0.12, seg=7, sy=0.75)
    for sz in (-1, 1):
        _bm_cono(bm, M, lung * 0.74, sz * r * 0.42, -r * 0.30, r * 0.16, r * 0.02,
                 r * 0.85, seg=6)
        # ala ripiegata lungo il fianco
        _bm_foglia(bm, r * 2.4, r * 0.85, r * 0.22,
                   M @ Matrix.Translation((lung * 0.10, sz * r * 0.62, r * 0.40))
                   @ Matrix.Rotation(math.radians(-102), 4, "Y")
                   @ Matrix.Rotation(sz * math.radians(22), 4, "X"),
                   piega=-0.10, gonfia=1.05)


def _bm_finnial_torre(bm_w, bm_p, M, x, y, z0, alt, larg):
    """Pinnacoletto laterale del coronamento: dado, fusto a costole, cresta
    fogliata a sega e bocciolo a tulipano.  Nella fotografia i pinnacoli
    laterali NON hanno una guglia propria: finiscono con un bocciolo."""
    hw = larg * 0.5
    _bm_box(bm_w, M, x, y, z0 + 0.035, larg * 1.30, larg * 1.30, 0.070)
    _bm_box(bm_p, M, x, y, z0 + 0.088, larg * 1.08, larg * 1.08, 0.046)
    h_f = alt * 0.52
    _bm_box(bm_w, M, x, y, z0 + 0.11 + h_f * 0.5, larg * 0.72, larg * 0.72, h_f)
    for sx2 in (-1, 1):
        for sy2 in (-1, 1):
            _bm_box(bm_w, M, x + sx2 * hw * 0.42, y + sy2 * hw * 0.42,
                    z0 + 0.11 + h_f * 0.5, larg * 0.22, larg * 0.22, h_f * 1.02)
    # cresta fogliata: foglie verticali a sega sui quattro spigoli
    for k in range(4):
        a = math.tau * k / 4.0 + math.pi * 0.25
        ca, sa = math.cos(a), math.sin(a)
        for j in range(3):
            t = j / 2.0
            Mf = (M @ Matrix.Translation((x + ca * hw * 0.46, y + sa * hw * 0.46,
                                          z0 + 0.14 + h_f * (0.55 + 0.42 * t)))
                  @ Vector((ca, sa, 1.15)).normalized()
                  .to_track_quat("Z", "Y").to_matrix().to_4x4())
            _bm_foglia(bm_p, alt * 0.20 * (1.0 - 0.22 * t), larg * 0.30,
                       larg * 0.11, Mf, piega=0.24, gonfia=1.25)
    # bocciolo a tulipano
    z_b = z0 + 0.11 + h_f
    _bm_lathe(bm_p, M @ Matrix.Translation((x, y, z_b)),
              ((0.000, hw * 0.30), (0.045, hw * 0.52), (0.120, hw * 0.60),
               (0.200, hw * 0.34), (0.260, hw * 0.10)),
              seg=10, sy=1.0)
    _bm_sfera(bm_p, M, x, y, z_b + alt * 0.30, hw * 0.20, sz=1.35, u=8, v=6)


def _torre_pinnacolo(side, cx_vis, w_vis, cx, tag):
    """v3.5 — Fusto a lastre di marmo bianco con due specchiature, registro
    grande di due lancette con ghimberghe, registro piccolo sotto la cornice,
    fasce a dente di cane, doccioni diagonali agli spigoli e coronamento
    PIENO: guglia scolpita a fogliame con figure e doccioni, quattro
    pinnacoletti a bocciolo e grande statua sommitale.  Niente piu' lanterna
    traforata con i vani neri, che nella fotografia non esiste."""
    bm_w = bmesh.new()      # marmo bianco: lastre, lesene, cornici, guglia
    bm_p = bmesh.new()      # pietra scolpita: gattoni, foglie, doccioni
    bm_s = bmesh.new()      # serpentino: solo fili d'ombra sotto le fasce
    bm_r = bmesh.new()      # marmo rosato chiaro: vena centrale e fondi lancette
    Mi = Matrix.Identity(4)

    z0, z1 = 19.58, 27.30            # fusto fra il registro basso e la cornice
    hw = w_vis * 0.5                 # 0.67 m
    y_c = -1.02                      # asse del coronamento

    # quote dei registri (uguali su fronte e fianco esterno)
    Z_BANDA = (21.92, 24.52, 25.98)  # fasce a dente di cane
    ZB_LANC, ZS_LANC = 22.14, 23.28  # registro grande: corpo e imposta arco
    RISE_LANC = 0.44
    ZB_MINI, ZS_MINI = 26.18, 26.58  # registro piccolo sotto la cornice
    RISE_MINI = 0.26

    def fascia(frame, hwl, zb):
        """Fascia marcapiano senese: filo d'ombra, lastra aggettante e fila
        di dentelli a diamante (il 'dente di cane' della fotografia)."""
        _bm_box(bm_s, frame, 0.0, -0.006, zb - 0.052, hwl * 2.0 + 0.05, 0.030, 0.026)
        _bm_box(bm_w, frame, 0.0, -0.028, zb, hwl * 2.0 + 0.10, 0.085, 0.075)
        n = max(5, int((hwl * 2.0) / 0.115))
        for i in range(n):
            xx = -hwl + (i + 0.5) * (2.0 * hwl / n)
            _bm_box(bm_p, frame, xx, -0.058, zb - 0.085, 0.062, 0.045, 0.062,
                    rot=Matrix.Rotation(math.pi * 0.25, 4, "Y"))

    def lancetta(frame, xx, zb, zs, span, rise, ghimberga_h, infill=True):
        """Lancetta cieca grande: fondo rosato chiaro incassato, doppia
        ghiera, montanti e ghimberga piena crochettata con bottone."""
        if infill:
            _bm_lastra(bm_r, frame,
                       [(xx - span * 0.26, zb), (xx + span * 0.26, zb),
                        (xx + span * 0.26, zs), (xx, zs + rise * 0.82),
                        (xx - span * 0.26, zs)],
                       0.020, y0=-0.026)
        _bm_arco_acuto(bm_w, frame, xx, -0.040, zs, span, rise, 0.030,
                       seg_u=14, seg_v=6)
        _bm_arco_acuto(bm_p, frame, xx, -0.052, zs, span * 0.78, rise * 0.82,
                       0.014, seg_u=14, seg_v=5)
        for s2 in (-1, 1):
            _bm_box(bm_w, frame, xx + s2 * span * 0.50, -0.038,
                    (zb + zs) * 0.5, 0.034, 0.055, zs - zb)
        if ghimberga_h > 0:
            # timpano pieno della ghimberga (nella foto non e' un contorno)
            _bm_lastra(bm_w, frame,
                       [(xx - span * 0.60, zs + rise * 0.50),
                        (xx + span * 0.60, zs + rise * 0.50),
                        (xx, zs + rise * 0.55 + ghimberga_h)],
                       0.030, y0=-0.030)
            _bm_ghimberga(bm_w, frame, xx, span * 0.60, zs + rise * 0.55,
                          zs + rise * 0.55 + ghimberga_h, -0.034, 0.034, 0.045,
                          crockets=bm_p, n_croc=4, croc_size=0.052)
            _bm_sfera(bm_p, frame, xx, -0.052, zs + rise * 0.55 + ghimberga_h + 0.02,
                      0.034, sz=1.45, u=8, v=6)

    def faccia(frame, hwl):
        """Una faccia della torre in coordinate locali: x sulla larghezza,
        y negativo verso l'osservatore, z assoluta."""
        # lastra di fondo in marmo bianco (niente piu' pannelli rosa scuro)
        _bm_box(bm_w, frame, 0.0, 0.030, (z0 + z1) * 0.5,
                hwl * 2.0, 0.070, (z1 - z0) - 0.10)
        # lesene piatte: due agli spigoli, una centrale (la foto ne mostra
        # 3), ma a tratti: si fermano sotto i registri di lancette
        for xx, wl in ((-hwl * 0.93, 0.15), (0.0, 0.11), (hwl * 0.93, 0.15)):
            for za, zb2 in ((z0 + 0.10, ZB_LANC - 0.05),
                            (Z_BANDA[1] + 0.07, ZB_MINI - 0.05),
                            (ZS_MINI + RISE_MINI + 0.34, z1 - 0.06)):
                _bm_box(bm_w, frame, xx, -0.018, (za + zb2) * 0.5,
                        wl, 0.055, zb2 - za)
                _bm_box(bm_p, frame, xx, -0.030, (za + zb2) * 0.5,
                        wl * 0.34, 0.030, zb2 - za)
        # vena salmone sottile al centro di ciascuna delle due specchiature:
        # due sole strisce chiare, interrotte dai registri e dalle fasce
        for xx in (-hwl * 0.47, hwl * 0.47):
            for za, zb2 in ((z0 + 0.14, Z_BANDA[0] - 0.10),
                            (Z_BANDA[1] + 0.10, Z_BANDA[2] - 0.10)):
                _bm_box(bm_r, frame, xx, -0.012, (za + zb2) * 0.5,
                        hwl * 0.26, 0.026, zb2 - za)
        # registro grande: DUE lancette con ghimberghe (non quattro piccole)
        for xx in (-hwl * 0.47, hwl * 0.47):
            lancetta(frame, xx, ZB_LANC, ZS_LANC, hwl * 0.60, RISE_LANC, 0.62)
        # registro piccolo sotto la cornice: tre lancette strette
        for xx in (-hwl * 0.60, 0.0, hwl * 0.60):
            lancetta(frame, xx, ZB_MINI, ZS_MINI, hwl * 0.36, RISE_MINI, 0.30,
                     infill=False)
            _bm_box(bm_r, frame, xx, -0.024, (ZB_MINI + ZS_MINI) * 0.5,
                    hwl * 0.09, 0.018, ZS_MINI - ZB_MINI)
        for zb in Z_BANDA:
            fascia(frame, hwl, zb)
        # zoccolo d'imposta della faccia
        _bm_box(bm_w, frame, 0.0, -0.026, z0 + 0.055, hwl * 2.0 + 0.08, 0.080, 0.11)

    # fronte e fianco esterno (quello che si vede in tre quarti)
    faccia(Matrix.Translation((cx_vis, -1.638, 0.0)), hw)
    faccia(Matrix.Translation((cx_vis + side * 0.675, -0.95, 0.0))
           @ Matrix.Rotation(side * math.pi * 0.5, 4, "Z"), 0.585)

    # ------------------------------------------------------------ doccioni
    # due quote, agli spigoli frontali, protesi in diagonale in fuori
    for zz in (Z_BANDA[0] + 0.06, Z_BANDA[2] + 0.04):
        for s2 in (-1, 1):
            _bm_doccione_torre(bm_p, Vector((cx_vis + s2 * 0.60, -1.60, zz)),
                               s2 * 0.72, -0.70, 0.66, 0.100)

    # ------------------------------------------------------------ cornice
    for i, (dz, ag, dep) in enumerate(((0.055, 0.14, 1.62), (0.135, 0.22, 1.56),
                                       (0.215, 0.12, 1.50))):
        _bm_box(bm_w if i != 1 else bm_p, Mi, cx_vis, y_c + 0.06, z1 + dz,
                w_vis + ag, dep, 0.075)
    for i in range(9):
        _bm_box(bm_p, Mi, cx_vis - 0.56 + i * 0.14, -1.80, z1 + 0.055,
                0.075, 0.10, 0.062, rot=Matrix.Rotation(math.pi * 0.25, 4, "Y"))

    # ========================================================== CORONAMENTO
    # Grappolo pieno e scolpito, come nella fotografia: plinto ottagonale,
    # quattro pinnacoletti a bocciolo, guglia centrale interamente coperta
    # di fogliame con figure e doccioni, capitello fogliato e statua.
    z_pl = z1 + 0.30
    _bm_lathe(bm_w, Mi @ Matrix.Translation((cx_vis, y_c, z1 + 0.235)),
              ((0.000, 0.600), (0.035, 0.600), (0.060, 0.545)), seg=8, sy=1.0)
    _bm_lathe(bm_r, Mi @ Matrix.Translation((cx_vis, y_c, z1 + 0.270)),
              ((0.000, 0.545), (0.038, 0.545), (0.055, 0.505)), seg=8, sy=1.0)

    # quattro pinnacoletti diagonali a bocciolo
    for k in range(4):
        a = math.tau * k / 4.0 + math.pi * 0.25
        px = cx_vis + 0.46 * math.cos(a)
        py = y_c + 0.46 * math.sin(a)
        _bm_finnial_torre(bm_w, bm_p, Mi, px, py, z_pl, 1.00, 0.30)

    # ------------------------------------------- guglia centrale scolpita
    # v3.5: guglia piu' massiccia alla base e piu' ricca di fogliame, come
    # nella fotografia: base allargata, collarino fogliato, dodici corone di
    # gattoni (invece di nove) e foglie piu' grandi in basso, ghimberghe
    # piramidali piu' marcate e due doccioni a mezza altezza.
    L_GUGL = 3.20
    z_s0, z_s1 = z_pl + 0.06, z_pl + 0.06 + L_GUGL
    # zoccolo / collarino fogliato alla base della guglia (parte massiccia)
    _bm_lathe(bm_p, Mi @ Matrix.Translation((cx_vis, y_c, z_s0 - 0.12)),
              ((0.000, 0.400), (0.060, 0.420), (0.130, 0.395), (0.200, 0.355)),
              seg=12, sy=1.0, rib=0.12, rib_n=8)
    for k in range(8):
        a = math.tau * k / 8.0
        Mf = (Mi @ Matrix.Translation((cx_vis + 0.34 * math.cos(a),
                                       y_c + 0.34 * math.sin(a), z_s0 - 0.02))
              @ Vector((math.cos(a), math.sin(a), 0.35)).normalized()
              .to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm_p, 0.18, 0.11, 0.045, Mf, piega=0.22, gonfia=1.40)
    _bm_lathe(bm_w, Mi @ Matrix.Translation((cx_vis, y_c, z_s0 - 0.10)),
              ((0.000, 0.360), (0.070, 0.340), (0.120, 0.300)), seg=8, sy=1.0)
    _bm_lathe(bm_w, Mi @ Matrix.Translation((cx_vis, y_c, z_s0)),
              ((0.000, 0.360), (0.700, 0.290), (1.500, 0.210),
               (2.300, 0.130), (3.000, 0.072), (L_GUGL, 0.040)),
              seg=16, sy=1.0, rib=0.16, rib_n=8)
    # ghimberghe piramidali a due ordini, sulla guglia, piu' marcate
    for zq in (0.95, 1.90):
        t_q = zq / L_GUGL
        rr_q = 0.36 * (1.0 - t_q) + 0.04 * t_q
        for k in range(4):
            a = math.tau * k / 4.0 + math.pi * 0.25
            px = cx_vis + (rr_q + 0.03) * math.cos(a)
            py = y_c + (rr_q + 0.03) * math.sin(a)
            _bm_cono(bm_w, Mi, px, py, z_s0 + zq + 0.14, 0.100, 0.0, 0.28,
                     rot=Matrix.Rotation(a, 4, "Z"), seg=4)
            _bm_sfera(bm_p, Mi, px, py, z_s0 + zq + 0.30, 0.036, u=6, v=4)
    # gattoni a corona su tutta la guglia: dodici corone, piu' fitte e piu'
    # grandi in basso (cono di fogliame piu' massiccio alla base)
    for j in range(12):
        t = 0.02 + 0.082 * j
        rr = 0.360 * (1.0 - t) + 0.040 * t
        for k in range(8):
            a = math.tau * k / 8.0 + (math.pi * 0.125 if j % 2 else 0.0)
            ca, sa = math.cos(a), math.sin(a)
            Mf = (Mi @ Matrix.Translation((cx_vis + rr * ca, y_c + rr * sa,
                                           z_s0 + (z_s1 - z_s0) * t))
                  @ Vector((ca, sa, 0.55)).normalized()
                  .to_track_quat("Z", "Y").to_matrix().to_4x4())
            _bm_foglia(bm_p, 0.165 * (1.0 - 0.28 * t), 0.095, 0.040, Mf,
                       piega=0.30, gonfia=1.38)
    # due doccioni che sporgono dalla guglia a mezza altezza
    for s2 in (-1, 1):
        _bm_doccione_torre(bm_p, Vector((cx_vis + s2 * 0.16, y_c - 0.16,
                                         z_s0 + 0.92)),
                           s2 * 0.68, -0.74, 0.46, 0.070)
    # figure nelle nicchie della guglia: fronte e fianco esterno
    for k, (fx, fy, rot) in enumerate((
            (cx_vis, y_c - 0.275, 0.0),
            (cx_vis + side * 0.275, y_c, side * math.pi * 0.5))):
        _bm_lathe(bm_p, Mi @ Matrix.Translation((fx, fy, z_s0 + 0.02)),
                  ((0.000, 0.085), (0.035, 0.105), (0.070, 0.070)), seg=10, sy=1.0)
        statua_gotica_v26(
            f"Figura_Guglia_Torre_{tag}_{k}", ST, fx, fy, z_s0 + 0.055, 0.50,
            spec=dict(gesto="petto" if k == 0 else "libro", barba=0.35,
                      copricapo="cappuccio", yaw=0.0, nod=0.08,
                      seed=5 + k * 7, lato=1, rot_z=rot,
                      scala_plinto=0.55),
            material=PIETRA_RIL)

    # -------------------------------- capitello fogliato e statua sommitale
    _bm_lathe(bm_p, Mi @ Matrix.Translation((cx_vis, y_c, z_s1 - 0.03)),
              ((0.000, 0.070), (0.055, 0.120), (0.130, 0.160),
               (0.190, 0.125), (0.225, 0.095)),
              seg=12, sy=1.0, rib=0.10, rib_n=8)
    for k in range(8):
        a = math.tau * k / 8.0
        Mf = (Mi @ Matrix.Translation((cx_vis + 0.110 * math.cos(a),
                                       y_c + 0.110 * math.sin(a), z_s1 + 0.055))
              @ Vector((math.cos(a), math.sin(a), 1.05)).normalized()
              .to_track_quat("Z", "Y").to_matrix().to_4x4())
        _bm_foglia(bm_p, 0.135, 0.062, 0.030, Mf, piega=0.18, gonfia=1.25)
    statua_gotica_v26(
        f"Statua_Sommitale_Torre_{tag}", ST, cx_vis, y_c - 0.010, z_s1 + 0.20,
        1.42,
        spec=dict(
            gesto=("croce" if side < 0 else "libro"),
            barba=(0.30 if side < 0 else 0.0),
            copricapo=("velo" if side < 0 else "cappuccio"),
            yaw=(-0.16 if side < 0 else 0.14), nod=0.06,
            seed=11 if side < 0 else 23, lato=(-1 if side < 0 else 1),
        ),
        material=PIETRA,
    )

    _mesh_da_bmesh(f"Torre_Fusto_Marmo_{tag}", G, bm_w, BIANCO)
    _mesh_da_bmesh(f"Torre_Fusto_Scolpito_{tag}", G, bm_p, PIETRA_RIL)
    _mesh_da_bmesh(f"Torre_Fusto_Serpentino_{tag}", G, bm_s, VERDE)
    _mesh_da_bmesh(f"Torre_Fusto_Rigato_{tag}", G, bm_r, ROSA_C)


def pilastro_centrale_completo(side):
    # Il fusto visibile del pilastro polistilo corre da |x| = 4.68 m (subito
    # fuori dal fregio di quatrifogli) fino a |x| = 6.02 m (dove si innesta
    # senza alcuno stacco lo spigolo interno del frontone laterale dei mosaici),
    # mentre una spalla interna a |x| = 4.42..4.70 m raccorda la cuspide
    # centrale sopra la trabeazione.
    cx_vis = side * 5.35
    w_vis = 1.40
    cx = side * 5.18
    tag = "Sx" if side < 0 else "Dx"
    h_shaft = Z_PIL_TOP - Z_GALLERIA
    z_mid = Z_GALLERIA + h_shaft * 0.5

    # Nucleo strutturale pieno fino al retro (nessuna fessura col corpo centrale
    # o laterale).  Il colmo scende a 27,12 m: sopra la cornice della torre il
    # coronamento a pinnacoli e' libero, come nella fotografia.
    z_top_box = 27.12
    box(f"Pilastro_Centrale_{tag}", G, side * 5.22, -0.15,
        (Z_GALLERIA + z_top_box) * 0.5, 1.60, 2.80, z_top_box - Z_GALLERIA, BIANCO)

    # Edicola d'angolo alla fine della Galleria dei Profeti (|x| = 4.45..4.70 m,
    # sopra il fregio di quatrifogli, ben visibile in riferimento_cuspidi.jpg).
    z_gal0 = Z_PAN + PAN_HH + 0.10
    h_gal0 = Z_TIMPANO - z_gal0 - 0.13
    edicola_galleria_profeta(
        f"Nicchia_Angolo_Profeti_{tag}", R, side * 4.56, -1.555,
        z_gal0, 0.28, h_gal0, variant=0 if side < 0 else 14,
    )

    # Statue inferiori alla base del pilastro (z = 15.65 m)
    for s2 in (-1, 1):
        sx_st = cx_vis + s2 * 0.32
        statue(f"Statua_PilCent_{tag}_{s2}", ST, sx_st, -1.68, Z_GALLERIA + 0.22, 1.55, PIETRA)

    # Costruzione gotica scolpita ad alta definizione del registro della loggia,
    # del fusto mediano e della guglia sommitale (bmesh consolidati)
    bm_w = bmesh.new()   # elementi in Marmo_Bianco
    bm_p = bmesh.new()   # elementi scolpiti / gattoni / capitelli in Pietra_Statue
    bm_pat_pil = bmesh.new()
    Mi = Matrix.Identity(4)

    # 1) Registro gotico scolpito all'imposta delle cuspidi laterali (z = 17.46..19.48 m):
    #    due alte ghimberghe acute con triplice archetto, 3 pinnacolini con edicola
    #    fogliata e grande cornicione poligonale aggettante a z = 19.38 m che
    #    ammorsa direttamente lo spigolo interno del frontone laterale dei mosaici!
    z_gh_low = 17.50
    h_gh_low = 1.08
    for s2 in (-1, 1):
        gx_l = cx_vis + s2 * 0.31
        gw_l = 0.62
        for ord_k, (sp_k, rs_k, y_k, min_k) in enumerate((
            (gw_l * 0.88, h_gh_low * 0.62, -1.65, 0.032),
            (gw_l * 0.68, h_gh_low * 0.50, -1.62, 0.026),
            (gw_l * 0.48, h_gh_low * 0.38, -1.59, 0.020),
        )):
            _bm_arco_acuto(bm_w if ord_k % 2 == 0 else bm_p, Mi, gx_l, y_k, z_gh_low - 0.18, sp_k, rs_k, min_k, seg_u=14, seg_v=6)
        ang_l = math.atan2(h_gh_low, gw_l * 0.5)
        sl_l = math.hypot(gw_l * 0.5, h_gh_low) + 0.05
        for gs in (-1, 1):
            _bm_box(
                bm_w, Mi, gx_l + gs * gw_l * 0.25, -1.67, z_gh_low + h_gh_low * 0.5,
                sl_l, 0.18, 0.068, rot=Matrix.Rotation(gs * ang_l, 4, "Y"),
            )
            for kc in range(4):
                tc = 0.16 + 0.70 * kc / 3.0
                _bm_foglia(
                    bm_p, 0.14, 0.078, 0.045,
                    Matrix.Translation((gx_l + gs * gw_l * 0.5 * (1.0 - tc), -1.69, z_gh_low + h_gh_low * tc + 0.03))
                    @ Matrix.Rotation(gs * 0.44, 4, "Y"),
                    piega=-0.15 * gs,
                )
        # Fiorone a cesto fogliato sulla punta di ciascuna ghimberga
        _bm_lathe(
            bm_p, Matrix.Translation((gx_l, -1.68, z_gh_low + h_gh_low)),
            ((0.0, 0.050), (0.10, 0.072), (0.24, 0.024)), seg=8, sy=0.88,
        )
        # Archetti ciechi superiori fra le punte delle ghimberghe e il cornicione (z = 18.60..19.32 m)
        _bm_arco_acuto(bm_w, Mi, gx_l, -1.62, 18.88, gw_l * 0.72, 0.36, 0.026, seg_u=12, seg_v=6)

    # 3 lesene/pinnacolini verticali con fiorone scolpito (sulle 3 nervature principali del registro basso)
    for s3 in (-0.59, 0.0, 0.59):
        px_l = cx_vis + s3
        _bm_box(bm_w, Mi, px_l, -1.65, 18.38, 0.13, 0.22, 1.85)
        _bm_lathe(
            bm_p, Matrix.Translation((px_l, -1.69, 18.62)),
            ((0.0, 0.055), (0.11, 0.078), (0.25, 0.028)), seg=8, sy=0.88,
        )
    # Cornicione poligonale sagomato a z = 19.36..19.50 m (corona il registro
    # inferiore del pilastro e si salda allo spigolo interno della cuspide laterale!)
    _bm_box(bm_w, Mi, cx_vis, -0.64, 19.38, w_vis + 0.18, 2.08, 0.11)
    _bm_box(bm_p, Mi, cx_vis, -0.66, 19.47, w_vis + 0.22, 2.12, 0.085)
    _bm_box(bm_pat_pil, Mi, cx_vis, -0.65, 19.30, w_vis + 0.14, 2.04, 0.050)
    for s_cr in (-0.59, -0.23, 0.0, 0.23, 0.59):
        _bm_box(bm_w, Mi, cx_vis + s_cr, -1.66, 19.42, 0.19, 0.26, 0.17)
        _bm_box(bm_pat_pil, Mi, cx_vis + s_cr, -1.65, 19.31, 0.17, 0.24, 0.048)

    # Doccioni zoomorfi alla base delle ghimberghe del pilastro (z = 17.52 m, ben visibili in foto!)
    gargolla(f"Gargolla_Pil_Loggia_{tag}_Est", D, cx_vis + side * 0.62, -1.58, 17.52, side, 0.52, 0.078, PIETRA, pitch_deg=-10.0)
    gargolla(f"Gargolla_Pil_Loggia_{tag}_Cen", D, cx_vis, -1.62, 17.48, side, 0.44, 0.072, PIETRA, pitch_deg=-12.0)

    # Consolidamento del registro inferiore del pilastro (v3.2)
    _mesh_da_bmesh(f"Registro_Basso_Torre_Marmo_{tag}", G, bm_w, BIANCO)
    _mesh_da_bmesh(f"Registro_Basso_Torre_Scolpito_{tag}", G, bm_p, PIETRA_RIL)
    _mesh_da_bmesh(f"Registro_Basso_Torre_Patina_{tag}", G, bm_pat_pil, PATINA)

    # Fusto, registri di lancette, doccioni e coronamento: v3.2
    _torre_pinnacolo(side, cx_vis, w_vis, cx, tag)


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
# 6.6 — LE DUE CUSPIDI LATERALI DEI MOSAICI (v3.0)
#    Presentazione al tempio (sinistra) e Natività (destra).  v3.0:
#    gattoni a giglio, cornice a mitra con gole d'ombra e banda a ovoli,
#    mosaici 1536 px de-velati, base a ovoli con fascia di serpentino e
#    statue apicali femminili su capitello di foglie.
# =============================================================================
def _apertura_cuspide(W, H, o):
    """Apertura interna di una cuspide arretrata di `o` (distanza
    perpendicolare) dal filo esterno: (semilarghezza alla base, quota apice).

    La linea interna è parallela allo spiovente, quindi il triangolo resta
    simile all'esterno: il fattore di scala è k = 1 - 2·L·o/(W·H), con
    L = lunghezza dello spiovente.  (Nella v2.7 il fattore era applicato al
    contrario e l'apertura riusciva più stretta del dovuto, lasciando una
    fascia di marmo fra cornice e mosaico.)
    """
    L = math.hypot(W * 0.5, H)
    k = max(0.30, 1.0 - 2.0 * L * o / max(W * H, 1e-6))
    return (W * 0.5) * k, H * k


# Sezione della cornice (dal filo esterno verso il campo del mosaico):
# (arretramento esterno, arretramento interno, y del fronte, profondità, materiale)
# Sezione della cornice della cuspide (dal filo esterno verso il campo del
# mosaico): frazioni dello spessore totale O_CUSPIDE_LAT, y del fronte,
# profondità e materiale.  Lo spessore è calibrato sulla fotografia: il
# triangolo dorato occupa circa l'80% della larghezza esterna.
O_CUSPIDE_LAT = 0.345
PROFILO_CUSPIDE_LAT = (
    (0.000, 0.038, -1.415, 0.60, CUSPIDE_BIANCO),    # filo esterno sottile e luminoso
    (0.038, 0.058, -1.368, 0.18, PATINA_ROS),        # gola d'ombra (v3.0)
    (0.058, 0.104, -1.398, 0.34, CUSPIDE_BIANCO),    # listello sotto i gattoni
    (0.104, 0.128, -1.362, 0.16, PATINA_ROS),        # canalino d'ombra
    (0.128, 0.188, -1.445, 0.62, CUSPIDE_BIANCO),    # toro esterno aggettante
    (0.188, 0.208, -1.358, 0.16, PATINA_ROS),        # gola stretta d'ombra
    (0.208, 0.282, -1.412, 0.58, CUSPIDE_PIETRA),    # banda a ovoli e dardi
    (0.282, 0.300, -1.366, 0.16, PATINA_ROS),        # filetto d'ombra
    (0.300, 0.332, -1.440, 0.60, CUSPIDE_BIANCO),    # toro interno perlinato
    (0.332, 0.345, -1.392, 0.56, CUSPIDE_BIANCO),    # battuta sul campo aureo
)
O_CUSPIDE_LAT = PROFILO_CUSPIDE_LAT[-1][1]
O_DENT_CUSP_LAT = 0.158       # asse dei dentelli (sul toro esterno)
O_PERLE_CUSP_LAT = 0.316      # asse delle perline (accanto al campo aureo)
O_FOGLIE_CUSP_LAT = 0.245     # asse della banda a ovoli e dardi


def _bm_gattone_cuspide(bm, base, u_dir, out_dir, size=0.12, piega=0.42):
    """Gattone (crocket) a giglio senese (v3.0), come quelli della foto.

    Nella fotografia i gattoni dei due frontoni non sono foglioline: sono
    grandi fiori di giglio scolpiti, con petalo centrale alto e appuntito,
    due petali laterali arcuati che ricadono in fuori, sepali bassi e un
    bottone nodoso alla base.  `size` e' la larghezza complessiva del
    fiore; il petalo centrale e' lungo circa 1,5 volte `size`.
    """
    # Direzione del fiore: soprattutto in fuori dallo spiovente, inclinata
    # verso la punta del frontone.
    up = (out_dir * 0.80 + u_dir * 0.60).normalized()
    phi = math.atan2(up.x, up.z)
    profilo = ((0.00, 0.30), (0.15, 0.52), (0.30, 0.40), (0.46, 0.54),
               (0.62, 0.42), (0.78, 0.34), (0.91, 0.20), (1.00, 0.07))
    # Bottone nodoso alla base e corto gambo che lo stacca dalla cornice.
    _bm_sfera(bm, Matrix.Translation(base), 0.0, 0.0, 0.0, size * 0.20,
              sx=1.10, sy=0.80, sz=1.10, u=9, v=6)
    base_f = base + up * size * 0.10
    # Petalo centrale eretto, il piu' alto del giglio.
    M = Matrix.Translation(base_f) @ Matrix.Rotation(phi, 4, "Y")
    _bm_foglia(bm, size * 1.12, size * 0.74, size * 0.44, M,
               profilo=profilo, piega=piega * 0.30, gonfia=1.45)
    for lato in (-1, 1):
        # Petali laterali arcuati che si aprono e ricadono in fuori.
        M3 = (Matrix.Translation(base_f + up * size * 0.08)
              @ Matrix.Rotation(phi + lato * 0.92, 4, "Y"))
        _bm_foglia(bm, size * 0.78, size * 0.50, size * 0.34, M3,
                   profilo=profilo, piega=piega * 0.45, gonfia=1.38)
        # Sepali bassi ricadenti contro la cornice.
        M4 = (Matrix.Translation(base_f - up * size * 0.02)
              @ Matrix.Rotation(phi + lato * 2.05, 4, "Y"))
        _bm_foglia(bm, size * 0.45, size * 0.28, size * 0.20, M4,
                   profilo=profilo, piega=-piega * 0.30 * lato, gonfia=1.22)
    # Ricciolo dietro il petalo centrale: chiude il volume del fiore.
    M2 = (Matrix.Translation(base_f + up * size * 0.05)
          @ Matrix.Rotation(phi + 0.34, 4, "Y"))
    _bm_foglia(bm, size * 0.62, size * 0.32, size * 0.24, M2,
               profilo=profilo, piega=piega * 1.05, gonfia=1.32)


def cuspide_laterale_mosaico_v30(tag, cx, side, z_base, w, h, mos_mat):
    """Frontone laterale del mosaico, riletto sul dettaglio fotografico frontale.

    Il campo musivo occupa circa l'80% della larghezza esterna, le
    modanature hanno gole d'ombra vere fra un filo e l'altro, i gattoni
    sono otto gigli senesi per falda e la statua apicale poggia su una
    lastra bassa con capitello di foglie, come nella fotografia.
    """
    y_wall = -1.02
    y_mos = -1.325

    # Corpo e fondo arretrati: nessuna fessura aperta dietro il mosaico.
    prism(f"Cuspide_Lat_Corpo_{tag}", R, cx, y_wall + 0.22, z_base, w, h, 0.44, CUSPIDE_BIANCO)
    half_in, h_in = _apertura_cuspide(w, h, O_CUSPIDE_LAT)
    prism(f"Cuspide_Lat_Fondo_{tag}", R, cx, y_wall + 0.10, z_base,
          2.0 * half_in + 0.08, h_in + 0.04, 0.22, ROSA_C)

    # Campo musivo arretrato di 15-20 cm rispetto ai fili sporgenti.  La
    # battuta e' pietra, non una sagoma nera che ingigantisce il contorno.
    alzata = 0.065
    fr = 1.0 - alzata / max(h_in, 1e-4)
    prism(f"Battuta_Mosaico_CuspLat_{tag}", D, cx, -1.150, z_base,
          2.0 * half_in + 0.020, h_in + 0.012, 0.08, CUSPIDE_PIETRA)
    prism(f"Mosaico_Laterale_Reale_{tag}", S, cx, y_mos + 0.055,
          z_base + alzata, 2.0 * half_in * fr, h_in - alzata,
          0.11, mos_mat, mosaic_uv=True)
    box(f"Soglia_Mosaico_CuspLat_{tag}", D, cx, -1.305, z_base + 0.027,
        2.0 * half_in * fr + 0.10, 0.22, 0.054, CUSPIDE_BIANCO)

    # Le lavorazioni degli spioventi nascono sull'asse locale x=0 e vengono
    # traslate insieme sul centro della cuspide.
    _prima = set(bpy.data.objects)
    _, L_slope = _angolo_spiovente(w, h)
    for s in (-1, 1):
        for k_f, (o0, o1, y_f, dep, mat_f) in enumerate(PROFILO_CUSPIDE_LAT):
            banda_mitrata(
                f"Fascia_CuspideLat_{tag}_{s}_{k_f}", D, s, w, h,
                o0, o1, y_f, dep, mat_f, z_base=z_base,
            )

        # Dentelli minuti e ravvicinati, con luce fra un dente e il successivo.
        tilt = -s * math.atan2(w * 0.5, h)
        bm_d = bmesh.new()
        n_d = max(24, int(L_slope / 0.078))
        for i in range(n_d):
            u = 0.012 + 0.976 * i / (n_d - 1)
            px, pz = punto_fascia(s, w, h, O_DENT_CUSP_LAT, u, z_base)
            _bm_box(bm_d, Matrix.Identity(4), px, -1.415, pz,
                    0.052, 0.100, 0.048, rot=Matrix.Rotation(tilt, 4, "Y"))
        _mesh_da_bmesh(f"Dentelli_CuspideLat_{tag}_{s}", D, bm_d, CUSPIDE_BIANCO)

        # Perlinatura lapidea (non dorata) sul filo interno: perle piu'
        # grandi e fitte della v2.9, si leggono anche da lontano.
        n_p = max(24, int(L_slope / 0.082))
        punti = []
        for i in range(n_p):
            u = 0.014 + 0.972 * i / (n_p - 1)
            px, pz = punto_fascia(s, w, h, O_PERLE_CUSP_LAT, u, z_base)
            punti.append((px, -1.472, pz))
        fila_perle(f"Perle_CuspideLat_{tag}_{s}", D, punti, 0.0175, CUSPIDE_BIANCO)

        # Banda a ovoli e dardi (v3.0): e' l'ornato scolpito continuo che
        # nella foto corre lungo tutto lo spiovente fra toro e perlinatura.
        # Ovoli a guscio allungati lungo la falda, dardi appuntiti fra l'uno
        # e l'altro, gusci d'ombra patinati dietro gli ovoli.
        bm_f = bmesh.new()
        bm_dart = bmesh.new()
        bm_ombra = bmesh.new()
        n_f = max(22, int(L_slope / 0.115))
        d_slope = Vector((-s * w * 0.5, 0.0, h)).normalized()
        q_slope = d_slope.to_track_quat("Z", "Y").to_matrix().to_4x4()
        for i in range(n_f):
            u = 0.018 + 0.964 * i / (n_f - 1)
            px, pz = punto_fascia(s, w, h, O_FOGLIE_CUSP_LAT, u, z_base)
            Mo = Matrix.Translation((px, -1.452, pz)) @ q_slope
            _bm_sfera(bm_f, Mo, 0.0, 0.0, 0.0, 0.030,
                      sx=0.78, sy=0.62, sz=1.42, u=9, v=7)
            _bm_sfera(bm_ombra, Matrix.Translation((px, -1.428, pz)) @ q_slope,
                      0.0, 0.0, 0.0, 0.036, sx=0.95, sy=0.40, sz=1.55, u=8, v=6)
            if i < n_f - 1:
                u2 = u + 0.482 / (n_f - 1)
                xd, zd = punto_fascia(s, w, h, O_FOGLIE_CUSP_LAT, u2, z_base)
                Md = Matrix.Translation((xd, -1.455, zd)) @ q_slope
                _bm_cono(bm_dart, Md, 0.0, 0.0, -0.030, 0.016, 0.002, 0.062, seg=7)
                _bm_sfera(bm_dart, Md, 0.0, 0.0, 0.040, 0.013,
                          sx=0.80, sy=0.70, sz=1.10, u=7, v=5)
        _mesh_da_bmesh(f"Ovoli_Battuta_CuspLat_{tag}_{s}", D, bm_f, CUSPIDE_BIANCO)
        _mesh_da_bmesh(f"Dardi_Battuta_CuspLat_{tag}_{s}", D, bm_dart, CUSPIDE_PIETRA)
        _mesh_da_bmesh(f"Gusci_Ovoli_CuspLat_{tag}_{s}", D, bm_ombra, CUSPIDE_PIETRA)

        # Otto gattoni a giglio per falda (v3.0), grandi come in fotografia:
        # il petalo centrale misura circa 0,45 m e la silhouette a fiore si
        # deve leggere gia' nell'inquadratura panoramica.
        bm_g = bmesh.new()
        n_g = 8
        u_g = Vector((-s * w * 0.5, 0.0, h)).normalized()
        out_g = Vector((u_g.z, 0.0, -u_g.x))
        if out_g.x * s < 0.0:
            out_g = -out_g
        out_g.normalize()
        for i in range(n_g):
            u = 0.045 + 0.875 * i / (n_g - 1)
            bx, bz = punto_fascia(s, w, h, 0.006, u, z_base)
            _bm_gattone_cuspide(
                bm_g, Vector((bx, -1.450, bz)), u_g, out_g,
                size=0.270 - 0.022 * u, piega=0.50,
            )
        _mesh_da_bmesh(f"Gattoni_CuspideLat_{tag}_{s}", D, bm_g, CUSPIDE_BIANCO)

    for _o in set(bpy.data.objects) - _prima:
        _o.location.x += cx

    # Muratura di raccordo sotto il frontone; le vecchie quattro ghimberghe
    # duplicate sono eliminate: sotto la base resta la loggia reale.
    # v3.0: niente piu' grande pannello rosa piatto (in foto sotto la base
    # corre la fascia scura di serpentino e poi la muratura chiara rigata).
    box(f"Fondo_Sotto_CuspLat_{tag}", R, cx, -1.02,
        z_base - 1.16, w + 0.16, 0.30, 1.90, CUSPIDE_BIANCO)
    box(f"Fondo_Sotto_CuspLat_B_{tag}", R, cx, -1.06,
        z_base - 0.86, w - 0.04, 0.24, 0.30, ROSA_C)
    box(f"Fascia_Serpentino_SottoCusp_{tag}", D, cx, -1.24,
        z_base - 0.475, w + 0.20, 0.30, 0.150, VERDE)

    # Base d'imposta: ovoli/foglie, perline e dentelli fra sottili fili di
    # cornice.  Tutti gli elementi sono allacciati alla soglia del mosaico.
    box(f"Cornice_Base_CuspLat_{tag}_C", D, cx, -1.08, z_base - 0.360,
        w + 0.14, 0.46, 0.070, CUSPIDE_BIANCO)
    box(f"Ombra_Base_CuspLat_{tag}", D, cx, -1.270, z_base - 0.310,
        w + 0.18, 0.08, 0.038, CUSPIDE_PIETRA)
    box(f"Cornice_Base_CuspLat_{tag}_B", D, cx, -1.18, z_base - 0.222,
        w + 0.26, 0.52, 0.066, CUSPIDE_BIANCO)
    box(f"Cornice_Base_CuspLat_{tag}_A", D, cx, -1.20, z_base - 0.074,
        w + 0.30, 0.54, 0.078, CUSPIDE_BIANCO)
    box(f"Zoccolo_Base_CuspLat_{tag}", D, cx, -1.10, z_base - 0.010,
        w + 0.10, 0.42, 0.048, CUSPIDE_BIANCO)

    bm_bd = bmesh.new()
    n_bd = max(30, int((w + 0.20) / 0.078))
    for i in range(n_bd):
        xb = cx - (w + 0.20) * 0.5 + (i + 0.5) * ((w + 0.20) / n_bd)
        _bm_box(bm_bd, Matrix.Identity(4), xb, -1.360, z_base - 0.270,
                0.043, 0.100, 0.052)
    _mesh_da_bmesh(f"Dentelli_Base_CuspLat_{tag}", D, bm_bd, CUSPIDE_BIANCO)

    n_bp = max(32, int((w + 0.22) / 0.072))
    punti_b = [(cx - (w + 0.22) * 0.5 + (i + 0.5) * ((w + 0.22) / n_bp),
                -1.474, z_base - 0.222) for i in range(n_bp)]
    fila_perle(f"Perle_Base_CuspLat_{tag}", D, punti_b, 0.014, CUSPIDE_BIANCO)

    # Fregio di base a ovoli e dardi a tutto tondo (v3.0): nella foto e'
    # l'elemento piu' leggibile della trabeazione sotto il mosaico.
    bm_base_f = bmesh.new()
    bm_base_d = bmesh.new()
    n_bf = max(24, int((w + 0.12) / 0.115))
    for i in range(n_bf):
        xf = cx - (w + 0.12) * 0.5 + (i + 0.5) * ((w + 0.12) / n_bf)
        _bm_sfera(bm_base_f, Matrix.Identity(4), xf, -1.462, z_base - 0.178,
                  0.031, sx=0.80, sy=0.60, sz=1.30, u=9, v=7)
        if i < n_bf - 1:
            xd = xf + ((w + 0.12) / n_bf) * 0.5
            _bm_cono(bm_base_d, Matrix.Identity(4), xd, -1.458, z_base - 0.208,
                     0.015, 0.002, 0.058, rot=Matrix.Rotation(math.pi, 4, "X"), seg=7)
    _mesh_da_bmesh(f"Ovoli_Base_CuspLat_{tag}", D, bm_base_f, CUSPIDE_BIANCO)
    _mesh_da_bmesh(f"Dardi_Base_CuspLat_{tag}", D, bm_base_d, CUSPIDE_PIETRA)

    # Apice (v3.0): niente piu' dado a torretta con specchiatura rosa.
    # Nella foto la statua poggia i piedi su una lastra bassa, sotto la
    # quale un capitello di foglie d'acanto abbraccia la punta del
    # frontone: tutto il sostegno misura circa un quinto della statua.
    z_ap = z_base + h
    y_dado = -1.205
    bm_ap = bmesh.new()
    bm_ap_pat = bmesh.new()
    for s in (-1, 1):
        for j in range(3):
            M = (Matrix.Translation((cx + s * (0.020 + j * 0.048),
                                     y_dado - 0.200, z_ap - 0.010 + j * 0.026))
                 @ Matrix.Rotation(s * (0.22 + j * 0.24), 4, "Y"))
            _bm_foglia(bm_ap, 0.205 - j * 0.024, 0.082 - j * 0.007,
                       0.044, M, gonfia=1.42)
        _bm_gattone_cuspide(
            bm_ap, Vector((cx + s * 0.080, y_dado - 0.180, z_ap - 0.005)),
            Vector((0.0, 0.0, 1.0)), Vector((float(s), 0.0, 0.10)).normalized(),
            size=0.145, piega=0.54,
        )
        _bm_sfera(bm_ap_pat, Matrix.Identity(4), cx + s * 0.105,
                  y_dado - 0.205, z_ap + 0.055, 0.026,
                  sx=1.0, sy=0.45, sz=1.0, u=9, v=6)
    _bm_sfera(bm_ap, Matrix.Identity(4), cx, y_dado - 0.198, z_ap + 0.120,
              0.050, sx=0.90, sy=0.82, sz=1.20, u=10, v=7)
    _mesh_da_bmesh(f"Capitello_Foglie_Apice_Cusp_{tag}", G, bm_ap, CUSPIDE_BIANCO)
    _mesh_da_bmesh(f"Occhi_Capitello_Apice_Cusp_{tag}", G, bm_ap_pat, PATINA)

    # Lastra d'appoggio bassa e cimasa appena modanata.
    box(f"Lastra_Apice_Cusp_{tag}", G, cx, y_dado, z_ap + 0.148,
        0.40, 0.34, 0.055, CUSPIDE_BIANCO)
    box(f"Cimasa_Apice_Cusp_{tag}", G, cx, y_dado, z_ap + 0.196,
        0.44, 0.37, 0.042, CUSPIDE_BIANCO)

    # Statue apicali piu' alte e snelle (1,52 m): due figure femminili
    # velate dal lungo panneggio verticale, mano al petto a sinistra e
    # mano alzata in gesto di parola a destra, come nella fotografia.
    statua_gotica_v26(
        f"Statua_Cuspide_{tag}", ST, cx, y_dado, z_ap + 0.218, 1.520,
        spec={"gesto": "petto" if side < 0 else "parla", "scala_plinto": 0.62,
              "barba": 0.0, "copricapo": "velo",
              "yaw": -0.08 * side, "nod": 0.030, "seed": 4 if side < 0 else 9},
    )


# =============================================================================
# 7. SETTORI LATERALI INTERNI (loggetta gotica sotto i frontoni dei mosaici)
# -----------------------------------------------------------------------------
# v3.7 — La loggetta della v3.6 era una fila di cinque arcatelle minuscole
# (0,78 m di luce) tutte appiattite sul filo della facciata, con una parete
# chiara dietro e quattro statuine piccole: davanti alla fotografia leggeva
# come un pannello a rilievo, non come un loggiato.  Nell'originale il
# loggiato e' un *vano profondo e buio* con colonnine binate sottili, quattro
# arcate alte (1,15 m di luce, 1,1 m di freccia) e statue a figura intera
# messe in controluce davanti al fondo nero.  Qui il vano viene scavato
# davvero (1,1 m di profondita', fondo quasi nero, spallette e soffitto),
# il parapetto e' una balaustra con cornice e filo d'ombra, le arcate hanno
# doppia ghiera e gattoni, e sopra ogni colonna torna la ghimberga con
# fiorone come in fotografia.
# =============================================================================
for side in (-1, 1):
    tag = "Sx" if side < 0 else "Dx"
    mos_mat = MOS_SX if side < 0 else MOS_DX
    cx_log = side * 7.70                 # asse del loggiato: in fotografia e'
                                        # spostato verso l'interno rispetto al
                                        # frontone del mosaico
    w_log = 4.45
    y_front = -1.46                      # filo delle colonnine
    y_fondo = -0.31                      # fondo del vano (1,15 m di profondita')
    z_par0, z_par1 = 15.55, 16.02        # parapetto
    z_imp = 17.32                        # imposta delle arcate
    z_sof = 19.02                        # soffitto del vano

    # --- vano scavato: parete di fondo CHIARA (i pennacchi fra gli archi
    # sono in luce nella fotografia) e, per ogni campata, un'apertura ad
    # arco in ombra: cosi' i vani bui hanno la forma dell'arco e non un
    # rettangolo nero dietro le colonnine
    box(f"Loggia_Fondo_{tag}", R, cx_log, y_fondo, (z_par1 + z_sof) * 0.5,
        w_log - 0.16, 0.10, z_sof - z_par1, NICCHIA)
    box(f"Loggia_Soffitto_{tag}", R, cx_log, (y_front + y_fondo) * 0.5, z_sof,
        w_log - 0.10, abs(y_fondo - y_front), 0.12, PATINA)
    for s_j in (-1, 1):
        box(f"Loggia_Spalletta_{tag}_{s_j}", R,
            cx_log + s_j * (w_log * 0.5 - 0.05), (y_front + y_fondo) * 0.5,
            (z_par1 + z_sof) * 0.5, 0.10, abs(y_fondo - y_front),
            z_sof - z_par1, NICCHIA)
    # pedana in ombra dietro il parapetto
    box(f"Loggia_Pedana_{tag}", R, cx_log, y_fondo + 0.45, z_par1 - 0.02,
        w_log - 0.14, 0.90, 0.10, NICCHIA)

    # --- balaustra: parapetto, cornice a due fili e filo d'ombra
    box(f"Loggia_Parapetto_{tag}", R, cx_log, y_front + 0.16, (z_par0 + z_par1) * 0.5,
        w_log + 0.10, 0.36, z_par1 - z_par0, BIANCO2)
    box(f"Loggia_Para_Cornice_{tag}", R, cx_log, y_front + 0.02, z_par1 + 0.05,
        w_log + 0.22, 0.46, 0.12, BIANCO)
    box(f"Loggia_Para_Ombra_{tag}", D, cx_log, y_front - 0.18, z_par1 - 0.03,
        w_log + 0.20, 0.05, 0.055, VERDE)
    for k_b in range(23):
        box(f"Loggia_Balaustrino_{tag}_{k_b}", R,
            cx_log - w_log * 0.5 + 0.12 + k_b * (w_log - 0.24) / 22.0,
            y_front + 0.01, z_par0 + 0.20, 0.075, 0.10, 0.32, BIANCO)

    # --- cinque piedritti a colonnine binate + quattro arcate acute
    n_archi = 4
    step_l = w_log / n_archi
    for i in range(n_archi + 1):
        col_x = cx_log - w_log * 0.5 + i * step_l
        box(f"Loggia_Piedritto_{tag}_{i}", R, col_x, y_front + 0.10, z_par1 + 0.13,
            0.24, 0.30, 0.26, BIANCO2)
        for s_c in (-1, 1):
            cyl(f"Loggia_Col_{tag}_{i}_{s_c}", R, col_x + s_c * 0.062,
                y_front - 0.02 - 0.06 * (s_c > 0), 16.60, 0.048, 1.32, BIANCO, vertices=10)
            cyl(f"Loggia_BaseCol_{tag}_{i}_{s_c}", R, col_x + s_c * 0.062,
                y_front - 0.02 - 0.06 * (s_c > 0), 16.26, 0.070, 0.10, BIANCO2, vertices=10)
        box(f"Loggia_Capitello_{tag}_{i}", R, col_x, y_front - 0.02, z_imp - 0.07,
            0.26, 0.22, 0.14, PIETRA)
        for k_f in range(3):
            sphere(f"Loggia_CapFoglia_{tag}_{i}_{k_f}", R,
                   col_x + (k_f - 1) * 0.070, y_front - 0.14, z_imp - 0.08,
                   0.038, PIETRA, sy=0.8)
        # mensola e ghimberga con gattoni sopra la colonna
        spioventi_modanati(f"Loggia_Ghimb_{tag}_{i}", R, col_x, -1.56, z_sof - 0.02,
                           0.72, 0.58, 0.075, 0.18, BIANCO)
        foglie_rampanti(f"Loggia_GhimbFoglie_{tag}_{i}", G, col_x, -1.60,
                        z_sof + 0.02, 0.72, 0.58, PIETRA, n=3, size=0.10)
        finial(f"Loggia_Fiorone_{tag}_{i}", G, col_x, -1.58, z_sof + 0.60, 0.34)

    for i in range(n_archi):
        ax = cx_log - w_log * 0.5 + (i + 0.5) * step_l
        # apertura in ombra della campata (parete piena sopra l'arco)
        box(f"Loggia_Buio_{tag}_{i}", R, ax, y_fondo + 0.09, (z_par1 + z_imp) * 0.5 - 0.30,
            step_l - 0.30, 0.06, z_imp - z_par1 + 0.60, SCURO)
        prism(f"Loggia_BuioTesta_{tag}_{i}", R, ax, y_fondo + 0.09, z_imp + 0.28,
              step_l - 0.30, step_l * 0.5 * 0.90, 0.06, SCURO)
        arch(f"Loggia_Arco_{tag}_{i}", R, ax, y_front - 0.06, z_imp,
             step_l * 0.5, 0.055, BIANCO, seg_u=26, pointed=0.92)
        arch(f"Loggia_ArcoFilo_{tag}_{i}", R, ax, y_front - 0.02, z_imp + 0.02,
             step_l * 0.5 + 0.075, 0.030, ROSA_C, seg_u=26, pointed=0.92)
        arch(f"Loggia_ArcoEst_{tag}_{i}", R, ax, y_front + 0.03, z_imp + 0.04,
             step_l * 0.5 + 0.125, 0.036, BIANCO2, seg_u=26, pointed=0.92)
        finial(f"Loggia_ArcoFiore_{tag}_{i}", G, ax, y_front - 0.04,
               z_imp + step_l * 0.5 * 1.92 + 0.02, 0.14)
    # fascia piena fra gli archi e il soffitto, con quatrefogli intagliati
    box(f"Loggia_Fregio_{tag}", R, cx_log, -1.30, z_sof - 0.22, w_log, 0.24, 0.30, BIANCO2)
    for k_q in range(9):
        rosetta_rilievo(f"Loggia_Quatrifoglio_{tag}_{k_q}", R,
                        cx_log - w_log * 0.5 + 0.28 + k_q * (w_log - 0.56) / 8.0,
                        -1.44, z_sof - 0.22, 0.062, petals=4)

    # --- statue a figura intera in controluce davanti al fondo nero
    for k_s in range(n_archi):
        sx_s = cx_log - w_log * 0.5 + (k_s + 0.5) * step_l
        box(f"Loggia_Piedistallo_{tag}_{k_s}", R, sx_s, -1.08, 16.12,
            0.36, 0.28, 0.24, BIANCO2)
        statua_gotica_v26(
            f"Statua_Loggia_{tag}_{k_s}", ST, sx_s, -1.10, 16.24, 1.56,
            spec=dict(gesto=("libro", "parla", "rotolo", "petto")[k_s],
                      barba=(0.55, 0.80, 0.35, 0.65)[k_s],
                      copricapo=("capelli", "capelli_lunghi", "berretta", "cappuccio")[k_s],
                      yaw=-side * (0.16 + 0.06 * k_s), nod=0.06,
                      seed=71 + k_s * 5 + (0 if side < 0 else 2), lato=-side),
            material=PIETRA,
        )

    # Trabeazione e cuspide laterale: H/W = 0,93 come nel dettaglio
    # frontale; la v3.0 rifa' gattoni, cornice, mosaici, base e apice.
    # la cuspide del mosaico resta sull'asse dei settori laterali (x = X_LAT):
    # e' la parte che nella v3.6 era gia' fedele e non va spostata
    cx_mos = side * X_LAT
    w_mos = DIM.get("larghezza_cuspidi_mosaico", 4.02)
    box(f"Trabeazione_Cuspide_{tag}", R, cx_mos, -1.02, Z_CUSP_LAT, w_mos + 0.35, 0.62, 0.38, BIANCO2)
    box(f"Trabeazione_Cuspide_Toro_{tag}", D, cx_mos, -1.36, Z_CUSP_LAT + 0.16,
        w_mos + 0.45, 0.14, 0.055, BIANCO)
    cuspide_laterale_mosaico_v30(
        tag, cx_mos, side,
        z_base=Z_CUSP_LAT + 0.30,
        w=w_mos,
        h=DIM.get("altezza_cuspidi_mosaico", 3.53),
        mos_mat=mos_mat,
    )


# =============================================================================
# 8. TORRIONI GOTICI ANGOLARI ESTERNI — rifatti sulla fotografia (v3.7)
# -----------------------------------------------------------------------------
# Nella v3.6 il torrione era un parallelepipedo di 4,65 x 2,65 m con una
# finestrella nera da 0,68 m, lesene piatte, una nicchia rosa con una
# statuina e, in cima, un cilindro ottagonale con un cono e quattro coni
# lisci: davanti alla fotografia leggeva come un *campanile da presepe*
# appiccicato al fianco della facciata.  Nell'originale il torrione e' una
# massa gotica piena, alta quasi come la galleria:
#
#   1. corpo unico a tre registri, con fascia bicroma di base, cornici a
#      dentelli e lesene d'angolo: non una parete liscia;
#   2. quattro LANCETTE GOTICHE alte e incassate (due per registro), con
#      vano in ombra, colonnine binate, doppia ghiera acuta e ghimberga
#      crochettata — non finestrelle piatte;
#   3. tabernacoli con statue a figura intera sotto baldacchino sui due
#      contrafforti d'angolo, piu' una Madonna su mensola aggettante;
#   4. coronamento a grappolo: grande ghimberga frontale crochettata,
#      due pinnacoli d'angolo a sezione ottagonale interamente fogliati e
#      una torretta ottagonale con monofora e statua (via i coni lisci e
#      il cilindro a "pedina");
#   5. doccioni sottili e inclinati sugli spigoli, come i draghi della foto.
# =============================================================================

def _ghiera_bicroma(name, col, cx, y, cz, r, n=11, pointed=0.60, depth=0.10,
                    thick=0.16, mat_a=None, mat_b=None):
    """Ghiera ad archivolto bicromo senese (v3.9): cunei alternati di marmo
    bianco e serpentino disposti lungo l'arco acuto, come la ghiera che nella
    fotografia orla OGNI apertura dei torrioni angolari (lancette, monofore,
    arco della corona).  Prima le ghiere del torrione erano bianche lisce (o
    rosa piatte): il tratto piu' riconoscibile delle torri vere mancava del
    tutto e le aperture leggevano come buchi neri bordati di bianco.
    """
    mat_a = mat_a or BIANCO
    mat_b = mat_b or VERDE
    for k in range(n):
        t = (k + 0.5) / n
        a = math.pi * (1.0 - t)
        px = r * math.cos(a)
        pz = r * math.sin(a) + pointed * r * (1.0 - abs(2.0 * t - 1.0)) ** 0.85
        phi = math.atan2(pz, px)
        box(f"{name}_V{k}", col, cx + px, y, cz + pz,
            thick, depth, (math.pi * r / n) * 1.30,
            mat_a if k % 2 == 0 else mat_b,
            rot_y=-phi)


def _lancetta_gotica(name, col, cx, y_face, z0, w, h, gable_h=0.85,
                     gable=True, scura=True, traforo=False, bicroma=False,
                     montante_ritorto=False):
    """Lancetta gotica senese incassata: vano in ombra, spallette, ghiere,
    colonnine binate e ghimberga crochettata.

    v3.8 (miglioria 1): con `traforo=True` il vano non e' piu' un rettangolo
    nero con due colonnine — riceve il traforo senese vero: un oculo a
    quatrifoglio nella testata, il montante centrale che sale dal davanzale
    e due archetti interni che si appoggiano alle spallette.  Era questo che
    mancava perche' le finestre del torrione leggessero come "buchi" neri.
    """
    h_testa = w * 0.80
    z_imp = z0 + h - h_testa
    box(f"{name}_Vano", col, cx, y_face + 0.24, z0 + (h - h_testa) * 0.5,
        w, 0.06, h - h_testa, SCURO if scura else NICCHIA)
    prism(f"{name}_VanoTesta", col, cx, y_face + 0.24, z_imp, w, h_testa, 0.06,
          SCURO if scura else NICCHIA)
    for s_v in (-1, 1):
        box(f"{name}_Spalletta_{s_v}", col, cx + s_v * w * 0.5, y_face + 0.12,
            z0 + (h - h_testa) * 0.5, 0.055, 0.26, h - h_testa, NICCHIA)
    for s_c in (-1, 1):
        cyl(f"{name}_Col_{s_c}", col, cx + s_c * (w * 0.30), y_face + 0.18,
            z0 + (h - h_testa) * 0.5, 0.038, h - h_testa, BIANCO2, vertices=10)
        box(f"{name}_Cap_{s_c}", col, cx + s_c * (w * 0.30), y_face + 0.16,
            z_imp - 0.07, 0.11, 0.13, 0.09, PIETRA)
    arch(f"{name}_Ghiera", col, cx, y_face + 0.03, z_imp, w * 0.5, 0.070,
         BIANCO, seg_u=24, pointed=0.60)
    if bicroma:
        # v3.9: archivolto a cunei bianco/serpentine al posto del filetto
        # rosa piatto: e' la rigatura bicroma che orla le finestre vere.
        _ghiera_bicroma(f"{name}_GhieraBicroma", col, cx, y_face - 0.015,
                        z_imp, w * 0.5 + 0.10, n=9, pointed=0.60,
                        depth=0.09, thick=0.15)
    else:
        arch(f"{name}_GhieraRosa", col, cx, y_face - 0.01, z_imp + 0.015,
             w * 0.5 + 0.078, 0.022, ROSA_C, seg_u=24, pointed=0.60)
    arch(f"{name}_GhieraEst", col, cx, y_face + 0.07, z_imp + 0.010,
         w * 0.5 + 0.135, 0.034, BIANCO2, seg_u=24, pointed=0.60)
    if traforo:
        # montante centrale che sale dal davanzale all'imposta
        if montante_ritorto:
            # v3.9: nelle lancette alte il montante e' una colonnina TORTILE,
            # come il fusto elicoidale che divide le finestre del torrione
            # nella fotografia (il montante dritto leggeva come una stecca).
            colonna_ritorta(f"{name}_Montante", col, cx, y_face + 0.20,
                            z0 + (h - h_testa) * 0.5, w * 0.075, h - h_testa,
                            BIANCO2, turns=2.4, ridges=3, ridge_amp=0.24)
        else:
            box(f"{name}_Montante", col, cx, y_face + 0.20, z0 + (h - h_testa) * 0.5,
                w * 0.085, 0.10, h - h_testa, BIANCO2)
        box(f"{name}_MontanteBase", col, cx, y_face + 0.19, z0 + 0.10,
            w * 0.16, 0.12, 0.20, PIETRA)
        # oculo a quatrifoglio nella testata: quattro lobi su fondo in ombra
        r_lob = w * 0.155
        torus(f"{name}_Oculo", col, cx, y_face + 0.02, z_imp + w * 0.46,
              w * 0.32, 0.030, BIANCO2)
        for k_l in range(4):
            ang_l = math.tau * k_l / 4.0 + math.pi / 4.0
            cyl(f"{name}_OculoLobo_{k_l}", col,
                cx + math.cos(ang_l) * r_lob, y_face + 0.20,
                z_imp + w * 0.46 + math.sin(ang_l) * r_lob, r_lob, 0.07,
                SCURO if scura else NICCHIA, vertices=12, rot_x=math.radians(90))
        cyl(f"{name}_OculoCuore", col, cx, y_face + 0.20, z_imp + w * 0.46,
            r_lob, 0.07, SCURO if scura else NICCHIA, vertices=14,
            rot_x=math.radians(90))
    if gable:
        z_g = z_imp + h_testa * 0.86
        spioventi_modanati(f"{name}_Ghimb", col, cx, y_face - 0.02, z_g,
                           w * 1.62, gable_h, 0.085, 0.22, BIANCO)
        for s_f in (-1, 1):
            _crocchi_falda(f"{name}_GhimbFoglie_{s_f}", col, s_f, cx,
                           y_face - 0.06, z_g + 0.03, w * 1.62, gable_h,
                           n=6, size=0.16)
        finial(f"{name}_Fiore", col, cx, y_face - 0.04, z_g + gable_h + 0.06, 0.30)


def _pinnacolo_crochettato(name, col, x, y, z0, alt, larg, n_croc=5):
    """Pinnacolo a sezione ottagonale interamente crochettato.

    v3.8 (miglioria 1): le crocchette erano coni lisci da 0,30 m infilzati
    sui sei spigoli — da lontano il pinnacolo leggeva come un cactus.  Ora
    sono foglie d'acanto ripiegate in fuori (una sola mesh per pinnacolo),
    quattro per giro e piu' piccole salendo, come nei pinnacoli senesi.
    """
    box(f"{name}_Zoccolo", col, x, y, z0 + 0.09, larg * 2.05, 0.40, 0.18, BIANCO2)
    box(f"{name}_Zoccolo2", col, x, y, z0 + 0.21, larg * 1.65, 0.34, 0.08, BIANCO)
    box(f"{name}_Nicchia", col, x, y - 0.02, z0 + 0.52, larg * 0.70, 0.16, 0.44, NICCHIA)
    cyl(f"{name}_Fusto", col, x, y, z0 + 0.26 + alt * 0.22, larg * 0.78,
        alt * 0.44, BIANCO, vertices=8)
    cyl(f"{name}_Gola", col, x, y, z0 + 0.26 + alt * 0.46, larg * 0.88, 0.10,
        PIETRA, vertices=8)
    cone(f"{name}_Guglia", col, x, y, z0 + 0.26 + alt * 0.74, larg * 0.76, 0.014,
         alt * 0.52, BIANCO, vertices=8)
    bm_cr = bmesh.new()
    for k in range(n_croc):
        t = 0.05 + k * (0.90 / max(1, n_croc - 1))
        z_k = z0 + 0.30 + alt * 0.46 + (alt * 0.50) * t
        r_k = larg * 0.76 * (1.0 - t) + 0.010
        for a_i in range(4):
            ang = math.tau * a_i / 4.0 + (math.radians(45) if k % 2 else 0.0)
            base = Vector((x + math.cos(ang) * r_k, y + math.sin(ang) * r_k * 0.92, z_k))
            # v3.8b: crocchette PIU' ADERENTI alla guglia (0,30 di sporgenza
            # invece di 0,66) e piu' piccole: cosi' il pinnacolo legge come
            # un pinnacolo fogliato e non come una pigna spinosa.
            direz = Vector((math.cos(ang) * 0.30, math.sin(ang) * 0.30, 1.0)).normalized()
            M = (Matrix.Translation(base)
                 @ direz.to_track_quat("Z", "Y").to_matrix().to_4x4())
            _bm_foglia(bm_cr, 0.26 * (1.0 - 0.40 * t), 0.075 * (1.0 - 0.35 * t),
                       0.022 * (1.0 - 0.30 * t), M, piega=0.34)
    _mesh_da_bmesh(f"{name}_Crocchette", col, bm_cr, PIETRA, uv_scale=(1.6, 1.6))
    # bocciolo terminale a goccia (il vecchio `finial` a quattro foglioline
    # letto in controluce sembrava una crocetta)
    bm_b = bmesh.new()
    _bm_lathe(bm_b, Matrix.Translation((x, y, z0 + 0.26 + alt * 0.96)),
              ((0.0, larg * 0.30), (0.05, larg * 0.34), (0.13, larg * 0.20),
               (0.22, larg * 0.02)), seg=8, sy=0.92)
    _mesh_da_bmesh(f"{name}_Bocciolo", col, bm_b, PIETRA, uv_scale=(0.6, 0.6))


# --- convergenza del coronamento: x dell'asse, y del fronte, quota d'inizio
#     (il torrione sinistro e' leggermente piu' basso di quello destro, come
#     nella fotografia)
for side, z_top_t in ((-1, 22.30), (1, 22.60)):
    tag = "Sx" if side < 0 else "Dx"
    z_imp_t = Z_IMPOSTA

    def X(v, _s=side):
        return _s * v

    xi_m, xs_m = 10.95, 14.85           # filo interno ed esterno del corpo
    w_m = xs_m - xi_m
    cx_m = (xi_m + xs_m) * 0.5
    y_f = -1.44                         # fronte del corpo

    # --- corpo murario unico, con il fianco esterno arretrato (prospettiva)
    box(f"Torre_Corpo_{tag}", S, X(cx_m), 0.02, (z_imp_t + z_top_t) * 0.5,
        w_m, 2.44, z_top_t - z_imp_t, BIANCO)
    box(f"Torre_Fianco_{tag}", S, X(xs_m + 0.18), 0.42, (z_imp_t + z_top_t) * 0.5,
        0.40, 1.70, z_top_t - z_imp_t - 0.6, BIANCO2)

    # --- fascia bicroma di base: corsi di serpentino sottili e distanziati
    # v3.9 (miglioria 1): i corsi galleggiavano 34 cm DAVANTI al muro (il
    # corpo termina a y = -1.20) e in vista frontale proiettavano un'ombra a
    # scaletta sotto ogni listello: il basamento della torre leggeva come una
    # persiana ondulata.  Ora sono intarsiati a filo (2 cm di risalto) e si
    # fermano sotto il registro delle monofore, come nella fotografia.
    for k_f in range(6):
        z_f = z_imp_t + 0.24 + k_f * 0.34
        box(f"Torre_Fascia_{tag}_{k_f}", D, X(cx_m), -1.19, z_f,
            w_m + 0.02, 0.06, 0.105, VERDE)
    # cornici a dentelli fra i registri, ciascuna alla propria quota
    for z_c in (13.40, 16.35, 19.85):
        box(f"Torre_Cornice_{tag}_{z_c:.2f}", G, X(cx_m), y_f - 0.07, z_c,
            w_m + 0.14, 0.20, 0.14, BIANCO2)
        n_d = int(w_m / 0.19)
        for d_i in range(n_d):
            box(f"Torre_Dentello_{tag}_{z_c:.0f}_{d_i}", D,
                X(xi_m + 0.10 + d_i * 0.19), y_f - 0.17, z_c - 0.10,
                0.080, 0.10, 0.070, BIANCO)
    # lesene che articolano la parete fra le campate
    for x_l in (xi_m + 0.30, cx_m, xs_m - 0.30):
        box(f"Torre_Lesena_{tag}_{x_l:.2f}", S, X(x_l), y_f - 0.06,
            (z_imp_t + z_top_t) * 0.5, 0.20, 0.14, z_top_t - z_imp_t - 0.20, BIANCO2)

    # --- contrafforti d'angolo: base a scarpa, fusto e capitello
    for x_b, w_b in ((xi_m + 0.10, 0.46), (xs_m - 0.10, 0.52)):
        box(f"Torre_Contrafforte_{tag}_{x_b:.2f}", S, X(x_b), y_f - 0.24,
            (z_imp_t + 21.9) * 0.5, w_b, 0.34, 21.9 - z_imp_t, BIANCO)
        box(f"Torre_Contrafforte_Scarpa_{tag}_{x_b:.2f}", S, X(x_b), y_f - 0.30,
            z_imp_t + 0.55, w_b + 0.14, 0.42, 1.10, BIANCO2)
        for z_k in (11.30, 15.10, 18.80):
            box(f"Torre_Contrafforte_Cap_{tag}_{x_b:.2f}_{z_k}", D, X(x_b),
                y_f - 0.30, z_k, w_b + 0.16, 0.26, 0.14, BIANCO2)

    # --- quattro lancette: due alte sul registro superiore, due basse
    # pannello in marmo rosato fra le due finestre di ogni registro: in foto
    # la specchiatura centrale del torrione e' salmone, non bianca
    for z_p0, z_p1 in ((13.62, 16.18), (16.55, 19.70)):
        box(f"Torre_Specchiatura_{tag}_{z_p0:.0f}", D, X(cx_m), y_f - 0.055,
            (z_p0 + z_p1) * 0.5, 0.56, 0.10, z_p1 - z_p0, RIGATO, fit_uv=True)
        for s_f in (-1, 1):
            box(f"Torre_Specchiatura_Filo_{tag}_{z_p0:.0f}_{s_f}", D,
                X(cx_m + s_f * 0.30), y_f - 0.062, (z_p0 + z_p1) * 0.5,
                0.045, 0.09, z_p1 - z_p0, VERDE)
    # v3.8 (miglioria 1): le quattro lancette ricevono il traforo vero
    # (montante, oculo a quatrifoglio, ghiere acute) e il vano delle due
    # alte non e' piu' nero pieno ma marmo rosato in ombra, come in foto.
    _lancetta_gotica(f"Lancetta_Alta_Sx_{tag}", S, X(cx_m - 0.92), y_f - 0.20,
                     16.58, 0.98, 2.86, gable_h=0.78, scura=True,
                     traforo=True, bicroma=True, montante_ritorto=True)
    _lancetta_gotica(f"Lancetta_Alta_Dx_{tag}", S, X(cx_m + 0.92), y_f - 0.20,
                     16.58, 0.98, 2.86, gable_h=0.78, scura=True,
                     traforo=True, bicroma=True, montante_ritorto=True)
    _lancetta_gotica(f"Lancetta_Bassa_Sx_{tag}", S, X(cx_m - 0.92), y_f - 0.20,
                     13.68, 0.98, 2.44, gable_h=0.68, scura=False,
                     traforo=True, bicroma=True)
    _lancetta_gotica(f"Lancetta_Bassa_Dx_{tag}", S, X(cx_m + 0.92), y_f - 0.20,
                     13.68, 0.98, 2.44, gable_h=0.68, scura=False,
                     traforo=True, bicroma=True)
    # registro di base: due monofore strette incassate (in foto il registro
    # basso ha aperture piu' piccole e piu' buie)
    # v3.9: alzate sopra la fascia bicroma (prima i corsi di serpentino
    # attraversavano le finestre come le stecche di una persiana) e orlate
    # dall'archivolto bicromo a cunei, come ogni apertura del torrione vero.
    for s_m in (-1, 1):
        box(f"Torre_Monofora_{tag}_{s_m}", D, X(cx_m + s_m * 0.92), y_f - 0.14,
            10.85, 0.46, 0.10, 1.50, SCURO)
        prism(f"Torre_MonoforaTesta_{tag}_{s_m}", D, X(cx_m + s_m * 0.92), y_f - 0.14,
              11.60, 0.46, 0.34, 0.10, SCURO)
        _ghiera_bicroma(f"Torre_MonoforaGhieraB_{tag}_{s_m}", D,
                        X(cx_m + s_m * 0.92), y_f - 0.16, 11.60, 0.30,
                        n=7, pointed=0.55, depth=0.08, thick=0.12)

    # --- tabernacoli con statue sui due contrafforti d'angolo
    for idx_t, (x_t, z_t) in enumerate(((xi_m + 0.10, 10.15), (xs_m - 0.10, 10.15),
                                        (xi_m + 0.10, 13.55), (xs_m - 0.10, 13.55))):
        box(f"Torre_Tabernacolo_{tag}_{idx_t}", D, X(x_t), y_f - 0.02,
            z_t + 0.86, 0.86, 0.12, 1.62, NICCHIA)
        box(f"Torre_Tab_Mensola_{tag}_{idx_t}", D, X(x_t), y_f - 0.34, z_t - 0.03,
            0.92, 0.46, 0.15, BIANCO2)
        cone(f"Torre_Tab_Tromba_{tag}_{idx_t}", D, X(x_t), y_f - 0.36, z_t - 0.24,
             0.07, 0.26, 0.28, PIETRA, vertices=8)
        for s_p in (-1, 1):
            cyl(f"Torre_Tab_Pil_{tag}_{idx_t}_{s_p}", D, X(x_t) + s_p * 0.45,
                y_f - 0.16, z_t + 0.86, 0.045, 1.72, BIANCO, vertices=8)
        statua_gotica_v26(
            f"Torre_Tab_Statua_{tag}_{idx_t}", ST, X(x_t), y_f - 0.42, z_t, 1.62,
            spec=dict(gesto=("libro", "parla", "rotolo", "petto")[idx_t],
                      barba=(0.60, 0.45, 0.78, 0.30)[idx_t],
                      copricapo=("capelli", "berretta", "capelli_lunghi", "mitra")[idx_t],
                      yaw=-side * 0.14, nod=0.05,
                      seed=101 + idx_t * 9 + (0 if side < 0 else 4), lato=side),
            material=PIETRA,
        )
        spioventi_modanati(f"Torre_Tab_Baldacchino_{tag}_{idx_t}", G, X(x_t),
                           y_f - 0.16, z_t + 1.66, 1.08, 0.72, 0.085, 0.24, BIANCO)
        foglie_rampanti(f"Torre_Tab_Foglie_{tag}_{idx_t}", G, X(x_t), y_f - 0.20,
                        z_t + 1.69, 1.08, 0.72, PIETRA, n=3, size=0.09)
        finial(f"Torre_Tab_Fiore_{tag}_{idx_t}", G, X(x_t), y_f - 0.16,
               z_t + 2.38, 0.30)

    # --- Madonna su mensola aggettante fra i due tabernacoli alti
    box(f"Torre_Madonna_Mensola_{tag}", D, X(cx_m), y_f - 0.40, 13.35,
        0.50, 0.62, 0.18, BIANCO2)
    cone(f"Torre_Madonna_Tromba_{tag}", D, X(cx_m), y_f - 0.44, 13.12,
         0.08, 0.24, 0.34, PIETRA, vertices=8)
    statua_gotica_v26(
        f"Torre_Madonna_{tag}", ST, X(cx_m), y_f - 0.52, 13.44, 1.34,
        spec=dict(gesto="petto", barba=0.0, copricapo="velo", yaw=-side * 0.10,
                  nod=0.06, seed=131 + (0 if side < 0 else 6), lato=side),
        material=PIETRA,
    )
    spioventi_modanati(f"Torre_Madonna_Cielo_{tag}", G, X(cx_m), y_f - 0.44,
                       14.92, 0.94, 0.58, 0.075, 0.20, BIANCO)
    finial(f"Torre_Madonna_Fiore_{tag}", G, X(cx_m), y_f - 0.44, 15.62, 0.28)

    # --- TERZO REGISTRO: il muro sopra le due lancette alte era un
    # rettangolo di marmo liscio; nella fotografia e' invece un registro
    # di due arcate cieche con ghimberghe, come una piccola loggia murata.
    # v3.8 (miglioria 1)
    z_reg0 = 19.98
    for idx_a, xo in enumerate((-0.92, 0.92)):
        xa = X(cx_m + xo)
        ha = 1.42
        box(f"Torre_ArcoCieco_{tag}_{idx_a}", D, xa, y_f - 0.055,
            z_reg0 + ha * 0.5, 0.86, 0.10, ha, SCURO)
        box(f"Torre_ArcoCiecoPied_{tag}_{idx_a}_{-1}", S, X(cx_m + xo) - 0.47,
            y_f - 0.10, z_reg0 + ha * 0.5, 0.13, 0.16, ha, BIANCO2)
        box(f"Torre_ArcoCiecoPied_{tag}_{idx_a}_{1}", S, X(cx_m + xo) + 0.47,
            y_f - 0.10, z_reg0 + ha * 0.5, 0.13, 0.16, ha, BIANCO2)
        arch(f"Torre_ArcoCiecoGhiera_{tag}_{idx_a}", S, xa, y_f - 0.10,
             z_reg0 + ha - 0.30, 0.40, 0.055, BIANCO, seg_u=18, pointed=0.62)
        # v3.9: anche le arcate cieche del terzo registro portano l'archivolto
        # a cunei bicromi della fotografia (prima solo ghiera bianca liscia)
        _ghiera_bicroma(f"Torre_ArcoCiecoGhieraB_{tag}_{idx_a}", S, xa,
                        y_f - 0.13, z_reg0 + ha - 0.30, 0.47, n=9,
                        pointed=0.62, depth=0.08, thick=0.13)
        spioventi_modanati(f"Torre_ArcoCiecoGhimb_{tag}_{idx_a}", S, xa,
                           y_f - 0.12, z_reg0 + ha + 0.02, 1.02, 0.34,
                           0.065, 0.14, BIANCO)
        for s_f in (-1, 1):
            _crocchi_falda(f"Torre_ArcoCiecoCroc_{tag}_{idx_a}_{s_f}", S, s_f,
                           xa, y_f - 0.15, z_reg0 + ha + 0.04, 1.02, 0.34,
                           n=4, size=0.085)
        finial(f"Torre_ArcoCiecoFiore_{tag}_{idx_a}", S, xa, y_f - 0.13,
               z_reg0 + ha + 0.40, 0.16)

    # --- CORONAMENTO ------------------------------------------------
    # cornicione a due fili che chiude il corpo
    box(f"Torre_Cornicione_{tag}", G, X(cx_m), y_f - 0.10, z_top_t,
        w_m + 0.20, 0.30, 0.12, BIANCO2)
    box(f"Torre_Cornicione2_{tag}", G, X(cx_m), y_f - 0.05, z_top_t + 0.21,
        w_m + 0.06, 0.26, 0.07, BIANCO)
    for d_i in range(int(w_m / 0.18)):
        box(f"Torre_Cornicione_Dent_{tag}_{d_i}", D, X(xi_m + 0.09 + d_i * 0.18),
            y_f - 0.20, z_top_t - 0.12, 0.075, 0.10, 0.075, BIANCO)

    # v3.8 (miglioria 1) — LA CORONA DEL TORRIONE.
    # Prima era un timpano triangolare pieno con una crocetta (un quatrifoglio
    # a quattro petali) in mezzo e, ai lati, due pinnacoli a coni lisci: da
    # lontano leggeva come il frontone di una cappella di paese, non come la
    # corona traforata del torrione senese.  Ora, come in fotografia:
    #   1. una grande bifora APERTA (due lancette + oculo a quatrifoglio)
    #      dentro un vano in ombra profondo 0,55 m, con le ghiere acute;
    #   2. la ghimberga crochettata che la inquadra, con fiorone all'apice;
    #   3. due pinnacoli fogliati sugli spigoli, piu' alti del corpo;
    #   4. la lanterna ottagonale forata, con quattro ghimberghe, la guglia
    #      e la statua sulla sommita' (il vecchio cilindro a "pedina" e'
    #      diventato un tiburio traforato e leggibile in controluce).
    z_bif0 = z_top_t + 0.30          # davanzale della bifora
    z_bif1 = z_bif0 + 1.32           # imposta degli archetti
    z_gh = z_top_t + 0.26
    gh_w, gh_h = w_m * 0.92, 2.60
    # v3.8b — il campo del ghimbergone e' MURATURA PIENA in marmo (prima non
    # c'era, e fra le due cornici spioventi si vedeva attraverso: un triangolo
    # nero al posto della testa del ghimbergone).  Sopra la muratura piena
    # si aprono, come in fotografia, la bifora e il suo oculo traforato.
    prism(f"Torre_Ghimb_Campo_{tag}", S, X(cx_m), y_f + 0.06, z_gh,
          gh_w * 0.99, gh_h * 0.995, 0.20, BIANCO2)
    # v3.9 (miglioria 1) — LA CORONA DEL TORRIONE, seconda lettura.
    # Nella v3.8 il ghimbergone era forato da due lancette rettangolari
    # scure affiancate: in vista frontale leggevano come due buchi neri (o
    # come le finestre di una casa delle bambole), mentre nella fotografia la
    # corona e' forata da UN SOLO grande arco acuto con l'archivolto a cunei
    # bicromi e il traforo a quatrifoglio nella testata.  Ora e' cosi':
    #   1. apertura unica acuta (vano in ombra, non nero pieno);
    #   2. oculo a quatrifoglio BIANCO dentro la testata scura (traforo);
    #   3. archivolto bicromo a cunei bianco/serpentine + ghiera esterna;
    #   4. davanzale modanato sotto l'apertura.
    box(f"Torre_Corona_Apertura_{tag}", D, X(cx_m), y_f - 0.06,
        z_bif0 + 0.73, 1.24, 0.06, 1.22, SCURO)
    prism(f"Torre_Corona_Testa_{tag}", D, X(cx_m), y_f - 0.06,
          z_bif0 + 1.34, 1.24, 0.74, 0.06, SCURO)
    # traforo: oculo a quatrifoglio bianco dentro la testata scura
    z_oc = z_bif0 + 1.60
    torus(f"Torre_Bifora_Oculo_{tag}", S, X(cx_m), y_f - 0.10, z_oc,
          0.40, 0.045, BIANCO)
    for k_l in range(4):
        ang_l = math.tau * k_l / 4.0 + math.pi / 4.0
        cyl(f"Torre_Bifora_Lobo_{tag}_{k_l}", D,
            X(cx_m) + math.cos(ang_l) * 0.21, y_f - 0.11,
            z_oc + math.sin(ang_l) * 0.21, 0.21, 0.05, SCURO,
            vertices=12, rot_x=math.radians(90))
    cyl(f"Torre_Bifora_LoboC_{tag}", D, X(cx_m), y_f - 0.11, z_oc,
        0.21, 0.05, SCURO, vertices=12, rot_x=math.radians(90))
    # archivolto bicromo a cunei + ghiera esterna bianca di contorno
    _ghiera_bicroma(f"Torre_Corona_GhieraB_{tag}", S, X(cx_m), y_f - 0.12,
                    z_bif0 + 1.34, 0.70, n=13, pointed=0.60, depth=0.11,
                    thick=0.20)
    arch(f"Torre_Corona_GhieraEst_{tag}", S, X(cx_m), y_f - 0.16,
         z_bif0 + 1.36, 0.90, 0.05, BIANCO2, seg_u=26, pointed=0.60)
    box(f"Torre_Corona_Davanzale_{tag}", S, X(cx_m), y_f - 0.10,
        z_bif0 + 0.06, 1.72, 0.24, 0.14, BIANCO2)
    # v3.9b: strombatura profonda attorno all'apertura della corona: le
    # spallette e l'intradosso aggettanti tengono il pannello scuro in ombra,
    # cosi' l'apertura legge come un vano profondo e non come una piastra
    # grigia appoggiata sul ghimbergone.
    for s_s in (-1, 1):
        box(f"Torre_Corona_Spalletta_{tag}_{s_s}", S,
            X(cx_m) + s_s * 0.72, y_f - 0.22, z_bif0 + 0.75,
            0.22, 0.36, 1.30, BIANCO2)
    arch(f"Torre_Corona_Soffitto_{tag}", S, X(cx_m), y_f - 0.22,
         z_bif0 + 1.36, 0.86, 0.16, BIANCO2, seg_u=24, pointed=0.60)
    # ghimberga coronaria crochettata: solo cornici, nessun campo pieno
    spioventi_modanati(f"Torre_Ghimb_{tag}", G, X(cx_m), y_f - 0.02, z_gh,
                       gh_w + 0.26, gh_h + 0.06, 0.13, 0.30, BIANCO)
    spioventi_modanati(f"Torre_Ghimb_Interno_{tag}", G, X(cx_m), y_f - 0.10,
                       z_gh + 0.16, gh_w * 0.84, gh_h * 0.86, 0.055, 0.20,
                       ROSA_C)
    for s_g in (-1, 1):
        _crocchi_falda(f"Torre_GhimbFoglie_{tag}_{s_g}", G, s_g, X(cx_m),
                       y_f - 0.08, z_gh + 0.03, gh_w + 0.26, gh_h + 0.06,
                       n=10, size=0.18)
    finial(f"Torre_GhimbFiore_{tag}", G, X(cx_m), y_f - 0.02, z_gh + gh_h + 0.16, 0.40)

    # pinnacoli fogliati sugli spigoli (piu' alti del corpo, come in foto)
    for x_p, alt_p, lar_p in ((xi_m + 0.16, 3.05, 0.30), (xs_m - 0.16, 2.85, 0.32)):
        _pinnacolo_crochettato(f"Torre_Pinnacolo_{tag}_{x_p:.2f}", G, X(x_p),
                               y_f - 0.18, z_top_t + 0.14, alt_p, lar_p)

    # lanterna ottagonale traforata con quattro ghimberghe, guglia e statua
    z_lan0 = z_top_t + 0.55
    cyl(f"Torre_Torretta_{tag}", G, X(cx_m), 0.30, z_lan0 + 0.78, 0.58, 1.56,
        BIANCO2, vertices=8)
    for a_l in range(4):
        ang = math.tau * a_l / 4.0 + math.pi / 4.0
        xm_ = X(cx_m) + math.cos(ang) * 0.45
        # v3.9: nella fotografia il tiburio ottagonale NON e' forato da
        # monofore nere: le facce portano specchiature rettangolari
        # incorniciate a rilievo (cornice bianca + campo chiaro + rosetta).
        # Le feritoie scure della v3.8 facevano leggere la lanterna come un
        # tamburo bucato; ora le facce sono pannelli modanati, e il traforo
        # resta solo nella corona sottostante.
        px_ = X(cx_m) + math.cos(ang) * 0.56
        py_ = 0.30 + math.sin(ang) * 0.56
        box(f"Torre_Torretta_CorniceP_{tag}_{a_l}", D, px_, py_,
            z_lan0 + 0.72, 0.40, 0.10, 0.74, BIANCO,
            rot_z=ang - math.pi / 2.0)
        box(f"Torre_Torretta_Pannello_{tag}_{a_l}", D, px_, py_,
            z_lan0 + 0.72, 0.26, 0.12, 0.56, BIANCO2,
            rot_z=ang - math.pi / 2.0)
        box(f"Torre_Torretta_FiloP_{tag}_{a_l}", D, px_, py_,
            z_lan0 + 0.72, 0.10, 0.14, 0.40, ROSA_C,
            rot_z=ang - math.pi / 2.0)
    cyl(f"Torre_Torretta_Cornice_{tag}", G, X(cx_m), 0.30, z_lan0 + 1.60, 0.68, 0.14,
        BIANCO, vertices=8)
    cyl(f"Torre_Torretta_Guglia_{tag}", G, X(cx_m), 0.30, z_lan0 + 2.24, 0.50, 1.16,
        BIANCO2, vertices=8)
    cone(f"Torre_Torretta_Cuspide_{tag}", G, X(cx_m), 0.30, z_lan0 + 3.10, 0.42, 0.03,
         0.72, PIETRA, vertices=8)
    bm_cr_lan = bmesh.new()
    for k_l in range(4):
        t = 0.12 + k_l * 0.21
        z_k = z_lan0 + 1.92 + 1.05 * t
        r_k = 0.46 * (1.0 - t) + 0.02
        for a_i in range(4):
            ang = math.tau * a_i / 4.0
            base_l = Vector((X(cx_m) + math.cos(ang) * r_k,
                             0.30 + math.sin(ang) * r_k, z_k))
            direz = Vector((math.cos(ang) * 0.62, math.sin(ang) * 0.62, 1.0)).normalized()
            _bm_foglia(bm_cr_lan, 0.30 * (1.0 - 0.4 * t), 0.09 * (1.0 - 0.3 * t),
                       0.024, Matrix.Translation(base_l)
                       @ direz.to_track_quat("Z", "Y").to_matrix().to_4x4(),
                       piega=0.22)
    _mesh_da_bmesh(f"Torre_Torretta_Crocchette_{tag}", G, bm_cr_lan, PIETRA,
                   uv_scale=(1.6, 1.6))
    statua_gotica_v26(
        f"Torre_Statua_Sommitale_{tag}", ST, X(cx_m), 0.30, z_lan0 + 3.34, 1.16,
        spec=dict(gesto="libro", barba=0.5, copricapo="capelli", yaw=-side * 0.10,
                  nod=0.05, seed=151 + (0 if side < 0 else 8), lato=side),
        material=PIETRA,
    )

    # --- doccioni sottili e inclinati sui due spigoli esterni
    for idx_g, (zg, gl, gr) in enumerate(((11.60, 1.15, 0.115),
                                          (16.55, 1.35, 0.130),
                                          (19.50, 1.05, 0.110))):
        gargolla(f"Gargolla_Torre_{tag}_{idx_g}", D, X(xs_m + 0.10), y_f - 0.10, zg,
                 side, gl, gr, PIETRA, pitch_deg=-26.0)


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
# 9-bis. MURI ESTERNI DEL CORPO DELLA CHIESA (v4.0)
# =============================================================================
# La facciata modellata sopra resta INTATTA.  Dietro di essa il modulo
# `muri_esterni.py` costruisce il perimetro semplice (navata, transetto, coro,
# tamburo esagonale, campanile, annessi, Duomo Nuovo incompiuto) tarato sulla
# pianta `riferimento_pianta.jpg`: 3 px = 1 m reale, asse X a x=166.5 px,
# retro facciata a y=333 px.  Le misure sono in metri reali (scala=1.0):
# la scala globale 3x della sezione 10 le ingrandisce con tutto il resto.
# Per escluderli: `CHIESA_NO_MURI=1` oppure `muri_esterni.attivi: false`.
MURI_CFG = CFG.get("muri_esterni", {})
if MURI_CFG.get("attivi", True) and not os.environ.get("CHIESA_NO_MURI"):
    try:
        if OUT_DIR not in sys.path:
            sys.path.insert(0, OUT_DIR)
        from muri_esterni import costruisci_muri_esterni
        costruisci_muri_esterni(scala=1.0, cfg=MURI_CFG)
        scene["titolo"] = "Duomo di Siena — facciata ovest e corpo della chiesa"
        scene["nota"] = ("Modello procedurale v4.0: facciata v3.9 invariata + "
                         "muri esterni semplici del corpo, proporzionati sulla "
                         "pianta allegata. CHIESA_NO_MURI=1 rigenera il solo fronte.")
    except Exception as e:
        print(f"Attenzione: muri esterni non generati ({e})")

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

_col_muri_preview = []
if os.environ.get("CHIESA_NO_RENDER"):
    print("Render anteprima saltato (CHIESA_NO_RENDER).")
else:
    # v4.0: le sei anteprime della facciata restano confronti "facciata pura":
    # i muri del corpo (raccolte 07*) vengono nascosti solo per la durata
    # dei render e ripristinati subito dopo (il .blend, gia' salvato, e
    # l'export GLB contengono invece la struttura completa).
    _col_muri_preview = [c for c in bpy.data.collections
                         if c.name.startswith("07")]
    for _c in _col_muri_preview:
        _c.hide_render = True
    try:
        # CHIESA_SOLO_GALLERIA=1 salta le prime due viste (prove rapide
        # sulla fascia dei Profeti senza rifare gli altri render).
        _solo_galleria = bool(os.environ.get("CHIESA_SOLO_GALLERIA"))
        _solo_rosone = bool(os.environ.get("CHIESA_SOLO_ROSone"))
        _solo_cuspidi = bool(os.environ.get("CHIESA_SOLO_CUSPIDI"))
        _salta_centrali = bool(os.environ.get("CHIESA_SALTA_DETTAGLI_CENTRALI"))
        _solo_torri = bool(os.environ.get("CHIESA_SOLO_TORRI"))
        # v3.9: prova rapida della sola vista d'insieme (torri, portali e
        # gradinata) senza rilanciare i cinque dettagli centrali.
        _solo_facciata = bool(os.environ.get("CHIESA_SOLO_FACCIATA"))
        _salta_tutto = (_solo_galleria or _solo_rosone or _solo_cuspidi
                        or _solo_torri or _solo_facciata)
        if not _salta_tutto or _solo_facciata:
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
        if not (_salta_centrali or (_salta_tutto and not _solo_torri)):
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
        if not (_solo_rosone or _solo_cuspidi or _solo_torri or _salta_centrali
                or _solo_facciata):
            target_galleria = Vector((0.0, -1.50 * SCALA, 23.25 * SCALA))
            cam.location = (0.0, -22.00 * SCALA, 23.55 * SCALA)
            cam.rotation_euler = (target_galleria - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 46.5
            scene.render.resolution_x = int(os.environ.get("CHIESA_GALLERIA_RES_X", 1600))
            scene.render.resolution_y = int(os.environ.get("CHIESA_GALLERIA_RES_Y", 520))
            scene.render.filepath = GALLERIA_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Dettaglio della galleria salvato: anteprima_galleria.png")

        # Quarta inquadratura (v2.7): il rosone e le statue che lo circondano,
        # inquadrati come nella fotografia di riferimento `riferimento_vetrata.jpg`.
        if not (_solo_cuspidi or _solo_torri or _salta_centrali or _solo_facciata):
            target_rosone = Vector((0.0, -1.45 * SCALA, (Z_PAN + 0.88) * SCALA))
            cam.location = (0.0, -15.0 * SCALA, (Z_PAN + 0.88) * SCALA)
            cam.rotation_euler = (target_rosone - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 47.5
            scene.render.resolution_x = int(os.environ.get("CHIESA_ROSone_RES_X", 1453))
            scene.render.resolution_y = int(os.environ.get("CHIESA_ROSone_RES_Y", 1582))
            scene.render.filepath = ROSONE_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Dettaglio del rosone salvato: anteprima_rosone.png")

        # Quinta inquadratura (v3.2): le due torri-pinnacolo con i loro
        # coronamenti completi, inquadrate dal basso come in riferimento_apice.jpg.
        if not (_solo_galleria or _solo_rosone or _solo_cuspidi or _solo_facciata):
            target_torri = Vector((0.0, -1.55 * SCALA, 26.20 * SCALA))
            cam.location = (0.0, -21.0 * SCALA, 21.00 * SCALA)
            cam.rotation_euler = (target_torri - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 36.0
            scene.render.resolution_x = int(os.environ.get("CHIESA_TORRI_RES_X", 1500))
            scene.render.resolution_y = int(os.environ.get("CHIESA_TORRI_RES_Y", 820))
            scene.render.filepath = TORRI_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Dettaglio delle due torri salvato: anteprima_torri.png")

            # v3.3: primi piani verticali di ciascuna torre (model_sx.png /
            # model_dx.png), usati da crea_confronto_torri.py.  Prima erano
            # render manuali fatti in Blender e non rigenerabili da script.
            for _side_t, _nome_t in ((-1, "model_sx.png"), (1, "model_dx.png")):
                _cx_t = _side_t * 5.35
                target_t = Vector((_cx_t * SCALA, -1.55 * SCALA, 24.55 * SCALA))
                cam.location = ((_cx_t + _side_t * 1.90) * SCALA,
                                -20.50 * SCALA, 23.40 * SCALA)
                cam.rotation_euler = (target_t - cam.location).to_track_quat("-Z", "Y").to_euler()
                cam.data.lens = 45.0
                scene.render.resolution_x = int(os.environ.get("CHIESA_TORRE1_RES_X", 520))
                scene.render.resolution_y = int(os.environ.get("CHIESA_TORRE1_RES_Y", 1420))
                scene.render.filepath = os.path.join(OUT_DIR, _nome_t)
                bpy.ops.render.render(write_still=True)
                print(f"Primo piano torre salvato: {_nome_t}")

        # Quinta inquadratura (v2.9): lo stesso taglio panoramico 3120×1146
        # del nuovo riferimento, con statue apicali intere e rosone in asse.
        if not (_solo_galleria or _solo_rosone or _solo_torri or _solo_facciata):
            target_cusp = Vector((0.0, -1.45 * SCALA, 22.33 * SCALA))
            cam.location = (0.0, -28.0 * SCALA, 22.33 * SCALA)
            cam.rotation_euler = (target_cusp - cam.location).to_track_quat("-Z", "Y").to_euler()
            cam.data.lens = 45.4
            scene.render.resolution_x = int(os.environ.get("CHIESA_CUSPIDI_RES_X", 1800))
            scene.render.resolution_y = int(os.environ.get("CHIESA_CUSPIDI_RES_Y", 660))
            scene.render.filepath = CUSPIDI_PNG_PATH
            bpy.ops.render.render(write_still=True)
            print("Dettaglio delle cuspidi con i mosaici salvato: anteprima_cuspidi.png")

        # Il .blend resta impostato sull'inquadratura generale.
        cam.location = camera_loc_main
        cam.rotation_euler = camera_rot_main
        cam.data.lens = lens_main
        scene.render.resolution_x, scene.render.resolution_y = res_main
        scene.render.filepath = PNG_PATH
    except Exception as e:
        print(f"Render anteprima non riuscito: {e}")
    finally:
        for _c in _col_muri_preview:
            _c.hide_render = False

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

print("Generazione v3.9 completata!")
sys.stdout.flush()
sys.stderr.flush()
if "bpy" in sys.modules and not bpy.app.binary_path:
    # Evita crash del distruttore C++ TBB in uscita quando bpy gira come modulo pip
    os._exit(0)
