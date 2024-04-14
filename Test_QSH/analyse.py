from datetime import datetime

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from pandas import DataFrame

path = 'C:/Users/Home/Documents/Workshop/AlgoTrade/Test_QSH/V/VTBR@TQBR/2024_04_08/trades.csv'

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
df['data_interval']  = df['data_interval'].astype(str)
df.sort_values(by=['date_time'])

df = df[df['data_interval'] == '08:20:00']

df = df.groupby(["data_interval", "price"])['delta'].sum()
# df = df.groupby(["data_interval", "price"], as_index=False)['delta'].sum()

print(df)


