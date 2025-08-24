import math
import random

class Point:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance(self, other: 'Point') -> float:
        return math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))

    def print(self):
        print(self.x, self.y)


class City:
    point: Point
    id: int

    def __init__(self, point: Point, city_id: int):
        self.point = point
        self.id = city_id

    def print(self):
        self.point.print()


class TSP:
    Cities: list[City]
    path: list[City]

    def __init__(self, filename: str):
        self.Cities = []
        self.path = []
        self.open(filename)

    # Open a .tsp file and readin all cities
    def open(self, filename):
        f = open(filename)
        line: str = ""

        while line[0:9] != "DIMENSION":
            line = f.readline()
        _, count = line.split(":")
        count = int(count)

        while line[0:18] != "NODE_COORD_SECTION":
            line = f.readline()
        line = f.readline().strip()

        # Read in cities
        while line[0:3] != "EOF":
            city_id, x, y = line.split()
            city_id = int(city_id)
            y = float(y)
            x = float(x)
            self.Cities.append(City(Point(x, y), city_id))
            line = f.readline().strip()

    # Calculate the cost of a path - defaults to the tsp instances path if not provided
    def pathCost(self, path: list[City] | None = None) -> float:
        if path is None:
            path = self.path
        cost: float = 0
        for i in range(len(path) - 1):
            cost += path[i].point.distance(path[i + 1].point)

        # Add the path cost from the last city to the first, to complete the loop
        cost += path[-1].point.distance(path[0].point)
        return cost

    # Create a random path from the tsp instances cities
    def randomPath(self) -> list[City]:
        cities: list[City] = self.Cities.copy()
        path: list[City] = []
        for i in range(len(cities)):
            path.append(cities.pop(random.randint(0, len(cities) - 1)))
        return path