import tsp
from population import Population
from individual import Individual

if __name__ == "__main__":
  # travel = TSP("st70.tsp")
  tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
  
  individual = Individual(tsp_instance)
  path = individual.path
  print(path[0].point.x, path[0].point.y)
  print(individual.evaluate())
