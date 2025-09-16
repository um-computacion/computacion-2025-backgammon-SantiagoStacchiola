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

    def test_valores_dados(self):
        g = BackgammonGame()
        g.tirar_dados()
        valores = g.get_valores_dados()
        self.assertTrue(all(1 <= v <= 6 for v in valores))
        self.assertIn(len(valores), [2, 4])
    
    def test_usar_dados(self):
        g = BackgammonGame()
        g.tirar_dados()
        valores = g.get_valores_dados()
        valor = valores[0]
        usado = g.usar_valor_dado(valor)
        self.assertTrue(usado)
        self.assertNotIn(valor, g.get_valores_dados())

    def test_mover(self):
        g = BackgammonGame()
        g.tirar_dados()
        valores = g.get_valores_dados()
        valor_dado = valores[0]
        origen = 0
        destino = origen + valor_dado
        # Asegura que hay una ficha del jugador en el origen
        g.get_tablero()[origen] = [g.get_turno().get_color()]
        g.mover(origen, destino, valor_dado)
        self.assertNotIn(valor_dado, g.get_valores_dados())

    def test_movimiento_valido(self):
        g = BackgammonGame()
        origen = 0
        destino = 2
        es_valido = g.movimiento_valido(origen, destino)
        self.assertIsInstance(es_valido, bool)

    def test_mover_movimiento_invalido(self):
        g = BackgammonGame()
        g.tirar_dados()
        valor_dado = g.get_valores_dados()[0]
        origen = 0
        destino = origen + valor_dado
        with self.assertRaises(ValueError):
            g.mover(origen, destino, valor_dado)

    def test_mover_dado_no_disponible(self):
        g = BackgammonGame()
        g.tirar_dados()
        valor_dado = max(g.get_valores_dados()) + 1  # Valor que seguro no está
        origen = 0
        destino = origen + valor_dado
        g.get_tablero()[origen] = [g.get_turno().get_color()]
        with self.assertRaises(ValueError):
            g.mover(origen, destino, valor_dado)

    def test_mover_captura_ficha(self):
        g = BackgammonGame()
        g.tirar_dados()
        valor_dado = g.get_valores_dados()[0]
        origen = 0
        destino = origen + valor_dado
        color = g.get_turno().get_color()
        rival = "negra" if color == "blanca" else "blanca"
        g.get_tablero()[origen] = [color]
        g.get_tablero()[destino] = [rival]
        g.mover(origen, destino, valor_dado)
        # La ficha rival debe haber sido removida del destino
        self.assertNotIn(rival, g.get_tablero()[destino])
        
    def test_cambio_turno(self):
        g = BackgammonGame()
        turno_inicial = g.get_turno()
        g.cambiar_turno()
        self.assertNotEqual(g.get_turno(), turno_inicial)

    def test_cambiar_turno_dos_veces(self):
        g = BackgammonGame()
        turno_inicial = g.get_turno()
        g.cambiar_turno()
        turno_segundo = g.get_turno()
        g.cambiar_turno()
        turno_tercero = g.get_turno()
        self.assertEqual(turno_tercero, turno_inicial)

    def test_quedan_movimientos(self):
        g = BackgammonGame()
        g.tirar_dados()
        self.assertTrue(g.quedan_movimientos())
        # Usar todos los valores
        for valor in list(g.get_valores_dados()):
            g.usar_valor_dado(valor)
        self.assertFalse(g.quedan_movimientos())

    def test_reset_dados_cambiar_turno(self):
        g = BackgammonGame()
        g.tirar_dados()
        g.cambiar_turno()
        self.assertEqual(g.get_valores_dados(), [])

    def test_verificar_victoria(self):
        g = BackgammonGame()
        jugador = g.get_turno()
        for _ in range(jugador.get_total_fichas()):
            jugador.sacar_del_tablero()
        self.assertTrue(g.verificar_victoria())