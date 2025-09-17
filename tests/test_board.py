import unittest
from core.board import Board
from core.checker import Ficha

class TestBoard(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()