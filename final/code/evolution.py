from population import Population
import time
import random
import copy
from individual import Individual


class Evolution:
    # SGA (Simple Genetic Algorithm) with elitism
    def EA1(population: population.Population, elites=0.1, generationCount=20000, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best: Individual | None = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)

        for i in range(generationCount):
            nextGeneration: list[Individual] = []
            nextGeneration.extend(population.elitism(elite_percentage=elites))

            # Future children
            childrenPool: list[Individual] = []

            # Create mating pool of individuals for next generation
            matingPool: list[Individual] = []
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
                childrenPool[j] = childrenPool[j].performMutation(mutation_type=mutation_method)

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
    def EA2(population: population.Population, generationCount=20000, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best: Individual | None = population.getBest()
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

            population.individuals = population.individuals[:-2] + [child1, child2]

            currentBest: Individual | None = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)

            # if gen % 100 == 0:
            #     print(f"generation: {gen} - best path with cost: {round(global_best.cost, 2)}")

        return global_best

    # Generation Gap
    def EA3(population: population.Population, generationCount=20000, generation_gap=0.5, crossover_method="order", mutation_method="insert", global_best=None):
        # Pass global best between generations
        if global_best is None:
            initial_best: Individual | None = population.getBest()
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
            survivors = population.individuals[:population.size - num_to_replace]

            # Perform tournament selection to construct the mating pool
            matingPool = []
            for j in range(num_to_replace):
                matingPool.append(population.tournament_Selection())

            random.shuffle(matingPool)
            
            # Create new individuals
            newIndividuals = []
            for j in range(0, num_to_replace, 2):
                if j + 1 >= len(matingPool):
                    parent2: Individual = population.tournament_Selection()
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