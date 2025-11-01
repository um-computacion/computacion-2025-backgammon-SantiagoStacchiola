## Registro de Prompts de IA — Desarrollo

A continuación se registran consultas reales/típicas que guían el desarrollo técnico del proyecto. Se listan solo las preguntas (consultas) y el contexto de uso, sin incluir respuestas largas, siguiendo el estilo del repositorio de referencia.

### Prompt 1

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo organizar el proyecto Backgammon separando core (reglas) de las interfaces (CLI y Pygame) para no mezclar responsabilidades?"
- Uso de la salida: Usada para definir estructura de carpetas y módulos
- Referencia en archivos finales: `core/`, `cli/cli.py`, `pygame_ui/`
- Referencia a commits: "correción de la estructura general" (2025-09-27), "primeros pasos cli" (2025-09-30)

### Prompt 2

- Modelo / herramienta usada: GitHub Copilot Chat (Septiembre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cuál es una buena representación interna del tablero (24 puntos, barra y fichas afuera) para poder validar movimientos y mostrar el estado en CLI?"
- Uso de la salida: Usada con modificaciones para el contenedor del `Tablero`
- Referencia en archivos finales: `core/board.py`
- Referencia a commits: "correcciones en las carpetas board y player" (2025-09-17)

### Prompt 3

- Modelo / herramienta usada: GitHub Copilot Chat (Septiembre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Ayudame a listar las clases mínimas (Juego, Tablero, Jugador, Dados, Ficha) y qué responsabilidad exacta tiene cada una."
- Uso de la salida: Usada como guía de diseño OO
- Referencia en archivos finales: `core/game.py`, `core/board.py`, `core/player.py`, `core/dice.py`, `core/checker.py`
- Referencia a commits: "correcciones en las carpetas board y player" (2025-09-17)

### Prompt 4

- Modelo / herramienta usada: GitHub Copilot Chat (Septiembre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo diseñar excepciones específicas del dominio (movimiento inválido, sacar ficha inválido, jugador inválido) y dónde lanzarlas?"
- Uso de la salida: Usada con ajustes (archivo de excepciones y uso en core)
- Referencia en archivos finales: `core/excepcions.py`, `core/board.py`, `core/game.py`
- Referencia a commits: "agregado y aplicado de exepciones" (2025-09-28), "mejora pylint y excepcion" (2025-09-28)

### Prompt 5

- Modelo / herramienta usada: GitHub Copilot Chat (Septiembre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Quiero iniciar el CLI pero que sea fino: ¿cómo delego toda la lógica al core y dejo el CLI solo como capa de entrada/salida?"
- Uso de la salida: Usada (CLI delgado)
- Referencia en archivos finales: `cli/cli.py`, `core/game.py`, `core/board.py`
- Referencia a commits: "primeros pasos cli" (2025-09-30), "Simplificación mayor del CLI y migración inicial al core" (2025-10-11)

### Prompt 6

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo implementar el flujo de turno con dados (incluye dobles) y consumo de tiradas sin duplicar lógica entre CLI y core?"
- Uso de la salida: Usada con modificaciones (métodos en `Dados` y orquestación en `Juego`)
- Referencia en archivos finales: `core/dice.py`, `core/game.py`
- Referencia a commits: "complementacion de game con cli" (2025-10-11)

### Prompt 7

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Reglas de barra y borneoff: ¿cómo valido que todas las fichas estén en el último cuadrante antes de permitir 'sacar ficha'?"
- Uso de la salida: Usada con modificaciones
- Referencia en archivos finales: `core/board.py`, `cli/cli.py`
- Referencia a commits: "mejora board y checker" (2025-10-13)

### Prompt 8

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "En CLI se imprime el tablero dos veces, ¿cómo organizo las impresiones para mostrar el estado solo cuando corresponde?"
- Uso de la salida: Usada (función auxiliar y lugar único de impresión)
- Referencia en archivos finales: `cli/cli.py`, `core/board.py`
- Referencia a commits: "funcionamiento correcto cli" (2025-10-14)

### Prompt 9

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Quiero empezar la interfaz Pygame: ¿cómo armo el bucle principal (event loop), el clock y el render inicial del tablero sin bloquear?"
- Uso de la salida: Usada (esqueleto de ventana y bucle)
- Referencia en archivos finales: `pygame_ui/main.py`, `pygame_ui/board_renderer.py`
- Referencia a commits: "compienzo de pygame" (2025-10-28)

### Prompt 10

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo mapeo coordenadas de puntos del tablero (0..23) a posiciones en pantalla para dibujar fichas en Pygame?"
- Uso de la salida: Usada con ajustes (funciones de posicionamiento)
- Referencia en archivos finales: `pygame_ui/board_renderer.py`
- Referencia a commits: "progreso pygame" (2025-10-31)

