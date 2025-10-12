"""Tests para la clase Board."""
# pylint: disable=missing-function-docstring

import unittest
from unittest.mock import patch
from core.board import Board
from core.checker import Ficha

class TestBoard(unittest.TestCase):
    """Conjunto de pruebas para verificar comportamiento del tablero."""

    def test_estado_inicial(self):
        b = Board()
        self.assertEqual(len(b.get_contenedor()), 24)
        self.assertEqual(b.contar_fichas(0), 2)
        self.assertEqual(b.contar_fichas(23), 2)

    def test_get_fichas_devuelve_copia(self):
        b = Board()
        fichas = b.get_fichas(0)
        self.assertIsInstance(fichas, list)
        self.assertIsNot(fichas, b.get_contenedor()[0])

    def test_guardar_y_quitar_ficha(self):
        b = Board()
        f = Ficha("blanca")
        b.guardar_ficha(5, f)
        self.assertEqual(b.contar_fichas(5), 6)
        ficha = b.quitar_ficha(5)
        self.assertIsInstance(ficha, Ficha)
        self.assertIsNone(b.quitar_ficha(20))  # posición vacía

    def test_color_en_posicion_vacia(self):
        b = Board()
        b.get_contenedor()[3] = []
        self.assertIsNone(b.color_en_posicion(3))

    def test_color_en_posicion_con_fichas(self):
        b = Board()
        b.get_contenedor()[5] = [Ficha("blanca", 5), Ficha("blanca", 5)]
        self.assertEqual(b.color_en_posicion(5), "blanca")

    def test_mover_ficha(self):
        b = Board()
        origen, destino = 0, 1
        ficha = b.get_fichas(origen)[-1]
        b.mover_ficha(origen, destino)
        self.assertEqual(b.contar_fichas(origen), 1)
        self.assertEqual(b.contar_fichas(destino), 1)
        self.assertEqual(ficha.obtener_posicion(), destino)

    def test_enviar_a_barra_y_fichas_en_barra(self):
        b = Board()
        f1 = Ficha("blanca", 4)
        f2 = Ficha("negra", 5)
        b.enviar_a_barra(f1)
        b.enviar_a_barra(f2)
        self.assertEqual(b.fichas_en_barra("blanca"), 1)
        self.assertEqual(b.fichas_en_barra("negra"), 1)
        self.assertTrue(f1.esta_en_barra())
        self.assertTrue(f2.esta_en_barra())

    def test_reingresar_desde_barra(self):
        b = Board()
        f = Ficha("blanca", 4)
        b.enviar_a_barra(f)
        b.reingresar_desde_barra("blanca", 2)
        self.assertEqual(b.contar_fichas(2), 1)
        self.assertEqual(b.fichas_en_barra("blanca"), 0)
        # Caso sin fichas en barra
        b.reingresar_desde_barra("blanca", 10)
        self.assertEqual(b.contar_fichas(10), 0)

    def test_reingresar_desde_barra_negra(self):
        b = Board()
        f = Ficha("negra", 5)
        b.enviar_a_barra(f)
        b.reingresar_desde_barra("negra", 3)
        self.assertEqual(b.contar_fichas(3), 1)
        self.assertEqual(b.fichas_en_barra("negra"), 0)

    def test_sacar_ficha(self):
        b = Board()
        f = Ficha("blanca", 6)
        b.guardar_ficha(6, f)
        ficha = b.sacar_ficha(6)
        self.assertIsNotNone(ficha)
        self.assertTrue(ficha.esta_afuera())
        # Caso posición vacía
        self.assertIsNone(b.sacar_ficha(15))

    def test_reset_sets_initial_positions(self):
        """Verifica que reset deja las posiciones iniciales correctamente."""
        b = Board()
        b.guardar_ficha(5, Ficha("blanca"))
        b.guardar_ficha(10, Ficha("negra"))
        b.reset()
        self.assertEqual(b.contar_fichas(5), 0)
        self.assertEqual(b.contar_fichas(10), 0)
        self.assertEqual(b.contar_fichas(0), 2)
        self.assertEqual(b.contar_fichas(23), 2)

    def test_metodo_mover(self):
        """Prueba el método mover del board."""
        b = Board()
        # Asegurar que hay fichas en posición 0
        if b.contar_fichas(0) > 0:
            b.mover(0, 1)
            self.assertEqual(b.contar_fichas(1), 1)

    def test_metodo_contar_punto(self):
        """Prueba el método contar_punto del board."""
        b = Board()
        count = b.contar_punto(0)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_mover_con_posicion_vacia(self):
        """Prueba el método mover cuando la posición origen está vacía."""
        b = Board()
        # Vaciar una posición y probar mover
        b.get_contenedor()[15] = []
        # Esto debería causar un error o comportamiento específico
        try:
            b.mover(15, 16)
        except IndexError:
            pass  # Esperado si no hay fichas

    def test_contar_punto_todas_posiciones(self):
        """Prueba contar_punto en diferentes posiciones."""
        b = Board()
        for i in range(24):
            count = b.contar_punto(i)
            self.assertGreaterEqual(count, 0)

    def test_mostrar_tablero_completo(self):
        """Test completo de mostrar_tablero con diferentes configuraciones."""
        board = Board()

        # Usar mock para capturar las llamadas a print
        with patch('builtins.print') as mock_print:
            board.mostrar_tablero()
            # Verificar que se llamó a print
            mock_print.assert_called()
            # Verificar que se imprimió información del tablero
            llamadas = [str(call) for call in mock_print.call_args_list]
            output = '\n'.join(llamadas)
            self.assertIn("TABLERO", output.upper())

    def test_aliases_en_ingles(self):
        """Test de los métodos alias en inglés."""
        board = Board()

        # Test move alias
        board.move(0, 1)
        self.assertEqual(board.contar_fichas(0), 1)
        self.assertEqual(board.contar_fichas(1), 1)

        # Test point_count alias
        count = board.point_count(11)
        self.assertEqual(count, 5)

    def test_mostrar_tablero_estados_diferentes(self):
        """Test de mostrar_tablero con diferentes estados del board."""
        board = Board()

        # Agregar fichas en barra para test
        ficha = Ficha("blanca", "barra")
        board.enviar_a_barra(ficha)

        # Usar mock para capturar las llamadas a print
        with patch('builtins.print') as mock_print:
            board.mostrar_tablero()
            # Verificar que se llamó a print
            mock_print.assert_called()
            # Verificar que se imprimió información de la barra
            llamadas = [str(call) for call in mock_print.call_args_list]
            output = '\n'.join(llamadas)
            self.assertIn("BARRA", output.upper())

    def test_metodos_adicionales_board(self):
        """Test de métodos adicionales del board."""
        board = Board()

        # Test color_en_posicion
        color = board.color_en_posicion(0)
        self.assertEqual(color, "blanca")

        # Test posición vacía
        board.get_contenedor()[15] = []
        color_vacio = board.color_en_posicion(15)
        self.assertIsNone(color_vacio)

    def test_validaciones_board_nuevas(self):
        """Test de métodos de validación del board."""
        board = Board()

        # Test validar_posicion
        valido, _ = board.validar_posicion(5)
        self.assertTrue(valido)

        valido, _ = board.validar_posicion(25)
        self.assertFalse(valido)

        valido, _ = board.validar_posicion("barra")
        self.assertTrue(valido)

        valido, _ = board.validar_posicion("invalid")
        self.assertFalse(valido)

        # Test validar_movimiento_posiciones
        valido, _ = board.validar_movimiento_posiciones(5, 11)
        self.assertTrue(valido)

        valido, _ = board.validar_movimiento_posiciones(5, 5)
        self.assertFalse(valido)

        valido, _ = board.validar_movimiento_posiciones("barra", "afuera")
        self.assertTrue(valido)

    def test_verificaciones_posicion_nuevas(self):
        """Test de métodos de verificación de posición."""
        board = Board()

        # Test hay_fichas_en_posicion (posición con fichas)
        self.assertTrue(board.hay_fichas_en_posicion(1))  # posición inicial con fichas

        # Test posicion_bloqueada (posición con fichas propias no está bloqueada)
        self.assertFalse(board.posicion_bloqueada(1, "blanca"))  # fichas propias

        # Test con alias en inglés
        valido, _ = board.validate_position(10)
        self.assertTrue(valido)

    def test_casos_especiales_validacion_nuevas(self):
        """Test de casos especiales en validación."""
        board = Board()

        # Test posición None
        valido, _ = board.validar_posicion(None)
        self.assertFalse(valido)

        # Test posición con tipo incorrecto
        valido, _ = board.validar_posicion(3.5)
        self.assertFalse(valido)

        # Test verificación en barra y afuera
        self.assertFalse(board.hay_fichas_en_posicion("barra"))
        self.assertFalse(board.hay_fichas_en_posicion("afuera"))

        # Test bloqueo hacia afuera (siempre falso)
        self.assertFalse(board.posicion_bloqueada("afuera", "blanca"))


if __name__ == '__main__':
    unittest.main()
# EOF

if __name__ == '__main__':
    unittest.main()
# EOF
