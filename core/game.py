"""Módulo que orquesta la lógica del juego (turnos, reglas y flujo)."""

# pylint: disable=missing-function-docstring

from core.dice import Dice
from core.board import Board
from core.player import Player
from core.excepcions import (MovimientoInvalidoError, DadoNoDisponibleError,
                            PosicionVaciaError, PosicionBloqueadaError,
                            MovimientoColorError)

class Game:  # pylint: disable=R0902
    """Controla el flujo de una partida entre dos jugadores."""

    def __init__(self, player1=None, player2=None):
        """Inicializa la partida; players son opcionales para facilitar tests."""
        # Si no se proporcionan jugadores, crear jugadores por defecto para los tests
        if player1 is None:
            player1 = Player("blanca")
        if player2 is None:
            player2 = Player("negra")

        self.__players__ = (player1, player2)
        self.__turn__ = 0
        self.__turno__ = self.__players__[0]  # Cambiar para que sea el objeto jugador
        # Instanciar en lugar de llamar a dunder __init__
        self.__dice__ = Dice()
        self.__dado__ = self.__dice__
        self.__board__ = Board()
        self.__tablero__ = self.__board__
        self.__state__ = "initialized"

    def get_turno(self):
        # Devuelve el jugador en turno (objeto jugador, no índice)
        return self.__players__[self.__turn__]

    def cambiar_turno(self):
        # Cambia el turno al otro jugador y resetea los dados.
        self.__turn__ = (self.__turn__ + 1) % 2
        # Actualizar para que sea el objeto jugador
        self.__turno__ = self.__players__[self.__turn__]
        self.__dice__ = Dice()  # Crear nueva instancia en lugar de __init__

    def usar_valor_dado(self, valor):
        # Usa un valor de dado si está disponible.
        # Usar el atributo real de Dice
        if hasattr(self.__dice__, "__valores__") and valor in self.__dice__.__valores__:
            self.__dice__.__valores__.remove(valor)
            return True
        return False

    def quedan_movimientos(self):
        # Devuelve True si quedan valores de dado por usar.
        return self.__dice__.quedan_valores()

    def movimiento_valido(self, origen, destino):
        # Verifica si un movimiento es válido según las reglas básicas.
        color = self.__players__[self.__turn__].get_color()
        fichas_origen = self.__board__.get_fichas(origen)
        fichas_destino = self.__board__.get_fichas(destino)
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
        color = self.__players__[self.__turn__].get_color()
        if not self.usar_valor_dado(valor_dado):
            raise DadoNoDisponibleError(
                f"El valor {valor_dado} no está disponible en los dados")

        # Verificar si hay fichas en origen antes de validar el movimiento
        fichas_origen = self.__board__.get_fichas(origen)
        if not fichas_origen:
            raise PosicionVaciaError(f"No hay fichas en la posición {origen}")

        # Verificar si la ficha es del color correcto
        if fichas_origen[0].obtener_color() != color:
            raise MovimientoColorError(
                f"La ficha en posición {origen} es {fichas_origen[0].obtener_color()}, "
                f"pero el turno es de {color}")

        # Verificar si el destino está bloqueado
        fichas_destino = self.__board__.get_fichas(destino)
        if (fichas_destino and fichas_destino[0].obtener_color() != color
                and len(fichas_destino) > 1):
            raise PosicionBloqueadaError(
                f"La posición {destino} está bloqueada por "
                f"{len(fichas_destino)} fichas enemigas")

        if not self.movimiento_valido(origen, destino):
            raise MovimientoInvalidoError("Movimiento inválido")

        # Realizar captura si es posible
        if (fichas_destino and fichas_destino[0].obtener_color() != color
                and len(fichas_destino) == 1):
            ficha_capturada = self.__board__.quitar_ficha(destino)
            self.__board__.enviar_a_barra(ficha_capturada)
        self.__board__.mover_ficha(origen, destino)

    def get_tablero(self):
        # Devuelve el estado del tablero (contenedor de posiciones).
        return self.__board__.get_contenedor()

    def verificar_victoria(self):
        # Verifica si el jugador en turno ganó (todas sus fichas fuera)
        return self.__players__[self.__turn__].fichas_restantes() == 0

    def siguiente_turno(self):
        """Avanza el turno al siguiente jugador y prepara la tirada."""
        self.__turn__ = (self.__turn__ + 1) % 2
        # Actualizar para que sea el objeto jugador
        self.__turno__ = self.__players__[self.__turn__]
        # línea corta para evitar C0301
        self.__state__ = "waiting"

    # Alias en inglés para compatibilidad con tests existentes
    def next_turn(self):
        """Alias en inglés para siguiente_turno()."""
        return self.siguiente_turno()

    def tirar_dados(self):
        """Realiza la tirada de dados usando la API disponible en Dice."""
        if hasattr(self.__dado__, "tirar"):
            return self.__dado__.tirar()
        if hasattr(self.__dado__, "roll"):
            return self.__dado__.roll()
        raise AttributeError("El objeto dado no expone método de tirada conocido")

    def turno_completo(self):
        """Ejecuta un turno completo del jugador actual."""
        # Mostrar estado del juego
        self.__board__.mostrar_tablero()
        print(f"\n>>> Turno del jugador: {self.get_turno().get_color().upper()} <<<")
        
        # Lanzar dados
        self.tirar_dados()
        dice = self.__dice__
        if hasattr(dice, '__valores__') and dice.__valores__:
            print(f"Dados disponibles: {dice.__valores__}")
        else:
            print("No hay dados disponibles")
        
        # Verificar si hay movimientos disponibles
        if not self.quedan_movimientos():
            print("No hay movimientos disponibles. Pasando turno...")
            return True
        
        # Bucle básico de entrada (simplificado por ahora)
        while self.quedan_movimientos():
            entrada = input("\n> ").strip().lower()
            
            if entrada == 'quit':
                return 'quit'
            elif entrada == 'pass':
                print("Pasando turno...")
                break
            else:
                print("Entrada no reconocida. Use 'pass' o 'quit'")
        
        return True

# alias en español para compatibilidad
BackgammonGame = Game
# EOF
