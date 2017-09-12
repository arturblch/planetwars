import sys

import pytest
from src import Location


def test_loc():
    test = Location.Location(1,2)
    assert test.X()==1 , 'X error'
    assert test.Y()==2 , 'Y error'
