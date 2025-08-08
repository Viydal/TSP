import tsp
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