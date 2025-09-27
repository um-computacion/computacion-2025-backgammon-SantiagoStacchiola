"""Tests para la clase Board."""
# pylint: disable=missing-function-docstring

import unittest
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

    def test_move_method(self):
        """Prueba el método move del board."""
        b = Board()
        # Asegurar que hay fichas en posición 0
        if b.contar_fichas(0) > 0:
            b.move(0, 1)
            self.assertEqual(b.contar_fichas(1), 1)

    def test_point_count_method(self):
        """Prueba el método point_count del board."""
        b = Board()
        count = b.point_count(0)
        self.assertIsInstance(count, int)
        self.assertGreaterEqual(count, 0)

    def test_reingresar_desde_barra_sin_fichas(self):
        """Prueba reingresar cuando no hay fichas en la barra."""
        b = Board()
        # Asegurar que no hay fichas en barra
        self.assertEqual(b.fichas_en_barra("blanca"), 0)
        # Intentar reingresar sin fichas en barra
        b.reingresar_desde_barra("blanca", 10)
        self.assertEqual(b.contar_fichas(10), 0)

    def test_reingresar_desde_barra_color_invalido(self):
        """Prueba reingresar con color que no tiene fichas en barra."""
        b = Board()
        f = Ficha("blanca", 5)
        b.enviar_a_barra(f)
        # Intentar reingresar con color diferente
        b.reingresar_desde_barra("negra", 10)
        self.assertEqual(b.contar_fichas(10), 0)

    def test_move_con_posicion_vacia(self):
        """Prueba el método move cuando la posición origen está vacía."""
        b = Board()
        # Vaciar una posición y probar move
        b.get_contenedor()[15] = []
        # Esto debería causar un error o comportamiento específico
        try:
            b.move(15, 16)
        except IndexError:
            pass  # Esperado si no hay fichas

    def test_point_count_todas_posiciones(self):
        """Prueba point_count en diferentes posiciones."""
        b = Board()
        for i in range(24):
            count = b.point_count(i)
            self.assertGreaterEqual(count, 0)

if __name__ == '__main__':
    unittest.main()

# EOF