from individual import Individual

class Population:
    def __init__(self, tsp, size, mutation=None):
        self.individuals = [Individual(tsp, mutation) for _ in range(size)]
            
    def getBest(self):
        """Returns the individual with the lowest cost."""
        min = None
        for individual in self.individuals:
            if (min == None):
                min = individual
            elif individual.evaluate() < min.cost:
                min = individual
        return min