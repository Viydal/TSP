import tsp
import individual
import population
import evolution

if __name__ == "__main__":
    # Load a TSP instance
    tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")  # Update path as needed
    
    # Create population of size 50
    population = population.Population(tsp_instance, 50)
    
    solution1 = evolution.Evolution.EA1(population, 300)
    print(solution1.printPath())
    print(f"best solution with cost: {solution1.evaluate()}")