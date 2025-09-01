import unittest
from core.game import BackgammonGame

class TestGame(unittest.TestCase):
    def test_creacion_juego(self):
        g = BackgammonGame()
        self.assertEqual(g.get_turno().get_color(), "blanca")
        self.assertEqual(len(g.get_tablero()), 24)

    def test_tirada_dados(self):
        g = BackgammonGame()
        tirada = g.tirar_dados()
        self.assertIn(len(tirada), [2, 4])

    def test_movimiento_valido_y_mover(self):
        g = BackgammonGame()
        g.get_valores_dados() == [1]  # simular dado disponible
        if g.movimiento_valido(11, 10):  # blancas de 11 → 10
            g.mover(11, 10, 1)
            self.assertEqual(g.get_tablero()[10][0], "blanca")

    def test_cambio_turno(self):
        g = BackgammonGame()
        turno_inicial = g.get_turno()
        g.cambiar_turno()
        self.assertNotEqual(g.get_turno(), turno_inicial)
