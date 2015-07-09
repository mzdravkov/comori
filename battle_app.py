from panda3d.core import Camera
from panda3d.core import NodePath
from panda3d.core import Texture
from direct.showbase import DirectObject
from panda3d.core import CollisionNode
from panda3d.core import CollisionPolygon
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Point3
from panda3d.core import Material
from panda3d.core import VBase4

class BattleEventHandler(DirectObject.DirectObject):
    def __init__(self, app):
        self.accept('mouse1', app.battleHandle, ['left_click'])

class BattleApp:
    def __init__(self):
        self.battleReady = False

    def drawBattle(self, battle):
        if not self.battleReady:
            self.battle = battle
            self.battleRender = NodePath('battleRender')
            self.battleRender.reparentTo(self.render)
            self.battleEventHandler = BattleEventHandler(self)

            self.camera.setPos(0, 0, 40)
            self.camera.setHpr(0, -90, 0)

            self.blackMaterial = Material()
            self.blackMaterial.setDiffuse(VBase4(0, 0, 0, 1))
            self.whiteMaterial = Material()
            self.whiteMaterial.setDiffuse(VBase4(256, 256, 256, 1))

            self.battleBoard = self.loader.loadModel('models/plane')
            self.battleBoard.setPos(0, 0, 4)
            self.battleBoard.setScale(2)
            self.battleBoard.setMaterial(self.blackMaterial)
            self.battleBoard.reparentTo(self.render)

            self.resources.setText('')

            self.battlePhase = 'initial'
            self.battleTurn = 0
            self.battlePlayedTurns = 0

            self.battleFields = []
            for x in range(0, 8):
                self.battleFields.append([])
                for y in range(0, 8):
                    field = self.loader.loadModel('models/plane')
                    posX = x * 2.4 - 8.5
                    posY = y * 2.4 - 8.5
                    field.setPos(posX, posY, 4.2)
                    field.setScale(0.11)

                    cs = CollisionPolygon(Point3(-10, -10, 0),
                                          Point3(-10, 10, 0),
                                          Point3(10, 10, 0),
                                          Point3(10, -10, 0))
                    cnodePath = field.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    cnodePath.show()
                    field.setTag('clickable', 'true')
                    field.reparentTo(self.battleRender)
                    self.battleFields[x].append(field)


            self.battleReady = True

    def destroyBattle(self):
        self.camera.setPos(0, 0, 10)
        self.camera.setHpr(0, -70, 0)
        self.battleBoard.destroy()
        # TODO check if this works
        self.gameEventHandler = GameEventHandler(self)
        self.battleEventHandler.ignoreAll()
        # self.battleFields = None
        self.battleReady = False

    # def battleCurrentPlayer(self):
    #     if self.battleTurn == 0:
    #         return self.battle.black
    #     return self.battle.white

    def battleHandle(self, event, *args):
        if event == 'left_click':
            field = self.highlight()
            if field != None:
                if self.battlePhase == 'initial':
                    figure = self.loader.loadModel('models/circle')
                    figure.setScale(7)
                    if self.battleTurn == 0:
                        figure.setMaterial(self.blackMaterial)
                    else:
                        figure.setMaterial(self.whiteMaterial)
                    figure.reparentTo(field)
                    if self.battlePlayedTurns == 9:
                        self.battlePhase = 'fight'
                    self.battlePlayedTurns += 1
                self.battleTurn = self.battleTurn ^ 1



    # TODO: think about destroying battle like menu is destroyed
