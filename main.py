import tsp
# import individual
# import population

if __name__ == "__main__":
  # travel = TSP("st70.tsp")
  travel = tsp.TSP("tsp_instances/eil101.tsp")
  travel.path = travel.randomPath()
  print(travel.pathCost())
