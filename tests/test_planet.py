import pytest
from src import Planet


class Test_Planet():
    def test_planet(self):
        arg = {
            'x': 0,
            'y': 0,
            'id': 1,
            'num_ships': 50,
            'owner': 1,
            'growth_rate': 2
        }
        test_planet = Planet.Planet(arg['x'], arg['y'], arg['id'],
                                    arg['num_ships'], arg['owner'],
                                    arg['growth_rate'])
        assert test_planet.X() == arg['x']
        assert test_planet.Y() == arg['y']
        assert test_planet.ID() == arg['id']
        assert test_planet.NumShips() == arg['num_ships']
        assert test_planet.Owner() == arg['owner']
        assert test_planet.GrowthRate() == arg['growth_rate']

    def test_vision_range(self):
        test_planet = Planet.Planet(0, 0, 1, 1, 50, 2)
        assert test_planet.VisionRange() == 5

    def test_copy(self):
        pass