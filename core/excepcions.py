"""Módulo de excepciones personalizadas para el juego de Backgammon."""


class BackgammonError(Exception):
    """Clase base para todas las excepciones del juego de Backgammon."""
    pass

class EntradaInvalidaError(BackgammonError):
    """Error cuando el input del usuario no es válido."""
    pass

class MovimientoInvalidoError(BackgammonError):
    """Excepción lanzada cuando se intenta realizar un movimiento inválido."""
    pass

class DadoNoDisponibleError(Exception):
    """Excepción lanzada cuando se intenta usar un valor de dado no disponible."""
    pass

class JugadorInvalidoError(BackgammonError):
    """Error relacionado con problemas de jugador (color inválido, etc)."""
    pass

class PosicionVaciaError(Exception):
    """Excepción lanzada cuando se intenta mover desde una posición vacía."""
    pass

class PosicionBloqueadaError(MovimientoInvalidoError):
    """Error cuando el destino está bloqueado por fichas enemigas (2 o más)."""
    pass

class MovimientoColorError(Exception):
    """Excepción lanzada cuando se intenta mover una ficha del color incorrecto."""
    pass

class JuegoTerminadoError(Exception):
    """Excepción lanzada cuando se intenta hacer una acción en un juego terminado."""
    pass

class ColorInvalidoError(Exception):
    """Excepción lanzada cuando se especifica un color inválido."""
    pass

class FichaInvalidaError(Exception):
    """Excepción lanzada cuando se crea una ficha con parámetros inválidos."""
    pass