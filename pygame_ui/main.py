import pygame
from core.game import Game
from pygame_ui.board_renderer import BoardView

pygame.init()

def main():
    width, height = 900, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Backgammon (Pygame)")

    clock = pygame.time.Clock()
    board_view = BoardView(width, height)

    # --- Estado de menú inicial ---
    mode = "menu"
    font = pygame.font.SysFont("arial", 28)
    small = pygame.font.SysFont("arial", 20)
    nombre_blancas = ""
    nombre_negras = ""
    activo = "blancas"  # campo activo por defecto
    cursor_timer = 0
    cursor_on = True

    game = None
    game_over = False
    winner_text = None
    # game_over_time se eliminó: no se usa para autocierre

    running = True
    selected_point = None
    destinos_posibles = []
    message = "Presione ESPACIO para tirar los dados."

    # Lista de dados visibles para el usuario durante el turno
    dados_actuales = []
    puede_tirar = True  # sólo una tirada por turno

    def hay_movimientos_posibles():
        """Determina si hay al menos un movimiento legal con los dados actuales."""
        nonlocal game, dados_actuales
        if not dados_actuales:
            return False
        color = game.get_turno().get_color()
        tablero = game.get_tablero()

        # Si hay fichas en barra, sólo se puede reingresar
        if game.fichas_en_barra(color) > 0:
            for d in set(dados_actuales):
                destino = (d - 1) if color == 'blanca' else (24 - d)
                if 0 <= destino <= 23:
                    cont = tablero[destino]
                    if not (cont and cont[0].obtener_color() != color and len(cont) > 1):
                        return True
            return False

        # Revisar todas las fichas propias en el tablero
        for i, fichas in enumerate(tablero):
            if not fichas:
                continue
            if fichas[0].obtener_color() != color:
                continue
            for d in set(dados_actuales):
                if color == 'blanca':
                    destino = i + d
                else:
                    destino = i - d
                if 0 <= destino <= 23:
                    cont = tablero[destino]
                    if not (cont and cont[0].obtener_color() != color and len(cont) > 1):
                        return True
        # Bearing off: si todas en home, verificar si existe alguna ficha con un dado >= necesario
        if game.todas_fichas_en_home() and dados_actuales:
            if color == 'blanca':
                for i in range(18, 24):
                    if tablero[i] and tablero[i][0].obtener_color() == 'blanca':
                        needed = 24 - i
                        if any(d >= needed for d in dados_actuales):
                            return True
            else:
                for i in range(0, 6):
                    if tablero[i] and tablero[i][0].obtener_color() == 'negra':
                        needed = i + 1
                        if any(d >= needed for d in dados_actuales):
                            return True

        return False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Si el juego terminó, sólo permitir salir con ENTER o ESC
                if game_over:
                    if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        running = False
                    continue
                # --- Manejo de menú ---
                if mode == "menu":
                    if event.key == pygame.K_TAB:
                        activo = "negras" if activo == "blancas" else "blancas"
                    elif event.key == pygame.K_RETURN:
                        if nombre_blancas.strip() and nombre_negras.strip():
                            mode = "game"
                            game = Game()
                            # reset estado del juego al entrar
                            selected_point = None
                            destinos_posibles = []
                            dados_actuales = []
                            puede_tirar = True
                            message = f"Turno de {game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
                    elif event.key == pygame.K_BACKSPACE:
                        if activo == "blancas" and nombre_blancas:
                            nombre_blancas = nombre_blancas[:-1]
                        elif activo == "negras" and nombre_negras:
                            nombre_negras = nombre_negras[:-1]
                    else:
                        # Aceptar caracteres imprimibles simples
                        ch = event.unicode
                        if ch and ch.isprintable() and len(ch) == 1:
                            if activo == "blancas" and len(nombre_blancas) < 16:
                                nombre_blancas += ch
                            elif activo == "negras" and len(nombre_negras) < 16:
                                nombre_negras += ch
                    continue  # no procesar entradas de juego si estamos en menú

                # --- Manejo del juego ---
                elif event.key == pygame.K_SPACE:
                    if not puede_tirar:
                        message = "Ya tiraste los dados este turno."
                    else:
                        dados_actuales = game.tirar_dados()
                        puede_tirar = False
                        message = f"{game.mostrar_turno_actual()} - Dados: {dados_actuales}"
                        # Chequear si no hay movimientos y pasar turno automáticamente
                        if not hay_movimientos_posibles():
                            message = f"{game.mostrar_turno_actual()} - Sin movimientos posibles. Cambio de turno."
                            game.cambiar_turno()
                            selected_point = None
                            destinos_posibles = []
                            dados_actuales = []
                            puede_tirar = True
                            message = f"Turno de {game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
                # ENTER ya no cambia turno en juego (para evitar trampas). Se usa en menú/fin.
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over:
                    continue
                if mode == "menu":
                    # Toggle foco por clic en las cajas
                    mx, my = event.pos
                    # cajas: blancas y negras (coordenadas al dibujar)
                    # Usaremos rects consistentes con el dibujo (ver abajo)
                    # Calculamos aquí de forma local
                    caja_w, caja_h = 360, 42
                    cx = width // 2 - caja_w // 2
                    y_blancas = height // 2 - 60
                    y_negras = height // 2 + 10
                    if pygame.Rect(cx, y_blancas, caja_w, caja_h).collidepoint(mx, my):
                        activo = "blancas"
                    elif pygame.Rect(cx, y_negras, caja_w, caja_h).collidepoint(mx, my):
                        activo = "negras"
                    continue

                punto = board_view.get_point_from_mouse(event.pos)
                if punto is not None:
                    # Primer clic: elegir origen (punto o 'barra')
                    if selected_point is None:
                        # Si hay fichas en barra, sólo permitir seleccionar la barra
                        color = game.get_turno().get_color()
                        if game.fichas_en_barra(color) > 0 and punto != 'barra':
                            message = "Debes reingresar desde la BARRA antes de mover otras fichas."
                            selected_point = None
                            destinos_posibles = []
                        elif punto == 'off':
                            # No se puede elegir la bandeja como origen
                            message = "Para sacar, primero selecciona una ficha y luego la bandeja derecha."
                            selected_point = None
                            destinos_posibles = []
                        else:
                            selected_point = punto
                            if punto == 'barra':
                                message = "Seleccionado origen: BARRA"
                            else:
                                message = f"Seleccionado origen: {punto+1}"
                            # Calcular zonas de destino posibles
                            destinos_posibles = []
                            if dados_actuales:
                                # Posibles movimientos a puntos
                                for d in set(dados_actuales):
                                    if punto == 'barra':
                                        if color == 'blanca':
                                            destino = d - 1
                                        else:
                                            destino = 24 - d
                                    else:
                                        if color == 'blanca':
                                            destino = punto + d
                                        else:
                                            destino = punto - d

                                    if 0 <= destino <= 23:
                                        # Filtrar posiciones bloqueadas (2+ del rival)
                                        cont = game.get_tablero()[destino]
                                        if cont and cont[0].obtener_color() != color and len(cont) > 1:
                                            continue
                                        destinos_posibles.append(destino)

                                # Posible movimiento a 'off' (sacar ficha) si hay un dado >= needed
                                if isinstance(punto, int) and game.todas_fichas_en_home() and dados_actuales:
                                    needed = (24 - punto) if color == 'blanca' else (punto + 1)
                                    if any(d >= needed for d in dados_actuales):
                                        destinos_posibles.append('off')
                    else:
                        destino = punto
                        if not dados_actuales:
                            message = "Tire los dados (ESPACIO) antes de mover."
                        else:
                            color = game.get_turno().get_color()

                            # Si hay fichas en barra, sólo se puede reingresar
                            if game.fichas_en_barra(color) > 0 and selected_point != 'barra':
                                message = "Debes reingresar desde la BARRA antes de mover otras fichas."
                                selected_point = None
                                destinos_posibles = []
                                continue

                            # Determinar valor de dado y validar dirección (incluye 'off')
                            valor_dado = None
                            if selected_point == 'barra' and isinstance(destino, int):
                                # Reingreso desde barra según color/dirección
                                if color == 'blanca' and 0 <= destino <= 5:
                                    valor_dado = destino + 1
                                elif color == 'negra' and 18 <= destino <= 23:
                                    valor_dado = 24 - destino
                                else:
                                    message = "Para reingresar, el destino debe estar en tu cuadrante de entrada (1-6)."
                            elif isinstance(selected_point, int) and destino == 'off':
                                # Bearing off: si todas en home, usar un dado >= needed (el menor posible)
                                if game.todas_fichas_en_home():
                                    if dados_actuales:
                                        needed = (24 - selected_point) if color == 'blanca' else (selected_point + 1)
                                        elegibles = sorted(d for d in set(dados_actuales) if d >= needed)
                                        if elegibles:
                                            valor_dado = elegibles[0]
                                        else:
                                            message = f"No tienes un dado suficiente (>= {needed}) para sacar esa ficha."
                                    else:
                                        message = "No tienes dados disponibles."
                                else:
                                    message = "Para sacar fichas, todas tus fichas deben estar en tu tablero local."
                            elif isinstance(selected_point, int) and isinstance(destino, int):
                                # Movimiento normal con restricción de sentido
                                if color == 'blanca':
                                    if destino <= selected_point:
                                        message = "Dirección inválida para BLANCAS."
                                    else:
                                        valor_dado = destino - selected_point
                                else:  # negras
                                    if destino >= selected_point:
                                        message = "Dirección inválida para NEGRAS."
                                    else:
                                        valor_dado = selected_point - destino

                            if valor_dado is not None:
                                if valor_dado not in dados_actuales:
                                    message = f"No tienes un dado de {valor_dado} disponible."
                                else:
                                    # Ejecutar movimiento (incluye 'off')
                                    origen_param = selected_point
                                    destino_param = destino
                                    if destino == 'off':
                                        ok, msg = game.ejecutar_bearing_off(origen_param, valor_dado)
                                    else:
                                        ok, msg = game.ejecutar_movimiento_completo(origen_param, destino_param, valor_dado)
                                    if ok:
                                        # Sincronizar visual de dados con el estado real del juego
                                        dados_actuales = game.get_dados_disponibles()
                                        if selected_point == 'barra':
                                            message = f"Reingreso desde BARRA a {destino+1} (dado {valor_dado}) OK"
                                        elif destino == 'off':
                                            message = f"Sacaste ficha de {selected_point+1} (dado {valor_dado}) OK"
                                        else:
                                            message = f"Movimiento {selected_point+1}->{destino+1} ({valor_dado}) OK"

                                        # ¿Victoria?
                                        if game.verificar_victoria():
                                            ganador_color = game.get_turno().get_color()
                                            ganador_nombre = nombre_blancas if ganador_color == 'blanca' else nombre_negras
                                            winner_text = f"Ganó {ganador_nombre} ({ganador_color.upper()})"
                                            game_over = True
                                            # No cambiar turno si ya terminó
                                        else:
                                            # Si no quedan dados, pasar turno automáticamente
                                            if not dados_actuales:
                                                game.cambiar_turno()
                                                selected_point = None
                                                destinos_posibles = []
                                                puede_tirar = True
                                                message = f"Turno de {game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
                                            else:
                                                # Si con los dados restantes no hay jugadas (incluye reingreso desde barra y sacar), pasar turno
                                                if not hay_movimientos_posibles():
                                                    message = f"{game.mostrar_turno_actual()} - Sin movimientos posibles. Cambio de turno."
                                                    game.cambiar_turno()
                                                    selected_point = None
                                                    destinos_posibles = []
                                                    dados_actuales = []
                                                    puede_tirar = True
                                                    message = f"Turno de {game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
                                    else:
                                        message = msg

                        # Reset selección y highlights
                        selected_point = None
                        destinos_posibles = []

        # Salvaguarda: si ya se tiraron los dados y no hay NINGUNA jugada posible,
        # pasar turno automáticamente para evitar quedar atascado (especialmente con fichas en barra bloqueadas).
        if mode == "game" and not game_over and not puede_tirar and dados_actuales:
            if not hay_movimientos_posibles():
                color = game.get_turno().get_color()
                if game.fichas_en_barra(color) > 0:
                    aviso = "No puedes reingresar desde la barra: posiciones bloqueadas. Pierdes el turno."
                else:
                    aviso = "Sin movimientos posibles. Pierdes el turno."
                message = f"{game.mostrar_turno_actual()} - {aviso}"
                game.cambiar_turno()
                selected_point = None
                destinos_posibles = []
                dados_actuales = []
                puede_tirar = True
                message = f"Turno de {game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."

        # --- Dibujo ---
        if mode == "menu":
            screen.fill((235, 225, 195))
            titulo = font.render("Backgammon", True, (0, 0, 0))
            subt = small.render("Ingrese nombres y presione ENTER", True, (0, 0, 0))
            screen.blit(titulo, (width // 2 - titulo.get_width() // 2, 80))
            screen.blit(subt, (width // 2 - subt.get_width() // 2, 120))

            etiqueta1 = small.render("Jugador BLANCAS:", True, (0, 0, 0))
            etiqueta2 = small.render("Jugador NEGRAS:", True, (0, 0, 0))
            screen.blit(etiqueta1, (width // 2 - 180, height // 2 - 90))
            screen.blit(etiqueta2, (width // 2 - 180, height // 2 - 20))

            caja_w, caja_h = 360, 42
            cx = width // 2 - caja_w // 2
            y_blancas = height // 2 - 60
            y_negras = height // 2 + 10

            # Cursor parpadeante
            cursor_timer = (cursor_timer + 1) % 30
            if cursor_timer == 0:
                cursor_on = not cursor_on

            for idx, (texto, y, es_activo) in enumerate([
                (nombre_blancas, y_blancas, activo == "blancas"),
                (nombre_negras, y_negras, activo == "negras"),
            ]):
                rect = pygame.Rect(cx, y, caja_w, caja_h)
                pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=6)
                pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=6)
                mostrar = texto
                if es_activo and cursor_on:
                    mostrar += "|"
                texto_render = font.render(mostrar or " ", True, (0, 0, 0))
                screen.blit(texto_render, (rect.x + 10, rect.y + 6))

            hint = small.render("TAB cambia de campo | ESC para salir", True, (0, 0, 0))
            screen.blit(hint, (width // 2 - hint.get_width() // 2, height - 80))

        else:
            board_view.draw_board(screen)
            board_view.draw_highlights(screen, destinos_posibles)
            board_view.draw_checkers(screen, game)
            # Nombres de jugadores en tablero
            board_view.draw_names(screen, nombre_blancas, nombre_negras)
            board_view.draw_message_bar(screen, message)
            board_view.draw_dados(screen, dados_actuales)

            # Overlay de fin de juego
            if game_over and winner_text:
                overlay = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(overlay, (0, 0, 0, 160), overlay.get_rect())
                panel_w, panel_h = 520, 140
                panel = pygame.Rect(0, 0, panel_w, panel_h)
                panel.center = (width // 2, height // 2)
                pygame.draw.rect(overlay, (245, 235, 210, 255), panel, border_radius=12)
                pygame.draw.rect(overlay, (0, 0, 0), panel, 3, border_radius=12)
                big = pygame.font.SysFont("arial", 32, bold=True)
                txt = big.render(winner_text, True, (0, 0, 0))
                sub = small.render("Presione ENTER o ESC para salir", True, (0, 0, 0))
                overlay.blit(txt, (panel.centerx - txt.get_width() // 2, panel.y + 36))
                overlay.blit(sub, (panel.centerx - sub.get_width() // 2, panel.y + 86))
                screen.blit(overlay, (0, 0))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
