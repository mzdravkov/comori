from panda3d.core import Camera
from panda3d.core import NodePath
from panda3d.core import Texture

class BattleApp:
    def __init__(self):
        # self.camera = Camera('battleCam')
        # self.cam = NodePath(self.camera)
        # self.render2 = NodePath('render2')
        # self.cam.reparentTo(self.render2)
        # self.cam.setPos(0, 0, 10)
        # self.cam.setHpr(0, -90, 0)
        # self.display = self.win.makeDisplayRegion()
        # self.display.setCamera(self.cam)
        # self.cam.reparentTo(self.render2)
        self.battleReady = False

    def drawBattle(self, battle):
        if not self.battleReady:
            self.battle = battle

            self.camera.setPos(0, 0, 20)
            self.camera.setHpr(0, -90, 0)

            self.battleBoard = self.loader.loadModel('models/plane')
            self.battleBoard.setPos(2, 2, 2)
            frame = self.loader.loadTexture('textures/frame.png')
            self.battleBoard.setTexture(frame)
            frame.setWrapU(Texture.WM_repeat)
            frame.setWrapV(Texture.WM_repeat)
            self.environ.reparentTo(self.render)

            self.battleReady = True

    def destroyBattle(self):
        self.camera.setPos(0, 0, 10)
        self.camera.setHpr(0, -70, 0)
        self.battleBoard.destroy()
        self.battleReady = False


    # TODO: think about destroying battle like menu is destroyed
