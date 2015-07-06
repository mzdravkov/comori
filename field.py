class Field:
    def __init__(self, island, x, y):
        self.x = x
        self.y = y
        self.island = island
        self.figure = None

    def put(self, figure):
        if self.figure != None:
            self.figure.field = None
        self.figure = figure
        if figure != None:
            figure.field = self

class SeaField(Field):
    def __init__(self, x, y, island=None):
        super().__init__(island, x, y)
        self.linked = []
