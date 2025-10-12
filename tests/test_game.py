"""Tests para la clase Game."""
# pylint: disable=missing-function-docstring,protected-access

import unittest
from unittest.mock import patch
from core.game import BackgammonGame
from core.checker import Ficha
from core.player import Player
from core.excepcions import (DadoNoDisponibleError, PosicionVaciaError,
                           PosicionBloqueadaError, MovimientoColorError,
                           MovimientoInvalidoError)


class TestGame(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Pruebas del flujo principal del juego."""

    def setUp(self):
        """Inicializa una nueva partida de backgammon antes de cada prueba."""
        self.game = BackgammonGame()

    def test_inicializacion_y_constructores(self):
        """Prueba la inicialización del juego y constructores."""
        # Constructor por defecto
        self.assertEqual(self.game.get_turno().get_color(), "blanca")
        self.assertEqual(self.game.__state__, "initialized")

        # Constructor con jugadores personalizados
        p1 = Player("blanca")
        p2 = Player("negra")
        game = BackgammonGame(p1, p2)
        self.assertEqual(game.get_turno().get_color(), "blanca")

        # Constructor con un jugador None
        game2 = BackgammonGame(p1, None)
        self.assertEqual(game2.get_turno().get_color(), "blanca")

        # Constructor con ambos None
        game3 = BackgammonGame(None, None)
        self.assertEqual(game3.get_turno().get_color(), "blanca")

    def test_turnos_y_estados(self):
        """Prueba el manejo de turnos y estados del juego."""
        # Turno inicial
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

        # Cambiar turno
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "negra")
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_turno().get_color(), "blanca")

        # Siguiente turno y estado
        color_inicial = self.game.get_turno().get_color()
        self.game.siguiente_turno()
        self.assertEqual(self.game.__state__, "waiting")
        self.assertNotEqual(color_inicial, self.game.get_turno().get_color())

        # Alias next_turn
        color_antes = self.game.get_turno().get_color()
        self.game.next_turn()
        self.assertNotEqual(color_antes, self.game.get_turno().get_color())

    def test_dados_completo(self):
        """Prueba completa de la funcionalidad de dados."""
        # Tirar dados básico
        valores = self.game.tirar_dados()
        self.assertTrue(all(1 <= v <= 6 for v in valores))
        self.assertIn(len(valores), [2, 4])

        # Usar valores de dados
        v = valores[0]
        ocurrencias = valores.count(v)
        for _ in range(ocurrencias):
            self.assertTrue(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(v))
        self.assertFalse(self.game.usar_valor_dado(99))

        # Quedan movimientos
        self.game.tirar_dados()
        self.assertTrue(self.game.quedan_movimientos())
        while self.game.quedan_movimientos():
            v = self.game.__dado__.__valores__[0]
            self.game.usar_valor_dado(v)
        self.assertFalse(self.game.quedan_movimientos())

    def test_movimiento_valido_completo(self):
        """Prueba exhaustiva del método movimiento_valido."""
        tablero = self.game.__tablero__

        # Caso: origen vacío
        tablero.__contenedor__[0] = []
        self.assertFalse(self.game.movimiento_valido(0, 1))

        # Caso: ficha color incorrecto
        tablero.__contenedor__[0] = [Ficha("negra", 0)]  # Turno de blancas
        self.assertFalse(self.game.movimiento_valido(0, 1))

        # Configurar ficha correcta para siguientes tests
        tablero.__contenedor__[0] = [Ficha("blanca", 0)]

        # Caso: destino vacío (válido)
        tablero.__contenedor__[1] = []
        self.assertTrue(self.game.movimiento_valido(0, 1))

        # Caso: destino con mismo color (válido)
        tablero.__contenedor__[1] = [Ficha("blanca", 1)]
        self.assertTrue(self.game.movimiento_valido(0, 1))

        # Caso: destino con una ficha enemiga (válido - captura)
        tablero.__contenedor__[1] = [Ficha("negra", 1)]
        self.assertTrue(self.game.movimiento_valido(0, 1))

        # Caso: destino bloqueado por 2+ fichas enemigas (inválido)
        tablero.__contenedor__[1] = [Ficha("negra", 1), Ficha("negra", 1)]
        self.assertFalse(self.game.movimiento_valido(0, 1))

        # Test con fichas negras
        self.game.cambiar_turno()  # Cambiar a jugador negro
        ficha_negra = Ficha("negra", 23)
        tablero.__contenedor__[23] = [ficha_negra]
        tablero.__contenedor__[22] = []
        self.assertTrue(self.game.movimiento_valido(23, 22))

    def test_movimientos_y_excepciones(self):
        """Prueba movimientos válidos e inválidos con todas las excepciones."""
        self.game.tirar_dados()
        tablero = self.game.__tablero__

        # MovimientoInvalidoError (usando mock)
        ficha_blanca = Ficha("blanca", 0)
        tablero.__contenedor__[0] = [ficha_blanca]
        tablero.__contenedor__[1] = []
        self.game.__dado__.__valores__ = [1]

        original_movimiento_valido = self.game.movimiento_valido
        self.game.movimiento_valido = lambda o, d: False
        try:
            with self.assertRaises(MovimientoInvalidoError):
                self.game.mover(0, 1, 1)
        finally:
            self.game.movimiento_valido = original_movimiento_valido

        # PosicionVaciaError
        tablero.__contenedor__[0] = []
        self.game.__dado__.__valores__ = [1]
        with self.assertRaises(PosicionVaciaError):
            self.game.mover(0, 1, 1)

        # DadoNoDisponibleError
        tablero.__contenedor__[0] = [Ficha("blanca", 0)]
        self.game.__dado__.__valores__ = [1]
        with self.assertRaises(DadoNoDisponibleError):
            self.game.mover(0, 1, 2)

        # MovimientoColorError
        tablero.__contenedor__[0] = [Ficha("negra", 0)]  # Ficha negra en turno de blancas
        self.game.__dado__.__valores__ = [1]
        with self.assertRaises(MovimientoColorError):
            self.game.mover(0, 1, 1)

        # PosicionBloqueadaError
        tablero.__contenedor__[0] = [Ficha("blanca", 0)]
        tablero.__contenedor__[1] = [Ficha("negra", 1), Ficha("negra", 1)]
        self.game.__dado__.__valores__ = [1]
        with self.assertRaises(PosicionBloqueadaError):
            self.game.mover(0, 1, 1)

    def test_movimientos_validos_y_capturas(self):
        """Prueba movimientos válidos incluyendo capturas."""
        self.game.tirar_dados()
        tablero = self.game.__tablero__

        # Movimiento sin captura
        ficha_blanca = Ficha("blanca", 0)
        tablero.__contenedor__[0] = [ficha_blanca]
        tablero.__contenedor__[1] = []
        self.game.__dado__.__valores__ = [1]
        self.game.mover(0, 1, 1)
        self.assertEqual(tablero.fichas_en_barra("negra"), 0)
        self.assertEqual(tablero.__contenedor__[1][0].obtener_color(), "blanca")

        # Reset para test de captura
        tablero.__contenedor__[0] = [Ficha("blanca", 0)]
        tablero.__contenedor__[1] = [Ficha("negra", 1)]
        tablero.__barra_blancas__.clear()
        tablero.__barra_negras__.clear()
        self.game.__dado__.__valores__ = [1]

        # Movimiento con captura
        self.game.mover(0, 1, 1)
        self.assertEqual(tablero.fichas_en_barra("negra"), 1)
        self.assertEqual(tablero.__contenedor__[1][0].obtener_color(), "blanca")

        # Movimiento a posición con mismo color
        tablero.__contenedor__[2] = [Ficha("blanca", 2)]
        tablero.__contenedor__[3] = [Ficha("blanca", 3)]
        self.game.__dado__.__valores__ = [1]
        self.game.mover(2, 3, 1)
        self.assertEqual(len(tablero.__contenedor__[3]), 2)

    def test_victoria_y_tablero(self):
        """Prueba verificación de victoria y obtención del tablero."""
        # Verificar victoria inicial (False)
        self.assertFalse(self.game.verificar_victoria())
        jugador_actual = self.game.get_turno()
        self.assertGreater(jugador_actual.fichas_restantes(), 0)

        # Simular victoria
        color = jugador_actual.get_color()
        jugador_actual.__fuera__.clear()
        for _ in range(jugador_actual.get_total_fichas()):
            jugador_actual.__fuera__.append(Ficha(color, None))
        self.assertTrue(self.game.verificar_victoria())

        # Obtener tablero
        tablero = self.game.get_tablero()
        self.assertIsInstance(tablero, list)
        self.assertEqual(len(tablero), 24)

    def test_nuevos_metodos_ui(self):
        """Test básico de los nuevos métodos de UI."""

        # Crear game específico para estos tests
        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Test mostrar_dados_disponibles
        resultado = game.mostrar_dados_disponibles()
        self.assertIn("No hay dados disponibles", resultado)

        # Test mostrar_turno_actual
        resultado = game.mostrar_turno_actual()
        self.assertIn("Turno del jugador: BLANCA", resultado)

        # Test obtener_opciones_movimiento
        opciones = game.obtener_opciones_movimiento()
        self.assertIsInstance(opciones, list)
        self.assertTrue(len(opciones) > 0)

    def test_todas_fichas_en_home_basico(self):
        """Test básico de todas_fichas_en_home."""

        game = BackgammonGame(Player("blanca"), Player("negra"))
        jugador = game.get_turno()

        # Al inicio, no todas las fichas están en home
        self.assertFalse(game.todas_fichas_en_home(jugador))

        # Test con jugador None (usa turno actual)
        self.assertFalse(game.todas_fichas_en_home())

    def test_procesar_entrada_usuario_basico(self):
        """Test básico del procesamiento de entrada."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Test quit
        movimiento, error = game.procesar_entrada_usuario("quit")
        self.assertEqual(movimiento, "quit")
        self.assertIsNone(error)

        # Test pass
        movimiento, error = game.procesar_entrada_usuario("pass")
        self.assertEqual(movimiento, "pass")
        self.assertIsNone(error)

        # Test formato inválido
        movimiento, error = game.procesar_entrada_usuario("1,2")
        self.assertIsNone(movimiento)
        self.assertIn("Error: Use formato origen,destino,dado", error)

    def test_ejecutar_movimiento_barra_casos(self):
        """Test de ejecutar_movimiento_barra con diferentes casos."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Sin fichas en barra, debería fallar
        exito, mensaje = game.ejecutar_movimiento_barra(5, 3)
        self.assertFalse(exito)
        self.assertIn("No tienes fichas en la barra", mensaje)

    def test_ejecutar_bearing_off_casos(self):
        """Test de ejecutar_bearing_off con diferentes casos."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Sin todas las fichas en home, debería fallar
        exito, mensaje = game.ejecutar_bearing_off(20, 3)
        self.assertFalse(exito)
        self.assertIn("Todas las fichas deben estar en el home board", mensaje)

    def test_ejecutar_movimiento_completo_casos(self):
        """Test de ejecutar_movimiento_completo con diferentes casos."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Test movimiento desde barra sin fichas
        exito, mensaje = game.ejecutar_movimiento_completo("barra", 5, 3)
        self.assertFalse(exito)
        self.assertIn("✗", mensaje)

        # Test bearing off sin estar en home
        exito, mensaje = game.ejecutar_movimiento_completo(18, "off", 3)
        self.assertFalse(exito)
        self.assertIn("✗", mensaje)

    def test_verificar_fin_juego_completo_casos(self):
        """Test de verificar_fin_juego_completo."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Al inicio, juego no ha terminado
        self.assertFalse(game.verificar_fin_juego_completo())

    def test_obtener_entrada_usuario_con_opciones(self):
        """Test de obtener_entrada_usuario mostrando opciones."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Mock la entrada del usuario
        with patch('builtins.input', return_value='test'):
            with patch('builtins.print'):
                entrada = game.obtener_entrada_usuario()
                self.assertEqual(entrada, "test")

    def test_mostrar_estado_juego_completo(self):
        """Test completo de mostrar_estado_juego."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Usar mock para capturar las llamadas a print
        with patch('builtins.print') as mock_print:
            game.mostrar_estado_juego()
            # Verificar que se llamó a print
            mock_print.assert_called()
            # Verificar que se imprimió información del tablero
            llamadas = [str(call) for call in mock_print.call_args_list]
            output = '\n'.join(llamadas)
            self.assertIn("TABLERO", output.upper())

    def test_procesar_entrada_usuario_completo(self):
        """Test completo del procesamiento de entrada del usuario."""

        game = BackgammonGame(Player("blanca"), Player("negra"))

        # Test ValueError
        movimiento, error = game.procesar_entrada_usuario("a,b,c")
        self.assertIsNone(movimiento)
        self.assertIn("Error: Ingrese números válidos", error)

        # Test movimiento normal
        movimiento, error = game.procesar_entrada_usuario("1,7,6")
        self.assertEqual(movimiento, (0, 6, 6))
        self.assertIsNone(error)

        # Test barra
        movimiento, error = game.procesar_entrada_usuario("barra,3,2")
        self.assertEqual(movimiento, ("barra", 2, 2))
        self.assertIsNone(error)

        # Test bearing off
        movimiento, error = game.procesar_entrada_usuario("19,off,3")
        self.assertEqual(movimiento, (18, "off", 3))
        self.assertIsNone(error)

    def test_turno_completo_casos_especiales(self):
        """Test de casos especiales en turno_completo."""
        # Mock dados para simular comportamiento
        with patch.object(self.game, 'tirar_dados'):
            with patch.object(self.game, 'obtener_entrada_usuario', return_value='salir'):
                with patch('builtins.print'):
                    # El método debe manejar la salida del turno correctamente
                    result = self.game.turno_completo()
                    # Verificar que el método retornó
                    self.assertIsNotNone(result)

    def test_validar_entrada_movimiento(self):
        """Test de validación de entrada de movimiento."""
        # Entradas válidas
        valido, resultado = self.game.validar_entrada_movimiento("5-11")
        self.assertTrue(valido)
        self.assertEqual(resultado, (5, 11))

        valido, resultado = self.game.validar_entrada_movimiento("barra-3")
        self.assertTrue(valido)
        self.assertEqual(resultado, ("barra", 3))

        valido, resultado = self.game.validar_entrada_movimiento("20-afuera")
        self.assertTrue(valido)
        self.assertEqual(resultado, (20, "afuera"))

        # Comandos especiales
        valido, resultado = self.game.validar_entrada_movimiento("help")
        self.assertTrue(valido)
        self.assertEqual(resultado, "comando_especial")

        # Entradas inválidas
        valido, _ = self.game.validar_entrada_movimiento("")
        self.assertFalse(valido)

        valido, _ = self.game.validar_entrada_movimiento("abc")
        self.assertFalse(valido)

        valido, _ = self.game.validar_entrada_movimiento("25-30")
        self.assertFalse(valido)

    def test_validar_movimiento_legal(self):
        """Test de validación de movimientos legales."""
        dados_disponibles = [1, 2, 3, 4, 5, 6]

        # Agregar una ficha blanca en posición 5 para el test
        ficha_test = Ficha("blanca", 5)
        self.game.get_tablero()[4].append(ficha_test)  # posición 5 es índice 4

        # Test con posiciones válidas
        valido, _ = self.game.validar_movimiento_legal(5, 11, dados_disponibles)
        # Debería ser válido si hay un dado de 6 disponible
        self.assertTrue(valido)

        # Test con dado no disponible
        valido, mensaje = self.game.validar_movimiento_legal(5, 12, [1, 2, 3])
        self.assertFalse(valido)
        self.assertIn("No tiene un dado", mensaje)

    def test_mostrar_ayuda_movimientos(self):
        """Test de mostrar ayuda de movimientos."""
        with patch('builtins.print') as mock_print:
            self.game.mostrar_ayuda_movimientos()
            # Verificar que se imprimió ayuda
            mock_print.assert_called()
            # Verificar que contiene información útil
            llamadas = [call[0][0] for call in mock_print.call_args_list]
            ayuda_completa = '\n'.join(llamadas)
            self.assertIn("AYUDA", ayuda_completa)
            self.assertIn("origen-destino", ayuda_completa)
            self.assertIn("5-11", ayuda_completa)

    def test_procesar_entrada_usuario_validada(self):
        """Test de procesamiento validado de entrada de usuario."""
        dados_disponibles = [1, 2, 3, 4, 5, 6]

        # Test comando especial
        with patch('builtins.print'):
            resultado = self.game.procesar_entrada_usuario_validada("help", dados_disponibles)
            self.assertEqual(resultado, "comando_especial")

        # Test entrada inválida
        with patch('builtins.print'):
            resultado = self.game.procesar_entrada_usuario_validada(
                "formato-incorrecto", dados_disponibles)
            self.assertIsNone(resultado)

        # Test movimiento válido
        with patch.object(self.game, 'validar_movimiento_legal', return_value=(True, "válido")):
            resultado = self.game.procesar_entrada_usuario_validada("5-11", dados_disponibles)
            self.assertIsNotNone(resultado)
            self.assertEqual(resultado[0], 5)  # origen
            self.assertEqual(resultado[1], 11)  # destino


if __name__ == '__main__':
    unittest.main()
# EOF
