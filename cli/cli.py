"""CLI simple para el juego de Backgammon."""

from core.game import Game
from core.player import Player


class BackgammonCLI:
    """CLI ultra simple para jugar Backgammon."""
    
    def jugar(self):
        """Función principal del juego."""
        print("🎲 ¡Bienvenido al Backgammon! 🎲")
        print("Jugador 1: fichas BLANCAS")
        print("Jugador 2: fichas NEGRAS")
        print("\nPresiona Enter para comenzar...")
        input()
        
        # Crear jugadores e inicializar juego
        player1 = Player("blanca")
        player2 = Player("negra") 
        game = Game(player1, player2)
        
        while True:
            # Ejecutar turno completo
            resultado = game.turno_completo()
            
            if resultado == 'quit':
                print("¡Gracias por jugar!")
                return
            elif resultado == 'fin':
                return
            
            # Cambiar turno
            game.cambiar_turno()
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
    except Exception as e:
        print(f"\n¡Ups! Ocurrió un error: {e}")


if __name__ == "__main__":
    main()
