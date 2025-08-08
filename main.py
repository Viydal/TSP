import tsp
from population import Population

if __name__ == "__main__":
  # travel = TSP("st70.tsp")
  travel = tsp.TSP("tsp_instances/eil101.tsp")
  travel.path = travel.randomPath()
  print(travel.pathCost())
  
  
    # travel = tsp.TSP("tsp_instances/eil101.tsp")  # <-- test on a small file first
    # print(f"Loaded {len(travel.Cities)} cities.")

    # # Check random path generation
    # travel.path = travel.randomPath()
    # print("Random tour cost:", travel.pathCost())

    # # Test population creation with mutation
    # pop = Population(travel, size=10, mutation='inversion')

    # for i, ind in enumerate(pop.individuals):
    #     print(f"Individual {i} cost: {ind.cost}")

    # best = pop.getBest()
    # print("Best individual cost:", best.cost)
