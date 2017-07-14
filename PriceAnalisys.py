import sqlite3 as lt

import numpy as np
import pandas as pd
from numba import autojit

databasePath = 'D:/projects/PriceAnalisys/Bovespa/BOVESPA'

conn = lt.connect(databasePath)
cur = conn.cursor()


def load_data(database_id=1, total_days=365, database_path='D:/projects/PriceAnalisys/Bovespa/BOVESPA'):
	conn = lt.connect(database_path)
	cur = conn.cursor()
	cur.execute('select data, preabe from atributos where id_acao = ' + str(database_id) + ' limit ' + str(total_days) + ';')
	df = pd.DataFrame(cur.fetchall(), columns=["date", "value"])
	df.date = pd.to_datetime(df.date)
	return (df)


@autojit
def is_buy_time(data, today, days=30, percent=.2):
	begin = today - pd.Timedelta(days=days)
	interval = data[(data.date > begin) & (data.date <= today)]
	today_price = interval[interval.date == today].value.iloc[0]
	smaller_prices = sum(interval.value < today_price)
	return smaller_prices / days < percent


@autojit
def is_sell_time(data, today, days=30, percent=.8):
	begin = today - pd.Timedelta(days=days)
	interval = data[(data.date > begin) & (data.date <= today)]
	today_price = interval[interval.date == today].value.iloc[0]
	greater_prices = sum(interval.value > today_price)
	return greater_prices / days > percent


def buy_sell_decision(buy, sell, mine):
	if sell == mine == True:
		return 1, False
	elif (not buy) == mine == False:
		return -1, True
	else:
		return 0, mine


@autojit
def buy_sell(buy_time, sell_time):
	bs = buy_time * 1
	it_is_mine = False
	for i, b, s in list(zip(sell_time.index, buy_time, sell_time)):
		bs[i], it_is_mine = buy_sell_decision(b, s, it_is_mine)
	bs.iloc[-1] = int(it_is_mine)
	return (bs)


@autojit
def profit(data):
	prices = data.value * data['buySell']
	operations = sum(abs(data['buySell']))
	min_price = abs(min(prices))
	gain = sum(prices)
	period = (max(data.date) - min(data.date)).days
	return gain / min_price, period, operations


def summary(database_id, buy_price, buy_days, sell_price, sell_days, range_days):
	return profit(order(database_id, [buy_price, buy_days, sell_price, sell_days], range_days))


def get_gain(database_id, parameters, range_days, oper_weight):
	gain, period, operations = profit(order(database_id, parameters, range_days))
	return np.array([gain - (oper_weight * operations / range_days), gain, operations])


def order(database_id, parameters, range_days):
	data = load_data(database_id)
	[bp, bd, sp, sd] = parameters
	bdi, sdi = np.ceil((bd * range_days, sd * range_days))
	buy_time = data.date.map(lambda x: is_buy_time(data, x, bdi, bp))
	sell_time = data.date.map(lambda x: is_sell_time(data, x, sdi, sp))
	data['buySell'] = pd.Series(buy_sell(buy_time, sell_time), index=data.index)
	return data
