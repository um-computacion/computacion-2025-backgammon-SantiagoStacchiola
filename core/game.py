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

    def todas_fichas_en_home(self, jugador=None):
        """Verifica si todas las fichas del jugador están en su home board."""
        if jugador is None:
            jugador = self.get_turno()
        
        tablero = self.get_tablero()
        color = jugador.get_color()
        
        # Home board para blancas: posiciones 19-24 (índices 18-23)
        # Home board para negras: posiciones 1-6 (índices 0-5)
        if color == "blanca":
            fuera_home_range = range(0, 18)
        else:
            fuera_home_range = range(6, 24)
        
        # Verificar que no haya fichas fuera del home board
        for i in fuera_home_range:
            if tablero[i]:
                for ficha in tablero[i]:
                    if ficha.obtener_color() == color:
                        return False
        
        # Verificar que no haya fichas en la barra
        if self.__board__.fichas_en_barra(color) > 0:
            return False
            
        return True

    def ejecutar_movimiento_barra(self, destino, dado):
        """Ejecuta un movimiento desde la barra."""
        jugador = self.get_turno()
        color = jugador.get_color()
        
        # Verificar que hay fichas en la barra
        if self.__board__.fichas_en_barra(color) == 0:
            return False, "No tienes fichas en la barra"
        
        # Verificar que el destino no esté bloqueado
        tablero = self.get_tablero()
        fichas_destino = tablero[destino]
        if (fichas_destino and 
            fichas_destino[0].obtener_color() != color and 
            len(fichas_destino) > 1):
            return False, f"Posición {destino + 1} está bloqueada"
        
        # Usar dado y reingresar
        if not self.usar_valor_dado(dado):
            return False, f"El dado {dado} no está disponible"
        
        self.__board__.reingresar_desde_barra(color, destino)
        return True, "Ficha reingresada desde la barra"

    def ejecutar_bearing_off(self, origen, dado):
        """Ejecuta un bearing off."""
        jugador = self.get_turno()
        
        # Verificar que todas las fichas estén en home board
        if not self.todas_fichas_en_home(jugador):
            return False, "Todas las fichas deben estar en el home board para bearing off"
        
        # Usar dado y sacar ficha
        if not self.usar_valor_dado(dado):
            return False, f"El dado {dado} no está disponible"
        
        ficha_sacada = self.__board__.sacar_ficha(origen)
        if ficha_sacada:
            jugador.sacar_del_tablero(ficha_sacada)
            return True, "Ficha sacada del tablero (bearing off)"
        else:
            return False, f"No hay fichas en posición {origen + 1}"

    def mostrar_dados_disponibles(self):
        """Devuelve una cadena con los dados disponibles."""
        dice = self.__dice__
        if hasattr(dice, '__valores__') and dice.__valores__:
            return f"Dados disponibles: {dice.__valores__}"
        else:
            return "No hay dados disponibles"

    def mostrar_turno_actual(self):
        """Devuelve información del turno actual."""
        jugador = self.get_turno()
        return f"Turno del jugador: {jugador.get_color().upper()}"

    def obtener_opciones_movimiento(self):
        """Devuelve las opciones de movimiento disponibles para el jugador actual."""
        jugador = self.get_turno()
        fichas_en_barra = self.__board__.fichas_en_barra(jugador.get_color())
        
        opciones = []
        if fichas_en_barra > 0:
            opciones.append("⚠️  Tienes fichas en la barra. Debes reingresarlas primero.")
            opciones.append("- Reingresar desde barra: barra,destino,dado (ej: barra,3,3)")
        else:
            opciones.append("- Movimiento normal: origen,destino,dado (ej: 1,7,6)")
            opciones.append("- Bearing off: origen,off,dado (ej: 19,off,3)")
        
        opciones.append("- Pasar turno: 'pass'")
        opciones.append("- Salir: 'quit'")
        
        return opciones

    def mostrar_estado_juego(self):
        """Muestra el estado completo del juego."""
        self.__board__.mostrar_tablero()
        print(f"\n>>> {self.mostrar_turno_actual()} <<<")
        print(self.mostrar_dados_disponibles())

    def procesar_entrada_usuario(self, entrada):
        """Procesa la entrada del usuario y devuelve el movimiento parseado."""
        entrada = entrada.strip().lower()
        
        if entrada == 'quit':
            return 'quit', None
        elif entrada == 'pass':
            return 'pass', None
        
        try:
            partes = entrada.split(',')
            if len(partes) != 3:
                return None, "Error: Use formato origen,destino,dado"
            
            origen_str = partes[0].strip()
            destino_str = partes[1].strip()
            dado = int(partes[2].strip())
            
            # Manejo especial para barra y bearing off
            if origen_str == 'barra':
                return ('barra', int(destino_str) - 1, dado), None
            elif destino_str == 'off':
                return (int(origen_str) - 1, 'off', dado), None
            else:
                origen = int(origen_str)
                destino = int(destino_str)
                # Convertir a índices (el usuario usa 1-24, el sistema 0-23)
                return (origen - 1, destino - 1, dado), None
            
        except ValueError:
            return None, "Error: Ingrese números válidos"

    def ejecutar_movimiento_completo(self, origen, destino, dado):
        """Ejecuta un movimiento completo y devuelve el resultado."""
        try:
            # Manejo de reingresar desde barra
            if origen == 'barra':
                exito, mensaje = self.ejecutar_movimiento_barra(destino, dado)
                return exito, f"{'✓' if exito else '✗'} {mensaje}"
            
            # Manejo de bearing off
            elif destino == 'off':
                exito, mensaje = self.ejecutar_bearing_off(origen, dado)
                return exito, f"{'✓' if exito else '✗'} {mensaje}"
            
            # Movimiento normal
            else:
                self.mover(origen, destino, dado)
                return True, "✓ Movimiento realizado exitosamente"
                
        except (MovimientoInvalidoError, DadoNoDisponibleError, 
                PosicionVaciaError, PosicionBloqueadaError, 
                MovimientoColorError) as e:
            return False, f"✗ Error: {e}"

    def verificar_fin_juego_completo(self):
        """Verifica si el juego ha terminado y muestra el mensaje correspondiente."""
        if self.verificar_victoria():
            ganador = self.get_turno()
            print(f"\n🎉 ¡JUEGO TERMINADO! 🎉")
            print(f"¡Ganó el jugador {ganador.get_color().upper()}!")
            return True
        return False

    def obtener_entrada_usuario(self):
        """Obtiene la entrada del usuario con las opciones disponibles."""
        print("\nOpciones:")
        opciones = self.obtener_opciones_movimiento()
        for opcion in opciones:
            print(f"  {opcion}")
        
        return input("\n> ")

    def turno_completo(self):
        """Ejecuta un turno completo del jugador actual."""
        # Mostrar estado del juego
        self.mostrar_estado_juego()
        
        # Lanzar dados
        self.tirar_dados()
        print(self.mostrar_dados_disponibles())
        
        # Verificar si hay movimientos disponibles
        if not self.quedan_movimientos():
            print("No hay movimientos disponibles. Pasando turno...")
            return True
        
        # Jugador hace movimientos
        movimientos_realizados = False
        while self.quedan_movimientos():
            entrada = self.obtener_entrada_usuario()
            movimiento, error = self.procesar_entrada_usuario(entrada)
            
            if movimiento == 'quit':
                return 'quit'
            elif movimiento == 'pass':
                print("Pasando turno...")
                break
            elif error:
                print(error)
                continue
            elif movimiento is None:
                continue
            
            origen, destino, dado = movimiento
            
            exito, mensaje = self.ejecutar_movimiento_completo(origen, destino, dado)
            print(mensaje)
            
            if exito:
                movimientos_realizados = True
                
                # Verificar si el juego terminó
                if self.verificar_fin_juego_completo():
                    return 'fin'
            
            # Mostrar dados restantes después de un movimiento exitoso
            if movimientos_realizados:
                print(self.mostrar_dados_disponibles())
        
        return True

# alias en español para compatibilidad
BackgammonGame = Game
# EOF
