class Tablero:
    def __init__(self, ):
        self.__contenedor__ = [0]*24
        self.__contenedor__[0] = -2
        self.__contenedor__[11] = -5
        self.__contenedor__[16] = -3
        self.__contenedor__[18] = -5
        self.__contenedor__[23] = 2
        self.__contenedor__[12] = 5
        self.__contenedor__[7] = 3
        self.__contenedor__[5] = 5
    def guardar_ficha(self, ):
        ...
    def get_contenedor(self, ):
        return self.__contenedor__