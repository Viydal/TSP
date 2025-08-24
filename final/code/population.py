from individual import Individual
import random
import copy
import math
import time
import tsp
import individual


class Population:
    # Initialise a list of individuals as a population
    def __init__(self, tsp: tsp.TSP, previous_path_costs: dict[tuple[tsp.City, ...],float] | None = None, size: int = 50):
        self.individuals: list[Individual] = []
        self.size: int = size
        self.tsp: 'tsp.TSP' = tsp
        for i in range(size):
            self.individuals.append(Individual(tsp))

        # If the instance has been used previously, load a dictionary of previous costs to allow for more efficient execution
        if previous_path_costs is None:
            self.path_costs: dict[tuple['tsp.City', ...],float] = {}
        else:
            self.path_costs = previous_path_costs

    # Return the best individual within the population
    def getBest(self):
        if not self.individuals:
            return None

        return min(self.individuals, key=lambda ind: ind.cost)

    # Return the best path cost from the population
    def bestPathCost(self):
        best_cost = self.getBest()
        return best_cost.cost

    # Only evaluate the cost of a path if it hasn't been seen before, if it has been seen use O(1) dictionary look up
    def efficient_evaluate(self, individual: Individual):
        key: tuple[tsp.City, ...] = tuple(individual.path)
        if key not in self.path_costs:
            individual.evaluate()
            self.path_costs[key] = individual.cost
        else:
            individual.cost = self.path_costs[key]

    # Generalised function to centralise the execution of a crossover
    def performCrossover(self, parent1, parent2, crossover_probability=0.8, crossover_type="order"):
        # Should crossover occur, if not return parents without modification
        random_number: float = random.random()
        if (random_number > crossover_probability):
            return parent1, parent2

        # If crossover should occur, perform crossover and return children
        child1: Individual
        child2: Individual
        if crossover_type == "order":
            child1, child2 = self.orderCrossover(parent1, parent2)
        elif crossover_type == "pmx":
            child1, child2 = self.PMXCrossover(parent1, parent2)
        elif crossover_type == "cycle":
            child1, child2 = self.cycleCrossover(parent1, parent2)
        else:
            print("Invalid crossover operation.")

        # Evaluate the new children
        self.efficient_evaluate(child1)
        self.efficient_evaluate(child2)

        return child1, child2

    # Update population with new list of individuals
    def updatePopulation(self, newPopulation: list[Individual]):
        self.individuals = newPopulation
        self.size = len(self.individuals)

    # Sort population by path cost of individuals
    def sortPopulation(self) -> list[Individual]:
        self.individuals.sort(key=lambda ind: ind.cost)
        return self.individuals

    # Get the list of individuals that makes up the population
    def getPopulation(self) -> list[Individual]:
        return self.individuals

    # Perform order crossover with two parents
    def orderCrossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual,Individual]:
        path_length = len(parent1.path)

        # Take index for random section
        start: int = random.randint(0, path_length - 1)
        end: int = random.randint(start, path_length - 1)
        
        # Initialise children
        child1: list[tsp.City | None] = [None] * path_length
        child2: list[tsp.City | None] = [None] * path_length

        # Copy segment from parent to children
        for i in range(start, end + 1):
            child1[i] = parent1.path[i]
            child2[i] = parent2.path[i]

        # Find which cities were not swapped in the copied segments for child1
        remaining_cities: list[tsp.City] = []
        for i in range(path_length):
            pos: int = i % len(parent2.path)
            if parent2.path[pos] not in child1:
                remaining_cities.append(parent2.path[pos])

        # Fill child1 cities with remaining cities from parent
        counter: int = 0
        for i in range(path_length):
            position: int = (end + 1 + i) % path_length
            if child1[position] is None and counter < len(remaining_cities):
                child1[position] = remaining_cities[counter]
                counter = counter + 1

        # Find which cities were not swapped in the copied segments for child2
        remaining_cities = []
        for i in range(path_length):
            pos = i % len(parent1.path)
            if parent1.path[pos] not in child2:
                remaining_cities.append(parent1.path[pos])

        # Fill child2 cities with remaining cities from parent
        counter = 0
        for i in range(path_length):
            position = (end + 1 + i) % path_length
            if child2[position] is None and counter < len(remaining_cities):
                child2[position] = remaining_cities[counter]
                counter = counter + 1

        # Create Individual objects to be directly appended within the Evolution class
        child1_individual: Individual = Individual(self.tsp)
        child1_individual.path = child1
        child2_individual = Individual(self.tsp)
        child2_individual.path = child2

        return child1_individual, child2_individual

    # Perform PMX crossover with two parents
    def PMXCrossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual,Individual]:
        path_length: int = len(parent1.path)

        # Take index for random section
        start: int = random.randint(0, path_length - 1)
        end: int = random.randint(start, path_length - 1)

        # Take index for random section
        child1_ids: list[int | None] = [None] * path_length
        child2_ids: list[int | None] = [None] * path_length

        # Take index for random section
        parent1_ids: list[int] = [city.id for city in parent1.path]
        parent2_ids: list[int] = [city.id for city in parent2.path]

        # Copy segment from parent to children
        for i in range(start, end + 1):
            child1_ids[i] = parent1.path[i].id
            child2_ids[i] = parent2.path[i].id

        # Within the copied segment of parent2, if something hasn't been copied find its suitable location within child1
        for i in range(start, end + 1):
            if parent2_ids[i] not in child1_ids:
                # Find index for the cities placement
                findValue: int = parent1_ids[i]
                index: int = parent2_ids.index(findValue)

                # If index for cities placement is again within copied segment, continue until this is no longer the case
                while index <= end and index >= start:
                    findValue = parent1_ids[index]
                    index = parent2_ids.index(findValue)
                    
                # Set index of child1 to relevant item from within parent2
                child1_ids[index] = parent2_ids[i]

        # If an index has not had something copied to it, copy directly from parent2
        for i in range(len(child1_ids)):
            if child1_ids[i] is None:
                child1_ids[i] = parent2_ids[i]

        # Within the copied segment of parent1, if something hasn't been copied find its suitable location within child2
        for i in range(start, end + 1):
            if parent1_ids[i] not in child2_ids:
                # Find index for the cities placement
                findValue = parent2_ids[i]
                index = parent1_ids.index(findValue)

                # If index for cities placement is again within copied segment, continue until this is no longer the case
                while index <= end and index >= start:
                    findValue = parent2_ids[index]
                    index = parent1_ids.index(findValue)

                # Set index of child2 to relevant item from within parent1
                child2_ids[index] = parent1_ids[i]

        # If an index has not had something copied to it, copy directly from parent1
        for i in range(len(child2_ids)):
            if child2_ids[i] is None:
                child2_ids[i] = parent1_ids[i]

        # Construct individual objects from the list of ids of children
        individual1: list[tsp.City] = []
        individual2: list[tsp.City] = []
        # Construct individual1
        for id in child1_ids:
            for j in range(path_length):
                if parent1.path[j].id == id:
                    individual1.append(parent1.path[j])
                    break
            else:  # If id not found in parent1, check parent2
                for j in range(path_length):
                    if parent2.path[j].id == id:
                        individual1.append(parent2.path[j])
                        break
        
        # Construct individual2
        for id in child2_ids:
            for j in range(path_length):
                if parent2.path[j].id == id:
                    individual2.append(parent2.path[j])
                    break
            else:  # If id not found in parent1, check parent2
                for j in range(path_length):
                    if parent1.path[j].id == id:
                        individual2.append(parent1.path[j])
                        break
        
        # Create Individual objects to be directly appended within the Evolution class
        child1_individual: Individual = Individual(self.tsp)
        child1_individual.path = individual1
        child2_individual: Individual = Individual(self.tsp)
        child2_individual.path = individual2

        return child1_individual, child2_individual

    # Perform cycle crossover with two parents
    def cycleCrossover(self, parent1: Individual, parent2: Individual) -> tuple[Individual, Individual]:
        path_length: int = len(parent1.path)

        # Take index for random section
        parent1_ids: list[int] = [city.id for city in parent1.path]
        parent2_ids: list[int] = [city.id for city in parent2.path]

        # Take index for random section
        child1_ids: list[int | None] = [None] * path_length
        child2_ids: list[int | None] = [None] * path_length

        # Find cycles within parent1, alternating between using and discarding the found cycle
        parent1Cycle: dict[int,int] = {}
        parent1CycleAvoid: dict[int,int] = {}

        # Find cycle within parent1
        used: set[int] = set()
        keep: bool = True
        while len(used) < path_length:
            for i in range(path_length):
                if i not in used:
                    index: int = i
                    break
            
            # Find cycle within parent1, if its supposed to be kept save it to appropriate array
            while parent1_ids[index] not in parent1CycleAvoid:
                if keep:
                    parent1Cycle[parent1_ids[index]] = index
                parent1CycleAvoid[parent1_ids[index]] = index
                # Add to set to ensure only unique cycles found
                used.add(index)

                value = parent2_ids[index]
                index = parent1_ids.index(value)

            keep = not keep

        # Set child1_ids to all found cycles
        for value, key in parent1Cycle.items():
            child1_ids[key] = value

        # If an index has not had something copied to it, copy directly from parent2
        for i in range(path_length):
            if child1_ids[i] is None:
                child1_ids[i] = parent2_ids[i]

        # Find cycles within parent2, alternating between using and discarding the found cycle
        parent2Cycle: dict[int, int] = {}
        parent2CycleAvoid: dict[int, int] = {}

        # Find cycle within parent2
        used = set()
        keep = True
        while len(used) < path_length:
            for i in range(path_length):
                if i not in used:
                    index = i
                    break
            
            # Find cycle within parent2, if its supposed to be kept save it to appropriate array
            while parent2_ids[index] not in parent2CycleAvoid:
                if keep:
                    parent2Cycle[parent2_ids[index]] = index
                parent2CycleAvoid[parent2_ids[index]] = index
                # Add to set to ensure only unique cycles found
                used.add(index)

                value = parent1_ids[index]
                index = parent2_ids.index(value)

            keep = not keep

        # Set child2_ids to all found cycles
        for value, key in parent2Cycle.items():
            child2_ids[key] = value

        # If an index has not had something copied to it, copy directly from parent1
        for i in range(path_length):
            if child2_ids[i] is None:
                child2_ids[i] = parent1_ids[i]

        # Construct individual objects from the list of ids of children
        individual1: list[tsp.City] = []
        individual2: list[tsp.City] = []
        for id in child1_ids:
            for j in range(path_length):
                if parent1.path[j].id == id:
                    individual1.append(parent1.path[j])
                    break
            else:  # If id not found in parent1, check parent2
                for j in range(path_length):
                    if parent2.path[j].id == id:
                        individual1.append(parent2.path[j])
                        break

        # Construct individual2
        for id in child2_ids:
            for j in range(path_length):
                if parent2.path[j].id == id:
                    individual2.append(parent2.path[j])
                    break
            else:  # If id not found in parent2, check parent1
                for j in range(path_length):
                    if parent1.path[j].id == id:
                        individual2.append(parent1.path[j])
                        break

        # Create Individual objects to be directly appended within the Evolution class
        child1_individual: Individual = Individual(self.tsp)
        child1_individual.path = individual1
        child2_individual: Individual = Individual(self.tsp)
        child2_individual.path = individual2

        return child1_individual, child2_individual

    def edge_recombination(parent1: list[tsp.City], parent2: list[tsp.City]) -> list[tsp.City]:
        # Build adjacency table
        adjacency: dict[tsp.City,set[tsp.City]] = {}

        def add_edge(city, neighbor):
            if city not in adjacency:
                adjacency[city] = set()
            adjacency[city].add(neighbor)

        for p in (parent1, parent2):
            for i in range(len(p)):
                left = p[i - 1]
                right = p[(i + 1) % len(p)]
                add_edge(p[i], left)
                add_edge(p[i], right)

        # Randomly choose starting city
        current: tsp.City = random.choice(parent1)
        child: list[tsp.City] = [current]

        # Build route
        while len(child) < len(parent1):
            # Remove current from adjacency
            for neighbors in adjacency.values():
                neighbors.discard(current)

            # Pick next city
            if adjacency[current]:
                next_city = min(adjacency[current],
                                key=lambda c: len(adjacency[c]))
            else:
                # If no adjacency left, choose random unused city
                unused = [c for c in parent1 if c not in child]
                next_city = random.choice(unused)

            child.append(next_city)
            current = next_city

        return child

    # Copy N individuals over to next generation and return the partially filled next generation
    def elitism(self, elite_percentage: float = 0.1) -> list[Individual]:
        elite_count: int = int(elite_percentage * self.size)
        # Ensure even count of individuals
        if not elite_count % 2 == 0:
            elite_count += 1

        self.sortPopulation()

        # Elitism - Take the top n individuals in the population
        nextGeneration: list[Individual] = []
        for i in range(elite_count):
            nextGeneration.append(self.individuals[i])

        # Return portion of elite individuals
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
    def tournament_Selection(self, k: int = 3) -> Individual:
        # Randomly select k individuals from the population
        tournament: list[Individual] = random.sample(self.individuals, k)
        # Get the individual with the lowest cost
        winner: Individual = min(tournament, key=lambda ind: ind.cost)
        return winner

    # Informal tournament selection for parent selection
    # This method selects two parents using tournament selection
    # Not sure if right
    def informal_tournament_selection(self, k: int = 3) -> tuple[Individual,Individual]:
        parent1: Individual = self.tournament_Selection(k)
        parent2: Individual = self.tournament_Selection(k)
        return parent1, parent2