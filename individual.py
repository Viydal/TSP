import tsp


class Individual:
    def __init__(self, tsp_instance, path=None):
        self.tsp = tsp_instance
        self.path = self.tsp.randomPath()
        self.cost = self.tsp.pathCost(self.path)

    def evaluate(self):
        self.cost = self.tsp.pathCost(self.path)
        return self.cost

    def path(self):
        return self.path

    def swap(self):
        print(self.path)