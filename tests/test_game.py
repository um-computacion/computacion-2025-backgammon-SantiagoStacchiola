"""Tests para la clase Game."""
# pylint: disable=missing-function-docstring,protected-access

import unittest
from core.game import BackgammonGame
from core.checker import Ficha
from core.player import Player
from core.excepcions import (DadoNoDisponibleError, PosicionVaciaError,
                            PosicionBloqueadaError, MovimientoColorError)

class TestGame(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Pruebas del flujo principal del juego."""

    def setUp(self):
        """Inicializa una nueva partida de backgammon antes de cada prueba."""
        self.game = BackgammonGame()

    def test_turno_inicial(self):
        """Verifica que el turno inicial sea del jugador con fichas blancas."""
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

    def test_cambiar_turno(self):
        """Verifica que los turnos roten correctamente entre jugadores."""
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "negra")
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

    def test_tirar_dados(self):
        """Prueba que los dados se tiren correctamente y den valores válidos."""
        valores = self.game.tirar_dados()
        self.assertTrue(all(1 <= v <= 6 for v in valores))
        self.assertIn(len(valores), [2, 4])

    def test_usar_valor_dado(self):
        """Verifica que se pueda usar el valor de un dado tirado."""
        valores = self.game.tirar_dados()
        v = valores[0]
        ocurrencias = valores.count(v)
        for _ in range(ocurrencias):
            self.assertTrue(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(99))

    def test_quedan_movimientos(self):
        """Verifica que queden movimientos disponibles mientras haya dados sin usar."""
        self.game.tirar_dados()
        self.assertTrue(self.game.quedan_movimientos())
        while self.game.quedan_movimientos():
            v = self.game._dado.__valores__[0]
            self.game.usar_valor_dado(v)
        self.assertFalse(self.game.quedan_movimientos())

    def test_movimiento_valido(self):
        """Prueba los diferentes escenarios de movimientos válidos e inválidos."""
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
        """Prueba un movimiento válido que resulta en captura de ficha."""
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
        """Prueba movimientos inválidos que deberían lanzar excepciones."""
        self.game.tirar_dados()
        self.game._tablero.__contenedor__[0] = []
        self.game._dado.__valores__ = [1]
        with self.assertRaises(PosicionVaciaError):
            self.game.mover(0, 1, 1)
        self.game._tablero.__contenedor__[0] = [Ficha("blanca", 0)]
        self.game._dado.__valores__ = [1]
        with self.assertRaises(DadoNoDisponibleError):
            self.game.mover(0, 1, 2)

    def test_get_tablero(self):
        """Verifica que el método get_tablero devuelva una representación correcta del tablero."""
        tablero = self.game.get_tablero()
        self.assertIsInstance(tablero, list)
        self.assertEqual(len(tablero), 24)

    def test_verificar_victoria(self):
        """Verifica la condición de victoria para un jugador."""
        self.assertFalse(self.game.verificar_victoria())
        color = self.game._turno.get_color()
        self.game._turno.__fuera__.clear()
        for _ in range(self.game._turno.get_total_fichas()):
            self.game._turno.__fuera__.append(Ficha(color, None))
        self.assertTrue(self.game.verificar_victoria())

    def test_tirar_dados_sin_metodo(self):
        """Prueba el error cuando el dado no tiene método de tirada."""
        class DadoSinMetodo:  # pylint: disable=too-few-public-methods
            """Mock de dado sin métodos."""

        self.game._dado = DadoSinMetodo()
        with self.assertRaises(AttributeError):
            self.game.tirar_dados()

    def test_movimiento_fichas_negras(self):
        """Prueba movimientos con fichas negras."""
        self.game.cambiar_turno()  # Cambiar a jugador negro
        tablero = self.game._tablero
        ficha_negra = Ficha("negra", 23)
        tablero.__contenedor__[23] = [ficha_negra]
        tablero.__contenedor__[22] = []
        self.assertTrue(self.game.movimiento_valido(23, 22))

    def test_game_con_jugadores_personalizados(self):
        """Prueba la creación del juego con jugadores específicos."""
        p1 = Player("blanca")
        p2 = Player("negra")
        game = BackgammonGame(p1, p2)
        self.assertEqual(game.get_turno().get_color(), "blanca")

    def test_siguiente_turno(self):
        """Prueba el método siguiente_turno."""
        color_inicial = self.game.get_turno().get_color()
        self.game.siguiente_turno()
        color_despues = self.game.get_turno().get_color()
        self.assertNotEqual(color_inicial, color_despues)

    def test_atributo_estado(self):
        """Prueba que el atributo _state se actualiza correctamente."""
        self.assertEqual(self.game._state, "initialized")
        self.game.siguiente_turno()
        self.assertEqual(self.game._state, "waiting")

    def test_tirar_dados_con_metodo_roll(self):
        """Prueba tirar dados usando el método roll."""
        # Eliminar el método tirar para forzar uso de roll
        if hasattr(self.game._dado, 'tirar'):
            delattr(self.game._dado.__class__, 'tirar')
        valores = self.game.tirar_dados()
        self.assertIsInstance(valores, list)

    def test_constructor_con_un_jugador(self):
        """Prueba constructor con solo un jugador."""
        p1 = Player("blanca")
        # Solo pasamos player1, player2 debería ser None y luego creado automáticamente
        game = BackgammonGame(p1, None)
        self.assertEqual(game.get_turno().get_color(), "blanca")

    def test_constructor_sin_jugadores(self):
        """Prueba constructor sin jugadores (valores None)."""
        game = BackgammonGame(None, None)
        self.assertEqual(game.get_turno().get_color(), "blanca")

    def test_tirar_dados_sin_metodos(self):
        """Prueba cuando el dado no tiene ni tirar ni roll."""
        class DadoSinNingunMetodo:  # pylint: disable=too-few-public-methods
            """Mock de dado sin ningún método."""

            def __init__(self):
                self.__valores__ = []

        self.game._dado = DadoSinNingunMetodo()
        with self.assertRaises(AttributeError):
            self.game.tirar_dados()

    def test_mover_sin_captura(self):
        """Prueba movimiento válido sin captura para cubrir todas las ramas."""
        self.game.tirar_dados()
        tablero = self.game._tablero
        ficha_blanca = Ficha("blanca", 0)
        tablero.__contenedor__[0] = [ficha_blanca]
        tablero.__contenedor__[1] = []  # Posición vacía, no hay captura
        # pylint: disable=attribute-defined-outside-init
        self.game._dado.__valores__ = [1]

        # Este movimiento no debería generar captura
        self.game.mover(0, 1, 1)
        self.assertEqual(tablero.fichas_en_barra("negra"), 0)  # No hay capturas
        self.assertEqual(tablero.__contenedor__[1][0].obtener_color(), "blanca")

    def test_verificar_victoria_sin_jugador_ganador(self):
        """Prueba verificación de victoria cuando no hay ganador."""
        # Asegurar que el jugador tiene fichas restantes
        jugador_actual = self.game.get_turno()
        self.assertGreater(jugador_actual.fichas_restantes(), 0)
        self.assertFalse(self.game.verificar_victoria())

    def test_mover_posicion_bloqueada(self):
        """Prueba movimiento a posición bloqueada por fichas enemigas."""
        self.game.tirar_dados()
        tablero = self.game._tablero
        ficha_blanca = Ficha("blanca", 0)
        ficha_negra1 = Ficha("negra", 1)
        ficha_negra2 = Ficha("negra", 1)
        tablero.__contenedor__[0] = [ficha_blanca]
        tablero.__contenedor__[1] = [ficha_negra1, ficha_negra2]  # Posición bloqueada
        # pylint: disable=attribute-defined-outside-init
        self.game._dado.__valores__ = [1]
        with self.assertRaises(PosicionBloqueadaError):
            self.game.mover(0, 1, 1)

    def test_mover_ficha_color_incorrecto(self):
        """Prueba movimiento de ficha del color incorrecto."""
        self.game.tirar_dados()
        tablero = self.game._tablero
        ficha_negra = Ficha("negra", 0)  # Ficha negra en turno de blancas
        tablero.__contenedor__[0] = [ficha_negra]
        tablero.__contenedor__[1] = []
        # pylint: disable=attribute-defined-outside-init
        self.game._dado.__valores__ = [1]
        with self.assertRaises(MovimientoColorError):
            self.game.mover(0, 1, 1)


if __name__ == "__main__":
    unittest.main()
# EOF