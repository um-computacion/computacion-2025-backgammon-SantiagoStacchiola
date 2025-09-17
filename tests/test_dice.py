import unittest
from core.dice import Dice
from unittest.mock import patch

class TestDice(unittest.TestCase):
    @patch("core.dice.random.randint", side_effect=[2, 5])
    def test_tirar_dados_no_doble(self, mock_randint):
        d = Dice()
        # Forzamos el resultado para evitar aleatoriedad
        resultado = d.tirar()
        self.assertEqual(resultado[0], 2)
        self.assertEqual(resultado[1], 5)

    @patch("core.dice.random.randint", side_effect=[4, 4])
    def test_tirar_dados_doble(self, mock_randint):
        d = Dice()
        resultado = d.tirar()
        self.assertIn(resultado[0], [4, 4, 4, 4])

    def test_quedan_valores_true(self):
        d = Dice()
        d.tirar()
        self.assertTrue(d.quedan_valores())

if __name__ == '__main__':
    unittest.main()
    