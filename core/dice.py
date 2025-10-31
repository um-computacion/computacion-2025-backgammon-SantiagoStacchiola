"""Módulo de dados usado en el juego de backgammon."""

import random

class Dice:
    """Representa un par de dados y sus tiradas."""

    def __init__(self):
        """Inicializa los dados con valores vacíos."""
        self.__valores__ = []

    def roll(self):
        """Realiza una tirada y actualiza los valores internos."""
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        self.__valores__ = [d1] * 4 if d1 == d2 else [d1, d2]
        return self.__valores__

    def quedan_valores(self):
        """Devuelve True si todavía quedan movimientos posibles."""
        return len(self.__valores__) > 0

    def values(self):
        """Devuelve una tupla con los valores actuales de los dados."""
        return tuple(self.__valores__)

    def tirar(self):
        """Alias en español para roll(), mantiene compatibilidad con tests."""
        return self.roll()
