import tsp
import copy
import random


class Individual:
    def __init__(self, tsp_instance, path=None):
        self.tsp = tsp_instance
        self.path = self.tsp.randomPath()
        self.cost = self.tsp.pathCost(self.path)

    def evaluate(self):
        self.cost = self.tsp.pathCost(self.path)
        return self.cost

    def getPath(self):
        return self.path

    def swap(self, i=None, j=None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)

        temp = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = temp
        
        self.evaluate()
        
        print(f"Swapped cities {i}, and {j}\n")

    def inversion(self, i=None, j=None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)
            
        if i > j:
            i, j = j, i
        # Dist betwenn i & j
        sub_length = (j - i + 1)
        for k in range(sub_length // 2):
            self.path[i + k], self.path[j - k] = self.path[j - k], self.path[i + k]
        self.evaluate()
        
        print(f"Inverted cities from {i} to {j}\n")

    def insert(self):
        # Placeholder
        pass
    
    def printPath(self, path_list):
        for i, city in enumerate(path_list):
            print(f"City {i}: ({city.point.x}, {city.point.y})")

    def performMutation(self, mutation=None):
        currentPath = self.path.copy()
        currentCost = self.evaluate()

        if mutation == "swap":
            self.swap()
        elif mutation == "inversion":
            self.inversion()
        elif mutation == "insert":
            self.insert()
        else:
            print("Invalid mutation operation.")

        if self.evaluate() > currentCost:
            self.path = currentPath
            self.cost = currentCost