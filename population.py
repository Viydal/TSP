import individual

class Population:
    def __init__(self, size):
        self.individuals = [Individual() for _ in range(size)]
            
    def getBest(self):
        """Returns the individual with the lowest cost."""
        for individual in self.individuals:
            temp = individual.evaluate()
            if (temp < min_cost):
                min_cost = temp
        return min_cost