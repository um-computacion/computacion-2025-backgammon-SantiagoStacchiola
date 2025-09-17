from core.board import Board
from core.dice import Dice
from core.player import Player

class BackgammonGame:
    #Lógica principal del juego de Backgammon.
    def __init__(self):
        self._tablero = Board()
        self._dado = Dice()
        self._jugador_blancas = Player("blanca")
        self._jugador_negras = Player("negra")
        self._turno = self._jugador_blancas

    def get_turno(self):
        #Devuelve el jugador en turno.
        return self._turno

    def cambiar_turno(self):
        #Cambia el turno al otro jugador y resetea los dados.
        if self._turno == self._jugador_blancas:
            self._turno = self._jugador_negras
        else:
            self._turno = self._jugador_blancas
        self._dado.__init__()  # reinicia los valores de los dados

    def tirar_dados(self):
        #Tira los dados para el jugador en turno.
        return self._dado.tirar()

    def usar_valor_dado(self, valor):
        #Usa un valor de dado si está disponible.
        # Usar el atributo real de Dice
        if hasattr(self._dado, "__valores__") and valor in self._dado.__valores__:
            self._dado.__valores__.remove(valor)
            return True
        return False

    def quedan_movimientos(self):
        #Devuelve True si quedan valores de dado por usar.
        return self._dado.quedan_valores()

    def movimiento_valido(self, origen, destino):
        #Verifica si un movimiento es válido según las reglas básicas.
        color = self._turno.get_color()
        fichas_origen = self._tablero.get_fichas(origen)
        fichas_destino = self._tablero.get_fichas(destino)
        if not fichas_origen:
            return False
        if fichas_origen[0].obtener_color() != color:
            return False
        if not fichas_destino:
            return True
        if fichas_destino[0].obtener_color() == color:
            return True
        if len(fichas_destino) == 1:
            return True
        return False

    def mover(self, origen, destino, valor_dado):
        #Mueve una ficha si el movimiento es válido y el dado corresponde.
        color = self._turno.get_color()
        if not self.usar_valor_dado(valor_dado):
            raise ValueError(f"El valor {valor_dado} no está disponible en los dados")
        if not self.movimiento_valido(origen, destino):
            raise ValueError("Movimiento inválido")
        fichas_destino = self._tablero.get_fichas(destino)
        if fichas_destino and fichas_destino[0].obtener_color() != color and len(fichas_destino) == 1:
            ficha_capturada = self._tablero.quitar_ficha(destino)
            self._tablero.enviar_a_barra(ficha_capturada)
        self._tablero.mover_ficha(origen, destino)

    def get_tablero(self):
        #Devuelve el estado del tablero (contenedor de posiciones).
        return self._tablero.get_contenedor()

    def verificar_victoria(self):
        #Verifica si el jugador en turno ganó (todas sus fichas fuera)
        return self._turno.fichas_restantes() == 0
