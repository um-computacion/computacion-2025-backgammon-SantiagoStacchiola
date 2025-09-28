"""Tests para la clase Checker."""
# pylint: disable=missing-function-docstring

import unittest
from core.checker import Ficha
from core.excepcions import JugadorInvalidoError


class TestChecker(unittest.TestCase):
    """Pruebas sobre la ficha (checker)."""

    def test_creacion_valida(self):
        """Prueba la creación de una ficha con valores válidos."""
        f = Ficha("blanca", 0)
        self.assertEqual(f.obtener_color(), "blanca")
        self.assertEqual(f.obtener_posicion(), 0)

    def test_creacion_invalida(self):
        """Prueba la creación de una ficha con valores inválidos."""
        with self.assertRaises(JugadorInvalidoError):
            Ficha("roja", 5)  # color inválido

    def test_mover(self):
        """Prueba el movimiento de una ficha."""
        f = Ficha("negra", 10)
        f.mover(15)
        self.assertEqual(f.obtener_posicion(), 15)

    def test_en_barra(self):
        """Prueba la verificación de si una ficha está en la barra."""
        f = Ficha("blanca", "barra")
        self.assertTrue(f.esta_en_barra())
        self.assertFalse(f.esta_afuera())

    def test_afuera(self):
        """Prueba la verificación de si una ficha está afuera."""
        f = Ficha("negra", "afuera")
        self.assertTrue(f.esta_afuera())
        self.assertFalse(f.esta_en_barra())

    def test_repr(self):
        """Prueba la representación en cadena de una ficha."""
        f = Ficha("blanca", 3)
        self.assertIn("blanca", repr(f))
        self.assertIn("3", repr(f))

    def test_puede_mover_basico(self):
        """Comprueba movimientos legales básicos de una ficha."""
        f = Ficha("blanca", 1)
        self.assertTrue(f.puede_mover_a(3))
        self.assertFalse(f.puede_mover_a(5))

    def test_puede_mover_fichas_negras(self):
        """Prueba movimientos de fichas negras."""
        f = Ficha("negra", 10)
        self.assertTrue(f.puede_mover_a(8))  # diferencia 2
        self.assertFalse(f.puede_mover_a(6))  # diferencia 4

    def test_puede_mover_posicion_none(self):
        """Prueba movimiento con posición None."""
        f = Ficha("blanca", None)
        self.assertFalse(f.puede_mover_a(3))

    def test_metodo_puede_mover(self):
        """Prueba el método puede_mover."""
        f = Ficha("blanca", 1)
        result = f.puede_mover(1, 3)
        self.assertTrue(result)

    def test_puede_mover_diferentes_distancias(self):
        """Prueba movimientos con diferentes distancias para fichas blancas."""
        f = Ficha("blanca", 5)
        # Probar todas las distancias válidas excepto 4
        self.assertTrue(f.puede_mover_a(6))   # diferencia 1
        self.assertTrue(f.puede_mover_a(7))   # diferencia 2
        self.assertTrue(f.puede_mover_a(8))   # diferencia 3
        self.assertFalse(f.puede_mover_a(9))  # diferencia 4 (no válida)
        self.assertTrue(f.puede_mover_a(10))  # diferencia 5
        self.assertTrue(f.puede_mover_a(11))  # diferencia 6

    def test_puede_mover_negras_diferentes_distancias(self):
        """Prueba movimientos con diferentes distancias para fichas negras."""
        f = Ficha("negra", 15)
        # Probar todas las distancias válidas excepto 4
        self.assertTrue(f.puede_mover_a(14))  # diferencia 1
        self.assertTrue(f.puede_mover_a(13))  # diferencia 2
        self.assertTrue(f.puede_mover_a(12))  # diferencia 3
        self.assertFalse(f.puede_mover_a(11)) # diferencia 4 (no válida)
        self.assertTrue(f.puede_mover_a(10))  # diferencia 5
        self.assertTrue(f.puede_mover_a(9))   # diferencia 6

    def test_obtener_posicion_method(self):
        """Prueba específica del método obtener_posicion."""
        f = Ficha("blanca", 10)
        pos = f.obtener_posicion()
        self.assertEqual(pos, 10)

    def test_puede_mover_casos_limite(self):
        """Prueba casos límite de puede_mover_a."""
        f = Ficha("blanca", 0)
        # Casos límite
        self.assertTrue(f.puede_mover_a(1))   # diferencia 1
        self.assertTrue(f.puede_mover_a(6))   # diferencia 6
        self.assertFalse(f.puede_mover_a(4))  # diferencia 4 (no válida)

        # Casos para fichas negras
        f_negra = Ficha("negra", 20)
        self.assertTrue(f_negra.puede_mover_a(19))  # diferencia 1
        self.assertTrue(f_negra.puede_mover_a(14))  # diferencia 6
        self.assertFalse(f_negra.puede_mover_a(16)) # diferencia 4 (no válida)


if __name__ == '__main__':
    unittest.main()

# EOF