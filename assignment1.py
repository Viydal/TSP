import math
import random

def dprint(val):
    print(val)

class Point:
    x: int
    y: int
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y
    def distance(self,other):
        return math.sqrt(math.pow(self.x-other.x,2)+math.pow(self.y-other.y,2))
    def print(self):
        print(self.x,self.y)


class City:
    point: Point
    def __init__(self,point: Point):
        self.point = point
    def print(self):
        self.point.print()


class TSP:
    Cities: ['City']
    path: ['City']
    def __init__(self,filename: str):
        self.Cities = []
        self.path = []
        self.open(filename)
        pass
    def open(self,filename):
        f = open(filename)
        line = ""
        while line[0:9] != "DIMENSION":
            line = f.readline()
        ex, count = line.split(":")
        count = int(count)
        #print(count)
        while line[0:18] != "NODE_COORD_SECTION":
            line = f.readline()
        #print(line.strip())
        line = f.readline().strip()
        while line[0:3] != "EOF":
            #dprint(line)
            ex, x, y = line.split()
            ex = int(ex)
            y = int(y)
            x = int(x)
            self.Cities.append(City(Point(x,y)))
            line = f.readline().strip()
        #print(f.readline().strip())
    def pathCost(self,path = None):
        if path is None:
            path = self.path
        cost =  0
        for i in range(len(path)-1):
                cost += path[i].point.distance(path[i+1].point)
        cost += path[-1].point.distance(path[0].point)
        return cost
    def randomPath(self):
        cities = self.Cities
        path = []
        for i in range(len(cities)):
            path.append(cities.pop(random.randint(0, len(cities)-1)))
        return path
    def run(self):
        pass

# This exchanges two cities/points in the citie list/array

# Tutor said keep it min to just 2 points for simplicity
def exchange(cities:['City'], i: int, j: int):
    #Checks within bounds of the path
    if i < 0 or i >= len(cities) or j < 0 or j >= len(cities):
        raise IndexError("Index out of bounds")
    #Edge case where they input same index
    if i == j:
        return
    cities[i], cities[j] = cities[j], cities[i]

# Implement local search using the exchange function
def localSearch(cities:['City']):
    improved = True
    while improved:
        improved = False
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                # Swap cities i and j
                exchange(cities, i, j)
                # Check if the new path is better
                if TSP.pathCost(cities) < TSP.pathCost():
                    improved = True
                else:
                    # Swap back if not better
                    exchange(cities, i, j)

travl = TSP("eil101.tsp")
travl.path = travl.randomPath()
print(travl.pathCost())