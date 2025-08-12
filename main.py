import tsp
import individual
from population import Population

if __name__ == "__main__":
  # travel = TSP("st70.tsp")
  # tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
  # individual = individual.Individual(tsp_instance)
  # path = individual.path
  # print(path[0].point.x, path[0].point.y)
  # print(individual.evaluate())
  # print(individual.swap())


    travel = tsp.TSP("tsp_instances/eil101.tsp")
    print(f"Loaded {len(travel.Cities)} cities.")

    # Check random path generation
    travel.path = travel.randomPath()
    print("Random tour cost:", travel.pathCost())

    # Test population creation with mutation
    pop = Population(travel, size=10, mutation='inversion')

    sum = 0
    
    for i, ind in enumerate(pop.individuals):
        print(f"Individual {i} cost: {ind.cost}")
        sum += ind.cost


    mean_cost = sum / len(pop.individuals)
    best = pop.getBest()
    print("Best individual cost:", best.cost)
    print("Mean cost:", mean_cost)