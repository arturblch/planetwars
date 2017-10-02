import pytest
from src.PlanetWarsProxy import PlanetWarsProxy
from src.PlanetWars import PlanetWars
from src.Planet import Planet
from src.Fleet import Fleet
import sys


class TestPlanetWarsProxy():
    @pytest.fixture
    def base_setup(self):
        self.test_proxy = PlanetWarsProxy()

    @pytest.fixture
    def set_planets(self):
        self.test_proxy._planets[1] = Planet(2, 2, 1, '1', 50, 4)
        self.test_proxy._planets[2] = Planet(15, 15, 2, '2', 50, 4)
        self.test_proxy._planets[3] = Planet(4, 14, 3, '0', 50, 4)

    @pytest.fixture
    def set_fleets(self):
        test_planet = Planet(0, 0, 1, 1, 50, 2)
        self.test_proxy._fleets[1] = Fleet(1, '1', 50, 5, 5, test_planet)
        self.test_proxy._fleets[2] = Fleet(2, '2', 50, 5, 5, test_planet)

    @pytest.fixture
    def main_proxy(self):
        self.main_pw = PlanetWars()
        self.main_pw._planets[1] = Planet(2, 2, 1, '1', 50, 4)
        self.main_pw._planets[1].VisionRange = lambda : 4  # mock range func
        self.main_pw._planets[2] = Planet(15, 15, 2, '2', 50, 4)
        self.main_pw._planets[3] = Planet(2, 5, 3, '0', 50, 4)

        test_planet = Planet(0, 0, 2, '2', 50, 2)
        self.main_pw._fleets[1] = Fleet(1, '1', 50, 2, 3, test_planet)
        self.main_pw._fleets[1].VisionRange = lambda : 2  # mock range func
        self.main_pw._fleets[2] = Fleet(2, '2', 50, 14, 15, test_planet)
        self.main_pw._fleets[3] = Fleet(3, '0', 50, 2, 4, test_planet)
        
        self.proxy = self.main_pw.MakeProxy('1') # has _update func

    def test_parse_planet(self, base_setup):
        test_planet = 'P 2 2 1 1 50 4'.split()
        result = self.test_proxy._ParsePlanet(test_planet)
        assert type(result) == Planet

    def test_parse_game_state(self, base_setup):
        test_map = 'M 1 0 0 0\n'\
                     + 'P 2 2 1 1 50 4\n'\
                     + 'P 15 15 2 2 50 4\n'\
                     + 'P 4 14 3 0 50 4\n'\
                     + 'G 123 asd\n'
        print(test_map.split('\n'))
        self.test_proxy._ParseGameState(test_map)
        assert self.test_proxy._planets[1] == Planet(2, 2, 1, '1', 50, 4)
        assert self.test_proxy._planets[2] == Planet(15, 15, 2, '2', 50, 4)
        assert self.test_proxy._planets[3] == Planet(4, 14, 3, '0', 50, 4)

    def test_find_size(self, base_setup, set_planets):
        self.test_proxy._FindSize()

        assert self.test_proxy._size == [21, 21]
        assert self.test_proxy._offset == [2, 2]

    def test_set_size(self, base_setup):
        self.test_proxy.SetSize([5, 5], [6, 6])
        assert self.test_proxy._size == [5, 5]
        assert self.test_proxy._offset == [6, 6]

    def test_set_player_id(self, base_setup):
        self.test_proxy.SetPlayerId('2')
        assert self.test_proxy._playerid == '2'

    def test_get_size(self, base_setup):
        self.test_proxy._size = [5, 5]
        assert self.test_proxy.GetSize() == [5, 5]

    def test_get_offset(self, base_setup):
        self.test_proxy._offset = [5, 5]
        assert self.test_proxy.GetOffset() == [5, 5]

    def test_player_id(self, base_setup):
        self.test_proxy._playerid = '0'
        assert self.test_proxy.PlayerID() == '0'

    def test_currentTick(self, base_setup):
        self.test_proxy._tick = 5
        assert self.test_proxy.CurrentTick() == 5

    def test_get_orders(self, base_setup): 
        self.test_proxy._orders.append((1,2,3,4))
        assert self.test_proxy._GetOrders() == [(1,2,3,4)]

    def test_clear_orders(self, base_setup): 
        self.test_proxy._orders.append((1,2,3,4))
        self.test_proxy._ClearOrders()
        assert self.test_proxy._orders == []

    def test_end_game(self, base_setup):
        self.test_proxy._EndGame(123)
        assert self.test_proxy._winner == 123

    def test_num_planets(self, base_setup, set_planets):
        assert self.test_proxy.NumPlanets() == 3

    def test_num_fleets(self, base_setup, set_fleets):
        assert self.test_proxy.NumFleets() == 2

    def test_total_ships(self, base_setup, set_planets, set_fleets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.TotalShips() == 100

    def test_get_planet(self, base_setup, set_planets):
        assert self.test_proxy.GetPlanet(1) == self.test_proxy._planets[1]
        assert self.test_proxy.GetPlanet(-1) == None

    def test_get_fleet(self, base_setup, set_fleets):
        assert self.test_proxy.GetFleet(1) == self.test_proxy._fleets[1]
        assert self.test_proxy.GetFleet(-1) == None

    def test_planets(self, base_setup, set_planets):
        assert list(self.test_proxy.Planets()) == [self.test_proxy._planets[1],
                                                   self.test_proxy._planets[2],
                                                   self.test_proxy._planets[3]]

    def test_fleets(self, base_setup, set_fleets):
        assert list(self.test_proxy.Fleets()) == [self.test_proxy._fleets[1],
                                                  self.test_proxy._fleets[2]]

    def test_my_planets(self, base_setup, set_planets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.MyPlanets() == [self.test_proxy._planets[1]]

    def test_neutral_my_planets(self, base_setup, set_planets):
        assert self.test_proxy.NeutralPlanets() == [self.test_proxy._planets[3]]

    def test_enemy_planets(self, base_setup, set_planets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.EnemyPlanets() == [self.test_proxy._planets[2]]

    def test_not_my_planets(self, base_setup, set_planets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.NotMyPlanets() == [self.test_proxy._planets[2],
                                                  self.test_proxy._planets[3]]

    def test_my_fleets(self, base_setup, set_fleets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.MyFleets() == [self.test_proxy._fleets[1]]

    def test_enemy_fleets(self, base_setup, set_fleets):
        self.test_proxy._playerid = '1'
        assert self.test_proxy.EnemyFleets() == [self.test_proxy._fleets[2]]

    def test_fleet_order(self, base_setup):
        import uuid
        destin_test = Planet(2, 2, 1, '1', 50, 4)
        test_planet = Planet(0, 0, 2, '2', 50, 2)
        sourse_test = Fleet(1, '1', 50, 5, 5, test_planet)
        self.test_proxy.FleetOrder(sourse_test, destin_test, 50)
        (name, source, fleetid, num, dest) = self.test_proxy._orders[0]
        assert name == 'fleet'
        assert source == sourse_test.ID()
        assert type(fleetid) == type(uuid.uuid4())
        assert num == 50
        assert dest == destin_test.ID()

    def test_planet_order(self, base_setup):
        import uuid
        destin_test = Planet(2, 2, 1, '1', 50, 4)
        sourse_test = Planet(2, 2, 2, '1', 50, 4)
        self.test_proxy.PlanetOrder(sourse_test, destin_test, 50)
        (name, source, fleetid, num, dest) = self.test_proxy._orders[0]
        assert name == 'planet'
        assert source == sourse_test.ID()
        assert type(fleetid) == type(uuid.uuid4())
        assert num == 50
        assert dest == destin_test.ID()

    def test_issue_order(self, base_setup):
        destin_test = Planet(2, 2, 1, '1', 50, 4)
        test_planet = Planet(0, 0, 2, '2', 50, 2)
        sourse_fleet = Fleet(1, '1', 50, 5, 5, test_planet)
        with pytest.raises(ValueError):
            self.test_proxy.IssueOrder(sourse_fleet, destin_test, 0)
        with pytest.raises(ValueError):
            self.test_proxy.IssueOrder(sourse_fleet, '999', 10)
        with pytest.raises(ValueError):
            self.test_proxy.IssueOrder(123, destin_test, 10)
        self.test_proxy.IssueOrder(sourse_fleet, destin_test, 10)
        (name, source, fleetid, num, dest) = self.test_proxy._orders[0]
        assert name == 'fleet'
        assert source == sourse_fleet.ID()
        assert num == 10
        assert dest == destin_test.ID()

    def test_update_error(self, base_setup):
        pw = PlanetWarsProxy()
        with pytest.raises(ValueError):
            self.test_proxy._Update(pw)

    def test_update(self, main_proxy):
        # check updating my planet
        self.main_pw._planets[1].RemoveShips(15)
        self.proxy._Update(self.main_pw)
        assert self.proxy._planets[1] is not self.main_pw._planets[1]  # Security
        assert self.proxy._planets[1].NumShips() == 35

        # check planets in vision
        self.main_pw._planets[3].RemoveShips(15)
        self.proxy._Update(self.main_pw)
        assert self.proxy._planets[3] is not self.main_pw._planets[3]  # Security
        assert self.proxy._planets[3].NumShips() == 35

        # check not updating not in vision planets
        self.main_pw._planets[2].RemoveShips(15)
        self.proxy._Update(self.main_pw)
        assert self.proxy._planets[2].NumShips() == 50

        # check fleet in vision
        self.main_pw._fleets[3].RemoveShips(15)
        self.proxy._Update(self.main_pw)
        assert self.proxy._fleets[3] is not self.main_pw._fleets[3]  # Security
        assert self.proxy._fleets[3].NumShips() == 35

        # chek fleet not in vision
        self.main_pw._fleets[2].RemoveShips(15)
        self.proxy._Update(self.main_pw)
        assert self.proxy._fleets.get(2) == None

        # check change defit planet
        self.main_pw._planets[1].Owner('2')
        self.proxy._Update(self.main_pw)
        assert self.proxy._planets[1].Owner() == '2'

    def test_change_vision_age(self, main_proxy):
        assert self.proxy._planets[2].VisionAge() == 0 
        self.proxy._Update(self.main_pw)
        assert self.proxy._planets[2].VisionAge() == 1