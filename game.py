from player import Player
from board import Board

HIGHLIGHT_SCALE = 1.25
REVERSE_HIGHLIGHT_SCALE = 1/HIGHLIGHT_SCALE

class Game:
    def __init__(self, program, ui):
        self.program = program
        self.ui = ui
        self.board = Board()
        self.players = [Player(), Player()]
        self.turn = 0
        self.camLimits = ui.camLimits
        self.lastHovered = None
        self.hovered = None

    def handle(self, event, args):
        print(event)
        if event == 'wheel_up':
            x, y, z = self.ui.getCameraCoords()
            if z > self.camLimits[2][0]:
                self.ui.setCameraCoords(x, y, z - 1)
        elif event == 'wheel_down':
            x, y, z = self.ui.getCameraCoords()
            if z < self.camLimits[2][1]:
                self.ui.setCameraCoords(x, y, z + 1)
        elif event == 'enter':
            if self.turn == 1:
                self.turn = -1
            self.turn += 1
        elif event == 'left_click':
            mousePos = self.ui.getMouseCoords()
            if mousePos == None:
                return
            x, y = mousePos
            print(x, ' ', y)

    def cameraSpeed(self, height, speedRange):
        # Figure out how 'wide' each range is
        leftSpan = self.camLimits[2][1] - self.camLimits[2][0]
        rightSpan = speedRange[1] - speedRange[0]

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(height - self.camLimits[2][0]) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return speedRange[0] + (valueScaled * rightSpan)

    def moveCamera(self):
        mousePos = self.ui.getMouseCoords()
        if mousePos == None:
            return
        x, y = mousePos
        camX, camY, camZ = self.ui.getCameraCoords()
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
        self.ui.setCameraCoords(newX, newY, camZ)

    def gameLoop(self):
        self.moveCamera()

    def hover(self, hovered):
        if self.hovered != None:
            reverseFactor = self.hovered.getScale()[0]
            reverseFactor *= REVERSE_HIGHLIGHT_SCALE
            self.hovered.setScale(reverseFactor)
        self.hovered = None
        if hovered != None:
            if hovered.getTag('player') != str(self.turn):
                return
            self.hovered = hovered
            factor = HIGHLIGHT_SCALE * hovered.getScale()[0]
            hovered.setScale(factor)
