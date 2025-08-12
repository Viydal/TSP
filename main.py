import tsp
import individual
from population import Population

if __name__ == "__main__":
    tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
    individual = individual.Individual(tsp_instance)
    path = individual.path
    print(path[0].point.x, path[0].point.y)
    print(individual.evaluate(), "\n")
    individual.performMutation("inversion")
    print(individual.evaluate(), "\n")