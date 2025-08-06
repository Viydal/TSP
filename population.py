class Population:
    def __init__(self, tsp, size):
        self.individuals = [Individual(tsp) for _ in range(size)]
            
    def getBest(self):
        return min(self.individuals, key=lambda ind: ind.cost)