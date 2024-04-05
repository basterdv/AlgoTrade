from datetime import datetime

import pandas as pd

import matplotlib.pyplot as plt

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

# print(df)

# plt.plot([1,2,3,4],[3,5,6,7],'ro')

# отрисовка
# unique_time = df.index.get_level_values(0).unique().sort_values()
# unique_price = df.index.get_level_values(1).unique().sort_values()
unique_time = [1,2,3,4,5,6,7,8,9]
unique_price = [1,2,3,4,5,6,7,8,9]

base = pd.DataFrame(unique_time)
print(base)

fig, ax = plt.subplots(figsize=(50, 20))

# xlabels = unique_time.astype(str)
# ylabels = unique_price.astype(str)
xlabels = unique_time
ylabels = unique_price

# Подготовка графика
ax.set_title(f"График кластеров ")
ax.set_xticks(range(len(xlabels)), xlabels, rotation=45)
ax.set_yticks(range(len(ylabels)), ylabels)
ax.yaxis.set_ticks_position('right')
ax.set_xlim([-0.5, len(xlabels)])
ax.set_ylim([-1, len(ylabels)])

for i, t in enumerate(unique_time):  # три графика по сути накладываются друг на друга - объемы, дельты плюс и дельты минус
    pr = base.join(values1.loc[t]).squeeze()
    # draw horizontal lines, shifted left by i-th timepoint
    ax.barh(ylabels, pr, 0.3, i, color='black')  # 0.3 - толщина линии

plt.show()
