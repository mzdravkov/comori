from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import Task
# from direct.showbase import DirectObject
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import CollisionSphere
from panda3d.core import PointLight
from panda3d.core import LPoint3, LVector3, BitMask32, Vec4
from panda3d.core import VBase4
from panda3d.core import WindowProperties
from panda3d.core import AmbientLight
from panda3d.core import Texture

from pandac.PandaModules import loadPrcFileData

from mouse import MouseHandler
from board import GameBoard


import os

CAM_LIMITS = ((-5, 5), (-8, 2), (1, 10))

ISLANDS_POS = ((0, -0.23),
               (1.79, 0.27),
               (-1.79, 0.27),
               (-0.79, 1.5),
               (0.79, 1.5),
               (-1.43, -1.27),
               (1.43, -1.27),
               (0, -1.96),
               (0, -3.355),
               (2.521, -2.140),
               (3.148, 0.585),
               (1.396, 2.767),
               (-1.396, 2.767),
               (-3.148, 0.585),
               (-2.521, -2.140),
               (-2.225, -4.749),
               (0, 5),
               (2.225, -4.749),
               (-4.01, 3.069),
               (5, -1.27),
               (-5, -1.27),
               (4.01, 3.069))

# def main_menu_context(game):
#     # game.context.removeNode()
#     game.context = render.attachNewNode('context')
#     game.context.setTag('context', 'main_menu')
#     x = game.win.getXSize()
#     y = game.win.getYSize()
#     imageObject = OnscreenImage(image = 'textures/main_menu.png', scale=(1920/x, 1, 1080/y))#, pos = (-0.5, 0, 0.02))
#     return imageObject

# def game_context():
#     pass

class Game(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.setFullscreen(1860, 1240)

        # main_menu_context(self)

        # Disable the default camera control
        self.disableMouse()

        self.camera.setPos(0, 0, 10)
        self.camera.setHpr(0, -70, 0)
        self.camLens.setNear(0.9)


        self.highlightableObjects = render.attachNewNode('highlightables')

        self.setupColisionForHighlight()
        for pos in ISLANDS_POS:
            # i = self.loader.loadModel('models/island2_104')
            i = self.loader.loadModel('models/island3_02')
            i.setPos(pos[0], pos[1], 0)
            i.setScale(0.05, 0.05, 0.05)
            i.reparentTo(self.render)

        self.environ = self.loader.loadModel('models/plane')
        self.sea = self.loader.loadTexture('textures/sea.png')
        self.environ.setTexture(self.sea)
        # self.environ = self.loader.loadModel("models/test")
        # self.environ.setScale(0.25, 0.25, 0.25)
        # self.environ.setPos(0, 13, 0)
        self.environ.setPos(0, 0, 0)
        self.sea.setWrapU(Texture.WM_repeat)
        self.sea.setWrapV(Texture.WM_repeat)


        self.environ.reparentTo(self.highlightableObjects)
        # self.environ.setTag('myObjectTag', '1')
        # cs = CollisionSphere(0, 0, 0, 1)
        # cnodePath = self.environ.attachNewNode(CollisionNode('cnode'))
        # cnodePath.node().addSolid(cs)
        # cnodePath.show()

        plight = PointLight('plight')
        plight.setColor(VBase4(1, 1, 1, 13))
        plnp = render.attachNewNode(plight)
        plnp.setPos(10, 0, 10)
        render.setLight(plnp)
        # Create Ambient Light
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.25, 0.25, 0.25, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)


        self.gameTask = taskMgr.add(self.gameLoop, 'gameLoop')

    def setFullscreen(self, width, height):
        wp = WindowProperties()
        wp.setSize(width, height)
        wp.setFullscreen(True)
        if os.name == 'posix':
            base.openMainWindow()
            base.graphicsEngine.openWindows()
        self.win.requestProperties(wp)

    def cameraSpeed(self, height, speedRange):
        # Figure out how 'wide' each range is
        leftSpan = CAM_LIMITS[2][1] - CAM_LIMITS[2][0]
        rightSpan = speedRange[1] - speedRange[0]

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(height - CAM_LIMITS[2][0]) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return speedRange[0] + (valueScaled * rightSpan)


    def cameraMoving(self):
        if self.mouseWatcherNode.hasMouse():
            x, y = self.mouseWatcherNode.getMouse()
            transformX, transformY = 0, 0
            height = self.camera.getZ()
            speed = self.cameraSpeed(height, (0.01, 0.2))
            if x < -0.7:
                transformX -= speed
            elif x > 0.7:
                transformX += speed
            if y < -0.7:
                transformY -= speed
            elif y > 0.7:
                transformY += speed
            newX = self.camera.getX() + transformX
            newY = self.camera.getY() + transformY
            if (newX < CAM_LIMITS[0][0] or newX > CAM_LIMITS[0][1] or
                    newY < CAM_LIMITS[1][0] or newY > CAM_LIMITS[1][1]):
                return
            self.camera.setPos(newX, newY, self.camera.getZ())


    def setupColisionForHighlight(self):
        # Since we are using collision detection to do picking, we set it up like
        # any other collision detection system with a traverser and a handler
        self.picker = CollisionTraverser()  # Make a traverser
        self.pq = CollisionHandlerQueue()  # Make a handler
        # Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay')
        # Attach that node to the camera since the ray will need to be positioned
        # relative to it
        self.pickerNP = camera.attachNewNode(self.pickerNode)
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
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())

            self.picker.traverse(self.render)
            if self.pq.getNumEntries() > 0:
                # This is so we get the closest object.
                self.pq.sortEntries()
                pickedObj = self.pq.getEntry(0).getIntoNodePath()
                pickedObj = pickedObj.findNetTag('myObjectTag')
                if not pickedObj.isEmpty():
                    print(pickedObj.getTag('myObjectTag'))


    def gameLoop(self, task):
        self.cameraMoving()
        self.highlight()
        # main_menu_context(self)
        return task.cont


# loadPrcFileData("","win-size  1840 768") 
# loadPrcFileData("",  "fullscreen 1")

game = Game()
mouseHandler = MouseHandler(game)
game.run()
