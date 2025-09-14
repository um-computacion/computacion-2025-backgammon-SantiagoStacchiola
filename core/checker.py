class Ficha:
    def __init__(self, color: str, posicion=None):
        if color not in ["blanca", "negra"]:
            raise ValueError("Color inválido: debe ser 'blanca' o 'negra'")
        self.__color__ = color
        self.__posicion__ = posicion 