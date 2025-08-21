from tsp import TSP, City

class LocalSearch:

    def exchange(cities, i, j):
        cities = cities[:] #shallow copy to avoid modifying the original list
        n = len(cities)

        if i < 0 or i >= n or j < 0 or j >= n: #edge case: if indices are out of bounds
            raise ValueError("Invalid indices for exchange operation")
        if i == j: #edge case: if indices are the same
            return cities

        #Swap the cities at indices i and j
        cities[i], cities[j] = cities[j], cities[i]

        return cities

    #improved feature allows for global optimization
    def local_search_exchange(cities, tsp_instance):
        cities = cities[:]  # shallow copy
        path = tsp_instance.randomPath()
        improved = True # start with an assumption that we can improve the path

        while improved:
            n = len(path) 
            best_cost = tsp_instance.pathCost(path)
            best_path = path
            # try all pairs of indices to find a better path
            for i in range(n):
                for j in range(i + 1, n):

                    new_path = LocalSearch.exchange(path, i, j) # exchange cities at indices i and j
                    new_cost = tsp_instance.pathCost(new_path) # calculate the cost of the new path

                    if new_cost < best_cost: # found a better path
                        best_path = new_path # update best path
                        best_cost = new_cost # update best cost
                        improved = False 

            path = best_path  # update path if improved
        print("Improved path cost after exchange:", best_cost)
        return 
    
    # 2-opt neighborhood search: reverses the segment between i and j
    # Your corrected function should be:



    def two_opt_neighborhood_local_search(tour, i, k):
        #2-opt neighborhood search: reverses the segment between i and j (inclusive)
        new_tour = tour[0:i] + tour[i:k + 1][::-1] + tour[k + 1:]
        return new_tour
    
    def local_search_2opt(tour, tsp_instance):
        #Full 2-opt local search: repeatedly applies 2-opt moves to improve the tour
        
        improved = True
        best_tour = tour[:]
        best_cost = tsp_instance.pathCost(best_tour)
        
        
        while improved:
            improved = False
            n = len(best_tour)
            
            # Try all possible 2-opt moves
            for i in range(n - 1):
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1:
                        continue  # skip full reversal
                    
                    new_tour = best_tour[:i+1] + best_tour[i+1:j+1][::-1] + best_tour[j+1:]
                    new_cost = tsp_instance.pathCost(new_tour)
                if new_cost < best_cost:
                    best_tour, best_cost = new_tour, new_cost
                    improved = True
                    break
            if improved:
                break
        print("Improved path cost after 2-opt:", best_cost)
        return 