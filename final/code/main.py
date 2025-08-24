import tsp
import individual
import population
import evolution
import os
import numpy as np
import local_search

if __name__ == "__main__":
    tsp_file = "pcb442.tsp"
    # # Load tsp instances
    # tsp_files = os.listdir("tsp_instances")
    # tsp_files.sort()

    # # Loop through each TSP instance
    # # Loop through each TSP instance
    # for tsp_file in tsp_files:
    print(f"Processing instance: {tsp_file}")
    tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")

    all_costs = []

    # Repeat 30 times with random initial paths
    for run in range(30):
        initial_path = tsp_instance.randomPath()
        improved_path = local_search.LocalSearch.jump(tsp_instance, initial_path)
        cost = tsp_instance.pathCost(improved_path)
        all_costs.append(cost)

    min_cost = round(np.min(all_costs), 2)
    mean_cost = round(np.mean(all_costs), 2)
    
    print(f"Finished {tsp_file}: Min={min_cost}, Mean={mean_cost}")

   
   
   
   
    # # Load tsp_instances

    # tsp_files = os.listdir("tsp_instances")
    # tsp_files.sort()
    
    # # Loop through each tsp instance
    # for tsp_file in tsp_files:
    #     # Store best recorded path in population in data list
    #     print(f"Instance: {tsp_file}")
        
    #     # Create tsp instance
    #     tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")
        
    #     # Create random assortment of individuals with specified size
    #     pop = population.Population(tsp_instance, size=50)
        
    #     # Perform evolutionary algorithm EA3 (can be changed), provide crossover and mutation methods as well as generation count
    #     evo = evolution.Evolution()
    #     best_individual = evo.handleEA(population=pop, elites=0.1, generationCount=20000, crossover_method="order", mutation_method="swap", algorithm_type="EA2", generation_gap=0.5)
        
    #     # Print average cost and std deviation for an instance with generationCount 20000 and population size 50
    #     print(f"Best cost: {round(best_individual.cost, 2)}\n")