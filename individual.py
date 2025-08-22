import tsp
import copy
import random


class Individual:
    def __init__(self, tsp_instance, path=None):
        self.tsp = tsp_instance
        self.path = self.tsp.randomPath()
        self.cost = self.tsp.pathCost(self.path)

    def evaluate(self):
        self.cost = self.tsp.pathCost(self.path)
        return self.cost

    def getPath(self):
        return self.path

    def swap(self, i=None, j=None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)

        temp = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = temp

        self.evaluate()

        # print(f"Swapped cities {i}, and {j}\n")

    def inversion(self, i=None, j=None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)

        if i > j:
            i, j = j, i
        # Dist betwenn i & j
        sub_length = (j - i + 1)
        for k in range(sub_length // 2):
            self.path[i + k], self.path[j -
                                        k] = self.path[j - k], self.path[i + k]
        self.evaluate()

        # print(f"Inverted cities from {i} to {j}\n")

    def insert(self, i: int | None = None, j: int | None = None):
        if i is None and j is None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
            while i == j:
                j = random.randint(0, len(self.path) - 1)
        if i == None:
            i = random.randint(0, len(self.path) - 1)
        if j == None:
            j = random.randint(0, len(self.path) - 1)
        if i > j:
            i,j = j,i # i is now always smaller than j

        j_item = self.path.pop(j)
        self.path.insert(i,j_item)

        # print(f"Inserted city {j} to {i}\n")
    
    # Scramble function doesn't work
    def scramble(self, i: int | None = None, j: int | None = None):
        section = []
        for _i in range(j-i):
            section.append(self.path.pop(i))
        while len(section) > 0:
            rand = random.randint(0,len(section))
            self.path.insert(i,section.pop(rand))

        # print(f"Cities scrambled between {i} and {j}")

    def printPath(self):
        for i, city in enumerate(self.path):
            print(f"City {i} ({city.id}): ({city.point.x}, {city.point.y})")

    def performMutation(self, mutation_probability=0.05, mutation_type="swap"):
        random_number = random.random()
        if (random_number > mutation_probability):
            return self
        currentPath = self.path.copy()
        currentCost = self.evaluate()

        if mutation_type == "swap":
            self.swap()
        elif mutation_type == "inversion":
            self.inversion()
        elif mutation_type == "insert":
            self.insert()
        elif mutation_type == "scramble":
            self.scramble()
        else:
            print("Invalid mutation operation.")
            
        # Take and update mutated individual
        self.path = currentPath
        self.cost = currentCost
        self.evaluate()
        
        return self

    def edge_recombination(parent1, parent2):
        # Build adjacency table
        adjacency = {}

        def add_edge(city, neighbor):
            if city not in adjacency:
                adjacency[city] = set()
            adjacency[city].add(neighbor)

        for p in (parent1, parent2):
            for i in range(len(p)):
                left = p[i - 1]
                right = p[(i + 1) % len(p)]
                add_edge(p[i], left)
                add_edge(p[i], right)

        # Randomly choose starting city
        current = random.choice(parent1)
        child = [current]

        # Build route
        while len(child) < len(parent1):
            # Remove current from adjacency
            for neighbors in adjacency.values():
                neighbors.discard(current)

            # Pick next city
            if adjacency[current]:
                next_city = min(adjacency[current],
                                key=lambda c: len(adjacency[c]))
            else:
                # If no adjacency left, choose random unused city
                unused = [c for c in parent1 if c not in child]
                next_city = random.choice(unused)

            child.append(next_city)
            current = next_city

        return child