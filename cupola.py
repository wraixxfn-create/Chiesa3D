#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIBURIO, CALOTTA E LANTERNA DEL DUOMO DI SIENA (v5.0)
=====================================================

Sostituisce la vecchia cupola "a campana liscia" di `muri_esterni.py` con il
gruppo tiburio-cupola disegnato sulle quattro fotografie allegate:

    riferimento_cupola.jpg            vista d'insieme dal Facciatone
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
3. CALOTTA con profilo calibrato sulle fotografie (freccia / diametro 0,34,
   prima era un emisfero schiacciato), otto costoloni in rilievo come nella
   cupola reale e LASTRE di piombo con giunti veri: le UV sono sferiche
   (u = giro, v = meridiano, un modulo per lastra) e il materiale disegna i
   riquadri con una Brick Texture, con colature di ruggine.
4. LANTERNA del Bernini (1667) leggibile: ottagono su basamento, bifore con
   colonnine, colonne binate ai cantonali, trabeazione a dentelli, tetto a
   padiglione in piombo con costoloni, pinnacolo lapideo a tornio, MELA
   dorata a coste, stella a dodici punte e croce.
5. Le quote ufficiali non cambiano: 48 m alla punta della croce, calotta
   impostata a 32,05 m.  La facciata (37,5 m) non viene toccata.

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
H_CALOTTA = 40.40         # apice della calotta = imposta della lanterna
H_LANTERNA_BASE = 40.40
H_CUPOLA = 48.00          # punta della croce (quota ufficiale)

R_ATTICO = 11.335         # esagono del tiburio (22,67 m fra i vertici)
R_LOGGE_INF = 11.10       # 24-gono della loggia inferiore
R_LOGGE_SUP = 10.35       # dodecagono della loggia superiore
R_CALOTTA = 10.10         # raggio della calotta alla base (diametro 20,2 m)
R_GRONDA = 10.55          # ghiaccio di gronda in piombo (aggetto)

R_LANTERNA = 2.72         # ottagono del tempietto (5,4 m di diametro)
R_LANTERNA_BASE = 3.05    # basamento e cornice
LATO_SUP = 0.55           # spessore dei muri delle logge
LATO_LANTERNA = 0.40      # spessore dei muri della lanterna

LATI_LOGGE_INF = 24       # due ordini entrambi a ventiquattro lati
LATI_LOGGE_SUP = 24
LATI_LANTERNA = 8
BAIE_LOGGE_INF = 48       # 48 archi acuti -> passo 1.45 m, luce 0.78 m
BAIE_LOGGE_SUP = 72       # 72 archetti -> passo 0.90 m, luce 0.46 m

PASSO_DENTELLI = 0.46
SPESSORE_FASCIA = 0.13

COSTOLONI = 8             # otto costoloni esterni, come nella cupola reale
SPICCHI = 8
PANNELLI_PER_SPICCHIO = 7  # lastre di piombo fra due costoloni
PANNELLO_V = 0.92          # altezza dei filari (m)

NOMI_MAT = {
    "marmo": "Marmo_Bianco_Caldo",
    "cornice": "Marmo_Bianco",
    "scuro": "Marmo_Verde_Scuro",
    "piombo": "Cupola_Piombo_Lastre",
    "piombo_costa": "Cupola_Piombo_Costoloni",
    "oro": "Cupola_Oro",
    "interno": "Cupola_Interno_Laterizio",
    "ferro": "Cupola_Ferro",
}


# -----------------------------------------------------------------------------
# 2. MATERIALI
# -----------------------------------------------------------------------------
VERSIONE_MATERIALI = "5.0.3"


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


