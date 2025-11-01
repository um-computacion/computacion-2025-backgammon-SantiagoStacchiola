# Backgammon Computación 2025

**Autor:** Santiago Stacchiola

---

## Descripción
Proyecto individual de la materia Computación 2025: implementación del juego clásico de Backgammon en Python, con foco en diseño limpio, separación de responsabilidades y pruebas automatizadas.

- Lógica de negocio en `core/` (tablero, fichas, jugadores, dados, reglas).
- Interfaz de línea de comandos en `cli/` para jugar por consola.
- Interfaz gráfica inicial con Pygame en `pygame_ui/` (tablero, barra, borne-off, resaltado de movimientos y panel de dados).

---

## Características principales

- Juego por consola (CLI) y UI gráfica básica con Pygame.
- Diseño orientado a objetos con bajo acoplamiento.
- Excepciones de dominio para validar reglas y estados.
- Suite de pruebas unitarias completa y cobertura alta (>90%).
- Pylint configurado con buen puntaje tras ajustes.

---

## Estructura del proyecto

```
core/        -> lógica central: Board, Checker, Game, Player, Dice, excepciones
cli/         -> interfaz de consola (BackgammonCLI)
pygame_ui/   -> interfaz gráfica (BoardView + loop de juego)
tests/       -> pruebas unitarias
```

Archivos destacados:
- `cli/cli.py`: entrada para el modo consola (`python -m cli.cli`).
- `pygame_ui/main.py`: entrada para la UI Pygame (`python -m pygame_ui.main`).
- `core/game.py`: orquestador del flujo de juego y reglas (turnos, barra, bearing off, victoria).
- `.pylintrc`: configuración de linting.
- `CHANGELOG.md`: registro de cambios.

---

## Requisitos

- Python 3.10+
- (Para UI) Pygame 2.x

Sistemas probados: Windows 10/11 (PowerShell). Funciona también en Linux/Mac con comandos equivalentes.

---

## Instalación (Windows PowerShell)

1) Clonar el repositorio
```
git clone https://github.com/um-computacion/computacion-2025-backgammon-SantiagoStacchiola.git
cd computacion-2025-backgammon-SantiagoStacchiola
```

2) Crear y activar entorno virtual
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Instalar dependencias
```
python -m pip install --upgrade pip
# requirements.txt puede estar vacío; instala lo necesario:
pip install pygame coverage pylint
```

---

## Cómo ejecutar

### Modo consola (CLI)
```
python -m cli.cli
```

### Modo gráfico (Pygame)
```
python -m pygame_ui.main
```

Controles UI:
- ESPACIO: tirar dados.
- Click: seleccionar origen y destino (incluye barra y bandeja de salida).
- ESC: salir.

La UI resalta destinos válidos, muestra dados disponibles y nombres de jugadores; cambia de turno automáticamente cuando corresponde y detecta victoria.

---

## Testing y cobertura

Ejecutar tests:
```
python -m unittest discover -s tests -p "test_*\.py"
```

Cobertura (texto y XML):
```
python -m coverage run -m unittest discover -s tests -p "test_*\.py"
python -m coverage report -m
python -m coverage xml -o coverage.xml
```

---

## Linting

Ejecutar Pylint (usa `.pylintrc`):
```
pylint --rcfile=.pylintrc core cli pygame_ui tests
```

---

 

## Reglas implementadas (resumen)

- Movimiento por puntos según los dados y dirección por color.
- Reingreso obligatorio desde la barra antes de cualquier otro movimiento.
- Captura válida sólo si hay exactamente una ficha rival en el punto destino.
- Bearing off habilitado cuando todas las fichas propias están en el home board.
- Detección de victoria al sacar todas las fichas.

Excepciones de dominio ayudan a detectar y comunicar jugadas inválidas de forma clara.

---

## Documentación y recursos

- `CHANGELOG.md`: historial detallado.
- `JUSTIFICACION.md`: decisiones de diseño.
- `prompts-*.md`: prompts usados para desarrollo, documentación y testing.

---

## CI y calidad

- Integración Continua: GitHub Actions corre tests y cobertura en cada push/PR (equivalente a CircleCI/Travis para los fines del curso). Workflow en `.github/workflows/ci.yml`.
- Linting: Pylint con configuración en `.pylintrc`.
- Cobertura: `coverage.xml` y reporte de texto en `coverage_report.txt`.

### Integración con Code Climate o Coveralls (recomendado por la cátedra)

Para publicar cobertura y calidad en tiempo real y apuntar a calificación “A” sin issues:

1) Crear cuenta en Code Climate Quality o Coveralls y vincular el repo.
2) Generar un token del repositorio y guardarlo como secreto en GitHub:
	- En GitHub: Settings → Secrets and variables → Actions → New repository secret.
	- Nombre sugerido: `CC_TEST_REPORTER_ID` (Code Climate) o `COVERALLS_REPO_TOKEN` (Coveralls).
3) Extender el workflow de GitHub Actions para subir cobertura (requiere el token). Ejemplos oficiales:
	- Code Climate Test Reporter: https://docs.codeclimate.com/docs/test-coverage
	- Coveralls GitHub Action: https://github.com/coverallsapp/github-action

Nota: La configuración de la calificación “A” y “0 issues” depende del servicio externo y no puede garantizarse solo desde el repositorio; requiere revisar y resolver findings en la plataforma elegida.

### Protección de rama `main`

Para cumplir con la regla de protección solicitada:
1) En GitHub: Settings → Branches → Branch protection rules → Add rule.
2) Branch name pattern: `main`.
3) Habilitar al menos:
	- Require a pull request before merging.
	- Require status checks to pass before merging (seleccionar el workflow de CI).
	- Restrict who can push to matching branches (opcional).

---

Trabajo práctico individual para la materia Computación 2025.