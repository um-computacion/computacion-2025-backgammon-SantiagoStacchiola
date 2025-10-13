"""Tests para el módulo CLI."""

import unittest
from unittest.mock import patch, MagicMock
from cli.cli import BackgammonCLI, main
from core.game import Game
from core.player import Player


class TestBackgammonCLI(unittest.TestCase):
    """Tests para la clase BackgammonCLI."""

    def setUp(self):
        """Configuración inicial para los tests."""
        self.cli = BackgammonCLI()

    def test_init(self):
        """Test inicialización del CLI."""
        self.assertIsInstance(self.cli, BackgammonCLI)
        self.assertIsNone(self.cli.__game__)

    @patch('builtins.print')
    @patch('builtins.input', return_value='')
    def test_mostrar_bienvenida(self, mock_input, mock_print):
        """Test del mensaje de bienvenida."""
        self.cli.mostrar_bienvenida()
        
        # Verificar que se imprimieron los mensajes esperados
        expected_calls = [
            unittest.mock.call("🎲 ¡Bienvenido al Backgammon! 🎲"),
            unittest.mock.call("Jugador 1: fichas BLANCAS"),
            unittest.mock.call("Jugador 2: fichas NEGRAS"),
            unittest.mock.call("\nPresiona Enter para comenzar...")
        ]
        mock_print.assert_has_calls(expected_calls)
        mock_input.assert_called_once()

    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch.object(BackgammonCLI, 'mostrar_bienvenida')
    @patch('builtins.print')
    def test_jugar_quit_inmediato(self, mock_print, mock_bienvenida, mock_game_class, mock_player_class):
        """Test de jugar cuando el usuario hace quit inmediatamente."""
        # Configurar mocks
        mock_game_instance = MagicMock()
        mock_game_instance.turno_completo.return_value = 'quit'
        mock_game_class.return_value = mock_game_instance
        
        mock_player1 = MagicMock()
        mock_player2 = MagicMock()
        mock_player_class.side_effect = [mock_player1, mock_player2]
        
        # Ejecutar
        self.cli.jugar()
        
        # Verificaciones
        mock_bienvenida.assert_called_once()
        mock_player_class.assert_any_call("blanca")
        mock_player_class.assert_any_call("negra")
        mock_game_class.assert_called_once_with(mock_player1, mock_player2)
        mock_game_instance.turno_completo.assert_called_once()
        mock_print.assert_called_with("¡Gracias por jugar!")

    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch.object(BackgammonCLI, 'mostrar_bienvenida')
    @patch('builtins.print')
    def test_jugar_fin_partida(self, mock_print, mock_bienvenida, mock_game_class, mock_player_class):
        """Test de jugar cuando la partida termina normalmente."""
        # Configurar mocks
        mock_game_instance = MagicMock()
        mock_game_instance.turno_completo.return_value = 'fin'
        mock_game_class.return_value = mock_game_instance
        
        mock_player1 = MagicMock()
        mock_player2 = MagicMock()
        mock_player_class.side_effect = [mock_player1, mock_player2]
        
        # Ejecutar
        self.cli.jugar()
        
        # Verificaciones
        mock_bienvenida.assert_called_once()
        mock_game_instance.turno_completo.assert_called_once()
        # No debería llamar a cambiar_turno ni print de gracias cuando es 'fin'

    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch.object(BackgammonCLI, 'mostrar_bienvenida')
    @patch('builtins.print')
    def test_jugar_varios_turnos(self, mock_print, mock_bienvenida, mock_game_class, mock_player_class):
        """Test de jugar con varios turnos antes de terminar."""
        # Configurar mocks
        mock_game_instance = MagicMock()
        mock_game_instance.turno_completo.side_effect = ['continua', 'continua', 'quit']
        mock_game_class.return_value = mock_game_instance
        
        mock_player1 = MagicMock()
        mock_player2 = MagicMock()
        mock_player_class.side_effect = [mock_player1, mock_player2]
        
        # Ejecutar
        self.cli.jugar()
        
        # Verificaciones
        self.assertEqual(mock_game_instance.turno_completo.call_count, 3)
        self.assertEqual(mock_game_instance.cambiar_turno.call_count, 2)
        
        # Verificar mensajes de cambio de turno
        expected_prints = [
            unittest.mock.call("\n" + "~"*60),
            unittest.mock.call("Cambiando turno..."),
            unittest.mock.call("~"*60),
            unittest.mock.call("\n" + "~"*60),
            unittest.mock.call("Cambiando turno..."),
            unittest.mock.call("~"*60),
            unittest.mock.call("¡Gracias por jugar!")
        ]
        mock_print.assert_has_calls(expected_prints)

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_ejecucion_normal(self, mock_print, mock_cli_class):
        """Test de la función main con ejecución normal."""
        mock_cli_instance = MagicMock()
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        mock_cli_class.assert_called_once()
        mock_cli_instance.jugar.assert_called_once()

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_keyboard_interrupt(self, mock_print, mock_cli_class):
        """Test de main cuando se interrumpe con Ctrl+C."""
        mock_cli_instance = MagicMock()
        mock_cli_instance.jugar.side_effect = KeyboardInterrupt()
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        mock_print.assert_called_with("\n\n¡Gracias por jugar!")

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_value_error(self, mock_print, mock_cli_class):
        """Test de main cuando ocurre un ValueError."""
        mock_cli_instance = MagicMock()
        error_msg = "Error de prueba"
        mock_cli_instance.jugar.side_effect = ValueError(error_msg)
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        mock_print.assert_called_with(f"\n¡Ups! Ocurrió un error: {error_msg}")

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_type_error(self, mock_print, mock_cli_class):
        """Test de main cuando ocurre un TypeError."""
        mock_cli_instance = MagicMock()
        error_msg = "Error de tipo"
        mock_cli_instance.jugar.side_effect = TypeError(error_msg)
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        mock_print.assert_called_with(f"\n¡Ups! Ocurrió un error: {error_msg}")

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_attribute_error(self, mock_print, mock_cli_class):
        """Test de main cuando ocurre un AttributeError."""
        mock_cli_instance = MagicMock()
        error_msg = "Error de atributo"
        mock_cli_instance.jugar.side_effect = AttributeError(error_msg)
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        mock_print.assert_called_with(f"\n¡Ups! Ocurrió un error: {error_msg}")


if __name__ == '__main__':
    unittest.main()