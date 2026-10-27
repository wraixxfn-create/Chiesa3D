import math
import unittest

import muri_esterni as m


class PiantaTest(unittest.TestCase):
    def test_aggancio_facciata_invariato(self):
        # Il perimetro nasce e muore sul retro della facciata da 30 m, con
        # due spalline di raccordo: la navata e' piu' stretta del fronte.
        self.assertEqual(m.PERIMETRO[0], (-m.X_SPALLA, m.Y_BACK_M))
        self.assertEqual(m.PERIMETRO[-1], (m.X_SPALLA, m.Y_BACK_M))
        self.assertEqual(m.PERIMETRO[1], (m.X_NAVATA_SX, m.Y_BACK_M))
        self.assertAlmostEqual(m.X_NAVATA_DX - m.X_NAVATA_SX, 25.87)
        self.assertAlmostEqual(2 * m.X_SPALLA + m.SPESSORE_MURO,
                               m.LARGHEZZA_FACCIATA)

    def test_continuita(self):
        # v4.4: i tratti sono indici dell'anello (i0, i1) e si susseguono
        # nell'ordine del perimetro, dal primo all'ultimo.
        self.assertEqual(m.TRATTI_MURO[0][2], 0)
        self.assertEqual(m.TRATTI_MURO[-1][3], len(m.PERIMETRO) - 1)
        for (_, _, _i0a, i1a), (_, _, i0b, _i1b) in zip(m.TRATTI_MURO,
                                                        m.TRATTI_MURO[1:]):
            self.assertEqual(i1a, i0b)

    def test_scala_uniforme(self):
        a = m.dalla_pianta_m(0, 0)
        b = m.dalla_pianta_m(100, 100)
        self.assertAlmostEqual(abs(b[0] - a[0]), abs(b[1] - a[1]))

    def test_conversione_pianta_reversibile(self):
        for punto in [(327.5, 820), (458, 501), (215, 478), (13, 101)]:
            x, y = m.dalla_pianta_m(*punto)
            px = (m.PIANTA_ASSE_X + x / m.K_PIANTA,
                  m.PIANTA_FACCIATA_Y - (y - m.Y_BACK_M) / m.K_PIANTA)
            self.assertAlmostEqual(px[0], punto[0])
            self.assertAlmostEqual(px[1], punto[1])

    def test_quote_perimetro_ufficiali(self):
        d = m.riepilogo_dimensioni()
        self.assertAlmostEqual(d["Larghezza esterna navata"], 27.37, places=2)
        self.assertAlmostEqual(d["Larghezza esterna transetto"], 57.48,
                               places=2)
        self.assertAlmostEqual(
            d["Lunghezza corpo (retro facciata->abside)"], 90.9, places=2)
        # Interni ufficiali: 24,37 m alle navate e 54,48 m alla crociera.
        self.assertAlmostEqual(d["Larghezza esterna navata"] -
                               2 * m.SPESSORE_MURO,
                               m.LARGHEZZA_INTERNA_NAVATA)
        self.assertAlmostEqual(d["Larghezza esterna transetto"] -
                               2 * m.SPESSORE_MURO,
                               m.LARGHEZZA_INTERNA_CROCIERA)
        self.assertAlmostEqual(d["Lunghezza corpo (retro facciata->abside)"] -
                               m.SPESSORE_MURO, m.LUNGHEZZA_INTERNA)
        self.assertLess(m.LARGHEZZA_CLERISTORIO,
                        d["Larghezza esterna navata"])

    def test_facciata_piu_larga_delle_fiancate(self):
        # Come nelle fotografie e nel modello di carta: il fronte da 30 m
        # aggetta sulle fiancate, non e' a filo con esse.
        self.assertGreater(m.LARGHEZZA_FACCIATA,
                           m.LARGHEZZA_INTERNA_NAVATA + 2 * m.SPESSORE_MURO)
        aggetto = m.riepilogo_dimensioni()["Aggetto facciata sulle fiancate"]
        self.assertAlmostEqual(aggetto, 1.315, places=2)

    def test_campanile_sul_fianco_destro_e_addossato(self):
        cx, cy = m.CAMPANILE_M
        _, cy_cupola = m.ESAGONO_M
        r = m.LATO_CAMPANILE / 2
        self.assertGreater(cx, m.X_NAVATA_DX)
        self.assertLess(cx - r, m.X_NAVATA_DX)  # addossato, non staccato
        self.assertGreater(cx + r, m.X_NAVATA_DX)
        self.assertLess(cy, cy_cupola)
        self.assertGreaterEqual(cy + r, m.Y_NAVATA_FINE - 1.0)
        self.assertLess(cy - r, m.Y_NAVATA_FINE)

    def test_cupola_sull_incrocio(self):
        cx, cy = m.ESAGONO_M
        self.assertAlmostEqual(cx, 0, delta=0.75)
        self.assertGreater(cy, m.Y_NAVATA_FINE)
        self.assertLess(cy, m.Y_CORO_INIZIO)
        self.assertGreater(m.R_TAMBURO, m.LATO_CAMPANILE)
        # Il tamburo copre l'esagono dei sei pilastroni (raggio ~10,6 m).
        self.assertGreater(m.R_TAMBURO, 10.6)
        self.assertAlmostEqual(cy - m.R_TAMBURO * math.sin(math.pi / 3),
                               m.Y_NAVATA_FINE, delta=0.8)
        self.assertLess(cy + m.R_TAMBURO * math.sin(math.pi / 3),
                        m.Y_CORO_INIZIO)


class AltezzeTest(unittest.TestCase):
    def test_gerarchia_delle_quote(self):
        self.assertLess(m.H_MURO, m.H_CLERISTORIO)
        self.assertLess(m.H_CLERISTORIO, m.H_COLMO_NAVATA)
        self.assertLess(m.H_COLMO_NAVATA, m.H_TAMBURO)
        self.assertLess(m.H_TAMBURO, m.H_CALOTTA)
        self.assertLess(m.H_CALOTTA, m.H_CUPOLA)
        self.assertLess(m.H_CUPOLA, m.H_CAMPANILE)
        self.assertLess(m.H_CAMPANILE, m.H_CAMPANILE_PUNTA)

    def test_rapporti_con_facciata_di_riferimento(self):
        self.assertAlmostEqual(m.H_CUPOLA / m.ALTEZZA_FACCIATA, 1.28)
        self.assertAlmostEqual(m.H_CAMPANILE_PUNTA / m.ALTEZZA_FACCIATA,
                               77 / 37.5)
        self.assertEqual(m.H_CUPOLA, 48.0)
        self.assertEqual(m.H_CAMPANILE_PUNTA, 77.0)

    def test_colmo_principale_allineato_alla_facciata(self):
        # La base del timpano centrale della facciata v3.9 e' a 23,95 m.
        self.assertAlmostEqual(m.H_COLMO_NAVATA, 23.95, delta=0.1)

    def test_riepilogo_usa_le_opzioni(self):
        h = m.riepilogo_altezze({"altezza_cupola": 49.5,
                                 "altezza_campanile_punta": 78.0})
        self.assertEqual(h["Cupola (croce compresa)"], 49.5)
        self.assertEqual(h["Campanile (punta centrale)"], 78.0)


if __name__ == "__main__":
    unittest.main()
