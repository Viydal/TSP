import population
import time
import random


class Evolution:
    # SGA (Simple Genetic Algorithm) with elitism
    def EA1(population: population.Population, generationCount=20000):
        for i in range(generationCount):
            nextGeneration = []
            nextGeneration.extend(population.elitism())
            
            for i in range(len(nextGeneration)):
                print(nextGeneration[i])
            
            # Future children
            nextChildren = []
            
            # Create mating pool of individuals for next generation
            matingPool = []
            for i in range(population.size - len(nextGeneration)):
                matingPool.append(population.tournament_Selection())
            
            # Shuffle mating pool
            random.shuffle(matingPool)
            
            # Perform crossover for each pair of individuals in the mating pool
            for i in range(0, len(matingPool), 2):
                child1, child2 = population.performCrossover(matingPool[i], matingPool[i + 1], crossover_type="order")
                nextChildren.append(child1)
                nextChildren.append(child2)
            
            # Perform mutation on each individual in the mating pool   
            for i in range(len(nextChildren) - 1):
                nextChildren[i] = nextChildren[i].performMutation()
            
            # New population
            nextGeneration.extend(nextChildren)
            population.updatePopulation(nextGeneration)
            
            print(f"population size of: {population.size}")
            print(f"best path with cost: {population.bestPathCost()}")
            
            # time.sleep(1)

    def EA2():
        pass

    def EA3():
        pass