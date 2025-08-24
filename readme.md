# TSP shortest path finder
This project implements a genetic algorithm-based solver to identify efficient solutions for Traveling Salesman Problem instances.
It is highly modular and customisable.

## How to use
1. Navigate to the `code` folder.
2. Replace `tsp_instances` folder as you see fit.
3. Configure genetic algorithm parameters within `main`:
   - Set population size with `size` parameter
   - Set crossover and mutation method with `crossover_method` and `mutation_method` parameters respectively
   - Set generation count with `generationCount` parameter
   - Set algorithm type: ("EA1", "EA2", "EA3")
   - Set number of elites with `elites` parameter (EA1 only)
   - Set generation gap with `generation_gap` parameter (EA3 only)
4. Run script with `python main.py`
