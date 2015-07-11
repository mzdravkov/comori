from field import Field
from field import SeaField

class Island:
    def __init__(self, pos):
        self.pos = pos
        self.model = 'island'
        fields = [(-1.135, -2.007),
                  (-1.703, -2.737),
                  (-1.925, -3.7),
                  (-0.1,   -1.923),
                  ( 0.8,   -2.3),
                  ( 1.2,   -3.1)]
        self.bay = SeaField(0, -5.5, self)
        self.fields = [Field(self, f[0], f[1]) for f in fields]
        self.buildings = [None, None, None]
        self.buildingFields = (Field(self, -5, 1),
                               Field(self, 2.7, -4.7),
                               Field(self, -3.2, 3.5))
