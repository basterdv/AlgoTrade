from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

path = 'C:/Users/Home/Documents/Workshop/AlgoTrade/Test_QSH/V/VTBR@TQBR/2024_04_05/trades.csv'

# data = pd.read_csv(path, names=('A', 'B', 'C', 'D'),index_col=0)
data = pd.read_csv(path, sep=";", encoding='ANSI',
                   names=['Время', '2', '3', 'Цена', 'Количество лотов', 'Направление', '7', '8'])

df = pd.DataFrame(data)
df = df.drop(columns=['2', '3', '7', '8'])

df = df.drop(np.where(df['Время'] < 70000000)[0])

# df2 = pd.DataFrame({'Data': ['092812047']})
# df2.Data = pd.to_datetime(df2.Data, format='%H%M%S%f', errors='coerce').dt.time
# df2.Data = pd.to_datetime(df2.Data, format='%H:%M:%S.%f', errors='coerce').dt.date.replace({pd.NaT: ''})  # или .fillna('')

df['Время'] = pd.to_datetime(df['Время'], format='%H%M%S%f', errors='coerce')  # .dt.time

timeframe = '10min'
df2 = df.copy(deep=True)
print(df2)
df['data_interval'] = df['Время'].dt.floor(timeframe).dt.time
df1 = df.groupby(['data_interval'])['Цена'].sum()  # шкала время

# df2 = df2.sort_values(by=["Цена"], ascending=[False])
# df2.index = df2['Цена']


df = df.groupby(['data_interval', 'Направление', 'Цена'])["Количество лотов"].sum().reset_index()
df2.index = df2['Время']
df2 = df2['Цена'].resample(timeframe)  #.ohlc(_method='ohlc')
print(df2)
# print(df.loc[0,'data_interval'])
# print(df.loc[0,'Количество лотов'])

# отрисовка
fig, ax = plt.subplots(figsize=(50, 20))

unique_time = df.index.get_level_values(0).unique().sort_values()
unique_price = df2.index.get_level_values(0).unique().sort_values()

ylabels = unique_time.astype(str)
xlabels = unique_price.astype(str)
# ylabels = df['Цена'].astype(str)
# xlabels = df['data_interval'].astype(str)

# for i, t in enumerate(unique_time):
    # print(xlabels[i])
    # ax.barh(i, ylabels[i], 0.3, i, color='green')
# for i in range(len(df)):
#     # print(df.loc[i, 'data_interval'], df.loc[i, 'Цена'])
#     # ax.barh(xlabels, ylabels, 0.3, i, color='green')

# plt.show()
