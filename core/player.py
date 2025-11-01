"""Módulo con la clase que representa a un jugador."""

from core.checker import Ficha
from core.excepcions import JugadorInvalidoError


class Player:
    """Representa a un jugador con su nombre, color y fichas."""

    def __init__(self, color: str):
        """Crea un nuevo jugador con color válido."""
        if color not in ["blanca", "negra"]:
            raise JugadorInvalidoError()

        self.__color__ = color
        self.__total_fichas__ = 15
        self.__barra__ = []            # fichas capturadas
        self.__fuera__ = []            # fichas que ya salieron

    def get_color(self):
        """Devuelve el color del jugador."""
        return self.__color__

    def get_total_fichas(self):
        """Devuelve el total de fichas que tiene el jugador."""
        return self.__total_fichas__

    def enviar_a_barra(self, ficha: Ficha):
        """Envía una ficha a la barra del jugador."""
        ficha.mover("barra")
        self.__barra__.append(ficha)

    def sacar_de_barra(self):
        """Saca una ficha de la barra del jugador."""
        if self.__barra__:
            ficha = self.__barra__.pop()
            ficha.mover(None)
            return ficha
        return None

    def fichas_en_barra(self):
        """Devuelve la cantidad de fichas que el jugador tiene en la barra."""
        return len(self.__barra__)

    def sacar_del_tablero(self, ficha: Ficha):
        """Saca una ficha del tablero y la envía a la zona de fuera."""
        ficha.mover("afuera")
        self.__fuera__.append(ficha)

    def fichas_fuera(self):
        """Devuelve la cantidad de fichas que el jugador tiene fuera del tablero."""
        return len(self.__fuera__)

    def fichas_restantes(self):
        """Cantidad de fichas que aún tiene en juego."""
        return self.__total_fichas__ - len(self.__fuera__)

    def has_checker(self, point):
        """Indica si el jugador tiene fichas en el punto indicado."""
        for ficha in self.__fuera__ + self.__barra__:
            if ficha.obtener_posicion() == point:
                return True
        return False

    def _tiene_ficha_en_punto(self, punto):
        """Alias en español para compatibilidad con tests."""
        return self.has_checker(punto)
# EOF
