import tsp
import copy
import random


class Individual:
    def __init__(self, tsp_instance: tsp.TSP):
        self.tsp: tsp.TSP = tsp_instance
        self.path: list[tsp.City] = self.tsp.randomPath()
        self.cost: float = self.tsp.pathCost(self.path)

    def evaluate(self) -> float:
        self.cost = self.tsp.pathCost(self.path)
        return self.cost

    def getPath(self) -> list[tsp.City]:
        return self.path

    def swap(self, i: int | None = None, j: int | None = None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)

        temp: tsp.City = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = temp

    def inversion(self, i: int | None = None, j: int | None = None):
        if i == None or j == None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
        while i == j:
            j = random.randint(0, len(self.path) - 1)

        if i > j:
            i, j = j, i
        # Dist betwenn i & j
        sub_length: int = (j - i + 1)
        for k in range(sub_length // 2):
            self.path[i + k], self.path[j - k] = self.path[j - k], self.path[i + k]

        # print(f"Inverted cities from {i} to {j}\n")


    # Randomly set i or j if not given - ensures that if this occurs i & j are different values
    def fixCityIndex(self, i: int | None, j: int | None) -> tuple[int,int]:
        if i is None and j is None:
            i = random.randint(0, len(self.path) - 1)
            j = random.randint(0, len(self.path) - 1)
            while i == j:
                j = random.randint(0, len(self.path) - 1)
        elif i is None:
            i = random.randint(0, len(self.path) - 1)
            while i == j:
                i = random.randint(0, len(self.path) - 1)
        elif j is None:
            j =  random.randint(0, len(self.path) - 1)
            while i == j:
                j =  random.randint(0, len(self.path) - 1)
        return (i,j)

    def insert(self, i: int | None = None, j: int | None = None):
        i,j = self.fixCityIndex(i,j)
        if i > j:
            i, j = j, i  # i is now always smaller than j

        j_item: tsp.City = self.path.pop(j)
        self.path.insert(i, j_item)

        # print(f"Inserted city {j} to {i}\n")

    def scramble(self, i: int | None = None, j: int | None = None):
        i,j = self.fixCityIndex(i,j)
        section: list[tsp.City] = []
        for _ in range(j-i):
            section.append(self.path.pop(i))
        
        while len(section) > 0:
            rand: int = random.randint(0, len(section)-1)
            self.path.insert(i, section.pop(rand))

        # print(f"Cities scrambled between {i} and {j}")

    def printPath(self):
        for i, city in enumerate(self.path):
            print(f"City {i} ({city.id}): ({city.point.x}, {city.point.y})")

    def performMutation(self, mutation_probability: float = 0.05, mutation_type: str = "swap") -> 'Individual':
        random_number: float = random.random()
        if (random_number > mutation_probability):
            return self

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
        self.evaluate()

        return self