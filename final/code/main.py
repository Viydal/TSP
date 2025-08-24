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
        data = []
        print(f"Instance: {tsp_file}")
        for index in range(30):
            # Create tsp instance
            tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")
            # Create random assortment of individuals with specified size
            pop = population.Population(tsp_instance, size=50)
            
            # Perform evolutionary algorithm EA3 (can be changed), provide crossover and mutation methods as well as generation count
            best_individual = evolution.Evolution.EA3(pop, crossover_method="order", mutation_method="insert", generationCount=20000)
            # Append best result to data
            data.append(round(best_individual.evaluate(), 2))
        
        # Find mean and std deviation of data for a given instance
        average_cost = np.mean(data)
        std_deviation = np.std(data)
        
        # Print average cost and std deviation for an instance with generationCount 20000 and population size 50
        print(f"Average Cost: {round(average_cost, 2)} | Standard deviation: {round(std_deviation, 2)}\n")