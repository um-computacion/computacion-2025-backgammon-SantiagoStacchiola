import pygame
from core.game import Game


class UIState:
	"""Estado de la UI y del flujo del juego para la capa gráfica.

	Mantiene datos de interacción (selecciones, mensajes, dados visibles, etc.)
	separados de la lógica de render y del bucle principal.
	"""

	def __init__(self):
		# Menú
		self.mode = "menu"  # "menu" | "game"
		self.nombre_blancas = ""
		self.nombre_negras = ""
		self.activo = "blancas"  # campo activo en el menú

		# Juego
		self.game: Game | None = None
		self.game_over = False
		self.winner_text: str | None = None

		# Interacción de turno
		self.selected_point = None  # int | 'barra' | None
		self.destinos_posibles = []  # lista de int o 'off'
		self.message = "Presione ESPACIO para tirar los dados."
		self.dados_actuales: list[int] = []
		self.puede_tirar = True

		# Control del main loop
		self.should_quit = False


class EventHandler:
	"""Maneja eventos de Pygame y actualiza el UIState.

	- Detecta clics y teclas (detección de eventos de interacción).
	- Invoca métodos del `Game` para ejecutar jugadas.
	- Calcula destinos posibles y cambios de turno.
	"""

	def __init__(self, board_view, state: UIState):
		self.board_view = board_view
		self.state = state

	# --------------------- Utilidades de reglas/estado ---------------------
	def _hay_movimientos_posibles(self) -> bool:
		state = self.state
		game = state.game
		dados = state.dados_actuales
		if not game or not dados:
			return False
		color = game.get_turno().get_color()
		tablero = game.get_tablero()

		# Si hay fichas en barra, solo reingreso
		if game.fichas_en_barra(color) > 0:
			for d in set(dados):
				destino = (d - 1) if color == 'blanca' else (24 - d)
				if 0 <= destino <= 23:
					cont = tablero[destino]
					if not (cont and cont[0].obtener_color() != color and len(cont) > 1):
						return True
			return False

		# Movimiento normal sobre el tablero
		for i, fichas in enumerate(tablero):
			if not fichas:
				continue
			if fichas[0].obtener_color() != color:
				continue
			for d in set(dados):
				destino = i + d if color == 'blanca' else i - d
				if 0 <= destino <= 23:
					cont = tablero[destino]
					if not (cont and cont[0].obtener_color() != color and len(cont) > 1):
						return True

		# Borne-off si todas en home
		if game.todas_fichas_en_home() and dados:
			if color == 'blanca':
				for i in range(18, 24):
					if tablero[i] and tablero[i][0].obtener_color() == 'blanca':
						needed = 24 - i
						if any(d >= needed for d in dados):
							return True
			else:
				for i in range(0, 6):
					if tablero[i] and tablero[i][0].obtener_color() == 'negra':
						needed = i + 1
						if any(d >= needed for d in dados):
							return True
		return False

	def _reset_seleccion(self):
		self.state.selected_point = None
		self.state.destinos_posibles = []

	# -------------------------- Manejo de eventos --------------------------
	def handle(self, event: pygame.event.Event):
		s = self.state

		if event.type == pygame.QUIT:
			s.should_quit = True
			return

		if event.type == pygame.KEYDOWN:
			# ESC siempre vuelve/sale
			if event.key == pygame.K_ESCAPE:
				s.should_quit = True
				return

			# Si hay fin de juego, permitir salir con ENTER o ESC
			if s.game_over:
				if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
					s.should_quit = True
				return

			# Menú: TAB cambia foco, ENTER confirma, BACKSPACE borra
			if s.mode == "menu":
				if event.key == pygame.K_TAB:
					s.activo = "negras" if s.activo == "blancas" else "blancas"
				elif event.key == pygame.K_RETURN:
					if s.nombre_blancas.strip() and s.nombre_negras.strip():
						s.mode = "game"
						s.game = Game()
						self._reset_seleccion()
						s.dados_actuales = []
						s.puede_tirar = True
						s.message = (
							f"Turno de {s.game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
						)
				elif event.key == pygame.K_BACKSPACE:
					if s.activo == "blancas" and s.nombre_blancas:
						s.nombre_blancas = s.nombre_blancas[:-1]
					elif s.activo == "negras" and s.nombre_negras:
						s.nombre_negras = s.nombre_negras[:-1]
				else:
					ch = event.unicode
					if ch and ch.isprintable() and len(ch) == 1:
						if s.activo == "blancas" and len(s.nombre_blancas) < 16:
							s.nombre_blancas += ch
						elif s.activo == "negras" and len(s.nombre_negras) < 16:
							s.nombre_negras += ch
				return

			# Juego: tirar dados con ESPACIO
			if event.key == pygame.K_SPACE and s.mode == "game":
				if not s.puede_tirar:
					s.message = "Ya tiraste los dados este turno."
				else:
					s.dados_actuales = s.game.tirar_dados()
					s.puede_tirar = False
					s.message = f"{s.game.mostrar_turno_actual()} - Dados: {s.dados_actuales}"
					if not self._hay_movimientos_posibles():
						s.message = f"{s.game.mostrar_turno_actual()} - Sin movimientos posibles. Cambio de turno."
						s.game.cambiar_turno()
						self._reset_seleccion()
						s.dados_actuales = []
						s.puede_tirar = True
						s.message = f"Turno de {s.game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
				return

		# Clics de mouse
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if s.game_over:
				return
			if s.mode == "menu":
				mx, my = event.pos
				# hitboxes del menú (coinciden con draw_menu)
				caja_w, caja_h = 360, 42
				cx = self.board_view.width // 2 - caja_w // 2
				y_blancas = self.board_view.height // 2 - 60
				y_negras = self.board_view.height // 2 + 10
				if pygame.Rect(cx, y_blancas, caja_w, caja_h).collidepoint(mx, my):
					s.activo = "blancas"
				elif pygame.Rect(cx, y_negras, caja_w, caja_h).collidepoint(mx, my):
					s.activo = "negras"
				return

			if s.mode == "game":
				punto = self.board_view.get_point_from_mouse(event.pos)
				if punto is None:
					return

				# Primer clic: elegir origen
				if s.selected_point is None:
					color = s.game.get_turno().get_color()
					if s.game.fichas_en_barra(color) > 0 and punto != 'barra':
						s.message = "Debes reingresar desde la BARRA antes de mover otras fichas."
						self._reset_seleccion()
						return
					if punto == 'off':
						s.message = "Para sacar, primero selecciona una ficha y luego la bandeja derecha."
						self._reset_seleccion()
						return

					s.selected_point = punto
					s.message = "Seleccionado origen: BARRA" if punto == 'barra' else f"Seleccionado origen: {punto+1}"

					# Calcular destinos posibles
					s.destinos_posibles = []
					if s.dados_actuales:
						tablero = s.game.get_tablero()
						for d in set(s.dados_actuales):
							if punto == 'barra':
								destino = (d - 1) if color == 'blanca' else (24 - d)
							else:
								destino = punto + d if color == 'blanca' else punto - d
							if 0 <= destino <= 23:
								cont = tablero[destino]
								if cont and cont[0].obtener_color() != color and len(cont) > 1:
									continue
								s.destinos_posibles.append(destino)

						# opção de borne-off
						if isinstance(punto, int) and s.game.todas_fichas_en_home() and s.dados_actuales:
							needed = (24 - punto) if color == 'blanca' else (punto + 1)
							if any(d >= needed for d in s.dados_actuales):
								s.destinos_posibles.append('off')
					return

				# Segundo clic: elegir destino y ejecutar
				destino = punto
				if not s.dados_actuales:
					s.message = "Tire los dados (ESPACIO) antes de mover."
					self._reset_seleccion()
					return

				color = s.game.get_turno().get_color()
				if s.game.fichas_en_barra(color) > 0 and s.selected_point != 'barra':
					s.message = "Debes reingresar desde la BARRA antes de mover otras fichas."
					self._reset_seleccion()
					return

				valor_dado = None
				if s.selected_point == 'barra' and isinstance(destino, int):
					if color == 'blanca' and 0 <= destino <= 5:
						valor_dado = destino + 1
					elif color == 'negra' and 18 <= destino <= 23:
						valor_dado = 24 - destino
					else:
						s.message = "Para reingresar, el destino debe estar en tu cuadrante de entrada (1-6)."
				elif isinstance(s.selected_point, int) and destino == 'off':
					if s.game.todas_fichas_en_home():
						needed = (24 - s.selected_point) if color == 'blanca' else (s.selected_point + 1)
						elegibles = sorted(d for d in set(s.dados_actuales) if d >= needed)
						if elegibles:
							valor_dado = elegibles[0]
						else:
							s.message = f"No tienes un dado suficiente (>= {needed}) para sacar esa ficha."
					else:
						s.message = "Para sacar fichas, todas tus fichas deben estar en tu tablero local."
				elif isinstance(s.selected_point, int) and isinstance(destino, int):
					if color == 'blanca':
						if destino <= s.selected_point:
							s.message = "Dirección inválida para BLANCAS."
						else:
							valor_dado = destino - s.selected_point
					else:
						if destino >= s.selected_point:
							s.message = "Dirección inválida para NEGRAS."
						else:
							valor_dado = s.selected_point - destino

				if valor_dado is None:
					self._reset_seleccion()
					return

				if valor_dado not in s.dados_actuales:
					s.message = f"No tienes un dado de {valor_dado} disponible."
					self._reset_seleccion()
					return

				# Ejecutar
				origen_param = s.selected_point
				destino_param = destino
				if destino == 'off':
					ok, msg = s.game.ejecutar_bearing_off(origen_param, valor_dado)
				else:
					ok, msg = s.game.ejecutar_movimiento_completo(origen_param, destino_param, valor_dado)

				if ok:
					s.dados_actuales = s.game.get_dados_disponibles()
					if s.selected_point == 'barra':
						s.message = f"Reingreso desde BARRA a {destino+1} (dado {valor_dado}) OK"
					elif destino == 'off':
						s.message = f"Sacaste ficha de {origen_param+1} (dado {valor_dado}) OK"
					else:
						s.message = f"Movimiento {origen_param+1}->{destino_param+1} ({valor_dado}) OK"

					if s.game.verificar_victoria():
						ganador_color = s.game.get_turno().get_color()
						ganador_nombre = s.nombre_blancas if ganador_color == 'blanca' else s.nombre_negras
						s.winner_text = f"Ganó {ganador_nombre} ({ganador_color.upper()})"
						s.game_over = True
					else:
						if not s.dados_actuales:
							s.game.cambiar_turno()
							self._reset_seleccion()
							s.puede_tirar = True
							s.message = f"Turno de {s.game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
						else:
							if not self._hay_movimientos_posibles():
								s.message = f"{s.game.mostrar_turno_actual()} - Sin movimientos posibles. Cambio de turno."
								s.game.cambiar_turno()
								self._reset_seleccion()
								s.dados_actuales = []
								s.puede_tirar = True
								s.message = f"Turno de {s.game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
				else:
					s.message = msg

				self._reset_seleccion()

	# -------------------------- Post-procesamiento -------------------------
	def auto_pass_if_stuck(self):
		"""Si ya se tiraron los dados y no existe ninguna jugada posible,
		pasa de turno automáticamente (evita loops atascados)."""
		s = self.state
		if s.mode != "game" or s.game_over or s.puede_tirar or not s.dados_actuales:
			return
		if not self._hay_movimientos_posibles():
			color = s.game.get_turno().get_color()
			if s.game.fichas_en_barra(color) > 0:
				aviso = "No puedes reingresar desde la barra: posiciones bloqueadas. Pierdes el turno."
			else:
				aviso = "Sin movimientos posibles. Pierdes el turno."
			s.message = f"{s.game.mostrar_turno_actual()} - {aviso}"
			s.game.cambiar_turno()
			self._reset_seleccion()
			s.dados_actuales = []
			s.puede_tirar = True
			s.message = f"Turno de {s.game.get_turno().get_color()}. Presione ESPACIO para tirar los dados."
