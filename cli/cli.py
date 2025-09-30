"""CLI simple para el juego de Backgammon."""

from core.game import Game
from core.player import Player
from core.excepcions import (MovimientoInvalidoError, DadoNoDisponibleError,
                           PosicionVaciaError, PosicionBloqueadaError,
                           MovimientoColorError)


class BackgammonCLI:
    """CLI simple para jugar Backgammon."""
    
    def __init__(self):
        self.game = None

    def mostrar_tablero(self):
        """Muestra una representación simple del tablero."""
        print("\n" + "="*60)
        print("TABLERO DE BACKGAMMON")
        print("="*60)
        
        contenedor = self.game.get_tablero()
        
        # Mostrar posiciones 13-24 (parte superior)
        print("Posiciones 13-24:")
        for i in range(13, 24):
            fichas = contenedor[i]
            if fichas:
                color = fichas[0].obtener_color()
                count = len(fichas)
                print(f"  {i+1:2d}: {count} fichas {color}")
        
        print("\n" + "-"*60)
        
        # Mostrar barras
        barra_blancas = self.game.__board__.fichas_en_barra("blanca")
        barra_negras = self.game.__board__.fichas_en_barra("negra")
        print(f"BARRA - Blancas: {barra_blancas} | Negras: {barra_negras}")
        
        print("-"*60 + "\n")
        
        # Mostrar posiciones 1-12 (parte inferior)
        print("Posiciones 1-12:")
        for i in range(0, 12):
            fichas = contenedor[i]
            if fichas:
                color = fichas[0].obtener_color()
                count = len(fichas)
                print(f"  {i+1:2d}: {count} fichas {color}")
        
        print("="*60)