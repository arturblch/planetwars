import pytest
from src import Planet


class Test_Planet():

    def test_vision_range(self):
        test_planet = Planet.Planet(0, 0, 1, 1, 50, 2)
        assert test_planet.VisionRange() == 5

    def test_planet_equal(self):
        test_planet1 = Planet.Planet(0, 0, 1, 1, 50, 2)
        test_planet2 = Planet.Planet(0, 0, 2, 1, 50, 2)
        assert test_planet1 == test_planet1
        assert test_planet1 != test_planet2

    def test_copy(self):
        test_planet = Planet.Planet(0, 0, 1, 1, 50, 2)
        result = test_planet.Copy()
        assert (result  is not test_planet)