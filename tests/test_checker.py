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