"""Módulo que orquesta la lógica del juego (turnos, reglas y flujo)."""

from core.dice import Dice
from core.board import Board
from core.player import Player
from core.excepcions import (MovimientoInvalidoError, DadoNoDisponibleError,
                            PosicionVaciaError, PosicionBloqueadaError,
                            MovimientoColorError)

class Game:
    """Controla el flujo de una partida entre dos jugadores."""

    def __init__(self, player1=None, player2=None):
        """Inicializa la partida; jugadores son opcionales para facilitar tests."""
        self.__players__ = (player1 or Player("blanca"), player2 or Player("negra"))
        self.__turn__ = 0
        self.__dice__ = Dice()
        self.__dado__ = self.__dice__
        self.__board__ = Board()
        self.__tablero__ = self.__board__
        self.__state__ = "initialized"

    def get_turno(self):
        """Devuelve el jugador en turno."""
        return self.__players__[self.__turn__]

    def cambiar_turno(self):
        """Cambia el turno al otro jugador."""
        self.__turn__ = (self.__turn__ + 1) % 2
        # No resetear dados aquí - se tiran en turno_completo()

    def usar_valor_dado(self, valor):
        """Usa un valor de dado si está disponible."""
        if hasattr(self.__dice__, "__valores__") and valor in self.__dice__.__valores__:
            self.__dice__.__valores__.remove(valor)
            return True
        return False

    def quedan_movimientos(self):
        """Devuelve True si quedan valores de dado por usar."""
        return self.__dice__.quedan_valores()

    def movimiento_valido(self, origen, destino):
        """Verifica si un movimiento es válido según las reglas básicas."""
        color = self.__players__[self.__turn__].get_color()
        fichas_origen = self.__board__.get_fichas(origen)
        fichas_destino = self.__board__.get_fichas(destino)

        if not fichas_origen or fichas_origen[0].obtener_color() != color:
            return False
        if not fichas_destino or fichas_destino[0].obtener_color() == color:
            return True
        return len(fichas_destino) == 1

    def mover(self, origen, destino, valor_dado):
        """Mueve una ficha si el movimiento es válido y el dado corresponde."""
        color = self.__players__[self.__turn__].get_color()

        fichas_origen = self.__board__.get_fichas(origen)
        if not fichas_origen:
            raise PosicionVaciaError()

        if fichas_origen[0].obtener_color() != color:
            raise MovimientoColorError()

        fichas_destino = self.__board__.get_fichas(destino)
        if (fichas_destino and fichas_destino[0].obtener_color() != color and
            len(fichas_destino) > 1):
            raise PosicionBloqueadaError()

        if not self.movimiento_valido(origen, destino):
            raise MovimientoInvalidoError()

        # Consumir el dado SOLO después de validar todo
        if not self.usar_valor_dado(valor_dado):
            raise DadoNoDisponibleError()

        # Realizar captura si es posible
        if (fichas_destino and fichas_destino[0].obtener_color() != color and
            len(fichas_destino) == 1):
            ficha_capturada = self.__board__.quitar_ficha(destino)
            self.__board__.enviar_a_barra(ficha_capturada)
        self.__board__.mover_ficha(origen, destino)

    def get_tablero(self):
        """Devuelve el estado del tablero (contenedor de posiciones)."""
        return self.__board__.get_contenedor()

    def verificar_victoria(self):
        """Verifica si el jugador en turno ganó (todas sus fichas fuera)."""
        return self.__players__[self.__turn__].fichas_restantes() == 0

    def siguiente_turno(self):
        """Avanza el turno al siguiente jugador y prepara la tirada."""
        self.__turn__ = (self.__turn__ + 1) % 2
        self.__state__ = "waiting"

    def next_turn(self):
        """Alias en inglés para siguiente_turno()."""
        return self.siguiente_turno()

    def tirar_dados(self):
        """Realiza la tirada de dados usando la API disponible en Dice."""
        if hasattr(self.__dice__, "tirar"):
            return self.__dice__.tirar()
        if hasattr(self.__dice__, "roll"):
            return self.__dice__.roll()
        raise AttributeError("El objeto dado no expone método de tirada conocido")

    # --- Métodos auxiliares para UI (no afectan lógica ni tests) ---
    def get_players(self):
        """Devuelve la tupla de jugadores (blanca, negra)."""
        return self.__players__

    def get_player_by_color(self, color):
        """Obtiene el jugador por color ('blanca' o 'negra')."""
        for p in self.__players__:
            if p.get_color() == color:
                return p
        return None

    def fichas_en_barra(self, color):
        """Cantidad de fichas de un color en la barra central (desde Board)."""
        return self.__board__.fichas_en_barra(color)

    def fichas_fuera(self, color):
        """Cantidad de fichas de un color fuera del tablero (borne-off)."""
        jugador = self.get_player_by_color(color)
        return jugador.fichas_fuera() if jugador else 0

    def get_dados_disponibles(self):
        """Devuelve una copia de los valores de dados aún disponibles."""
        if hasattr(self.__dice__, '__valores__'):
            return list(self.__dice__.__valores__)
        return []

    def todas_fichas_en_home(self, jugador=None):
        """Verifica si todas las fichas del jugador están en su tablero local."""
        jugador = jugador or self.get_turno()
        tablero, color = self.get_tablero(), jugador.get_color()

        # Determinar rango fuera del home board según color
        fuera_home_range = range(0, 18) if color == "blanca" else range(6, 24)

        # Verificar fichas fuera del home board
        for i in fuera_home_range:
            if any(f.obtener_color() == color for f in tablero[i]):
                return False

        return self.__board__.fichas_en_barra(color) == 0

    def ejecutar_movimiento_barra(self, destino, dado):
        """Ejecuta un movimiento desde la barra."""
        color = self.get_turno().get_color()

        if self.__board__.fichas_en_barra(color) == 0:
            return False, "No tienes fichas en la barra"

        fichas_destino = self.get_tablero()[destino]
        if (fichas_destino and fichas_destino[0].obtener_color() != color and
            len(fichas_destino) > 1):
            return False, f"Posición {destino + 1} está bloqueada"

        # Consumir el dado SOLO si el movimiento es legal (no bloqueado)
        if not self.usar_valor_dado(dado):
            return False, f"El dado {dado} no está disponible"

        # Captura si hay exactamente una ficha rival en destino (blot)
        fichas_destino = self.get_tablero()[destino]
        if (fichas_destino and fichas_destino[0].obtener_color() != color and
            len(fichas_destino) == 1):
            ficha_capturada = self.__board__.quitar_ficha(destino)
            self.__board__.enviar_a_barra(ficha_capturada)

        # Reingresar la ficha propia desde la barra
        self.__board__.reingresar_desde_barra(color, destino)
        return True, "Ficha reingresada desde la barra"

    def ejecutar_bearing_off(self, origen, dado):
        """Ejecuta el movimiento de sacar una ficha del tablero."""
        jugador = self.get_turno()

        if not self.todas_fichas_en_home(jugador):
            return False, "Todas las fichas deben estar en el tablero local para sacar"

        if not self.usar_valor_dado(dado):
            return False, f"El dado {dado} no está disponible"

        ficha_sacada = self.__board__.sacar_ficha(origen)
        if ficha_sacada:
            jugador.sacar_del_tablero(ficha_sacada)
            return True, "Ficha sacada del tablero"
        return False, f"No hay fichas en posición {origen + 1}"

    def mostrar_dados_disponibles(self):
        """Devuelve una cadena con los dados disponibles."""
        dice = self.__dice__
        if hasattr(dice, '__valores__') and dice.__valores__:
            return f"Dados disponibles: {dice.__valores__}"
        return "No hay dados disponibles"

    def mostrar_turno_actual(self):
        """Devuelve información del turno actual."""
        jugador = self.get_turno()
        return f"Turno del jugador: {jugador.get_color().upper()}"

    def obtener_opciones_movimiento(self):
        """Devuelve las opciones de movimiento disponibles para el jugador actual."""
        fichas_en_barra = self.__board__.fichas_en_barra(self.get_turno().get_color())
        
        opciones = ["AVISO: Tienes fichas en la barra. Debes reingresarlas primero.",
                   "- Reingresar desde barra: barra,destino,dado (ej: barra,3,3)"] if fichas_en_barra > 0 else [
                   "- Movimiento normal: origen,destino,dado (ej: 1,7,6)",
                   "- Sacar ficha: origen,off,dado (ej: 19,off,3)"]
        
        opciones.extend(["- Pasar turno: 'pass'", "- Salir: 'quit'"])
        return opciones

    def mostrar_estado_juego(self):
        """Muestra el estado completo del juego."""
        self.__board__.mostrar_tablero()
        print(f"\n{self.mostrar_turno_actual()}")
        print(self.mostrar_dados_disponibles())

    def procesar_entrada_usuario(self, entrada):
        """Procesa la entrada del usuario y devuelve el movimiento parseado."""
        entrada = entrada.strip().lower()

        if entrada in ['quit', 'pass']:
            return entrada, None

        try:
            partes = entrada.split(',')
            if len(partes) != 3:
                return None, "Error: Use formato origen,destino,dado"

            origen_str, destino_str, dado_str = [p.strip() for p in partes]
            dado = int(dado_str)

            # Procesar casos especiales
            if origen_str == 'barra':
                return ('barra', int(destino_str) - 1, dado), None
            if destino_str == 'off':
                return (int(origen_str) - 1, 'off', dado), None
            
            # Caso normal
            return (int(origen_str) - 1, int(destino_str) - 1, dado), None

        except ValueError:
            return None, "Error: Ingrese números válidos"

    def ejecutar_movimiento_completo(self, origen, destino, dado):
        """Ejecuta un movimiento completo y devuelve el resultado."""
        try:
            if origen == 'barra':
                exito, mensaje = self.ejecutar_movimiento_barra(destino, dado)
            elif destino == 'off':
                exito, mensaje = self.ejecutar_bearing_off(origen, dado)
            else:
                self.mover(origen, destino, dado)
                return True, "Movimiento realizado exitosamente"

            return exito, f"{'OK' if exito else 'ERROR'} {mensaje}"

        except (MovimientoInvalidoError, DadoNoDisponibleError,
                PosicionVaciaError, PosicionBloqueadaError,
                MovimientoColorError) as e:
            return False, f"ERROR: {e}"

    def verificar_fin_juego_completo(self):
        """Verifica si el juego ha terminado y muestra el mensaje correspondiente."""
        if not self.verificar_victoria():
            return False

        ganador = self.get_turno()
        print(f"\n¡JUEGO TERMINADO!\n¡Ganó el jugador {ganador.get_color().upper()}!")
        return True

    def obtener_entrada_usuario(self):
        """Obtiene la entrada del usuario con las opciones disponibles."""
        try:
            # Mostrar opciones e ingresar una sola vez (tests pueden mockear input/print)
            print("\nOpciones:")
            for opcion in self.obtener_opciones_movimiento():
                print(f"  {opcion}")
            return input("\n> ")
        except (EOFError, KeyboardInterrupt, StopIteration):
            return 'quit'

    def turno_completo(self):
        """Ejecuta un turno completo del jugador actual."""
        self.mostrar_estado_juego()

        # Limpiar dados anteriores y tirar nuevos dados
        self.__dice__ = Dice()  # Resetear dados al inicio del turno
        self.tirar_dados()
        print(self.mostrar_dados_disponibles())

        if not self.quedan_movimientos():
            print("No hay movimientos disponibles. Pasando turno...")
            return True

        movimientos_realizados = False
        intentos_invalidos = 0  # Solo contar intentos inválidos
        max_intentos_invalidos = 10  # Límite para entradas inválidas

        while self.quedan_movimientos():
            entrada = self.obtener_entrada_usuario()
            movimiento, error = self.procesar_entrada_usuario(entrada)

            if movimiento == 'quit':
                return 'quit'
            if movimiento == 'pass':
                print("Pasando turno...")
                # Limpiar todos los dados al pasar turno
                if hasattr(self.__dice__, '__valores__'):
                    dados_antes = self.__dice__.__valores__.copy()
                    self.__dice__.__valores__.clear()
                    print(f"Dados limpiados: {dados_antes} -> []")
                # Verificar victoria antes de terminar el turno
                if self.verificar_fin_juego_completo():
                    return 'fin'
                # Asegurarse de que no quedan movimientos
                print("Turno completado con 'pass'")
                return True  # Terminar turno inmediatamente
            if error:
                print(error)
                intentos_invalidos += 1
                if intentos_invalidos >= max_intentos_invalidos:
                    print(f"ERROR: Demasiados intentos inválidos "
                          f"({max_intentos_invalidos}). Pasando turno...")
                    return True
                continue
            if movimiento is None:
                intentos_invalidos += 1
                if intentos_invalidos >= max_intentos_invalidos:
                    print(f"ERROR: Demasiados intentos inválidos "
                          f"({max_intentos_invalidos}). Pasando turno...")
                    return True
                continue

            origen, destino, dado = movimiento
            exito, mensaje = self.ejecutar_movimiento_completo(origen, destino, dado)
            print(mensaje)

            if exito:
                movimientos_realizados = True
                if self.verificar_fin_juego_completo():
                    return 'fin'

            if movimientos_realizados:
                print(self.mostrar_dados_disponibles())

        # Verificar victoria al final del turno
        if self.verificar_fin_juego_completo():
            return 'fin'

        return True

    def validar_entrada_movimiento(self, entrada):
        """Valida que la entrada del usuario sea correcta para un movimiento."""
        if not entrada or not isinstance(entrada, str):
            return False, "Entrada inválida"

        entrada = entrada.strip().lower()

        if entrada in ["salir", "exit", "quit", "help", "ayuda"]:
            return True, "comando_especial"

        if "-" not in entrada:
            return False, "Formato incorrecto. Use: origen-destino (ej: 5-11)"

        partes = entrada.split("-")
        if len(partes) != 2:
            return False, "Formato incorrecto. Use: origen-destino"

        origen, destino = partes[0].strip(), partes[1].strip()

        # Validar origen
        if origen == "barra":
            origen_num = "barra"
        else:
            try:
                origen_num = int(origen)
                if not 0 <= origen_num <= 24:
                    return False, "Posición origen debe estar entre 0-24 o 'barra'"
            except ValueError:
                return False, "Posición origen debe ser un número o 'barra'"

        # Validar destino
        if destino in ["afuera", "out"]:
            destino_num = "afuera"
        else:
            try:
                destino_num = int(destino)
                if not 0 <= destino_num <= 24:
                    return False, "Posición destino debe estar entre 0-24 o 'afuera'"
            except ValueError:
                return False, "Posición destino debe ser un número o 'afuera'"

        return True, (origen_num, destino_num)

    def validar_movimiento_legal(self, origen, destino, dados_disponibles):
        """Valida que un movimiento sea legal según las reglas del backgammon."""
        try:
            # Calcular distancia del movimiento
            if origen == "barra":
                color = self.get_turno().get_color()
                if destino == "afuera":
                    distancia = 0
                else:
                    distancia = destino if color == "blanca" else 25 - destino
            elif destino == "afuera":
                if not self.todas_fichas_en_home():
                    return False, ("No puede sacar fichas hasta que todas "
                                   "las fichas estén en home")
                color = self.get_turno().get_color()
                distancia = 25 - origen if color == "blanca" else origen
            else:
                distancia = abs(destino - origen)

            if distancia not in dados_disponibles:
                return False, f"No tiene un dado de {distancia} disponible"

            # Validar que hay ficha en posición origen
            if origen == "barra":
                if self.__board__.fichas_en_barra(self.get_turno().get_color()) == 0:
                    return False, "No tiene fichas en la barra"
            else:
                tablero = self.get_tablero()
                fichas_en_origen = tablero[origen - 1] if origen > 0 else []
                color_jugador = self.get_turno().get_color()
                if not any(f.obtener_color() == color_jugador for f in fichas_en_origen):
                    return False, f"No tiene ninguna ficha en la posición {origen}"

            # Validar que el destino esté disponible
            if destino != "afuera" and destino > 0:
                tablero = self.get_tablero()
                fichas_en_destino = tablero[destino - 1]
                if fichas_en_destino:
                    color_destino = fichas_en_destino[0].obtener_color()
                    if color_destino != self.get_turno().get_color() and len(fichas_en_destino) > 1:
                        return False, f"La posición {destino} está bloqueada por el oponente"

            return True, "Movimiento válido"

        except (ValueError, TypeError, AttributeError) as e:
            return False, f"Error al validar movimiento: {str(e)}"

    def mostrar_ayuda_movimientos(self):
        """Muestra ayuda sobre cómo realizar movimientos."""
        print("\n=== AYUDA DE MOVIMIENTOS ===")
        print("Formato: origen-destino")
        print("Ejemplos:")
        print("  5-11    : Mover ficha de posición 5 a posición 11")
        print("  barra-3 : Mover ficha de la barra a posición 3")
        print("  20-afuera : Sacar ficha de posición 20")
        print("\nComandos especiales:")
        print("  salir   : Terminar el turno")
        print("  help    : Mostrar esta ayuda")
        print("  ayuda   : Mostrar esta ayuda")
        print("============================\n")

    def procesar_entrada_usuario_validada(self, entrada, dados_disponibles):
        """Procesa la entrada del usuario con validación completa."""
        valido, resultado = self.validar_entrada_movimiento(entrada)
        if not valido:
            print(f"Error: {resultado}")
            return None

        if resultado == "comando_especial":
            if entrada.strip().lower() in ["help", "ayuda"]:
                self.mostrar_ayuda_movimientos()
            return "comando_especial"

        origen, destino = resultado
        valido, mensaje = self.validar_movimiento_legal(origen, destino, dados_disponibles)
        if not valido:
            print(f"Movimiento ilegal: {mensaje}")
            return None

        # Calcular el dado necesario
        color_blanca = self.get_turno().get_color() == "blanca"
        if origen == "barra":
            dado_necesario = destino if color_blanca else 25 - destino
        elif destino == "afuera":
            dado_necesario = 25 - origen if color_blanca else origen
        else:
            dado_necesario = abs(destino - origen)

        return (origen, destino, dado_necesario)

# alias en español para compatibilidad
BackgammonGame = Game
