import population
import time
import random
import copy


class Evolution:
    # General EA handler
    def handleEA(self, population: population.Population, elites=0.1, generationCount=20000, crossover_method="order", mutation_method="insert", global_best=None, generation_gap=0.5, algorithm_type="EA1"):
        if algorithm_type == "EA1":
            return self.EA1(population, elites=elites, generationCount=generationCount, crossover_method=crossover_method, mutation_method=mutation_method, global_best=global_best)
        elif algorithm_type == "EA2":
            return self.EA2(population, generationCount=generationCount, crossover_method=crossover_method, mutation_method=mutation_method, global_best=global_best)
        elif algorithm_type == "EA3":
            return self.EA3(population, generationCount=generationCount, generation_gap=generation_gap, crossover_method=crossover_method, mutation_method=mutation_method, global_best=global_best)

    # SGA (Simple Genetic Algorithm) with elitism
    def EA1(self, population: population.Population, elites=0.1, generationCount=20000, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)

        for i in range(generationCount):
            nextGeneration = []
            nextGeneration.extend(population.elitism(elite_percentage=elites))

            # Future children
            childrenPool = []

            # Create mating pool of individuals for next generation
            matingPool = []
            for j in range(population.size - len(nextGeneration)):
                matingPool.append(population.tournament_Selection())

            # Shuffle mating pool
            random.shuffle(matingPool)

            # Perform crossover for each pair of individuals in the mating pool
            for j in range(0, len(matingPool), 2):
                child1, child2 = population.performCrossover(
                    matingPool[j], matingPool[j + 1], crossover_type=crossover_method)
                childrenPool.append(child1)
                childrenPool.append(child2)

            # Perform mutation on each individual in the mating pool
            for j in range(len(childrenPool)):
                childrenPool[j] = childrenPool[j].performMutation(
                    mutation_type=mutation_method)

            # New population
            nextGeneration.extend(childrenPool)
            population.updatePopulation(nextGeneration)

            # If current best cost is less than the globally recorded minimum, update
            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)

            # Debugging
            # if i % 100 == 0:
            #     print(f"generation: {i} - best path with cost: {round(global_best.cost, 2)}")

        return global_best

    # SSGA
    def EA2(self, population: population.Population, generationCount=20000, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)

        # For a generation in the total generations
        for gen in range(generationCount):
            parent1 = population.tournament_Selection()
            parent2 = population.tournament_Selection()

            child1, child2 = population.performCrossover(
                parent1, parent2, crossover_type=crossover_method)

            child1 = child1.performMutation(mutation_type=mutation_method)
            child2 = child2.performMutation(mutation_type=mutation_method)

            population.sortPopulation()

            population.individuals = population.individuals[:-2] + [
                child1, child2]

            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)

            # if gen % 100 == 0:
            #     print(f"generation: {gen} - best path with cost: {round(global_best.cost, 2)}")

        return global_best

    # Generation Gap
    def EA3(self, population: population.Population, generationCount=20000, generation_gap=0.5, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)

        # How much of the original population needs to be replaced
        num_to_replace = max(2, int(population.size * generation_gap))
        if num_to_replace % 2 != 0:
            num_to_replace += 1

        num_to_replace = min(num_to_replace, population.size)

        # For a generation in the total generations
        for gen in range(generationCount):
            # Sort and collect fittest individuals to pass on to next generation
            population.sortPopulation()
            survivors = population.individuals[:
                                               population.size - num_to_replace]

            # Perform tournament selection to construct the mating pool
            matingPool = []
            for j in range(num_to_replace):
                matingPool.append(population.tournament_Selection())

            random.shuffle(matingPool)

            # Create new individuals
            newIndividuals = []
            for j in range(0, num_to_replace, 2):
                if j + 1 >= len(matingPool):
                    parent2 = population.tournament_Selection()
                else:
                    parent2 = matingPool[j + 1]

                child1, child2 = population.performCrossover(
                    matingPool[j], parent2, crossover_type=crossover_method)

                # Perform mutation to children
                child1 = child1.performMutation(mutation_type=mutation_method)
                child2 = child2.performMutation(mutation_type=mutation_method)

                # Add children to new individuals array
                newIndividuals.extend([child1, child2])

            # Keep a given number of individuals
            newIndividuals = newIndividuals[:num_to_replace]

            # Construct next generation
            nextGeneration = survivors + newIndividuals
            population.updatePopulation(nextGeneration)

            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)

            # Debugging
            # if gen % 100 == 0:
            #     print(f"generation: {gen} - best path with cost: {round(global_best.cost, 2)} - replaced: {num_to_replace}/{population.size}")

        return global_best
        
    # Inver-over
    def inver_over(population, generationCount=20000, p=0.02, global_best=None):

        if global_best is None:
            global_best = copy.copy(population.getBest())
        
        for gen in range(generationCount):
            pop_list = population.getPopulation()
            new_population = []
            
            for ind in pop_list:
                # Create copy of individual
                S0 = copy.copy(ind)
                S0.path = ind.path[:]  # Copy path
                
                # Select random starting city
                c = random.choice(S0.path)
                
                while True:
                    if random.random() < p:
                        # Select random city other than c
                        other_cities = [city for city in S0.path if city.id != c.id]
                        c_prime = random.choice(other_cities)
                    else:
                        # Select random individual and get next city after c
                        other_individual = random.choice(pop_list)
                        # Find position of c in the other individual
                        c_pos = next(i for i, city in enumerate(other_individual.path) if city.id == c.id)
                        # Get next city
                        next_pos = (c_pos + 1) % len(other_individual.path)
                        c_prime = other_individual.path[next_pos]
                    
                    # Check if c' is next to c in S0
                    c_pos_in_S0 = next(i for i, city in enumerate(S0.path) if city.id == c.id)
                    n = len(S0.path)
                    
                    # Get previous and next cities of c in S0
                    prev_city = S0.path[c_pos_in_S0 - 1]
                    next_city = S0.path[(c_pos_in_S0 + 1) % n]
                    
                    # If c' is next to c, stop repeat loop
                    if c_prime.id == prev_city.id or c_prime.id == next_city.id:
                        break
                    
                    # Inverse section from next city of c to c'
                    next_c_pos = (c_pos_in_S0 + 1) % n
                    c_prime_pos = next(i for i, city in enumerate(S0.path) if city.id == c_prime.id)
                    
                    # Determine the segment to reverse
                    start_pos = next_c_pos
                    end_pos = c_prime_pos
                    
                    if start_pos <= end_pos:
                        # Reverse from start to end
                        S0.path[start_pos:end_pos + 1] = reversed(S0.path[start_pos:end_pos + 1])
                    else:
                        # Reverse the segment that wraps around
                        segment = S0.path[start_pos:] + S0.path[:end_pos + 1]
                        segment.reverse()
                        S0.path[start_pos:] = segment[:len(S0.path) - start_pos]
                        S0.path[:end_pos + 1] = segment[len(S0.path) - start_pos:]
                    
                    # Move to next city
                    c = c_prime
                
                # Evaluate both individuals if needed
                if not hasattr(ind, 'cost') or ind.cost is None:
                    ind.evaluate()
                
                # Keep better individual
                if S0.evaluate() <= ind.cost:
                    new_population.append(S0)
                else:
                    new_population.append(ind)
            
            # Update population for next generation
            population.updatePopulation(new_population)
            
            # Track best
            current_best = population.getBest()
            if current_best.cost < global_best.cost:
                global_best = copy.copy(current_best)
            
            if gen % 100 == 0:
                print(f"[Gen {gen}] Best cost: {global_best.cost}")
        
        return global_best
