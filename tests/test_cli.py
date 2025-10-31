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
        self.cli.set_test_mode(True)  # Activar modo test para evitar inputs reales

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
            unittest.mock.call("¡Bienvenido al Backgammon!"),
            unittest.mock.call("Presiona Enter para comenzar...")
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
        mock_print.assert_called_with("\n¡Gracias por jugar Backgammon!")

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
        
        # Verificar mensajes de cambio de turno (solo buscar las partes importantes)
        mock_print.assert_any_call("Cambiando turno...")
        mock_print.assert_any_call("\n¡Gracias por jugar Backgammon!")

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
        
        # Verificar que se imprimieron los mensajes de error esperados
        mock_print.assert_any_call(f"\nERROR: {error_msg}")
        mock_print.assert_any_call("El juego terminó inesperadamente.")

    @patch.object(BackgammonCLI, 'mostrar_bienvenida', return_value=False)
    @patch('builtins.print')
    def test_jugar_bienvenida_false(self, mock_print, mock_bienvenida):
        """Cubre la salida temprana de jugar cuando la bienvenida devuelve False."""
        cli = BackgammonCLI()
        cli.jugar()
        # No debería intentar crear Game ni avanzar turnos; solo retorna
        mock_bienvenida.assert_called_once()

    @patch.object(BackgammonCLI, 'mostrar_bienvenida', return_value=True)
    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch('builtins.print')
    def test_jugar_error_inesperado_continua(self, mock_print, mock_game_class, mock_player_class, mock_bienvenida):
        """Cubre el bloque except Exception en jugar y que continúa luego."""
        mock_game_instance = unittest.mock.MagicMock()
        # Primera llamada lanza ValueError, segunda devuelve 'quit'
        mock_game_instance.turno_completo.side_effect = [ValueError("boom"), 'quit']
        mock_game_class.return_value = mock_game_instance
        mock_player_class.side_effect = [unittest.mock.MagicMock(), unittest.mock.MagicMock()]

        cli = BackgammonCLI()
        cli.set_test_mode(True)  # Evitar pausa entre turnos
        cli.jugar()

        # Debe haber impreso el error inesperado y luego el mensaje de salida
        calls = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("ERROR inesperado" in s for s in calls))
        self.assertTrue(any("Gracias por jugar Backgammon" in s for s in calls))

    @patch.object(BackgammonCLI, 'mostrar_bienvenida', return_value=True)
    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch('builtins.input', side_effect=StopIteration())
    @patch('builtins.print')
    def test_jugar_stopiteration_en_pausa(self, mock_print, mock_input, mock_game_class, mock_player_class, mock_bienvenida):
        """Cubre el except StopIteration durante la pausa entre turnos."""
        mock_game_instance = unittest.mock.MagicMock()
        mock_game_instance.turno_completo.side_effect = ['continua']
        mock_game_class.return_value = mock_game_instance
        mock_player_class.side_effect = [unittest.mock.MagicMock(), unittest.mock.MagicMock()]

        cli = BackgammonCLI()
        cli.set_test_mode(False)  # Forzar pausa de turno
        cli.jugar()

        calls = [str(c.args[0]) for c in mock_print.call_args_list if c.args]
        self.assertTrue(any("Entrada agotada" in s for s in calls))

    @patch('builtins.input', side_effect=StopIteration())
    @patch('builtins.print')
    def test_mostrar_bienvenida_stopiteration(self, mock_print, mock_input):
        """Cubre la rama StopIteration en mostrar_bienvenida."""
        cli = BackgammonCLI()
        cli.set_test_mode(False)
        ok = cli.mostrar_bienvenida()
        self.assertFalse(ok)
        mock_print.assert_any_call("\n¡Hasta luego!")

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_type_error(self, mock_print, mock_cli_class):
        """Test de main cuando ocurre un TypeError."""
        mock_cli_instance = MagicMock()
        error_msg = "Error de tipo"
        mock_cli_instance.jugar.side_effect = TypeError(error_msg)
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        # Verificar que se imprimieron los mensajes de error esperados
        mock_print.assert_any_call(f"\nERROR: {error_msg}")
        mock_print.assert_any_call("El juego terminó inesperadamente.")

    @patch('cli.cli.BackgammonCLI')
    @patch('builtins.print')
    def test_main_attribute_error(self, mock_print, mock_cli_class):
        """Test de main cuando ocurre un AttributeError."""
        mock_cli_instance = MagicMock()
        error_msg = "Error de atributo"
        mock_cli_instance.jugar.side_effect = AttributeError(error_msg)
        mock_cli_class.return_value = mock_cli_instance
        
        main()
        
        # Verificar que se imprimieron los mensajes de error esperados
        mock_print.assert_any_call(f"\nERROR: {error_msg}")
        mock_print.assert_any_call("El juego terminó inesperadamente.")

    @patch('builtins.input', side_effect=[KeyboardInterrupt()])
    @patch('builtins.print')
    def test_mostrar_bienvenida_interrumpida(self, mock_print, mock_input):
        """Cubre la rama de excepción en mostrar_bienvenida (KeyboardInterrupt)."""
        cli = BackgammonCLI()
        cli.set_test_mode(False)  # Forzar ruta 'normal' pero con input parcheado
        ok = cli.mostrar_bienvenida()
        self.assertFalse(ok)
        mock_print.assert_any_call("\n¡Hasta luego!")

    @patch('cli.cli.Player')
    @patch('cli.cli.Game')
    @patch('builtins.input', side_effect=[''])
    @patch('builtins.print')
    def test_jugar_con_pausa_de_turno(self, mock_print, mock_input, mock_game_class, mock_player_class):
        """Cubre la rama de pausa entre turnos cuando __test_mode__ es False."""
        cli = BackgammonCLI()
        cli.set_test_mode(False)

        # Configurar mocks de Game/Player para evitar lógica real
        mock_game_instance = unittest.mock.MagicMock()
        mock_game_instance.turno_completo.side_effect = ['continua', 'quit']
        mock_game_class.return_value = mock_game_instance

        mock_player1 = unittest.mock.MagicMock()
        mock_player2 = unittest.mock.MagicMock()
        mock_player_class.side_effect = [mock_player1, mock_player2]

        # Evitar llamada a input de bienvenida pero mantener pausa entre turnos
        cli.mostrar_bienvenida = unittest.mock.MagicMock(return_value=True)

        cli.jugar()

        # Debe haberse llamado a cambiar_turno al menos una vez
        self.assertGreaterEqual(mock_game_instance.cambiar_turno.call_count, 1)
        # Debe haberse impreso el mensaje de cambio de turno
        calls = [call.args[0] for call in mock_print.call_args_list if call.args]
        self.assertTrue(any("Cambiando turno" in str(c) for c in calls))


    def test_obtener_entrada_usuario_sin_movimientos(self):
        """Test obtener_entrada_usuario cuando no quedan movimientos."""
        cli = BackgammonCLI()
        cli.set_test_mode(True)
        cli.__game__ = Game(Player("blanca"), Player("negra"))
        
        # Mock para que no queden movimientos
        with patch.object(cli.__game__, 'quedan_movimientos', return_value=False), \
             patch('builtins.print') as mock_print:
            resultado = cli.obtener_entrada_usuario()
            self.assertEqual(resultado, 'pass')
            mock_print.assert_any_call("No quedan movimientos, terminando turno...")

    def test_obtener_entrada_usuario_entrada_vacia(self):
        """Test obtener_entrada_usuario con entrada vacía seguida de entrada válida."""
        cli = BackgammonCLI()
        cli.set_test_mode(True)
        cli.__game__ = Game(Player("blanca"), Player("negra"))
        cli.__game__ = Game(Player("blanca"), Player("negra"))
        
        with patch.object(cli.__game__, 'quedan_movimientos', return_value=True), \
             patch.object(cli.__game__, 'obtener_opciones_movimiento', return_value=['pass']), \
             patch('builtins.input', side_effect=['', 'pass']) as mock_input, \
             patch('builtins.print') as mock_print:
            resultado = cli.obtener_entrada_usuario()
            self.assertEqual(resultado, 'pass')
            # Verificar que se pidió ingresar comando válido
            mock_print.assert_any_call("Por favor ingresa un comando válido.")

    def test_obtener_entrada_usuario_keyboard_interrupt(self):
        """Test obtener_entrada_usuario con KeyboardInterrupt."""
        cli = BackgammonCLI()
        cli.set_test_mode(True)
        cli.__game__ = Game(Player("blanca"), Player("negra"))
        
        with patch.object(cli.__game__, 'quedan_movimientos', return_value=True), \
             patch.object(cli.__game__, 'obtener_opciones_movimiento', return_value=['pass']), \
             patch('builtins.input', side_effect=KeyboardInterrupt()), \
             patch('builtins.print'):
            resultado = cli.obtener_entrada_usuario()
            self.assertEqual(resultado, 'quit')

if __name__ == '__main__':
    unittest.main()
# EOF
