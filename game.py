from player import Player
from board import Board
from warrior import Warrior
from king import King
from peasant import Peasant
from ship import Ship
from building import Building

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
                island = self.board.islands[-2]

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

    def changeTurn(self):
        if self.turn == 1:
            self.turn = -1;
        self.turn += 1
        self.__unfreezeFigures(self.players[self.turn])
