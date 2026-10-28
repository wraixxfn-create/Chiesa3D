#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIBURIO, CALOTTA E LANTERNA DEL DUOMO DI SIENA (v5.2)
=====================================================

Sostituisce la vecchia cupola "a campana liscia" di `muri_esterni.py` con il
gruppo tiburio-cupola disegnato sulle fotografie allegate:

    riferimento_cupola.jpg            vista d'insieme dal Facciatone
    riferimento_cupola_fianco.jpg     fianco destro, calotta e tiburio
    riferimento_cupola_lanterna.jpg   lanterna e mela dorata in primo piano
    riferimento_cupola_aerea.jpg      volumi visti dall'alto
    riferimento_cupola_tramonto.jpg   calotta in controluce

Che cosa cambia rispetto alla v4.4
----------------------------------
1. TAMBUrRO a due ordini di logge, come nella realta': in basso colonne
   BINATE con archetti a sesto acuto, in alto colonne singole piu' corte con
   archetti a tutto sesto.  Le aperture sono vera geometria (parete
   poligonale forata, con spessore di muro), non una superficie dipinta:
   dentro si vede la canna in laterizio e il pavimento della galleria,
   quindi la loggia ha profondita' e ombra.
2. Bicromia senese: attico con fasce di serpentino, fregio a scacchiera fra
   i due ordini, dentelli sotto ogni cornice.
3. CALOTTA a LASTRE, riscritta nella v5.2: il profilo non e' piu' una
   semisfera ma una curva OGIVALE desunta dalle fotografie (spalla quasi
   verticale, chiusura a punta).  768 lastre di piombo vere sono disposte in
   12 filari e 16 spicchi da 4 strisce, con pieghe di giunzione rilevate,
   SEDICI costoloni a nastro rastremato, linguette di gronda e una patina
   procedurale piu' scura (velature, colature, ruggine) al posto del grigio
   uniforme.
4. LANTERNA del Bernini (1667) ricostruita nella v5.2 sulla fotografia in
   primo piano: corpo circolare a 64 facce con OTTO finestre RETTANGOLARI
   traforate (montanti, traversi e rosette ovali), colonnine binate, cornice
   a mensole, fascia in piombo con oculi ovali, tetto concavo a OTTO LOBI
   con i colmi di piombo, vaso lapideo a risalti, mela dorata sfaccettata,
   stella d'oro a raggi piramidali e segnavento.
5. Le quote ufficiali non cambiano: 48 m alla punta del segnavento, calotta
   impostata a 30,05 m.  La facciata (37,5 m) non viene toccata.

Tutte le misure sono in METRI REALI e vengono moltiplicate per `scala`.

Uso
---
    python aggiorna_cupola.py                    # aggiorna il .blend
    blender --background --python aggiorna_cupola.py

oppure, da `muri_esterni.costruisci_muri_esterni()`:

    from cupola import costruisci_cupola
    costruisci_cupola(scala=3.0, col=collezione_07d)
"""

import math

try:
    import bpy
    from mathutils import Vector  # noqa: F401
except ImportError:  # pragma: no cover - i dati restano importabili in 2D
    bpy = None


# -----------------------------------------------------------------------------
# 1. QUOTE (metri reali, facciata di riferimento 37,5 m)
# -----------------------------------------------------------------------------
H_ATTICO_BASE = 23.60     # piede del tiburio (l'esagono sopra la crociera)
H_ATTICO_TOP = 24.55      # cornice superiore dell'attico bicromo
H_LOGGE_INF_BASE = 24.72  # piano della loggia inferiore
H_LOGGE_INF_TOP = 27.30   # trabeazione della loggia inferiore
H_LOGGE_SUP_BASE = 28.30  # piano della loggetta (sopra la fascia bicroma)
H_LOGGE_SUP_TOP = 29.80   # trabeazione della loggetta
H_CALOTTA_BASE = 30.05    # filo di gronda in piombo (imposta della calotta)
H_CALOTTA = 39.20         # apice della calotta = imposta della lanterna
H_LANTERNA_BASE = H_CALOTTA
H_CUPOLA = 48.00          # punta della croce (quota ufficiale)

# --- lanterna (v5.2): quote interne, tutte riferite a H_LANTERNA_BASE -------
# Nelle fotografie il tempietto e' cilindrico, non ottagono: il corpo e' un
# 64-gono con OTTO finestre rettangolari.  Il tetto e' una copertura concava
# a otto lobi, piu' alta della piramide v5.1, e il fastigio (mela, stella e
# segnavento) e' stato ridisegnato con volumi sfaccettati.
L_ZOCOLO = 0.92           # dado pieno, dal basamento al davanzale
L_DAVANZALE = 0.95        # piano delle finestre
L_IMPOSTA = 3.02          # sommita' delle finestre rettangolari
L_ARCHI = 0.0             # niente arco: le finestre sono rettangolari
L_CORONA = 3.58           # sommita' del corpo finestrato
L_TRABEAZIONE = 3.98      # sommita' della cornice a mensole
L_GRONDA = 4.48           # bordo della fascia in piombo con gli oculi
L_TETTO = 7.15            # colmo del tetto concavo a otto lobi
L_VASO = 7.58             # sommita' del vaso lapideo
L_MELA = 7.74             # centro della mela dorata (46,94 m)
L_STELLA = 8.24           # centro della stella
R_MELA = 0.40
R_STELLA = 0.36

R_ATTICO = 11.335         # esagono del tiburio (22,67 m fra i vertici)
R_LOGGE_INF = 11.10       # 24-gono della loggia inferiore
R_LOGGE_SUP = 10.35       # dodecagono della loggia superiore
R_CALOTTA = 10.10         # raggio della calotta alla base (diametro 20,2 m)
R_GRONDA = 10.55          # ghiaccio di gronda in piombo (aggetto)

# Tempietto: 5,84 m di diametro.  Nelle fotografie la lanterna e' circa un
# quarto del diametro della calotta (20,2 m) e il suo corpo, escluse le
# modanature, e' piu' stretto che alto.
R_LANTERNA = 2.92
R_LANTERNA_BASE = 3.22    # basamento e cornice
LATO_SUP = 0.55           # spessore dei muri delle logge
LATO_LANTERNA = 0.40      # spessore dei muri della lanterna

LATI_LOGGE_INF = 24       # due ordini entrambi a ventiquattro lati
LATI_LOGGE_SUP = 24
LATI_CORPO_LANTERNA = 64  # cilindro del corpo finestrato
LATI_LANTERNA = LATI_CORPO_LANTERNA   # compatibilita' con i test v5.1
BAIE_LANTERNA = 8         # otto finestre rettangolari
BAIE_LOGGE_INF = 48       # 48 archi acuti -> passo 1.45 m, luce 0.78 m
BAIE_LOGGE_SUP = 48       # 48 archetti -> passo 1.35 m, come nella foto

PASSO_DENTELLI = 0.46
SPESSORE_FASCIA = 0.13

COSTOLONI = 16            # sedici costoloni esterni, come nella cupola reale
SPICCHI = 16
FILARI_CALOTTA = 12       # filari di lastre lungo il meridiano
STRISCE_PER_SPICCHIO = 4  # 16 x 4 x 12 = 768 lastre in tutto
PANNELLO_V = 0.92         # altezza media dei filari (m), usata solo nei test


NOMI_MAT = {
    "marmo": "Marmo_Bianco_Caldo",
    "cornice": "Marmo_Bianco",
    "scuro": "Marmo_Verde_Scuro",
    "piombo": "Cupola_Piombo_Lastre",
    "piombo_costa": "Cupola_Piombo_Costoloni",
    "giunti": "Cupola_Piombo_Giunti",
    "oro": "Cupola_Oro",
    "interno": "Cupola_Interno_Laterizio",
    "ferro": "Cupola_Ferro",
}


# -----------------------------------------------------------------------------
# 2. MATERIALI
# -----------------------------------------------------------------------------
VERSIONE_MATERIALI = "5.2.0"


def _versione_ok(m):
    """I materiali della cupola si rigenerano se la versione e' cambiata.

    Senza questo controllo un materiale gia' salvato nel .blend resterebbe
    quello della run precedente e le modifiche ai colori non si vedrebbero.
    """
    return m.get("versione_cupola") == VERSIONE_MATERIALI


def _nuovo_materiale_cupola(nome):
    vecchio = bpy.data.materials.get(nome)
    if vecchio is not None:
        bpy.data.materials.remove(vecchio)
    m = bpy.data.materials.new(nome)
    m["versione_cupola"] = VERSIONE_MATERIALI
    return m


# Materiali CONDIVISI con la facciata: si usano sempre quelli del .blend,
# con le loro texture PBR.  Rigenerarli qui vorrebbe dire cancellare i marmi
# del fronte, che sono il riferimento fisso del progetto.
NOMI_CONDIVISI = (NOMI_MAT["marmo"], NOMI_MAT["cornice"], NOMI_MAT["scuro"])


def _materiale_esistente_o_piatto(nome, colore, roughness=0.72, noise=0.0,
                                  scala=3.0):
    m = bpy.data.materials.get(nome)
    if m is not None and (nome in NOMI_CONDIVISI or _versione_ok(m)):
        return m
    m = _nuovo_materiale_cupola(nome)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (420, 60)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (120, 60)
    bsdf.inputs["Base Color"].default_value = (*colore, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    if noise > 0.0:
        coord = nodes.new("ShaderNodeTexCoord")
        coord.location = (-760, -120)
        scl = nodes.new("ShaderNodeVectorMath")
        scl.operation = "SCALE"
        scl.inputs["Scale"].default_value = 0.34 / max(scala, 1e-6)
        scl.location = (-560, -120)
        ntx = nodes.new("ShaderNodeTexNoise")
        ntx.inputs["Scale"].default_value = 1.0
        ntx.inputs["Detail"].default_value = 3.0
        ntx.location = (-360, -120)
        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.location = (-140, -120)
        k = noise
        ramp.color_ramp.elements[0].color = (
            max(0.0, colore[0] * (1 - k)), max(0.0, colore[1] * (1 - k)),
            max(0.0, colore[2] * (1 - k)), 1.0)
        ramp.color_ramp.elements[1].color = (
            min(1.0, colore[0] * (1 + k)), min(1.0, colore[1] * (1 + k)),
            min(1.0, colore[2] * (1 + k)), 1.0)
        links.new(coord.outputs["Object"], scl.inputs[0])
        links.new(scl.outputs["Vector"], ntx.inputs["Vector"])
        links.new(ntx.outputs["Fac"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    return m


def _tex_noise(nodes, links, coord, scala, metri, detail=6.0, rough=0.55,
               distortion=0.0, loc=(-700, 0), aniso=None):
    """Noise texture in coordinate OGGETTO con dimensione in metri reali.

    Gli oggetti della cupola non hanno trasformazioni e le mesh sono in unita'
    modello (1 m = `scala`); il fattore di scala del Mapping vale quindi
    `1 / (scala * metri)`, cioe' "una chiazza ogni `metri` metri".
    """
    mappa = nodes.new("ShaderNodeMapping")
    mappa.location = (loc[0] + 180, loc[1])
    base = 1.0 / max(scala * metri, 1e-6)
    if aniso is None:
        mappa.inputs["Scale"].default_value = (base, base, base)
    else:
        mappa.inputs["Scale"].default_value = (base * aniso[0], base * aniso[1],
                                               base * aniso[2])
    ntx = nodes.new("ShaderNodeTexNoise")
    ntx.location = loc
    ntx.inputs["Scale"].default_value = 1.0
    ntx.inputs["Detail"].default_value = detail
    ntx.inputs["Roughness"].default_value = rough
    if "Distortion" in ntx.inputs:
        ntx.inputs["Distortion"].default_value = distortion
    links.new(coord, mappa.inputs["Vector"])
    links.new(mappa.outputs["Vector"], ntx.inputs["Vector"])
    return ntx


def _materiale_piombo(scala=3.0):
    """Piombo vecchio della calotta (v5.2).

    Le lastre non sono piu' disegnate da una texture: dalla v5.2 sono 768
    piastre di geometria vera con le pieghe di giunzione rilevate, quindi il
    materiale deve solo raccontare la MATERIA.  Rispetto alla v5.1 il piombo
    e' piu' scuro e meno azzurrato, con velature piu' fredde, colature lunghe
    e poche chiazze di ruggine: nelle fotografie la calotta e' quasi nera
    quando e' in ombra, non grigio chiaro.
    """
    nome = NOMI_MAT["piombo"]
    m = bpy.data.materials.get(nome)
    if m is not None and _versione_ok(m):
        return m
    m = _nuovo_materiale_cupola(nome)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (980, 60)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (700, 60)
    bsdf.inputs["Metallic"].default_value = 0.24
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    coord = nodes.new("ShaderNodeTexCoord")
    coord.location = (-1180, 0)

    # 1) patina: chiazze larghe, dal piombo scuro alla velatura chiara
    patina = _tex_noise(nodes, links, coord.outputs["Object"], scala, 11.0,
                        detail=4.0, rough=0.48, distortion=0.12,
                        loc=(-900, 300))
    ramp_p = nodes.new("ShaderNodeValToRGB")
    ramp_p.location = (-620, 300)
    e = ramp_p.color_ramp.elements
    e[0].position = 0.34
    e[0].color = (0.185, 0.195, 0.205, 1.0)     # piombo annerito
    e[1].position = 0.68
    e[1].color = (0.305, 0.315, 0.322, 1.0)     # velatura chiara
    medio = ramp_p.color_ramp.elements.new(0.50)
    medio.color = (0.245, 0.255, 0.265, 1.0)
    links.new(patina.outputs["Fac"], ramp_p.inputs["Fac"])

    # 2) colature verticali: rumore stirato in altezza
    cola = _tex_noise(nodes, links, coord.outputs["Object"], scala, 0.55,
                      detail=6.0, rough=0.58,
                      loc=(-900, 0), aniso=(1.0, 1.0, 0.22))
    ramp_c = nodes.new("ShaderNodeValToRGB")
    ramp_c.location = (-620, 0)
    ec = ramp_c.color_ramp.elements
    ec[0].position = 0.46
    ec[0].color = (0.0, 0.0, 0.0, 1.0)
    ec[1].position = 0.70
    ec[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(cola.outputs["Fac"], ramp_c.inputs["Fac"])

    scuro = nodes.new("ShaderNodeMixRGB")
    scuro.location = (-340, 200)
    scuro.blend_type = "MULTIPLY"
    scuro.inputs["Fac"].default_value = 0.55
    scuro.inputs["Color2"].default_value = (0.56, 0.57, 0.59, 1.0)
    links.new(ramp_p.outputs["Color"], scuro.inputs["Color1"])
    links.new(ramp_c.outputs["Color"], scuro.inputs["Fac"])

    # 3) ruggine: poche chiazze calde, larghe, non uniformi
    # 2b) seconda velatura, scala media: due rumori sovrapposti tolgono
    #     l'effetto "foglio grigio" e danno il piombo vecchio a chiazze
    velo = _tex_noise(nodes, links, coord.outputs["Object"], scala, 2.6,
                      detail=6.0, rough=0.55, distortion=0.25,
                      loc=(-900, 620))
    ramp_v = nodes.new("ShaderNodeValToRGB")
    ramp_v.location = (-620, 620)
    ev = ramp_v.color_ramp.elements
    ev[0].position = 0.38
    ev[0].color = (0.70, 0.70, 0.70, 1.0)
    ev[1].position = 0.72
    ev[1].color = (0.98, 0.98, 0.98, 1.0)
    links.new(velo.outputs["Fac"], ramp_v.inputs["Fac"])

    rugg = _tex_noise(nodes, links, coord.outputs["Object"], scala, 0.85,
                      detail=9.0, rough=0.68, distortion=0.6,
                      loc=(-900, -320))
    ramp_r = nodes.new("ShaderNodeValToRGB")
    ramp_r.location = (-620, -320)
    er = ramp_r.color_ramp.elements
    er[0].position = 0.60
    er[0].color = (0.0, 0.0, 0.0, 1.0)
    er[1].position = 0.78
    er[1].color = (0.55, 0.55, 0.55, 1.0)
    links.new(rugg.outputs["Fac"], ramp_r.inputs["Fac"])

    velato = nodes.new("ShaderNodeMixRGB")
    velato.location = (-200, 300)
    velato.blend_type = "MULTIPLY"
    velato.inputs["Fac"].default_value = 0.85
    links.new(scuro.outputs["Color"], velato.inputs["Color1"])
    links.new(ramp_v.outputs["Color"], velato.inputs["Color2"])

    ruggine = nodes.new("ShaderNodeMixRGB")
    ruggine.location = (-60, 160)
    ruggine.inputs["Color2"].default_value = (0.205, 0.090, 0.045, 1.0)
    links.new(velato.outputs["Color"], ruggine.inputs["Color1"])
    links.new(ramp_r.outputs["Color"], ruggine.inputs["Fac"])
    links.new(ruggine.outputs["Color"], bsdf.inputs["Base Color"])

    # 4) rugosita': la patina e' opaca, i punti lucidi sono pochi
    rug = nodes.new("ShaderNodeMapRange")
    rug.location = (300, -260)
    rug.inputs["From Min"].default_value = 0.0
    rug.inputs["From Max"].default_value = 1.0
    rug.inputs["To Min"].default_value = 0.70
    rug.inputs["To Max"].default_value = 0.46
    links.new(patina.outputs["Fac"], rug.inputs["Value"])
    links.new(rug.outputs["Result"], bsdf.inputs["Roughness"])

    # 5) micro-rilievo della lamiera battuta
    fine = _tex_noise(nodes, links, coord.outputs["Object"], scala, 0.055,
                      detail=4.0, rough=0.5, loc=(-900, -640))
    bump = nodes.new("ShaderNodeBump")
    bump.location = (300, -520)
    bump.inputs["Strength"].default_value = 0.22
    bump.inputs["Distance"].default_value = 0.012
    links.new(fine.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def _materiale_piombo_costa(scala=3.0):
    """Piombo dei costoloni e delle pieghe: un filo piu' chiaro e piu'
    lucido delle lastre, cosi' i nastri si leggono in rilievo anche quando
    la calotta e' in ombra."""
    nome = NOMI_MAT["piombo_costa"]
    m = bpy.data.materials.get(nome)
    if m is not None and _versione_ok(m):
        return m
    m = _nuovo_materiale_cupola(nome)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (520, 40)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (260, 40)
    bsdf.inputs["Metallic"].default_value = 0.45
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    coord = nodes.new("ShaderNodeTexCoord")
    coord.location = (-700, 0)
    ntx = _tex_noise(nodes, links, coord.outputs["Object"], scala, 0.55,
                     detail=6.0, rough=0.55, loc=(-480, 0))
    ramp = nodes.new("ShaderNodeValToRGB")
    ramp.location = (-220, 0)
    ramp.color_ramp.elements[0].color = (0.270, 0.280, 0.286, 1.0)
    ramp.color_ramp.elements[1].color = (0.410, 0.418, 0.416, 1.0)
    links.new(ntx.outputs["Fac"], ramp.inputs["Fac"])
    links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = 0.36
    return m


