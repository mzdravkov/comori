import math
import functools

def sin(angle):
    return math.sin(math.radians(angle))

def cos(angle):
    return math.cos(math.radians(angle))

def union(*args):
    sets = map(lambda x: set(x), args)
    return list(functools.reduce(lambda x, y: x | y, sets))

class Battle:
    def __init__(self, player1, player2):
        self.black = player1
        self.white = player2

    @staticmethod
    def width(fields):
        return len(fields)

    @staticmethod
    def height(fields):
        return len(fields[0])

    @staticmethod
    def rotate(x, y, angle):
        newX = x * cos(angle) - y * sin(angle)
        newY = x * sin(angle) + y * cos(angle)
        return (round(newX), round(newY))

    def isOutside(self, x, y, fields):
        if (x < 0 or x >= self.width(fields) or
            y < 0 or y >= self.height(fields)):
            return True
        return False

    def hit(self, collNeighs, fields, target):
        collisions = []
        for (x, y) in collNeighs:
            if not self.isOutside(x, y, fields):
                if fields[x][y] == target:
                    collisions.append((x, y))
        return collisions

    def move(self, fields, fromX, fromY, toX, toY):
        deltaX = toX - fromX
        deltaY = toY - fromY
        player = fields[fromX][fromY]
        fields[fromX][fromY] = 0
        enemy = 2 if player == 1 else 1
        x, y = fromX, fromY
        tired = False
        path = []
        allWallsHits = []
        while True:
            # collision neighbours
            collNeighs = [(x + deltaX, y + deltaY)]
            if deltaX != 0 and deltaY != 0:
                collNeighs.append((x + deltaX, y))
                collNeighs.append((x, y + deltaY))

            killedEnemies = self.hit(collNeighs, fields, enemy)
            for (kx, ky) in killedEnemies:
                fields[kx][ky] = 0
            if killedEnemies:
                tired = True

            friendsHit = self.hit(collNeighs, fields, player)
            if tired and friendsHit:
                path.append((x, y, killedEnemies))
                return path

            wallsHit = [(x, y) for (x, y) in collNeighs if self.isOutside(x, y, fields)]
            common = [1 for x in wallsHit for y in allWallsHits if x == y]
            if common:
                path.append((x, y, killedEnemies, 'dead'))
                return path
            allWallsHits += wallsHit
            if tired and wallsHit:
                path.append((x, y, killedEnemies, 'dead'))
                return path

            obstacles = union(killedEnemies, friendsHit, wallsHit)

            if deltaX == 0 or deltaY == 0:
                if obstacles:
                    deltaX, deltaY = self.rotate(deltaX, deltaY, 180)
            else:
                if len(obstacles) == 1 and obstacles[0] == (x + deltaX, y + deltaY):
                    deltaX, deltaY = self.rotate(deltaX, deltaY, 180)
                else:
                    if (x + deltaX, y) in obstacles:
                        if deltaX * deltaY < 0:
                            deltaX, deltaY = self.rotate(deltaX, deltaY, -90)
                        else:
                            deltaX, deltaY = self.rotate(deltaX, deltaY, 90)
                    if (x, y + deltaY) in obstacles:
                        if deltaX * deltaY > 0:
                            deltaX, deltaY = self.rotate(deltaX, deltaY, -90)
                        else:
                            deltaX, deltaY = self.rotate(deltaX, deltaY, 90)

            x += deltaX
            y += deltaY

            path.append((x, y, killedEnemies))
