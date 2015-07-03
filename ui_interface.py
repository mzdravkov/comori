class UIInterface():
    def exit(self):
        raise NotImplementedError

    def drawMainMenu(self):
        raise NotImplementedError

    def drawGame(self):
        raise NotImplementedError

    def drawOptions(self):
        raise NotImplementedError

    def destroyMainMenu(self):
        raise NotImplementedError

    def destroyGame(self):
        raise NotImplementedError

    def destroyOptions(self):
        raise NotImplementedError

    def getCameraCoords(self):
        raise NotImplementedError

    def setCameraCoords(self, x, y, z):
        raise NotImplementedError

    def getMouseCoords(self):
        raise NotImplementedError

    def highlight(self):
        raise NotImplementedError

    def hover(self, ):
        raise NotImplementedError

