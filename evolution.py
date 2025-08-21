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
            
            # Create mating pool for next generation
            matingPool = []
            for i in range(population.size - len(nextGeneration)):
                matingPool.append(population.tournament_Selection())
            
            # Shuffle mating pool
            random.shuffle(matingPool)
            
            for i in range(len(matingPool) - 1):
                population.performCrossover(matingPool[i], matingPool[i + 1], crossover_type="order")
                
                
            time.sleep(1)

    def EA2():
        pass

    def EA3():
        pass