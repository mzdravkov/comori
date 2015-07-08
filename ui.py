# from program import Program
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
# from direct.gui.OnscreenText import OnscreenText
# from panda3d.core import TransparencyAttrib
# from panda3d.core import PointLight
# from panda3d.core import AmbientLight
# from panda3d.core import VBase4
# from panda3d.core import LPoint3, LVector3, BitMask32, Vec4
# from panda3d.core import Texture
# from panda3d.core import CollisionSphere
# from panda3d.core import TextNode
# from direct.task.Task import Task

# from direct.gui.DirectGui import DirectButton
# from direct.showutil import BuildGeometry
# import math

from main_menu import MainMenu
from game_app import GameApp
from battle_app import BattleApp

from game import Game
from battle import Battle

class EventHandler(DirectObject.DirectObject):
    def __init__(self, app):
        self.accept('mouse1', app.handle, ['left_click'])
        self.accept('wheel_up', app.handle, ['wheel_up'])
        self.accept('wheel_down', app.handle, ['wheel_down'])
        self.accept('arrow_up', app.handle, ['up'])
        self.accept('arrow_down', app.handle, ['down'])
        self.accept('enter', app.handle, ['enter'])
        for i in range(1, 10):
            self.accept(str(i), app.handle, [str(i)])


class MyApp(ShowBase, MainMenu, GameApp, BattleApp):
    def __init__(self):
        ShowBase.__init__(self)
        MainMenu.__init__(self)
        GameApp.__init__(self)
        BattleApp.__init__(self)

        self.stack = [MainMenu()]
        self.gameTask = taskMgr.add(self.programLoop, 'programLoop')
        self.eventHandler = EventHandler(self)
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

