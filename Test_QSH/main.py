from datetime import datetime

import pandas as pd

path = 'C:/Users/Home/Documents/Workshop/AlgoTrade/Test_QSH/2024_04_02/trades.csv'

# data = pd.read_csv(path, names=('A', 'B', 'C', 'D'),index_col=0)
data = pd.read_csv(path, sep=";", encoding='ANSI',
                   names=['Время', '2', 'Номер сделки', 'Цена', 'Количество лотов', 'Направление', '7', '8'])

df = pd.DataFrame(data)
df = df.drop(columns=['2', '7', '8'])

# df2 = pd.DataFrame({'Data': ['092812047']})
# df2.Data = pd.to_datetime(df2.Data, format='%H%M%S%f', errors='coerce').dt.time
# df2.Data = pd.to_datetime(df2.Data, format='%H:%M:%S.%f', errors='coerce').dt.date.replace({pd.NaT: ''})  # или .fillna('')

df['Время'] = pd.to_datetime(df.Время, format='%H%M%S%f', errors='coerce').dt.time

print(df)
