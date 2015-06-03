# from program import Program
from ui_interface import UIInterface
from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib
from panda3d.core import PointLight
from panda3d.core import AmbientLight
from panda3d.core import VBase4
from panda3d.core import LPoint3, LVector3, BitMask32, Vec4
from panda3d.core import Texture
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
    def __init__(self):
        self.camLimits = ((-5, 5), (-8, 2), (1, 10))

    def start(self):
        self.app = MyApp()
        self.app.gameTask = taskMgr.add(self.program.programLoop, 'programLoop')
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

    def destroyMainMenu(self):
        self.background.destroy()
        self.newGameButton.destroy()
        self.optionsButton.destroy()
        self.exitButton.destroy()

    def getCameraCoords(self):
        return self.app.camera.getPos()

    def setCameraCoords(self, x, y, z):
        self.app.camera.setPos(x, y, z)

    def getMouseCoords(self):
        if self.app.mouseWatcherNode.hasMouse():
            return self.app.mouseWatcherNode.getMouse()
        return None

    def drawGame(self, game):
        if not hasattr(self, 'gameReady'):
            self.app.disableMouse()
            self.app.environ = self.app.loader.loadModel('models/plane')
            self.app.sea = self.app.loader.loadTexture('textures/sea.png')
            self.app.environ.setTexture(self.app.sea)
            self.app.environ.setPos(0, 0, 0)
            self.app.environ.setScale(1.1)
            self.app.sea.setWrapU(Texture.WM_repeat)
            self.app.sea.setWrapV(Texture.WM_repeat)

            self.app.camera.setPos(0, 0, 10)
            self.app.camera.setHpr(0, -70, 0)
            self.app.camLens.setNear(0.85)

            plight = PointLight('plight')
            plight.setColor(VBase4(1, 1, 1, 3))
            plnp = self.app.render.attachNewNode(plight)
            plnp.setPos(10, 0, 10)
            self.app.render.setLight(plnp)
            # Create Ambient Light
            ambientLight = AmbientLight('ambientLight')
            ambientLight.setColor(Vec4(0.25, 0.25, 0.25, .3))
            ambientLightNP = self.app.render.attachNewNode(ambientLight)
            self.app.render.setLight(ambientLightNP)

            self.app.environ.reparentTo(self.app.render)

            for island in game.board.islands:
                i = self.app.loader.loadModel('models/island2_104')
                i.setPos(island.pos[0], island.pos[1], 0)
                i.setScale(0.05, 0.05, 0.05)
                i.reparentTo(self.app.render)

            self.gameReady = True


