import pytest

from src import Fleet
from src import Planet
from src import Location


class TestFleet():
    @pytest.fixture
    def one_fleet(self, request):

        self.test_planet = Planet.Planet(0, 0, 1, 1, 50, 2)
        self.test_fleet = Fleet.Fleet(1, 1, 50, 5, 5, self.test_planet)

        def teardown():
            del self.test_fleet

        request.addfinalizer(teardown)
        return 'add test_fleet'

    def test_wrong_parameters(self):
        test_planet = Planet.Planet(0, 0, 1, 1, 50, 2)
        with pytest.raises(ValueError):
            Fleet.Fleet(1, 1, 50, 0, 0, test_planet)
        with pytest.raises(ValueError):
            Fleet.Fleet(1, 1, 50, 2, 2, test_planet,10)

    def test_get_in_range(self, one_fleet):
        test_list = (
                     Planet.Planet(0, 0, 1, 50, 1, 1),
                     Planet.Planet(1, 1, 2, 50, 1, 1),
                     Planet.Planet(2, 2, 3, 50, 2, 1),
                     Planet.Planet(3, 3, 4, 50, 2, 1),
                     Planet.Planet(4, 4, 5, 50, 2, 1)
                    )
        assert self.test_fleet.GetInRange(test_list) == {
                                                          5: test_list[4],
                                                         }

    def test_vision_range(self, one_fleet):
        assert self.test_fleet.VisionRange() == 2

    def test_destination_planet(self, one_fleet):
        assert self.test_fleet.DestinationPlanet() == self.test_planet

    def test_total_trip_length(self, one_fleet):
        assert self.test_fleet.TotalTripLength() == 8

    def test_turns_remaining(self, one_fleet):
        assert self.test_fleet.TurnsRemaining() == 8

    def test_source(self, one_fleet):
        assert type(self.test_fleet.Source()) == Location.Location

    def test_progress(self, one_fleet):
        assert self.test_fleet.Progress() == 0

    def test_tick(self, one_fleet):
        assert self.test_fleet.TurnsRemaining() == 8
        self.test_fleet.Tick()
        assert self.test_fleet.TurnsRemaining() == 7
        assert self.test_fleet.X() == 4.375
        assert self.test_fleet.Y() == 4.375

    def test_copy(self, one_fleet):
        temp = self.test_fleet.Copy()
        assert (temp  is not self.test_fleet)


