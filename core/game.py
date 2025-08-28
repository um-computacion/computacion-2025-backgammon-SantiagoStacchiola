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

    def get_turno(self):
        # Muestra el turno
        return self.__turno__
    
    def cambiar_turno(self):
        # Pasa el turno al otro jugador
        if self.__turno__ == self.__jugador_blancas__:
            self.__turno__ = self.__jugador_negras__
        else:
            self.__turno__ = self.__jugador_blancas__
        # Resetear los dados para el nuevo turno
        self.__dado__.reset()

    def tirar_dados(self):
        # Tira los dados para el jugador en turno
        return self.__dado__.tirar()

    def get_valores_dados(self):
        # Muestra el dado
        return self.__dado__.get_valores()

    def usar_valor_dado(self, valor):
        # Usa el numero del dado
        return self.__dado__.usar_valor(valor)

    def quedan_movimientos(self):
        # Verifica si quedan movimientos 
        return self.__dado__.quedan_valores()

    def movimiento_valido(self, origen, destino):
        color = self.__turno__.get_color()
        fichas_origen = self.__tablero__.get_fichas(origen)
        fichas_destino = self.__tablero__.get_fichas(destino)

        # No hay ficha en origen
        if not fichas_origen:
            return False
        # Ficha no pertenece al jugador en turno
        if fichas_origen[0] != color:
            return False
        # Destino vacío
        if not fichas_destino:
            return True
        # Destino ocupado por fichas propias
        if fichas_destino[0] == color:
            return True
        # Destino con UNA ficha rival → captura posible
        if len(fichas_destino) == 1:
            return True
        return False

    def mover(self, origen, destino, valor_dado):
        # Intenta mover una ficha según las reglas
        color = self.__turno__.get_color()

        # Verificar que el valor del dado esté disponible
        if not self.usar_valor_dado(valor_dado):
            raise ValueError(f"El valor {valor_dado} no está disponible en los dados")

        # Validar movimiento
        if not self.movimiento_valido(origen, destino):
            raise ValueError("Movimiento inválido")

        # Captura si hay 1 ficha enemiga
        fichas_destino = self.__tablero__.get_fichas(destino)
        if fichas_destino and fichas_destino[0] != color and len(fichas_destino) == 1:
            ficha_capturada = self.__tablero__.quitar_ficha(destino)
            self.__tablero__.enviar_a_barra(ficha_capturada)

        # Ejecutar movimiento
        self.__tablero__.mover_ficha(origen, destino)

    def get_tablero(self):
        # Muestra el tablero
        return self.__tablero__.get_contenedor()

    def verificar_victoria(self):
        # Verifica si el jugador gano
        color = self.__turno__.get_color()
        return self.__tablero__.puede_sacar_fichas(color)



