from individual import Individual
import random

class Population:
    def __init__(self, tsp, size, mutation=None):

        self.individuals = []
        for i in range(size):
            self.individuals.append(Individual(tsp))

            
    def getBest(self):
        """Returns the individual with the lowest cost."""
        min = None
        for individual in self.individuals:
            if (min == None):
                min = individual
            elif individual.evaluate() < min.cost:
                min = individual
        return min
    
    def getPopulation(self):
        return self.individuals
    
    def orderCrossover(self, parent1, parent2):
        path_length = len(parent1.path)
        
        start = random.randint(0, path_length - 1)
        end = random.randint(start, path_length - 1)
        
        print(f"Performing order crossover on index {start} to index {end}\n")
        
        child1 = [None] * path_length
        child2 = [None] * path_length
        
        for i in range(start, end + 1):
            child1[i] = parent1.path[i]
            child2[i] = parent2.path[i]
            
        remaining_cities = []
        
        for i in range(end + 1, len(parent2.path) + start):
            i = i % len(parent2.path)
            if parent2.path[i] not in child1:
                remaining_cities.append(parent2.path[i])
    
        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child1[position] is None and counter < len(remaining_cities):
                child1[position] = remaining_cities[counter]
                counter = counter + 1
                
        print("child1 order crossover complete.\n")
                
        remaining_cities = []
        
        for i in range(end + 1, len(parent1.path) + start):
            i = i % len(parent1.path)
            if parent1.path[i] not in child2:
                remaining_cities.append(parent1.path[i])
    
        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child2[position] is None and counter < len(remaining_cities):
                child2[position] = remaining_cities[counter]
                counter = counter + 1
        
        print("child2 order crossover complete.\n")
    
    def PMXCrossover(self, parent1, parent2):
        path_length = len(parent1.path)
        
        start = random.randint(0, path_length - 1)
        end = random.randint(start, path_length - 1)
        
        print(f"Performing PMX crossover on index {start} to index {end}\n")
        
        child1 = [None] * path_length
        child2 = [None] * path_length
        
        for i in range(start, end + 1):
            child1[i] = parent1.path[i]
            child2[i] = parent2.path[i]
        
        for i in range(start, end):
            if parent2.path[i] not in child1:
                print("city not in child")
                findValue = parent1.path[i]
                index = parent2.path.index(findValue)
                
                while index <= end and index >= start:
                    print("city is within crossover portion, continue.")
                    findValue = parent1.path[index]
                    index = parent2.path.index(findValue)
                    child1[index] = parent2.path[i]
        
        for i in range(len(child1)):
            if child1[i] is None:
                child1[i] = parent2.path[i]
                
        print("child1 PMX crossover complete.\n")
                
        for i in range(start, end):
            if parent1.path[i] not in child2:
                print("city not in child")
                findValue = parent2.path[i]
                index = parent1.path.index(findValue)
                
                while index <= end and index >= start:
                    print("city is within crossover portion, continue.")
                    findValue = parent2.path[index]
                    index = parent1.path.index(findValue)
                    child2[index] = parent1.path[i]
        
        for i in range(len(child1)):
            if child2[i] is None:
                child2[i] = parent1.path[i]
                
        print("child2 PMX crossover complete.\n")
            
    def cycleCrossover(self):
        pass