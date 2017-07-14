import numpy as np
import matplotlib.pylab as plt
from IPython.display import clear_output
from numpy import random as rnd

from Plots import *
from PriceAnalisys import *


def gen_population(population_size, parameter_size):
	return rnd.rand(population_size * parameter_size).reshape((population_size, parameter_size))


def fit(population, database_id, max_days, oper_weight):
	return np.asarray([get_gain(database_id, p, max_days, oper_weight) for p in population])


def cross_pop(population):
	rnd.shuffle(population)

	for i in range(1, len(population), 2):
		cut = 2
		p1, p2 = population[i - 1:i + 1][0], population[i - 1:i + 1][1]
		p3, p4 = np.concatenate((p1[0:cut], p2[cut:4])),
		np.concatenate((p2[0:cut], p1[cut:4]))
	population[i - 1:i + 1] = np.array([p3, p4])
	return population


def crossover(population, big_fits, database_id, max_days, elite=0.2, mutation=0.2, oper_weight=10):
	fits = big_fits[:, 0]
	population = population[np.argsort(-fits)]
	population_size = len(fits)
	elite_size = int(population_size * elite)
	new_population = cross_pop(population[elite_size:])

	select_mutables = rnd.rand(population_size - elite_size) < mutation
	mutant_size = sum(select_mutables)
	new_population[select_mutables, rnd.randint(0, 4, mutant_size)] = rnd.rand(mutant_size)

	new_big_fits = fit(new_population, database_id, max_days, oper_weight)

	output_population = np.concatenate((population, new_population), axis=0)
	output_fits = np.concatenate((big_fits, new_big_fits), axis=0)

	fits_order = np.argsort(-output_fits[:, 0])

	return output_population[fits_order[:population_size]], output_fits[fits_order[:population_size]]


def printPop(population, fits, max_days, print_size=10, text="Chromossome:"):
	real_print_size = int(min(abs(print_size), len(fits)) * (print_size / abs(print_size)))
	fits_order = np.argsort(-fits)
	index = range(min(0, real_print_size), max(0, real_print_size))
	for i in index:
		p = population[fits_order[i]]
		print(text, fits_order[i], "- Fit: %.2f" % fits[fits_order[i]],
		      "(%.2f,% 4d, %.2f,% 4d)" % (p[0], p[1] * max_days, p[2], p[3] * max_days))


def evaluate_ga(population_size, database_id, max_days, oper_weight):
	max_fit, mean_fit, min_fit, max_pop = list(), list(), list(), list()
	population = gen_population(population_size, parameter_size=4)
	big_fits = fit(population, database_id, max_days, oper_weight)
	fits = big_fits[:, 0]
	epoch = 0
	while epoch < 50:
		epoch += 1
		max_id = np.argmax(fits)
		max_fit.append(fits[max_id])
		mean_fit.append(np.mean(fits))
		min_fit.append(fits[np.argmax(-fits)])
		max_pop.append(population[max_id])

		clear_output()
		print("Epoch %d: min %.2f, mean %.2f, max %.2f" % (epoch, np.min(fits), np.mean(fits), np.max(fits)))
		printPop(population, fits, max_days, print_size=5)

		fig = plt.figure(figsize=(15, 4))
		plot_population(population, fits, fig, max_days)
		plot_epochs(min_fit, mean_fit, max_fit, fig)
		plot_pareto(big_fits, fig)
		plt.show()

		population, big_fits = crossover(population, big_fits, database_id, max_days, oper_weight)
		fits = big_fits[:, 0]

	return population, big_fits
