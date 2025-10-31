"""Tests para las excepciones del juego de Backgammon."""
import unittest
from core.excepcions import (
    BackgammonError, EntradaInvalidaError, MovimientoInvalidoError,
    DadoNoDisponibleError, JugadorInvalidoError, PosicionVaciaError,
    PosicionBloqueadaError, MovimientoColorError, JuegoTerminadoError,
    ColorInvalidoError, FichaInvalidaError, BearingOffInvalidoError,
    MovimientoBarraError, TurnoInvalidoError, ConfiguracionJuegoError,
    EstadoJuegoInconsistenteError
)


class TestExcepciones(unittest.TestCase):
    """Suite de tests para verificar el comportamiento de todas las excepciones."""

    def test_backgammon_error_base(self):
        """Test de la excepción base BackgammonError."""
        error = BackgammonError("Error general")
        self.assertIsInstance(error, Exception)
        self.assertEqual(str(error), "Error general")

    def test_entrada_invalida_error(self):
        """Test de EntradaInvalidaError."""
        error = EntradaInvalidaError("mensaje de prueba")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "mensaje de prueba")

    def test_movimiento_invalido_error(self):
        """Test de MovimientoInvalidoError."""
        error = MovimientoInvalidoError("mensaje de prueba")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "mensaje de prueba")

    def test_jugador_invalido_error(self):
        """Test de JugadorInvalidoError."""
        error = JugadorInvalidoError("mensaje de prueba")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "mensaje de prueba")

    def test_ficha_invalida_error(self):
        """Test de FichaInvalidaError."""
        error = FichaInvalidaError("mensaje de prueba")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "mensaje de prueba")

    def test_dado_no_disponible_error(self):
        """Test de DadoNoDisponibleError."""
        error = DadoNoDisponibleError("Dado no disponible")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Dado no disponible")

    def test_posicion_vacia_error(self):
        """Test de PosicionVaciaError."""
        error = PosicionVaciaError("Posición vacía")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Posición vacía")

    def test_posicion_bloqueada_error(self):
        """Test de PosicionBloqueadaError."""
        error = PosicionBloqueadaError("Posición bloqueada")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Posición bloqueada")

    def test_movimiento_color_error(self):
        """Test de MovimientoColorError."""
        error = MovimientoColorError("Movimiento de color incorrecto")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Movimiento de color incorrecto")

    def test_juego_terminado_error(self):
        """Test de JuegoTerminadoError."""
        error = JuegoTerminadoError("Juego terminado")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Juego terminado")

    def test_color_invalido_error(self):
        """Test de ColorInvalidoError."""
        error = ColorInvalidoError("Color inválido")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Color inválido")

    def test_bearing_off_invalido_error(self):
        """Test de BearingOffInvalidoError."""
        error = BearingOffInvalidoError("Bearing off inválido")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Bearing off inválido")

    def test_movimiento_barra_error(self):
        """Test de MovimientoBarraError."""
        error = MovimientoBarraError("Movimiento desde barra inválido")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Movimiento desde barra inválido")

    def test_turno_invalido_error(self):
        """Test de TurnoInvalidoError."""
        error = TurnoInvalidoError("Turno inválido")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Turno inválido")

    def test_configuracion_juego_error(self):
        """Test de ConfiguracionJuegoError."""
        error = ConfiguracionJuegoError("Configuración de juego inválida")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Configuración de juego inválida")

    def test_estado_juego_inconsistente_error(self):
        """Test de EstadoJuegoInconsistenteError."""
        error = EstadoJuegoInconsistenteError("Estado de juego inconsistente")
        self.assertIsInstance(error, BackgammonError)
        self.assertEqual(str(error), "Estado de juego inconsistente")

    def test_herencia_excepciones(self):
        """Test de que todas las excepciones heredan de BackgammonError."""
        excepciones_backgammon = [
            EntradaInvalidaError("test"),
            MovimientoInvalidoError("test"),
            DadoNoDisponibleError("test"),
            JugadorInvalidoError("test"),
            PosicionVaciaError("test"),
            MovimientoColorError("test"),
            JuegoTerminadoError("test"),
            ColorInvalidoError("test"),
            FichaInvalidaError("test"),
            BearingOffInvalidoError("test"),
            MovimientoBarraError("test"),
            TurnoInvalidoError("test"),
            ConfiguracionJuegoError("test"),
            EstadoJuegoInconsistenteError("test"),
            PosicionBloqueadaError("test")
        ]

        for excepcion in excepciones_backgammon:
            self.assertIsInstance(excepcion, BackgammonError)
            self.assertIsInstance(excepcion, Exception)


if __name__ == '__main__':
    unittest.main()
