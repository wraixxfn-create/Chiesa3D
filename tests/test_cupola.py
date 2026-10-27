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


if __name__ == "__main__":
    unittest.main()
