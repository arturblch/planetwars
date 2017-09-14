# PlanetWars #
[![Build Status](https://travis-ci.org/arturblch/planetwars.svg?branch=master)](https://travis-ci.org/arturblch/planetwars)
[![Coverage Status](https://coveralls.io/repos/github/arturblch/planetwars/badge.svg?branch=master)](https://coveralls.io/github/arturblch/planetwars?branch=master)
 
 
 PlanetWars is a simple turn based strategy game based on Galcon and the Google AI Challenge.It has been modified to include rerouting fleets in flight and fog of war.
## 1.  Gameplay
PlanetWars takes place in a “system” of planets, which are statically located in a 2-dimensional space.
Each player begins the game controlling at least one planet with some ships on it. The player can issue
commands to the planets and fleets that they control, capturing more planets and increasing their
army size. Each turn, a planet under a player’s control will produce more ships, with some planets
producing more ships than others.

## 2.  Software Structure
In order to facilitate deception, PlanetWars has a fog of war. This prevents each player from seeing
their opponent’s activities when they aren’t nearby. To prevent players from cheating, each player is
given a facade object each turn which can be queried for information about the game state. The
information that each facade yields will represent the parts of the game that aren’t covered by fog of
war. For the parts of the game that are out of vision range, the facade will contain old or possible no
information. When planets are out of range, the facade will contain the last known state of that planet. Growth
and control will not be visible through the facade, but the planet will still be there. When a fleet
moves out of range, the facade forgets about it. Fleets that are accessible through the facade object
are guaranteed to be within vision range, and fleets that are out of vision are guaranteed to not be
accessible through the facade.

## 3. Making Players
### 3.1 Player Classes
Players in PlanetWars are required to implement a DoTurn method. This method will be called each
turn by the game engine to give players a chance to issue orders. This method must take a single object
parameter. It will be passed a PlanetWars object which contains a version of the game state, filtered
for your player program. During your turn, you can query the PlanetWars object for information
about the game, log messages to a file (useful for debugging/analysis) and issue orders to the fleets
and planets under your control.
Your player class should extend from the BasePlayer class. This class has a basic constructor that
assigns an ID to the player class. If you require some code to be run when your player is instantiated,
make sure you call the BasePlayer’s constructor.
