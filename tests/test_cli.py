"""Tests para el CLI de Backgammon - Versión Concisa."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.cli import BackgammonCLI
from core.game import Game
from core.player import Player
from core.checker import Ficha


class TestBackgammonCLI(unittest.TestCase):
    """Tests principales para la clase BackgammonCLI."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.cli = BackgammonCLI()
        self.cli.game = Game(Player("blanca"), Player("negra"))

    def test_init_cli(self):
        """Test de inicialización del CLI."""
        cli = BackgammonCLI()
        self.assertIsNone(cli.game)

    def test_mostrar_tablero(self):
        """Test que verifica la visualización del tablero."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.mostrar_tablero()
            output = fake_output.getvalue()
            
        # Verificar elementos clave del output
        self.assertIn("TABLERO DE BACKGAMMON", output)
        self.assertIn("BARRA", output)
        self.assertIn("1: 2 fichas blanca", output)  # Configuración inicial
        self.assertIn("24: 2 fichas negra", output)

    def test_mostrar_dados(self):
        """Test de mostrar dados con y sin valores."""
        # Con dados
        self.cli.game.tirar_dados()
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.mostrar_dados()
            self.assertIn("Dados disponibles:", fake_output.getvalue())
        
        # Sin dados
        self.cli.game.__dice__.__valores__ = []
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.mostrar_dados()
            self.assertIn("No hay dados disponibles", fake_output.getvalue())

    def test_mostrar_turno(self):
        """Test de mostrar turno para ambos jugadores."""
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.mostrar_turno()
            self.assertIn("BLANCA", fake_output.getvalue())
        
        # Cambiar turno
        self.cli.game.cambiar_turno()
        with patch('sys.stdout', new=StringIO()) as fake_output:
            self.cli.mostrar_turno()
            self.assertIn("NEGRA", fake_output.getvalue())

    @patch('builtins.input')
    def test_pedir_movimiento_formatos(self, mock_input):
        """Test de todos los formatos de entrada válidos."""
        test_cases = [
            ('quit', 'quit'),
            ('pass', 'pass'),
            ('1,7,6', (0, 6, 6)),
            ('barra,3,3', ('barra', 2, 3)),
            ('19,off,3', (18, 'off', 3)),
            ('  1 , 7 , 6  ', (0, 6, 6)),  # Con espacios
            ('QUIT', 'quit'),  # Mayúsculas
        ]
        
        for entrada, esperado in test_cases:
            with self.subTest(entrada=entrada):
                mock_input.return_value = entrada
                with patch('sys.stdout', new=StringIO()):
                    resultado = self.cli.pedir_movimiento()
                self.assertEqual(resultado, esperado)

    @patch('builtins.input')
    def test_pedir_movimiento_errores(self, mock_input):
        """Test de manejo de errores en entrada de usuario."""
        entradas_invalidas = ['1,7', '1,7,6,extra', 'a,b,c', 'barra,off,3']
        
        for entrada in entradas_invalidas:
            with self.subTest(entrada=entrada):
                mock_input.return_value = entrada
                with patch('sys.stdout', new=StringIO()) as fake_output:
                    resultado = self.cli.pedir_movimiento()
                    output = fake_output.getvalue()
                self.assertIsNone(resultado)
                self.assertIn("Error:", output)

    def test_pedir_movimiento_opciones_barra(self):
        """Test que muestra opciones especiales cuando hay fichas en barra."""
        # Enviar ficha a la barra
        jugador = self.cli.game.get_turno()
        ficha = Ficha(jugador.get_color(), 0)
        self.cli.game.__board__.enviar_a_barra(ficha)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            with patch('builtins.input', return_value='quit'):
                self.cli.pedir_movimiento()
            output = fake_output.getvalue()
            
        self.assertIn("Tienes fichas en la barra", output)
        self.assertIn("barra,destino,dado", output)

    def test_ejecutar_movimiento_normal(self):
        """Test de ejecución de movimiento normal."""
        self.cli.game.__dice__.__valores__ = [6]
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            resultado = self.cli.ejecutar_movimiento(0, 6, 6)
            
        self.assertTrue(resultado)
        self.assertIn("exitosamente", fake_output.getvalue())

    def test_ejecutar_movimiento_errores(self):
        """Test de errores en ejecución de movimientos."""
        # Dado no disponible
        self.cli.game.__dice__.__valores__ = [4]
        with patch('sys.stdout', new=StringIO()) as fake_output:
            resultado = self.cli.ejecutar_movimiento(0, 5, 5)
        self.assertFalse(resultado)
        self.assertIn("Error", fake_output.getvalue())

    def test_ejecutar_movimiento_desde_barra(self):
        """Test de ejecución de movimiento desde la barra."""
        # Configurar ficha en barra
        jugador = self.cli.game.get_turno()
        ficha = Ficha(jugador.get_color(), 0)
        self.cli.game.__board__.enviar_a_barra(ficha)
        self.cli.game.__dice__.__valores__ = [3]
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            resultado = self.cli.ejecutar_movimiento('barra', 2, 3)
            
        self.assertTrue(resultado)
        self.assertIn("reingresada", fake_output.getvalue())

    def test_ejecutar_movimiento_barra_errores(self):
        """Test de errores en movimientos desde barra."""
        # Sin fichas en barra
        self.cli.game.__dice__.__valores__ = [3]
        with patch('sys.stdout', new=StringIO()) as fake_output:
            resultado = self.cli.ejecutar_movimiento('barra', 2, 3)
        self.assertFalse(resultado)
        self.assertIn("No tienes fichas en la barra", fake_output.getvalue())

    def test_ejecutar_movimiento_bearing_off(self):
        """Test de bearing off exitoso y con errores."""
        self.cli.game.__dice__.__valores__ = [3]
        
        # Test sin estar en home board
        with patch('sys.stdout', new=StringIO()) as fake_output:
            resultado = self.cli.ejecutar_movimiento(18, 'off', 3)
        self.assertFalse(resultado)
        self.assertIn("home board", fake_output.getvalue())
        
        # Test exitoso (mock)
        with patch.object(self.cli, '_todas_fichas_en_home', return_value=True):
            # Asegurar que hay ficha en la posición
            tablero = self.cli.game.get_tablero()
            if not tablero[18]:
                tablero[18] = [Ficha("blanca", 18)]
            
            with patch('sys.stdout', new=StringIO()) as fake_output:
                resultado = self.cli.ejecutar_movimiento(18, 'off', 3)
            self.assertTrue(resultado)
            self.assertIn("bearing off", fake_output.getvalue())

    def test_todas_fichas_en_home(self):
        """Test de verificación de fichas en home board."""
        player1 = self.cli.game.get_turno()
        
        # Configuración inicial - fichas fuera de home
        self.assertFalse(self.cli._todas_fichas_en_home(player1))
        
        # Configurar todas en home board
        tablero = self.cli.game.get_tablero()
        for i in range(24):
            tablero[i] = []
        tablero[18] = [Ficha("blanca", 18) for _ in range(15)]
        
        self.assertTrue(self.cli._todas_fichas_en_home(player1))
        
        # Con ficha en barra - debe ser False
        ficha = Ficha("blanca", 0)
        self.cli.game.__board__.enviar_a_barra(ficha)
        self.assertFalse(self.cli._todas_fichas_en_home(player1))


class TestCasosEspeciales(unittest.TestCase):
    """Tests para casos especiales y edge cases."""

    def test_cli_sin_juego(self):
        """Test de métodos CLI sin juego inicializado."""
        cli = BackgammonCLI()
        
        with self.assertRaises(AttributeError):
            cli.mostrar_tablero()
        with self.assertRaises(AttributeError):
            cli.mostrar_dados()
        with self.assertRaises(AttributeError):
            cli.mostrar_turno()

    def test_tablero_con_posiciones_vacias(self):
        """Test de tablero con posiciones vacías."""
        cli = BackgammonCLI()
        cli.game = Game(Player("blanca"), Player("negra"))
        
        # Vaciar algunas posiciones
        tablero = cli.game.get_tablero()
        tablero[5] = []
        tablero[7] = []
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            cli.mostrar_tablero()
            output = fake_output.getvalue()
            
        self.assertIn("TABLERO DE BACKGAMMON", output)

    def test_bearing_off_desde_posicion_vacia(self):
        """Test de bearing off desde posición sin fichas."""
        cli = BackgammonCLI()
        cli.game = Game(Player("blanca"), Player("negra"))
        cli.game.__dice__.__valores__ = [3]
        
        # Limpiar posición
        tablero = cli.game.get_tablero()
        tablero[18] = []
        
        with patch.object(cli, '_todas_fichas_en_home', return_value=True):
            with patch('sys.stdout', new=StringIO()) as fake_output:
                resultado = cli.ejecutar_movimiento(18, 'off', 3)
                
        self.assertFalse(resultado)
        self.assertIn("No hay fichas", fake_output.getvalue())


class TestIntegracion(unittest.TestCase):
    """Tests de integración del CLI."""

    def setUp(self):
        """Configuración para tests de integración."""
        self.cli = BackgammonCLI()
        self.cli.game = Game(Player("blanca"), Player("negra"))

    def test_flujo_completo_juego(self):
        """Test de flujo completo: dados, visualización, movimiento."""
        # Tirar dados
        self.cli.game.tirar_dados()
        
        # Verificar visualización
        with patch('sys.stdout', new=StringIO()):
            self.cli.mostrar_tablero()
            self.cli.mostrar_turno()
            self.cli.mostrar_dados()
        
        # Verificar que hay dados disponibles
        self.assertTrue(self.cli.game.quedan_movimientos())
        
        # Ejecutar movimiento si hay dados
        dados_disponibles = self.cli.game.__dice__.__valores__
        if dados_disponibles:
            valor_dado = dados_disponibles[0]
            with patch('sys.stdout', new=StringIO()):
                resultado = self.cli.ejecutar_movimiento(0, valor_dado, valor_dado)
            self.assertTrue(resultado)

    @patch('builtins.input')
    def test_validacion_entrada_completa(self, mock_input):
        """Test completo de validación de entradas."""
        entradas_validas = [
            ('1,7,6', (0, 6, 6)),
            ('barra,3,3', ('barra', 2, 3)),
            ('19,off,3', (18, 'off', 3)),
            ('quit', 'quit'),
            ('pass', 'pass')
        ]
        
        for entrada, esperado in entradas_validas:
            with self.subTest(entrada=entrada):
                mock_input.return_value = entrada
                with patch('sys.stdout', new=StringIO()):
                    resultado = self.cli.pedir_movimiento()
                self.assertEqual(resultado, esperado)


if __name__ == '__main__':
    unittest.main()