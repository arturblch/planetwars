import pytest
from src.PlanetWarsProxy import PlanetWarsProxy
from src.Planet import Planet
import sys


class TestPlanetWarsProxy():
    def setup(self):
        self.test_proxy = PlanetWarsProxy()

    def test_parse_planet(self):
        test_planet = 'P 2 2 1 1 50 4'.split()
        result = self.test_proxy._ParsePlanet(test_planet)
        assert type(result) == Planet

    def test_find_size(self):
        self.test_proxy._planets[1] = Planet(2, 2, 1, 1, 50, 4)
        self.test_proxy._planets[2] = Planet(15, 15, 2, 2, 50, 4)

        self.test_proxy._FindSize()

        assert self.test_proxy._size == [21, 21]
        assert self.test_proxy._offset == [2, 2]
