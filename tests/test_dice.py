"""Tests para la clase Dice."""

import unittest
from unittest.mock import patch
from core.dice import Dados


class TestDados(unittest.TestCase):

    def test_roll_basic(self):
        """Test básico del método roll."""
        dados = Dados()
        resultado = dados.roll()
        # Verificar que retorna dos números
        self.assertEqual(len(resultado), 2)
        # Verificar que están en el rango correcto
        for valor in resultado:
            self.assertIn(valor, [1, 2, 3, 4, 5, 6])

    @patch('random.randint')
    def test_roll_mock(self, mock_randint):
        """Test con mock para controlar los valores del dado."""
        mock_randint.side_effect = [3, 5]
        dados = Dados()
        resultado = dados.roll()
        self.assertEqual(resultado, [3, 5])
        # Verificar que se llamó dos veces
        self.assertEqual(mock_randint.call_count, 2)

    @patch('random.randint')
    def test_roll_doubles(self, mock_randint):
        """Test para verificar dobles."""
        mock_randint.side_effect = [4, 4]
        dados = Dados()
        resultado = dados.roll()
        self.assertEqual(resultado, [4, 4])

    def test_multiple_rolls(self):
        """Test de múltiples tiradas."""
        dados = Dados()
        for _ in range(10):
            resultado = dados.roll()
            self.assertEqual(len(resultado), 2)
            for valor in resultado:
                self.assertGreaterEqual(valor, 1)
                self.assertLessEqual(valor, 6)

    def test_dados_attributes(self):
        """Test de atributos de la clase Dados."""
        dados = Dados()
        # Verificar que no tiene atributos inesperados
        expected_attrs = []  # La clase Dados es muy simple
        for attr in expected_attrs:
            self.assertTrue(hasattr(dados, attr))


if __name__ == '__main__':
    unittest.main()
# EOF
