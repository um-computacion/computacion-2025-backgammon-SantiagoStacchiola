## Registro de Prompts de IA — Documentación y Tooling

Consultas usadas para mejorar documentación, calidad y CI del proyecto. Se registran solo las preguntas y el contexto de uso, siguiendo el formato del repositorio de referencia.

### Prompt 1

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Quiero reescribir mi README tomando como base el de un repo de referencia, ¿cómo comparo y adapto la estructura a mi proyecto (CLI y Pygame incluidos)?"
- Uso de la salida: Usada con modificaciones
- Referencia en archivos finales: `README.md`
- Referencia a commits: actualización del README (2025-10-31)

### Prompt 2

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo actualizo el CHANGELOG siguiendo 'Keep a Changelog' y basándome en mis últimos commits y PRs?"
- Uso de la salida: Usada
- Referencia en archivos finales: `CHANGELOG.md`
- Referencia a commits: merges y versiones 2.1.0 / 2.2.0 (2025-10-14, 2025-10-28)

### Prompt 3

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "En GitHub Actions me falla: 'coverage: command not found'. ¿Cómo lo soluciono instalando dependencias y ejecutando `coverage` de forma robusta?"
- Uso de la salida: Usada (instalar dependencias y usar `python -m coverage`)
- Referencia en archivos finales: `.github/workflows/ci.yml`
- Referencia a commits: fix del workflow de CI (2025-10-31)

### Prompt 4

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "¿Cómo ejecuto Pylint en Windows usando venv y cuáles son las reglas más importantes a corregir primero?"
- Uso de la salida: Usada (ejecución y correcciones básicas)
- Referencia en archivos finales: `.pylintrc` (si corresponde), ajustes en `core/*`
- Referencia a commits: "mejora pylint y excepcion" (2025-09-28)

### Prompt 5

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Estoy escribiendo JUSTIFICACION.md; ¿qué estructura seguir (diseño general, clases, atributos, excepciones, testing, SOLID) y cómo aterrizarlo a mi código?"
- Uso de la salida: Usada con modificaciones
- Referencia en archivos finales: `JUSTIFICACION.md`
- Referencia a commits: documentación final (2025-10-31)

### Prompt 6

- Modelo / herramienta usada: GitHub Copilot Chat (Octubre 2025)
- Instrucciones del sistema: Configuración por defecto
- Prompt exacto usado: "Quiero registrar prompts como en el repo de referencia. ¿Qué secciones mínimas necesito y cómo dejar constancia del uso/commits?"
- Uso de la salida: Usada (este archivo y los de desarrollo/testing)
- Referencia en archivos finales: `prompts-desarrollo.md`, `prompts-documentacion.md`, `prompts-testing.md`
- Referencia a commits: documentación de prompts (2025-10-31)

