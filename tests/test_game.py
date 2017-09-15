import pytest
from src import Game
from src.Logger import Logger
from src.PlanetWars import PlanetWars

class TestGame():
    def setup(self):
        self.log = Logger('./%s.log')
        try:
            #import the two players
            from src.Players.VariableAggressionPlayer import VariableAggressionPlayer
            from src.Players.Dave2Player import Dave2Player
            from src.Players.Dave2Player_old import Dave2Player_old
            from src.Players.ScoutPlayer import ScoutPlayer
            self.bot1 = Dave2Player() #your player!
            self.bot2 = Dave2Player_old()

            test_map = '''M 1 0 0 0
                          P 10 10 1 1 119 4
                          P 10 20 2 0 100 5
                          P 20 10 3 0 100 5
                          P 20 20 4 2 119 4
                       '''
            self.pw = PlanetWars(test_map, logger=self.log.turn)
        except KeyboardInterrupt:
            print('ctrl-c, leaving ...' )

    def test_do_game(self):
        Game.do_game(1, self.log, self.bot1, self.bot2, self.pw)