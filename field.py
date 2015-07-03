class Field:
    def __init__(self, island, x, y):
        self.x = x
        self.y = y
        self.island = island
        self.figure = None

    def put(self, figure):
        self.figure = figure
