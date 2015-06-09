# from options import Options
from game import Game

class MainMenu:
    def newGame(self):
        self.program.push(Game(self.program, self.ui))


    def options(self):
        self.program.push(Options(self.program, self.ui))


    def __init__(self, program, ui):
        self.program = program
        self.ui = ui


    def handle(self, event, args):
        if event == 'click':
            if args[0] == 'newGame':
                self.newGame()
            elif args[0] == 'options':
                self.options()
            elif args[0] == 'exit':
                self.ui.exit()

