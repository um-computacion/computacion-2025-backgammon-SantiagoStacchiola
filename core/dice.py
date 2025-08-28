import random

class Dice:
    def __init__(self):
        self.__valores__ = []  # guarda la tirada actual

    def tirar(self):
        # Lanza los dados y guarda el resultado
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)

        if d1 == d2:
            # Doble → cuatro movimientos
            self.__valores__ = [d1] * 4
        else:
            self.__valores__ = [d1, d2]

        return self.__valores__
    
    def get_valores(self):
        # Devuelve los valores de los dados
        return self.__valores__
    
