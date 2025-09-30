"""CLI simple para el juego de Backgammon."""

from core.game import Game
from core.player import Player
from core.excepcions import (MovimientoInvalidoError, DadoNoDisponibleError,
                           PosicionVaciaError, PosicionBloqueadaError,
                           MovimientoColorError)


class BackgammonCLI:
    """CLI simple para jugar Backgammon."""
    
    def __init__(self):
        self.game = None