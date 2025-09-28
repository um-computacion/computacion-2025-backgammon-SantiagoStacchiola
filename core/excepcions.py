"""Módulo de excepciones personalizadas para el juego de Backgammon."""


class BackgammonError(Exception):
    """Clase base para todas las excepciones del juego de Backgammon."""
    pass


class EntradaInvalidaError(BackgammonError):
    """Error cuando el input del usuario no es válido."""
    pass


class MovimientoInvalidoError(BackgammonError):
    """Error para un movimiento no permitido por las reglas del Backgammon."""
    pass


class DadoNoDisponibleError(BackgammonError):
    """Error cuando se intenta usar un valor de dado que no está disponible."""
    pass


class JugadorInvalidoError(BackgammonError):
    """Error relacionado con problemas de jugador (color inválido, etc)."""
    pass


class PosicionVaciaError(MovimientoInvalidoError):
    """Error cuando se intenta mover desde una posición sin fichas."""
    pass
# EOF