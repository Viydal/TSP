def dprint(val):
    print(val)

class Point:
    x: int
    y: int
    def __init__(self,x: int, y: int):
        self.x = x
        self.y = y


class agent:
    point: Point
    def __init__(self,point: Point):
        self.point = point


class TSP:
    agents: [int]
    def __init__(self,filename: str):
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
        print(line.strip())
        while line[0:3] != "EOF":
            line = f.readline().strip()
            ex, x, y = line.split()
            self.agents.append(agent(Point(x,y)))
        print(f.readline().strip())

#travel = TSP("st70.tsp")
travl = TSP("eil101.tsp")