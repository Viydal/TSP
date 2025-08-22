import population
import time
import random


class Evolution:
    # SGA (Simple Genetic Algorithm) with elitism
    def EA1(population: population.Population, generationCount=20000):
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
                child1, child2 = population.performCrossover(matingPool[j], matingPool[j + 1], crossover_type="pmx")
                childrenPool.append(child1)
                childrenPool.append(child2)
            
            # Perform mutation on each individual in the mating pool   
            for j in range(len(childrenPool) - 1):
                childrenPool[j] = childrenPool[j].performMutation(mutation_type="swap")
            
            # New population
            nextGeneration.extend(childrenPool)
            population.updatePopulation(nextGeneration)
            
            if i % 100 == 0:
                print(f"generation: {i} - best path with cost: {population.bestPathCost()}")
            
        return population.getBest()

    def EA2():
        pass

    def EA3():
        pass