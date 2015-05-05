from direct.showbase import DirectObject

CAM_LIMITS = ((-5, 5), (-7, 10), (1, 10))

class MouseHandler(DirectObject.DirectObject):
    def __init__(self, game):
        self.game = game
        self.accept('mouse1', self.leftClick)
        self.accept('wheel_up', self.wheelUp)
        self.accept('wheel_down', self.wheelDown)


    def leftClick(self):
        print('left click')


    def wheelUp(self):
        cam = self.game.camera
        if cam.getZ() <= CAM_LIMITS[2][0]:
            return
        cam.setPos(cam.getX(), cam.getY(), cam.getZ() - 1)


    def wheelDown(self):
        cam = self.game.camera
        if cam.getZ() >= CAM_LIMITS[2][1]:
            return
        cam.setPos(cam.getX(), cam.getY(), cam.getZ() + 1)
