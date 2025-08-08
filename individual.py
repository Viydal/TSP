

class Individual:
    def __init__(self, tsp, mutation=None):
        self.tsp = tsp
        self.path = self.tsp.path
        self.cost = self.tsp.pathCost(self.path)
        
        if mutation == 'inversion':
            self.inversion()
        elif mutation == 'swap':
            self.swap()
        elif mutation == 'insert':
            self.insert()
        
    def evaluate(self):
        self.cost = self.tsp.pathCost(self.path)
        return self.cost
    
    def inversion(self):
        import random
        i = random.randint(0, len(self.path) - 1)
        j = random.randint(0, len(self.path) - 1)
        if i > j:
            i, j = j, i
        # Dist betwenn i & j
        sub_length = (j - i + 1)
        for k in range(sub_length // 2):
            self.path[i + k], self.path[j - k] = self.path[j - k], self.path[i + k]
        self.evaluate()