import pygame

# --- Colores ---
BEIGE = (240, 220, 180)
BROWN_LIGHT = (210, 160, 100)
BROWN_DARK = (140, 90, 40)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)


class BoardView:
    """Encargado de dibujar el tablero, fichas y zona de mensajes.

    Este renderer sólo dibuja; no modifica la lógica del juego. Se añadieron
    mejoras de layout: números inferiores visibles, barra central y bandeja
    derecha para borne-off.
    """

    def __init__(self, width=900, height=600):
        self.width = width
        self.height = height

        # Geometría general
        self.margin = 40
        self.message_bar_height = 60
        self.bottom_labels_band = 50
        self.top_labels_band = 26  # banda superior reservada para números
        self.off_tray_width = 70
        # La barra central será del mismo ancho que la bandeja derecha
        self.center_bar_width = self.off_tray_width

        # Tamaño de triángulos dejando espacio para bandeja y barra central
        self.triangle_width = (
            self.width - 2 * self.margin - self.off_tray_width - self.center_bar_width
        ) / 12
        self.triangle_height = (
            self.height - (
                self.message_bar_height + self.bottom_labels_band + self.top_labels_band + self.margin
            )
        ) / 2

        # Tipografías
        self.font = pygame.font.SysFont("arial", 18)
        self.message_font = pygame.font.SysFont("arial", 22, bold=True)

    # --- utilidades de geometría ---
    def _col_x(self, col: int) -> float:
        """X inicial de la columna 0..11 considerando la barra central."""
        base = self.margin + col * self.triangle_width
        if col >= 6:
            base += self.center_bar_width
        return base

    def _col_center(self, col: int) -> float:
        return self._col_x(col) + self.triangle_width / 2

    # ------------------------------------------------------------------
    def draw_board(self, screen):
        """Dibuja el fondo y los triángulos del tablero."""
        screen.fill(BEIGE)

        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
        tablero_height = tablero_bottom - tablero_top

        # Triángulos superiores (inician debajo de la banda de números)
        top_y = tablero_top + self.top_labels_band

        for i in range(12):
            color = BROWN_DARK if i % 2 == 0 else BROWN_LIGHT
            x = self._col_x(i)
            pts = [
                (x, top_y),
                (x + self.triangle_width, top_y),
                (x + self.triangle_width / 2, top_y + self.triangle_height),
            ]
            pygame.draw.polygon(screen, color, pts)

        # Triángulos inferiores
        for i in range(12):
            color = BROWN_LIGHT if i % 2 == 0 else BROWN_DARK
            x = self._col_x(i)
            base_y = tablero_bottom
            pts = [
                (x, base_y),
                (x + self.triangle_width, base_y),
                (x + self.triangle_width / 2, base_y - self.triangle_height),
            ]
            pygame.draw.polygon(screen, color, pts)

        # Barra central (bar) — mismo ancho que bandeja derecha, dibujada DESPUÉS de los triángulos
        bar_left = self.margin + 6 * self.triangle_width
        # Color igual a la bandeja derecha
        pygame.draw.rect(
            screen,
            (205, 186, 150),
            pygame.Rect(bar_left, tablero_top, self.center_bar_width, tablero_height),
            border_radius=2,
        )

        # Bandeja de borne-off a la derecha
        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        tray_rect = pygame.Rect(tray_left, tablero_top, self.off_tray_width, tablero_height)
        pygame.draw.rect(screen, (205, 186, 150), tray_rect)
        pygame.draw.rect(screen, BLACK, tray_rect, 2)

        # Números de posiciones
        for i in range(12):
            num = self.font.render(str(12 - i), True, BLACK)
            screen.blit(num, (self._col_x(i) + 10, tablero_top + 5))

        # Números inferiores por encima de la barra de mensajes
        bottom_num_y = (
            self.height - self.message_bar_height - self.bottom_labels_band + 18
        )
        for i in range(12):
            num = self.font.render(str(13 + i), True, BLACK)
            screen.blit(num, (self._col_x(i) + 10, bottom_num_y))

    # ------------------------------------------------------------------
    def draw_menu(self, screen, nombre_blancas: str, nombre_negras: str, activo: str, cursor_on: bool):
        """Dibuja la pantalla de menú inicial para ingresar nombres.

        activo: "blancas" o "negras" indica cuál input tiene foco visual.
        cursor_on: si True, muestra un cursor parpadeante al final del texto activo.
        """
        screen.fill((235, 225, 195))

        titulo = self.message_font.render("Backgammon", True, BLACK)
        small = pygame.font.SysFont("arial", 20)
        subt = small.render("Ingrese nombres y presione ENTER", True, BLACK)
        screen.blit(titulo, (self.width // 2 - titulo.get_width() // 2, 80))
        screen.blit(subt, (self.width // 2 - subt.get_width() // 2, 120))

        etiqueta1 = small.render("Jugador BLANCAS:", True, BLACK)
        etiqueta2 = small.render("Jugador NEGRAS:", True, BLACK)
        screen.blit(etiqueta1, (self.width // 2 - 180, self.height // 2 - 90))
        screen.blit(etiqueta2, (self.width // 2 - 180, self.height // 2 - 20))

        caja_w, caja_h = 360, 42
        cx = self.width // 2 - caja_w // 2
        y_blancas = self.height // 2 - 60
        y_negras = self.height // 2 + 10

        for texto, y, es_activo in [
            (nombre_blancas, y_blancas, activo == "blancas"),
            (nombre_negras, y_negras, activo == "negras"),
        ]:
            rect = pygame.Rect(cx, y, caja_w, caja_h)
            pygame.draw.rect(screen, WHITE, rect, border_radius=6)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
            mostrar = texto
            if es_activo and cursor_on:
                mostrar += "|"
            texto_render = self.message_font.render(mostrar or " ", True, BLACK)
            screen.blit(texto_render, (rect.x + 10, rect.y + 6))

        hint = small.render("TAB cambia de campo | ESC para salir", True, BLACK)
        screen.blit(hint, (self.width // 2 - hint.get_width() // 2, self.height - 80))

    # ------------------------------------------------------------------
    def draw_checkers(self, screen, game):
        """Dibuja las fichas en puntos, barra central y bandeja de borne-off."""
        board = game.get_tablero()

        # puntos 0-11 abajo, 12-23 arriba
        radius = int(min(self.triangle_width * 0.33, (self.off_tray_width * 0.45)))
        max_visible = 5
        for i, fichas in enumerate(board):
            count = len(fichas)
            if count == 0:
                continue

            color = WHITE if fichas[0].obtener_color() == "blanca" else BLACK
            # coordenadas base
            if i < 12:  # parte inferior
                col = 11 - i
                x = self._col_center(col)
                y_base = (
                    self.height - self.message_bar_height - self.bottom_labels_band - 10
                )
                dy = -radius * 1.9
            else:  # parte superior
                col = i - 12
                x = self._col_center(col)
                y_base = self.margin + self.top_labels_band + radius * 1.1
                dy = radius * 1.9

            visibles = min(count, max_visible)
            for j in range(visibles):
                y = y_base + j * dy
                pygame.draw.circle(screen, color, (int(x), int(y)), int(radius))
                pygame.draw.circle(screen, GRAY, (int(x), int(y)), int(radius), 2)

            # Si hay más de 5, mostrar número
            if count > max_visible:
                y = y_base + (max_visible - 1) * dy
                text_color = BLACK if color == WHITE else WHITE
                label = self.font.render(str(count), True, text_color)
                rect = label.get_rect(center=(x, y))
                screen.blit(label, rect)

        # --- BARRA central ---
        try:
            blancas_en_barra = game.fichas_en_barra("blanca")
            negras_en_barra = game.fichas_en_barra("negra")
        except AttributeError:
            blancas_en_barra = 0
            negras_en_barra = 0

        bar_left = self.margin + 6 * self.triangle_width
        cx = bar_left + self.center_bar_width / 2
        # Top (blancas) hacia abajo
        y_top_base = self.margin + self.top_labels_band + radius * 1.1
        for j in range(min(max_visible, blancas_en_barra)):
            y = y_top_base + j * (radius * 1.9)
            pygame.draw.circle(screen, WHITE, (int(cx), int(y)), radius)
            pygame.draw.circle(screen, GRAY, (int(cx), int(y)), radius, 2)
        if blancas_en_barra > max_visible:
            y = y_top_base + (max_visible - 1) * (radius * 1.9)
            label = self.font.render(str(blancas_en_barra), True, BLACK)
            rect = label.get_rect(center=(cx, y))
            screen.blit(label, rect)

        # Bottom (negras) hacia arriba
        y_bottom_base = (
            self.height - self.message_bar_height - self.bottom_labels_band - 10
        )
        for j in range(min(max_visible, negras_en_barra)):
            y = y_bottom_base - j * (radius * 1.9)
            pygame.draw.circle(screen, BLACK, (int(cx), int(y)), radius)
            pygame.draw.circle(screen, GRAY, (int(cx), int(y)), radius, 2)
        if negras_en_barra > max_visible:
            y = y_bottom_base - (max_visible - 1) * (radius * 1.9)
            label = self.font.render(str(negras_en_barra), True, WHITE)
            rect = label.get_rect(center=(cx, y))
            screen.blit(label, rect)

        # --- Bandeja de BORNE-OFF derecha ---
        try:
            fuera_blancas = game.fichas_fuera("blanca")
            fuera_negras = game.fichas_fuera("negra")
        except AttributeError:
            fuera_blancas = fuera_negras = 0

        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        tray_center_x = tray_left + self.off_tray_width / 2

        # Negras arriba (hacia abajo)
        y_base_top = self.margin + radius * 1.1
        for j in range(min(max_visible, fuera_negras)):
            y = y_base_top + j * (radius * 1.9)
            pygame.draw.circle(screen, BLACK, (int(tray_center_x), int(y)), radius)
            pygame.draw.circle(screen, GRAY, (int(tray_center_x), int(y)), radius, 2)
        if fuera_negras > max_visible:
            y = y_base_top + (max_visible - 1) * (radius * 1.9)
            label = self.font.render(str(fuera_negras), True, WHITE)
            rect = label.get_rect(center=(tray_center_x, y))
            screen.blit(label, rect)

        # Blancas abajo (hacia arriba)
        y_base_bottom = (
            self.height - self.message_bar_height - self.bottom_labels_band - 10
        )
        for j in range(min(max_visible, fuera_blancas)):
            y = y_base_bottom - j * (radius * 1.9)
            pygame.draw.circle(screen, WHITE, (int(tray_center_x), int(y)), radius)
            pygame.draw.circle(screen, GRAY, (int(tray_center_x), int(y)), radius, 2)
        if fuera_blancas > max_visible:
            y = y_base_bottom - (max_visible - 1) * (radius * 1.9)
            label = self.font.render(str(fuera_blancas), True, BLACK)
            rect = label.get_rect(center=(tray_center_x, y))
            screen.blit(label, rect)

    # ------------------------------------------------------------------
    def draw_message_bar(self, screen, message):
        """Dibuja la barra de mensajes inferior."""
        bar_rect = pygame.Rect(
            0, self.height - self.message_bar_height, self.width, self.message_bar_height
        )
        pygame.draw.rect(screen, (220, 200, 160), bar_rect)
        pygame.draw.line(
            screen,
            BLACK,
            (0, self.height - self.message_bar_height),
            (self.width, self.height - self.message_bar_height),
            2,
        )
        text = self.message_font.render(message, True, BLACK)
        rect = text.get_rect(
            center=(self.width // 2, self.height - self.message_bar_height // 2)
        )
        screen.blit(text, rect)

    # ------------------------------------------------------------------
    def get_point_from_mouse(self, pos):
        """Traduce un clic en coordenadas a índice de punto (0–23)."""
        x, y = pos
        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band

        if y < tablero_top or y > tablero_bottom:
            return None

        # Detectar clic en la barra central para permitir reingreso desde "barra"
        bar_left = self.margin + 6 * self.triangle_width
        bar_right = bar_left + self.center_bar_width
        if bar_left <= x <= bar_right:
            return 'barra'

        # Detectar clic en bandeja de borne-off (tray) -> destino especial 'off'
        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        if x >= tray_left:
            return 'off'

        # zona superior/inferior con tolerancia para pilas altas
        overflow = int(min(self.triangle_height * 0.2, 24))
        top_limit = tablero_top + self.top_labels_band + self.triangle_height + overflow
        bottom_limit = tablero_bottom - self.triangle_height - overflow
        if y < top_limit:
            row = "top"
        elif y > bottom_limit:
            row = "bottom"
        else:
            return None

        # Calcular columna (0..11) con gap de la barra central
        if x < bar_left:
            col = int((x - self.margin) / self.triangle_width)
        elif x > bar_right:
            # lado derecho: compensar el ancho de la barra central, sin sumar 6
            col = int((x - (self.margin + self.center_bar_width)) / self.triangle_width)
        else:
            return 'barra'

        if col < 0 or col > 11:
            return None

        if row == "top":
            return 12 + col
        else:
            return 11 - col

    # ------------------------------------------------------------------
    def draw_dados(self, screen, valores):
        """Dibuja un pequeño panel de dados en la bandeja derecha.

        Se muestran hasta 4 valores (soporta dobles). No modifica estado de juego.
        """
        if not valores:
            return

        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
        tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
        tray_center_x = tray_left + self.off_tray_width / 2

        # Dimensiones de dado
        size = 26
        gap = 8
        start_y = tablero_top + 10

        def dibujar_dado(cx, cy, valor):
            rect = pygame.Rect(0, 0, size, size)
            rect.center = (cx, cy)
            pygame.draw.rect(screen, WHITE, rect, border_radius=4)
            pygame.draw.rect(screen, BLACK, rect, 2, border_radius=4)

            # Puntos (pips)
            r = 3
            ox, oy = rect.left + size * 0.25, rect.top + size * 0.25
            mx, my = rect.centerx, rect.centery
            px, py = rect.right - size * 0.25, rect.bottom - size * 0.25
            posiciones = {
                1: [(mx, my)],
                2: [(ox, oy), (px, py)],
                3: [(ox, oy), (mx, my), (px, py)],
                4: [(ox, oy), (px, oy), (ox, py), (px, py)],
                5: [(ox, oy), (px, oy), (mx, my), (ox, py), (px, py)],
                6: [(ox, oy), (px, oy), (ox, my), (px, my), (ox, py), (px, py)],
            }
            for (pxx, pyy) in posiciones.get(int(valor), []):
                pygame.draw.circle(screen, BLACK, (int(pxx), int(pyy)), r)

        # Distribuir los dados en columnas dentro de la bandeja
        cols = 2
        for idx, val in enumerate(valores[:4]):
            col = idx % cols
            row = idx // cols
            cx = tray_center_x + (col - 0.5) * (size + gap)
            cy = start_y + row * (size + gap)
            dibujar_dado(cx, cy, val)

    # ------------------------------------------------------------------
    def draw_highlights(self, screen, indices):
        """Dibuja indicadores VERDES en forma de rectángulo translúcido que
        cubren el área completa de la posición (triángulo) para que se vean más.

        indices: lista de índices de punto (0-23) válidos para mover.
        """
        if not indices:
            return

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        verde = (50, 200, 80, 90)   # Destinos a puntos
        azul  = (80, 140, 255, 90)  # Destino especial 'off' (bandeja)

        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
        top_y = tablero_top + self.top_labels_band

        for i in indices:
            # Destino especial: bandeja de borne-off ("off")
            if i == 'off':
                tray_left = self.margin + 12 * self.triangle_width + self.center_bar_width
                rect = pygame.Rect(
                    int(tray_left) + 3,
                    int(tablero_top) + 3,
                    int(self.off_tray_width) - 6,
                    int(tablero_bottom - tablero_top) - 6,
                )
                pygame.draw.rect(overlay, azul, rect)
                continue

            if not isinstance(i, int) or i < 0 or i > 23:
                continue

            if i < 12:
                # fila inferior: el triángulo ocupa la parte baja
                col = 11 - i
                x = self._col_x(col)
                base_y = tablero_bottom
                rect = pygame.Rect(
                    int(x) + 1,
                    int(base_y - self.triangle_height) + 1,
                    int(self.triangle_width) - 2,
                    int(self.triangle_height) - 2,
                )
            else:
                # fila superior: el triángulo ocupa desde top_y hacia abajo
                col = i - 12
                x = self._col_x(col)
                rect = pygame.Rect(
                    int(x) + 1,
                    int(top_y) + 1,
                    int(self.triangle_width) - 2,
                    int(self.triangle_height) - 2,
                )

            pygame.draw.rect(overlay, verde, rect)

        screen.blit(overlay, (0, 0))

    # ------------------------------------------------------------------
    def draw_names(self, screen, nombre_blancas: str, nombre_negras: str):
        """Dibuja los nombres de los jugadores por FUERA del tablero para no tapar nada.

        - Negras: parte superior izquierda, en la banda de margen superior.
        - Blancas: parte superior derecha, en la banda de margen superior.
        """
        top_y = 8  # dentro del margen superior (fuera del tablero)

        if nombre_negras:
            txt = self.message_font.render(f"Negras: {nombre_negras}", True, BLACK)
            screen.blit(txt, (self.margin, top_y))

        if nombre_blancas:
            txt = self.message_font.render(f"Blancas: {nombre_blancas}", True, BLACK)
            x = self.width - self.margin - txt.get_width()
            screen.blit(txt, (x, top_y))

    # ------------------------------------------------------------------
    def draw_win_overlay(self, screen, winner_text: str):
        """Dibuja el panel final con el ganador."""
        if not winner_text:
            return
        tablero_top = self.margin
        tablero_bottom = self.height - self.message_bar_height - self.bottom_labels_band
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (0, 0, 0, 160), overlay.get_rect())
        panel_w, panel_h = 520, 140
        panel = pygame.Rect(0, 0, panel_w, panel_h)
        panel.center = (self.width // 2, (tablero_top + tablero_bottom) // 2)
        pygame.draw.rect(overlay, (245, 235, 210, 255), panel, border_radius=12)
        pygame.draw.rect(overlay, BLACK, panel, 3, border_radius=12)
        big = pygame.font.SysFont("arial", 32, bold=True)
        txt = big.render(winner_text, True, BLACK)
        small = pygame.font.SysFont("arial", 20)
        sub = small.render("Presione ENTER o ESC para salir", True, BLACK)
        overlay.blit(txt, (panel.centerx - txt.get_width() // 2, panel.y + 36))
        overlay.blit(sub, (panel.centerx - sub.get_width() // 2, panel.y + 86))
        screen.blit(overlay, (0, 0))
