from figure import Figure

class Ship(Figure):
    def __init__(self, field, player):
        super().__init__(field, player)
        self.fields = [None, None]

    def removeFigure(self, figure):
        if self.fields[0] == figure:
            self.fields[0] = None
        if self.fields[1] == figure:
            self.fields[1] = None

