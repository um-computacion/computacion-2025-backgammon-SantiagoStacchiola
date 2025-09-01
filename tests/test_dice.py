import unittest
from core.dice import Dice

class TestDice(unittest.TestCase):
    def test_tirada_normal_o_doble(self):
        d = Dice()
        valores = d.tirar()
        self.assertIn(len(valores), [2, 4])
        for v in valores:
            self.assertTrue(1 <= v <= 6)

    def test_usar_valor(self):
        d = Dice()
        d.set_valores([3, 5]) # simular tirada
        self.assertTrue(d.usar_valor(3))
        self.assertNotIn(3, d.get_valores())
        self.assertFalse(d.usar_valor(6))

    def test_reset(self):
        d = Dice()
        d.get_valores() == [1, 2]
        d.reset()
        self.assertEqual(d.get_valores(), [])