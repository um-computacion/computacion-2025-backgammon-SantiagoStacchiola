import pygame
from core.game import Game
from pygame_ui.board_renderer import BoardView

pygame.init()

def main():
    game = Game()
    width, height = 900, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Backgammon (Pygame)")

    clock = pygame.time.Clock()
    board_view = BoardView(width, height)

    running = True
    selected_point = None
    message = "Presione ESPACIO para tirar los dados."

    dados_actuales = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    dados_actuales = game.tirar_dados()
                    message = f"{game.mostrar_turno_actual()} - Dados: {dados_actuales}"
                elif event.key == pygame.K_RETURN:
                    game.cambiar_turno()
                    selected_point = None
                    message = f"Turno de {game.get_turno().get_color()}"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                point = board_view.get_point_from_mouse(event.pos)
                if point is not None:
                    if selected_point is None:
                        selected_point = point
                        message = f"Seleccionado origen: {point+1}"
                    else:
                        destino = point
                        if not dados_actuales:
                            message = "Tire los dados (ESPACIO) antes de mover."
                        else:
                            valor = abs(destino - selected_point)
                            ok, msg = game.ejecutar_movimiento_completo(selected_point, destino, valor)
                            if ok:
                                message = f"Movimiento {selected_point+1}->{destino+1} ({valor}) OK"
                            else:
                                message = msg
                        selected_point = None

        # --- Dibujo ---
        board_view.draw_board(screen)
        board_view.draw_checkers(screen, game)
        board_view.draw_message_bar(screen, message)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
