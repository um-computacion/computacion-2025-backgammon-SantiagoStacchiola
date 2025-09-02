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