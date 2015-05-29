from player import Player

class Game:
    def __init__(self, program, ui):
        self.program = program
        self.ui = ui
        self.players = [Player(), Player()]
        self.turn = 0

    def handle(self, event, args):
        print(event)
