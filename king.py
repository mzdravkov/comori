from figure import Figure

class King(Figure):
    def __init__(self, field, player):
        super().__init__(field, player)
        self.modelFile = 'models/warrior100'
