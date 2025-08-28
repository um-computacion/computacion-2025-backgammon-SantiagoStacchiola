class Tablero:
    def __init__(self):
         # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

        # Barras (fichas capturadas)
        self.__barra_blancas__ = []
        self.__barra_negras__ = []

        # Posiciones iniciales estándar del Backgammon
        # Blancas
        self.__contenedor__[0] = ["negra"]*2
        self.__contenedor__[11] = ["negra"]*5
        self.__contenedor__[16] = ["negra"]*3
        self.__contenedor__[18] = ["negra"]*5

        # Negras
        self.__contenedor__[23] = ["blanca"]*2
        self.__contenedor__[12] = ["blanca"]*5
        self.__contenedor__[7] = ["blanca"]*3
        self.__contenedor__[5] = ["blanca"]*5
    
    def get_contenedor(self):
        # Muestra el contenedor
        return self.__contenedor__

    def get_fichas(self, posicion)
        # devuelve una copia de las fichas en una posicion
        return list(self.__contenedor__[posicion])

    def contar_fichas(self, posicion):
        # Cantidad de fichas en una posición
        return len(self.__contenedor__[posicion])

    def color_en_posicion(self, posicion):
        # Devuelve el color de las fichas en una posición (None si está vacía)
        if not self.__contenedor__[posicion]:
            return None
        return self.__contenedor__[posicion][0]

    def guardar_ficha(self, posicion, color):
        # Agrega una ficha en la posición indicada
        self.__contenedor__[posicion].append(color)

    def quitar_ficha(self, posicion):
        # Saca una ficha de la posición indicada
        if self.__contenedor__[posicion]:
            return self.__contenedor__[posicion].pop()
        return None
    
    def mover_ficha(self, origen, destino):
        # Mueve una ficha desde origen a destino (si es posible)
        ficha = self.__contenedor__[origen].pop()
        self.__contenedor__[destino].append(ficha)
    
    def enviar_a_barra(self):
        ...
    
    def reingrasar_desde_barra(self):
        ...
    
    def fichas_en_barra(self):
        ...

    def sacar_ficha(self, posicion):
        #Saca una ficha del tablero
        return self.quitar_ficha(posicion)
