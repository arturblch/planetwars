'''
Created on 23/03/2011

@author: Michael Jensen
'''
import sys
import pygame

from pygame.locals import *  #@UnusedWildImport

#from Players import *
from PlanetWars import PlanetWars
MAX_GAME_TICKS = 500

GAME_SIZE = (500, 500)
SCREEN_SIZE = (3 * GAME_SIZE[0], GAME_SIZE[1])
COLOUR = {
    "0": (200, 200, 200),
    "1": (255, 0, 0),
    "2": (0, 0, 255),
    "3": (0, 255, 0)
}
PLANET_MIN_R = 0.85
PLANET_FACTOR = 0.05
MARGIN = 20
DISPLAY = True


class Drawer():

    MARGIN = 20
    PLANET_MIN_R = 0.85
    PLANET_FACTOR = 0.05
    COLOUR = {
        "0": (200, 200, 200),
        "1": (255, 0, 0),
        "2": (0, 0, 255),
        "3": (0, 255, 0)
    }

    def __init__(self, world, display, background=None, offset=(0, 0)):
        self.world = world
        self.display = display
        self.background = background
        self.offset = offset

        self.display_size = []
        self.display_offset = []
        self.display_res = 0

        self.world_size = []
        self.world_offset = []
        self.world_res = 0
        self.factor = 0

        self.has_fog = False
        self.fog = None
        self.surf = None

        self._init_params()

    def _init_params(self):
        self.display_size = [
            self.display.get_size()[0] - (MARGIN * 2),
            self.display.get_size()[1] - (MARGIN * 2)
        ]
        self.display_offset = [
            self.offset[0] + MARGIN, self.offset[1] + MARGIN
        ]
        self.display_res = float(self.display_size[0]) / float(
            self.display_size[1])

        self.world_size = self.world.GetSize()
        self.world_offset = self.world.GetOffset()

        if self.world_size[1] == 0:
            pass
        else:
            self.world_res = float(self.world_size[0]) / float(
                self.world_size[1])

        if self.world_res > self.display_res:
            self.display_offset[1] += int(self.display_size[1] *
                                          (1 - 1 / self.world_res) / 2.0)
            self.display_size[1] = self.display_size[0] / self.world_res
        else:
            self.display_offset[0] += int(self.display_size[0] *
                                          (1 - self.world_res) / 2.0)
            self.display_size[0] = self.display_size[0] * self.world_res

        self.factor = (float(self.display_size[0]) / float(self.world_size[0]))
        self.surf = pygame.Surface(self.display_size)
        if (self.background):
            self.surf.blit(self.background, (0, 0))
        self.has_fog = self.world.PlayerID() != 0
        if (self.has_fog):
            self.fog = pygame.Surface(self.display_size, flags=SRCALPHA)
            self.fog.fill((128, 128, 128, 0))

    def draw_planets(self):
        for p in self.world.Planets():
            screen_x = int(float(p.X() + self.world_offset[0]) * self.factor)
            screen_y = int(float(p.Y() + self.world_offset[1]) * self.factor)
            radius = int((PLANET_MIN_R * self.factor) +
                         ((PLANET_FACTOR * self.factor) * p.GrowthRate()))
            pygame.draw.circle(self.surf, COLOUR[p.Owner()],
                               (screen_x, screen_y), radius)
            if ((p.Owner() == self.world.PlayerID()) and self.has_fog):
                pygame.draw.circle(self.fog, (0, 0, 0, 0), (screen_x,
                                                            screen_y),
                                   int(p.VisionRange() * self.factor))
            text = pygame.font.Font(None, 20).render(
                str(p.NumShips()), False, (0, 0, 0))
            text_pos = (screen_x - (text.get_width() / 2),
                        screen_y - (text.get_height() / 2))
            self.surf.blit(text, text_pos)
            pid = pygame.font.Font(None, 18).render(
                str(p.ID()), False, (255, 255, 255))
            self.surf.blit(pid, (screen_x - radius, screen_y - radius))

    def draw_fleet(self):
        for f in self.world.Fleets():
            screen_x = int(float(f.X() + self.world_offset[0]) * self.factor)
            screen_y = int(float(f.Y() + self.world_offset[1]) * self.factor)
            text = pygame.font.Font(None, 16).render(
                str(f.NumShips()), False, COLOUR[f.Owner()])
            text_pos = (screen_x - (text.get_width() / 2),
                        screen_y - (text.get_height() / 2))
            self.surf.blit(text, text_pos)
            if ((f.Owner() == self.world.PlayerID()) and self.has_fog):
                pygame.draw.circle(self.fog, (0, 0, 0, 0), (screen_x,
                                                            screen_y),
                                   int(f.VisionRange() * self.factor))

    def draw(self):
        self.surf = pygame.Surface(self.display_size)
        self.fog = pygame.Surface(self.display_size, flags=SRCALPHA)
        self.fog.fill((128, 128, 128, 0))
        if (self.background):
            self.surf.blit(self.background, (0, 0))
        self.draw_fleet()
        self.draw_planets()

        if (self.has_fog):
            self.surf.blit(self.fog, (0, 0), special_flags=BLEND_SUB)
        self.surf.blit(
            pygame.font.Font(None, 22).render(
                str(self.world.CurrentTick()), False, (255, 255, 255)), (20,
                                                                         20))
        self.display.blit(self.surf, self.display_offset)
        pygame.display.update()


