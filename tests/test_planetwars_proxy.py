import pytest
from src.PlanetWarsProxy import PlanetWarsProxy
import sys


class TestPlanetWarsProxy():
    def setup(self):
        self.test_proxy = PlanetWarsProxy()

    def test_parse_game_state(self):
        test_map = 'M 1 0 0 0\n'\
                     + 'P 10 10 1 1 119 4\n'\
                     + 'P 10 20 2 0 100 5\n'\
                     + 'P 20 10 3 0 100 5\n'\
                     + 'P 20 20 4 2 119 4\n'
        self.test_proxy._ParseGameState(test_map)

        