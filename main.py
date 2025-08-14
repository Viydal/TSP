import tsp
from individual import Individual
from population import Population
import individual
import population

if __name__ == "__main__":
#   travel = TSP("st70.tsp")
#   tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
#   individual = individual.Individual(tsp_instance)
#   path = individual.path
#   print(path[0].point.x, path[0].point.y)
#   print(individual.evaluate())
#   print(individual.swap())
    
    
    
    # Code to test edge recombination
    # # Load a TSP instance
    # tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
    # print(f"Loaded {len(tsp_instance.Cities)} cities.")

    # # Create two random parent individuals
    # parent1 = Individual(tsp_instance)
    # parent2 = Individual(tsp_instance)

    # print("Parent 1 cost:", parent1.cost)
    # print("Parent 2 cost:", parent2.cost)

    # # Perform edge recombination
    # from individual import Individual  # ensure edge_recombination is accessible
    # child_path = Individual.edge_recombination(parent1.getPath(), parent2.getPath())
    
    # # Wrap the child path into a new Individual
    # child = Individual(tsp_instance, path=child_path)

    # print("Child cost:", child.cost)

    # # Optional: print first 5 cities in the paths for verification
    # print("Parent 1 path (first 5 cities):", [c.id for c in parent1.getPath()[:50]])
    # print("Parent 2 path (first 5 cities):", [c.id for c in parent2.getPath()[:50]])
    # print("Child path (first 5 cities):", [c.id for c in child.getPath()[:50]])

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
