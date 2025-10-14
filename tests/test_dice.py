"""Tests para la clase Dice."""

import unittest
from unittest.mock import patch
from core.dice import Dice


class TestDados(unittest.TestCase):
    """Tests para la funcionalidad de dados en Backgammon."""

    def test_roll_basic(self):
        """Test básico del método roll."""
        dados = Dice()
        resultado = dados.roll()
        # Verificar que retorna al menos dos números o cuatro en caso de dobles
        self.assertGreaterEqual(len(resultado), 2)
        # Verificar que están en el rango correcto
        for valor in resultado:
            self.assertIn(valor, [1, 2, 3, 4, 5, 6])

    @patch('random.randint')
    def test_roll_mock(self, mock_randint):
        """Test con mock para controlar los valores del dado."""
        mock_randint.side_effect = [3, 5]
        dados = Dice()
        resultado = dados.roll()
        self.assertEqual(resultado, [3, 5])
        # Verificar que se llamó dos veces
        self.assertEqual(mock_randint.call_count, 2)

    @patch('random.randint')
    def test_roll_doubles(self, mock_randint):
        """Test para verificar dobles."""
        mock_randint.side_effect = [4, 4]
        dados = Dice()
        resultado = dados.roll()
        self.assertEqual(resultado, [4, 4, 4, 4])

    def test_multiple_rolls(self):
        """Test de múltiples tiradas."""
        dados = Dice()
        for _ in range(10):
            resultado = dados.roll()
            self.assertGreaterEqual(len(resultado), 2)
            for valor in resultado:
                self.assertGreaterEqual(valor, 1)
                self.assertLessEqual(valor, 6)

    def test_dados_attributes(self):
        """Test de atributos de la clase Dados."""
        dados = Dice()
        # Verificar que tiene el método quedan_valores
        self.assertTrue(hasattr(dados, 'quedan_valores'))
        self.assertTrue(hasattr(dados, 'values'))
        self.assertTrue(hasattr(dados, 'tirar'))

    def test_values_method_linea24(self):
        """Test método values() - línea 24."""
        dados = Dice()
        dados.__valores__ = [3, 5]  # Configurar valores específicos
        resultado = dados.values()  # Ejecutar línea 24
        self.assertEqual(resultado, (3, 5))
        self.assertIsInstance(resultado, tuple)


if __name__ == '__main__':
    unittest.main()
# EOF
