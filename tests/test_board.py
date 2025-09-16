import unittest
from core.board import Board

class TestBoard(unittest.TestCase):
    def test_estado_inicial_board(self):
        b = Board()
        self.assertEqual(len(b.get_contenedor()), 24)
        self.assertEqual(b.contar_fichas(0), 2)   # blancas
        self.assertEqual(b.contar_fichas(23), 2)  # negras

    def test_guardar_y_quitar_ficha(self):
        b = Board()
        b.guardar_ficha(5, "blanca")
        self.assertEqual(b.contar_fichas(5), 6)
        ficha = b.quitar_ficha(5)
        self.assertEqual(ficha, "blanca")
        self.assertEqual(b.contar_fichas(5), 5)

    def test_color_en_posicion_vacia(self):
        b = Board()
        # Vacía la posición 3
        b.get_contenedor()[3] = []
        self.assertIsNone(b.color_en_posicion(3))

    def test_color_en_posicion_con_fichas(self):
        b = Board()
        b.get_contenedor()[5] = ["blanca", "blanca"]
        self.assertEqual(b.color_en_posicion(5), "blanca")

    def test_quitar_ficha_vacia(self):
        b = Board()
        # Vacía la posición 4
        b.get_contenedor()[4] = []
        self.assertIsNone(b.quitar_ficha(4))

    def test_reingresar_desde_barra_sin_fichas(self):
        b = Board()
        # No hay fichas en la barra
        b.reingresar_desde_barra("blanca", 10)
        self.assertEqual(b.contar_fichas(10), 0)
        b.reingresar_desde_barra("negra", 15)
        self.assertEqual(b.contar_fichas(15), 0)

    def test_sacar_ficha_vacia(self):
        b = Board()
        # Vacía la posición 8
        b.get_contenedor()[8] = []
        self.assertIsNone(b.sacar_ficha(8))

    def test_mover_ficha(self):
        b = Board()
        origen, destino = 0, 1
        b.mover_ficha(origen, destino)
        self.assertEqual(b.contar_fichas(origen), 1)
        self.assertEqual(b.contar_fichas(destino), 1)

    def test_barra_y_reingreso(self):
        b = Board()
        b.enviar_a_barra("blanca")
        self.assertEqual(b.fichas_en_barra("blanca"), 1)
        b.reingresar_desde_barra("blanca", 2)
        self.assertEqual(b.contar_fichas(2), 1)
        self.assertEqual(b.fichas_en_barra("blanca"), 0)