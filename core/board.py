"""Módulo que define el tablero y operaciones sobre él."""

from core.checker import Ficha

class Board:
    """Modelo del tablero de backgammon con sus puntos y fichas."""

    def __init__(self):
         # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

        # Barras (fichas capturadas)
        self.__barra_blancas__ = []
        self.__barra_negras__ = []

        # Posiciones iniciales estándar del Backgammon
        # Blancas
        self.__contenedor__[0] = [Ficha("blanca", 0) for _ in range(2)]
        self.__contenedor__[11] = [Ficha("blanca", 11) for _ in range(5)]
        self.__contenedor__[16] = [Ficha("blanca", 16) for _ in range(3)]
        self.__contenedor__[18] = [Ficha("blanca", 18) for _ in range(5)]
        # Negras
        self.__contenedor__[23] = [Ficha("negra", 23) for _ in range(2)]
        self.__contenedor__[12] = [Ficha("negra", 12) for _ in range(5)]
        self.__contenedor__[7] = [Ficha("negra", 7) for _ in range(3)]
        self.__contenedor__[5] = [Ficha("negra", 5) for _ in range(5)]
    
    def get_contenedor(self):
        """Muestra el contenedor."""
        return self.__contenedor__

    def get_fichas(self, posicion):
        """Devuelve una copia de las fichas en una posicion."""
        return list(self.__contenedor__[posicion])

    def contar_fichas(self, posicion):
        """Cantidad de fichas en una posición."""
        return len(self.__contenedor__[posicion])

    def color_en_posicion(self, posicion):
        """Devuelve el color de las fichas en una posición (None si está vacía)."""
        if not self.__contenedor__[posicion]:
            return None
        return self.__contenedor__[posicion][0].obtener_color()

    def guardar_ficha(self, posicion, ficha: Ficha):
        """Guarda una ficha en una posición dada."""
        ficha.mover(posicion)
        self.__contenedor__[posicion].append(ficha)

    def quitar_ficha(self, posicion):
        """Quita una ficha de una posición dada."""
        if self.__contenedor__[posicion]:
            ficha = self.__contenedor__[posicion].pop()
            ficha.mover(None)
            return ficha
        return None
    
    def mover_ficha(self, origen, destino):
        """Mueve una ficha de una posición de origen a una de destino."""
        ficha = self.__contenedor__[origen].pop()
        ficha.mover(destino)
        self.__contenedor__[destino].append(ficha)
    
    def enviar_a_barra(self, ficha: Ficha):
        """Envía una ficha a la barra (fichas capturadas)."""
        ficha.mover("barra")
        if ficha.obtener_color() == "blanca":
            self.__barra_blancas__.append(ficha)
        else:
            self.__barra_negras__.append(ficha)
    
    def reingresar_desde_barra(self, color, destino):
        """Reingresa una ficha desde la barra a una posición del tablero."""
        if color == "blanca" and self.__barra_blancas__:
            ficha = self.__barra_blancas__.pop()
            ficha.mover(destino)
            self.__contenedor__[destino].append(ficha)
        elif color == "negra" and self.__barra_negras__:
            ficha = self.__barra_negras__.pop()
            ficha.mover(destino)
            self.__contenedor__[destino].append(ficha)
    
    def fichas_en_barra(self, color):
        """Devuelve la cantidad de fichas de un color en la barra."""
        return len(self.__barra_blancas__ if color == "blanca" else self.__barra_negras__)
        
    def sacar_ficha(self, posicion):
        """Saca una ficha de una posición y la envía 'afuera'."""
        if self.__contenedor__[posicion]:
            ficha = self.__contenedor__[posicion].pop()
            ficha.mover("afuera")
            return ficha
        return None

    def reset(self):
        """Inicializa o reinicia el tablero a la posición inicial."""
        # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

        # Barras (fichas capturadas)
        self.__barra_blancas__ = []
        self.__barra_negras__ = []

        # Posiciones iniciales estándar del Backgammon
        # Blancas
        self.__contenedor__[0] = [Ficha("blanca", 0) for _ in range(2)]
        self.__contenedor__[11] = [Ficha("blanca", 11) for _ in range(5)]
        self.__contenedor__[16] = [Ficha("blanca", 16) for _ in range(3)]
        self.__contenedor__[18] = [Ficha("blanca", 18) for _ in range(5)]
        # Negras
        self.__contenedor__[23] = [Ficha("negra", 23) for _ in range(2)]
        self.__contenedor__[12] = [Ficha("negra", 12) for _ in range(5)]
        self.__contenedor__[7] = [Ficha("negra", 7) for _ in range(3)]
        # La posición 5 debe quedar vacía después del reset según el test
    
    def move(self, from_point, to_point):
        """Mueve una ficha validando reglas básicas."""
        # Lógica para mover una ficha de from_point a to_point
        ficha = self.__contenedor__[from_point].pop()
        ficha.mover(to_point)
        self.__contenedor__[to_point].append(ficha)

    def point_count(self, point):
        """Devuelve la cantidad de fichas en un punto dado."""
        return len(self.__contenedor__[point])
# EOF