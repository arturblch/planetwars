import sys

import pytest
from src import Location
from src import Entity


class Test_Location():
    def test_location_coordinats(self):
        location = Location.Location(1, 2)
        assert location.X() == 1, 'Location X error'
        assert location.Y() == 2, 'Location Y error'

    def test_location_distance_to(self):
        location1 = Location.Location(0, 0)
        location2 = Location.Location(3, 4)
        assert location1.DistanceTo(location2) == 5, 'Location Distance error'


class Test_Entity():
    @pytest.fixture
    def one_entity(self, request):
        self.test_entity = Entity.Entity(1, 2, 34, 50, 1)

        def teardown():
            del self.test_entity

        request.addfinalizer(teardown)
        return 'add test_entity'

    @pytest.fixture
    def tow_entity(self, request):
        self.test_entity1 = Entity.Entity(0, 0, 1, 50, 1)
        self.test_entity2 = Entity.Entity(3, 4, 1, 50, 1)

        def teardown():
            del self.test_entity1
            del self.test_entity2

        request.addfinalizer(teardown)
        return 'add test_entity1 and test_entity2'

    def test_location_coordinats(self, one_entity):
        assert type(self.test_entity.Location()) == \
                    Location.Location, 'Entity Location error'
        assert self.test_entity.X() == 1, 'Entity X error'
        assert self.test_entity.Y() == 2, 'Entity Y error'

    def test_entity_distance_to(self, tow_entity):
        assert self.test_entity1.DistanceTo(
            self.test_entity2) == 5, 'Entity Distance error'

    def test_id(self, one_entity):
        assert self.test_entity.ID() == 34, 'Entity ID error'

    def test_num_ships(self, one_entity):
        assert self.test_entity.NumShips() == 50, 'Entity NumShips error'
        assert self.test_entity.NumShips(
            49) == 49, 'Entity NumShips with num error'
        # with pytest.raises(ValueError):
        #     self.test_entity.NumShips(-1)

    def test_remove_ships(self, one_entity):
        self.test_entity.RemoveShips(1)
        assert self.test_entity.NumShips() == 49, 'Entity RemoveShips with '\
                                                + 'nagetive error'
        with pytest.raises(ValueError):
            self.test_entity.RemoveShips(-1)
        self.test_entity.NumShips(1)    
        with pytest.raises(ValueError):
            self.test_entity.RemoveShips(2)

    def test_add_ships(self, one_entity):
        self.test_entity.AddShips(1)
        assert self.test_entity.NumShips() == 51, 'Entity AddShips with '\
                                                + 'nagetive error'
        with pytest.raises(ValueError):
            self.test_entity.AddShips(-1)

    def test_owner(self, one_entity):
        assert self.test_entity.Owner() == 1, 'Entity Owner error'
        assert self.test_entity.Owner(2) == 2, 'Entity Owner with num error'

    def test_vision_range(self, one_entity):
        with pytest.raises(NotImplementedError):
            self.test_entity.VisionRange()

    def test_tick(self, one_entity):
        with pytest.raises(NotImplementedError):
            self.test_entity.Tick()

    def test_vision_age(self, one_entity):
        assert self.test_entity.VisionAge() == 99999, 'Entity VisionAge error'
        assert self.test_entity.VisionAge(2) == 2, 'Entity VisionAge with '\
                                                 + 'num error'

    def test_is_in_vision(self, one_entity):
        assert self.test_entity.IsInVision() == False, 'Entity IsInVision '\
                                                     + 'age != 0 error'
        self.test_entity.VisionAge(0)
        assert self.test_entity.IsInVision() == True, 'Entity IsInVision '\
                                                     + 'age = 0 error'

    def test_get_in_range(self, one_entity):
        test_list = (
                     Entity.Entity(0, 0, 1, 50, 1),
                     Entity.Entity(1, 1, 2, 50, 1),
                     Entity.Entity(2, 2, 3, 50, 2),
                     Entity.Entity(3, 3, 4, 50, 2),
                     Entity.Entity(4, 4, 5, 50, 2)
                    )
        self.test_entity.VisionRange = lambda : 2 #mock
        assert self.test_entity.GetInRange(test_list) == {
                                                          2: test_list[1],
                                                          3: test_list[2]
                                                         }


# def GetInRange(self, list):
