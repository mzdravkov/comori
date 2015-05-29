# from program import Program
from ui_interface import UIInterface
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
import sys

class MyApp(ShowBase):
    pass


class EventHandler(DirectObject.DirectObject):
    def __init__(self, program):
        self.program = program
        self.accept('mouse1', program.handle, ['left_click'])
        self.accept('wheel_up', program.handle, ['wheel_up'])
        self.accept('wheel_down', program.handle, ['wheel_down'])
        self.accept('arrow_up', program.handle, ['up'])
        self.accept('arrow_down', program.handle, ['down'])
        self.accept('enter', program.handle, ['enter'])


class UI(UIInterface):
    def start(self):
        self.app = MyApp()
        self.app.gameTask = taskMgr.add(self.program.gameLoop, 'gameLoop')
        self.eventHandler = EventHandler(self.program)
        self.app.run()

    def exit(self):
        sys.exit()

    def __setMainMenuTransparency(self):
        self.newGameButton.setTransparency(TransparencyAttrib.MAlpha)
        self.optionsButton.setTransparency(TransparencyAttrib.MAlpha)
        self.exitButton.setTransparency(TransparencyAttrib.MAlpha)

    def drawMainMenu(self):
        x = self.app.win.getXSize()
        y = self.app.win.getYSize()

        if not hasattr(self, 'background'):
            self.background = OnscreenImage(image = 'textures/main_menu.png')
        if not hasattr(self, 'newGameButton'):
            self.newGameButton = OnscreenImage(image = 'textures/continue.png')
            self.newGameButton.setPos(0, 0, .6)
            self.newGameButton.setSx(.30)
            self.newGameButton.setSz(.13)
        if not hasattr(self, 'optionsButton'):
            self.optionsButton = OnscreenImage(image = 'textures/options.png')
            self.optionsButton.setPos(0, 0, .36)
            self.optionsButton.setSx(.30)
            self.optionsButton.setSz(.13)
        if not hasattr(self, 'exitButton'):
            self.exitButton = OnscreenImage(image = 'textures/exit.png')
            self.exitButton.setPos(0, 0, .12)
            self.exitButton.setSx(.30)
            self.exitButton.setSz(.13)

        self.background.setSx(x/y)

        selected = self.program.current().selected
        if selected == 0:
            self.newGameButton.setImage('textures/continue_hover.png')
            self.optionsButton.setImage('textures/options.png')
            self.exitButton.setImage('textures/exit.png')
        elif selected == 1:
            self.newGameButton.setImage('textures/continue.png')
            self.optionsButton.setImage('textures/options_hover.png')
            self.exitButton.setImage('textures/exit.png')
        elif selected == 2:
            self.newGameButton.setImage('textures/continue.png')
            self.optionsButton.setImage('textures/options.png')
            self.exitButton.setImage('textures/exit_hover.png')

        self.__setMainMenuTransparency()
