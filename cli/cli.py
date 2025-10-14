"""CLI simple para el juego de Backgammon."""

from core.game import Game
from core.player import Player


class BackgammonCLI:
    """CLI ultra simple para jugar Backgammon."""

    def __init__(self):
        """Inicializa el CLI."""
        self.__game__ = None
        self.__test_mode__ = False  # Para controlar comportamiento en tests

    def set_test_mode(self, enabled=True):
        """Activa o desactiva el modo test para evitar inputs reales."""
        self.__test_mode__ = enabled

    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida."""
        print("¡Bienvenido al Backgammon!")
        print("Presiona Enter para comenzar...")
        try:
            # Protección para tests - solo usar test_mode
            if self.__test_mode__ or hasattr(input, '_mock_name'):
                # Hay un mock activo o estamos en modo test, usar el mock
                input()
            else:
                # Ejecución normal
                input()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta luego!")
            return False
        return True

    def obtener_entrada_usuario(self):
        """Obtiene entrada del usuario para el CLI."""
        # Verificar si aún quedan dados antes de pedir entrada
        if not self.__game__.quedan_movimientos():
            print("No quedan movimientos, terminando turno...")
            return 'pass'

        print("\nOpciones:")
        for opcion in self.__game__.obtener_opciones_movimiento():
            print(f"  {opcion}")

        while True:
            try:
                entrada = input("\n> ").strip()
                if entrada:
                    return entrada
                print("Por favor ingresa un comando válido.")
            except (EOFError, KeyboardInterrupt):
                print("\n¡Saliendo del juego!")
                return 'quit'

    def jugar(self):
        """Función principal del juego."""
        if not self.mostrar_bienvenida():
            return

        # Crear jugadores e inicializar juego
        player1 = Player("blanca")
        player2 = Player("negra")
        self.__game__ = Game(player1, player2)

        # Establecer el método de entrada para el juego
        self.__game__.obtener_entrada_usuario = self.obtener_entrada_usuario

        turnos_jugados = 0

        while True:
            turnos_jugados += 1
            print(f"\n{'='*20} TURNO {turnos_jugados} {'='*20}")

            try:
                # Ejecutar turno completo
                print(f"Iniciando turno {turnos_jugados}...")
                resultado = self.__game__.turno_completo()
                print(f"Resultado del turno: {resultado}")

                if resultado == 'quit':
                    print("\n¡Gracias por jugar Backgammon!")
                    return
                if resultado == 'fin':
                    print("\n¡Partida terminada!")
                    return

                # Cambiar turno
                print(f"\nFinalizando turno {turnos_jugados}...")
                self.__game__.cambiar_turno()
                print("\n" + "~"*60)
                print("Cambiando turno...")
                print("~"*60)

                # Pausa para que el usuario vea el cambio de turno
                try:
                    # Protección para tests - solo hacer input si NO estamos en modo test
                    if not self.__test_mode__:
                        input("Presiona Enter para continuar al siguiente turno...")
                except (EOFError, KeyboardInterrupt):
                    print("\n\n¡Gracias por jugar!")
                    return

            except (EOFError, KeyboardInterrupt):
                print("\n\n¡Gracias por jugar!")
                return
            except Exception as e:
                print(f"\nERROR inesperado: {e}")
                print("Continuando con el juego...")
                continue

        # Este punto nunca debería alcanzarse
        print(f"\nBucle terminado inesperadamente después de {turnos_jugados} turnos.")


def main():
    """Función principal del CLI."""
    try:
        cli = BackgammonCLI()
        cli.jugar()
    except KeyboardInterrupt:
        print("\n\n¡Gracias por jugar!")
    except Exception as e:
        print(f"\nERROR: {e}")
        print("El juego terminó inesperadamente.")


if __name__ == "__main__":
    main()
