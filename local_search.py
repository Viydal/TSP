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
        improved = True

        while improved:
            improved = False
            n = len(path)
            best_cost = tsp_instance.pathCost(path)
            best_path = path

            for i in range(n):
                for j in range(i + 1, n):
                    new_path = LocalSearch.exchange(path, i, j)
                    new_cost = tsp_instance.pathCost(new_path)

                    if new_cost < best_cost:
                        best_path = new_path
                        best_cost = new_cost
                        improved = True

            path = best_path  # update path if improved

        return path
    
    #