def _materiale_piombo():
    """Lastre di piombo con giunti veri.

    La calotta nasce con UV sferiche: u conta i pannelli lungo il giro, v i
    filari lungo il meridiano.  Una Brick Texture con scala 1 disegna quindi
    esattamente i riquadri delle lastre, senza texture esterne e senza
    effetti "mappa applicata a caso" sulle superfici curve.
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
    out.location = (940, 40)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (660, 40)
    bsdf.inputs["Metallic"].default_value = 0.42
    bsdf.inputs["Roughness"].default_value = 0.55
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    uv = nodes.new("ShaderNodeUVMap")
    uv.uv_map = "UVMap"
    uv.location = (-1020, 240)
    lastre = nodes.new("ShaderNodeTexBrick")
    lastre.location = (-800, 240)
    lastre.offset = 0.5
    lastre.offset_frequency = 1
    lastre.squash = 1.0
    lastre.squash_frequency = 1
    lastre.inputs["Color1"].default_value = (0.345, 0.368, 0.383, 1.0)
    lastre.inputs["Color2"].default_value = (0.290, 0.308, 0.320, 1.0)
    lastre.inputs["Mortar"].default_value = (0.150, 0.158, 0.163, 1.0)
    lastre.inputs["Scale"].default_value = 1.0
    lastre.inputs["Mortar Size"].default_value = 0.035
    lastre.inputs["Mortar Smooth"].default_value = 0.35
    lastre.inputs["Bias"].default_value = 0.0
    lastre.inputs["Brick Width"].default_value = 1.0
    lastre.inputs["Row Height"].default_value = 0.72
    links.new(uv.outputs["UV"], lastre.inputs["Vector"])

    # Colature di ruggine: chiazze allungate in verticale, poche e larghe.
    coord = nodes.new("ShaderNodeTexCoord")
    coord.location = (-1020, -240)
    mappa = nodes.new("ShaderNodeMapping")
    mappa.location = (-840, -240)
    mappa.inputs["Scale"].default_value = (0.34, 0.34, 0.085)
    colature = nodes.new("ShaderNodeTexNoise")
    colature.location = (-640, -240)
    colature.inputs["Scale"].default_value = 1.0
    colature.inputs["Detail"].default_value = 6.0
    colature.inputs["Roughness"].default_value = 0.62
    links.new(coord.outputs["Object"], mappa.inputs["Vector"])
    links.new(mappa.outputs["Vector"], colature.inputs["Vector"])
    soglia = nodes.new("ShaderNodeValToRGB")
    soglia.location = (-420, -240)
    soglia.color_ramp.elements[0].position = 0.62
    soglia.color_ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    soglia.color_ramp.elements[1].position = 0.80
    soglia.color_ramp.elements[1].color = (1.0, 1.0, 1.0, 1.0)
    links.new(colature.outputs["Fac"], soglia.inputs["Fac"])

    ruggine = nodes.new("ShaderNodeMixRGB")
    ruggine.location = (-100, 140)
    ruggine.inputs["Color2"].default_value = (0.290, 0.150, 0.088, 1.0)
    ruggine.inputs["Fac"].default_value = 0.40
    links.new(lastre.outputs["Color"], ruggine.inputs["Color1"])
    links.new(soglia.outputs["Color"], ruggine.inputs["Fac"])
    links.new(ruggine.outputs["Color"], bsdf.inputs["Base Color"])

    # Le lastre sono battute una sull'altra: il giunto scava un solco.
    bump = nodes.new("ShaderNodeBump")
    bump.location = (400, -180)
    bump.inputs["Strength"].default_value = 0.35
    bump.inputs["Distance"].default_value = 0.04
    links.new(lastre.outputs["Fac"], bump.inputs["Height"])
    links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])

    # Opacita' variabile: il piombo vecchio e' lucido solo a chiazze.
    rug = nodes.new("ShaderNodeMapRange")
    rug.location = (400, -40)
    rug.inputs["From Min"].default_value = 0.0
    rug.inputs["From Max"].default_value = 0.55
    rug.inputs["To Min"].default_value = 0.34
    rug.inputs["To Max"].default_value = 0.74
    links.new(colature.outputs["Fac"], rug.inputs["Value"])
    links.new(rug.outputs["Result"], bsdf.inputs["Roughness"])
    return m


def _materiale_piombo_costa():
    """Piombo dei costoloni: piu' chiaro e piu' lucido delle lastre, cosi'
    i nastri si leggono in rilievo anche quando la calotta e' in ombra."""
    nome = NOMI_MAT["piombo_costa"]
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
    bsdf.inputs["Base Color"].default_value = (0.345, 0.362, 0.372, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.60
    bsdf.inputs["Roughness"].default_value = 0.30
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def _materiale_oro():
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
    bsdf.inputs["Base Color"].default_value = (0.90, 0.68, 0.24, 1.0)
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.16
    bsdf.inputs["Coat Weight"].default_value = 0.3
    bsdf.inputs["Coat Roughness"].default_value = 0.10
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
        "piombo": _materiale_piombo(),
        "piombo_costa": _materiale_piombo_costa(),
        "oro": _materiale_oro(),
        # Il vano delle gallerie e' laterizio a vista: rosso scuro e opaco,
        # cosi' dentro le logge si legge un'ombra calda e non del marmo.
        "interno": _materiale_esistente_o_piatto(
            NOMI_MAT["interno"], (0.175, 0.088, 0.062), roughness=0.95,
            noise=0.10, scala=scala),
        "ferro": _materiale_esistente_o_piatto(
            NOMI_MAT["ferro"], (0.10, 0.10, 0.11), roughness=0.42,
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
    """Profilo della calotta dal filo di gronda all'apice.

    La cupola senese non e' un emisfero regolare: la spalla sale subito e la
    volta si chiude piu' in fretta.  Un'esponente > 1 sul seno alza la
    spalla, un coseno smorzato tiene il piede piu' pieno.
    """
    out = []
    for k in range(passi + 1):
        th = (k / passi) * math.pi / 2.0
        r = r_base * math.cos(th) ** 0.97
        z = z_base + (z_apice - z_base) * math.sin(th) ** 0.90
        out.append((r, z))
    return out


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

    colonne(acc_colonne, esterno, z_sill, z_imp + 0.04, raggio_col,
            coppia=coppia, sporgenza=LATO_SUP / 2.0 + sporgenza)

    acc_cornice.anello(poligono(cx, cy, raggio + 0.11, lati, ruota), interno,
                       z_cornice, z_trabeazione)
    # i dentelli sono cubetti sotto la corona, non mensole alte quanto la
    # trabeazione: l'altezza si limita in proporzione allo spazio disponibile
    h_dent = min(0.16, 0.5 * (z_trabeazione - z_cornice))
    dentelli(acc_cornice, poligono(cx, cy, raggio + 0.01, lati, ruota),
             z_trabeazione - 0.12 - h_dent, z_trabeazione - 0.12, passo=passo,
             sporgenza=0.08, larghezza=0.12, profondita=0.10)
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


def _crea(nome, acc, materiale, col, scala, uv_sferiche=None):
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
    return obj


def costruisci_cupola(scala=3.0, cfg=None, col=None, cx=None, cy=None):
    """Ricostruisce tiburio, calotta e lanterna nella raccolta 07d*.

    Ritorna un dizionario con il numero di oggetti e le quote usate.
    """
    opt = dict(cfg or {})
    h_attico_base = float(opt.get("altezza_tamburo_base", H_ATTICO_BASE))
    h_cleristorio = float(opt.get("altezza_cleristorio", 21.80))
    h_apice_calotta = float(opt.get("altezza_calotta", H_CALOTTA))
    h_cupola = float(opt.get("altezza_cupola", H_CUPOLA))

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
        0.56, 0.50, 0.62, 0.78, 0.135, 0.084, True, H_LOGGE_INF_TOP,
        passo=0.44)
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
    # Tre archetti per lato (72): colonnine sottili con archi a tutto sesto,
    # il ricamo che nella fotografia corona il tamburo sotto la gronda.
    ruota_sup = math.pi / LATI_LOGGE_SUP
    acc_para, acc_archi, acc_col, acc_corn = (Accumulatore() for _ in range(4))
    z_sill_sup, z_imp_sup, z_corona_sup, z_corn_sup = loggia(
        acc_para, acc_archi, acc_col, acc_corn,
        cx, cy, R_LOGGE_SUP, LATI_LOGGE_SUP, ruota_sup,
        BAIE_LOGGE_SUP, H_LOGGE_SUP_BASE,
        0.38, 0.34, 0.24, 0.46, 0.0, 0.058, False, H_LOGGE_SUP_TOP,
        passo=0.34, sporgenza=0.06, allunga=0.16, campioni=11)
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

    # --- 6.7 calotta in lastre di piombo --------------------------------
    profilo = profilo_calotta(R_CALOTTA, H_CALOTTA_BASE, h_apice_calotta)
    acc = Accumulatore()
    lati = 96
    anelli = []
    for r, z in profilo[:-1]:
        riga = []
        for i in range(lati):
            ang = 2.0 * math.pi * i / lati
            riga.append(acc.v(cx + r * math.cos(ang), cy + r * math.sin(ang), z))
        anelli.append(riga)
    apice = acc.v(cx, cy, h_apice_calotta)
    for k in range(len(anelli) - 1):
        for i in range(lati):
            j = (i + 1) % lati
            acc.faces.append((anelli[k][i], anelli[k][j],
                              anelli[k + 1][j], anelli[k + 1][i]))
    for i in range(lati):
        acc.faces.append((anelli[-1][i], anelli[-1][(i + 1) % lati], apice))

    def uv_calotta(co):
        """UV sferiche allineate ai costoloni: u = pannelli lungo il giro,
        v = filari lungo il meridiano.  I giunti della texture cadono esatti
        sui costoloni e sulle file di lastre."""
        x = co.x / scala - cx
        y = co.y / scala - cy
        z = co.z / scala
        ang = math.atan2(y, x) % (2.0 * math.pi)
        u = ang / (2.0 * math.pi) * (SPICCHI * PANNELLI_PER_SPICCHIO)
        raggio = math.hypot(x, y)
        th = math.atan2(max(z - H_CALOTTA_BASE, 0.0), max(raggio, 1e-6))
        v = th * R_CALOTTA / PANNELLO_V
        return (u, v)

    creati.append(_crea("Cupola_Calotta", acc, mats["piombo"], col, scala,
                        uv_sferiche=uv_calotta))

    # otto costoloni tondi: piu' grossi alla base, assottigliati all'apice
    acc = Accumulatore()
    for i in range(COSTOLONI):
        ang = 2.0 * math.pi * i / COSTOLONI
        pts, raggi = [], []
        for k in range(0, len(profilo) - 1):
            r, z = profilo[k]
            t = k / float(len(profilo) - 1)
            pts.append((r - 0.04, z, ang))
            raggi.append(0.255 - 0.150 * t)
        # chiusura in punta: il costolone si assottiglia fino all'apice
        pts.append((0.02, H_CALOTTA - 0.02, ang))
        raggi.append(0.045)
        acc.tubo(pts, raggi, seg=14, cx=cx, cy=cy, schiacciamento=0.80)
    creati.append(_crea("Cupola_Costoloni", acc, mats["piombo_costa"], col,
                        scala))

    # --- 6.8 lanterna del Bernini ---------------------------------------
    # Misure ricavate dal primo piano `riferimento_cupola_lanterna.jpg`:
    # ottagono di 4,9 m di diametro, corpo finestrato con bifore e colonne
    # binate ai cantonali, trabeazione a dentelli, tetto a padiglione in
    # piombo con costoloni sui cantonali, pinnacolo lapideo e mela dorata.
    # La somma delle altezze arriva esattamente alla quota di 48 m.
    z0 = H_LANTERNA_BASE
    lant = poligono(cx, cy, R_LANTERNA, LATI_LANTERNA,
                    math.pi / LATI_LANTERNA)
    lant_int = poligono(cx, cy, R_LANTERNA - LATO_LANTERNA, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA)
    spor_l = LATO_LANTERNA / 2.0 + 0.070

    z_bas = z0 + 0.22
    z_zoc = z0 + 0.48
    z_dav = z_zoc + 0.32
    z_imp_l = z0 + 2.85
    z_top_l = z0 + 3.42
    z_trab = z0 + 3.80

    # 1) basamento: piattaforma che raccorda la calotta al tempietto
    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LANTERNA_BASE + 0.16, 32),
               poligono(cx, cy, R_LANTERNA - 0.04, 32), z0 - 0.22, z0 + 0.08)
    acc.anello(poligono(cx, cy, R_LANTERNA_BASE, 32),
               poligono(cx, cy, R_LANTERNA - 0.04, 32), z0 + 0.08, z_bas)
    creati.append(_crea("Lanterna_Basamento", acc, mats["cornice"], col, scala))

    # 2) zoccolo pieno e davanzale
    acc = Accumulatore()
    acc.anello(lant, lant_int, z_bas, z_dav)
    acc.anello(poligono(cx, cy, R_LANTERNA + 0.07, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               lant_int, z_dav - 0.07, z_dav)
    creati.append(_crea("Lanterna_Zoccolo", acc, mats["marmo"], col, scala))

    # 2b) pavimento del tempietto: dentro le bifore si legge il vano in
    # ombra, non il cielo (nella v5.0.1 si vedeva un foro azzurro)
    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LANTERNA + 0.02, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               poligono(cx, cy, 0.35, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               z_bas + 0.02, z_bas + 0.07)
    creati.append(_crea("Lanterna_Pavimento", acc, mats["interno"], col, scala))

    # 3) corpo finestrato: otto bifore passanti
    acc = Accumulatore()
    parete_arche(acc, lant, z_dav, z_top_l, LATO_LANTERNA, LATI_LANTERNA,
                 1.34, 0.36, z_imp_l, acuto=False, campioni=9, allunga=0.14)
    creati.append(_crea("Lanterna_Pareti", acc, mats["marmo"], col, scala))

    # 4) colonne binate ai cantonali e colonnine centrali delle bifore
    acc = Accumulatore()
    colonne(acc, lant, z_dav, z_top_l, 0.086, coppia=0.155, sporgenza=spor_l)
    creati.append(_crea("Lanterna_Colonne", acc, mats["cornice"], col, scala))

    acc = Accumulatore()
    for i in range(LATI_LANTERNA):
        p0, p1 = lant[i], lant[(i + 1) % LATI_LANTERNA]
        mx, my = (p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0
        vx, vy = mx - cx, my - cy
        lung = math.hypot(vx, vy) or 1.0
        vx, vy = vx / lung, vy / lung
        acc.cilindro(mx - vx * 0.03, my - vy * 0.03, z_dav, z_imp_l + 0.20,
                     0.068, seg=8)
        acc.cilindro(mx - vx * 0.03, my - vy * 0.03, z_imp_l + 0.20,
                     z_imp_l + 0.28, 0.100, seg=8)
    creati.append(_crea("Lanterna_Colonnine_Bifore", acc, mats["cornice"], col,
                        scala))

    # 5) trabeazione: fascia, dentelli, cornice aggettante
    acc = Accumulatore()
    acc.anello(poligono(cx, cy, R_LANTERNA + 0.09, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               poligono(cx, cy, R_LANTERNA - LATO_LANTERNA - 0.04,
                        LATI_LANTERNA, math.pi / LATI_LANTERNA),
               z_top_l, z_top_l + 0.12)
    dentelli(acc, poligono(cx, cy, R_LANTERNA + 0.01, LATI_LANTERNA,
                           math.pi / LATI_LANTERNA),
             z_top_l + 0.13, z_top_l + 0.23, passo=0.28, sporgenza=0.10,
             larghezza=0.12, profondita=0.09)
    acc.anello(poligono(cx, cy, R_LANTERNA + 0.28, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               poligono(cx, cy, R_LANTERNA - 0.16, LATI_LANTERNA,
                        math.pi / LATI_LANTERNA),
               z_top_l + 0.23, z_trab)
    creati.append(_crea("Lanterna_Trabeazione", acc, mats["cornice"], col,
                        scala))

    # 6) tetto a padiglione in piombo, a campana, con costoloni
    z_gronda = z_trab
    z_tetto = z0 + 5.55
    r_gronda = R_LANTERNA + 0.62
    # profilo a campana: gronda che si allarga, poi salita ripida
    nodi = [(0.00, 1.000), (0.06, 1.015), (0.14, 0.968), (0.26, 0.845),
            (0.40, 0.690), (0.55, 0.520), (0.70, 0.350), (0.84, 0.200),
            (0.94, 0.095), (1.00, 0.030)]
    passi = 24
    prof = []
    for k in range(passi + 1):
        t = k / passi
        prof.append((r_gronda * _interp(nodi, t),
                     z_gronda + (z_tetto - z_gronda) * t))
    lati_t = 64
    acc = Accumulatore()
    anelli = []
    for r, z in prof:
        riga = []
        for i in range(lati_t):
            ang = 2.0 * math.pi * i / lati_t + math.pi / LATI_LANTERNA
            riga.append(acc.v(cx + r * math.cos(ang), cy + r * math.sin(ang), z))
        anelli.append(riga)
    for k in range(len(anelli) - 1):
        for i in range(lati_t):
            j = (i + 1) % lati_t
            acc.faces.append((anelli[k][i], anelli[k][j],
                              anelli[k + 1][j], anelli[k + 1][i]))
    acc.faces.append(tuple(reversed(anelli[0])))
    acc.faces.append(tuple(anelli[-1]))
    creati.append(_crea("Lanterna_Tetto", acc, mats["piombo"], col, scala))

    acc = Accumulatore()
    for i in range(LATI_LANTERNA):
        ang = 2.0 * math.pi * i / LATI_LANTERNA + math.pi / LATI_LANTERNA
        pts, raggi = [], []
        for k, (r, z) in enumerate(prof):
            if r < 0.26:
                break
            pts.append((r + 0.012, z, ang))
            raggi.append(0.052 - 0.022 * (k / float(passi)))
        acc.tubo(pts, raggi, seg=8, cx=cx, cy=cy)
    # anello di gronda che chiude il bordo del tetto
    acc.anello(poligono(cx, cy, r_gronda + 0.02, 64),
               poligono(cx, cy, r_gronda - 0.16, 64),
               z_gronda - 0.11, z_gronda + 0.06)
    creati.append(_crea("Lanterna_Costoloni_Tetto", acc, mats["piombo_costa"],
                        col, scala))

    # 7) pinnacolo lapideo a vaso (profilo a tornio, dalla foto ravvicinata)
    z_fin = z_tetto - 0.14
    profilo_pin = [
        (z_fin, 0.26), (z_fin + 0.04, 0.34), (z_fin + 0.10, 0.31),
        (z_fin + 0.16, 0.20), (z_fin + 0.24, 0.16), (z_fin + 0.34, 0.24),
        (z_fin + 0.44, 0.30), (z_fin + 0.55, 0.27), (z_fin + 0.65, 0.20),
        (z_fin + 0.73, 0.14), (z_fin + 0.79, 0.10), (z_fin + 0.85, 0.13),
    ]
    acc = Accumulatore()
    acc.rivoluzione(cx, cy, profilo_pin, seg=24)
    creati.append(_crea("Lanterna_Pinnacolo", acc, mats["cornice"], col, scala))

    # 8) mela dorata (sfera a coste) infilata sull'asta del pinnacolo
    r_mela = 0.40
    z_fondo_mela = z_fin + 0.66
    z_centro_mela = z_fondo_mela + r_mela
    acc = Accumulatore()
    profilo_mela = []
    passi_m = 16
    for k in range(passi_m + 1):
        a = -math.pi / 2.0 + math.pi * k / passi_m
        profilo_mela.append((z_centro_mela + r_mela * math.sin(a),
                             r_mela * math.cos(a) * 0.995))
    acc.rivoluzione(cx, cy, profilo_mela, seg=40, costa=0.085, coste=12)
    creati.append(_crea("Lanterna_Mela_Dorata", acc, mats["oro"], col, scala))

    # 9) stella a dodici punte: appoggiata alla sommita' della mela
    z_stella = z_centro_mela + r_mela + 0.18
    acc = Accumulatore()
    punte = 12
    r_out = 0.44
    spess = 0.07
    poly = []
    for k in range(punte * 2):
        a = math.pi * k / punte + math.pi / 2.0
        r = r_out if k % 2 == 0 else r_out * 0.24
        poly.append((r * math.cos(a), r * math.sin(a)))
    n = len(poly)
    for segno in (-1, 1):
        acc.faces.append(tuple(
            acc.v(cx + px, cy + segno * spess / 2.0, z_stella + pz)
            for px, pz in poly))
    for k in range(n):
        j = (k + 1) % n
        a0 = acc.v(cx + poly[k][0], cy - spess / 2.0, z_stella + poly[k][1])
        a1 = acc.v(cx + poly[j][0], cy - spess / 2.0, z_stella + poly[j][1])
        b0 = acc.v(cx + poly[k][0], cy + spess / 2.0, z_stella + poly[k][1])
        b1 = acc.v(cx + poly[j][0], cy + spess / 2.0, z_stella + poly[j][1])
        acc.faces.append((a0, a1, b1, b0))
    creati.append(_crea("Lanterna_Stella_Dorata", acc, mats["oro"], col, scala))

    # 10) asta in punta con il braccio della croce, fino ai 48 m ufficiali
    acc = Accumulatore()
    z_asta = z_stella + r_out - 0.12
    acc.cilindro(cx, cy, z_asta, h_cupola, 0.030, seg=8,
                 raggio_alto=0.014)
    z_braccio = h_cupola - 0.26
    acc.scatola(cx, cy, z_braccio, 1.0, 0.0, 0.22, 0.050, 0.050)
    acc.scatola(cx, cy, z_braccio, 0.0, 1.0, 0.22, 0.050, 0.050)
    creati.append(_crea("Lanterna_Croce", acc, mats["oro"], col, scala))


    print("=" * 72)
    print("CUPOLA v5.0 — due ordini di logge, calotta in lastre, lanterna")
    print("=" * 72)
    for k, v in quote().items():
        print(f"  {k:<44s} {v:>8.2f}")
    print(f"  oggetti creati: {len(creati)}")
    print("=" * 72)

    return {"oggetti": len(creati), "collezione": col.name, "quote": quote(),
            "vertici": sum(len(o.data.vertices) for o in creati)}


def quote():
    """Quote del gruppo cupola, in metri reali (per il riepilogo)."""
    return {
        "Piede del tiburio": H_ATTICO_BASE,
        "Sommita delle due logge [m]": H_LOGGE_SUP_TOP,
        "Imposta della calotta [m]": H_CALOTTA_BASE,
        "Apice della calotta / lanterna [m]": H_CALOTTA,
        "Punta della croce [m]": H_CUPOLA,
        "Freccia della calotta [m]": H_CALOTTA - H_CALOTTA_BASE,
        "Rapporto freccia/diametro": (H_CALOTTA - H_CALOTTA_BASE) /
                                     (2.0 * R_CALOTTA),
    }
