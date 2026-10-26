import unittest
import muri_esterni as m

class PiantaTest(unittest.TestCase):
    def test_aggancio(self):
        self.assertEqual(m.PERIMETRO_PX[0], (124,333))
        self.assertEqual(m.PERIMETRO_PX[-1], (209,333))
    def test_continuita(self):
        tratti = [m.TRATTI_MURO[i][2] for i in [0,2,3,4,5,6,1]]
        for a,b in zip(tratti,tratti[1:]):
            self.assertEqual(a[-1],b[0])
    def test_scala_uniforme(self):
        a=m.dalla_pianta(0,0); b=m.dalla_pianta(100,100)
        self.assertAlmostEqual(b[0]-a[0],b[1]-a[1])
    def test_campanile(self):
        self.assertGreater(m.CAMPANILE_PX[0],209)
        self.assertGreater(m.CAMPANILE_PX[1],m.ESAGONO_PX[1])

if __name__ == '__main__': unittest.main()
