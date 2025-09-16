import unittest
from core.player import Player

class TestPlayer(unittest.TestCase):
    def test_creacion_jugador(self):
        p = Player("blanca")
        self.assertEqual(p.get_color(), "blanca")
        self.assertEqual(p.get_total_fichas(), 15)

    def test_barra(self):
        p = Player("negra")
        p.enviar_a_barra()
        self.assertEqual(p.fichas_en_barra(), 1)
        p.sacar_de_barra()
        self.assertEqual(p.fichas_en_barra(), 0)

    def test_barra_devuelve_none(self):
        p = Player("negra")
        p.sacar_de_barra() 
        self.assertEqual(p.sacar_de_barra(), None)

    def test_fichas_fuera_y_restantes(self):
        p = Player("blanca")
        p.sacar_del_tablero()
        self.assertEqual(p.fichas_fuera(), 1)
        self.assertEqual(p.fichas_restantes(), 14)

    def test_color_invalido(self):
        with self.assertRaises(ValueError):
            Player("verde")