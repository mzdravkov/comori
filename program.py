# from game import Game
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

    def handle(self, *event):
        self.current().handle(event[0], event[1:])

    def start(self):
        self.ui.start()
