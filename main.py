import tsp
import individual
import population
import evolution
import os

if __name__ == "__main__":
    tsp_files = os.listdir("tsp_instances")
    tsp_files.sort()
    
    population_sizes = [20, 50, 100, 200]
    
    generation_counts = [2000, 5000, 10000, 20000]
    
    algorithms = {
        'EA1': evolution.Evolution.EA1,
        'EA2': evolution.Evolution.EA2,
        'EA3': evolution.Evolution.EA3
    }
    
    for algorithm in algorithms:
        print(f"Algorithm: {algorithm}")
        for tsp_file in tsp_files:
            print(f"Instance: {tsp_file}\n")
            path_costs = {}
            for population_size in population_sizes:
                print(f"Population: {population_size}\n")
                print("Generations | Best Cost")
                
                tsp_instance = tsp.TSP(f"tsp_instances/{tsp_file}")
                pop = population.Population(tsp_instance, size=population_size, previous_path_costs=path_costs)
                
                best_solution = None
                current_generation = 0
                for generation_count in generation_counts:
                    generations_to_run = generation_count - current_generation
                    
                    algorithm_version = algorithms[algorithm]
                    solution = algorithm_version(pop, generations_to_run, global_best=best_solution)
                    
                    print(f"{generation_count} | {round(solution.evaluate(), 2)}")
                    
                    current_generation = generation_count
                    best_solution = solution
                    
                print()