from GA import evaluate_ga
from GridSeach import evaluate_grid


#population, fits = evaluate_ga(population_size=10, database_id=1, max_days=200, oper_weight=10)

population, gain = evaluate_grid(database_id=1, max_days=200, oper_weight=10)
