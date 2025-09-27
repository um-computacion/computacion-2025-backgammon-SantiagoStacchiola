# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Sin liberar]

### En desarrollo
- Finalización de refactoring y optimizaciones
- Preparación para entrega final del proyecto

---

## [0.1.0] - 2025-08-24

### "GitHub Classroom Feedback"
#### Agregado
- Inicialización del repositorio del proyecto
- Configuración básica de Git y estructura inicial

### "Setting up GitHub Classroom Feedback"
#### Agregado
- Configuración inicial de GitHub Classroom
- Setup de repositorio educativo para proyecto de Computación

### "creacion de estructura basica"
#### Agregado
- **Estructura fundamental del proyecto**:
  - Directorio `core/` para lógica de negocio
  - Directorio `tests/` para pruebas unitarias
  - Archivos `__init__.py` para módulos Python
- **Clases base del dominio**:
  - Esqueleto de clase `Game` para control de flujo
  - Esqueleto de clase `Board` para tablero
  - Esqueleto de clase `Player` para jugadores
  - Esqueleto de clase `Dice` para dados
- **Configuración inicial**:
  - Setup de proyecto Python con arquitectura modular
  - Definición de separación entre lógica y presentación

### Merge pull request #3 - Estructura inicial
#### Agregado
- Integración de estructura inicial del proyecto

---

## [0.1.1] - 2025-08-25

### "progreso de la clase tablero"
#### Agregado
- **Implementación inicial completa de `Board`**:
  - Estructura fundamental del tablero de Backgammon
  - Contenedor de 24 posiciones (`__contenedor__`)
  - Métodos fundamentales de acceso y manipulación
- **Configuración del proyecto**:
  - Organización modular definida
  - Interfaces básicas entre componentes

### Merge pull request #4 - Estructura básica completa
#### Agregado
- Integración final de estructura básica del proyecto

---

## [0.2.0] - 2025-08-26

### "avances en las clases board y game"
#### Agregado
- **Desarrollo significativo en clase `Board`**:
  - Sistema completo de 24 posiciones del tablero
  - Configuración inicial estándar del Backgammon
  - Gestión correcta de fichas blancas y negras en posiciones iniciales
- **Desarrollo significativo en clase `Game`**:
  - Control de flujo principal del juego
  - Integración con Board y componentes del sistema
  - Lógica fundamental de turnos y estados

### Merge pull request #6 - Avances board y game
#### Agregado
- Integración de avances significativos en clases principales

---

## [0.2.1] - 2025-08-27

### "desarrollo de metodos en las clases game y board"
#### Agregado
- **Métodos principales en clase `Game`**:
  - `mover()` - Lógica completa de movimientos con validación
  - `movimiento_valido()` - Validación según reglas de Backgammon
  - `cambiar_turno()` - Control de turnos entre jugadores
  - `verificar_victoria()` - Detección de condiciones de fin de juego
- **Métodos principales en clase `Board`**:
  - `mover_ficha()` - Movimiento físico de fichas en tablero
  - `enviar_a_barra()` - Sistema completo de capturas
  - `reingresar_desde_barra()` - Reingreso de fichas capturadas
  - `sacar_ficha()` - Salida de fichas del tablero

### Merge pull request #7 - Métodos principales
#### Agregado
- Integración de métodos principales desarrollados

---

## [0.2.2] - 2025-08-28

### "modificacion en las clases dice y player"
#### Cambiado
- **Mejoras significativas en clase `Dice`**:
  - Soporte completo para dobles (4 movimientos)
  - Sistema de valores consumibles (`__valores__`)
  - Métodos `roll()` y `tirar()` para compatibilidad
#### Agregado
- **Avances importantes en clase `Player`**:
  - Estructura mejorada para gestión de fichas
  - Preparación para funcionalidades avanzadas

### Merge pull request #8 - Desarrollo dice y player
#### Agregado
- Integración de desarrollos en Dice y Player

### "desarrollo de funciones en las clases"
#### Agregado
- **Funciones avanzadas distribuidas**:
  - Mejoras en interacción entre Game, Board y Player
  - Optimización de algoritmos existentes
  - Funcionalidades complementarias en múltiples clases

### Merge pull request #10 - Funciones avanzadas
#### Agregado
- Integración de funcionalidades avanzadas distribuidas

---

## [0.2.3] - 2025-08-31

### "desarrollo de la clase player"
#### Agregado
- **Clase `Player` completamente implementada**:
  - Gestión completa de fichas del jugador
  - Sistema de barra para fichas capturadas (`__barra__`)
  - Control de fichas fuera del tablero (`__fuera__`)
  - Validación de colores (blanca/negra)
  - Métodos: `enviar_a_barra`, `sacar_de_barra`, `fichas_restantes`

### Merge pull request #11 - Desarrollo completo player
#### Agregado
- Integración del desarrollo completo de la clase Player

---

## [0.2.4] - 2025-09-01

### "funcion agregada en la clase board"
#### Agregado
- **Funcionalidades complementarias en `Board`**:
  - Métodos adicionales para gestión avanzada del tablero
  - Optimizaciones en manipulación de fichas

### Merge pull request #12 - Funciones avanzadas board
#### Agregado
- Integración de funcionalidades avanzadas en Board

