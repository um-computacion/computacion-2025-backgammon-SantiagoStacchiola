class Player:
    def __init__(self, color: str):
        if color not in ["blanca", "negra"]:
            raise ValueError("Color inválido, debe ser 'blanca' o 'negra'")
        
        self.__color__ = color
        self.__total_fichas__ = 15
        self.__barra__ = []            # fichas capturadas
        self.__fuera__ = []            # fichas que ya salieron 

    def get_color(self):
        # Muestra el color
        return self.__color__
    
    def get_total_fichas(self):
        return self.__total_fichas__

    def enviar_a_barra(self):
        # Agrega una ficha a la barra
        self.__barra__.append(self.__color__)
    
    def sacar_de_barra(self):
        # Saca una ficha de la barra (si existe)
        if self.__barra__:
            return self.__barra__.pop()
        return None
    
    def fichas_en_barra(self):
        return len(self.__barra__)

    def sacar_del_tablero(self):
        # Agrega una ficha a la zona de fichas fuera
        self.__fuera__.append(self.__color__)

    def fichas_fuera(self):
        return len(self.__fuera__)

    def fichas_restantes(self):
        # Cantidad de fichas que aún tiene en juego
        return self.__total_fichas__ - len(self.__fuera__)
