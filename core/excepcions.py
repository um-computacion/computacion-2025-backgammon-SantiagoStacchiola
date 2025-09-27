"""Módulo de excepciones personalizadas para el juego de Backgammon."""


class BackgammonError(Exception):
    """Clase base para todas las excepciones del juego de Backgammon."""
    pass


class EntradaInvalidaError(BackgammonError):
    """Error cuando el input del usuario no es válido."""
    pass