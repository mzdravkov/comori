from king import King
from warrior import Warrior
from peasant import Peasant


class Player:
    def __init__(self):
        self.figures = [King(), Warrior(), Peasant()]
        self.buildings = []
