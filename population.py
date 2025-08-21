from individual import Individual
import random
import copy


class Population:
    def __init__(self, tsp, size, mutation=None):
        self.individuals = []
        self.size = size
        self.tsp = tsp
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

    def performCrossover(self, parent1, parent2, crossover_probability=0.8, crossover_type="order"):
        # Should crossover occur, if not return parents without modification
        random_number = random.random()
        if (random_number > crossover_probability):
            return parent1, parent2
        
        # If crossover should occur, perform crossover and return children
        if crossover_type == "order":
            child1, child2 = self.orderCrossover(parent1, parent2)
        elif crossover_type == "pmx":
            child1, child2 = self.PMXCrossover(parent1, parent2)
        elif crossover_type == "cycle":
            child1, child2 = self.cycleCrossover(parent1, parent2)
        else:
            print("Invalid crossover operation.")

        return child1, child2

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
            pos = (end + i + 1) % len(parent2.path)
            if parent2.path[pos] not in child1:
                remaining_cities.append(parent2.path[pos])

        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child1[position] is None and counter < len(remaining_cities):
                child1[position] = remaining_cities[counter]
                counter = counter + 1

        print("child1 order crossover complete.\n")

        remaining_cities = []

        for i in range(end + 1, len(parent1.path) + start):
            pos = (end + i + 1) % len(parent1.path)
            if parent1.path[pos] not in child2:
                remaining_cities.append(parent1.path[pos])

        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child2[position] is None and counter < len(remaining_cities):
                child2[position] = remaining_cities[counter]
                counter = counter + 1

        child1_individual = Individual(self.tsp)
        child1_individual.path = child1
        print(child1_individual.path)
        child1_individual.evaluate()

        child2_individual = Individual(self.tsp)
        child2_individual.path = child2
        child2_individual.evaluate()

        print("child2 order crossover complete.\n")

        return child1_individual, child2_individual

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

        child1_individual = Individual(self.tsp)
        child1_individual.path = child1
        child1_individual.evaluate()

        child2_individual = Individual(self.tsp)
        child2_individual.path = child2
        child2_individual.evaluate()

        print("child2 PMX crossover complete.\n")

        return child1_individual, child2_individual

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

        child1_individual = Individual(self.tsp)
        child1_individual.path = child1
        child1_individual.evaluate()

        child2_individual = Individual(self.tsp)
        child2_individual.path = child2
        child2_individual.evaluate()

        print("Cycle crossover complete.\n")

        return child1_individual, child2_individual

    # Copy N individuals over to next generation and return the partially filled next generation
    def elitism(self, elite_percentage=0.1):
        elite_count = int(elite_percentage * self.size)

        self.sortPopulation()

        # Elitism - Take the top n individuals in the population
        nextGeneration = []
        for i in range(elite_count):
            nextGeneration.append(self.individuals[i])

        return nextGeneration

    # tournament selection for parent selection
    def tournament_Selection(self, k=3):
        # Randomly select k individuals from the population
        tournament = random.sample(self.individuals, k)
        # Get the individual with the lowest cost
        winner = min(tournament, key=lambda ind: ind.cost)
        return winner

    # Informal tournament selection for parent selection
    # This method selects two parents using tournament selection
    # Not sure if right
    def informal_tournament_selection(self, k=3):
        parent1 = self.tournament_Selection(k)
        parent2 = self.tournament_Selection(k)
        return parent1, parent2
