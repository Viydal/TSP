import tsp
import os
from individual import Individual
from population import Population
from Local_Search import local_search
import individual
import population

import os
import sys
import random
import statistics
from datetime import datetime

# your modules
import tsp
from individual import Individual 
if __name__ == "__main__":
    # travel = tsp.TSP("st70.tsp")
    # tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
    # individual = individual.Individual(tsp_instance)
    # path = individual.path
    # print(path[0].point.x, path[0].point.y)
    # print(individual.evaluate())
    # print(individual.swap())

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
    # tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")
    # individual = individual.Individual(tsp_instance)
    # path = individual.path
    # print(path[0].point.x, path[0].point.y)
    # print(individual.evaluate(), "\n")
    # individual.performMutation("inversion")
    # print(individual.evaluate(), "\n")
    
    # Load a TSP instance
    tsp_instance = tsp.TSP("tsp_instances/eil101.tsp")  # Update path as needed

    # Create a random individual
    ind = Individual(tsp_instance)
    path = ind.getPath()  # Make sure your Individual class has getPath()
    print("Original path cost:", tsp_instance.pathCost(path), "\n")

    # EXCHANGE LOCAL SEARCH 
    # print("Performing local search (Exchange)...")
    # improved_path = local_search.LocalSearch.local_search_exchange(path, tsp_instance)

    #2 OPT LOCAL SEARCH
    print("Performing 2-opt local search...")
    improved_path_2opt = local_search.LocalSearch.local_search_2opt(path, tsp_instance)


    population = population.Population(tsp_instance, 50)

    individualList = population.getPopulation()
    # nextGen = population.elitism()

    # for i in range(len(nextGen)):
    #     print(nextGen[i].cost)


########################################### BRIAN ##########################################
# import statistics as stats

# # import instances
# INSTANCES = [
#     "eil51.tsp", "eil76.tsp", "eil101.tsp", "st70.tsp",
#     "kroA100.tsp", "kroC100.tsp", "kroD100.tsp", "lin105.tsp", "pcb442.tsp", "pr2392.tsp", "usa13509.tsp"
# ]

# def main():
#     # results directory
#     os.makedirs("results", exist_ok=True)
    
#     # write results header
#     with open("results/local_search.txt", "w") as f:
#         f.write("instance,algorithm,runs,min_tour_length,mean_tour_length\n")
    
#     # process each instance
#     for instance_file in INSTANCES:
#         print(f"\n=== {instance_file} ===")
        
#         # load TSP instance
#         tsp_instance = tsp.TSP(f"tsp_instances/{instance_file}")
        
#         # run exchange algorithm 30 times
#         costs = []
#         for run in range(30):
#             # create random individual
#             random.seed()  # Fresh randomness each run
#             ind = Individual(tsp_instance)
#             path = ind.getPath()
            
#             # apply local search exchange
#             improved_path = local_search.LocalSearch.local_search_2opt(path, tsp_instance)
            
#             # handle case where function returns None (modifies in-place)
#             if improved_path is None:
#                 improved_path = path
            
#             # calculate cost and store
#             cost = tsp_instance.pathCost(improved_path)
#             costs.append(cost)
            
#             # progress indicator
#             if (run + 1) % 10 == 0:
#                 print(f"  Run {run + 1}/30 complete")
        
#         # calculate min and mean
#         min_cost = min(costs)
#         mean_cost = stats.fmean(costs)
        
#         print(f"  Min: {min_cost:.6f}, Mean: {mean_cost:.6f}")
        
#         # write to results file
#         with open("results/local_search.txt", "a") as f:
#             f.write(f"{instance_file},2opt,30,{min_cost:.6f},{mean_cost:.6f}\n")
    
#     print(f"\nDone! Results written to results/local_search.txt")

# if __name__ == "__main__":
    main()