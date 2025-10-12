"""Tests para la clase Game."""
# pylint: disable=missing-function-docstring,protected-access

import unittest
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
        from core.game import BackgammonGame
        from core.player import Player
        
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
        from core.game import BackgammonGame
        from core.player import Player
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        jugador = game.get_turno()
        
        # Al inicio, no todas las fichas están en home
        self.assertFalse(game.todas_fichas_en_home(jugador))
        
        # Test con jugador None (usa turno actual)
        self.assertFalse(game.todas_fichas_en_home())

    def test_procesar_entrada_usuario_basico(self):
        """Test básico del procesamiento de entrada."""
        from core.game import BackgammonGame
        from core.player import Player
        
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
        from core.game import BackgammonGame
        from core.player import Player
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Sin fichas en barra, debería fallar
        exito, mensaje = game.ejecutar_movimiento_barra(5, 3)
        self.assertFalse(exito)
        self.assertIn("No tienes fichas en la barra", mensaje)

    def test_ejecutar_bearing_off_casos(self):
        """Test de ejecutar_bearing_off con diferentes casos."""
        from core.game import BackgammonGame
        from core.player import Player
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Sin todas las fichas en home, debería fallar
        exito, mensaje = game.ejecutar_bearing_off(20, 3)
        self.assertFalse(exito)
        self.assertIn("Todas las fichas deben estar en el home board", mensaje)

    def test_ejecutar_movimiento_completo_casos(self):
        """Test de ejecutar_movimiento_completo con diferentes casos."""
        from core.game import BackgammonGame
        from core.player import Player
        
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
        from core.game import BackgammonGame
        from core.player import Player
        from io import StringIO
        import sys
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Al inicio, juego no ha terminado
        self.assertFalse(game.verificar_fin_juego_completo())

    def test_obtener_entrada_usuario_con_opciones(self):
        """Test de obtener_entrada_usuario mostrando opciones."""
        from core.game import BackgammonGame
        from core.player import Player
        from io import StringIO
        import sys
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Simular entrada del usuario
        sys.stdin = StringIO("test\n")
        
        # Capturar salida
        captured_output = StringIO()
        sys.stdout = captured_output
        
        entrada = game.obtener_entrada_usuario()
        
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
        
        self.assertEqual(entrada, "test")
        output = captured_output.getvalue()
        self.assertIn("Opciones:", output)

    def test_mostrar_estado_juego_completo(self):
        """Test completo de mostrar_estado_juego."""
        from core.game import BackgammonGame
        from core.player import Player
        from io import StringIO
        import sys
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Capturar la salida
        captured_output = StringIO()
        sys.stdout = captured_output
        game.mostrar_estado_juego()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("TABLERO DE BACKGAMMON", output)
        self.assertIn("Turno del jugador", output)

    def test_procesar_entrada_usuario_completo(self):
        """Test completo del procesamiento de entrada del usuario."""
        from core.game import BackgammonGame
        from core.player import Player
        
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
        """Test de turno_completo con casos especiales."""
        from core.game import BackgammonGame
        from core.player import Player
        from io import StringIO
        import sys
        
        game = BackgammonGame(Player("blanca"), Player("negra"))
        
        # Simular entrada "quit"
        sys.stdin = StringIO("quit\n")
        captured_output = StringIO()
        sys.stdout = captured_output
        
        resultado = game.turno_completo()
        
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
        
        self.assertEqual(resultado, "quit")

if __name__ == "__main__":
    unittest.main()
# EOF


if __name__ == "__main__":
    unittest.main()
# EOF
