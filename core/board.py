class Tablero:
    def __init__(self):
         # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

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
    
    def quitar_ficha(self, posicion):
        # Saca una ficha de la posición indicada
        if self.__contenedor__[posicion]:
            return self.__contenedor__[posicion].pop()
        return None
    
    def get_contenedor(self):
        # Muestra el contenedor
        return self.__contenedor__
    
    def mover_ficha(self, origen, destino):
        # Mueve una ficha desde `origen` a `destino` (si es posible).
        if not self.__contenedor__[origen]:
            raise ValueError("No hay fichas en la posición de origen")
        # Elimina una ficha
        ficha = self.__contenedor__[origen].pop()
        # Guarda una ficha
        self.__contenedor__[destino].append(ficha)
    
    def puede_sacar_fichas(self, color):
         # Verifica si todas las fichas del jugador están en su último cuadrante.
        if color == "blanca":
         # blancas en posiciones 18–23
            return all(ficha == "blanca" for i in range(18, 24) for ficha in self.__contenedor__[i])
        else:
         # negras en posiciones 0–5
            return all(ficha == "negra" for i in range(0, 6) for ficha in self.__contenedor__[i])


