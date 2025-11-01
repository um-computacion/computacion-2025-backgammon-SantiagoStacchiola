import pygame
from pygame_ui.board_renderer import BoardView
from pygame_ui.events import UIState, EventHandler


pygame.init()


def main():
    width, height = 900, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Backgammon (Pygame)")

    clock = pygame.time.Clock()
    board_view = BoardView(width, height)

    # Estado y manejador de eventos
    state = UIState()
    handler = EventHandler(board_view, state)

    # Cursor parpadeante para el menú
    cursor_timer = 0
    cursor_on = True

    running = True
    while running:
        for event in pygame.event.get():
            handler.handle(event)
        if state.should_quit:
            break

        # Salvaguarda: auto-pass si no hay movimientos con dados ya tirados
        handler.auto_pass_if_stuck()

        # --- Dibujo ---
        if state.mode == "menu":
            cursor_timer = (cursor_timer + 1) % 30
            if cursor_timer == 0:
                cursor_on = not cursor_on
            board_view.draw_menu(
                screen,
                state.nombre_blancas,
                state.nombre_negras,
                state.activo,
                cursor_on,
            )
        else:
            board_view.draw_board(screen)
            board_view.draw_highlights(screen, state.destinos_posibles)
            board_view.draw_checkers(screen, state.game)
            board_view.draw_names(screen, state.nombre_blancas, state.nombre_negras)
            board_view.draw_message_bar(screen, state.message)
            board_view.draw_dados(screen, state.dados_actuales)
            if state.game_over and state.winner_text:
                board_view.draw_win_overlay(screen, state.winner_text)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