def do_game(
        game_id,  # int
        logger,  # Logger()
        p1,  # BasePlayer()
        p2,  # BasePlayer()
        pw,  # PlanetWars()
        show_gui=False,  # bool
):

    #we want to:
    #  - Load the map
    #  - instantiate two players (objects that respond to player.DoTurn(PlanetWars)
    # (we'll substitute a "real" planetwars object above with a proxy for each
    #  player. This proxy will have an output queue of commands rather than dealing with
    #  stdio)
    #  - instantiate two proxies, which will remember what the player knows,
    #    rather than the actual state of the game.

    #then, while not [victory conditions]
    #  - get an array of moves from p1's proxy world
    #  - get an array of moves from p2's proxy world
    #  - apply the moves to the world
    #  - update each proxy with the real world
    #  - render the current state
    #  - pause for framerate?

    if show_gui:
        pygame.init()
        view = 'world'
        if view == 'all':
            window_size = SCREEN_SIZE
        else:
            window_size = GAME_SIZE

        screen = pygame.display.set_mode(window_size, 0, 32)
        background = pygame.image.load("../space.jpg").convert_alpha()
        clock = pygame.time.Clock()
        paused = True
    else:
        paused = False

    p1Proxy = pw.MakeProxy("1", logger.p1log)
    p2Proxy = pw.MakeProxy("2", logger.p2log)
    fps = 4
    #min_100_ships = lambda p, pw: 100
    #p1 = VariableAggressionPlayer(0.2, min_100_ships)
    #p2 = VariableAggressionPlayer(0.2, min_100_ships)
    p1view = Drawer(p1Proxy, screen, background)
    p2view = Drawer(p2Proxy, screen, background)
    pwview = Drawer(pw, screen, background)


    while pw.IsAlive(p1Proxy.PlayerID()) and \
          pw.IsAlive(p2Proxy.PlayerID()) and \
          pw.CurrentTick() < MAX_GAME_TICKS:
        onestep = False
        if show_gui:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == KEYDOWN:
                    if event.key == K_p:
                        paused = not paused
                    elif (event.key == K_PLUS) or (event.key == K_EQUALS):
                        fps = fps + 1
                    elif event.key == K_MINUS:
                        fps = fps - 1
                        if fps < 1: fps = 1
                    elif event.key == K_n:
                        onestep = True
                    elif event.key == K_a:
                        if (view != 'all'):
                            screen = pygame.display.set_mode(
                                SCREEN_SIZE, 0, 32)
                        view = 'all'
                    elif event.key == K_e:
                        if (view != 'world'):
                            screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
                        view = 'world'
                    elif event.key == K_1:
                        if (view != 'p1'):
                            screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
                        view = 'p1'
                    elif event.key == K_2:
                        if (view != 'p2'):
                            screen = pygame.display.set_mode(GAME_SIZE, 0, 32)
                        view = 'p2'
            if (view == 'world'):
                pwview.draw()
            elif (view == 'p1'):
                p1view.draw()
            elif (view == 'p2'):
                p2view.draw()
            elif (view == 'all'):
                pass
            # draw(p1Proxy, screen,background,(-GAME_SIZE[0],0))
            # draw(pw, screen, background, (0,0))
            # draw(p2Proxy, screen, background, (GAME_SIZE[0], 0))
            time_passed = clock.tick(fps)

        if ((not paused) or onestep):
            p1.DoTurn(p1Proxy)
            p2.DoTurn(p2Proxy)
            pw.ProcessOrders(p1Proxy.PlayerID(), p1Proxy._GetOrders())
            pw.ProcessOrders(p2Proxy.PlayerID(), p2Proxy._GetOrders())

            p1Proxy._ClearOrders()
            p2Proxy._ClearOrders()

            pw.Tick()

            p1Proxy._Update(pw)
            p2Proxy._Update(pw)

    if p1Proxy.TotalShips() == p2Proxy.TotalShips():
        #tie
        winner = "no"
    elif p1Proxy.TotalShips() > p2Proxy.TotalShips():
        #p1 wins!
        winner = p1.id
    else:
        #p2 wins!
        winner = p2.id

    logger.result("Game {0}: {1} victory at turn {2} - {3}: {4}, {5}: {6}".
                  format(game_id, winner,
                         pw.CurrentTick(), p1.id,
                         p1Proxy.TotalShips(), p2.id, p2Proxy.TotalShips()))
    logger.data("{0}:{1}:{2}:{3}:{4},{5}:{6},{7}".format(
        game_id, pw._gameid, winner,
        pw.CurrentTick(), p1.id,
        p1Proxy.TotalShips(), p2.id, p2Proxy.TotalShips()))


from Logger import Logger

if __name__ == '__main__':
    log = Logger('./%s.log')
    try:
        #import the two players
        from Players.VariableAggressionPlayer import VariableAggressionPlayer
        from Players.PredictingPlayer import PredictingPlayer
        from Players.ScoutPlayer import ScoutPlayer
        bot1 = PredictingPlayer()  #your player!
        bot2 = ScoutPlayer()

        pw = PlanetWars(open(sys.argv[1]).read(), logger=log.turn)
        do_game(1, log, bot1, bot2, pw, show_gui=True)
    except KeyboardInterrupt:
        print 'ctrl-c, leaving ...'
    finally:
        log.flush()
