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

    def mostrar_dados(self):
        """Muestra los dados disponibles."""
        dice = self.game.__dice__
        if hasattr(dice, '__valores__') and dice.__valores__:
            valores = dice.__valores__
            print(f"Dados disponibles: {valores}")
        else:
            print("No hay dados disponibles")
    
    def mostrar_turno(self):
        """Muestra de quién es el turno."""
        jugador = self.game.get_turno()
        print(f"\n>>> Turno del jugador: {jugador.get_color().upper()} <<<")
    
    def pedir_movimiento(self):
        """Pide al usuario que ingrese un movimiento."""
        jugador = self.game.get_turno()
        fichas_en_barra = self.game.__board__.fichas_en_barra(jugador.get_color())
        
        print("\nOpciones:")
        if fichas_en_barra > 0:
            print("  ⚠️  Tienes fichas en la barra. Debes reingresarlas primero.")
            print("  - Reingresar desde barra: barra,destino,dado (ej: barra,3,3)")
        else:
            print("  - Movimiento normal: origen,destino,dado (ej: 1,7,6)")
            print("  - Bearing off: origen,off,dado (ej: 19,off,3)")
        print("  - Pasar turno: 'pass'")
        print("  - Salir: 'quit'")
        
        entrada = input("\n> ").strip().lower()
        
        if entrada == 'quit':
            return 'quit'
        elif entrada == 'pass':
            return 'pass'
        
        try:
            partes = entrada.split(',')
            if len(partes) != 3:
                print("Error: Use formato origen,destino,dado")
                return None
            
            origen_str = partes[0].strip()
            destino_str = partes[1].strip()
            dado = int(partes[2].strip())
            
            # Manejo especial para barra y bearing off
            if origen_str == 'barra':
                return ('barra', int(destino_str) - 1, dado)
            elif destino_str == 'off':
                return (int(origen_str) - 1, 'off', dado)
            else:
                origen = int(origen_str)
                destino = int(destino_str)
                # Convertir a índices (el usuario usa 1-24, el sistema 0-23)
                return (origen - 1, destino - 1, dado)
            
        except ValueError:
            print("Error: Ingrese números válidos")
            return None
    
    def ejecutar_movimiento(self, origen, destino, dado):
        """Ejecuta un movimiento en el juego."""
        try:
            jugador = self.game.get_turno()
            
            # Manejo de reingresar desde barra
            if origen == 'barra':
                if self.game.__board__.fichas_en_barra(jugador.get_color()) == 0:
                    print("✗ Error: No tienes fichas en la barra")
                    return False
                
                # Verificar que el destino no esté bloqueado
                tablero = self.game.get_tablero()
                fichas_destino = tablero[destino]
                if (fichas_destino and 
                    fichas_destino[0].obtener_color() != jugador.get_color() and 
                    len(fichas_destino) > 1):
                    print(f"✗ Error: Posición {destino + 1} está bloqueada")
                    return False
                
                # Usar dado y reingresar
                if not self.game.usar_valor_dado(dado):
                    print(f"✗ Error: El dado {dado} no está disponible")
                    return False
                
                self.game.__board__.reingresar_desde_barra(jugador.get_color(), destino)
                print("✓ Ficha reingresada desde la barra")
                return True
            
            # Manejo de bearing off
            elif destino == 'off':
                # Verificar que todas las fichas estén en home board
                if not self._todas_fichas_en_home(jugador):
                    print("✗ Error: Todas las fichas deben estar en el home board para bearing off")
                    return False
                
                # Usar dado y sacar ficha
                if not self.game.usar_valor_dado(dado):
                    print(f"✗ Error: El dado {dado} no está disponible")
                    return False
                
                ficha_sacada = self.game.__board__.sacar_ficha(origen)
                if ficha_sacada:
                    jugador.sacar_del_tablero(ficha_sacada)
                    print("✓ Ficha sacada del tablero (bearing off)")
                    return True
                else:
                    print(f"✗ Error: No hay fichas en posición {origen + 1}")
                    return False
            
            # Movimiento normal
            else:
                self.game.mover(origen, destino, dado)
                print("✓ Movimiento realizado exitosamente")
                return True
                
        except (MovimientoInvalidoError, DadoNoDisponibleError, 
                PosicionVaciaError, PosicionBloqueadaError, 
                MovimientoColorError) as e:
            print(f"✗ Error: {e}")
            return False
    
    def _todas_fichas_en_home(self, jugador):
        """Verifica si todas las fichas del jugador están en su home board."""
        tablero = self.game.get_tablero()
        color = jugador.get_color()
        
        # Home board para blancas: posiciones 19-24 (índices 18-23)
        # Home board para negras: posiciones 1-6 (índices 0-5)
        if color == "blanca":
            home_range = range(18, 24)
            fuera_home_range = range(0, 18)
        else:
            home_range = range(0, 6)
            fuera_home_range = range(6, 24)
        
        # Verificar que no haya fichas fuera del home board
        for i in fuera_home_range:
            if tablero[i]:
                for ficha in tablero[i]:
                    if ficha.obtener_color() == color:
                        return False
        
        # Verificar que no haya fichas en la barra
        if self.game.__board__.fichas_en_barra(color) > 0:
            return False
            
        return True
    
    def verificar_fin_juego(self):
        """Verifica si el juego ha terminado."""
        if self.game.verificar_victoria():
            ganador = self.game.get_turno()
            print(f"\n🎉 ¡JUEGO TERMINADO! 🎉")
            print(f"¡Ganó el jugador {ganador.get_color().upper()}!")
            return True
        return False
    
    def jugar(self):
        """Bucle principal del juego."""
        print("🎲 ¡Bienvenido al Backgammon! 🎲")
        print("Jugador 1: fichas BLANCAS")
        print("Jugador 2: fichas NEGRAS")
        print("\nPresiona Enter para comenzar...")
        input()
        
        # Crear jugadores
        player1 = Player("blanca")
        player2 = Player("negra") 
        
        # Inicializar juego
        self.game = Game(player1, player2)
        
        while True:
            # Mostrar estado del juego
            self.mostrar_tablero()
            self.mostrar_turno()
            
            # Lanzar dados
            self.game.tirar_dados()
            self.mostrar_dados()
            
            # Verificar si hay movimientos disponibles
            if not self.game.quedan_movimientos():
                print("No hay movimientos disponibles. Pasando turno...")
                self.game.cambiar_turno()
                continue
            
            # Jugador hace movimientos
            movimientos_realizados = False
            while self.game.quedan_movimientos():
                movimiento = self.pedir_movimiento()
                
                if movimiento == 'quit':
                    print("¡Gracias por jugar!")
                    return
                elif movimiento == 'pass':
                    print("Pasando turno...")
                    break
                elif movimiento is None:
                    continue
                
                origen, destino, dado = movimiento
                
                if self.ejecutar_movimiento(origen, destino, dado):
                    movimientos_realizados = True
                    
                    # Verificar si el juego terminó
                    if self.verificar_fin_juego():
                        return
                
                # Mostrar tablero actualizado después de un movimiento exitoso
                if movimientos_realizados:
                    self.mostrar_dados()  # Mostrar dados restantes
            
            # Cambiar turno
            self.game.cambiar_turno()
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
