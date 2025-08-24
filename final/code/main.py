import tsp
import individual
import population
import evolution
import os
import numpy as np

if __name__ == "__main__":
    # Load tsp_instances
    tsp_files = os.listdir("tsp_instances")
    tsp_files.sort()
    
    # Loop through each tsp instance
    for tsp_file in tsp_files:
        # Store best recorded path in population in data list
        print(f"Instance: {tsp_file}")
        
        # Create tsp instance
        tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")
        
        # Create random assortment of individuals with specified size
        pop = population.Population(tsp_instance, size=50)
        
        # Perform evolutionary algorithm EA3 (can be changed), provide crossover and mutation methods as well as generation count
        evo = evolution.Evolution()
        best_individual = evo.handleEA(population=pop, elites=0.1, generationCount=20000, crossover_method="order", mutation_method="swap", algorithm_type="EA2", generation_gap=0.5)
        
        # Print average cost and std deviation for an instance with generationCount 20000 and population size 50
        print(f"Best cost: {round(best_individual.cost, 2)}\n")