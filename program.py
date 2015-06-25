from game import Game
from main_menu import MainMenu
# from ui import UI

class Program:
    def __init__(self, ui):
        self.stack = [MainMenu(self, ui)]
        self.ui = ui

    def current(self):
        return self.stack[-1]

    def push(self, elem):
        if len(self.stack) == 1:
            self.stack[0] = MainMenu(self, self.ui)
        self.stack.append(elem)

    def pop(self):
        self.stack = self.stack[:-1]

    def handle(self, event, *args):
        self.current().handle(event, args)

    def start(self):
        self.ui.start()

    def programLoop(self, task):
        if not hasattr(self, 'last'):
            self.last = self.current()
        elif self.current() != self.last:
            getattr(self.ui, 'destroy' + type(self.last).__name__)()
            self.last = self.current()
        hovered = self.ui.highlight()

        if type(self.current()) == MainMenu:
            self.ui.drawMainMenu()
        elif type(self.current()) == Game:
            if hovered == None or (hovered.getTag('handler') == 'game'):
                self.current().hover(hovered)
            self.current().gameLoop()
            self.ui.drawGame(self.current())


        return task.cont
