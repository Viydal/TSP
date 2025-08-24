import tsp
import individual
import population
import evolution
import os
import numpy as np

if __name__ == "__main__":
    tsp_files = os.listdir("tsp_instances")
    tsp_files.sort()
    
    for tsp_file in tsp_files:
        data = []
        print(f"Instance: {tsp_file}")
        for index in range(30):
            tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")
            pop = population.Population(tsp_instance, size=50)
            
            best_individual = evolution.Evolution.EA3(pop, generationCount=20000)
            data.append(round(best_individual.evaluate(), 2))
        
        average_cost = np.mean(data)
        std_deviation = np.std(data)
        
        print(f"Average Cost: {round(average_cost, 2)} | Standard deviation: {round(std_deviation, 2)}\n")