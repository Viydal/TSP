import tsp
import individual

if __name__ == "__main__":
  # travel = TSP("st70.tsp")
  tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
  individual = individual.Individual(tsp_instance)
  path = individual.path
  print(path[0].point.x, path[0].point.y)
  print(individual.evaluate())
  print(individual.swap())
