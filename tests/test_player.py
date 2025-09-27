"""Tests para la clase Player."""
# pylint: disable=missing-function-docstring,protected-access

import unittest
from core.player import Player
from core.checker import Ficha


class TestPlayer(unittest.TestCase):
    """Pruebas sobre la lógica del jugador."""

    def test_creacion_color_valido(self):
        """Prueba la creación de jugadores con colores válidos."""
        p1 = Player("blanca")
        p2 = Player("negra")
        self.assertEqual(p1.get_color(), "blanca")
        self.assertEqual(p2.get_color(), "negra")
        self.assertEqual(p1.get_total_fichas(), 15)

    def test_creacion_color_invalido(self):
        """Prueba que se lanza una excepción al crear un jugador con un color inválido."""
        with self.assertRaises(ValueError):
            Player("rojo")

    def test_enviar_y_sacar_de_barra(self):
        """Prueba el envío y la salida de fichas de la barra."""
        p = Player("blanca")
        f = Ficha("blanca")
        p.enviar_a_barra(f)
        self.assertEqual(p.fichas_en_barra(), 1)
        ficha = p.sacar_de_barra()
        self.assertIsInstance(ficha, Ficha)
        self.assertEqual(p.fichas_en_barra(), 0)
        self.assertIsNone(p.sacar_de_barra())

    def test_sacar_del_tablero(self):
        """Prueba la mecánica de sacar fichas del tablero."""
        p = Player("negra")
        f = Ficha("negra")
        p.sacar_del_tablero(f)
        self.assertEqual(p.fichas_fuera(), 1)
        self.assertTrue(f.esta_afuera())

    def test_fichas_restantes(self):
        """Verifica el conteo de fichas restantes del jugador."""
        p = Player("blanca")
        f1 = Ficha("blanca")
        f2 = Ficha("blanca")
        p.sacar_del_tablero(f1)
        p.sacar_del_tablero(f2)
        self.assertEqual(p.fichas_restantes(), 13)

    def test_player_has_checker(self):
        """Comprueba detección de fichas en un punto."""
        p = Player("blanca")
        f1 = Ficha("blanca")
        f2 = Ficha("blanca")
        p.sacar_del_tablero(f1)
        p.sacar_del_tablero(f2)
        self.assertTrue(p._tiene_ficha_en_punto(f1.get_posicion()))
        self.assertFalse(p._tiene_ficha_en_punto((0, 0)))

    def test_has_checker_en_barra(self):
        """Prueba detección de fichas en la barra."""
        p = Player("blanca")
        f = Ficha("blanca", 5)
        p.enviar_a_barra(f)
        # La ficha debería estar en "barra", no en posición 5
        self.assertTrue(p.has_checker("barra"))
        self.assertFalse(p.has_checker(99))  # Posición inexistente

    def test_has_checker_multiple_locations(self):
        """Prueba has_checker buscando en múltiples ubicaciones."""
        p = Player("negra")

        # Ficha en barra
        f1 = Ficha("negra", 10)
        p.enviar_a_barra(f1)  # Esto la mueve a "barra"

        # Ficha fuera del tablero
        f2 = Ficha("negra", 15)
        p.sacar_del_tablero(f2)  # Esto la mueve a "afuera"

        # Verificar que encuentra fichas en ambas ubicaciones
        self.assertTrue(p.has_checker("barra"))
        self.assertTrue(p.has_checker("afuera"))
        self.assertFalse(p.has_checker("inexistente"))

    def test_sacar_de_barra_vacia(self):
        """Prueba sacar de barra cuando está vacía."""
        p = Player("blanca")
        # Barra vacía inicialmente
        ficha = p.sacar_de_barra()
        self.assertIsNone(ficha)
        self.assertEqual(p.fichas_en_barra(), 0)

    def test_has_checker_casos_especificos(self):
        """Prueba has_checker con casos específicos para cubrir todas las ramas."""
        p = Player("blanca")

        # Caso 1: ficha en __fuera__ con posición específica
        f1 = Ficha("blanca", 5)
        f1.mover("afuera")
        p.__fuera__.append(f1)
        self.assertTrue(p.has_checker("afuera"))

        # Caso 2: ficha en __barra__ con posición específica
        f2 = Ficha("blanca", 10)
        f2.mover("barra")
        p.__barra__.append(f2)
        self.assertTrue(p.has_checker("barra"))

        # Caso 3: punto que no existe en ninguna lista
        self.assertFalse(p.has_checker("punto_inexistente"))


if __name__ == '__main__':
    unittest.main()

# EOF