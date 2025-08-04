def dprint(val):
    print(val)

class Point:
    x: int
    y: int
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y
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
    def __init__(self,filename: str):
        self.Cities = []
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
            self.Cities.append(City(Point(x,y)))
            line = f.readline().strip()
        #print(f.readline().strip())

#travel = TSP("st70.tsp")
travl = TSP("eil101.tsp")
for i in travl.Cities:
    i.print()