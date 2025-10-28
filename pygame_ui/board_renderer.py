import pygame

# --- Colores ---
BEIGE = (240, 220, 180)
BROWN_LIGHT = (210, 160, 100)
BROWN_DARK = (140, 90, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)

class BoardView:
    """Encargado de dibujar el tablero, fichas y zona de mensajes."""

    def __init__(self, width=900, height=600):
        self.width = width
        self.height = height
        self.margin = 40
        self.triangle_width = (self.width - 2*self.margin) / 12
        self.triangle_height = (self.height - 150) / 2
        self.font = pygame.font.SysFont("arial", 18)
        self.message_font = pygame.font.SysFont("arial", 22, bold=True)

    # ------------------------------------------------------------------
    def draw_board(self, screen):
        """Dibuja el fondo y los triángulos del tablero."""
        screen.fill(BEIGE)

        # Línea central
        pygame.draw.line(screen, BLACK,
                         (self.margin + 6*self.triangle_width, self.margin),
                         (self.margin + 6*self.triangle_width,
                          self.height - 110), 3)

        # Triángulos superiores
        for i in range(12):
            color = BROWN_DARK if i % 2 == 0 else BROWN_LIGHT
            x = self.margin + i*self.triangle_width
            pts = [(x, self.margin),
                   (x + self.triangle_width, self.margin),
                   (x + self.triangle_width/2, self.triangle_height)]
            pygame.draw.polygon(screen, color, pts)

        # Triángulos inferiores
        for i in range(12):
            color = BROWN_LIGHT if i % 2 == 0 else BROWN_DARK
            x = self.margin + i*self.triangle_width
            pts = [(x, self.height - 110),
                   (x + self.triangle_width, self.height - 110),
                   (x + self.triangle_width/2,
                    self.height - 110 - self.triangle_height)]
            pygame.draw.polygon(screen, color, pts)

        # Números de posiciones
        for i in range(12):
            num = self.font.render(str(12 - i), True, BLACK)
            screen.blit(num, (self.margin + i*self.triangle_width + 10,
                              self.margin + 5))
        for i in range(12):
            num = self.font.render(str(13 + i), True, BLACK)
            screen.blit(num, (self.margin + i*self.triangle_width + 10,
                              self.height - 30))

    # ------------------------------------------------------------------
    def draw_checkers(self, screen, game):
        """Dibuja las fichas según el estado del tablero."""
        board = game.get_tablero()

        # puntos 0-11 abajo, 12-23 arriba
        radius = self.triangle_width * 0.33
        max_visible = 5
        for i, fichas in enumerate(board):
            count = len(fichas)
            if count == 0:
                continue

            color = WHITE if fichas[0].obtener_color() == "blanca" else BLACK
            # coordenadas base
            if i < 12:  # parte inferior
                x = self.margin + (11 - i) * self.triangle_width + self.triangle_width/2
                y_base = self.height - 120
                dy = -radius*1.9
            else:        # parte superior
                x = self.margin + (i - 12) * self.triangle_width + self.triangle_width/2
                y_base = self.margin + radius*1.1
                dy = radius*1.9

            visibles = min(count, max_visible)
            for j in range(visibles):
                y = y_base + j*dy
                pygame.draw.circle(screen, color, (int(x), int(y)), int(radius))
                pygame.draw.circle(screen, GRAY, (int(x), int(y)), int(radius), 2)

            # Si hay más de 5, mostrar número
            if count > max_visible:
                y = y_base + (max_visible - 1)*dy
                text_color = BLACK if color == WHITE else WHITE
                label = self.font.render(str(count), True, text_color)
                rect = label.get_rect(center=(x, y))
                screen.blit(label, rect)

    # ------------------------------------------------------------------
    def draw_message_bar(self, screen, message):
        """Dibuja la barra de mensajes inferior."""
        bar_rect = pygame.Rect(0, self.height - 60, self.width, 60)
        pygame.draw.rect(screen, (220, 200, 160), bar_rect)
        pygame.draw.line(screen, BLACK, (0, self.height - 60),
                         (self.width, self.height - 60), 2)
        text = self.message_font.render(message, True, BLACK)
        rect = text.get_rect(center=(self.width//2, self.height - 30))
        screen.blit(text, rect)

    # ------------------------------------------------------------------
    def get_point_from_mouse(self, pos):
        """Traduce un clic en coordenadas a índice de punto (0–23)."""
        x, y = pos
        if y < self.margin or y > self.height - 110:
            return None

        # zona superior
        if y < self.triangle_height + self.margin:
            row = "top"
        elif y > self.height - 110 - self.triangle_height:
            row = "bottom"
        else:
            return None

        i = int((x - self.margin) / self.triangle_width)
        if i < 0 or i > 11:
            return None

        if row == "top":
            return 12 + i
        else:
            return 11 - i
