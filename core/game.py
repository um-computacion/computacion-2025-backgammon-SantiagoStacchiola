from core.board import Tablero
from core.dice import Dice
from core.player import Player

class BackgammonGame:
    def __init__(self):
        # Tablero y lógica central
        self.__tablero__ = Tablero()
        self.__dado__ = Dice()

        # Jugadores
        self.__jugador_blancas__ = Player("blanca")
        self.__jugador_negras__ = Player("negra")

        # Arranca siempre el mismo o se sortea
        self.__turno__ = self.__jugador_blancas__
    
    def get_tablero(self):
        # Muestra el tablero
        return self.__tablero__

    def get_turno(self):
        # Muestra el turno
        return self.__turno__
    
    def cambiar_turno(self):
        # Pasa el turno al otro jugador
        if self.__turno__ == self.__jugador_blancas__:
            self.__turno__ = self.__jugador_negras__
        else:
            self.__turno__ = self.__jugador_blancas__

    def verificar_victoria(self):
        # Verifica si el jugador gano
        color = self.__turno__.get_color()
        if self.__tablero__.puede_sacar_fichas(color):
            # condición simplificada: todas fuera
            return True
        return False  


