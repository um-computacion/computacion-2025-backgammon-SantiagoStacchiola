"""Módulo que orquesta la lógica del juego (turnos, reglas y flujo)."""

# pylint: disable=missing-function-docstring

from core.dice import Dice
from core.board import Board
from core.player import Player
from core.excepcions import MovimientoInvalidoError, DadoNoDisponibleError, PosicionVaciaError

class Game:  # pylint: disable=R0902
    """Controla el flujo de una partida entre dos jugadores."""

    def __init__(self, player1=None, player2=None):
        """Inicializa la partida; players son opcionales para facilitar tests."""
        # Si no se proporcionan jugadores, crear jugadores por defecto para los tests
        if player1 is None:
            player1 = Player("blanca")
        if player2 is None:
            player2 = Player("negra")

        self._players = (player1, player2)
        self._turn = 0
        self._turno = self._players[0]  # Cambiar para que sea el objeto jugador
        # Instanciar en lugar de llamar a dunder __init__
        self._dice = Dice()
        self._dado = self._dice
        self._board = Board()
        self._tablero = self._board
        self._state = "initialized"

    def get_turno(self):
        # Devuelve el jugador en turno (objeto jugador, no índice)
        return self._players[self._turn]

    def cambiar_turno(self):
        # Cambia el turno al otro jugador y resetea los dados.
        self._turn = (self._turn + 1) % 2
        self._turno = self._players[self._turn]  # Actualizar para que sea el objeto jugador
        self._dice = Dice()  # Crear nueva instancia en lugar de __init__

    def usar_valor_dado(self, valor):
        # Usa un valor de dado si está disponible.
        # Usar el atributo real de Dice
        if hasattr(self._dice, "__valores__") and valor in self._dice.__valores__:
            self._dice.__valores__.remove(valor)
            return True
        return False

    def quedan_movimientos(self):
        # Devuelve True si quedan valores de dado por usar.
        return self._dice.quedan_valores()

    def movimiento_valido(self, origen, destino):
        # Verifica si un movimiento es válido según las reglas básicas.
        color = self._players[self._turn].get_color()
        fichas_origen = self._board.get_fichas(origen)
        fichas_destino = self._board.get_fichas(destino)
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
        # Mueve una ficha si el movimiento es válido y el dado corresponde.
        color = self._players[self._turn].get_color()
        if not self.usar_valor_dado(valor_dado):
            raise DadoNoDisponibleError(f"El valor {valor_dado} no está disponible en los dados")
        
        # Verificar si hay fichas en origen antes de validar el movimiento
        fichas_origen = self._board.get_fichas(origen)
        if not fichas_origen:
            raise PosicionVaciaError(f"No hay fichas en la posición {origen}")
            
        if not self.movimiento_valido(origen, destino):
            raise MovimientoInvalidoError("Movimiento inválido")
        fichas_destino = self._board.get_fichas(destino)
        if fichas_destino and fichas_destino[0].obtener_color() != color and len(fichas_destino) == 1:
            ficha_capturada = self._board.quitar_ficha(destino)
            self._board.enviar_a_barra(ficha_capturada)
        self._board.mover_ficha(origen, destino)

    def get_tablero(self):
        # Devuelve el estado del tablero (contenedor de posiciones).
        return self._board.get_contenedor()

    def verificar_victoria(self):
        # Verifica si el jugador en turno ganó (todas sus fichas fuera)
        return self._players[self._turn].fichas_restantes() == 0

    def next_turn(self):
        """Avanza el turno al siguiente jugador y prepara la tirada."""
        self._turn = (self._turn + 1) % 2
        self._turno = self._players[self._turn]  # Actualizar para que sea el objeto jugador
        # línea corta para evitar C0301
        self._state = "waiting"

    def tirar_dados(self):
        """Realiza la tirada de dados usando la API disponible en Dice."""
        if hasattr(self._dado, "tirar"):
            return self._dado.tirar()
        if hasattr(self._dado, "roll"):
            return self._dado.roll()
        raise AttributeError("El objeto dado no expone método de tirada conocido")

# alias en español para compatibilidad
BackgammonGame = Game
# EOF
