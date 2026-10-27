"""v5.0 — prove sulla cupola: quote, archi e proporzioni.

Come gli altri test del progetto lavorano senza `bpy`: verificano solo la
matematica del modulo `cupola.py` (profili, archi, poligoni, quote), quella
che determina la silhouette nelle fotografie di riferimento.
"""

import math
import unittest

import cupola as c


class QuoteTest(unittest.TestCase):
    def test_gerarchia_delle_quote(self):
        self.assertLess(c.H_ATTICO_BASE, c.H_ATTICO_TOP)
        self.assertLess(c.H_ATTICO_TOP, c.H_LOGGE_INF_BASE)
        self.assertLess(c.H_LOGGE_INF_TOP, c.H_LOGGE_SUP_BASE)
        self.assertLess(c.H_LOGGE_SUP_TOP, c.H_CALOTTA_BASE)
        self.assertLess(c.H_CALOTTA_BASE, c.H_CALOTTA)
        self.assertLess(c.H_CALOTTA, c.H_CUPOLA)

    def test_croce_alla_quota_ufficiale(self):
        # La quota ufficiale (48 m croce compresa) non si tocca: resta il
        # rapporto 1,28 con la facciata da 37,5 m.
        self.assertEqual(c.H_CUPOLA, 48.0)
        self.assertAlmostEqual(c.H_CUPOLA / 37.5, 1.28, places=6)

    def test_calotta_impostata_sotto_la_facciata(self):
        # La calotta parte a 31,55 m, sotto i 37,5 m della facciata: nelle
        # fotografie la cupola e' piu' bassa del fronte.
        self.assertLess(c.H_CALOTTA_BASE, 37.5)
        self.assertGreater(c.H_CALOTTA, 37.5)

    def test_proporzione_della_calotta(self):
        # Freccia / diametro misurata sulle fotografie (0,45-0,50): la cupola
        # senese e' piu' alta di un emisfero schiacciato ma piu' bassa di
        # quella di Santa Maria del Fiore.
        q = c.quote()
        self.assertGreater(q["Rapporto freccia/diametro"], 0.40)
        self.assertLess(q["Rapporto freccia/diametro"], 0.60)

    def test_tiburio_copre_l_esagono_della_crociera(self):
        # L'esagono del tiburio e' quello della crociera (22,67 m fra i
        # vertici) e le logge restano dentro quel filo.
        self.assertGreater(c.R_ATTICO, 10.6)
        self.assertAlmostEqual(2 * c.R_ATTICO, 22.67, places=2)
        self.assertLessEqual(c.R_LOGGE_INF, c.R_ATTICO)

    def test_lanterna_piu_stretta_del_tiburio(self):
        self.assertLess(c.R_LANTERNA, c.R_CALOTTA / 3.0)
        self.assertGreater(c.R_LANTERNA, 2.0)


class ProfiloTest(unittest.TestCase):
    def test_profilo_parte_dalla_gronda_e_chiude_all_apice(self):
        prof = c.profilo_calotta(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                 c.H_CALOTTA)
        self.assertAlmostEqual(prof[0][0], c.R_CALOTTA, places=6)
        self.assertAlmostEqual(prof[0][1], c.H_CALOTTA_BASE, places=6)
        self.assertAlmostEqual(prof[-1][0], 0.0, places=6)
        self.assertAlmostEqual(prof[-1][1], c.H_CALOTTA, places=6)

    def test_profilo_monotono(self):
        # Il raggio cala e la quota sale: nessun rigonfiamento che farebbe
        # leggere la calotta come una campana.
        prof = c.profilo_calotta(c.R_CALOTTA, c.H_CALOTTA_BASE, c.H_CALOTTA)
        for (r0, z0), (r1, z1) in zip(prof, prof[1:]):
            self.assertLessEqual(r1, r0 + 1e-9)
            self.assertGreaterEqual(z1, z0 - 1e-9)

    def test_interpolazione_nodi(self):
        nodi = [(0.0, 1.0), (0.5, 0.8), (1.0, 0.0)]
        self.assertAlmostEqual(c._interp(nodi, 0.0), 1.0)
        self.assertAlmostEqual(c._interp(nodi, 0.5), 0.8)
        self.assertAlmostEqual(c._interp(nodi, 0.25), 0.9)
        self.assertAlmostEqual(c._interp(nodi, 1.0), 0.0)


