from game import Game
from main_menu import MainMenu
# from ui import UI

class Program:
    def __init__(self, ui):
        self.stack = [MainMenu(self, ui)]
        self.ui = ui




    def start(self):
        self.ui.start()
