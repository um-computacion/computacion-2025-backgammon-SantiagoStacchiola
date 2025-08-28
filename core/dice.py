import random

class Dice:
    def __init__(self):
        # guarda la tirada actual
        self.__valores__ = []

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
    
    def usar_valor(self, valor):
        # Consume un valor de la tirada si está disponible
        if valor in self.__valores__:
            self.__valores__.remove(valor)
            return True
        return False

    def quedan_valores(self):
        # Devuelve True si todavía quedan movimientos posibles
        return len(self.__valores__) > 0
    
    def reset(self):
        # Vacia los valores (cuando termina el turno)
        self.__valores__ = []
    