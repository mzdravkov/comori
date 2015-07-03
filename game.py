from player import Player
from board import Board
from warrior import Warrior
from king import King
from peasant import Peasant

class Game:
    def __init__(self,):
        self.board = Board()
        self.players = [Player('0'), Player('1')]
        self.turn = 0

    def setupFigures(self):
        for player in self.players:
            if player.color == '0':
                island = self.board.islands[-1]

                field = island.fields[0]
                field.put(King(field, player))
                player.figures.append(field.figure)
                field = island.fields[1]
                field.put(Warrior(field, player))
                player.figures.append(field.figure)
                field = island.fields[2]
                field.put(Peasant(field, player))
                player.figures.append(field.figure)
