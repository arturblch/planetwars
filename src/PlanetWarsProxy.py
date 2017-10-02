from .Fleet import Fleet
from .Planet import Planet
import uuid


class PlanetWarsProxy(object):
    NEUTRAL_PLAYER = "0"

    def __init__(self, gamestate=None):
        self._planets = {}
        self._fleets = {}
        self._tick = 0
        self._playerid = None
        self._winner = 0
        self._gameid = None
        self._orders = []
        self._size = [0, 0]
        self._offset = [0, 0]
        if (gamestate):
            self._ParseGameState(gamestate)

    def _ParsePlanet(self, tokens):
        p = Planet(
            float(tokens[1]),  # x
            float(tokens[2]),  # y
            int(tokens[3]),  # planet id
            tokens[4],  # owner id
            int(tokens[5]),  # num_ships
            int(tokens[6]))  # growth_rate
        self._planets[p.ID()] = p
        return p

    # def _ParseFleet(self, tokens):
    #     if len(tokens) != 8:
    #         return 0
    #     f = Fleet(
    #         int(tokens[1]),  # Fleet ID
    #         int(tokens[2]),  # Owner
    #         int(tokens[3]),  # NumShips
    #         int(tokens[4]),  # Source X
    #         int(tokens[5]),  # Source Y
    #         int(tokens[6]),  # Destination
    #         int(tokens[7]))  # Progress
    #     self._fleets[f.FleetID()] = f

    def _ParseGameState(self, state):
        lines = state.split("\n")

        for line in lines:
            line = line.split("#")[0]  # remove comments
            tokens = line.split(" ")
            if len(tokens) == 1:
                continue
            if tokens[0] == "P" and len(tokens) == 7:
                self._ParsePlanet(tokens)
            # elif tokens[0] == "F":            #useless
            #     self._ParseFleet(tokens)
            elif tokens[0] == "M":
                self._gameid = int(tokens[1])
                self._playerid = int(tokens[2])
                self._tick = int(tokens[3])
                self._winner = int(tokens[4])
        self._FindSize()

    def _FindSize(self):
        extent = [0, 0, 0, 0]
        for p in self._planets.values():
            if (p.Y() + p.GrowthRate() > extent[0]):
                extent[0] = p.Y() + p.GrowthRate()
            if (p.X() + p.GrowthRate() > extent[1]):
                extent[1] = p.X() + p.GrowthRate()
            if (p.Y() - p.GrowthRate() < extent[2]):
                extent[2] = p.Y() - p.GrowthRate()
            if (p.X() - p.GrowthRate() < extent[3]):
                extent[3] = p.X() - p.GrowthRate()
        self._size[0] = extent[1] - extent[3]
        self._size[1] = extent[0] - extent[2]

        if (extent[3] < 0):
            self._offset[0] = abs(extent[3])
        if (extent[2] < 0):
            self._offset[1] = abs(extent[2])

    def SetSize(self, size, offset):
        self._size = size
        self._offset = offset

    def SetPlayerId(self, playerid):
        self._playerid = playerid

    def GetSize(self):
        return self._size

    def GetOffset(self):
        return self._offset

    def PlayerID(self):
        return self._playerid

    def CurrentTick(self):
        return self._tick

    def _GetOrders(self):
        return self._orders

    def _ClearOrders(self):
        self._orders = []

    def _EndGame(self, winnerid):
        self._winner = winnerid

    def NumPlanets(self):
        return len(self._planets)

    def TotalShips(self):
        total = 0
        for planet in self.MyPlanets():
            total += planet.NumShips()
        for fleet in self.MyFleets():
            total += fleet.NumShips()

        return total

    def GetPlanet(self, planet_id):
        if (planet_id in self._planets):
            return self._planets[planet_id]
        else:
            return None

    def NumFleets(self):
        return len(self._fleets)

    def GetFleet(self, fleet_id):
        if (fleet_id in self._fleets):
            return self._fleets[fleet_id]
        else:
            return None

    def Planets(self):
        return self._planets.values()

    def MyPlanets(self):
        r = []
        for p in self._planets:
            planet = self._planets[p]
            if planet.Owner() == self._playerid:
                r.append(planet)
        return r

    def NeutralPlanets(self):
        r = []
        for p in self._planets:
            planet = self._planets[p]
            if planet.Owner() == PlanetWarsProxy.NEUTRAL_PLAYER:
                r.append(planet)
        return r

    def EnemyPlanets(self):
        r = []
        for p in self._planets:
            planet = self._planets[p]
            if ((planet.Owner() != self._playerid) and
                (planet.Owner() != PlanetWarsProxy.NEUTRAL_PLAYER)):
                r.append(planet)
        return r

    def NotMyPlanets(self):
        r = []
        for p in self._planets:
            planet = self._planets[p]
            if planet.Owner() != self._playerid:
                r.append(planet)
        return r

    def Fleets(self):
        return self._fleets.values()

    def MyFleets(self):
        r = []
        for f in self._fleets:
            fleet = self._fleets[f]
            if fleet.Owner() == self._playerid:
                r.append(fleet)
        return r

    def EnemyFleets(self):
        r = []
        for f in self._fleets:
            fleet = self._fleets[f]
            #we assume there are no neutral fleets
            if fleet.Owner() != self.PlayerID():
                r.append(fleet)
        return r
    #  == Save Function ==
    # def _ToString(self):
    #     s = ''
    #     s+= "M %d %d %d %d\n" % \
    #         (self._gameid, self._playerid, self._tick, self._winnerid)
    #     for p in self._planets:
    #         s += "P %f %f %d %d %d\n" % \
    #          (p.X(), p.Y(), p.Owner(), p.NumShips(), p.GrowthRate())
    #     for f in self._fleets:
    #         s += "F %d %d %d %d %d %d\n" % \
    #          (f.Owner(), f.NumShips(), f.SourcePlanet(), f.DestinationPlanet(), \
    #             f.TotalTripLength(), f.TurnsRemaining())
    #     return s

    def IssueOrder(self, source, destination_planet, num_ships):
        #is source a fleet or planet?
        num_ships = int(num_ships)
        if num_ships <= 0:
            raise ValueError("You must send 1 or more ships!")
        if (type(destination_planet) == Planet):
            dest = destination_planet
        else:
            dest = self.GetPlanet(destination_planet)
        if (not dest):
            raise ValueError(
                "You must pass a valid Planet as the destination!")
        if (type(source) == Fleet):
            f = source
            return self.FleetOrder(f, dest, num_ships)
        elif (type(source) == Planet):
            p = source
            return self.PlanetOrder(p, dest, num_ships)            
        else:
            raise ValueError("You must pass a fleet or planet or an ID.")

    def FleetOrder(self, source_fleet, destination_planet, num_ships):
        source_fleet.RemoveShips(num_ships)
        fleetid = uuid.uuid4()
        self._orders.append(('fleet', source_fleet.ID(), fleetid, num_ships,
                             destination_planet.ID()))
        return fleetid

    def PlanetOrder(self, source_planet, destination_planet, num_ships):
        source_planet.RemoveShips(num_ships)
        fleetid = uuid.uuid4()
        self._orders.append(('planet', source_planet.ID(), fleetid, num_ships,
                             destination_planet.ID()))
        return fleetid

    def _Update(self, pw, first_turn=False):
        if (not self._playerid):
            raise ValueError("No player id, can't determine what's in range!")

        planetsinview = {}
        fleetsinview = {}
        self._tick = pw.CurrentTick()

        if (first_turn):
            planets = pw.Planets()
            for planet in planets:
                planetsinview[planet.ID()] = planet  # View all planets at first step

        for my_entity in pw.MyPlanets(self._playerid) + pw.MyFleets(self._playerid):
            planetsinview.update(my_entity.GetInRange(pw.Planets()))
            fleetsinview.update(my_entity.GetInRange(pw.Fleets()))              # View all enttitys if range 

        for planet in self.MyPlanets():
            if (pw.GetPlanet(planet.ID()).Owner() != planet.Owner()):
                planetsinview[planet.ID()] = pw.GetPlanet(planet.ID())  # If my planet change owner in main PW

        for planet in planetsinview.values():
            self._planets[planet.ID()] = planet.Copy()
            self._planets[planet.ID()].VisionAge(0)                # Add planets in view

        # clear out the fleet list, if they aren't in view they disappear
        self._fleets = {}
        for fleet in fleetsinview.values():
            self._fleets[fleet.ID()] = fleet.Copy()
            self._fleets[fleet.ID()].VisionAge(0)               # Add fleets in view 

        for id, planet in self._planets.items():
            if id not in planetsinview:
                planet.VisionAge(planet.VisionAge() + 1)        # Change vision age if not in view
