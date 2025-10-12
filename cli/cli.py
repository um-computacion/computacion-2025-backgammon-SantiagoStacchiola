"""CLI simple para el juego de Backgammon."""

from core.game import Game
from core.player import Player


class BackgammonCLI:
    """CLI ultra simple para jugar Backgammon."""

    def __init__(self):
        """Inicializa el CLI del Backgammon."""
        self.__game__ = None

    def mostrar_bienvenida(self):
        """Muestra el mensaje de bienvenida del juego."""
        print("🎲 ¡Bienvenido al Backgammon! 🎲")
        print("Jugador 1: fichas BLANCAS")
        print("Jugador 2: fichas NEGRAS")
        print("\nPresiona Enter para comenzar...")
        input()

    def jugar(self):
        """Función principal del juego."""
        self.mostrar_bienvenida()

        # Crear jugadores e inicializar juego
        player1 = Player("blanca")
        player2 = Player("negra")
        self.__game__ = Game(player1, player2)

        while True:
            # Ejecutar turno completo
            resultado = self.__game__.turno_completo()

            if resultado == 'quit':
                print("¡Gracias por jugar!")
                return
            if resultado == 'fin':
                return

            # Cambiar turno
            self.__game__.cambiar_turno()
            print("\n" + "~"*60)
            print("Cambiando turno...")
            print("~"*60)


def main():
    """Función principal para ejecutar el CLI."""
    try:
        cli = BackgammonCLI()
        cli.jugar()
    except KeyboardInterrupt:
        print("\n\n¡Gracias por jugar!")
    except (ValueError, TypeError, AttributeError) as e:
        print(f"\n¡Ups! Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
