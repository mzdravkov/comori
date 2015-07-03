from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from direct.gui.DirectGui import DirectButton

from game import Game

import sys

# from base_ui import BaseUI

# class MainMenu(BaseUI):
class MainMenu:
    def __init__(self):
        self.background = None
        self.newGameButton = None
        self.optionsButton = None
        self.exitButton = None

    def drawMainMenu(self):
        x = self.win.getXSize()
        y = self.win.getYSize()

        self.background = OnscreenImage(image = 'textures/main_menu.png')

        self.background.setSx(x/y)

        clickNewGameButton = lambda: self.push(Game())
        clickOptionsButton = lambda: self.push('Options')
        clickExitButton = lambda: sys.exit()

        def setButtonAttributes(button):
            button.setSx(.60)
            button.setSz(.26)
            button.setTransparency(TransparencyAttrib.MAlpha)

        maps = loader.loadModel('textures/continue_maps.egg')
        geom = (maps.find('**/continue'),
                maps.find('**/continue_click'),
                maps.find('**/continue_hover'))
        self.newGameButton = DirectButton(geom = geom, relief=None,
                                          command=clickNewGameButton)
        setButtonAttributes(self.newGameButton)
        self.newGameButton.setPos(0, 0, .6)

        maps = loader.loadModel('textures/options_maps.egg')
        geom = (maps.find('**/options'),
                maps.find('**/options_click'),
                maps.find('**/options_hover'))
        self.optionsButton = DirectButton(geom = geom, relief=None,
                                          command=clickOptionsButton)
        setButtonAttributes(self.optionsButton)
        self.optionsButton.setPos(0, 0, .36)

        maps = loader.loadModel('textures/exit_maps.egg')
        geom = (maps.find('**/exit'),
                maps.find('**/exit_click'),
                maps.find('**/exit_hover'))
        self.exitButton = DirectButton(geom = geom, relief=None,
                                       command=clickExitButton)
        setButtonAttributes(self.exitButton)
        self.exitButton.setPos(0, 0, .12)

        self.hasDrawnMainMenu = True

    def destroyMainMenu(self):
        self.background.destroy()
        self.newGameButton.destroy()
        self.optionsButton.destroy()
        self.exitButton.destroy()

        self.hasDrawnMainMenu = False
