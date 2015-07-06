from island import Island
from field import SeaField
import csv

class Board:
    def __init__(self):
        self.islands = []
        self.seawayFields = []
        self.islandsPos = []
        self.setupIslandsPositions()
        for pos in self.islandsPos:
            island = Island(pos)
            self.islands.append(island)
        self.setupSeawayFields()
        self.setupSeaways()
        self.setupBays()

    def possible_moves(self, figure):
        pred1 = lambda field: field.figure == None
        pred2 = lambda field: field.figure.player != figure.player
        island = figure.field.island
        return [field for field in island.fields if pred1(field) or pred2(field)]

    def setupIslandsPositions(self):
        with open('islands.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.islandsPos.append((float(row[0]), float(row[1])))

    def setupSeawayFields(self):
        with open('water_fields.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                field = SeaField(float(row[0]), float(row[1]))
                self.seawayFields.append(field)

    def setupSeaways(self):
        with open('water_fields_links.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            rowNum = 0
            for row in spamreader:
                field = self.seawayFields[rowNum]
                for linked in row:
                    linked = int(linked)
                    field.linked.append(self.seawayFields[linked-1])
                rowNum += 1

    def setupBays(self):
        with open('harbor_links.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            rowNum = 0
            for row in spamreader:
                bay = self.islands[rowNum].bay
                for linked in row:
                    linked = int(linked)
                    field = self.seawayFields[linked-1]
                    bay.linked.append(field)
                    field.linked.append(bay)
                rowNum += 1
                    # self.seawayFields.append(harbor)
