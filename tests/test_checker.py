import unittest
from core.checker import Ficha

class TestFicha(unittest.TestCase):
    def test_creacion_ficha_valida(self):
        f = Ficha("blanca", 0)
        self.assertEqual(f.obtener_color(), "blanca")
        self.assertEqual(f.obtener_posicion(), 0)
    
    def test_creacion_ficha_invalida(self):
        with self.assertRaises(ValueError):
            Ficha("roja", 5)  # color inválido

    def test_mover_ficha(self):
        f = Ficha("negra", 10)
        f.mover(15)
        self.assertEqual(f.obtener_posicion(), 15)

    def test_ficha_en_barra(self):
        f = Ficha("blanca", "barra")
        self.assertTrue(f.esta_en_barra())
        self.assertFalse(f.esta_afuera())

    