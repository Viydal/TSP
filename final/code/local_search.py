from tsp import TSP, City


class LocalSearch:
    @staticmethod
    def exchange(cities: list[City], i: int, j: int) -> list[City]:
        cities = cities[:]  # shallow copy to avoid modifying the original list
        n: int = len(cities)

        if i < 0 or i >= n or j < 0 or j >= n:  # edge case: if indices are out of bounds
            raise ValueError("Invalid indices for exchange operation")
        if i == j:  # edge case: if indices are the same
            return cities

        # Swap the cities at indices i and j
        cities[i], cities[j] = cities[j], cities[i]

        return cities

    # improved feature allows for global optimization
    @staticmethod
    def local_search_exchange(cities: list[City], tsp_instance: TSP) -> list[City]:
        cities = cities[:]  # shallow copy
        path: list[City] = tsp_instance.randomPath()
        improved: bool = True  # start with an assumption that we can improve the path

        while improved:
            n: int = len(path)
            best_cost: float = tsp_instance.pathCost(path)
            best_path: list[City] = path
            # try all pairs of indices to find a better path
            for i in range(n):
                for j in range(i + 1, n):

                    # exchange cities at indices i and j
                    new_path: list[City] = LocalSearch.exchange(path, i, j)
                    # calculate the cost of the new path
                    new_cost: float = tsp_instance.pathCost(new_path)

                    if new_cost < best_cost:  # found a better path
                        best_path = new_path  # update best path
                        best_cost = new_cost  # update best cost
                        improved = False

            path = best_path  # update path if improved
        #print("Improved path cost after exchange:", best_cost)
        return path

    # 2-opt neighborhood search: reverses the segment between i and j
    # Your corrected function should be:
    @staticmethod
    def two_opt_neighborhood_local_search(tour: list[City], i: int, k: int) -> list[City]:
        # 2-opt neighborhood search: reverses the segment between i and j (inclusive)
        new_tour = tour[0:i] + tour[i:k + 1][::-1] + tour[k + 1:]
        return new_tour

    @staticmethod
    def local_search_2opt(tour: list[City], tsp_instance: TSP) -> list[City]:
        # Full 2-opt local search: repeatedly applies 2-opt moves to improve the tour

        improved: bool = True
        best_tour: list[City] = tour[:]
        best_cost: float = tsp_instance.pathCost(best_tour)

        while improved:
            improved = False
            n: int = len(best_tour)

            # Try all possible 2-opt moves
            for i in range(n - 1):
                new_cost: float = best_cost
                new_tour: list[City] = best_tour
                for j in range(i + 2, n):
                    if i == 0 and j == n - 1:
                        continue  # skip full reversal
                    new_tour = best_tour[:i+1] + \
                        best_tour[i+1:j+1][::-1] + best_tour[j+1:]
                    new_cost = tsp_instance.pathCost(new_tour)
                if new_cost < best_cost:
                    best_tour, best_cost = new_tour, new_cost
                    improved = True
                    break
            if improved:
                break
        #print("Improved path cost after 2-opt:", best_cost)
        return best_tour
    @staticmethod
    def jump(tsp_instance: TSP, path: list[City]) -> list[City]:

        path = path[:]
        cost: float = tsp_instance.pathCost(path)
        improved: bool = True

        # loop through possible jumps
        while improved:
            improved = False
            for i in range(len(path)):
                for j in range(len(path)):
                    if i == j:
                        continue

                    # perform jump
                    new_path: list[City] = path[:]
                    city: City = new_path.pop(i)
                    new_path.insert(j, city)

                    # Check if new path better
                    new_cost: float = tsp_instance.pathCost(new_path)

                    if new_cost < cost:
                        path = new_path
                        cost = new_cost
                        improved = True

        return path
