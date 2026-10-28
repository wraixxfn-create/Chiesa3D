"""v5.2 — prove sulla cupola: quote, profili, archi e proporzioni.

Come gli altri test del progetto lavorano senza `bpy`: verificano solo la
matematica del modulo `cupola.py` (profili, archi, poligoni, finestre, quote),
quella che determina la silhouette nelle fotografie di riferimento.
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
        # La quota ufficiale (48 m croce/segnavento compresi) non si tocca:
        # resta il rapporto 1,28 con la facciata da 37,5 m.
        self.assertEqual(c.H_CUPOLA, 48.0)
        self.assertAlmostEqual(c.H_CUPOLA / 37.5, 1.28, places=6)

    def test_calotta_impostata_sotto_la_facciata(self):
        # La calotta parte a 30,05 m, sotto i 37,5 m della facciata: nelle
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

    def test_apice_ogivale_a_punta(self):
        # v5.2: l'apice non ha la tangente orizzontale dell'emisfero.  A
        # 0,98 della freccia il raggio e' quasi zero, non il 20% della base.
        prof = c.profilo_calotta(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                 c.H_CALOTTA, 100)
        r_quasi_cima = prof[98][0]
        self.assertLess(r_quasi_cima, 0.12 * c.R_CALOTTA)
        self.assertGreater(r_quasi_cima, 0.005 * c.R_CALOTTA)
        # un emisfero avrebbe ancora r/R = sqrt(1 - 0,98^2) = 0,199
        self.assertLess(r_quasi_cima / c.R_CALOTTA,
                        0.199)

    def test_spalla_verticale(self):
        # Nei primi 2 m la calotta resta quasi cilindrica: nella fotografia
        # dal Facciatone la spalla sale dritta sopra la gronda.
        prof = c.profilo_calotta(c.R_CALOTTA, c.H_CALOTTA_BASE,
                                 c.H_CALOTTA, 100)
        r_10 = prof[10][0]
        self.assertGreater(r_10 / c.R_CALOTTA, 0.96)
        self.assertLess(r_10 / c.R_CALOTTA, 1.001)


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
    """v5.2 — la calotta e' un reticolo ogivale di 768 lastre."""

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
        # La calotta deve incontrare il basamento e non lasciare una fessura.
        self.assertGreaterEqual(nodi[-1][1], c.H_CALOTTA - 0.50)

    def test_reticolo_di_lastre_completo(self):
        # 16 spicchi x 4 strisce x 12 filari = 768 piastre, e nessun buco:
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
        # sedici costoloni, uno per spicchio, alla stessa rotazione delle
        # finestre della lanterna
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
                                 1) % c.SPICCHI)
        self.assertEqual(len(angoli), c.SPICCHI)
        for x, y, z in acc.verts:
            self.assertLessEqual(math.hypot(x, y), r_max)

    def test_sedici_costoloni_e_quattro_strisce(self):
        # v5.2: il passo dei costoloni dimezza, quello delle lastre resta
        # tale da conservare le 768 piastre della versione precedente.
        self.assertEqual(c.COSTOLONI, 16)
        self.assertEqual(c.SPICCHI, 16)
        self.assertEqual(c.STRISCE_PER_SPICCHIO, 4)
        self.assertEqual(c.FILARI_CALOTTA, 12)
        self.assertEqual(c.COSTOLONI * c.STRISCE_PER_SPICCHIO *
                         c.FILARI_CALOTTA, 768)


class FinestreTest(unittest.TestCase):
    """v5.2 — la lanterna ha finestre rettangolari, non archi acuti."""

    def test_parete_con_finestre_rettangolari(self):
        self.assertEqual(c.L_ARCHI, 0.0)
        self.assertEqual(c.LATI_CORPO_LANTERNA, 64)
        self.assertEqual(c.BAIE_LANTERNA, 8)
        acc = c.Accumulatore()
        z0 = c.H_CALOTTA + c.L_DAVANZALE - 0.10
        z1 = c.H_CALOTTA + c.L_CORONA
        z_dav = c.H_CALOTTA + c.L_DAVANZALE
        z_top = c.H_CALOTTA + c.L_IMPOSTA + c.L_ARCHI
        pannelli = c.parete_finestre_rettangolari(
            acc, 0.0, 0.0, c.R_LANTERNA, c.LATI_CORPO_LANTERNA,
            z0, z1, c.LATO_LANTERNA, c.BAIE_LANTERNA, 1.18,
            z_dav, z_top, math.pi / c.BAIE_LANTERNA)
        self.assertGreater(pannelli, 0)
        self.assertLess(pannelli, c.LATI_CORPO_LANTERNA)
        self.assertGreater(len(acc.faces), c.LATI_CORPO_LANTERNA * 4)
        # gli ovali dei trafori e degli oculi sono dischi a due facce
        acc2 = c.Accumulatore()
        c.disco_ovale(acc2, (0.0, 0.0, 1.0), (1.0, 0.0, 0.0),
                      (0.0, 0.0, 1.0), (0.0, 1.0, 0.0),
                      0.12, 0.08, 0.03, 16)
        self.assertEqual(len(acc2.verts), 32)
        self.assertEqual(len(acc2.faces), 18)


class LanternaTest(unittest.TestCase):
    """v5.2 — la lanterna sta fra la calotta e i 48 m, senza sfondare."""

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
        # stella + asta + bandiera restano sotto la punta del segnavento
        cima = c.L_STELLA + c.R_STELLA + 0.10
        self.assertLess(cima, c.H_CUPOLA - c.H_LANTERNA_BASE)

    def test_lanterna_piu_slancia_che_larga(self):
        # Dalla base alla punta del tetto la lanterna e' piu' alta del suo
        # diametro (nelle fotografie il tempietto e' snello), ma non e' una
        # torre: il rapporto resta sotto 1,8.
        altezza = c.L_TETTO
        diametro = 2.0 * c.R_LANTERNA
        self.assertGreater(altezza / diametro, 1.05)
        self.assertLess(altezza / diametro, 1.80)
        # le finestre rettangolari sono piu' alte che larghe
        self.assertGreater((c.L_IMPOSTA + c.L_ARCHI) - c.L_DAVANZALE,
                           1.6 * 1.02)

    def test_tetto_a_otto_lobi_e_fastigio_sfaccettato(self):
        # v5.2: tetto piu' alto, mela e stella piu' grandi, logge superiori
        # riproporzionate da 72 a 48 archetti.
        self.assertGreater(c.L_TETTO, 7.0)
        self.assertAlmostEqual(c.H_LANTERNA_BASE + c.L_TETTO, 46.35,
                               places=6)
        self.assertAlmostEqual(c.H_LANTERNA_BASE + c.L_MELA, 46.94,
                               places=6)
        self.assertGreaterEqual(c.R_MELA, 0.38)
        self.assertGreater(c.R_STELLA, 0.30)
        self.assertEqual(c.BAIE_LOGGE_SUP, 48)
        n = 8
        stella = c.Accumulatore()
        c.stella_oro(stella, 0.0, 0.0, 1.0, c.R_STELLA, punte=n)
        self.assertGreater(len(stella.faces), 6 * n)


if __name__ == "__main__":
    unittest.main()
