# from panda3d.core import TransparencyAttrib
from panda3d.core import PointLight
from panda3d.core import AmbientLight
from panda3d.core import VBase4
# from panda3d.core import LPoint3, LVector3, BitMask32, Vec4
from panda3d.core import BitMask32
from panda3d.core import Vec4
from panda3d.core import Texture
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
# from direct.gui.DirectGui import *
# from direct.gui.OnscreenImage import OnscreenImage
# from panda3d.core import TransparencyAttrib
# from panda3d.core import Camera
# from panda3d.core import NodePath

from game import Game
from figure import Figure
from ship import Ship
import math

HIGHLIGHT_SCALE = 1.25
REVERSE_HIGHLIGHT_SCALE = 1/HIGHLIGHT_SCALE

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

class GameApp:
    def __init__(self):
        self.camLimits = ((-5, 5), (-6.5, 5), (1, 10))
        self.gameReady = False
        self.hovered = None
        self.clicked = None
        self.modelToFigure = {}
        self.modelToField = {}
        self.modelToSeaField = {}
        self.modelToBuildingField = {}
        # self.highlightableObjects = render.attachNewNode('highlightables')
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

    def getCameraCoords(self):
        return self.camera.getPos()

    def setCameraCoords(self, x, y, z):
        self.camera.setPos(x, y, z)

    def getMouseCoords(self):
        if self.mouseWatcherNode.hasMouse():
            return self.mouseWatcherNode.getMouse()
        return None

    def drawIsland(self, island, suppressRot=False):
        island.model.setPos(island.pos[0], island.pos[1], 0.001)
        island.model.setScale(0.05, 0.05, 0.05)
        island.model.reparentTo(self.render)
        for f in range(0, 6):
            circle = self.loader.loadModel('models/circle')
            pos = (island.fields[f].x, island.fields[f].y, 0.4)
            circle.setPos(pos)
            circle.setScale(0.4)
            circle.reparentTo(island.model)
            circle.setTag('clickable', 'true')
            cs = CollisionSphere(0, 0, 0, 1)
            cnodePath = circle.attachNewNode(CollisionNode('cnode'))
            cnodePath.node().addSolid(cs)
            island.fields[f].model = circle
            self.modelToField[circle.getKey()] = island.fields[f]

        for i in range(0, 3):
            buildingField = island.buildingFields[i]
            circle = self.loader.loadModel('models/circle')
            pos = (buildingField.x, buildingField.y, 0.1)
            circle.setPos(pos)
            circle.setScale(0.6)
            circle.reparentTo(island.model)
            circle.setTag('clickable', 'true')
            cs = CollisionSphere(0, 0, 0, 1)
            cnodePath = circle.attachNewNode(CollisionNode('cnode'))
            cnodePath.node().addSolid(cs)
            buildingField.model = circle
            self.modelToBuildingField[circle.getKey()] = buildingField

        # put the bay field
        circle = self.loader.loadModel('models/circle')
        pos = (island.bay.x, island.bay.y, 0.2)
        circle.setPos(pos)
        circle.setScale(0.6)
        circle.reparentTo(island.model)
        circle.setTag('clickable', 'true')
        cs = CollisionSphere(0, 0, 0, 1)
        cnodePath = circle.attachNewNode(CollisionNode('cnode'))
        cnodePath.node().addSolid(cs)
        island.bay.model = circle
        self.modelToSeaField[circle.getKey()] = island.bay
        degree = angle((0, 1), island.pos)*180/math.pi
        if island.pos[0] > 0:
            degree *= -1
        if not suppressRot:
            island.model.setHpr(degree, 0, 0)

    def drawFigures(self):
        for player in self.game.players:
            for figure in player.figures:
                if type(figure) == Ship:
                    field = figure.field
                    figure.model = self.loader.loadModel('models/ship')
                    figure.model.reparentTo(field.model)
                    cs = CollisionSphere(1.5, 0, 1, 1.3)
                    cnodePath = figure.model.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    # cnodePath.show()
                    cs = CollisionSphere(0, 0, 1.4, 1.3)
                    cnodePath = figure.model.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    # cnodePath.show()
                    cs = CollisionSphere(-1.8, 0, 1, 1)
                    cnodePath = figure.model.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    # cnodePath.show()
                    figure.model.setScale(1.4)
                    figure.model.setHpr(90, 0, 0)
                    # figure.model.setTag('highlightable', 'true')
                    figure.model.setTag('clickable', 'true')
                    self.modelToFigure[figure.model.getKey()] = figure
                else:
                    field = figure.field
                    figure.model = self.loader.loadModel('models/warrior100')
                    figure.model.reparentTo(field.model)
                    cs = CollisionSphere(0, -.35, 7, 1)
                    cnodePath = figure.model.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    figure.model.setScale(0.35)
                    figure.model.setTag('highlightable', 'true')
                    figure.model.setTag('clickable', 'true')
                    self.modelToFigure[figure.model.getKey()] = figure

                    col = 256*int(player.color)
                    # set figure title
                    title = TextNode(str(figure.model.getKey()) + '_title')
                    title.setText('1')
                    title.setCardColor(col, col, col, 1)
                    title.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
                    title.setCardDecal(True)
                    titleNode = self.render.attachNewNode(title)
                    titleNode.reparentTo(figure.model)
                    titleNode.setScale(5)
                    titleNode.setPos(0, 3, 10)
                    titleNode.setBillboardPointEye()

    def drawSeaways(self):
        for field in self.game.board.seawayFields:
            circle = self.loader.loadModel('models/circle')
            pos = (field.x, field.y, 0)
            circle.setPos(pos)
            circle.setScale(0.04)
            circle.reparentTo(self.render)
            circle.setTag('clickable', 'true')
            cs = CollisionSphere(0, 0, 0, 1)
            cnodePath = circle.attachNewNode(CollisionNode('cnode'))
            cnodePath.node().addSolid(cs)
            field.model = circle
            self.modelToSeaField[circle.getKey()] = field

    def drawGame(self, game):
        if not self.gameReady:
            self.game = game
            # menu = OnscreenImage(image = 'textures/menu.png', pos = (1.53, 0, 0), scale=(0.35, 1, 1))
            # menu.setTransparency(TransparencyAttrib.MAlpha)

            # setup the background of the board
            self.environ = self.loader.loadModel('models/plane')
            sea = self.loader.loadTexture('textures/sea.png')
            self.environ.setTexture(sea)
            self.environ.setPos(0, 1, 0)
            self.environ.setScale(1.1)
            sea.setWrapU(Texture.WM_repeat)
            sea.setWrapV(Texture.WM_repeat)
            self.environ.reparentTo(self.render)

            # setup camera
            self.camera.setPos(0, 0, 10)
            self.camera.setHpr(0, -70, 0)
            self.camLens.setNear(0.85)

            # setup lighting
            plight = PointLight('plight')
            plight.setColor(VBase4(1, 1, 1, 3))
            plnp = self.render.attachNewNode(plight)
            plnp.setPos(10, 0, 10)
            self.render.setLight(plnp)
            ambientLight = AmbientLight('ambientLight')
            ambientLight.setColor(Vec4(0.25, 0.25, 0.25, .3))
            ambientLightNP = self.render.attachNewNode(ambientLight)
            self.render.setLight(ambientLightNP)

            # place islands
            first = True
            for island in game.board.islands:
                island.drawable = True
                island.model = self.loader.loadModel('models/island2_104')
                self.drawIsland(island, first)
                first = False

            # NOT HERE!
            game.setupFigures()

            self.drawFigures()
            self.drawSeaways()

            self.turn = OnscreenText(text = 'Black\'s turn.',
                                     pos = (0.06, -0.1),
                                     align = TextNode.ALeft,
                                     parent = base.a2dTopLeft,
                                     scale = 0.06)
            self.gameReady = True

        player = 'Black'
        if game.turn == 1:
            player = 'White'
        self.turn.setText(player + '\'s turn.')


    def cameraSpeed(self, height, speedRange):
        # Figure out how 'wide' each range is
        leftSpan = self.camLimits[2][1] - self.camLimits[2][0]
        rightSpan = speedRange[1] - speedRange[0]

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(height - self.camLimits[2][0]) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return speedRange[0] + (valueScaled * rightSpan)

    def moveCamera(self):
        mousePos = self.getMouseCoords()
        if mousePos == None:
            return
        x, y = mousePos
        camX, camY, camZ = self.getCameraCoords()
        transformX, transformY = 0, 0
        speed = self.cameraSpeed(camZ, (0.01, 0.2))
        if x < -0.7 and y < -0.7:
            transformX -= speed
            transformY -= speed
        elif x > 0.7 and y < -0.7:
            transformX += speed
            transformY -= speed
        elif x < -0.7 and y > 0.7:
            transformX -= speed
            transformY += speed
        elif x > 0.7 and y > 0.7:
            transformX += speed
            transformY += speed
        else:
            if x < -0.7:
                transformX -= speed
            elif x > 0.7:
                transformX += speed
            if y < -0.7:
                transformY -= speed
            elif y > 0.7:
                transformY += speed
        newX = camX + transformX
        newY = camY + transformY
        if newX < self.camLimits[0][0] or newX > self.camLimits[0][1]:
            newX = camX
        if newY < self.camLimits[1][0] or newY > self.camLimits[1][1]:
            newY = camY
        self.setCameraCoords(newX, newY, camZ)

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
                # pick the model and not the cnode
                pickedObj = pickedObj.findNetTag('clickable')
                if not pickedObj.isEmpty():
                    return pickedObj

    @staticmethod
    def boardingTransformations(figure, pos):
        figure.model.setScale(0.2)
        figure.model.setPos(1 + pos, 0, 1)

    @staticmethod
    def unboardingTransformations(figure):
        figure.model.setScale(0.35)
        figure.model.setPos(0,0,0)

    def clickFigure(self, figure):
        print('figure')
        if type(figure) == Ship:
            ship = figure
            figure = self.clicked
            if isinstance(figure, Figure) and type(figure) != Ship:
                if figure.hasMoved:
                    self.clicked = ship
                    return
                if (figure.field.island == ship.field.island and
                    figure.player == ship.player and
                    None in ship.fields):
                        figure.field.put(None)
                        pos = 0
                        if ship.fields[0] == None:
                            ship.fields[0] = figure
                        else:
                            ship.fields[1] = figure
                            pos = 1
                        figure.field = ship
                        figure.model.reparentTo(ship.model)
                        self.boardingTransformations(figure, pos)
                        figure.hasMoved = True
            self.clicked = ship
        else:
            self.clicked = figure

    def clickField(self, field):
        if type(self.clicked) == Ship:
            return
        if self.clicked and isinstance(self.clicked, Figure):
            figure = self.clicked
            board = self.game.board
            if figure.hasMoved:
                return
            if type(figure.field) == Ship:
                if field in board.possible_moves(figure.field):
                    figure.field.removeFigure(figure)
                    field.put(figure)
                    figure.model.reparentTo(field.model)
                    self.unboardingTransformations(figure)
                    figure.hasMoved = True
            if field in board.possible_moves(self.clicked):
                figure.field.put(None)
                field.put(figure)
                figure.model.reparentTo(field.model)
                figure.hasMoved = True

    def clickSeaField(self, field):
        print(self.clicked)
        if type(self.clicked) == Ship:
            figure = self.clicked
            if field in figure.field.linked:
                figure.field.put(None)
                field.put(figure)
                figure.model.reparentTo(field.model)
                figure.hasMoved = True

    def clickBuildingField(self, field):
        print("Gonna build, huh?")
        print(field)

    def handle(self, event, *args):
        print(event)
        if type(self.current()) != Game:
            return
        if event == 'wheel_up':
            x, y, z = self.getCameraCoords()
            if z > self.camLimits[2][0]:
                self.setCameraCoords(x, y, z - 1)
        elif event == 'wheel_down':
            x, y, z = self.getCameraCoords()
            if z < self.camLimits[2][1]:
                self.setCameraCoords(x, y, z + 1)
        elif event == 'enter':
            self.game.changeTurn()
        elif event == 'left_click':
            obj = self.highlight()
            if obj != None:
                key = obj.getKey()
                # if it's a figure
                if key in self.modelToFigure:
                    figure = self.modelToFigure[key]
                    self.clickFigure(figure)
                # if it's a figure field
                if key in self.modelToField:
                    field = self.modelToField[key]
                    self.clickField(field)
                # if it's a building field
                if key in self.modelToBuildingField:
                    field = self.modelToBuildingField[key]
                    self.clickBuildingField(field)
                # if it's a sea field
                if key in self.modelToSeaField:
                    field = self.modelToSeaField[key]
                    self.clickSeaField(field)
            else:
                self.clicked = None

    def hoverFigure(self, hovered):
        if self.hovered != None:
            reverseFactor = self.hovered.getScale()[0]
            reverseFactor *= REVERSE_HIGHLIGHT_SCALE
            self.hovered.setScale(reverseFactor)
        self.hovered = None
        if hovered != None:
            figure = self.modelToFigure[hovered.getKey()]
            if figure.player.color != str(self.current().turn):
                return
            self.hovered = hovered
            factor = HIGHLIGHT_SCALE * hovered.getScale()[0]
            hovered.setScale(factor)
