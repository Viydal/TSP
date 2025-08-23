import math
import random


def dprint(val):
    print(val)


class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def print(self):
        print(self.x, self.y)


class City:
    point: Point

    def __init__(self, point: Point, city_id: int):
        self.point = point
        self.id = city_id

    def print(self):
        self.point.print()


class TSP:
    Cities: ["City"]
    path: ["City"]

    def __init__(self, filename: str):
        self.Cities = []
        self.path = []
        self.open(filename)
        pass

    def open(self, filename):
        f = open(filename)
        line = ""
        while line[0:9] != "DIMENSION":
            line = f.readline()
        ex, count = line.split(":")
        count = int(count)
        # print(count)
        while line[0:18] != "NODE_COORD_SECTION":
            line = f.readline()
        # print(line.strip())
        line = f.readline().strip()
        while line[0:3] != "EOF":
            # dprint(line)
            ex, x, y = line.split()
            ex = int(ex)
            y = float(y)
            x = float(x)
            self.Cities.append(City(Point(x, y), ex))
            line = f.readline().strip()
        # print(f.readline().strip())

    def pathCost(self, path=None):
        if path is None:
            path = self.path
        cost = 0
        for i in range(len(path) - 1):
            cost += path[i].point.distance(path[i + 1].point)
        cost += path[-1].point.distance(path[0].point)
        return cost

    def randomPath(self):
        cities = self.Cities.copy()
        path = []
        for i in range(len(cities)):
            path.append(cities.pop(random.randint(0, len(cities) - 1)))
        return path

    def run(self):
        pass