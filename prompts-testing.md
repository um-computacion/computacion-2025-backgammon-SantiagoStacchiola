## Registro de Prompts de IA — Testing y Cobertura

Consultas que guiaron la estrategia de pruebas unitarias/integración y la cobertura. Solo se registran las preguntas y el contexto de uso, sin respuestas extensas.

### Prompt 1

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Tengo poca cobertura en Board. ¿Qué casos faltantes puedo testear (rangos inválidos, barra vacía, mover desde barra, sacar ficha con color incorrecto) sin repetir lo existente?"
- Uso de la salida: Usada
- Referencia en archivos finales: `tests/test_board.py`
- Referencia a commits: mejoras de cobertura y reglas de tablero (2025-10-13)

### Prompt 2

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "También quiero subir cobertura de Game: ¿qué tests de turnos, ganador y estado de juego me faltan?"
- Uso de la salida: Usada
- Referencia en archivos finales: `tests/test_game.py`
- Referencia a commits: "mejora de cobertura tests game" (2025-10-12)

### Prompt 3

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo testeo el CLI sin ejecutar el loop real, simulando input y capturando print con unittest.mock.patch?"
- Uso de la salida: Usada con modificaciones
- Referencia en archivos finales: `tests/test_cli.py`
- Referencia a commits: "tests cli y game" (2025-10-13)

### Prompt 4

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Quiero generar coverage.xml y un reporte de texto. ¿Cómo ejecuto coverage con unittest discover y exporto ambos reportes?"
- Uso de la salida: Usada
- Referencia en archivos finales: `coverage.xml`, `coverage_report.txt`
- Referencia a commits: integración de coverage en CI (2025-10-31)

### Prompt 5

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Qué patrón de descubrimiento conviene para unittest en este repo (carpeta tests/ y archivos test_*.py) para que no se ejecuten cosas de Pygame accidentalmente?"
- Uso de la salida: Usada (scope de discovery)
- Referencia en archivos finales: `.github/workflows/ci.yml`
- Referencia a commits: fix del workflow (2025-10-31)

### Prompt 6

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Para tests deterministas, ¿cómo mockeo los dados y algunas funciones del tablero sin acoplarme a detalles internos?"
- Uso de la salida: Usada con modificaciones
- Referencia en archivos finales: `tests/test_cli.py`, `tests/test_game.py`
- Referencia a commits: suite de tests ampliada (2025-10-12 / 2025-10-13)

