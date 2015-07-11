from core.player import Player
from core.board import Board
from core.warrior import Warrior
from core.king import King
from core.peasant import Peasant
from core.ship import Ship
from core.building import Building
from core.battle import Battle

GARDEN_INCOME = 1
PEASANT_PRICE = 2
WARRIOR_PRICE = 5
SHIP_PRICE = 25


class Game:

    def __init__(self,):
        self.board = Board()
        self.players = [Player('0'), Player('1')]
        self.turn = 0
        self.songs = {1: 'Birth',
                      2: 'Death',
                      3: 'Resistance',
                      4: 'Reign',
                      5: 'Ascent',
                      6: 'Tirany',
                      7: 'the Mysteries'}
        self.buildings = {'Birth': ['Garden', 'House'],
                          'Death': [],
                          'Resistance': ['Thorn wall', 'Barracks'],
                          'Reign': ['Bridge'],
                          'Ascent': ['Harbor', 'Library', 'Statue'],
                          'Tirany': ['Prison', 'Rebel camp'],
                          'the Mysteries': ['Shrine']}
        self.setupFigures()
        self.loosers = None

    def possibleSongs(self, island):
        songsBits = self.board.possibleSongs(island, self.currentPlayer())
        songKeys = self.songs.keys()
        return [self.songs[key] for key in songKeys if key & songsBits == key]

    def possibleBuildings(self, island):
        songs = self.possibleSongs(island)
        buildings = []
        for song in songs:
            for building in self.buildings[song]:
                buildings.append(building)
        return buildings

    def build(self, building, field):
        if field.figure != None:
            return False
        building = Building(building, field)
        player = self.currentPlayer()
        if building.price <= player.resources:
            player.buildings.append(building)
            field.put(building)
            player.resources -= building.price
            return building
        return False

    def setupFigures(self):
        for player in self.players:
            island = None
            if player.color == '0':
                island = self.board.islands[-3]
            else:
                # island = self.board.islands[-2]
                island = self.board.islands[10]

            field = island.fields[0]
            field.put(King(field, player))
            player.figures.append(field.figure)
            field = island.fields[1]
            field.put(Warrior(field, player))
            player.figures.append(field.figure)
            field = island.fields[2]
            field.put(Peasant(field, player))
            player.figures.append(field.figure)
            field = island.bay
            field.put(Ship(field, player))
            player.figures.append(field.figure)

    def __unfreezeFigures(self, player):
        for figure in player.figures:
            figure.hasMoved = False

    def currentPlayer(self):
        return self.players[self.turn]

    def newBattle(self):
        black = self.players[self.turn]
        white = self.players[self.turn ^ 1]
        return Battle(black, white)

    def giveBirthToPeasant(self, field):
        player = self.currentPlayer()
        if player.resources >= PEASANT_PRICE:
            peasant = Peasant(field, player)
            field.put(peasant)
            player.resources -= PEASANT_PRICE
            player.figures.append(peasant)
            return peasant
        return False

    def giveBirthToWarrior(self, field):
        player = self.currentPlayer()
        if player.resources >= WARRIOR_PRICE:
            warrior = Warrior(field, player)
            field.put(warrior)
            player.resources -= WARRIOR_PRICE
            player.figures.append(warrior)
            return warrior
        return False

    def buildShip(self, field):
        player = self.currentPlayer()
        if player.resources >= SHIP_PRICE:
            ship = Ship(field, player)
            field.put(ship)
            player.resources -= SHIP_PRICE
            player.figures.append(ship)
            return ship
        return False

    def __harvestResources(self):
        player = self.currentPlayer()
        for building in player.buildings:
            if building.building == 'Garden':
                player.resources += GARDEN_INCOME

    def __checkForLoosers(self):
        black = False
        for figure in self.players[0].figures:
            if type(figure) == King:
                black = True
        white = False
        for figure in self.players[1].figures:
            if type(figure) == King:
                white = True
        if not black:
            self.loosers = 'black'
        if not white:
            self.loosers = 'both' if not black else 'white'

    def __onTurnStart(self):
        self.__harvestResources()
        self.__unfreezeFigures(self.currentPlayer())
        self.__checkForLoosers()

    def changeTurn(self):
        if self.turn == 1:
            self.turn = -1
        self.turn += 1
        self.__onTurnStart()
