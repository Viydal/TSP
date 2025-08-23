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
    def EA2(population, generationCount=20000):
        for gen in range(generationCount):
            
            # Parent selection
            parent1 = population.tournament_Selection()
            parent2 = population.tournament_Selection()
            
            # Crossover and mutation
            child1, child2 = population.performCrossover(parent1, parent2, crossover_type="order")
            child = random.choice([child1, child2])
            child = child.performMutation(mutation_type="insert")
            
            # replace worst
            worst = max(population.individuals, key=lambda ind: ind.cost)
            population.individuals.remove(worst)
            population.individuals.append(child)
            
            if gen % 100 == 0:
                print(f"Generation {gen} - best cost: {population.bestPathCost()}")
        
        return population.getBest()

    def EA3():
        pass