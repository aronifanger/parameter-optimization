import numpy as np
from PriceAnalisys import get_gain
from Plots import plot_grid


def generate_grid():
	range_days_norm = np.arange(0.10, 1.10, 0.10)
	range_percent_buy = np.arange(0.05, 0.55, 0.05)
	range_percent_sell = np.arange(0.55, 1.05, 0.05)

	return range_days_norm, range_percent_buy, range_percent_sell


def evaluate_grid(database_id, max_days, oper_weight):
	range_days_norm, range_percent_buy, range_percent_sell = generate_grid()
	grid = list()
	gain = list()
	for bp in range_percent_buy:
		for bd in range_days_norm:
			for sp in range_percent_sell:
				for sd in range_days_norm:
					grid.append(np.array([bp, bd, sp, sd]))
					gain.append(get_gain(database_id, [bp, bd, sp, sd], max_days, oper_weight))
					plot_grid(parameters=np.array(grid), big_fits=np.array(gain),
					          max_days=max_days, freeze_perc=bp, freeze_days=bd)

	return np.array(grid, gain)
