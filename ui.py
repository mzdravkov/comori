from direct.showbase.ShowBase import ShowBase

from main_menu import MainMenu
from game_app import GameApp
from battle_app import BattleApp

from core.game import Game
from core.battle import Battle


class MyApp(ShowBase, MainMenu, GameApp, BattleApp):

    def __init__(self):
        ShowBase.__init__(self)
        MainMenu.__init__(self)
        GameApp.__init__(self)
        BattleApp.__init__(self)

        self.stack = [MainMenu()]
        self.gameTask = taskMgr.add(self.programLoop, 'programLoop')
        self.last = self.current()
        self.hasDrawnMainMenu = False
        self.disableMouse()

    def current(self):
        return self.stack[-1]

    def programLoop(self, task):
        if self.current() != self.last:
            if type(self.current()) != Battle:
                getattr(self, 'destroy' + type(self.last).__name__)()
            self.last = self.current()

        hovered = self.highlight()

        if type(self.current()) == MainMenu:
            if not self.hasDrawnMainMenu:
                self.drawMainMenu()
        elif type(self.current()) == Game:
            if hovered == None or hovered.getTag('highlightable') == 'true':
                self.hoverFigure(hovered)
            self.moveCamera()
            self.drawGame(self.current())
        elif type(self.current()) == Battle:
            self.drawBattle(self.current())

        return task.cont

    def push(self, elem):
        self.stack.append(elem)

    def pop(self):
        self.stack = self.stack[:-1]
