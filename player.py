from king import King
from warrior import Warrior
from peasant import Peasant


class Player:
    def __init__(self, color):
        self.figures = []
        self.buildings = []
        self.color = color
        self.resources = 50
