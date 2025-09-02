# Changelog
Todas las modificaciones notables de este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [1.0.0] - 2025-08-26
### Added
- Clase `Board` con métodos básicos: mover_ficha, guardar_ficha, quitar_ficha, enviar_a_barra, etc.
- Clase `Dice` con soporte para dobles y valores consumibles.
- Clase `Player` para gestionar fichas, barra y fichas fuera.
- Clase `Game` con lógica de turnos, reglas de movimiento y verificación de victoria.
- Tests unitarios con `unittest` cubriendo más del 95% de `core/`.

### Changed
- Se renombró la clase `Tablero` a `Board` para cumplir con la consigna.
- Se reorganizó la lógica: reglas pasaron de `Board` a `Game`.

### Fixed
- Bug en `mover_ficha` que quitaba todas las fichas en lugar de solo una.
- Corrección de casos de captura en `Game`.

### Removed
- Eliminados accesos directos a atributos privados de `Dice` en los tests; ahora se propone un método `set_valores` para control de tests.
