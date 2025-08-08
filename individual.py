class Individual:
    def __init__(self, tsp):
        self.tsp = tsp
        self.path = tsp.randomPath()
        self.cost = tsp.pathCost(self.path)
        
    def evaluate(self):
        self.cost = self.tsp.pathCost(self.path)
        return self.cost