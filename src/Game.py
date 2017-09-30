'''
Created on 23/03/2011

@author: Michael Jensen
'''
import sys
import pygame
import random
from pprint import pprint
from pygame.locals import *  #@UnusedWildImport


from .PlanetWars import PlanetWars
from .Logger import Logger






MAX_GAME_TICKS = 500

GAME_SIZE = (500, 500)
SCREEN_SIZE = (3 * GAME_SIZE[0], GAME_SIZE[1])
COLOUR = {
    "0": (200, 200, 200),
    "1": (255, 0, 0),
    "2": (0, 255, 0),
    "3": (0, 0, 255)
}
PLANET_MIN_R = 1
PLANET_FACTOR = 0.1
MARGIN = 20
DISPLAY = True

IMAGES = {}

PLANET_ADDRES = './planets/planet%d.png'
MAPS_ADDRES = './newmaps/%s.txt'
BACKGROUND_IMAGE = "./space.jpg"

class Drawer():


    def __init__(self, world, display,list_of_planets, background=None,clock = None, offset=(0, 0)):
        self.world = world
        self.display = display
        self.list_of_planets = list_of_planets
        self.background = background
        self.clock = clock
        self.offset = offset
        self.list_rand_planets = {}

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

        self.world_res = float(self.world_size[0]) / float(
                self.world_size[1])

        if self.world_res > self.display_res:
            self.display_offset[1] += int((self.display_size[1] - self.display_size[0] / self.world_res) / 2.0)
            self.display_size[1] = self.display_size[0] / self.world_res
        else:
            self.display_offset[0] += int((self.display_size[0] - self.display_size[1] * self.world_res) / 2.0)
            self.display_size[0] = self.display_size[1] * self.world_res

        self.background = pygame.transform.scale(self.background, (int(self.display_size[0]),
                                                                  int(self.display_size[1])) )
        self.factor = (float(self.display_size[0]) / float(self.world_size[0]))
        self.surf = pygame.Surface(self.display_size)


        for p in self.world.Planets():
            randPl = self.list_of_planets[p.ID()]
            plimg = pygame.image.load(PLANET_ADDRES % randPl)
            plimg = plimg.convert_alpha()
            self.list_rand_planets[p.ID()] = plimg

        self.has_fog = self.world.PlayerID() != 0
        self.fog = pygame.Surface(self.display_size, flags=SRCALPHA)

    def colorize(self, image, newColor):

        image = image.copy()
        # zero out RGB values
        image.fill(newColor + (255,), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        #image.fill(newColor[0:3], None, pygame.BLEND_RGB_ADD)

        return image

    def draw_planets(self):
        for p in self.world.Planets():
            radius = int((PLANET_MIN_R * self.factor) +
                         ((PLANET_FACTOR * self.factor) * p.GrowthRate()))
            screen_x = int(float(p.X() + self.world_offset[0]) * self.factor)
            screen_y = int(float(p.Y() + self.world_offset[1]) * self.factor)
            #pygame.draw.circle(self.surf, COLOUR[p.Owner()], (screen_x, screen_y), radius)
            plimg = self.list_rand_planets[p.ID()]
            plimg = pygame.transform.scale(plimg, (2*radius ,2*radius))
            plimg = self.colorize(plimg, COLOUR[p.Owner()])
            self.surf.blit(plimg, (screen_x - radius, screen_y-radius))
            if ((p.Owner() == self.world.PlayerID()) and self.has_fog):
                pygame.draw.circle(self.fog, (0, 0, 0, 0), (screen_x,
                                                            screen_y),
                                   int(p.VisionRange() * self.factor))
            text = pygame.font.Font(None, 20).render(
                str(p.NumShips()), False, (255,255,255))
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
        self.surf.fill((128, 128, 128, 0))
        self.surf.blit(self.background, (0,0))
        self.fog.fill((128, 128, 128, 0))
        self.draw_fleet()
        self.draw_planets()
        if (self.has_fog):
            self.surf.blit(self.fog, (0, 0), special_flags=BLEND_SUB)
        self.surf.blit(
            pygame.font.Font(None, 22).render(
                str(self.world.CurrentTick()), False, (255, 255, 255)), 
                                                      (20, 20))
        self.surf.blit(
            pygame.font.Font(None, 22).render(
                str(self.clock.get_fps()), False, (255, 255, 255)),
                            (self.display_size[0] - 20, self.display_size[1] - 20))
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

    p1Proxy = pw.MakeProxy("1", logger.p1log)
    p2Proxy = pw.MakeProxy("2", logger.p2log)
    fps = 4
    if show_gui:
        pygame.init()
        view = 'world'
        if view == 'all':
            window_size = SCREEN_SIZE
        else:
            window_size = GAME_SIZE

        screen = pygame.display.set_mode(window_size, 0, 32)
        background = pygame.image.load(BACKGROUND_IMAGE).convert_alpha()
        clock = pygame.time.Clock()
        paused = True
        list_of_planets = {p.ID():random.randint(1,18) for p in pw.Planets()}
        p1view = Drawer(p1Proxy, screen, list_of_planets, background, clock, )
        p2view = Drawer(p2Proxy, screen, list_of_planets, background, clock)
        pwview = Drawer(pw, screen, list_of_planets, background, clock)
        #allview = Drawer()
    else:
        paused = False

    #min_100_ships = lambda p, pw: 100
    #p1 = VariableAggressionPlayer(0.2, min_100_ships)
    #p2 = VariableAggressionPlayer(0.2, min_100_ships)
    

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
            # draw(p2Proxy, screen, background, )
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
        winner = p1.__module__.split('.')[1] # Player.BotName
    else:
        #p2 wins!
        winner = p2.__module__.split('.')[1]

    logger.result("Game {0}: {1} victory at turn {2} \n {3}: {4}, {5}: {6}".
                  format(game_id, winner,
                         pw.CurrentTick(), p1.__module__.split('.')[1],
                         p1Proxy.TotalShips(), p2.__module__.split('.')[1], p2Proxy.TotalShips()))
    logger.data("{0}:{1}:{2}:{3}:{4},{5}:{6},{7}".format(
        game_id, pw._gameid, winner,
        pw.CurrentTick(), p1.__module__.split('.')[1],
        p1Proxy.TotalShips(), p2.__module__.split('.')[1], p2Proxy.TotalShips()))
    return 1



if __name__ == '__main__':
    log = Logger('./Log/')
    try:
        #import the two players
        from .Players.VariableAggressionPlayer import VariableAggressionPlayer
        from .Players.Dave2Player import Dave2Player
        from .Players.Dave2Player_old import Dave2Player_old
        from .Players.ScoutPlayer import ScoutPlayer
        bot1 = Dave2Player() #your player!
        bot2 = Dave2Player_old()

        pw = PlanetWars(open(MAPS_ADDRES % sys.argv[1]).read(), logger=log.turn)
        do_game(1, log, bot1, bot2, pw, show_gui=True)
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    finally:
        log.flush()