class ArchiTest(unittest.TestCase):
    def test_arco_a_tutto_sesto(self):
        self.assertAlmostEqual(c._quota_arco(0.0, 1.0, False), 1.0)
        self.assertAlmostEqual(c._quota_arco(1.0, 1.0, False), 0.0)
        self.assertAlmostEqual(c._quota_arco(-1.0, 1.0, False), 0.0)

    def test_arco_acuto_a_equilatero(self):
        # Arco acuto equilatero: stessa freccia di quello a tutto sesto, ma
        # piu' "a punta", cioe' piu' stretto sui fianchi a parita' di quota.
        self.assertAlmostEqual(c._quota_arco(0.0, 1.0, True), 1.0)
        self.assertAlmostEqual(c._quota_arco(1.0, 1.0, True), 0.0)
        for t in (0.25, 0.5, 0.75):
            self.assertLess(c._quota_arco(t, 1.0, True),
                            c._quota_arco(t, 1.0, False))
        # Rapporto fra freccia e luce dell'arco equilatero: radice di 3 / 2.
        self.assertAlmostEqual(c._quota_arco(0.0, math.sqrt(3.0) / 2.0, True),
                               math.sqrt(3.0) / 2.0, places=9)

    def test_quota_limitata_fuori_intervallo(self):
        # Il profilo viene campionato con t in [-1, 1]: oltre, il clamp
        # evita archi che "rientrano" sotto il davanzale.
        self.assertAlmostEqual(c._quota_arco(-2.0, 1.0, False), 0.0)
        self.assertAlmostEqual(c._quota_arco(3.0, 1.0, True), 0.0)


class PoligoniTest(unittest.TestCase):
    def test_esagono_del_tiburio(self):
        poly = c.poligono(0.0, 0.0, c.R_ATTICO, 6)
        self.assertEqual(len(poly), 6)
        for x, y in poly:
            self.assertAlmostEqual(math.hypot(x, y), c.R_ATTICO, places=6)

    def test_lati_di_lunghezza_costante(self):
        poly = c.poligono(3.0, -2.0, c.R_LOGGE_SUP, c.LATI_LOGGE_SUP)
        lati = []
        for i in range(len(poly)):
            p0 = poly[i]
            p1 = poly[(i + 1) % len(poly)]
            lati.append(math.hypot(p1[0] - p0[0], p1[1] - p0[1]))
        for lat in lati[1:]:
            self.assertAlmostEqual(lat, lati[0], places=9)

    def test_lato_restituisce_normale_e_lunghezza(self):
        dx, dy, nx, ny, lung = c._lato((0.0, 0.0), (2.0, 0.0))
        self.assertAlmostEqual(dx, 1.0)
        self.assertAlmostEqual(dy, 0.0)
        self.assertAlmostEqual(lung, 2.0)
        self.assertAlmostEqual(nx * dx + ny * dy, 0.0)
        self.assertAlmostEqual(math.hypot(nx, ny), 1.0)


