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


    def test_get_in_range(self):
        pass

    def test_vision_range(self, one_fleet):
        assert self.test_fleet.VisionRange() == 2

    def test_destination_planet(self, one_fleet):
        assert self.test_fleet.DestinationPlanet() == self.test_planet

    def test_total_trip_length(self, one_fleet):
        assert self.test_fleet.TotalTripLength() == 8

    def test_turns_remaining(self, one_fleet):
        assert self.test_fleet.TurnsRemaining() == 8

    def test_progress(self, one_fleet):
        assert self.test_fleet.Progress() == 0

    

