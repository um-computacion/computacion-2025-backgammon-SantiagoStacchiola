# JUSTIFICACION

Este documento detalla las decisiones de diseño y las estrategias de desarrollo tomadas en el proyecto de Backgammon. El objetivo es justificar la estructura, explicar las elecciones técnicas y mostrar cómo se garantiza calidad (tests, linting y CI), siguiendo el formato del repositorio de referencia y adaptado a este código.

## Resumen del diseño general

El proyecto se pensó con foco en la separación de responsabilidades:

- Capa de dominio (core): lógica del juego, independiente de cualquier interfaz.
- Capas de presentación: CLI (texto) y Pygame (gráfica), que consumen el core.

Esta modularidad permite evolucionar las interfaces sin tocar la lógica central, favorece el testing y habilita futuras extensiones (por ejemplo, una IA). El diseño es orientado a objetos, con clases que representan componentes del dominio y cumplen el Principio de Responsabilidad Única (SRP).

Estructura principal del repositorio:

- `core/`: `game.py`, `board.py`, `player.py`, `dice.py`, `checker.py`, `excepcions.py`
- `cli/`: `cli.py`
- `pygame_ui/`: `main.py`, `board_renderer.py`
- `tests/`: pruebas unitarias e integración

## Justificación de las clases elegidas

- `Juego` (`core/game.py`): Orquesta la partida. Coordina turnos, interacción entre tablero, jugadores y dados. Expone operaciones de alto nivel para que las capas de interfaz no conozcan detalles internos.
- `Tablero` (`core/board.py`): Modela los 24 puntos, la barra y el área de fichas afuera. Valida movimientos, reingreso desde la barra y condiciones de “borneoff” (sacar fichas).
- `Jugador` (`core/player.py`): Datos y estado de cada jugador (nombre, color, fichas restantes) y utilidades para verificar victoria.
- `Dados` (`core/dice.py`): Encapsula la tirada y el consumo de tiradas, incluyendo el caso de dobles.
- `Ficha` (`core/checker.py`): Representa una ficha del juego. Mantenerla separada permite extender comportamiento o estado específico si se requiere.
- Interfaz de texto `CLI` (`cli/cli.py`) y UI `Pygame` (`pygame_ui/*.py`): Capas de presentación que interactúan con `Juego` sin duplicar reglas. El CLI es intencionalmente delgado.

## Atributos y decisiones de diseño relevantes

Se usan atributos internos con convención `__nombre__` para reforzar encapsulamiento y cumplir la consigna. Decisiones puntuales:

- Encapsular el estado del tablero en `Tablero` para centralizar validaciones.
- Delegar en `Juego` el flujo de turnos y la consulta de ganador, evitando lógica en CLI.
- Mantener `Dados` aislado: la interfaz solo consulta y consume tiradas.
- CLI “fino”: imprime estado y recolecta entradas; no valida reglas complejas.
- Pygame: bucle principal con `clock` y `display.flip()` dentro del loop, evitando bloqueos y asegurando FPS estables.

## Excepciones y manejo de errores

Se definen excepciones específicas del dominio para evitar estados inconsistentes y comunicar causas claras a las interfaces:

- `MovimientoInvalidoError`
- `SacarFichaError`
- `JugadorInvalidoError`

Ubicación y uso:

- Declaradas en `core/excepcions.py`.
- Lanzadas desde `board.py`/`game.py` cuando una regla se viola.
- Capturadas en capas de interfaz (por ejemplo, CLI) para emitir mensajes entendibles.

## Estrategia de testing y cobertura

- Unit tests en `tests/` para core (tablero, juego, dados, jugador, ficha).
- Tests de integración para CLI usando `unittest.mock.patch` sobre `input`/`print`.
- Cobertura medida con `coverage` generando `coverage.xml` y reporte de texto.
- Casos cubiertos destacados:
	- Movimientos válidos/ inválidos y límites de rango.
	- Reingreso desde barra con/ sin fichas disponibles.
	- Reglas de borneoff: validar “todas en último cuadrante”.
	- Detección de ganador y finalización de juego.

## Referencias a SOLID

- S (Single Responsibility): cada clase tiene una responsabilidad clara.
- O (Open/Closed): nuevas interfaces (por ejemplo, IA o UI adicional) se suman sin modificar el core.
- L (Liskov): posibles subclases de `Jugador` podrían sustituirse sin romper a `Juego`.
- I (Interface Segregation): las capas de interfaz exponen solo lo necesario al usuario.
- D (Dependency Inversion): `Juego` (alto nivel) no depende de implementaciones concretas de la UI; las capas externas dependen del core.

## Relación con hitos y commits

Algunas consultas y cambios relevantes que guiaron el diseño (ver `prompts-*.md`):

- Separación de capas y primeros pasos del CLI: "primeros pasos cli" (2025-09-30).
- Excepciones y lint: "agregado y aplicado de exepciones" / "mejora pylint y excepcion" (2025-09-28).
- Simplificación fuerte del CLI y migración al core: "Simplificación mayor del CLI…" (2025-10-11).
- Cobertura de tests de `game` y `cli`: (2025-10-12 / 2025-10-13).
- Reglas de tablero (barra y borneoff): "mejora board y checker" (2025-10-13).
- Funcionamiento correcto del CLI: (2025-10-14).
- Inicio y progreso de Pygame: (2025-10-28 / 2025-10-31).
- CI estable con coverage y pylint: (2025-10-31).

## Anexos

- Diagrama de clases ![alt text](image.png)

## Conclusión

El diseño prioriza la separación de responsabilidades y la testabilidad. Las excepciones garantizan flujos controlados desde el core y mensajes claros en la interfaz. La estrategia de pruebas y la integración de lint/coverage en CI sustentan la calidad del código. La modularidad lograda habilita seguir iterando (por ejemplo, IA o mejoras gráficas) sin comprometer la lógica central del juego.

