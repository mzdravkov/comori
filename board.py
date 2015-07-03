from island import Island

ISLANDS_POS = ((0, -0.23),
               (1.79, 0.27),
               (-1.79, 0.27),
               (-0.79, 1.5),
               (0.79, 1.5),
               (-1.43, -1.27),
               (1.43, -1.27),
               (0, -1.96),
               (0, -3.355),
               (2.521, -2.140),
               (3.148, 0.585),
               (1.396, 2.767),
               (-1.396, 2.767),
               (-3.148, 0.585),
               (-2.521, -2.140),
               (-2.225, -4.749),
               (0, 5),
               (2.225, -4.749),
               (-4.01, 3.069),
               (5, -1.27),
               (-5, -1.27),
               (4.01, 3.069))


class Board:
    def __init__(self):
        self.islands = []
        for pos in ISLANDS_POS:
            island = Island(pos)
            self.islands.append(island)

    def possible_moves(self, figure):
        if figure.hasMoved:
            return []
        pred1 = lambda field: field.figure == None
        pred2 = lambda field: field.figure.player != figure.player
        island = figure.field.island
        return [field for field in island.fields if pred1(field) or pred2(field)]
