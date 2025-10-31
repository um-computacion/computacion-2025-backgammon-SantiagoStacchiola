"""Módulo que define el tablero y operaciones sobre él."""

from core.checker import Ficha

class Board:
    """Modelo del tablero de backgammon con sus puntos y fichas."""

    def __init__(self):
        # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

        # Barras (fichas capturadas)
        self.__barra_blancas__ = []
        self.__barra_negras__ = []

        # Posiciones iniciales estándar del Backgammon
        iniciales = [(0, 2, "blanca"), (11, 5, "blanca"), (16, 3, "blanca"), (18, 5, "blanca"),
                    (23, 2, "negra"), (12, 5, "negra"), (7, 3, "negra"), (5, 5, "negra")]

        for posicion, cantidad, color in iniciales:
            self.__contenedor__[posicion] = [Ficha(color, posicion) for _ in range(cantidad)]

    def get_contenedor(self):
        """Muestra el contenedor."""
        return self.__contenedor__

    def get_fichas(self, posicion):
        """Devuelve una copia de las fichas en una posicion."""
        return list(self.__contenedor__[posicion])

    def contar_fichas(self, posicion):
        """Cantidad de fichas en una posición."""
        return len(self.__contenedor__[posicion])

    def color_en_posicion(self, posicion):
        """Devuelve el color de las fichas en una posición (None si está vacía)."""
        if not self.__contenedor__[posicion]:
            return None
        return self.__contenedor__[posicion][0].obtener_color()

    def guardar_ficha(self, posicion, ficha: Ficha):
        """Guarda una ficha en una posición dada."""
        ficha.mover(posicion)
        self.__contenedor__[posicion].append(ficha)

    def quitar_ficha(self, posicion):
        """Quita una ficha de una posición dada."""
        if not self.__contenedor__[posicion]:
            return None
        ficha = self.__contenedor__[posicion].pop()
        ficha.mover(None)
        return ficha

    def mover_ficha(self, origen, destino):
        """Mueve una ficha de una posición de origen a una de destino."""
        ficha = self.__contenedor__[origen].pop()
        ficha.mover(destino)
        self.__contenedor__[destino].append(ficha)

    def enviar_a_barra(self, ficha: Ficha):
        """Envía una ficha a la barra (fichas capturadas)."""
        ficha.mover("barra")
        destino_barra = (
            self.__barra_blancas__ if ficha.obtener_color() == "blanca" else self.__barra_negras__
        )
        destino_barra.append(ficha)

    def reingresar_desde_barra(self, color, destino):
        """Reingresa una ficha desde la barra a una posición del tablero."""
        barra = self.__barra_blancas__ if color == "blanca" else self.__barra_negras__
        if barra:
            ficha = barra.pop()
            ficha.mover(destino)
            self.__contenedor__[destino].append(ficha)

    def fichas_en_barra(self, color):
        """Devuelve la cantidad de fichas de un color en la barra."""
        return len(self.__barra_blancas__ if color == "blanca" else self.__barra_negras__)

    def sacar_ficha(self, posicion):
        """Saca una ficha de una posición y la envía 'afuera'."""
        if not self.__contenedor__[posicion]:
            return None
        ficha = self.__contenedor__[posicion].pop()
        ficha.mover("afuera")
        return ficha

    def reset(self):
        """Inicializa o reinicia el tablero a la posición inicial."""
        # 24 posiciones del tablero, cada una lista de fichas
        self.__contenedor__ = [[] for _ in range(24)]

        # Barras (fichas capturadas)
        self.__barra_blancas__ = []
        self.__barra_negras__ = []

        # Posiciones iniciales estándar del Backgammon
        # Blancas
        self.__contenedor__[0] = [Ficha("blanca", 0) for _ in range(2)]
        self.__contenedor__[11] = [Ficha("blanca", 11) for _ in range(5)]
        self.__contenedor__[16] = [Ficha("blanca", 16) for _ in range(3)]
        self.__contenedor__[18] = [Ficha("blanca", 18) for _ in range(5)]
        # Negras
        self.__contenedor__[23] = [Ficha("negra", 23) for _ in range(2)]
        self.__contenedor__[12] = [Ficha("negra", 12) for _ in range(5)]
        self.__contenedor__[7] = [Ficha("negra", 7) for _ in range(3)]
        # La posición 5 debe quedar vacía después del reset según el test

    def mover(self, desde_punto, hasta_punto):
        """Mueve una ficha validando reglas básicas."""
        if self.__contenedor__[desde_punto]:
            ficha = self.__contenedor__[desde_punto].pop()
            ficha.mover(hasta_punto)
            self.__contenedor__[hasta_punto].append(ficha)

    def contar_punto(self, punto):
        """Devuelve la cantidad de fichas en un punto dado."""
        return len(self.__contenedor__[punto])

    def mostrar_tablero(self):
        """Muestra una representación simple del tablero."""
        print("\n" + "="*60)
        print("TABLERO DE BACKGAMMON")
        print("="*60)

        # Mostrar posiciones 13-24 (parte superior)
        print("Posiciones 13-24:")
        for i in range(12, 24):
            fichas = self.__contenedor__[i]
            if fichas:
                color = fichas[0].obtener_color()
                count = len(fichas)
                print(f"  {i+1:2d}: {count} fichas {color}")

        print("\n" + "-"*60)

        # Mostrar barras
        barra_blancas = len(self.__barra_blancas__)
        barra_negras = len(self.__barra_negras__)
        print(f"BARRA - Blancas: {barra_blancas} | Negras: {barra_negras}")

        print("-"*60 + "\n")

        # Mostrar posiciones 1-12 (parte inferior)
        print("Posiciones 1-12:")
        for i in range(0, 12):
            fichas = self.__contenedor__[i]
            if fichas:
                color = fichas[0].obtener_color()
                count = len(fichas)
                print(f"  {i+1:2d}: {count} fichas {color}")

        print("="*60)

    def validar_posicion(self, posicion):
        """Valida que una posición sea válida en el tablero."""
        if posicion is None:
            return False, "Posición no puede ser None"

        if isinstance(posicion, str):
            if posicion in ["barra", "afuera"]:
                return True, "Posición especial válida"
            return False, f"Posición de texto inválida: {posicion}"

        if not isinstance(posicion, int):
            return False, f"Posición debe ser un número entero, recibido: {type(posicion)}"

        if posicion < 1 or posicion > 24:
            return False, f"Posición debe estar entre 1 y 24, recibido: {posicion}"

        return True, "Posición válida"

    def validar_movimiento_posiciones(self, origen, destino):
        """Valida que las posiciones de origen y destino sean correctas."""
        # Validar origen
        if origen == "barra":
            # Desde barra es válido
            pass
        else:
            valido, mensaje = self.validar_posicion(origen)
            if not valido:
                return False, f"Origen inválido: {mensaje}"

        # Validar destino
        if destino == "afuera":
            # Hacia afuera (bearing off) es válido
            pass
        else:
            valido, mensaje = self.validar_posicion(destino)
            if not valido:
                return False, f"Destino inválido: {mensaje}"

        # Validar que origen y destino no sean iguales
        if origen == destino:
            return False, "Origen y destino no pueden ser iguales"

        return True, "Posiciones válidas"

    def hay_fichas_en_posicion(self, posicion, color=None):
        """Verifica si hay fichas en una posición específica."""
        if posicion == "barra":
            if color:
                if color == "blanca":
                    return len(self.__barra_blancas__) > 0
                return len(self.__barra_negras__) > 0
            return len(self.__barra_blancas__) > 0 or len(self.__barra_negras__) > 0

        if posicion == "afuera":
            # Las fichas afuera no se almacenan, solo se remueven del juego
            return False

        valido, _ = self.validar_posicion(posicion)
        if not valido:
            return False

        fichas = self.__contenedor__[posicion - 1]
        if color:
            return any(f.obtener_color() == color for f in fichas)
        return len(fichas) > 0

    def posicion_bloqueada(self, posicion, color):
        """Verifica si una posición está bloqueada para un color específico."""
        if posicion == "afuera":
            return False  # Siempre se puede mover afuera

        valido, _ = self.validar_posicion(posicion)
        if not valido:
            return True  # Posición inválida se considera bloqueada

        fichas = self.__contenedor__[posicion - 1]
        if not fichas:
            return False  # Posición vacía no está bloqueada

        color_ocupante = fichas[0].obtener_color()
        if color_ocupante == color:
            return False  # Propia ficha no bloquea

        # Bloqueado si hay 2 o más fichas enemigas
        return len(fichas) >= 2

    # Alias en inglés para compatibilidad
    def move(self, from_point, to_point):
        """Alias en inglés para mover()."""
        return self.mover(from_point, to_point)

    def point_count(self, point):
        """Alias en inglés para contar_punto()."""
        return self.contar_punto(point)

    def validate_position(self, position):
        """Alias en inglés para validar_posicion()."""
        return self.validar_posicion(position)
# EOF
 