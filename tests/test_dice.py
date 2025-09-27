"""Tests para la clase Dice."""

import unittest
from unittest.mock import patch
from core.dice import Dice


class TestDice(unittest.TestCase):
    """Verifica comportamiento de las tiradas de dados."""

    @patch("random.randint", side_effect=[2, 5])
    def test_tirar_dados_no_doble(self, _mock_randint):
        """Comprueba que tirar dados no produce dobles."""
        d = Dice()
        resultado = d.tirar()
        self.assertEqual(resultado[0], 2)
        self.assertEqual(resultado[1], 5)

    @patch("random.randint", side_effect=[4, 4])
    def test_tirar_dados_doble(self, _mock_randint):
        """Comprueba que tirar dados produce dobles."""
        d = Dice()
        resultado = d.tirar()
        self.assertEqual(len(resultado), 4)
        self.assertTrue(all(v == 4 for v in resultado))

    def test_quedan_valores_true(self):
        """Comprueba que quedan valores tras una tirada."""
        d = Dice()
        d.tirar()
        self.assertTrue(d.quedan_valores())

    def test_quedan_valores_false(self):
        """Comprueba que no quedan valores cuando se agotan."""
        d = Dice()
        d.tirar()
        while d.quedan_valores():
            if d.__valores__:
                d.__valores__.pop()
        self.assertFalse(d.quedan_valores())

    @patch("random.randint", side_effect=[1, 2])
    def test_values_no_doble(self, _mock_randint):
        """Prueba el método values con tirada no doble."""
        d = Dice()
        d.tirar()
        valores = d.values()
        self.assertEqual(len(valores), 2)
        self.assertIn(1, valores)
        self.assertIn(2, valores)

    def test_roll_method_direct(self):
        """Prueba directa del método roll."""
        d = Dice()
        resultado = d.roll()
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)
        for valor in resultado:
            self.assertIn(valor, [1, 2, 3, 4, 5, 6])


if __name__ == '__main__':
    unittest.main()

# EOF
