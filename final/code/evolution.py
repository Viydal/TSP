import population
import time
import random
import copy


class Evolution:
    # SGA (Simple Genetic Algorithm) with elitism
    def EA1(population: population.Population, generationCount=20000, global_best=None):
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)
            
        for i in range(generationCount):
            nextGeneration = []
            nextGeneration.extend(population.elitism())

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
                child1, child2 = population.performCrossover(matingPool[j], matingPool[j + 1], crossover_type="order")
                childrenPool.append(child1)
                childrenPool.append(child2)

            # Perform mutation on each individual in the mating pool
            for j in range(len(childrenPool)):
                childrenPool[j] = childrenPool[j].performMutation(mutation_type="insert")

            # New population
            nextGeneration.extend(childrenPool)
            population.updatePopulation(nextGeneration)
            
            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)
                
            # if i % 100 == 0:
            #     print(f"generation: {i} - best path with cost: {round(global_best.cost, 2)}")

        return global_best

    # SSGA
    def EA2(population: population.Population, generationCount=20000, global_best=None):
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)
            
        for gen in range(generationCount):
            parent1 = population.tournament_Selection()
            parent2 = population.tournament_Selection()
            
            child1, child2 = population.performCrossover(parent1, parent2, crossover_type="order")
            
            child1 = child1.performMutation(mutation_type="insert")
            child2 = child2.performMutation(mutation_type="insert")
            
            population.sortPopulation()
            
            population.individuals = population.individuals[:-2] + [child1, child2]
            
            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)
            
            # if gen % 100 == 0:
            #     print(f"generation: {gen} - best path with cost: {round(global_best.cost, 2)}")
        
        return global_best

    # Generation Gap
    def EA3(population: population.Population, generationCount=20000, generation_gap=0.5, global_best=None):
        if global_best is None:
            initial_best = population.getBest()
            initial_best.evaluate()
            global_best = copy.deepcopy(initial_best)
        
        num_to_replace = max(2, int(population.size * generation_gap))
        if num_to_replace % 2 != 0:
            num_to_replace += 1
        
        num_to_replace = min(num_to_replace, population.size)
        
        for gen in range(generationCount):
            population.sortPopulation()
            
            survivors = population.individuals[:population.size - num_to_replace]
            
            matingPool = []
            for j in range(num_to_replace):
                matingPool.append(population.tournament_Selection())
            
            random.shuffle(matingPool)
            
            newIndividuals = []
            for j in range(0, num_to_replace, 2):
                if j + 1 >= len(matingPool):
                    parent2 = population.tournament_Selection()
                else:
                    parent2 = matingPool[j + 1]
                
                child1, child2 = population.performCrossover(matingPool[j], parent2, crossover_type="order")
                
                child1 = child1.performMutation(mutation_type="insert")
                child2 = child2.performMutation(mutation_type="insert")
                
                newIndividuals.extend([child1, child2])
            
            newIndividuals = newIndividuals[:num_to_replace]
            
            nextGeneration = survivors + newIndividuals
            population.updatePopulation(nextGeneration)
            
            currentBest = population.getBest()
            if currentBest.cost < global_best.cost:
                global_best = copy.deepcopy(currentBest)
            
            # if gen % 100 == 0:
            #     print(f"generation: {gen} - best path with cost: {round(global_best.cost, 2)} - replaced: {num_to_replace}/{population.size}")
        
        return global_best