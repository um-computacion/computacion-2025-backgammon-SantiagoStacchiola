"""Tests para la clase Ficha."""
# pylint: disable=missing-function-docstring

import unittest
from core.checker import Ficha
from core.excepcions import (JugadorInvalidoError, FichaInvalidaError,
                           MovimientoInvalidoError)


class TestChecker(unittest.TestCase):
    """Pruebas sobre la ficha del juego."""

    def test_creacion_valida(self):
        """Prueba la creación de una ficha con valores válidos."""
        f = Ficha("blanca", 0)
        self.assertEqual(f.obtener_color(), "blanca")
        self.assertEqual(f.obtener_posicion(), 0)

    def test_creacion_invalida(self):
        """Prueba la creación de una ficha con valores inválidos."""
        with self.assertRaises(JugadorInvalidoError):
            Ficha("roja", 5)  # color inválido

    def test_mover(self):
        """Prueba el movimiento de una ficha."""
        f = Ficha("negra", 10)
        f.mover(15)
        self.assertEqual(f.obtener_posicion(), 15)

    def test_en_barra(self):
        """Prueba la verificación de si una ficha está en la barra."""
        f = Ficha("blanca", "barra")
        self.assertTrue(f.esta_en_barra())
        self.assertFalse(f.esta_afuera())

    def test_afuera(self):
        """Prueba la verificación de si una ficha está afuera."""
        f = Ficha("negra", "afuera")
        self.assertTrue(f.esta_afuera())
        self.assertFalse(f.esta_en_barra())

    def test_repr(self):
        """Prueba la representación en cadena de una ficha."""
        f = Ficha("blanca", 3)
        self.assertIn("blanca", repr(f))
        self.assertIn("3", repr(f))

    def test_puede_mover_basico(self):
        """Comprueba movimientos legales básicos de una ficha."""
        f = Ficha("blanca", 1)
        self.assertTrue(f.puede_mover_a(3))
        self.assertFalse(f.puede_mover_a(5))

    def test_puede_mover_fichas_negras(self):
        """Prueba movimientos de fichas negras."""
        f = Ficha("negra", 10)
        self.assertTrue(f.puede_mover_a(8))  # diferencia 2
        self.assertFalse(f.puede_mover_a(6))  # diferencia 4

    def test_puede_mover_posicion_none(self):
        """Prueba movimiento con posición None."""
        f = Ficha("blanca", None)
        self.assertFalse(f.puede_mover_a(3))

    def test_metodo_puede_mover(self):
        """Prueba el método puede_mover."""
        f = Ficha("blanca", 1)
        result = f.puede_mover(1, 3)
        self.assertTrue(result)

    def test_puede_mover_diferentes_distancias(self):
        """Prueba movimientos con diferentes distancias para fichas blancas."""
        f = Ficha("blanca", 5)
        # Probar todas las distancias válidas excepto 4
        self.assertTrue(f.puede_mover_a(6))   # diferencia 1
        self.assertTrue(f.puede_mover_a(7))   # diferencia 2
        self.assertTrue(f.puede_mover_a(8))   # diferencia 3
        self.assertFalse(f.puede_mover_a(9))  # diferencia 4 (no válida)
        self.assertTrue(f.puede_mover_a(10))  # diferencia 5
        self.assertTrue(f.puede_mover_a(11))  # diferencia 6

    def test_puede_mover_negras_diferentes_distancias(self):
        """Prueba movimientos con diferentes distancias para fichas negras."""
        f = Ficha("negra", 15)
        # Probar todas las distancias válidas excepto 4
        self.assertTrue(f.puede_mover_a(14))  # diferencia 1
        self.assertTrue(f.puede_mover_a(13))  # diferencia 2
        self.assertTrue(f.puede_mover_a(12))  # diferencia 3
        self.assertFalse(f.puede_mover_a(11)) # diferencia 4 (no válida)
        self.assertTrue(f.puede_mover_a(10))  # diferencia 5
        self.assertTrue(f.puede_mover_a(9))   # diferencia 6

    def test_obtener_posicion_method(self):
        """Prueba específica del método obtener_posicion."""
        f = Ficha("blanca", 10)
        pos = f.obtener_posicion()
        self.assertEqual(pos, 10)

    def test_puede_mover_casos_limite(self):
        """Prueba casos límite de puede_mover_a."""
        f = Ficha("blanca", 0)
        # Casos límite
        self.assertTrue(f.puede_mover_a(1))   # diferencia 1
        self.assertTrue(f.puede_mover_a(6))   # diferencia 6
        self.assertFalse(f.puede_mover_a(4))  # diferencia 4 (no válida)

        # Casos para fichas negras
        f_negra = Ficha("negra", 20)
        self.assertTrue(f_negra.puede_mover_a(19))  # diferencia 1
        self.assertTrue(f_negra.puede_mover_a(14))  # diferencia 6
        self.assertFalse(f_negra.puede_mover_a(16)) # diferencia 4 (no válida)

    def test_can_move_alias_en_ingles(self):
        """Test del método alias en inglés can_move."""
        f = Ficha("blanca", 5)
        # Test del alias en inglés
        self.assertTrue(f.can_move(5, 11))   # diferencia 6
        self.assertFalse(f.can_move(5, 12))  # diferencia 7 (demasiado)

    def test_estados_especiales_ficha(self):
        """Test de estados especiales de la ficha."""
        # Test ficha en barra
        f_barra = Ficha("negra", "barra")
        self.assertTrue(f_barra.esta_en_barra())
        self.assertFalse(f_barra.esta_afuera())

        # Test ficha afuera
        f_afuera = Ficha("blanca", "afuera")
        self.assertTrue(f_afuera.esta_afuera())
        self.assertFalse(f_afuera.esta_en_barra())

        # Test repr
        f_normal = Ficha("blanca", 3)
        repr_str = repr(f_normal)
        self.assertIn("blanca", repr_str)
        self.assertIn("3", repr_str)

    def test_movimientos_casos_limite(self):
        """Test de movimientos en casos límite."""
        # Test ficha en posición None
        f = Ficha("blanca", None)
        self.assertFalse(f.puede_mover_a(3))

        # Test movimiento desde posición 0
        f_inicio = Ficha("negra", 0)
        self.assertTrue(f_inicio.puede_mover_a(1))   # diferencia 1
        self.assertTrue(f_inicio.puede_mover_a(6))   # diferencia 6
        self.assertFalse(f_inicio.puede_mover_a(4))  # diferencia 4 (no válida)

    def test_validaciones_nuevas_ficha(self):
        """Test de nuevas validaciones de ficha."""
        # Test validar_nueva_posicion
        f = Ficha("blanca", 5)
        self.assertTrue(f.validar_nueva_posicion(10))
        self.assertTrue(f.validar_nueva_posicion("barra"))
        self.assertTrue(f.validar_nueva_posicion("afuera"))
        self.assertFalse(f.validar_nueva_posicion(25))
        self.assertFalse(f.validar_nueva_posicion("invalid"))

        # Test validar_nueva_posicion como reemplazo de es_posicion_valida
        self.assertTrue(f.validar_nueva_posicion(15))
        self.assertFalse(f.validar_nueva_posicion(-1))

        # Test alias en inglés
        self.assertEqual(f.get_color(), "blanca")
        self.assertEqual(f.get_position(), 5)
        self.assertFalse(f.is_on_bar())
        self.assertFalse(f.is_off_board())

    def test_puede_mover_casos_especiales(self):
        """Test de puede_mover con casos especiales."""
        f = Ficha("blanca", 5)

        # Test con valores None
        self.assertFalse(f.puede_mover(None, 10))
        self.assertFalse(f.puede_mover(5, None))

        # Test desde barra
        self.assertTrue(f.puede_mover("barra", 3))
        self.assertFalse(f.puede_mover("barra", "invalid"))

        # Test hacia afuera
        self.assertTrue(f.puede_mover(20, "afuera"))
        self.assertFalse(f.puede_mover("invalid", "afuera"))

        # Test con tipos incorrectos
        self.assertFalse(f.puede_mover("invalid", 10))
        self.assertFalse(f.puede_mover(5, "invalid"))

    def test_mover_con_validacion(self):
        """Test de mover() con validación."""

        f = Ficha("blanca", 5)

        # Movimiento válido
        f.mover(10)
        self.assertEqual(f.obtener_posicion(), 10)

        # Movimiento inválido debería lanzar excepción
        with self.assertRaises(MovimientoInvalidoError):
            f.mover("invalid_position")

    def test_excepciones_creacion(self):
        """Test de excepciones en la creación de fichas."""

        # Color inválido
        with self.assertRaises(JugadorInvalidoError):
            Ficha("roja", 5)

        # Tipo de color incorrecto
        with self.assertRaises(FichaInvalidaError):
            Ficha(123, 5)

    def test_puede_mover_tipos_incorrectos(self):
        """Test para cubrir línea 63 - validación de tipos incorrectos."""
        f = Ficha("blanca", 5)
        
        # Test con desde_punto string pero no válido
        resultado = f.puede_mover("invalido", 10)
        self.assertFalse(resultado)
        
        # Test con hasta_punto string pero no válido  
        resultado = f.puede_mover(5, "invalido")
        self.assertFalse(resultado)

    def test_puede_mover_excepciones(self):
        """Test para cubrir líneas 69-70 - manejo de excepciones ValueError/TypeError."""
        f = Ficha("blanca", 5)
        
        # Crear situación que genere excepción interna con operaciones matemáticas
        resultado = f.puede_mover(float('inf'), 10)
        self.assertFalse(resultado)
        
        resultado = f.puede_mover(5, float('inf'))
        self.assertFalse(resultado)
        
        # Casos que podrían generar TypeError en operaciones internas
        resultado = f.puede_mover(complex(1, 1), 10)
        self.assertFalse(resultado)
        
        resultado = f.puede_mover(10, complex(1, 1))
        self.assertFalse(resultado)

    def test_puede_mover_forzar_excepciones_lineas_69_70(self):
        """Test para forzar excepciones en líneas 69-70."""
        f = Ficha("blanca", 5)
        
        # Crear un objeto que herede de int pero cause problemas en operaciones
        class ProblematicInt(int):
            def __new__(cls, value):
                return int.__new__(cls, value)
            
            def __sub__(self, other):
                raise ValueError("Error forzado en __sub__")
            
            def __rsub__(self, other):
                raise TypeError("Error forzado en __rsub__")
            
            def __abs__(self):
                raise ValueError("Error forzado en __abs__")
        
        # Estos objetos pasarán isinstance(x, int) pero fallarán en abs()
        problematic_5 = ProblematicInt(5)
        problematic_10 = ProblematicInt(10)
        
        # Esto debería activar el except ValueError/TypeError (líneas 69-70)
        resultado = f.puede_mover(problematic_5, 10)
        self.assertFalse(resultado)
        
        resultado = f.puede_mover(5, problematic_10) 
        self.assertFalse(resultado)
        
        resultado = f.puede_mover(problematic_5, problematic_10)
        self.assertFalse(resultado)


if __name__ == '__main__':
    unittest.main()
# EOF
