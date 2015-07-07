class Building:
    def __init__(self, building, field):
        self.building = building
        self.field = field
        self.price = None
        self.__setPrice()

    def __setPrice(self):
        if self.building == 'House':
            self.price = 15
        elif self.building == 'Garden':
            self.price = 20
        elif self.building == 'Thorn wall':
            self.price = 50
        elif self.building == 'Barracks':
            self.price = 30
        elif self.building == 'Bridge':
            self.price = 50
        elif self.building == 'Harbor':
            self.price = 40
        elif self.building == 'Library':
            self.price = 60
        elif self.building == 'Statue':
            self.price = 60
        elif self.building == 'Prison':
            self.price = 60
        elif self.building == 'Rebel camp':
            self.price = 70
        elif self.building == 'Shrine':
            self.price = 100
