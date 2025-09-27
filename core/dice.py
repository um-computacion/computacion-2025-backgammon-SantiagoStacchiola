"""Módulo de dados usado en el juego de backgammon."""


import random


class Dice:
    """Representa un par de dados y sus tiradas."""

    def __init__(self):
        # guarda la tirada actual
        self.__valores__ = []

    def roll(self):
        """Realiza una tirada y actualiza los valores internos."""
        # Lanza los dados y guarda el resultado
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)

        if d1 == d2:
            # Doble → cuatro movimientos
            self.__valores__ = [d1] * 4
        else:
            self.__valores__ = [d1, d2]

        return self.__valores__

    def quedan_valores(self):
        """Devuelve True si todavía quedan movimientos posibles"""
        # Devuelve True si todavía quedan movimientos posibles
        return len(self.__valores__) > 0

    def values(self):
        """Devuelve una tupla con los valores actuales de los dados."""
        return tuple(self.__valores__)

    def tirar(self):
        """Alias en español para roll(), mantiene compatibilidad con tests que llaman 'tirar'."""
        return self.roll()
