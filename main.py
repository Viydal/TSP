import tsp
import individual
import population

if __name__ == "__main__":
    tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
    individual = individual.Individual(tsp_instance)
    path = individual.path
    print(path[0].point.x, path[0].point.y)
    print(individual.evaluate(), "\n")
    individual.performMutation("inversion")
    print(individual.evaluate(), "\n")
    
    population = population.Population(tsp_instance, 50)
    
    individualList = population.getPopulation()
    population.PMXCrossover(individualList[0], individualList[1])