from individual import Individual
import random
import copy

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
    
    def sortPopulation(self):
        individuals = self.individuals
        # Double for loop sorting the population by fitness
        for i in range(len(individuals)):
            for j in range(len(individuals) - 1):
                if individuals[j].cost > individuals[j + 1].cost:
                    temp = individuals[j]
                    individuals[j] = individuals[j + 1]
                    individuals[j + 1] = temp
        return individuals

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

    def cycleCrossover(self, parent1, parent2):
        used = set()

        child1 = [None] * len(parent1.path)
        child2 = [None] * len(parent2.path)

        parent1Cycle = {}
        parent1CycleAvoid = {}
        parent2Cycle = {}
        parent2CycleAvoid = {}

        print("Performing cycle crossover for child1\n")

        keep = True
        while len(used) < len(parent1.path):
            for i in range(0, len(parent1.path) - 1):
                if i not in used:
                    index = i
                    break

            while parent1.path[index] not in parent1CycleAvoid:
                if keep:
                    parent1Cycle[parent1.path[index]] = index
                parent1CycleAvoid[parent1.path[index]] = index
                used.add(index)

                value = parent2.path[index]
                index = parent1.path.index(value)

            if keep:
                keep = False
            else:
                keep = True

        for value, key in parent1Cycle.items():
            child1[key] = value

        for i in range(len(child1)):
            if child1[i] is None:
                child1[i] = parent2.path[i]

        print("Performing cycle crossover for child2\n")

        used = set()
        keep = True
        while len(used) < len(parent2.path):
            for i in range(0, len(parent2.path) - 1):
                if i not in used:
                    index = i
                    break

            while parent2.path[index] not in parent2CycleAvoid:
                if keep:
                    parent2Cycle[parent2.path[index]] = index
                parent2CycleAvoid[parent2.path[index]] = index
                used.add(index)

                value = parent1.path[index]
                index = parent2.path.index(value)

            if keep:
                keep = False
            else:
                keep = True

        for value, key in parent2Cycle.items():
            child2[key] = value

        for i in range(len(child2)):
            if child2[i] is None:
                child2[i] = parent1.path[i]

        print("Cycle crossover complete.\n")

    # Copy N individuals over to next generation - fill rest with 60% crossover and 40% mutation
    def elitism(self, n=10, c=None, m=None):
        # Error checking
        if c is None:
            c = 0.6 * 50 - n
        if m is None:
            m = 0.4 * 50 - n
        if n + c + m != 50:
            print(f"Invalid parameters, proposed population size of {n + c + m}")
            return
        
        individuals = self.sortPopulation()
        
        for i in range(len(individuals)):
            print(individuals[i].cost)
        print()
        
        # Elitism - Take the top n individuals in the population
        nextGeneration = []
        for i in range(n):
            nextGeneration.append(individuals[i])

    # Choose best n random individuals to cary over till next generation
    # choose k individual to carry over to next generation
    def tournament_Selection(self, k=3):

        #uses self.sortPopulation() to sort the population
        tournament = random.sample(self.individuals, k)
        
        # Select the top two individuals as parents
        winner = max(tournament, key=lambda ind: ind.evaluate())

        return winner

    # Informal tournament selection - select two parents from the population
    # This is similar to tournament selection but allows for self-mating
    def informal_tournament_selection(self, k=3):
        
        parent1 = self.tournament_Selection(k)
        parent2 = self.tournament_Selection(k)

        #returns same individuals as in GA -> there is self mating. 
        # Don't know if want to keep diversity or not

        #DIVERSITY -> INCLUDE IF WANT THIS
        # while parent1 == parent2:
        #     parent2 = self.tournament_Selection(k)
        
        return parent1, parent2
    
    # Rank of i => higher ranked individuals are more likley to win tournament 
    # Tournament size k => bigger k stronger selection pressure. With more contestants, it's 
    
    # FUNCTION ARGUMENTS:
    #   pop: list of individuals; each has .fitness

    #   k: number of contestants in each tournament

    #   replace: 
    #       if True, contestants can be selected multiple times
    #       if False, each contestant is unique in the tournament

    #   deterministic: if True, the best contestant always wins
    
    #   p: probability that the best contestant wins; if < 1.0, allows for some randomness
    def tournament_select(pop, k=3, replace=True, deterministic=True, p=1.0):
        # pop: list of individuals; each has .fitness
        contestants = (random.choices(pop, k=k) if replace
                    else random.sample(pop, k=min(k, len(pop))))
        contestants.sort(key=lambda ind: ind.fitness, reverse=True)  # higher is better

        if deterministic or p >= 1.0:
            return contestants[0]  # best always wins

        # probabilistic: best wins with prob p, otherwise pick one of the rest
        if random.random() < p:
            return contestants[0]
        # pick a non-best uniformly (you can bias by rank if you want)
        return random.choice(contestants[1:]) if len(contestants) > 1 else contestants[0]
