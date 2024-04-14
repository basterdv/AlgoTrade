from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pandas import DataFrame

path = 'C:/Users/Home/Documents/Workshop/AlgoTrade/Test_QSH/V/VTBR@TQBR/2024_04_02/trades.csv'
title = '2024_04_02'
data = pd.read_csv(path, sep=";", encoding='ANSI',
                   names=['date_time', '2', '3', 'price', 'quantity', 'delta', '7', '8'])

df = pd.DataFrame(data)
df = df.drop(columns=['2', '3', '7', '8'])

df = df.drop(np.where(df['date_time'] < 70000000)[0])

# df2 = pd.DataFrame({'Data': ['092812047']})
# df2.Data = pd.to_datetime(df2.Data, format='%H%M%S%f', errors='coerce').dt.time
# df2.Data = pd.to_datetime(df2.Data, format='%H:%M:%S.%f', errors='coerce').dt.date.replace({pd.NaT: ''})  # или .fillna('')

df['date_time'] = pd.to_datetime(df['date_time'], format='%H%M%S%f', errors='coerce')  # .dt.time

timeframe = '10min'

df = df[['quantity', 'delta', 'date_time', "price"]]

# df = df.groupby([pd.Grouper(key='Время', freq='30min')]).agg(quantity=('Количество лотов', 'sum')).reset_index()

df['price'] = df['price'].astype(str).astype(float)
df['quantity'] = pd.to_numeric(df['quantity']).astype(int)  # quantity - кол-во сделок

df.loc[df['delta'] == 'Sell', 'delta'] = df['quantity'] * (-1)  # делаю знак дельты
df.loc[df['delta'] == 'Buy', 'delta'] = df['quantity']

df = df[['quantity', 'delta', 'date_time', "price"]]

df['data_interval'] = df['date_time'].dt.floor(timeframe).dt.time
df.sort_values(by=['date_time'])

df = df.groupby(["data_interval", "price"])[['delta']].sum()
# df = df.groupby(['data_interval', 'Цена', 'Направление'])['Количество лотов'].sum().reset_index()

df_0 = df.copy(deep=True)
df_0.loc[df['delta'] >= 0, 'delta_plus'] = df_0['delta']
df_0.loc[df['delta'] < 0, 'delta_minus'] = df_0[
    'delta'].abs()  # если убрать модуль, то в разные стороны смотреть будет

# 2-й этап - отрисовка
unique_time = df.index.get_level_values(0).unique().sort_values()
unique_price = df.index.get_level_values(1).unique().sort_values()

spacing = 0.1  # a minimum distance between two consecutive horizontal lines 0.1
values1 = (1 - spacing) * df['delta'] / df[
    'delta'].max()  # relative lengths of horizontal lines - для каждого графика (кол-во сделок, дельты минус, дельты плюс)

values2 = (1 - spacing) * df_0['delta_plus'] / df_0['delta'].max()
values3 = (1 - spacing) * df_0['delta_minus'] / df_0['delta'].max()
base = DataFrame(index=unique_price)  # the widest blank frame with prices

fig, ax = plt.subplots(figsize=(20, 10))

xlabels = unique_time.astype(str)
ylabels = unique_price.astype(str)

ax.set_title("   ".join(title), fontsize=18)
ax.set_xticks(range(len(xlabels)), xlabels, rotation=45)
ax.set_yticks(range(len(ylabels)), ylabels)
ax.yaxis.set_ticks_position('right')
ax.set_xlim([-0.5, len(xlabels)])
ax.set_ylim([-1, len(ylabels)])

for i, t in enumerate(unique_time):
    # pr = base.join(df.loc[t]).squeeze()
    pr = base.join(values1.loc[t]).squeeze()
    # ax.barh(ylabels, pr, 0.3, i, color='black')  # 0.3 - толщина линии

    pr2 = base.join(values2.loc[t]).squeeze()
    ax.barh(ylabels, pr2, 0.3, i, color='green')

    pr3 = base.join(values3.loc[t]).squeeze()
    ax.barh(ylabels, pr3, 0.3, i, color='red')

fig.tight_layout()
plt.show()
