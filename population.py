from individual import Individual
import random
import copy
import math
import time

import individual


class Population:
    def __init__(self, tsp, path_costs=None, size=50):
        self.individuals = []
        self.size = size
        self.tsp = tsp
        for i in range(size):
            self.individuals.append(Individual(tsp))
            
        if path_costs is None:
            self.path_costs = {}
        else:
            self.path_costs = path_costs

    def getBest(self):
        """Returns the individual with the lowest cost."""
        if not self.individuals:
            return None
        
        for individual in self.individuals:
            self.efficient_evaluate(individual)
            
        return min(self.individuals, key=lambda ind: ind.cost)

    def bestPathCost(self):
        best_cost = self.getBest()
        return best_cost
    
    def efficient_evaluate(self, individual: Individual):
        key = tuple(individual.path)
        if key not in self.path_costs:
            individual.evaluate()
            self.path_costs[key] = individual.cost
        else:
            individual.cost = self.path_costs[key]

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

    def updatePopulation(self, newPopulation: list[Individual]):
        self.individuals = newPopulation
        self.size = len(self.individuals)

    def sortPopulation(self):
        for individual in self.individuals:
            self.efficient_evaluate(individual)
            
        self.individuals.sort(key=lambda ind: ind.cost)
        return self.individuals

    def getPopulation(self):
        return self.individuals

    def orderCrossover(self, parent1, parent2):
        path_length = len(parent1.path)

        start = random.randint(0, path_length - 1)
        end = random.randint(start, path_length - 1)

        # print(f"Performing order crossover on index {start} to index {end}\n")

        child1 = [None] * path_length
        child2 = [None] * path_length

        for i in range(start, end + 1):
            child1[i] = parent1.path[i]
            child2[i] = parent2.path[i]

        remaining_cities = []

        for i in range(path_length):
            pos = i % len(parent2.path)
            if parent2.path[pos] not in child1:
                remaining_cities.append(parent2.path[pos])

        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child1[position] is None and counter < len(remaining_cities):
                child1[position] = remaining_cities[counter]
                counter = counter + 1

        # print("child1 order crossover complete.\n")

        remaining_cities = []

        for i in range(path_length):
            pos = i % len(parent1.path)
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
        self.efficient_evaluate(child1_individual)

        child2_individual = Individual(self.tsp)
        child2_individual.path = child2
        self.efficient_evaluate(child2_individual)

        # print("child2 order crossover complete.\n")

        return child1_individual, child2_individual

    def PMXCrossover(self, parent1, parent2):
        path_length = len(parent1.path)

        start = random.randint(0, path_length - 1)
        end = random.randint(start, path_length - 1)
        
        # print(f"start: {start}")
        # print(f"end: {end}")

        child1_ids = [None] * path_length
        child2_ids = [None] * path_length

        parent1_ids = [city.id for city in parent1.path]
        parent2_ids = [city.id for city in parent2.path]

        # print(parent1_ids)
        # print(parent2_ids)

        for i in range(start, end + 1):
            child1_ids[i] = parent1.path[i].id
            child2_ids[i] = parent2.path[i].id

        for i in range(start, end + 1):
            if parent2_ids[i] not in child1_ids:
                findValue = parent1_ids[i]
                index = parent2_ids.index(findValue)
                # print(f"index: {index}")
                
                while index <= end and index >= start:
                    # print(f"index: {index}")
                    findValue = parent1_ids[index]
                    index = parent2_ids.index(findValue)
                    # time.sleep(0.1)
                child1_ids[index] = parent2_ids[i]

        for i in range(len(child1_ids)):
            if child1_ids[i] is None:
                child1_ids[i] = parent2_ids[i]

        for i in range(start, end + 1):
            if parent1_ids[i] not in child2_ids:
                findValue = parent2_ids[i]
                index = parent1_ids.index(findValue)

                while index <= end and index >= start:
                    findValue = parent2_ids[index]
                    index = parent1_ids.index(findValue)

                child2_ids[index] = parent1_ids[i]

        for i in range(len(child2_ids)):
            if child2_ids[i] is None:
                child2_ids[i] = parent1_ids[i]

        individual1 = []
        individual2 = []
        for id in child1_ids:
            for j in range(path_length):
                if parent1.path[j].id == id:
                    individual1.append(parent1.path[j])
                    break
            else:  # If not found in parent1, check parent2
                for j in range(path_length):
                    if parent2.path[j].id == id:
                        individual1.append(parent2.path[j])
                        break

        for id in child2_ids:
            for j in range(path_length):
                if parent2.path[j].id == id:
                    individual2.append(parent2.path[j])
                    break
            else:  # If not found in parent2, check parent1
                for j in range(path_length):
                    if parent1.path[j].id == id:
                        individual2.append(parent1.path[j])
                        break

        child1_individual = Individual(self.tsp)
        child1_individual.path = individual1
        self.efficient_evaluate(child1_individual)

        child2_individual = Individual(self.tsp)
        child2_individual.path = individual2
        self.efficient_evaluate(child2_individual)

        return child1_individual, child2_individual

    def cycleCrossover(self, parent1, parent2):
        path_length = len(parent1.path)
        
        parent1_ids = [city.id for city in parent1.path]
        parent2_ids = [city.id for city in parent2.path]
        
        child1_ids = [None] * path_length
        child2_ids = [None] * path_length

        # Child1 creation
        parent1Cycle = {}
        parent1CycleAvoid = {}
        
        used = set()
        keep = True
        while len(used) < path_length:
            for i in range(path_length):
                if i not in used:
                    index = i
                    break

            while parent1_ids[index] not in parent1CycleAvoid:
                if keep:
                    parent1Cycle[parent1_ids[index]] = index
                parent1CycleAvoid[parent1_ids[index]] = index
                used.add(index)

                value = parent2_ids[index]
                index = parent1_ids.index(value)

            keep = not keep

        for value, key in parent1Cycle.items():
            child1_ids[key] = value

        for i in range(path_length):
            if child1_ids[i] is None:
                child1_ids[i] = parent2_ids[i]
        
        # Child2 creation
        parent2Cycle = {}
        parent2CycleAvoid = {}

        used = set()
        keep = True
        while len(used) < path_length:
            for i in range(path_length):
                if i not in used:
                    index = i
                    break

            while parent2_ids[index] not in parent2CycleAvoid:
                if keep:
                    parent2Cycle[parent2_ids[index]] = index
                parent2CycleAvoid[parent2_ids[index]] = index
                used.add(index)

                value = parent1_ids[index]
                index = parent2_ids.index(value)

            keep = not keep

        for value, key in parent2Cycle.items():
            child2_ids[key] = value

        for i in range(path_length):
            if child2_ids[i] is None:
                child2_ids[i] = parent1_ids[i]

        # Map ids back to original cities
        individual1 = []
        individual2 = []
        for id in child1_ids:
            for j in range(path_length):
                if parent1.path[j].id == id:
                    individual1.append(parent1.path[j])
                    break
            else:  # If not found in parent1, check parent2
                for j in range(path_length):
                    if parent2.path[j].id == id:
                        individual1.append(parent2.path[j])
                        break

        for id in child2_ids:
            for j in range(path_length):
                if parent2.path[j].id == id:
                    individual2.append(parent2.path[j])
                    break
            else:  # If not found in parent2, check parent1
                for j in range(path_length):
                    if parent1.path[j].id == id:
                        individual2.append(parent1.path[j])
                        break

        child1_individual = Individual(self.tsp)
        child1_individual.path = individual1
        self.efficient_evaluate(child1_individual)

        child2_individual = Individual(self.tsp)
        child2_individual.path = individual2
        self.efficient_evaluate(child2_individual)
        
        return child1_individual, child2_individual

    # Copy N individuals over to next generation and return the partially filled next generation
    def elitism(self, elite_percentage=0.1):
        elite_count = int(elite_percentage * self.size)
        if not elite_count % 2 == 0:
            elite_count += 1

        self.sortPopulation()

        # Elitism - Take the top n individuals in the population
        nextGeneration = []
        for i in range(elite_count):
            nextGeneration.append(self.individuals[i])

        return nextGeneration

    # Fitness Proportional Selection
    def fitness_proportionalSelection(self, PopulationPerRoll: int = 1, rolls: int = 3) -> list[individual.Individual]:
        self.sortPopulation()
        newPopulation: list[individual.Individual] = []
        totalFitnessSum: int = 0
        fitness: list[int] = [] # List of Fitness(cost) of each path
        for i in self.individuals:
            fitness.append(math.ceil(i.cost))
            totalFitnessSum += math.floor(i.cost)
        # For larger numbers the highest fitness individual becomes gradually less chosen.
        # To fix this for a 200 large population, about 10% of the last item needs to be added onto the total Fitness Sum.
        # Using this an approximate for other values has been created and checked to be approximatley accurate.
        totalFitnessSum = math.ceil(totalFitnessSum + fitness[-1]*(self.size/2000))

        # Loop for each Roll/Spin of the wheel
        for i in range(rolls):
            rand: int = random.randint(0, totalFitnessSum)
            WinningRolls: list[float] = []

            # Add other evenly spaced individuals to newPopulation

            #   Create list of fitness(cost) values which align with the Rolled/Spun wheel
            for j in range(PopulationPerRoll):
                WinningRolls.append(rand + j*totalFitnessSum/PopulationPerRoll)
                if WinningRolls[-1] > totalFitnessSum:
                    WinningRolls[-1] -= totalFitnessSum
            
            #   Extend newPopulation from WinningRolls
            for indiv in WinningRolls:
                sum: int = 0
                index: int = 0
                while sum < indiv and index < len(fitness):
                    sum += fitness[index]
                    index += 1
                if sum < indiv:
                    sum += fitness[-1]
                if index > 0:
                    index -= 1
                newPopulation.append(self.individuals[index % len(self.individuals)])
        
        return newPopulation

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
