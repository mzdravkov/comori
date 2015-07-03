from field import Field

class Island:
    def __init__(self, pos):
        self.pos = pos
        self.model = 'island'
        self.fields = [[-1.135, -2.007],
                       [-1.703, -2.737],
                       [-1.925, -3.7],
                       [-0.1,   -1.923],
                       [ 0.8,   -2.3],
                       [ 1.2,   -3.1]]
        self.fields = [Field(self, f[0], f[1]) for f in self.fields]
