import unittest
from core.player import Player
from core.checker import Ficha

class TestPlayer(unittest.TestCase):
    def test_creacion_color_valido(self):
        p1 = Player("blanca")
        p2 = Player("negra")
        self.assertEqual(p1.get_color(), "blanca")
        self.assertEqual(p2.get_color(), "negra")
        self.assertEqual(p1.get_total_fichas(), 15)

    def test_creacion_color_invalido(self):
        with self.assertRaises(ValueError):
            Player("rojo")

    def test_enviar_y_sacar_de_barra(self):
        p = Player("blanca")
        f = Ficha("blanca")
        p.enviar_a_barra(f)
        self.assertEqual(p.fichas_en_barra(), 1)
        ficha = p.sacar_de_barra()
        self.assertIsInstance(ficha, Ficha)
        self.assertEqual(p.fichas_en_barra(), 0)
        self.assertIsNone(p.sacar_de_barra())

    def test_sacar_del_tablero(self):
        p = Player("negra")
        f = Ficha("negra")
        p.sacar_del_tablero(f)
        self.assertEqual(p.fichas_fuera(), 1)
        self.assertTrue(f.esta_afuera())

    def test_fichas_restantes(self):
        p = Player("blanca")
        f1 = Ficha("blanca")
        f2 = Ficha("blanca")
        p.sacar_del_tablero(f1)
        p.sacar_del_tablero(f2)
        self.assertEqual(p.fichas_restantes(), 13)

if __name__ == '__main__':
    unittest.main()