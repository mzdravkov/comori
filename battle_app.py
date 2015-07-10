from panda3d.core import Camera
from panda3d.core import NodePath
from panda3d.core import Texture
from direct.showbase import DirectObject
from panda3d.core import CollisionNode
from panda3d.core import CollisionSphere
from panda3d.core import CollisionPolygon
from panda3d.core import Point3
from panda3d.core import Material
from panda3d.core import VBase4

import time
import threading

class BattleEventHandler(DirectObject.DirectObject):
    def __init__(self, app):
        self.accept('mouse1', app.battleHandle, ['left_click'])

class PieceMover(threading.Thread):
    def __init__(self, piece, moves, fields):
        threading.Thread.__init__(self)
        self.moves = moves
        self.piece = piece
        self.fields = fields

    def run(self):
        dead = False
        print(self.moves)
        for move in self.moves:
            moveX, moveY, killed = None, None, None
            if len(move) == 3:
                moveX, moveY, killed = move
            else:
                print('llama')
                print(move)
                moveX, moveY, killed, dead = move
                dead = True
            nextField = self.fields[moveX][moveY]
            self.piece.reparentTo(nextField)
            if dead:
                self.piece.removeNode()
            for corpse in killed:
                self.fields[corpse[0]][corpse[1]].getChildren()[-1].removeNode()
            time.sleep(0.3)

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

            self.clicked = None
            self.isMoving = False
            self.mover = None

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
                    field.setTag('clickable', 'true')
                    field.setTag('field', 'true')
                    field.setTag('x', str(x))
                    field.setTag('y', str(y))
                    field.reparentTo(self.battleRender)
                    self.battleFields[x].append(field)


            self.battleReady = True
        if self.mover and not self.mover.is_alive():
            self.mover = None
            self.isMoving = False

    def destroyBattle(self):
        self.camera.setPos(0, 0, 10)
        self.camera.setHpr(0, -70, 0)('models/plane')
        self.battleBoard.destroy()
        # TODO check if this works
        self.gameEventHandler = GameEventHandler(self)
        self.battleEventHandler.ignoreAll()
        self.clicked = None
        self.mover = None
        # self.battleFields = None
        self.isMoving = False
        self.battleReady = False

    # def battleCurrentPlayer(self):
    #     if self.battleTurn == 0:
    #         return self.battle.black
    #     return self.battle.white
    def normalizeBattleFields(self):
        fields = self.battleFields
        normalized = []
        for x in fields:
            normalized.append([])
            for y in x:
                figures = y.getChildren()
                figure = figures[-1] if figures[-1].hasTag('piece') else None
                if not figure:
                    normalized[-1].append(0)
                    continue

                print(figure)
                mat = figure.getMaterial()
                print(mat)
                print(self.blackMaterial)
                if mat == self.blackMaterial:
                    normalized[-1].append(1)
                else:
                    normalized[-1].append(2)
        return normalized

    def battleHandle(self, event, *args):
        if event == 'left_click':
            obj = self.highlight()
            if obj != None:
                if self.battlePhase == 'initial' and obj.hasTag('field'):
                    figure = self.loader.loadModel('models/circle')
                    figure.setScale(7)
                    if self.battleTurn == 0:
                        figure.setMaterial(self.blackMaterial)
                    else:
                        figure.setMaterial(self.whiteMaterial)
                    cs = CollisionSphere(0, 0, 0, 1)
                    cnodePath = figure.attachNewNode(CollisionNode('cnode'))
                    cnodePath.node().addSolid(cs)
                    figure.setTag('clickable', 'true')
                    figure.setTag('piece', 'true')
                    figure.reparentTo(obj)
                    if self.battlePlayedTurns == 9:
                        self.battlePhase = 'fight'
                    self.battlePlayedTurns += 1
                    self.battleTurn = self.battleTurn ^ 1
                elif (self.battlePhase == 'fight' and
                      obj.hasTag('piece') and
                      not self.isMoving):
                    color = self.blackMaterial
                    if self.battleTurn == 1:
                        color = self.whiteMaterial
                    if obj.getMaterial() == color:
                        self.clicked = obj
                    else:
                        self.clicked = None
                elif self.battlePhase == 'fight' and obj.hasTag('field'):
                    if self.clicked != None:
                        fromField = self.clicked.getParent()
                        fromX = int(fromField.getTag('x'))
                        fromY = int(fromField.getTag('y'))
                        toX = int(obj.getTag('x'))
                        toY = int(obj.getTag('y'))
                        deltaX = toX - fromX
                        deltaY = toY - fromY
                        # if have not clicked on the same field
                        if deltaX | deltaY == 0:
                            return
                        if -1 <= deltaX <= 1 and -1 <= deltaY <= 1:
                            fields = self.normalizeBattleFields()
                            moves = self.battle.move(fields, fromX, fromY, toX, toY)
                            self.mover = PieceMover(self.clicked, moves, self.battleFields)
                            self.mover.start()
                            self.isMoving = True
                        self.battleTurn = self.battleTurn ^ 1
                    self.clicked = None



    # TODO: think about destroying battle like menu is destroyed
