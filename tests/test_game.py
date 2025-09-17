import unittest
from core.game import BackgammonGame
from core.checker import Ficha

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.game = BackgammonGame()

    def test_turno_inicial(self):
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

    def test_cambiar_turno(self):
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "negra")
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

    def test_tirar_dados(self):
        valores = self.game.tirar_dados()
        self.assertTrue(all(1 <= v <= 6 for v in valores))
        self.assertIn(len(valores), [2, 4])

    def test_usar_valor_dado(self):
        valores = self.game.tirar_dados()
        v = valores[0]
        ocurrencias = valores.count(v)
        for _ in range(ocurrencias):
            self.assertTrue(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(99))

    def test_quedan_movimientos(self):
        self.game.tirar_dados()
        self.assertTrue(self.game.quedan_movimientos())
        while self.game.quedan_movimientos():
            v = self.game._dado.__valores__[0]
            self.game.usar_valor_dado(v)
        self.assertFalse(self.game.quedan_movimientos())

    def test_movimiento_valido(self):
        tablero = self.game._tablero
        ficha = Ficha("blanca", 0)
        tablero.__contenedor__[0] = [ficha]
        tablero.__contenedor__[1] = []
        self.assertTrue(self.game.movimiento_valido(0, 1))
        tablero.__contenedor__[1] = [Ficha("blanca", 1)]
        self.assertTrue(self.game.movimiento_valido(0, 1))
        tablero.__contenedor__[1] = [Ficha("negra", 1)]
        self.assertTrue(self.game.movimiento_valido(0, 1))
        tablero.__contenedor__[1] = [Ficha("negra", 1), Ficha("negra", 1)]
        self.assertFalse(self.game.movimiento_valido(0, 1))
        tablero.__contenedor__[0] = []
        self.assertFalse(self.game.movimiento_valido(0, 1))
        tablero.__contenedor__[0] = [Ficha("negra", 0)]
        self.assertFalse(self.game.movimiento_valido(0, 1))

    def test_mover_valido_y_captura(self):
        self.game.tirar_dados()
        tablero = self.game._tablero
        ficha_blanca = Ficha("blanca", 0)
        ficha_negra = Ficha("negra", 1)
        tablero.__contenedor__[0] = [ficha_blanca]
        tablero.__contenedor__[1] = [ficha_negra]
        self.game._dado.__valores__ = [1]
        self.game.mover(0, 1, 1)
        self.assertEqual(tablero.fichas_en_barra("negra"), 1)
        self.assertEqual(tablero.__contenedor__[1][0].obtener_color(), "blanca")

    def test_mover_invalido(self):
        self.game.tirar_dados()
        self.game._tablero.__contenedor__[0] = []
        self.game._dado.__valores__ = [1]
        with self.assertRaises(ValueError):
            self.game.mover(0, 1, 1)
        self.game._tablero.__contenedor__[0] = [Ficha("blanca", 0)]
        self.game._dado.__valores__ = [1]
        with self.assertRaises(ValueError):
            self.game.mover(0, 1, 2)

    def test_get_tablero(self):
        tablero = self.game.get_tablero()
        self.assertIsInstance(tablero, list)
        self.assertEqual(len(tablero), 24)

    def test_verificar_victoria(self):
        self.assertFalse(self.game.verificar_victoria())
        color = self.game._turno.get_color()
        self.game._turno.__fuera__.clear()
        for _ in range(self.game._turno.get_total_fichas()):
            self.game._turno.__fuera__.append(Ficha(color, None))
        self.assertTrue(self.game.verificar_victoria())

if __name__ == "__main__":
    unittest.main()