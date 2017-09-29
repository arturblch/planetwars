import pytest
from src.PlanetWarsProxy import PlanetWarsProxy
from src.Planet import Planet
from src.Fleet import Fleet
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

    def test_set_size(self):
        self.test_proxy.SetSize([5,5],[6,6])
        assert self.test_proxy._size == [5, 5]
        assert self.test_proxy._offset == [6, 6]

    def test_get_size(self):
        self.test_proxy._size = [5,5]
        assert self.test_proxy.GetSize() == [5, 5]

    def test_get_offset(self):
        self.test_proxy._offset = [5,5]
        assert self.test_proxy.GetOffset() == [5, 5]

    def test_num_planets(self):
        self.test_proxy._planets[1] = Planet(2, 2, 1, 1, 50, 4)
        self.test_proxy._planets[2] = Planet(15, 15, 2, 2, 50, 4)

        assert self.test_proxy.NumPlanets() == 2


    def test_num_fleets(self):
        test_planet = Planet(0, 0, 1, 1, 50, 2)
        self.test_proxy._fleets[1] = Fleet(1, 1, 50, 5, 5, test_planet)
        self.test_proxy._fleets[2] = Fleet(2, 2, 50, 5, 5, test_planet)

        assert self.test_proxy.NumFleets() == 2

    def test_total_ships(self):
        self.test_proxy._playerid = 2
        self.test_proxy._planets[1] = Planet(2, 2, 1, 1, 50, 4)
        self.test_proxy._planets[2] = Planet(15, 15, 2, 2, 50, 4)
        test_planet = Planet(0, 0, 1, 1, 50, 2)
        self.test_proxy._fleets[1] = Fleet(1, 1, 50, 5, 5, test_planet)
        self.test_proxy._fleets[2] = Fleet(2, 2, 50, 5, 5, test_planet)

        assert self.test_proxy.TotalShips() == 100

    def test_get_planet(self):
        pass

    def test_get_fleet(self):
        pass

    def test_planets(self):
        test_planet1 = Planet(2, 2, 1, 1, 50, 4)
        test_planet2 = Planet(15, 15, 2, 2, 50, 4)

        self.test_proxy._planets[1] = test_planet1
        self.test_proxy._planets[2] = test_planet2
        assert list(self.test_proxy.Planets()) == [test_planet1, test_planet2] 

    def test_fleets(self):
        test_planet = Planet(0, 0, 1, 1, 50, 2)
        test_fleet1 = Fleet(1, 1, 50, 5, 5, test_planet)
        test_fleet2 = Fleet(2, 2, 50, 5, 5, test_planet)
        self.test_proxy._fleets[1] = test_fleet1
        self.test_proxy._fleets[2] = test_fleet2

        assert list(self.test_proxy.Fleets()) == [test_fleet1, test_fleet2]

    def test_my_planets(self):
        self.test_proxy._playerid = 1
        self.test_proxy._planets[1] = Planet(2, 2, 1, 1, 50, 4)
        self.test_proxy._planets[2] = Planet(15, 15, 2, 2, 50, 4)
        assert self.test_proxy.MyPlanets() == [self.test_proxy._planets[1]]

    def test_enemy_planets(self):
        pass

    def test_not_my_planets(self):
        pass

    def test_not_my_planets(self):
        pass

    def test_my_fleets(self):
        pass

    def test_enemy_fleets(self):
        pass