### "creacion de los tests y correccion general de las clases"
#### Agregado
- **Suite inicial completa de tests unitarios**:
  - `tests/test_game.py` - Tests del flujo principal del juego
  - `tests/test_board.py` - Tests completos del tablero
  - `tests/test_player.py` - Tests de gestión de jugadores
  - `tests/test_dice.py` - Tests de dados con mocking
#### Cambiado
- **Correcciones generales en todas las clases**:
  - Ajustes para compatibilidad con framework de testing
  - Mejoras en encapsulación y interfaces
  - Estandarización de métodos y atributos

### Merge pull request #14 - Suite inicial de tests
#### Agregado
- Integración completa de la primera suite de tests

---

## [0.3.0] - 2025-09-02

### "ampleacion de los tests"
#### Agregado
- **Tests adicionales para todas las clases**:
  - Expansión de `test_game.py`, `test_board.py`, `test_player.py`
  - Validación de casos límite y errores
  - Mejora en robustez de las pruebas

### Merge pull request #15 - Ampliación tests
#### Agregado
- Merge de ampliación de tests desarrollados

### "ampleacion de tests"
#### Agregado
- **Expansión mayor de suite de tests**:
  - Cobertura mejorada para casos edge
  - Tests adicionales para validación de reglas
  - Mejora significativa en porcentaje de cobertura

### Merge pull request #16 - Ampliación de tests
#### Agregado
- Integración de ampliación significativa de tests

---

## [0.3.1] - 2025-09-14

### "clase ficha"
#### Agregado
- **Implementación completa de clase `Checker` (Ficha)**:
  - Estructura base con atributos `__privados__`
  - Métodos fundamentales: `mover`, `obtener_color`, `obtener_posicion`
  - Validación de colores y posiciones
  - Estados: tablero, barra, afuera

### Merge pull request #17 - Implementación clase ficha
#### Agregado
- Integración completa de la clase Ficha al proyecto principal

---

## [0.3.2] - 2025-09-15

### "agregar funciones a checker"
#### Agregado
- **Funciones básicas en clase `Checker`**:
  - Métodos de movimiento básicos
  - Validación inicial de posiciones
  - Estructura base de la clase

### Merge pull request #19 - Creación de funciones
#### Agregado
- Integración de nuevas funcionalidades desarrolladas

### "avances con la clase checker"
#### Agregado
- Desarrollo intermedio de funcionalidades en `Checker`
- Mejoras en encapsulación y métodos fundamentales

### Merge pull request #20 - Avances checker
#### Agregado
- Merge de desarrollos significativos en funcionalidades de fichas

### "desarrollo de funciones en la clase checker"
#### Agregado
- **Métodos avanzados en clase `Checker`**:
  - Validación completa de movimientos según reglas
  - Lógica de posicionamiento y estados
  - Métodos `puede_mover_a()` y `can_move()`

### Merge pull request #21 - Funciones avanzadas checker
#### Agregado
- Integración de funcionalidades avanzadas desarrolladas

---

## [0.3.3] - 2025-09-16

### "tests de checker"
#### Agregado
- Implementación base de tests unitarios para clase `Checker`
- Estructura fundamental de validaciones y casos de prueba

### Merge pull request #22 - Tests iniciales checker
#### Agregado
- Merge de implementación inicial de tests para Checker

### "desarrollo de tests de checker"
#### Agregado
- **Suite exhaustiva de tests para clase `Checker`**:
  - Tests de creación válida e inválida de fichas
  - Validación de movimientos según reglas de Backgammon
  - Tests de estados: barra, afuera, en tablero
  - Cobertura completa de casos edge y límite

### Merge pull request #23 - Tests completos checker
#### Agregado
- Integración completa de todos los tests para clase Checker

### Merge pull request #24 - Resolución de conflictos
#### Corregido
- Conflictos de merge entre diferentes ramas de desarrollo
- Sincronización correcta del código base

---

## [0.4.0] - 2025-09-17

### "solucion problema ramas"
#### Corregido
- Problemas de sincronización entre ramas de desarrollo
- Consolidación del código base para evitar conflictos futuros

### "correcciones en las carpetas board y player"
#### Corregido
- Bugs críticos en la clase `Board` relacionados con movimiento de fichas
- Problemas de lógica en la clase `Player` para gestión de fichas
- Mejoras en la gestión correcta de posiciones y estados

### Merge pull request #26 - Correcciones importantes
#### Agregado
- Integración de correcciones críticas en clases principales

### "correcciones y adaptacion de clase ficha"
#### Cambiado
- Adaptación completa de la clase `Checker` (Ficha) para compatibilidad total
- Optimización de métodos de movimiento y validación
- Mejoras en integración con el resto del sistema

### Merge pull request #27 - Correcciones finales
#### Agregado
- Integración final de todas las correcciones y adaptaciones

---

## [1.0.0] - 2025-09-27

### "correción de la estructura general"
#### Cambiado
- Refactoring completo de la estructura del proyecto
- Optimización de arquitectura para cumplir con todos los requisitos del documento
- Estandarización final de nomenclatura y convenciones de código
- Ajustes finales para 100% de cobertura y calidad de código

---