def _materiale_giunti(scala=3.0):
    """Pieghe di giunzione delle lastre: piombo un filo piu' scuro e opaco
    dei pannelli, cosi' le linee si leggono senza brillare."""
    nome = NOMI_MAT["giunti"]
    m = bpy.data.materials.get(nome)
    if m is not None and _versione_ok(m):
        return m
    m = _nuovo_materiale_cupola(nome)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (320, 40)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (60, 40)
    bsdf.inputs["Base Color"].default_value = (0.165, 0.175, 0.182, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.30
    bsdf.inputs["Roughness"].default_value = 0.44
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def _materiale_oro(scala=3.0):
    nome = NOMI_MAT["oro"]
    m = bpy.data.materials.get(nome)
    if m is not None and _versione_ok(m):
        return m
    m = _nuovo_materiale_cupola(nome)
    m.use_nodes = True
    nodes, links = m.node_tree.nodes, m.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (360, 40)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (100, 40)
    bsdf.inputs["Base Color"].default_value = (0.960, 0.720, 0.230, 1.0)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.13
    bsdf.inputs["Coat Weight"].default_value = 0.25
    bsdf.inputs["Coat Roughness"].default_value = 0.08
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def _materiali(scala):
    return {
        "marmo": _materiale_esistente_o_piatto(
            NOMI_MAT["marmo"], (0.79, 0.75, 0.68), noise=0.10, scala=scala),
        "cornice": _materiale_esistente_o_piatto(
            NOMI_MAT["cornice"], (0.86, 0.82, 0.75), scala=scala),
        "scuro": _materiale_esistente_o_piatto(
            NOMI_MAT["scuro"], (0.15, 0.18, 0.17), roughness=0.55,
            noise=0.06, scala=scala),
        "piombo": _materiale_piombo(scala),
        "piombo_costa": _materiale_piombo_costa(scala),
        "giunti": _materiale_giunti(scala),
        "oro": _materiale_oro(scala),
        # Il vano delle gallerie e' laterizio a vista: rosso caldo e opaco,
        # cosi' dentro le logge si legge un'ombra calda e non del marmo.
        "interno": _materiale_esistente_o_piatto(
            NOMI_MAT["interno"], (0.115, 0.082, 0.068), roughness=0.96,
            noise=0.10, scala=scala),
        "ferro": _materiale_esistente_o_piatto(
            NOMI_MAT["ferro"], (0.075, 0.078, 0.085), roughness=0.45,
            scala=scala),
    }


# -----------------------------------------------------------------------------
# 3. ACCUMULATORE DI GEOMETRIA (un oggetto per "materiale/ruolo")
# -----------------------------------------------------------------------------
class Accumulatore(object):
    def __init__(self):
        self.verts = []
        self.faces = []

    def v(self, x, y, z):
        self.verts.append((x, y, z))
        return len(self.verts) - 1

    def poligono(self, poly, z):
        return [self.v(x, y, z) for x, y in poly]

    def prisma(self, poly, z0, z1):
        n = len(poly)
        a = self.poligono(poly, z0)
        b = self.poligono(poly, z1)
        self.faces.append(tuple(reversed(a)))
        self.faces.append(tuple(b))
        for i in range(n):
            j = (i + 1) % n
            self.faces.append((a[i], a[j], b[j], b[i]))

    def anello(self, poly_est, poly_int, z0, z1):
        """Muro cavo fra due poligoni (cornici, parapetti, canne)."""
        n = len(poly_est)
        e0 = self.poligono(poly_est, z0)
        e1 = self.poligono(poly_est, z1)
        i0 = self.poligono(poly_int, z0)
        i1 = self.poligono(poly_int, z1)
        for k in range(n):
            j = (k + 1) % n
            self.faces.append((e0[k], e0[j], e1[j], e1[k]))
            self.faces.append((i0[j], i0[k], i1[k], i1[j]))
            self.faces.append((e1[k], e1[j], i1[j], i1[k]))
            self.faces.append((e0[j], e0[k], i0[k], i0[j]))

    def rombo(self, cx, cy, z, ux, uy, larghezza, altezza, profondita):
        """Prisma a sezione di rombo, disteso nel piano della parete.

        Serve per la fascia bicroma del tamburo: il tassello di serpentino e'
        un quadrato ruotato di 45 gradi *nella faccia*, non in pianta, quindi
        `(ux, uy)` e' la direzione tangente alla parete e la profondita'
        sporge lungo la normale.
        """
        vx, vy = -uy, ux          # normale uscente
        semil, semia = larghezza / 2.0, altezza / 2.0
        prof = profondita / 2.0
        fuori, dentro = [], []
        for dx, dy, dz in ((0.0, 0.0, semia), (semil, 0.0, 0.0),
                           (0.0, 0.0, -semia), (-semil, 0.0, 0.0)):
            fuori.append(self.v(cx + ux * dx + vx * prof,
                                cy + uy * dx + vy * prof, z + dz))
            dentro.append(self.v(cx + ux * dx - vx * prof,
                                 cy + uy * dx - vy * prof, z + dz))
        self.faces.append(tuple(fuori))
        self.faces.append(tuple(reversed(dentro)))
        for i in range(4):
            j = (i + 1) % 4
            self.faces.append((fuori[i], fuori[j], dentro[j], dentro[i]))

    def canna(self, poly, z0, z1, tappo=False):
        """Cilindro poligonale (canna interna delle gallerie)."""
        n = len(poly)
        a = self.poligono(poly, z0)
        b = self.poligono(poly, z1)
        for i in range(n):
            j = (i + 1) % n
            self.faces.append((a[j], a[i], b[i], b[j]))
        if tappo:
            self.faces.append(tuple(b))

    def scatola(self, cx, cy, z, ux, uy, sx, sy, sz):
        """Parallelepipedo orientato: (ux, uy) e' la direzione locale x in
        pianta, `z` e' la quota del CENTRO."""
        vx, vy = -uy, ux
        hx, hy, hz = sx / 2.0, sy / 2.0, sz / 2.0
        base, cima = [], []
        for zz, dst in ((z - hz, base), (z + hz, cima)):
            for sxs, sys in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                dst.append(self.v(cx + ux * sxs * hx + vx * sys * hy,
                                  cy + uy * sxs * hx + vy * sys * hy, zz))
        self.faces.append(tuple(reversed(base)))
        self.faces.append(tuple(cima))
        for i in range(4):
            j = (i + 1) % 4
            self.faces.append((base[i], base[j], cima[j], cima[i]))

    def cilindro(self, cx, cy, z0, z1, raggio, seg=12, raggio_alto=None,
                 tappo=True):
        r1 = raggio if raggio_alto is None else raggio_alto
        a, b = [], []
        for i in range(seg):
            ang = 2.0 * math.pi * i / seg
            ca, sa = math.cos(ang), math.sin(ang)
            a.append(self.v(cx + raggio * ca, cy + raggio * sa, z0))
            b.append(self.v(cx + r1 * ca, cy + r1 * sa, z1))
        for i in range(seg):
            j = (i + 1) % seg
            self.faces.append((a[i], a[j], b[j], b[i]))
        if tappo:
            self.faces.append(tuple(reversed(a)))
            self.faces.append(tuple(b))

    def rivoluzione(self, cx, cy, profilo, seg=16, sy=1.0, costa=0.0,
                    coste=8, ruota=0.0):
        """Solido di rotazione: `profilo` = sequenza di (z, raggio)."""
        anelli = []
        for k, (zz, rr) in enumerate(profilo):
            riga = []
            for j in range(seg):
                ang = 2.0 * math.pi * j / seg + ruota
                f = 1.0 + costa * math.cos(coste * ang)
                riga.append(self.v(cx + rr * f * math.cos(ang),
                                   cy + rr * f * math.sin(ang) * sy, zz))
            anelli.append(riga)
        for k in range(len(profilo) - 1):
            for j in range(seg):
                j2 = (j + 1) % seg
                self.faces.append((anelli[k][j], anelli[k][j2],
                                   anelli[k + 1][j2], anelli[k + 1][j]))
        self.faces.append(tuple(reversed(anelli[0])))
        self.faces.append(tuple(anelli[-1]))

    def tubo(self, pts, raggio, seg=8, cx=0.0, cy=0.0, schiacciamento=1.0):
        """Tubo lungo una polilinea di punti (raggio, quota, angolo).

        Il centro dell'anello (`cx`, `cy`) e' quello del tamburo: le
        coordinate dei punti sono cilindriche rispetto a quell'asse.

        La sezione e' orientata con due versori ricavati punto per punto:
        quello RADIALE (nel piano del meridiano) e quello AZIMUTALE.  Cosi'
        il costolone resta tondo anche dove il profilo si impenna.
        """
        n = len(pts)
        raggi = raggio if isinstance(raggio, (list, tuple)) else [raggio] * n
        anelli = []
        for i, (r, z, ang) in enumerate(pts):
            if i == 0:
                r2, z2, _ = pts[1]
                t = (r2 - r, z2 - z)
            elif i == n - 1:
                r2, z2, _ = pts[-2]
                t = (r - r2, z - z2)
            else:
                r0, z0, _ = pts[i - 1]
                r2, z2, _ = pts[i + 1]
                t = (r2 - r0, z2 - z0)
            lt = math.hypot(*t) or 1.0
            tr, tz = t[0] / lt, t[1] / lt
            nr, nz = -tz, tr
            ca, sa = math.cos(ang), math.sin(ang)
            riga = []
            for j in range(seg):
                phi = 2.0 * math.pi * j / seg
                cp, sp = math.cos(phi), math.sin(phi)
                # sezione ellittica: `schiacciamento` < 1 abbassa il
                # rilievo e allarga il nastro (costoloni bassi e larghi)
                rr = r + raggi[i] * (cp * nr) * schiacciamento
                zz = z + raggi[i] * (cp * nz) * schiacciamento
                riga.append(self.v(cx + rr * ca - raggi[i] * sp * sa,
                                   cy + rr * sa + raggi[i] * sp * ca, zz))
            anelli.append(riga)
        for k in range(n - 1):
            for j in range(seg):
                j2 = (j + 1) % seg
                self.faces.append((anelli[k][j], anelli[k][j2],
                                   anelli[k + 1][j2], anelli[k + 1][j]))
        self.faces.append(tuple(reversed(anelli[0])))
        self.faces.append(tuple(anelli[-1]))

    def tubo3d(self, punti, raggio, seg=10):
        """Tubo lungo una polilinea 3D qualsiasi (croce, bracci, tiranti).

        I versori di sezione si ricavano dal vettore tangente e da un "alto"
        di riferimento: stabile per curve planari come i bracci ricurvi.
        """
        n = len(punti)
        raggi = raggio if isinstance(raggio, (list, tuple)) else [raggio] * n
        anelli = []
        for i, p in enumerate(punti):
            if i == 0:
                t = (punti[1][0] - p[0], punti[1][1] - p[1], punti[1][2] - p[2])
            elif i == n - 1:
                t = (p[0] - punti[-2][0], p[1] - punti[-2][1],
                     p[2] - punti[-2][2])
            else:
                t = (punti[i + 1][0] - punti[i - 1][0],
                     punti[i + 1][1] - punti[i - 1][1],
                     punti[i + 1][2] - punti[i - 1][2])
            lt = math.sqrt(t[0] ** 2 + t[1] ** 2 + t[2] ** 2) or 1.0
            tx, ty, tz = t[0] / lt, t[1] / lt, t[2] / lt
            # versore di riferimento: asse Y se il tubo non e' verticale,
            # altrimenti asse X
            if abs(ty) < 0.9:
                ux, uy, uz = 0.0, 1.0, 0.0
            else:
                ux, uy, uz = 1.0, 0.0, 0.0
            nx = ty * uz - tz * uy
            ny = tz * ux - tx * uz
            nz = tx * uy - ty * ux
            ln = math.sqrt(nx * nx + ny * ny + nz * nz) or 1.0
            nx, ny, nz = nx / ln, ny / ln, nz / ln
            bx = ty * nz - tz * ny
            by = tz * nx - tx * nz
            bz = tx * ny - ty * nx
            riga = []
            for j in range(seg):
                phi = 2.0 * math.pi * j / seg
                c, s = math.cos(phi), math.sin(phi)
                riga.append(self.v(p[0] + raggi[i] * (c * nx + s * bx),
                                   p[1] + raggi[i] * (c * ny + s * by),
                                   p[2] + raggi[i] * (c * nz + s * bz)))
            anelli.append(riga)
        for k in range(n - 1):
            for j in range(seg):
                j2 = (j + 1) % seg
                self.faces.append((anelli[k][j], anelli[k][j2],
                                   anelli[k + 1][j2], anelli[k + 1][j]))
        self.faces.append(tuple(reversed(anelli[0])))
        self.faces.append(tuple(anelli[-1]))


# -----------------------------------------------------------------------------
# 4. PEZZI TIPICI
# -----------------------------------------------------------------------------
def poligono(cx, cy, raggio, lati, ruota=0.0):
    return [(cx + raggio * math.cos(ruota + 2.0 * math.pi * i / lati),
             cy + raggio * math.sin(ruota + 2.0 * math.pi * i / lati))
            for i in range(lati)]


def _lato(p0, p1):
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    lung = math.hypot(dx, dy) or 1.0
    return dx / lung, dy / lung, dy / lung, -dx / lung, lung


def _quota_arco(t, freccia, acuto):
    """Quota dell'intradosso di un arco, con t in [-1, 1].

    `acuto` = arco a sesto acuto (due archi di cerchio che si incontrano in
    punta, come nella loggia inferiore); altrimenti arco a tutto sesto.
    """
    t = max(-1.0, min(1.0, t))
    if acuto:
        # Due archi di raggio = luce, con centri sui piedritti opposti:
        # l'incontro in punta cade a 0,866 della freccia.
        return freccia * math.sqrt(max(0.0, 4.0 - (abs(t) + 1.0) ** 2)) / math.sqrt(3.0)
    return freccia * math.sqrt(max(0.0, 1.0 - t * t))


def parete_arche(acc, lati_poligono, z_sill, z_top, spessore, baie, luce,
                 freccia, z_imposta, acuto=True, campioni=9, allunga=0.0):
    """Parete poligonale chiusa forata da archi PASSANTI.

    Per ogni lato si dispongono `baie` aperture divise in parti uguali; il
    profilo inferiore della parete segue l'intradosso dell'arco, quindi le
    aperture hanno uno spessore di muro da vedere in prospettiva.
    `allunga` sfalsa le testate di ogni lato, cosi' agli spigoli i lati si
    compenetrano invece di lasciare fessure.
    """
    n_lati = len(lati_poligono)
    for i in range(n_lati):
        p0 = lati_poligono[i]
        p1 = lati_poligono[(i + 1) % n_lati]
        dx, dy, nx, ny, lung = _lato(p0, p1)
        n_baie = baie // n_lati if baie >= n_lati else baie
        passo = lung / n_baie
        meta = spessore / 2.0
        profilo = []
        for b in range(n_baie):
            u0 = b * passo
            centro = u0 + passo / 2.0
            semi = luce / 2.0
            profilo.append((u0, z_sill))
            profilo.append((centro - semi, z_sill))
            for k in range(campioni):
                t = -1.0 + 2.0 * k / (campioni - 1)
                profilo.append((centro + semi * t,
                                z_imposta + _quota_arco(t, freccia, acuto)))
            profilo.append((centro + semi, z_sill))
        profilo.append((lung, z_sill))
        est_inf, est_sup, int_inf, int_sup = [], [], [], []
        for u, z in profilo:
            x, y = p0[0] + dx * u, p0[1] + dy * u
            est_inf.append(acc.v(x + nx * meta, y + ny * meta, z))
            est_sup.append(acc.v(x + nx * meta, y + ny * meta, z_top))
            int_inf.append(acc.v(x - nx * meta, y - ny * meta, z))
            int_sup.append(acc.v(x - nx * meta, y - ny * meta, z_top))
        for k in range(len(profilo) - 1):
            acc.faces.append((est_inf[k], est_inf[k + 1],
                              est_sup[k + 1], est_sup[k]))
            acc.faces.append((int_inf[k + 1], int_inf[k],
                              int_sup[k], int_sup[k + 1]))
            acc.faces.append((est_sup[k], est_sup[k + 1],
                              int_sup[k + 1], int_sup[k]))
            acc.faces.append((est_inf[k + 1], est_inf[k],
                              int_inf[k], int_inf[k + 1]))
        # testate (sfalsate di `allunga` per chiudere gli spigoli)
        a0 = acc.v(p0[0] - dx * allunga + nx * meta,
                   p0[1] - dy * allunga + ny * meta, z_sill)
        a1 = acc.v(p0[0] - dx * allunga + nx * meta,
                   p0[1] - dy * allunga + ny * meta, z_top)
        a2 = acc.v(p0[0] - dx * allunga - nx * meta,
                   p0[1] - dy * allunga - ny * meta, z_top)
        a3 = acc.v(p0[0] - dx * allunga - nx * meta,
                   p0[1] - dy * allunga - ny * meta, z_sill)
        acc.faces.append((a0, a1, a2, a3))
        b0 = acc.v(p1[0] + dx * allunga + nx * meta,
                   p1[1] + dy * allunga + ny * meta, z_sill)
        b1 = acc.v(p1[0] + dx * allunga + nx * meta,
                   p1[1] + dy * allunga + ny * meta, z_top)
        b2 = acc.v(p1[0] + dx * allunga - nx * meta,
                   p1[1] + dy * allunga - ny * meta, z_top)
        b3 = acc.v(p1[0] + dx * allunga - nx * meta,
                   p1[1] + dy * allunga - ny * meta, z_sill)
        acc.faces.append((b3, b2, b1, b0))


def colonne(acc, lati_poligono, z0, z1, raggio, coppia=0.0, sporgenza=0.30,
            capitello=True, seg=10):
    """Colonne (o colonne binate) sui vertici del poligono.

    `sporgenza` e' la distanza del centro colonna dal filo del poligono:
    va scelta MAGGIORE di mezzo spessore del muro, altrimenti la colonna
    finisce dentro la muratura e sparisce.
    """
    n = len(lati_poligono)
    cx = sum(p[0] for p in lati_poligono) / n
    cy = sum(p[1] for p in lati_poligono) / n
    for i in range(n):
        x, y = lati_poligono[i]
        vx, vy = x - cx, y - cy
        lung = math.hypot(vx, vy) or 1.0
        vx, vy = vx / lung, vy / lung
        tx, ty = -vy, vx
        posizioni = [0.0] if coppia <= 0.0 else (-coppia, coppia)
        for s in posizioni:
            px = x + vx * sporgenza + tx * s
            py = y + vy * sporgenza + ty * s
            acc.cilindro(px, py, z0, z0 + 0.09, raggio * 1.55, seg=seg)
            acc.cilindro(px, py, z0 + 0.09, z1 - 0.17, raggio, seg=seg,
                         raggio_alto=raggio * 0.93)
            if capitello:
                acc.cilindro(px, py, z1 - 0.17, z1 - 0.10, raggio * 1.35,
                             seg=seg)
                acc.cilindro(px, py, z1 - 0.10, z1, raggio * 1.85, seg=seg)


def colonne_agli_archi(acc, lati_poligono, baie, z0, z1, raggio, coppia,
                       sporgenza, seg=10, capitello=True):
    """Colonne BINATE a ogni piedritto, non solo ai vertici del poligono.

    Nelle logge senesi fra un archetto e il successivo non c'e' un pilastro
    di muratura: ci sono due colonnine accostate, e dietro si vede il vano in
    ombra. Questa funzione mette una coppia di fusti su ogni piedritto,
    compresi quelli a meta' lato.
    """
    n_lati = len(lati_poligono)
    cx = sum(p[0] for p in lati_poligono) / n_lati
    cy = sum(p[1] for p in lati_poligono) / n_lati
    for i in range(n_lati):
        p0 = lati_poligono[i]
        p1 = lati_poligono[(i + 1) % n_lati]
        dx, dy, nx, ny, lung = _lato(p0, p1)
        n_baie = baie // n_lati if baie >= n_lati else baie
        for b in range(n_baie):
            u = b * lung / n_baie
            bx, by = p0[0] + dx * u, p0[1] + dy * u
            ox, oy = bx + nx * sporgenza, by + ny * sporgenza
            for s in (-coppia, coppia):
                px, py = ox + dx * s, oy + dy * s
                # basi e capitelli contenuti: su fusti cosi' sottili un
                # collarino troppo largo si legge come una tazzina appoggiata
                acc.cilindro(px, py, z0, z0 + 0.055, raggio * 1.35, seg=seg)
                acc.cilindro(px, py, z0 + 0.055, z1 - 0.11, raggio, seg=seg,
                             raggio_alto=raggio * 0.94)
                if capitello:
                    acc.cilindro(px, py, z1 - 0.11, z1 - 0.06, raggio * 1.18,
                                 seg=seg)
                    acc.cilindro(px, py, z1 - 0.06, z1, raggio * 1.45, seg=seg)


def dentelli(acc, lati, z0, z1, passo=PASSO_DENTELLI, sporgenza=0.11,
             larghezza=0.15, profondita=0.12):
    """Fila di dentelli sotto una cornice: uno degli elementi che nelle
    fotografie rende riconoscibile il tiburio senese."""
    n = len(lati)
    for i in range(n):
        p0, p1 = lati[i], lati[(i + 1) % n]
        dx, dy, nx, ny, lung = _lato(p0, p1)
        quanti = max(1, int(round(lung / passo)))
        for k in range(quanti):
            u = (k + 0.5) * lung / quanti
            acc.scatola(p0[0] + dx * u + nx * sporgenza,
                        p0[1] + dy * u + ny * sporgenza,
                        (z0 + z1) / 2.0, dx, dy,
                        larghezza, profondita, z1 - z0)


# -----------------------------------------------------------------------------
# 5. PROFILO DELLA CALOTTA
# -----------------------------------------------------------------------------
def _interp(nodi, t):
    """Interpolazione lineare su una spezzata di nodi (t, valore)."""
    for (t0, v0), (t1, v1) in zip(nodi, nodi[1:]):
        if t <= t1:
            f = 0.0 if t1 <= t0 else (t - t0) / (t1 - t0)
            return v0 + (v1 - v0) * min(max(f, 0.0), 1.0)
    return nodi[-1][1]


def profilo_calotta(r_base, z_base, z_apice, passi=30):
    """Profilo OGIVALE della calotta dal filo di gronda all'apice (v5.2).

    Nelle fotografie la cupola senese non e' una semisfera: la spalla e'
    quasi verticale per i primi due metri, poi il meridiano si stringe con
    una curva continua e si chiude a PUNTA sotto la lanterna.  La spezzata
    qui sotto e' il rapporto raggio/quota letto sul fianco destro della
    fotografia: e' monotona, parte da `r_base` e arriva a raggio zero con
    una pendenza finita (non con la tangente orizzontale dell'emisfero).
    """
    nodi = [(0.00, 1.000), (0.10, 0.985), (0.22, 0.930), (0.36, 0.835),
            (0.50, 0.775), (0.64, 0.670), (0.78, 0.550), (0.88, 0.435),
            (0.95, 0.300), (0.98, 0.100), (1.00, 0.000)]
    out = []
    for k in range(passi + 1):
        t = k / passi
        out.append((r_base * _interp(nodi, t),
                    z_base + (z_apice - z_base) * t))
    return out


def _lunghezza_profilo(nodi):
    return sum(math.hypot(r1 - r0, z1 - z0)
               for (r0, z0), (r1, z1) in zip(nodi, nodi[1:]))


def _profilo_archi(nodi, quanti):
    """Ricampiona una spezzata (r, z) a passi di ARCO costanti.

    Serve alla calotta: se i filari fossero distribuiti sull'angolo, le lastre
    in cima diventerebbero strisce sottilissime.  A passi di arco costanti
    ogni filaro ha la stessa altezza di lamiera, come nel vero.
    """
    cum = [0.0]
    for (r0, z0), (r1, z1) in zip(nodi, nodi[1:]):
        cum.append(cum[-1] + math.hypot(r1 - r0, z1 - z0))
    totale = cum[-1]
    out, j = [], 0
    for k in range(quanti + 1):
        s = totale * k / quanti
        while j < len(cum) - 2 and cum[j + 1] < s:
            j += 1
        seg = cum[j + 1] - cum[j]
        f = 0.0 if seg <= 0.0 else min(max((s - cum[j]) / seg, 0.0), 1.0)
        out.append((nodi[j][0] + (nodi[j + 1][0] - nodi[j][0]) * f,
                    nodi[j][1] + (nodi[j + 1][1] - nodi[j][1]) * f))
    return out


def profilo_calotta_lastre(r_base, z_base, z_apice, filari=FILARI_CALOTTA,
                           r_min=None):
    """Profilo della calotta dal filo di gronda fino alla lanterna.

    Ritorna `filari + 1` nodi equidistanti lungo l'arco del meridiano,
    dall'imposta fino a `r_min` (il raggio del basamento della lanterna):
    oltre quella quota il guscio e' coperto dalla lanterna e non servono
    lastre.
    """
    if r_min is None:
        r_min = R_LANTERNA_BASE * 0.93
    grezzo = profilo_calotta(r_base, z_base, z_apice, 400)
    tagliato = []
    for i, (r, z) in enumerate(grezzo):
        if r <= r_min and i > 0:
            r0, z0 = grezzo[i - 1]
            f = (r0 - r_min) / max(r0 - r, 1e-9)
            f = min(max(f, 0.0), 1.0)
            tagliato.append((r_min, z0 + (z - z0) * f))
            break
        tagliato.append((r, z))
    else:                                   # pragma: no cover - profil rari
        tagliato.append((r_min, z_apice))
    return _profilo_archi(tagliato, filari)


def _punto_meridiano(nodi, k):
    """Punto (r, z) a parametro frazionario `k` lungo il profilo."""
    k = min(max(k, 0.0), len(nodi) - 1.0)
    i = int(math.floor(k))
    if i >= len(nodi) - 1:
        return nodi[-1]
    f = k - i
    r0, z0 = nodi[i]
    r1, z1 = nodi[i + 1]
    return (r0 + (r1 - r0) * f, z0 + (z1 - z0) * f)


def _normale_meridiano(nodi, k):
    """Normale uscente nel piano del meridiano, come (nr, nz)."""
    r0, z0 = _punto_meridiano(nodi, k - 0.4)
    r1, z1 = _punto_meridiano(nodi, k + 0.4)
    dr, dz = r1 - r0, z1 - z0
    lung = math.hypot(dr, dz) or 1.0
    return dz / lung, -dr / lung


def _vertice_calotta(acc, cx, cy, nodi, k, ang, off=0.0):
    """Vertice sul guscio, spostato di `off` metri lungo la normale uscente."""
    r, z = _punto_meridiano(nodi, k)
    nr, nz = _normale_meridiano(nodi, k)
    rr = r + off * nr
    return acc.v(cx + rr * math.cos(ang), cy + rr * math.sin(ang), z + off * nz)


def _nastro_meridiano(acc, cx, cy, nodi, ang, larghezza, altezza, k0, k1):
    """Piega di giunzione che sale lungo un meridiano.

    Cinque corsie con sporgenze digradanti: al centro il colmo, ai bordi
    quota zero, cosi' il nastro e' una modanatura tonda e non una lama.
    """
    corsie = ((-1.0, 0.003), (-0.5, altezza * 0.70), (0.0, altezza),
              (0.5, altezza * 0.70), (1.0, 0.003))
    passi = max(2, int(round((k1 - k0) * 3)))
    righe = []
    for s in range(passi + 1):
        k = k0 + (k1 - k0) * s / passi
        r, _ = _punto_meridiano(nodi, k)
        hw = larghezza / 2.0 / max(r, 0.05)
        righe.append([_vertice_calotta(acc, cx, cy, nodi, k, ang + f * hw, off)
                      for f, off in corsie])
    for a, b in zip(righe, righe[1:]):
        for i in range(len(a) - 1):
            acc.faces.append((a[i], a[i + 1], b[i + 1], b[i]))


def _nastro_anello(acc, cx, cy, nodi, k, larghezza, altezza, ds, passi=192):
    """Piega orizzontale: gira intorno alla calotta a quota `k`."""
    dk = larghezza / 2.0 / max(ds, 1e-6)
    corsie = ((-1.0, 0.003), (-0.5, altezza * 0.72), (0.5, altezza * 0.72),
              (1.0, 0.003))
    righe = []
    for d, off in corsie:
        riga = []
        for p in range(passi + 1):
            ang = 2.0 * math.pi * p / passi
            riga.append(_vertice_calotta(acc, cx, cy, nodi, k + d * dk, ang, off))
        righe.append(riga)
    for a, b in zip(righe, righe[1:]):
        for i in range(passi):
            acc.faces.append((a[i], a[i + 1], b[i + 1], b[i]))


def calotta_lastre(acc_lastre, acc_giunti, acc_costoloni, cx, cy, nodi,
                   spicchi=SPICCHI, strisce=STRISCE_PER_SPICCHIO,
                   h_giunto=0.013, larg_giunto=0.072,
                   h_costa=0.086, larg_costa=0.220):
    """Guscio della calotta fatto di LASTRE, non di una superficie liscia.

    - `acc_lastre`: le piastre di piombo (una per filaro e per striscia);
    - `acc_giunti`: le pieghe di giunzione, orizzontali e verticali;
    - `acc_costoloni`: i sedici costoloni, nastri piu' larghi e piu' alti che
      salgono sui confini degli spicchi, allineati alle finestre della lanterna.

    Le lastre sono un reticolo continuo: le strisce verticali corrono dalla
    gronda alla lanterna senza sfalsamenti, come nelle fotografie, dove le
    pieghe di piombo disegnano raggi regolari.
    """
    filari = len(nodi) - 1
    passo = 2.0 * math.pi / spicchi
    sub = passo / strisce
    # Mezzo passo di baia: i costoloni cadono in mezzo alle otto finestre
    # rettangolari della lanterna e non sugli spigoli di un finto ottagono.
    ruota = math.pi / BAIE_LANTERNA
    ds = _lunghezza_profilo(nodi) / filari

    for g in range(spicchi):
        for j in range(strisce):
            a0 = ruota + g * passo + j * sub
            a1 = a0 + sub
            for k in range(filari):
                p00 = _vertice_calotta(acc_lastre, cx, cy, nodi, k, a0)
                p10 = _vertice_calotta(acc_lastre, cx, cy, nodi, k, a1)
                p11 = _vertice_calotta(acc_lastre, cx, cy, nodi, k + 1, a1)
                p01 = _vertice_calotta(acc_lastre, cx, cy, nodi, k + 1, a0)
                acc_lastre.faces.append((p00, p10, p11, p01))

    # pieghe verticali di lastra (una ogni striscia, esclusi i costoloni)
    for g in range(spicchi):
        for j in range(1, strisce):
            ang = ruota + g * passo + j * sub
            _nastro_meridiano(acc_giunti, cx, cy, nodi, ang, larg_giunto,
                              h_giunto, 0.0, float(filari))

    # pieghe orizzontali: ogni filaro e' battuto sul precedente.  Sono
    # volutamente BASSE: nelle fotografie le linee orizzontali sono appena
    # percettibili, mentre a leggersi in rilievo sono gli otto costoloni.
    for k in range(1, filari):
        _nastro_anello(acc_giunti, cx, cy, nodi, float(k), larg_giunto * 0.70,
                       h_giunto * 0.28, ds, passi=160)

    # SEDICI costoloni: nastri tondi, piu' stretti che nella v5.1 perche'
    # il passo dimezza, ma sempre piu' alti delle pieghe di giunzione.
    passo_costa = 2.0 * math.pi / COSTOLONI
    for g in range(COSTOLONI):
        ang = ruota + g * passo_costa
        _nastro_meridiano(acc_costoloni, cx, cy, nodi, ang, larg_costa,
                          h_costa, 0.0, float(filari))


def loggia(acc_para, acc_archi, acc_colonne, acc_cornice, cx, cy, raggio,
           lati, ruota, baie, z_piano, parapetto, stipite, freccia, luce,
           coppia, raggio_col, acuto, z_trabeazione, passo=0.40,
           sporgenza=0.075, allunga=0.25, campioni=15):
    """Un ordine di loggia: parapetto, parete forata, colonne, trabeazione.

    Le quote si dichiarano come in un prospetto — davanzale (`parapetto`),
    piedritti (`stipite`) e arco (`freccia`) — cosi' l'apertura risulta piu'
    alta che larga, come nelle fotografie del tamburo, invece di un arco
    schiacciato.  Sopra la corona resta un piccolo spandrelo e poi la
    trabeazione, che finisce sempre in `z_trabeazione`.
    """
    esterno = poligono(cx, cy, raggio, lati, ruota)
    interno = poligono(cx, cy, raggio - LATO_SUP, lati, ruota)
    z_sill = z_piano + parapetto
    z_imp = z_sill + stipite
    z_corona = z_imp + freccia
    z_cornice = min(z_corona + 0.22, z_trabeazione - 0.16)

    acc_para.anello(esterno, interno, z_piano, z_sill)
    acc_para.anello(poligono(cx, cy, raggio + 0.09, lati, ruota), interno,
                    z_sill - 0.09, z_sill)

    parete_arche(acc_archi, esterno, z_sill, z_cornice, LATO_SUP, baie, luce,
                 freccia, z_imp, acuto=acuto, campioni=campioni,
                 allunga=allunga)

    # I fusti partono dal piano della galleria (non dal davanzale degli
    # archi): cosi' le colonnine si vedono per tutta la loro altezza e il
    # parapetto fa solo da zoccolo fra l'una e l'altra.
    z_base_col = z_piano + min(parapetto, 0.12)
    if coppia > 0.0:
        colonne_agli_archi(acc_colonne, esterno, baie, z_base_col,
                           z_imp + 0.04, raggio_col, coppia,
                           LATO_SUP / 2.0 + sporgenza)
    else:
        colonne(acc_colonne, esterno, z_base_col, z_imp + 0.04, raggio_col,
                sporgenza=LATO_SUP / 2.0 + sporgenza)

    acc_cornice.anello(poligono(cx, cy, raggio + 0.11, lati, ruota), interno,
                       z_cornice, z_trabeazione)
    # i dentelli sono cubetti sotto la corona, non mensole alte quanto la
    # trabeazione: l'altezza si limita in proporzione allo spazio disponibile
    h_dent = min(0.11, 0.38 * (z_trabeazione - z_cornice))
    dentelli(acc_cornice, poligono(cx, cy, raggio + 0.01, lati, ruota),
             z_trabeazione - 0.09 - h_dent, z_trabeazione - 0.09,
             passo=passo * 0.62, sporgenza=0.07, larghezza=0.085,
             profondita=0.085)
    return z_sill, z_imp, z_corona, z_cornice


# -----------------------------------------------------------------------------
# 6. COSTRUZIONE
# -----------------------------------------------------------------------------
def _collezione(nome, parent=None):
    c = bpy.data.collections.get(nome)
    if c is None:
        c = bpy.data.collections.new(nome)
        (parent or bpy.context.scene.collection).children.link(c)
    return c


def rimuovi_cupola():
    """Cancella gli oggetti del gruppo cupola (idempotenza)."""
    c = bpy.data.collections.get("07d_Tiburio_e_Cupola")
    if c is None:
        return
    for o in list(c.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def _ricalcola_normali(mesh):
    import bmesh
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()


def _crea(nome, acc, materiale, col, scala, uv_sferiche=None, smooth=False,
          angolo_spigolo=34.0):
    """Trasforma un `Accumulatore` (in metri reali) in un oggetto Blender."""
    verts = [(x * scala, y * scala, z * scala) for x, y, z in acc.verts]
    mesh = bpy.data.meshes.new(nome + "Mesh")
    mesh.from_pydata(verts, [], [list(f) for f in acc.faces])
    mesh.validate(verbose=False)
    mesh.update()
    uv = mesh.uv_layers.new(name="UVMap")
    if uv_sferiche is None:
        # proiezione a scatola (come i muri esterni)
        k = 1.0 / (3.2 * max(scala, 1e-6))
        for poly in mesh.polygons:
            vs = [mesh.vertices[mesh.loops[li].vertex_index].co
                  for li in poly.loop_indices]
            xs = [v.x for v in vs]
            ys = [v.y for v in vs]
            zs = [v.z for v in vs]
            verticale = (max(zs) - min(zs)) > 1e-6
            asse_x = (max(xs) - min(xs)) >= (max(ys) - min(ys))
            for li in poly.loop_indices:
                v = mesh.vertices[mesh.loops[li].vertex_index].co
                if verticale and asse_x:
                    uv.data[li].uv = (v.x * k, v.z * k)
                elif verticale:
                    uv.data[li].uv = (v.y * k, v.z * k)
                else:
                    uv.data[li].uv = (v.x * k, v.y * k)
    else:
        for li, vindex in enumerate(mesh.loops):
            co = mesh.vertices[vindex.vertex_index].co
            uv.data[li].uv = uv_sferiche(co)
    obj = bpy.data.objects.new(nome, mesh)
    col.objects.link(obj)
    mesh.materials.append(materiale)
    _ricalcola_normali(mesh)
    if smooth:
        # facce morbide solo dove serve (nastri, tubi, volte): gli spigoli
        # vivi restano vivi, cosi' le lastre di piombo restano piane
        for f in mesh.polygons:
            f.use_smooth = True
        if hasattr(mesh, "set_sharp_from_angle"):
            mesh.set_sharp_from_angle(angle=math.radians(angolo_spigolo))
    return obj


# -----------------------------------------------------------------------------
# 7. FINESTRE RETTANGOLARI, TRAFORI E FASTIGIO DELLA LANTERNA (v5.2)
# -----------------------------------------------------------------------------
def parete_finestre_rettangolari(acc, cx, cy, raggio, lati, z0, z1,
                                 spessore, baie, luce, z_dav, z_top,
                                 ruota=0.0):
    """Parete cilindrica forata da `baie` finestre RETTANGOLARI passanti.

    Il corpo della lanterna senese non e' un ottagono: e' un cilindro (qui
    un 64-gono) con otto aperture.  Ogni apertura e' un taglio rettangolare
    nella parete, con spessore di muro e spalle verticali in muratura.
    """
    z_dav = max(z0, min(z_dav, z1))
    z_top = max(z_dav, min(z_top, z1))
    esterno = poligono(cx, cy, raggio, lati, ruota)
    interno = poligono(cx, cy, raggio - spessore, lati, ruota)
    semi_ang = min(0.42 * 2.0 * math.pi / baie,
                   1.15 * luce / (2.0 * max(raggio, 1e-6)))
    centri = [ruota + 2.0 * math.pi * (i + 0.5) / baie
              for i in range(baie)]

    def _in_finestra(ang):
        return any(abs((ang - c + math.pi) % (2.0 * math.pi) - math.pi)
                   < semi_ang for c in centri)

    dentro = []
    for j in range(lati):
        a = ruota + 2.0 * math.pi * (j + 0.5) / lati
        dentro.append(_in_finestra(a))

    def _pannello(j, za, zb):
        p0, p1 = esterno[j], esterno[(j + 1) % lati]
        q0, q1 = interno[j], interno[(j + 1) % lati]
        o0 = acc.v(p0[0], p0[1], za)
        o1 = acc.v(p1[0], p1[1], za)
        o2 = acc.v(p1[0], p1[1], zb)
        o3 = acc.v(p0[0], p0[1], zb)
        i0 = acc.v(q0[0], q0[1], za)
        i1 = acc.v(q1[0], q1[1], za)
        i2 = acc.v(q1[0], q1[1], zb)
        i3 = acc.v(q0[0], q0[1], zb)
        acc.faces.append((o0, o1, o2, o3))
        acc.faces.append((i1, i0, i3, i2))
        acc.faces.append((o3, o2, i2, i3))
        acc.faces.append((i0, i1, o1, o0))

    def _spalla(j, za, zb):
        p, q = esterno[j], interno[j]
        a = acc.v(p[0], p[1], za)
        b = acc.v(p[0], p[1], zb)
        c = acc.v(q[0], q[1], zb)
        d = acc.v(q[0], q[1], za)
        acc.faces.append((a, b, c, d))

    for j in range(lati):
        segmenti = ((z0, z_dav), (z_top, z1)) if dentro[j] else ((z0, z1),)
        for za, zb in segmenti:
            if zb - za > 1e-6:
                _pannello(j, za, zb)

    # spalle verticali delle finestre: una per ogni transizione aperto/chiuso
    for j in range(lati):
        if dentro[j] != dentro[(j - 1) % lati]:
            _spalla(j, z_dav, z_top)
    return sum(1 for x in dentro if x)


def disco_ovale(acc, centro, asse_u, asse_v, normale, ru, rv,
                spessore=0.03, lati=16):
    """Disco ovale in un piano verticale, con spessore lungo `normale`.

    Serve sia alle rosette dei trafori sia agli oculi della fascia di gronda
    della lanterna: nelle fotografie sono ovali, non cerchi perfetti.
    """
    def _unita(v):
        lung = math.sqrt(sum(q * q for q in v)) or 1.0
        return tuple(q / lung for q in v)

    ux, uy, uz = _unita(asse_u)
    vx, vy, vz = _unita(asse_v)
    nx, ny, nz = _unita(normale)
    cx, cy, cz = centro
    h = spessore / 2.0
    fronte, retro = [], []
    for k in range(lati):
        a = 2.0 * math.pi * k / lati
        du, dv = ru * math.cos(a), rv * math.sin(a)
        px = cx + ux * du + vx * dv
        py = cy + uy * du + vy * dv
        pz = cz + uz * du + vz * dv
        fronte.append(acc.v(px - nx * h, py - ny * h, pz - nz * h))
        retro.append(acc.v(px + nx * h, py + ny * h, pz + nz * h))
    acc.faces.append(tuple(fronte))
    acc.faces.append(tuple(reversed(retro)))
    for k in range(lati):
        j = (k + 1) % lati
        acc.faces.append((fronte[k], fronte[j], retro[j], retro[k]))


def traforo_finestra(acc, cx, cy, raggio, baie, luce, z_dav, z_top,
                     ruota=0.0):
    """Montanti e traversi in pietra delle otto finestre rettangolari."""
    h = z_top - z_dav
    for i in range(baie):
        am = ruota + 2.0 * math.pi * (i + 0.5) / baie
        ux, uy = -math.sin(am), math.cos(am)
        ca, sa = math.cos(am), math.sin(am)
        r = raggio - 0.10
        px, py = cx + r * ca, cy + r * sa
        # due montanti -> tre luci verticali
        for u in (-luce / 6.0, luce / 6.0):
            acc.scatola(px + ux * u, py + uy * u, z_dav + h / 2.0,
                        ux, uy, 0.055, 0.070, h)
        # due traversi -> tre registri orizzontali
        for f in (0.38, 0.72):
            acc.scatola(px, py, z_dav + h * f, ux, uy,
                        luce, 0.070, 0.055)


def rosette_finestre(acc, cx, cy, raggio, baie, luce, z_dav, z_top,
                     ruota=0.0):
    """Piccole rosette ovali nel registro alto di ogni finestra."""
    h = z_top - z_dav
    for i in range(baie):
        am = ruota + 2.0 * math.pi * (i + 0.5) / baie
        ux, uy = -math.sin(am), math.cos(am)
        ca, sa = math.cos(am), math.sin(am)
        r = raggio - 0.10
        px, py = cx + r * ca, cy + r * sa
        for u in (-luce / 3.0, 0.0, luce / 3.0):
            disco_ovale(acc,
                        (px + ux * u, py + uy * u, z_dav + h * 0.86),
                        (ux, uy, 0.0), (0.0, 0.0, 1.0), (ca, sa, 0.0),
                        0.075, 0.098, 0.020, 12)


def stella_oro(acc, cx, cy, z, raggio, punte=8, spessore=0.055):
    """Stella d'oro sfaccettata: raggi piramidali su due piani incrociati."""
    r_in = raggio * 0.30
    delta = math.pi / punte * 0.78
    # nucleo a bassa poligonizzazione: si legge come una stella di lamiera
    prof = []
    for k in range(9):
        phi = -math.pi / 2.0 + math.pi * k / 8.0
        prof.append((z + raggio * 0.26 * math.sin(phi),
                     raggio * 0.26 * math.cos(phi)))
    acc.rivoluzione(cx, cy, prof, seg=12)
    for piano in (0, 1):
        for k in range(punte):
            a = math.pi / 2.0 + 2.0 * math.pi * k / punte
            if piano == 0:
                f = acc.v(cx, cy - spessore, z)
                b = acc.v(cx, cy + spessore, z)
                tip = acc.v(cx + raggio * math.cos(a), cy,
                            z + raggio * math.sin(a))
                s1 = acc.v(cx + r_in * math.cos(a - delta), cy,
                           z + r_in * math.sin(a - delta))
                s2 = acc.v(cx + r_in * math.cos(a + delta), cy,
                           z + r_in * math.sin(a + delta))
            else:
                f = acc.v(cx - spessore, cy, z)
                b = acc.v(cx + spessore, cy, z)
                tip = acc.v(cx, cy + raggio * math.cos(a),
                            z + raggio * math.sin(a))
                s1 = acc.v(cx, cy + r_in * math.cos(a - delta),
                           z + r_in * math.sin(a - delta))
                s2 = acc.v(cx, cy + r_in * math.cos(a + delta),
                           z + r_in * math.sin(a + delta))
            acc.faces.extend(((f, s1, tip), (f, tip, s2),
                              (b, tip, s1), (b, s2, tip),
                              (f, s2, s1), (b, s1, s2)))


def costruisci_lanterna(mats, col, scala, cx, cy, z0, h_cupola):
    """Lanterna del Bernini (1667), v5.2: corpo circolare e fastigio rifatto.

    Rispetto alla v5.1 il corpo non e' piu' un ottagono con archi acuti ma
    un cilindro a 64 facce con OTTO finestre rettangolari traforate; il tetto
    e' una copertura concava a OTTO LOBI; mela, stella e segnavento sono
    volumi sfaccettati.  La punta del segnavento resta a `h_cupola` (48 m).
    """
    creati = []
    R = R_LANTERNA
    ri = R - LATO_LANTERNA
    lati = LATI_CORPO_LANTERNA
    ruota = math.pi / BAIE_LANTERNA
    luce = 1.18

    z_dav = z0 + L_DAVANZALE
    z_imp = z0 + L_IMPOSTA
    z_top = z_imp + L_ARCHI
    z_corona = z0 + L_CORONA
    z_trab = z0 + L_TRABEAZIONE
    z_gronda = z0 + L_GRONDA
    z_tetto = z0 + L_TETTO
    z_vaso = z0 + L_VASO
    z_mela = z0 + L_MELA
    z_stella = z0 + L_STELLA

    def _p(r_, extra=0.0, n=None):
        return poligono(cx, cy, r_ + extra, n or lati, ruota)

    def _centro_finestra(i):
        return ruota + 2.0 * math.pi * (i + 0.5) / BAIE_LANTERNA

    # 1) basamento a risalti: raccorda la calotta al tempietto
    acc = Accumulatore()
    z = z0 - 0.42
    for r_out, dz in ((R_LANTERNA_BASE + 0.28, 0.14),
                      (R_LANTERNA_BASE + 0.06, 0.13),
                      (R_LANTERNA_BASE - 0.16, 0.15)):
        acc.anello(poligono(cx, cy, r_out, 64),
                   poligono(cx, cy, R - 0.06, 64), z, z + dz)
        z += dz
    acc.anello(_p(R, extra=0.14), _p(R, extra=-0.06), z, z + 0.05)
    creati.append(_crea("Lanterna_Basamento", acc, mats["cornice"], col, scala))

    # 2) dado, zoccolo e davanzale delle finestre
    acc = Accumulatore()
    acc.anello(_p(R, extra=0.05), _p(ri), z0 + 0.10, z0 + L_ZOCOLO)
    acc.anello(_p(R, extra=0.13), _p(ri), z_dav - 0.11, z_dav)
    creati.append(_crea("Lanterna_Zoccolo", acc, mats["marmo"], col, scala))

    # 3) vano interno in ombra
    acc = Accumulatore()
    acc.canna(_p(ri - 0.05), z_dav - 0.40, z_corona + 0.06)
    acc.anello(_p(ri - 0.01), poligono(cx, cy, 0.24, 64, ruota),
               z_dav - 0.20, z_dav - 0.14)
    creati.append(_crea("Lanterna_Interno", acc, mats["interno"], col, scala))

    # 4) corpo finestrato: otto aperture rettangolari passanti
    acc = Accumulatore()
    parete_finestre_rettangolari(acc, cx, cy, R, lati,
                                 z_dav - 0.10, z_corona,
                                 LATO_LANTERNA, BAIE_LANTERNA, luce,
                                 z_dav, z_top, ruota)
    creati.append(_crea("Lanterna_Pareti", acc, mats["marmo"], col, scala))

    # 4b) cornici modanate rettangolari intorno alle finestre
    acc = Accumulatore()
    for i in range(BAIE_LANTERNA):
        am = _centro_finestra(i)
        ux, uy = -math.sin(am), math.cos(am)
        ca, sa = math.cos(am), math.sin(am)
        px, py = cx + (R + 0.012) * ca, cy + (R + 0.012) * sa
        for s in (-1.0, 1.0):
            u = s * (luce / 2.0 + 0.055)
            acc.scatola(px + ux * u, py + uy * u,
                        (z_dav + z_top) / 2.0, ux, uy,
                        0.075, 0.085, z_top - z_dav + 0.12)
        for zz in (z_dav - 0.045, z_top + 0.045):
            acc.scatola(px, py, zz, ux, uy, luce + 0.19, 0.085, 0.075)
    creati.append(_crea("Lanterna_Cornici_Finestre", acc, mats["cornice"],
                        col, scala))

    # 4c) trafori in pietra: montanti, traversi e rosette ovali
    acc = Accumulatore()
    traforo_finestra(acc, cx, cy, R, BAIE_LANTERNA, luce, z_dav, z_top, ruota)
    creati.append(_crea("Lanterna_Trafori_Finestre", acc, mats["cornice"],
                        col, scala))

    acc = Accumulatore()
    rosette_finestre(acc, cx, cy, R, BAIE_LANTERNA, luce, z_dav, z_top, ruota)
    creati.append(_crea("Lanterna_Rosette_Ovali", acc, mats["ferro"],
                        col, scala))

    # 5) colonnine binate sugli stipiti delle otto finestre
    acc = Accumulatore()
    for i in range(BAIE_LANTERNA):
        am = _centro_finestra(i)
        for s in (-1.0, 1.0):
            ang = am + s * (luce / (2.0 * R) + 0.09)
            px = cx + (R + 0.045) * math.cos(ang)
            py = cy + (R + 0.045) * math.sin(ang)
            acc.cilindro(px, py, z_dav - 0.10, z_dav - 0.035,
                         0.105, seg=12)
            acc.cilindro(px, py, z_dav - 0.035, z_imp - 0.05,
                         0.072, seg=12, raggio_alto=0.066)
            acc.cilindro(px, py, z_imp - 0.05, z_imp + 0.03,
                         0.105, seg=12)
    creati.append(_crea("Lanterna_Colonne", acc, mats["cornice"], col, scala))

    # 6) grate in ferro delle finestre rettangolari
    acc = Accumulatore()
    for i in range(BAIE_LANTERNA):
        am = _centro_finestra(i)
        ux, uy = -math.sin(am), math.cos(am)
        ca, sa = math.cos(am), math.sin(am)
        px, py = cx + (R - 0.16) * ca, cy + (R - 0.16) * sa
        for k in range(5):
            u = -luce / 2.0 + 0.08 + (luce - 0.16) * k / 4.0
            acc.cilindro(px + ux * u, py + uy * u,
                         z_dav + 0.02, z_top - 0.02, 0.013, seg=6)
        for f in (0.22, 0.48, 0.76):
            z = z_dav + (z_top - z_dav) * f
            acc.tubo3d([(px - ux * (luce / 2.0 - 0.03),
                         py - uy * (luce / 2.0 - 0.03), z),
                        (px + ux * (luce / 2.0 - 0.03),
                         py + uy * (luce / 2.0 - 0.03), z)], 0.011, seg=6)
    creati.append(_crea("Lanterna_Grate", acc, mats["ferro"], col, scala))

    # 7) chiavi e cornice a mensole
    acc = Accumulatore()
    for i in range(BAIE_LANTERNA):
        am = _centro_finestra(i)
        ux, uy = -math.sin(am), math.cos(am)
        ca, sa = math.cos(am), math.sin(am)
        acc.scatola(cx + (R + 0.02) * ca, cy + (R + 0.02) * sa,
                    z_top + 0.09, ux, uy, 0.17, 0.10, 0.22)
    creati.append(_crea("Lanterna_Chiavi", acc, mats["cornice"], col, scala))

    acc = Accumulatore()
    acc.anello(_p(R, extra=0.06), _p(ri), z_corona, z_corona + 0.10)
    dentelli(acc, _p(R, extra=0.02), z_corona + 0.10, z_corona + 0.24,
             passo=0.24, sporgenza=0.12, larghezza=0.10, profondita=0.10)
    acc.anello(_p(R, extra=0.26), _p(R, extra=-0.08),
               z_corona + 0.24, z_trab)
    creati.append(_crea("Lanterna_Trabeazione", acc, mats["cornice"],
                        col, scala))

    # 8) fascia in piombo con gli oculi ovali
    acc = Accumulatore()
    anelli = []
    for f, dz in ((0.0, 0.0), (0.35, 0.14), (0.70, 0.28), (1.0, 0.44)):
        r = R + 0.20 + 0.34 * f
        anelli.append((acc.poligono(poligono(cx, cy, r, 64), z_trab + dz),
                       acc.poligono(poligono(cx, cy, r - 0.12, 64),
                                    z_trab + dz + 0.02)))
    for (a0, b0), (a1, b1) in zip(anelli, anelli[1:]):
        for i in range(64):
            j = (i + 1) % 64
            acc.faces.append((a0[i], a0[j], a1[j], a1[i]))
            acc.faces.append((b1[i], b1[j], b0[j], b0[i]))
    a0, b0 = anelli[-1]
    a1, b1 = anelli[0]
    for i in range(64):
        j = (i + 1) % 64
        acc.faces.append((a0[i], a0[j], b0[j], b0[i]))
        acc.faces.append((a1[j], a1[i], b1[i], b1[j]))
    creati.append(_crea("Lanterna_Fascia_Piombo", acc, mats["piombo"],
                        col, scala, smooth=True, angolo_spigolo=30.0))

    acc = Accumulatore()
    for i in range(16):
        ang = ruota + 2.0 * math.pi * i / 16.0
        ca, sa = math.cos(ang), math.sin(ang)
        disco_ovale(acc,
                    (cx + (R + 0.34) * ca, cy + (R + 0.34) * sa,
                     z_trab + 0.22),
                    (-sa, ca, 0.0), (0.0, 0.0, 1.0), (ca, sa, 0.0),
                    0.125, 0.082, 0.060, 16)
    creati.append(_crea("Lanterna_Oculi_Ovali", acc, mats["ferro"],
                        col, scala))

    # 9) tetto concavo a OTTO LOBI in lastre di piombo
    z_gr = z_gronda - 0.03
    r_gr = R + 0.34
    nodi_tetto = [(0.00, 1.000), (0.04, 0.960), (0.12, 0.820),
                  (0.25, 0.620), (0.40, 0.440), (0.55, 0.300),
                  (0.70, 0.190), (0.85, 0.105), (0.94, 0.055),
                  (1.00, 0.000)]
    passi = 36

    def _r_lobo(t, ang):
        r = r_gr * _interp(nodi_tetto, t)
        # otto lobi: il colmo e' in asse con le finestre, l'avvallamento
        # fra finestra e finestra; l'ampiezza si annulla all'apice
        ampiezza = 0.055 * (1.0 - t) ** 0.55
        return r * (1.0 - ampiezza *
                    math.cos(BAIE_LANTERNA * (ang - ruota)))

    acc = Accumulatore()
    anelli = []
    for k in range(passi):
        t = k / float(passi)
        z = z_gr + (z_tetto - z_gr) * t
        riga = []
        for i in range(lati):
            ang = ruota + 2.0 * math.pi * i / lati
            r = _r_lobo(t, ang)
            riga.append(acc.v(cx + r * math.cos(ang),
                              cy + r * math.sin(ang), z))
        anelli.append(riga)
    apice = acc.v(cx, cy, z_tetto)
    for a, b in zip(anelli, anelli[1:]):
        for i in range(lati):
            j = (i + 1) % lati
            acc.faces.append((a[i], a[j], b[j], b[i]))
    for i in range(lati):
        j = (i + 1) % lati
        acc.faces.append((anelli[-1][i], anelli[-1][j], apice))
    acc.faces.append(tuple(reversed(anelli[0])))
    creati.append(_crea("Lanterna_Tetto", acc, mats["piombo"], col, scala,
                        smooth=True, angolo_spigolo=40.0))

    # colmi di piombo: due per lobo (sedici in tutto)
    acc = Accumulatore()
    for i in range(COSTOLONI):
        ang = ruota + 2.0 * math.pi * i / COSTOLONI
        pts, raggi = [], []
        for k in range(passi):
            t = k / float(passi)
            r = _r_lobo(t, ang)
            if r < 0.30:
                break
            pts.append((r + 0.014, z_gr + (z_tetto - z_gr) * t, ang))
            raggi.append(0.055 - 0.027 * t)
        if len(pts) > 1:
            acc.tubo(pts, raggi, seg=8, cx=cx, cy=cy)
    creati.append(_crea("Lanterna_Colmi_Tetto", acc, mats["piombo_costa"],
                        col, scala, smooth=True, angolo_spigolo=60.0))

    acc = Accumulatore()
    acc.anello(poligono(cx, cy, r_gr + 0.06, 64, ruota),
               poligono(cx, cy, r_gr - 0.14, 64, ruota),
               z_gr - 0.11, z_gr + 0.06)
    creati.append(_crea("Lanterna_Gronda_Tetto", acc, mats["piombo_costa"],
                        col, scala))

    # 10) vaso lapideo a risalti sopra il colmo
    z_fin = z_tetto - 0.04
    h_vaso = max(z_vaso - z_fin, 0.20)
    forma = [(0.00, 0.42), (0.08, 0.62), (0.20, 0.62), (0.26, 0.40),
             (0.42, 0.40), (0.48, 0.56), (0.60, 0.56), (0.66, 0.34),
             (0.80, 0.24), (0.90, 0.30), (1.00, 0.22)]
    profilo_vaso = [(z_fin + h_vaso * f, 0.46 * r) for f, r in forma]
    acc = Accumulatore()
    acc.rivoluzione(cx, cy, profilo_vaso, seg=20)
    creati.append(_crea("Lanterna_Vaso", acc, mats["cornice"], col, scala,
                        smooth=True, angolo_spigolo=46.0))

    # 11) mela dorata SFACCETTATA, con gambo e fascia equatoriale
    acc = Accumulatore()
    acc.cilindro(cx, cy, z_vaso - 0.04, z_mela - R_MELA * 0.82,
                 0.075, seg=12, raggio_alto=0.055)
    prof = []
    for k in range(13):
        a = -math.pi / 2.0 + math.pi * k / 12.0
        prof.append((z_mela + R_MELA * 0.98 * math.sin(a),
                     R_MELA * 0.98 * math.cos(a)))
    acc.rivoluzione(cx, cy, prof, seg=20)
    acc.anello(poligono(cx, cy, R_MELA * 1.02, 20),
               poligono(cx, cy, R_MELA * 0.97, 20),
               z_mela - 0.035, z_mela + 0.035)
    creati.append(_crea("Lanterna_Mela_Dorata", acc, mats["oro"], col, scala))

    # 12) stella d'oro a raggi piramidali
    acc = Accumulatore()
    stella_oro(acc, cx, cy, z_stella, R_STELLA, punte=8, spessore=0.055)
    creati.append(_crea("Lanterna_Stella_Dorata", acc, mats["oro"], col, scala))

    # 13) segnavento: asta e bandiera a fiamma, punta esattamente a 48 m
    z_base_asta = z_stella + R_STELLA * 0.55
    h_pennello = 0.30
    z_pennello = h_cupola - h_pennello
    acc = Accumulatore()
    acc.cilindro(cx, cy, z_base_asta, z_pennello + 0.02,
                 0.016, seg=8, raggio_alto=0.009)
    acc.cilindro(cx, cy, z_pennello - 0.03, z_pennello + 0.03,
                 0.027, seg=10)
    creati.append(_crea("Lanterna_Segnavento_Asta", acc, mats["oro"],
                        col, scala, smooth=True, angolo_spigolo=60.0))

    acc = Accumulatore()
    sagoma = [(0.000, 0.000), (0.110, 0.060), (0.030, 0.130),
              (0.150, 0.210), (0.000, 0.300), (-0.040, 0.210),
              (-0.120, 0.130), (-0.030, 0.060)]
    fronte, retro = [], []
    for dx, dz in sagoma:
        fronte.append(acc.v(cx + dx, cy - 0.010, z_pennello + dz))
        retro.append(acc.v(cx + dx, cy + 0.010, z_pennello + dz))
    acc.faces.append(tuple(fronte))
    acc.faces.append(tuple(reversed(retro)))
    for k in range(len(sagoma)):
        j = (k + 1) % len(sagoma)
        acc.faces.append((fronte[k], fronte[j], retro[j], retro[k]))
    creati.append(_crea("Lanterna_Segnavento_Bandiera", acc, mats["oro"],
                        col, scala))
    return creati

def costruisci_cupola(scala=3.0, cfg=None, col=None, cx=None, cy=None):
    """Ricostruisce tiburio, calotta e lanterna nella raccolta 07d*.

    Ritorna un dizionario con il numero di oggetti e le quote usate.
    """
    opt = dict(cfg or {})
    h_attico_base = float(opt.get("altezza_tamburo_base", H_ATTICO_BASE))
    h_cleristorio = float(opt.get("altezza_cleristorio", 21.80))
    h_cupola = float(opt.get("altezza_cupola", H_CUPOLA))
    # La quota dell'apice puo' arrivare dal config, ma il fastigio della
    # lanterna (mela, stella, croce) le sta sopra: se l'apice fosse piu' alto
    # di H_CALOTTA la stella sfonderebbe la croce.  L'apice viene quindi
    # limitato, e la lanterna parte SEMPRE dalla quota effettiva del guscio.
    # Il margine sopra la stella deve bastare all'asta e alla bandiera del
    # segnavento; con L_STELLA + R_STELLA + 0,10 = 8,70 m l'apice ufficiale
    # di 39,20 m resta disponibile (48 - 8,70 = 39,30 m).
    h_apice_calotta = min(float(opt.get("altezza_calotta", H_CALOTTA)),
                          h_cupola - (L_STELLA + R_STELLA + 0.10))

    mats = _materiali(scala)

    if col is None:
        root = _collezione("07_Corpo_Chiesa")
        col = _collezione("07d_Tiburio_e_Cupola", root)

    # Il centro del tiburio e' lo stesso esagono della crociera: arriva da
    # `muri_esterni` se disponibile.
    if cx is None or cy is None:
        try:
            from muri_esterni import ESAGONO_M
            cx, cy = ESAGONO_M
        except Exception:  # pragma: no cover
            cx, cy = (5.6, 45.0)

    ruota_sup = math.pi / LATI_LOGGE_SUP
    esagono = poligono(cx, cy, R_ATTICO, 6)
    inf = poligono(cx, cy, R_LOGGE_INF, LATI_LOGGE_INF, math.pi / LATI_LOGGE_INF)
    sup = poligono(cx, cy, R_LOGGE_SUP, LATI_LOGGE_SUP, ruota_sup)
    canna = poligono(cx, cy, R_LOGGE_INF - 1.70, LATI_LOGGE_INF,
                     math.pi / LATI_LOGGE_INF)

    creati = []

    # --- 6.1 attico esagonale bicromo ------------------------------------
    # Il piede scende fino al filo del cleristorio (dentro il volume della
    # crociera): cosi' fra tetto e tiburio non resta nessuna fessura di luce,
    # lo stesso accorgimento della v4.4.
    z_attico = min(h_attico_base, h_cleristorio)
    acc = Accumulatore()
    acc.prisma(esagono, z_attico, H_ATTICO_TOP)
    creati.append(_crea("Tamburo_Attico_Esagonale", acc, mats["marmo"], col,
                        scala))

    acc = Accumulatore()
    for z in (h_attico_base + 0.28, h_attico_base + 0.88):
        acc.anello(poligono(cx, cy, R_ATTICO + 0.045, 6),
                   poligono(cx, cy, R_ATTICO - 0.10, 6), z, z + SPESSORE_FASCIA)
    creati.append(_crea("Tamburo_Attico_Fasce", acc, mats["scuro"], col, scala))

    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_ATTICO + 0.20, 6),
               poligono(cx, cy, R_LOGGE_INF - LATO_SUP / 2.0, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               H_ATTICO_TOP, H_ATTICO_TOP + 0.20)
    creati.append(_crea("Tamburo_Cornice_Atto", acc, mats["cornice"], col,
                        scala))

    # --- 6.2 loggia inferiore: parapetto, archi acuti, colonne binate --
    # Due baie per lato (48 archi in tutto): passo 1.45 m con luce 0.78 m e
    # apertura alta 1.12 m, quindi archi snelli come nelle fotografie.
    acc_para, acc_archi, acc_col, acc_corn = (Accumulatore() for _ in range(4))
    z_sill_inf, z_imp_inf, z_corona_inf, z_corn_inf = loggia(
        acc_para, acc_archi, acc_col, acc_corn,
        cx, cy, R_LOGGE_INF, LATI_LOGGE_INF, math.pi / LATI_LOGGE_INF,
        BAIE_LOGGE_INF, H_LOGGE_INF_BASE,
        0.18, 0.65, 1.35, 0.80, 0.092, 0.062, True, H_LOGGE_INF_TOP,
        passo=0.38)
    creati.append(_crea("Tamburo_LoggiaInferiore_Parapetto", acc_para,
                        mats["marmo"], col, scala))
    creati.append(_crea("Tamburo_LoggiaInferiore_Archi", acc_archi,
                        mats["marmo"], col, scala))
    creati.append(_crea("Tamburo_LoggiaInferiore_Colonne", acc_col,
                        mats["cornice"], col, scala))
    creati.append(_crea("Tamburo_LoggiaInferiore_Cornice", acc_corn,
                        mats["cornice"], col, scala))

    # --- 6.3 fascia bicroma a rombi fra i due ordini --------------------
    r_fascia = R_LOGGE_INF - 0.25
    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LOGGE_INF + 0.16, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               poligono(cx, cy, r_fascia, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               H_LOGGE_INF_TOP, H_LOGGE_INF_TOP + 0.16)
    acc.anello(poligono(cx, cy, r_fascia, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               poligono(cx, cy, r_fascia - 0.58, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               H_LOGGE_INF_TOP + 0.16, H_LOGGE_SUP_BASE)
    acc.anello(poligono(cx, cy, r_fascia + 0.24, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               poligono(cx, cy, R_LOGGE_SUP - 0.10, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               H_LOGGE_SUP_BASE - 0.16, H_LOGGE_SUP_BASE)
    creati.append(_crea("Tamburo_Fascia_Bicroma", acc, mats["marmo"], col,
                        scala))

    # rombi di serpentino su fondo bianco: il tassello e' un quadrato ruotato
    # di 45 gradi nella faccia della parete, come nel fregio senese
    acc = Accumulatore()
    apotema = r_fascia * math.cos(math.pi / LATI_LOGGE_INF) - 0.02
    z_rombo = (H_LOGGE_INF_TOP + 0.16 + H_LOGGE_SUP_BASE - 0.16) / 2.0
    lati_rombi = 72
    for i in range(lati_rombi):
        ang = 2.0 * math.pi * i / lati_rombi
        acc.rombo(cx + apotema * math.cos(ang), cy + apotema * math.sin(ang),
                  z_rombo, -math.sin(ang), math.cos(ang),
                  0.62, 0.72, 0.11)
    dentelli(acc, poligono(cx, cy, r_fascia + 0.02, LATI_LOGGE_INF,
                           math.pi / LATI_LOGGE_INF),
             H_LOGGE_SUP_BASE - 0.30, H_LOGGE_SUP_BASE - 0.18, passo=0.30,
             sporgenza=0.08, larghezza=0.11, profondita=0.09)
    creati.append(_crea("Tamburo_Fascia_Rombi", acc, mats["scuro"], col, scala))

    # --- 6.4 loggetta superiore -----------------------------------------
    # Due archetti per lato (48): passo 1,35 m come nella fotografia, non i
    # 72 archetti troppo fitti della v5.1.
    ruota_sup = math.pi / LATI_LOGGE_SUP
    acc_para, acc_archi, acc_col, acc_corn = (Accumulatore() for _ in range(4))
    z_sill_sup, z_imp_sup, z_corona_sup, z_corn_sup = loggia(
        acc_para, acc_archi, acc_col, acc_corn,
        cx, cy, R_LOGGE_SUP, LATI_LOGGE_SUP, ruota_sup,
        BAIE_LOGGE_SUP, H_LOGGE_SUP_BASE,
        0.20, 0.26, 0.62, 0.52, 0.048, 0.042, False, H_LOGGE_SUP_TOP,
        passo=0.30, sporgenza=0.06, allunga=0.16, campioni=11)
    creati.append(_crea("Tamburo_LoggiaSuperiore_Parapetto", acc_para,
                        mats["marmo"], col, scala))
    creati.append(_crea("Tamburo_LoggiaSuperiore_Archi", acc_archi,
                        mats["marmo"], col, scala))
    creati.append(_crea("Tamburo_LoggiaSuperiore_Colonne", acc_col,
                        mats["cornice"], col, scala))
    creati.append(_crea("Tamburo_LoggiaSuperiore_Cornice", acc_corn,
                        mats["cornice"], col, scala))

    # --- 6.5 canna interna, pavimenti e cielo delle gallerie ------------
    acc = Accumulatore()
    acc.canna(canna, H_LOGGE_INF_BASE, H_LOGGE_SUP_TOP - 0.08)
    creati.append(_crea("Tamburo_Canna_Interna", acc, mats["interno"], col,
                        scala))

    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LOGGE_INF - 0.25, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               poligono(cx, cy, R_LOGGE_INF - 1.66, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               H_LOGGE_INF_BASE, H_LOGGE_INF_BASE + 0.05)
    acc.anello(poligono(cx, cy, R_LOGGE_INF - 0.25, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               poligono(cx, cy, R_LOGGE_INF - 1.66, LATI_LOGGE_INF,
                        math.pi / LATI_LOGGE_INF),
               z_sill_sup - 0.05, z_sill_sup)
    creati.append(_crea("Tamburo_Gallerie_Pavimenti", acc, mats["interno"], col,
                        scala))

    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LOGGE_SUP - 0.05, LATI_LOGGE_SUP, ruota_sup),
               poligono(cx, cy, R_LOGGE_SUP - 1.70, LATI_LOGGE_SUP, ruota_sup),
               H_LOGGE_SUP_TOP - 0.09, H_LOGGE_SUP_TOP - 0.01)
    creati.append(_crea("Tamburo_Gallerie_Cielo", acc, mats["interno"], col,
                        scala))

    # ringhiera in ferro della galleria inferiore (dettaglio delle foto)
    acc = Accumulatore()
    for i in range(60):
        ang = 2.0 * math.pi * i / 60
        r = R_LOGGE_INF - 0.45
        acc.cilindro(cx + r * math.cos(ang), cy + r * math.sin(ang),
                     z_sill_inf, z_sill_inf + 0.72, 0.018, seg=5)
    acc.anello(poligono(cx, cy, R_LOGGE_INF - 0.42, 60),
               poligono(cx, cy, R_LOGGE_INF - 0.48, 60),
               z_sill_inf + 0.70, z_sill_inf + 0.75)
    creati.append(_crea("Tamburo_Gallerie_Ringhiera", acc, mats["ferro"], col,
                        scala))

    # --- 6.6 corona e ghiaccio di gronda della calotta ------------------
    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LOGGE_SUP + 0.26, 36),
               poligono(cx, cy, R_LOGGE_SUP - LATO_SUP, 36),
               H_LOGGE_SUP_TOP, H_CALOTTA_BASE - 0.22)
    dentelli(acc, poligono(cx, cy, R_LOGGE_SUP + 0.26, 36),
             H_LOGGE_SUP_TOP + 0.02, H_LOGGE_SUP_TOP + 0.14, passo=0.30,
             sporgenza=0.07, larghezza=0.10, profondita=0.09)
    creati.append(_crea("Cupola_Corona", acc, mats["cornice"], col, scala))

    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_GRONDA, 72),
               poligono(cx, cy, R_CALOTTA - 0.30, 72),
               H_CALOTTA_BASE - 0.22, H_CALOTTA_BASE)
    creati.append(_crea("Cupola_Ghiaccio_di_Gronda", acc, mats["piombo"], col,
                        scala))

    # linguette di piombo battute sul bordo della gronda: 64 tasselli
    # trapezoidali, uno ogni quarto di costolone
    acc = Accumulatore()
    n_lingue = COSTOLONI * 4
    passo_l = 2.0 * math.pi / n_lingue
    for i in range(n_lingue):
        a0 = math.pi / BAIE_LANTERNA + i * passo_l
        a1 = a0 + passo_l * 0.72
        r0, r1 = R_GRONDA - 0.03, R_GRONDA + 0.13
        poly = [(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)),
                (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)),
                (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)),
                (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))]
        acc.prisma(poly, H_CALOTTA_BASE - 0.23, H_CALOTTA_BASE + 0.05)
    creati.append(_crea("Cupola_Gronda_Linguette", acc,
                        mats["piombo_costa"], col, scala))

    # --- 6.7 calotta: 768 lastre di piombo, giunti e 16 costoloni --------
    nodi = profilo_calotta_lastre(R_CALOTTA, H_CALOTTA_BASE, h_apice_calotta)
    acc_lastre, acc_giunti, acc_coste = (Accumulatore() for _ in range(3))
    calotta_lastre(acc_lastre, acc_giunti, acc_coste, cx, cy, nodi)
    creati.append(_crea("Cupola_Lastre", acc_lastre, mats["piombo"], col,
                        scala))
    creati.append(_crea("Cupola_Giunti_Lastre", acc_giunti,
                        mats["giunti"], col, scala, smooth=True,
                        angolo_spigolo=52.0))
    creati.append(_crea("Cupola_Costoloni", acc_coste, mats["piombo_costa"],
                        col, scala, smooth=True, angolo_spigolo=52.0))

    # calottina cieca fra l'ultimo filaro e la lanterna: sta sotto il
    # basamento della lanterna, quindi non si vede, ma chiude il guscio
    acc = Accumulatore()
    r_fine, z_fine = nodi[-1]
    anelli = []
    lati_cap = 48
    for f in (0.0, 0.35, 0.62, 0.82, 0.95):
        r = r_fine * (1.0 - f)
        z = z_fine + (h_apice_calotta - z_fine) * f
        anelli.append([acc.v(cx + r * math.cos(2.0 * math.pi * i / lati_cap),
                             cy + r * math.sin(2.0 * math.pi * i / lati_cap), z)
                       for i in range(lati_cap)])
    apice = acc.v(cx, cy, h_apice_calotta)
    for a, b in zip(anelli, anelli[1:]):
        for i in range(lati_cap):
            j = (i + 1) % lati_cap
            acc.faces.append((a[i], a[j], b[j], b[i]))
    for i in range(lati_cap):
        acc.faces.append((anelli[-1][i], anelli[-1][(i + 1) % lati_cap], apice))
    creati.append(_crea("Cupola_Calottina", acc, mats["piombo"], col, scala))

    # --- 6.8 lanterna del Bernini ---------------------------------------
    creati.extend(costruisci_lanterna(mats, col, scala, cx, cy,
                                      h_apice_calotta, h_cupola))

    print("=" * 72)
    print("CUPOLA v5.2 — calotta ogivale a 768 lastre, 16 costoloni, "
          "lanterna a 8 lobi")
    print("=" * 72)
    for k, v in quote(h_apice_calotta).items():
        print(f"  {k:<44s} {v:>8.2f}")
    print(f"  oggetti creati: {len(creati)}")
    print("=" * 72)

    return {"oggetti": len(creati), "collezione": col.name,
            "quote": quote(h_apice_calotta),
            "vertici": sum(len(o.data.vertices) for o in creati)}


def quote(apice=None):
    """Quote del gruppo cupola, in metri reali (per il riepilogo)."""
    apice = H_CALOTTA if apice is None else apice
    return {
        "Piede del tiburio": H_ATTICO_BASE,
        "Sommita delle due logge [m]": H_LOGGE_SUP_TOP,
        "Imposta della calotta [m]": H_CALOTTA_BASE,
        "Apice della calotta / lanterna [m]": apice,
        "Punta della croce [m]": H_CUPOLA,
        "Freccia della calotta [m]": apice - H_CALOTTA_BASE,
        "Sommita del tetto della lanterna [m]": apice + L_TETTO,
        "Mela dorata (centro) [m]": apice + L_MELA,
        "Rapporto freccia/diametro": (apice - H_CALOTTA_BASE) /
                                     (2.0 * R_CALOTTA),
    }
