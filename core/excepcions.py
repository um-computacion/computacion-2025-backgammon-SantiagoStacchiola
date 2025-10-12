"""Módulo que define todas las excepciones específicas para el juego Backgammon."""

class BackgammonError(Exception):
    """Excepción base para errores específicos del Backgammon."""
    pass

class EntradaInvalidaError(BackgammonError):
    """Error cuando el input del usuario no es válido."""
    pass

class MovimientoInvalidoError(BackgammonError):
    """Excepción lanzada cuando se intenta realizar un movimiento inválido."""
    pass

class DadoNoDisponibleError(BackgammonError):
    """Excepción lanzada cuando se intenta usar un valor de dado no disponible."""
    pass

class JugadorInvalidoError(BackgammonError):
    """Error relacionado con problemas de jugador (color inválido, etc)."""
    pass

class PosicionVaciaError(BackgammonError):
    """Excepción lanzada cuando se intenta mover desde una posición vacía."""
    pass

class PosicionBloqueadaError(BackgammonError):
    """Error cuando el destino está bloqueado por fichas enemigas (2 o más)."""
    pass

class MovimientoColorError(BackgammonError):
    """Excepción lanzada cuando se intenta mover una ficha del color incorrecto."""
    pass

class JuegoTerminadoError(BackgammonError):
    """Excepción lanzada cuando se intenta hacer una acción en un juego terminado."""
    pass

class ColorInvalidoError(BackgammonError):
    """Excepción lanzada cuando se especifica un color inválido."""
    pass

class FichaInvalidaError(BackgammonError):
    """Excepción lanzada cuando se crea una ficha con parámetros inválidos."""
    pass

class BearingOffInvalidoError(BackgammonError):
    """Error específico para movimientos de bearing off inválidos."""
    pass

class MovimientoBarraError(BackgammonError):
    """Error específico para movimientos desde la barra."""
    pass

class TurnoInvalidoError(BackgammonError):
    """Error cuando se intenta realizar una acción fuera de turno."""
    pass

class ConfiguracionJuegoError(BackgammonError):
    """Error en la configuración inicial del juego."""
    pass

class EstadoJuegoInconsistenteError(BackgammonError):
    """Error cuando el estado del juego se vuelve inconsistente."""
    pass
