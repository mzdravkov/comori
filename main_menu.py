# from options import Options
from game import Game

class MainMenu:
    def new_game(self):
        self.program.push(Game(self.program, self.ui))


    def options(self):
        self.program.push(Options(self.program, self.ui))


    def __init__(self, program, ui):
        self.program = program
        self.ui = ui
        self.menu = [('New game', self.new_game),
                     ('Options', self.options),
                     ('Exit', ui.exit)]
        self.selected = 0


    def handle(self, event, args):
        if event == 'up':
            if self.selected > 0:
                self.selected -= 1
        elif event == 'down':
            if self.selected < 2:
                self.selected += 1
        elif event == 'enter':
            self.menu[self.selected][1]()
