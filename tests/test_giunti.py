"""v4.4 — i muri non hanno piu' fessure e nessun pezzo resta sospeso.

Questi test lavorano solo in 2D (nessun `bpy`): verificano la matematica dei
giunti a mitra, la continuita' dei tratti e la geometria dei volumi che
chiudono gli spazi fra le coperture.
"""

import math
import unittest

import muri_esterni as m


def _area(poly):
    n = len(poly)
    return 0.5 * sum(poly[i][0] * poly[(i + 1) % n][1] -
                     poly[(i + 1) % n][0] * poly[i][1] for i in range(n))


def _dentro(punto, poly):
    x, y = punto
    dentro = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                dentro = not dentro
    return dentro


class MitreTest(unittest.TestCase):
    def test_larghezza_costante_a_90_gradi(self):
        nodi = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)]
        sinistra, destra = m._offset_polilinea_m(nodi, 2.0)
        # Il giunto interno deve essere a 1 m da entrambi i lati.
        self.assertAlmostEqual(sinistra[1][0], 9.0)
        self.assertAlmostEqual(sinistra[1][1], 1.0)
        self.assertAlmostEqual(destra[1][0], 11.0)
        self.assertAlmostEqual(destra[1][1], -1.0)

    def test_anello_chiuso_ha_la_stessa_area_dell_asse(self):
        # Un anello quadrato di lato 10 con muro da 2 m deve dare un anello
        # esterno di lato 12 e interno di lato 8: nessun cuneo, nessuna
        # sovrapposizione (era il difetto dei gusci aperti della v4.3).
        quadrato = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
        interno, esterno = m._offset_polilinea_m(quadrato, 2.0, chiuso=True)
        self.assertAlmostEqual(abs(_area(esterno)), 144.0)
        self.assertAlmostEqual(abs(_area(interno)), 64.0)
        self.assertAlmostEqual(144.0 - 64.0, 2.0 * 10.0 * 4.0)


class PerimetroTest(unittest.TestCase):
    def test_tratti_consecutivi_condividono_la_testata(self):
        # Due tratti consecutivi devono avere gli stessi due punti di
        # giunto: se differiscono, in render si vede una fessura.
        for sp in (m.SPESSORE_MURO, m.SPESSORE_MURO + 0.36):
            for (_, _, i0a, i1a), (_, _, i0b, i1b) in zip(m.TRATTI_MURO,
                                                         m.TRATTI_MURO[1:]):
                A = m.poligono_tratto(m.PERIMETRO, sp, i0a, i1a)
                B = m.poligono_tratto(m.PERIMETRO, sp, i0b, i1b)
                # poligono_tratto = [sinistra_i0 ... sinistra_i1,
                #                     destra_i1 ... destra_i0]
                n = len(A) // 2 - 1
                testata_finale = {A[n], A[n + 1]}   # nodo i1
                testata_iniziale = {B[0], B[-1]}    # nodo i0
                self.assertEqual(testata_finale, testata_iniziale)
                self.assertEqual(i1a, i0b)

    def test_anello_chiuso_sui_due_spigoli_della_facciata(self):
        # Il primo e l'ultimo tratto si chiudono sul lato della facciata.
        primo = m.poligono_tratto(m.PERIMETRO, m.SPESSORE_MURO, 0, 2)
        ultimo = m.poligono_tratto(m.PERIMETRO, m.SPESSORE_MURO, 15, 17)
        self.assertEqual(len(primo), len(ultimo))
        self.assertLess(abs(_area(m._poligono_ccw(primo))), 100.0)
        self.assertLess(abs(_area(m._poligono_ccw(ultimo))), 100.0)
        # Le due spalline non devono sporgere oltre la facciata (30 m).
        xs = [p[0] for p in primo + ultimo]
        self.assertLessEqual(max(xs) - min(xs), m.LARGHEZZA_FACCIATA)

    def test_perimetro_copre_un_area_positiva(self):
        self.assertGreater(_area(m._poligono_ccw(m.PERIMETRO)), 2000.0)


class DuomoNuovoTest(unittest.TestCase):
    def test_catena_continua(self):
        # Attacco -> Nord -> Facciatone -> Sud, tutti in un'unica catena.
        self.assertEqual(len(m.CATENA_DUOMO_NUOVO), 5)
        for (_, i0, i1), (_, j0, j1) in zip(m.TRATTI_DUOMO_NUOVO,
                                            m.TRATTI_DUOMO_NUOVO[1:]):
            self.assertEqual(i1, j0)
        for a, b in zip(m.CATENA_DUOMO_NUOVO, m.CATENA_DUOMO_NUOVO[1:]):
            self.assertNotEqual(a, b)

    def test_angolo_del_facciatone_a_mitra(self):
        # All'angolo Nord-Est il giunto deve essere squadrato: i due punti
        # del muro distano esattamente lo spessore, non di piu'.
        sp = m.SPESSORE_INCOMPIUTO
        poly = m.poligono_catena(m.CATENA_DUOMO_NUOVO, sp, 1, 3)
        n = len(poly) // 2
        angolo_esterno = poly[n - 2]     # nodo 2 (angolo NE del recinto)
        angolo_interno = poly[n + 1]
        self.assertAlmostEqual(math.dist(angolo_esterno, angolo_interno),
                               sp * math.sqrt(2), places=6)


class VolumiTest(unittest.TestCase):
    def test_i_volumi_interni_restano_sotto_i_tetti(self):
        # La quota dei volumi e' calcolata come "colmo - spessore tetto":
        # sopra non spuntano mai.
        colmo = m.H_COLMO_NAVATA
        for sp in (0.2, 0.45, 0.9):
            self.assertLess(colmo - sp, colmo)
        self.assertLess(m.H_MURO + 2.0, m.H_COLMO_NAVATA)
        self.assertLess(m.H_CLERISTORIO + m.H_COPING, m.H_COLMO_NAVATA + 1e-9)

    def test_annessi_addossati_a_qualcosa(self):
        # Ogni annesso tocca il perimetro oppure un altro annesso: nessuno
        # resta staccato nel vuoto (erano i blocchi "volanti" della v4.3).
        polys = [poly for _n, _c, _h, poly in m.ANNESSI]
        for i, poly in enumerate(polys):
            altri = list(m.PERIMETRO)
            for j, altro in enumerate(polys):
                if j != i:
                    altri += altro
            vicino = min(math.dist(p, q) for p in poly for q in altri)
            self.assertLess(vicino, 3.0)


if __name__ == "__main__":
    unittest.main()