class LastreTest(unittest.TestCase):
    """v5.1 — la calotta e' un reticolo di lastre, non una superficie."""

    def test_profilo_ricampionato_sull_arco(self):
        nodi = c.profilo_calotta_lastre(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                        c.H_CALOTTA)
        self.assertEqual(len(nodi), c.FILARI_CALOTTA + 1)
        # passi di arco (quasi) costanti: le lastre in cima non si
        # assottigliano come succederebbe campionando l'angolo
        passi = [math.hypot(r1 - r0, z1 - z0)
                 for (r0, z0), (r1, z1) in zip(nodi, nodi[1:])]
        self.assertLess(max(passi) / min(passi), 1.25)
        # il profilo parte dalla gronda e si ferma al basamento della lanterna
        self.assertAlmostEqual(nodi[0][0], c.R_CALOTTA, places=6)
        self.assertAlmostEqual(nodi[0][1], c.H_CALOTTA_BASE, places=6)
        self.assertLess(nodi[-1][0], c.R_LANTERNA_BASE)

    def test_reticolo_di_lastre_completo(self):
        # 8 spicchi x 8 strisce x 12 filari = 768 piastre, e nessun buco:
        # ogni lastra ha quattro vertici distinti
        nodi = c.profilo_calotta_lastre(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                        c.H_CALOTTA)
        acc = c.Accumulatore()
        c.calotta_lastre(acc, c.Accumulatore(), c.Accumulatore(),
                         0.0, 0.0, nodi)
        attese = c.SPICCHI * c.STRISCE_PER_SPICCHIO * (len(nodi) - 1)
        self.assertEqual(len(acc.faces), attese)
        self.assertEqual(attese, 768)
        for f in acc.faces:
            self.assertEqual(len(set(f)), 4)

    def test_costoloni_sugli_spigoli_degli_spicchi(self):
        # otto costoloni, uno per spicchio, alla stessa rotazione dei
        # cantonali della lanterna
        nodi = c.profilo_calotta_lastre(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                        c.H_CALOTTA)
        acc = c.Accumulatore()
        c.calotta_lastre(c.Accumulatore(), c.Accumulatore(), acc,
                         0.0, 0.0, nodi)
        passo = 2.0 * math.pi / c.SPICCHI
        r_max = c.R_CALOTTA + 0.40
        angoli = set()
        for x, y, z in acc.verts:
            if abs(z - c.H_CALOTTA_BASE) < 0.02:
                angoli.add(round((math.atan2(y, x) % (2.0 * math.pi)) / passo,
                                 1))
        self.assertEqual(len(angoli), c.SPICCHI)
        for x, y, z in acc.verts:
            self.assertLessEqual(math.hypot(x, y), r_max)


class LanternaTest(unittest.TestCase):
    """v5.1 — la lanterna sta fra la calotta e i 48 m, senza sfondare."""

    def test_quote_della_lanterna_in_ordine(self):
        self.assertLess(c.L_ZOCOLO, c.L_DAVANZALE)
        self.assertLess(c.L_DAVANZALE, c.L_IMPOSTA)
        self.assertLess(c.L_IMPOSTA + c.L_ARCHI, c.L_CORONA + 0.10)
        self.assertLess(c.L_CORONA, c.L_TRABEAZIONE)
        self.assertLess(c.L_TRABEAZIONE, c.L_GRONDA)
        self.assertLess(c.L_GRONDA, c.L_TETTO)
        self.assertLess(c.L_TETTO, c.L_VASO)
        self.assertLess(c.L_VASO, c.L_MELA)
        self.assertLess(c.L_MELA, c.L_STELLA)

    def test_fastigio_sotto_la_croce(self):
        # la stella deve stare sotto la punta della croce, con un margine
        # per l'asta: e' il vincolo che limita l'altezza dell'apice
        cima_stella = c.L_STELLA + 0.30
        self.assertLess(cima_stella + 0.30, c.H_CUPOLA - c.H_LANTERNA_BASE)

    def test_lanterna_piu_slancia_che_larga(self):
        # Dalla base alla punta del tetto la lanterna e' piu' alta del suo
        # diametro (nelle fotografie il tempietto e' snello), ma non e' una
        # torre: il rapporto resta sotto 1,8.
        altezza = c.L_TETTO
        diametro = 2.0 * c.R_LANTERNA
        self.assertGreater(altezza / diametro, 1.05)
        self.assertLess(altezza / diametro, 1.80)
        # le finestre sono piu' alte che larghe, come nei primi piani
        self.assertGreater((c.L_IMPOSTA + c.L_ARCHI) - c.L_DAVANZALE,
                           1.6 * 1.02)


if __name__ == "__main__":
    unittest.main()
