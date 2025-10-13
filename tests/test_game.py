"""Tests para la clase Juego."""
# pylint: disable=missing-function-docstring,protected-access

import unittest
from unittest.mock import patch
from core.game import Game
from core.checker import Ficha
from core.player import Player
from core.excepcions import (DadoNoDisponibleError, PosicionVaciaError,
                           PosicionBloqueadaError, MovimientoColorError,
                           MovimientoInvalidoError)


class TestGame(unittest.TestCase):  # pylint: disable=too-many-public-methods
    """Pruebas del flujo principal del juego."""

    def setUp(self):
        """Inicializa una nueva partida de backgammon antes de cada prueba."""
        self.game = Game()

    def test_inicializacion_y_constructores(self):
        """Prueba la inicialización del juego y constructores."""
        # Constructor por defecto
        self.assertEqual(self.game.get_turno().get_color(), "blanca")
        self.assertEqual(self.game.__state__, "initialized")

        # Constructor con jugadores personalizados
        p1 = Player("blanca")
        p2 = Player("negra")
        game = Game(p1, p2)
        self.assertEqual(game.get_turno().get_color(), "blanca")

        # Constructor con un jugador None
        game2 = Game(p1, None)
        self.assertEqual(game2.get_turno().get_color(), "blanca")

        # Constructor con ambos None
        game3 = Game(None, None)
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
        game = Game(Player("blanca"), Player("negra"))

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

        game = Game(Player("blanca"), Player("negra"))
        jugador = game.get_turno()

        # Al inicio, no todas las fichas están en home
        self.assertFalse(game.todas_fichas_en_home(jugador))

        # Test con jugador None (usa turno actual)
        self.assertFalse(game.todas_fichas_en_home())

    def test_procesar_entrada_usuario_basico(self):
        """Test básico del procesamiento de entrada."""

        game = Game(Player("blanca"), Player("negra"))

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

        game = Game(Player("blanca"), Player("negra"))

        # Sin fichas en barra, debería fallar
        exito, mensaje = game.ejecutar_movimiento_barra(5, 3)
        self.assertFalse(exito)
        self.assertIn("No tienes fichas en la barra", mensaje)

    def test_ejecutar_bearing_off_casos(self):
        """Test de ejecutar_bearing_off con diferentes casos."""

        game = Game(Player("blanca"), Player("negra"))

        # Sin todas las fichas en home, debería fallar
        exito, mensaje = game.ejecutar_bearing_off(20, 3)
        self.assertFalse(exito)
        self.assertIn("Todas las fichas deben estar en el tablero local", mensaje)

    def test_ejecutar_movimiento_completo_casos(self):
        """Test de ejecutar_movimiento_completo con diferentes casos."""

        game = Game(Player("blanca"), Player("negra"))

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

        game = Game(Player("blanca"), Player("negra"))

        # Al inicio, juego no ha terminado
        self.assertFalse(game.verificar_fin_juego_completo())

    def test_obtener_entrada_usuario_con_opciones(self):
        """Test de obtener_entrada_usuario mostrando opciones."""

        game = Game(Player("blanca"), Player("negra"))

        # Mock la entrada del usuario
        with patch('builtins.input', return_value='test'):
            with patch('builtins.print'):
                entrada = game.obtener_entrada_usuario()
                self.assertEqual(entrada, "test")

    def test_mostrar_estado_juego_completo(self):
        """Test completo de mostrar_estado_juego."""

        game = Game(Player("blanca"), Player("negra"))

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

        game = Game(Player("blanca"), Player("negra"))

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

    def test_turno_completo_con_quit(self):
        """Test de turno_completo cuando el usuario escribe quit."""
        with patch('builtins.input', return_value='quit'), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', return_value=True), \
             patch('builtins.print'):
            self.assertEqual(self.game.turno_completo(), 'quit')

    def test_turno_completo_sin_movimientos(self):
        """Test de turno_completo cuando no quedan movimientos."""
        with patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', return_value=False), \
             patch('builtins.print') as mock_print:
            self.assertTrue(self.game.turno_completo())
            mock_print.assert_any_call("No hay movimientos disponibles. Pasando turno...")

    def test_turno_completo_con_pass(self):
        """Test de turno_completo cuando el usuario pasa el turno."""
        with patch('builtins.input', return_value='pass'), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', return_value=True), \
             patch.object(self.game, 'procesar_entrada_usuario', return_value=('pass', None)), \
             patch('builtins.print') as mock_print:
            self.assertTrue(self.game.turno_completo())
            mock_print.assert_any_call("Pasando turno...")

    def test_turno_completo_movimiento_exitoso(self):
        """Test de turno_completo con movimiento exitoso."""
        with patch('builtins.input', side_effect=['1,2,1', 'pass']), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', side_effect=[True, True, False]), \
             patch.object(self.game, 'procesar_entrada_usuario', side_effect=[((0, 1, 1), None), ('pass', None)]), \
             patch.object(self.game, 'ejecutar_movimiento_completo', return_value=(True, "Movimiento exitoso")), \
             patch.object(self.game, 'verificar_fin_juego_completo', return_value=False), \
             patch('builtins.print'):
            self.assertTrue(self.game.turno_completo())

    def test_turno_completo_fin_de_juego(self):
        """Test de turno_completo que termina el juego."""
        with patch('builtins.input', return_value='1,2,1'), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', return_value=True), \
             patch.object(self.game, 'procesar_entrada_usuario', return_value=((0, 1, 1), None)), \
             patch.object(self.game, 'ejecutar_movimiento_completo', return_value=(True, "Movimiento exitoso")), \
             patch.object(self.game, 'verificar_fin_juego_completo', return_value=True), \
             patch('builtins.print'):
            self.assertEqual(self.game.turno_completo(), 'fin')

    def test_validar_entrada_movimiento_casos_especiales(self):
        """Test de validar_entrada_movimiento con comandos especiales."""
        for comando in ["salir", "exit", "quit", "help", "ayuda"]:
            resultado = self.game.validar_entrada_movimiento(comando)
            self.assertEqual(resultado, (True, "comando_especial"))

    def test_validar_entrada_movimiento_formatos_incorrectos(self):
        """Test de validar_entrada_movimiento con formatos incorrectos."""
        casos = [
            ("12", "Formato incorrecto. Use: origen-destino (ej: 5-11)"),
            ("1-2-3", "Formato incorrecto. Use: origen-destino"),
            ("25-5", "Posición origen debe estar entre 0-24 o 'barra'"),
            ("abc-5", "Posición origen debe ser un número o 'barra'"),
            ("5-25", "Posición destino debe estar entre 0-24 o 'afuera'"),
            ("5-abc", "Posición destino debe ser un número o 'afuera'")
        ]
        for entrada, mensaje_esperado in casos:
            resultado = self.game.validar_entrada_movimiento(entrada)
            self.assertEqual(resultado, (False, mensaje_esperado))

    def test_validar_entrada_movimiento_casos_validos(self):
        """Test de validar_entrada_movimiento con entradas válidas."""
        casos = [
            ("5-11", (5, 11)),
            ("barra-5", ("barra", 5)),
            ("20-afuera", (20, "afuera")),
            ("0-24", (0, 24))
        ]
        for entrada, esperado in casos:
            resultado = self.game.validar_entrada_movimiento(entrada)
            self.assertEqual(resultado, (True, esperado))

    def test_procesar_entrada_usuario_casos_basicos(self):
        """Test de procesar_entrada_usuario con casos básicos."""
        casos = [
            ("entrada_invalida", (None, "Error: Use formato origen,destino,dado")),
            ("quit", ("quit", None)),
            ("pass", ("pass", None)),
            ("1,2,1", ((0, 1, 1), None)),
            ("barra,5,4", (("barra", 4, 4), None)),
            ("20,off,4", ((19, "off", 4), None)),
            ("abc,def,ghi", (None, "Error: Ingrese números válidos"))
        ]
        for entrada, esperado in casos:
            resultado = self.game.procesar_entrada_usuario(entrada)
            self.assertEqual(resultado, esperado)

    def test_obtener_entrada_usuario_sin_opciones(self):
        """Test de obtener_entrada_usuario sin opciones."""
        with patch('builtins.input', return_value='entrada_libre'), \
             patch.object(self.game, 'obtener_opciones_movimiento', return_value=['opcion1', 'opcion2']), \
             patch('builtins.print') as mock_print:
            resultado = self.game.obtener_entrada_usuario()
            self.assertEqual(resultado, 'entrada_libre')
            mock_print.assert_any_call("\nOpciones:")

    def test_mostrar_ayuda_movimientos_completa(self):
        """Test completo de mostrar_ayuda_movimientos."""
        with patch('builtins.print') as mock_print:
            self.game.mostrar_ayuda_movimientos()
            
            # Verificar que se imprimen las líneas esperadas
            calls = [call.args[0] for call in mock_print.call_args_list]
            self.assertIn("\n=== AYUDA DE MOVIMIENTOS ===", calls)
            self.assertIn("Formato: origen-destino", calls)
            self.assertIn("Ejemplos:", calls)

    def test_tirar_dados_diferentes_metodos(self):
        """Test de tirar_dados con diferentes tipos de dados."""
        # Método tirar
        with patch.object(self.game, '__dado__') as mock_dado:
            mock_dado.tirar.return_value = [3, 4]
            del mock_dado.roll
            resultado = self.game.tirar_dados()
            self.assertEqual(resultado, [3, 4])
            mock_dado.tirar.assert_called_once()

        # Método roll
        with patch.object(self.game, '__dado__') as mock_dado:
            del mock_dado.tirar
            mock_dado.roll.return_value = [5, 6]
            resultado = self.game.tirar_dados()
            self.assertEqual(resultado, [5, 6])
            mock_dado.roll.assert_called_once()

        # Sin método conocido
        with patch.object(self.game, '__dado__') as mock_dado:
            del mock_dado.tirar
            del mock_dado.roll
            with self.assertRaises(AttributeError) as context:
                self.game.tirar_dados()
            self.assertIn("no expone método de tirada conocido", str(context.exception))

    def test_turno_completo_casos_error(self):
        """Test de turno_completo con diferentes tipos de errores."""
        # Movimiento None
        with patch('builtins.input', side_effect=['entrada_invalida', 'pass']), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', side_effect=[True, True, False]), \
             patch.object(self.game, 'procesar_entrada_usuario', side_effect=[(None, "Error"), ('pass', None)]), \
             patch('builtins.print') as mock_print:
            self.assertTrue(self.game.turno_completo())
            mock_print.assert_any_call("Error")

        # Error específico
        with patch('builtins.input', side_effect=['entrada_con_error', 'pass']), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles'), \
             patch.object(self.game, 'quedan_movimientos', side_effect=[True, True, False]), \
             patch.object(self.game, 'procesar_entrada_usuario', side_effect=[(None, "Error específico"), ('pass', None)]), \
             patch('builtins.print') as mock_print:
            self.assertTrue(self.game.turno_completo())
            mock_print.assert_any_call("Error específico")

    def test_turno_completo_mostrar_dados_tras_movimiento(self):
        """Test de turno_completo que muestra dados después de movimiento exitoso."""
        with patch('builtins.input', side_effect=['1,2,1', 'pass']), \
             patch.object(self.game, 'tirar_dados'), \
             patch.object(self.game, 'mostrar_dados_disponibles', return_value="Dados disponibles"), \
             patch.object(self.game, 'quedan_movimientos', side_effect=[True, True, False]), \
             patch.object(self.game, 'procesar_entrada_usuario', side_effect=[((0, 1, 1), None), ('pass', None)]), \
             patch.object(self.game, 'ejecutar_movimiento_completo', return_value=(True, "Movimiento exitoso")), \
             patch.object(self.game, 'verificar_fin_juego_completo', return_value=False), \
             patch('builtins.print') as mock_print:
            self.assertTrue(self.game.turno_completo())
            calls = [call.args[0] for call in mock_print.call_args_list]
            self.assertIn("Dados disponibles", calls)

    def test_obtener_entrada_usuario_simple(self):
        """Test de obtener_entrada_usuario."""
        with patch('builtins.input', return_value='entrada_libre'), \
             patch.object(self.game, 'obtener_opciones_movimiento', return_value=['opcion1', 'opcion2']), \
             patch('builtins.print') as mock_print:
            resultado = self.game.obtener_entrada_usuario()
            self.assertEqual(resultado, 'entrada_libre')
            mock_print.assert_any_call("\nOpciones:")

    def test_mostrar_ayuda_movimientos_contenido(self):
        """Test de contenido de mostrar_ayuda_movimientos."""
        with patch('builtins.print') as mock_print:
            self.game.mostrar_ayuda_movimientos()
            calls = [call.args[0] for call in mock_print.call_args_list]
            self.assertIn("\n=== AYUDA DE MOVIMIENTOS ===", calls)
            self.assertIn("Formato: origen-destino", calls)

    def test_procesar_entrada_usuario_valor_error(self):
        """Test de procesar_entrada_usuario con ValueError."""
        resultado = self.game.procesar_entrada_usuario("abc,def,ghi")
        self.assertEqual(resultado, (None, "Error: Ingrese números válidos"))

    def test_validar_movimiento_legal_excepcion(self):
        """Test de validar_movimiento_legal que maneja excepciones."""
        with patch.object(self.game, 'get_turno', side_effect=AttributeError("Test error")):
            resultado = self.game.validar_movimiento_legal(5, 10, [5])
            self.assertFalse(resultado[0])
            self.assertIn("Error al validar movimiento", resultado[1])

    def test_procesar_entrada_usuario_valor_error(self):
        """Test de procesar_entrada_usuario con ValueError en conversión."""
        resultado = self.game.procesar_entrada_usuario("abc,def,ghi")
        self.assertEqual(resultado, (None, "Error: Ingrese números válidos"))

    def test_validar_movimiento_legal_con_excepciones(self):
        """Test de validar_movimiento_legal que maneja excepciones."""
        # Simular una excepción en el método
        with patch.object(self.game, 'get_turno', side_effect=AttributeError("Test error")):
            resultado = self.game.validar_movimiento_legal(5, 10, [5])
            self.assertFalse(resultado[0])
            self.assertIn("Error al validar movimiento", resultado[1])
    
    def test_configurar_tablero_inicial_completo(self):
        """Test configuración inicial completa del tablero."""
        game = Game(Player("blanca"), Player("negra"))
        
        # Verificar configuración inicial específica
        tablero = game.get_tablero()
        
        # Posiciones iniciales según reglas Backgammon
        self.assertEqual(len(tablero[0]), 2)  # 2 fichas blancas en pos 1
        self.assertEqual(len(tablero[23]), 2)  # 2 fichas negras en pos 24
        self.assertEqual(len(tablero[5]), 5)   # 5 fichas negras en pos 6
        self.assertEqual(len(tablero[18]), 5)  # 5 fichas blancas en pos 19
        
        # Verificar colores
        self.assertEqual(tablero[0][0].obtener_color(), "blanca")
        self.assertEqual(tablero[23][0].obtener_color(), "negra")

    def test_cambio_turno_estados(self):
        """Test cambio de turno y estados internos."""
        game = Game(Player("blanca"), Player("negra"))
        
        turno_inicial = game.get_turno()
        game.cambiar_turno()
        turno_despues = game.get_turno()
        
        self.assertNotEqual(turno_inicial, turno_despues)
        
        # Cambiar de nuevo para volver al inicial
        game.cambiar_turno()
        turno_final = game.get_turno()
        self.assertEqual(turno_inicial, turno_final)

    def test_constructor_con_jugadores_none(self):
        """Test constructor con jugadores None."""
        game = Game(None, None)
        
        # Debe crear jugadores por defecto
        self.assertEqual(game.get_turno().get_color(), "blanca")
        self.assertEqual(game.__state__, "initialized")
        
        # El segundo jugador debe ser negro
        game.cambiar_turno()
        self.assertEqual(game.get_turno().get_color(), "negra")

    def test_movimiento_valido_casos_basicos(self):
        """Test casos básicos de movimientos válidos."""
        game = Game(Player("blanca"), Player("negra"))
        
        # Testear que el método existe y retorna un booleano
        resultado = game.movimiento_valido(0, 5)  # Pos 1 a 6
        self.assertIsInstance(resultado, bool)
        
        # Movimiento desde posición vacía debería ser False
        resultado = game.movimiento_valido(2, 7)  # Pos vacía
        self.assertIsInstance(resultado, bool)

    def test_quedan_movimientos_inicial(self):
        """Test que al inicio no quedan movimientos (dados no tirados)."""
        game = Game(Player("blanca"), Player("negra"))
        
        # Al inicio los dados no han sido tirados
        resultado = game.quedan_movimientos()
        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()
# EOF
