import matplotlib.pyplot as plt


def plot_population(population, fits, fig, max_days):
	x1, y1, x2, y2 = population[:, 0], population[:, 1] * max_days, population[:, 2], population[:, 3] * max_days
	area = (fits + 2) * 100 + 20
	area[area < 1] = 5

	ax = fig.add_subplot(1, 3, 1)
	fig.subplots_adjust(top=0.85)
	ax.set_title('Parameters vs Fitness')
	ax.set_xlabel('Percentiles')
	ax.set_ylabel('Days')

	plt.scatter(x1, y1, s=area, cmap='Blue', alpha=0.8)
	plt.scatter(x2, y2, s=area, cmap='Red', alpha=0.8)
	for i in range(0, len(fits)):
		plt.plot((x1[i], x2[i]), (y1[i], y2[i]), color='Grey', alpha=0.1)


def plot_epochs(min_fit, mean_fit, max_fit, fig):
	ax = fig.add_subplot(1, 3, 2)
	fig.subplots_adjust(top=0.85)
	ax.set_title('Fitness function')
	ax.set_xlabel('Epoch')
	ax.set_ylabel('Fitness')

	x = [i for i, y in enumerate(min_fit)]
	plt.plot(x, min_fit, linestyle='solid', color='Red', markersize=10)
	plt.plot(x, mean_fit, linestyle='solid', color='Blue', markersize=10)
	plt.plot(x, max_fit, linestyle='solid', color='Green', markersize=10)
	plt.xlim(0, 50)


def plot_pareto(fits, fig):
	ax = fig.add_subplot(1, 3, 3)
	fig.subplots_adjust(top=0.85)
	ax.set_title('Pareto')
	ax.set_xlabel('Transactions Count')
	ax.set_ylabel('Fitness')

	plt.scatter(fits[:, 2], fits[:, 1], s=50)
	plt.xlim(0, 200)
	plt.ylim(0, 5)


def plot_grid(parameters, big_fits, max_days, freeze_perc, freeze_days):
	selected_lines = parameters[:, 0], parameters[:, 1] == freeze_perc, freeze_days
	plot_parameters = parameters[selected_lines, 2:4]
	plot_fits = big_fits[selected_lines, 0]
	norm_plot_fits = (plot_fits - min(plot_fits)) / (max(plot_fits) - min(plot_fits))

	x = plot_parameters[:, 0]
	y = plot_parameters[:, 1] * max_days
	area = (norm_plot_fits + 0.1) * 100
	rgb = [norm_plot_fits, 0, 1 - norm_plot_fits]

	fig = plt.figure(figsize=(5, 5))
	ax = fig.add_subplot(1, 1, 1)
	ax.set_title('Parameters vs Fitness')
	ax.set_xlabel('Percentiles')
	ax.set_ylabel('Days')

	plt.scatter(x, y, s=area, color=rgb)
	plt.show()

