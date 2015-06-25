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
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollisionSphere
from direct.gui.DirectGui import DirectButton
# from direct.showutil import BuildGeometry
import sys
import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.highlightableObjects = render.attachNewNode('highlightables')
        self.setupColisionForHighlight()

    def setupColisionForHighlight(self):
        # Since we are using collision detection to do picking, we set it up like
        # any other collision detection system with a traverser and a handler
        self.picker = CollisionTraverser()  # Make a traverser
        self.pq = CollisionHandlerQueue()  # Make a handler
        # Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay')
        # Attach that node to the camera since the ray will need to be positioned
        # relative to it
        self.pickerNP = self.camera.attachNewNode(self.pickerNode)
        # Everything to be picked will use bit 1. This way if we were doing other
        # collision we could seperate it
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()  # Make our ray
        # Add it to the collision node
        self.pickerNode.addSolid(self.pickerRay)
        # Register the ray as something that can cause collisions
        self.picker.addCollider(self.pickerNP, self.pq)

    def highlight(self):
        if self.mouseWatcherNode.hasMouse():
            mPos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mPos.getX(), mPos.getY())

            self.picker.traverse(self.render)
            if self.pq.getNumEntries() > 0:
                # This is so we get the closest object.
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('id')
                if not pickedObj.isEmpty():
                    print(pickedObj.getTag('id'))
                    return pickedObj


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

    def drawMainMenu(self):
        x = self.app.win.getXSize()
        y = self.app.win.getYSize()

        if not hasattr(self, 'background'):
            self.background = OnscreenImage(image = 'textures/main_menu.png')

        self.background.setSx(x/y)

        clickNewGameButton = lambda: self.program.handle('click', 'newGame')
        clickOptionsButton = lambda: self.program.handle('click', 'options')
        clickExitButton = lambda: self.program.handle('click', 'exit')

        def setButtonAttributes(button):
            button.setSx(.60)
            button.setSz(.26)
            button.setTransparency(TransparencyAttrib.MAlpha)

        if not hasattr(self, 'newGameButton'):
            maps = loader.loadModel('textures/continue_maps.egg')
            geom = (maps.find('**/continue'),
                    maps.find('**/continue_click'),
                    maps.find('**/continue_hover'))
            self.newGameButton = DirectButton(geom = geom, relief=None,
                                              command=clickNewGameButton)
            setButtonAttributes(self.newGameButton)
            self.newGameButton.setPos(0, 0, .6)

        if not hasattr(self, 'optionsButton'):
            maps = loader.loadModel('textures/options_maps.egg')
            geom = (maps.find('**/options'),
                    maps.find('**/options_click'),
                    maps.find('**/options_hover'))
            self.optionsButton = DirectButton(geom = geom, relief=None,
                                              command=clickOptionsButton)
            setButtonAttributes(self.optionsButton)
            self.optionsButton.setPos(0, 0, .36)

        if not hasattr(self, 'exitButton'):
            maps = loader.loadModel('textures/exit_maps.egg')
            geom = (maps.find('**/exit'),
                    maps.find('**/exit_click'),
                    maps.find('**/exit_hover'))
            self.exitButton = DirectButton(geom = geom, relief=None,
                                           command=clickExitButton)
            setButtonAttributes(self.exitButton)
            self.exitButton.setPos(0, 0, .12)

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

    def highlight(self):
        return self.app.highlight()

    def drawGame(self, game):
        if not hasattr(self, 'gameReady'):
            a = self.app.loader.loadModel('models/warrior100')
            a.setTag('id', '1')
            a.setTag('handler', 'game')
            a.setTag('type', 'figure')
            a.setTag('player', '0')
            cs = CollisionSphere(0, -.35, 7, 3.5)
            cnodePath = a.attachNewNode(CollisionNode('cnode'))
            cnodePath.node().addSolid(cs)
            # cnodePath.show()
            a.reparentTo(self.app.highlightableObjects)
            a.setScale(0.007)
            a.setPos(0, -.35, 0)
            # a.reparentTo(self.app.render)


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

            first = True
            for island in game.board.islands:
                i = self.app.loader.loadModel('models/island2_104')
                i.setPos(island.pos[0], island.pos[1], 0.001)
                i.setScale(0.05, 0.05, 0.05)
                i.reparentTo(self.app.render)
                for f in range(0, 6):
                    circle = self.app.loader.loadModel('models/circle')
                    pos = (island.fields[f][0], island.fields[f][1], 0.4)
                    circle.setPos(pos)
                    circle.setScale(0.4)
                    circle.reparentTo(i)
                degree = angle((0, 1), island.pos)*180/math.pi
                if island.pos[0] > 0:
                    degree *= -1
                if first:
                    first = False
                    continue
                i.setHpr(degree, 0, 0)
                self.gameReady = True
