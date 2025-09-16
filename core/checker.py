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
    
    