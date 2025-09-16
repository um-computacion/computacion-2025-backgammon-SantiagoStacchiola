class Ficha:
    def __init__(self, color: str, posicion=None):
        if color not in ["blanca", "negra"]:
            raise ValueError("Color inválido: debe ser 'blanca' o 'negra'")
        self.__color__ = color
        self.__posicion__ = posicion

    def obtener_color(self):
        return self.__color__

    def obtener_posicion(self):
        return self.__posicion__
    
    def mover(self, nueva_posicion):
        #Cambia la posición de la ficha
        self.__posicion__ = nueva_posicion
    
    def esta_en_barra(self):
        return self.__posicion__ == "barra"

    def esta_afuera(self):
        return self.__posicion__ == "afuera"

    def __repr__(self):
        return f"Ficha({self.__color__}, pos={self.__posicion__})"