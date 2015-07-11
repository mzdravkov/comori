class Building:
    def __init__(self, building, field):
        self.building = building
        self.field = field
        self.price = self.buildingPrice(building)

    @staticmethod
    def buildingPrice(building):
        if building == 'House':
            return 15
        elif building == 'Garden':
            return 20
        elif building == 'Thorn wall':
            return 50
        elif building == 'Barracks':
            return 30
        elif building == 'Bridge':
            return 50
        elif building == 'Harbor':
            return 40
        elif building == 'Library':
            return 60
        elif building == 'Statue':
            return 60
        elif building == 'Prison':
            return 60
        elif building == 'Rebel camp':
            return 70
        elif building == 'Shrine':
            return 100
