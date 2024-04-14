# import pandas as pd
# import pyodbc
# import matplotlib.pyplot as plt
# from matplotlib.colors import TABLEAU_COLORS
# from itertools import cycle
# from pandas import DataFrame, Timestamp
# from datetime import timedelta
# import requests
# import datetime
# import winsound
#
# connection = pyodbc.connect(
#     'Driver={SQL Server}; Server=1-ПК\SQLEXPRESS; Database=Quik_export');  # Соединяемся с сервером
#
# SymbolList = ['yndx', 'LKOH']
# timeframe = '5min'
# h = 3  # кол-во отображаемых часов за день
# if (timeframe == '60min' or timeframe == '15min'):
#     h = 12
# last_hour = max((datetime.datetime.now() - timedelta(hours=h)).strftime('%H:%M:%S'),
#                 '10:00:00')  # для последующего среза данных
#
# while True:
#     try:
#         # готовлю данные из SQL
#         data0 = pd.read_sql("SELECT * FROM Quik_export.dbo.sdelki", connection)
#         data0['symbol'] = data0['symbol'].str.replace(r'\[TQBR]', '').map(str.strip)  # убираем [TQBR] и пробелы
#         data0['date'] = str(datetime.datetime.now().date())
#         data0['date_time'] = pd.to_datetime(data0['date'] + ' ' + data0['time_str'])  # datetime формат делаю
#
#         # обрабатываю данные
#         for i in SymbolList:
#             # 1-й этап - подготовка мультииндексного таймфрейма
#             symbol = i.upper()  # изменение на заглавные буквы
#             data = data0.copy(deep=True)  # уже не помню, но почему-то такое решение сделал
#             data = data.loc[(data['symbol'] == symbol) & (data['date_time'] >= last_hour)]  # делаю срез данных
#
#             df = data.drop_duplicates(subset=['numerator'])  # убираю дубликаты по номеру сделок на всякий случай
#
#             df['price'] = df['price'].astype(str).astype(float)
#             df['quantity'] = pd.to_numeric(df['quantity']).astype(int)  # quantity - кол-во сделок
#
#             df.loc[df['operation'] == 'SELL', 'delta'] = df['quantity'] * (-1)  # делаю знак дельты
#             df.loc[df['operation'] == 'BUY', 'delta'] = df['quantity']
#
#             df = df[['quantity', 'delta', 'date_time', "price"]]
#
#             df['data_interval'] = df['date_time'].dt.floor(timeframe)
#
#             df_0 = df.copy(deep=True)
#             df_0.index = df_0['date_time']
#             df_0 = df_0['price'].resample(timeframe).ohlc(_method='ohlc')
#
#             df.sort_values(by=['date_time'])
#
#             df = df.groupby(["data_interval", "price"]).sum()
#             df = df.sort_values(by=["data_interval", "price"],
#                                 ascending=[True, False])  # мультииндексная основа для графиков готова
#
#             df.loc[df['delta'] >= 0, 'delta_plus'] = df['delta']
#             df.loc[df['delta'] < 0, 'delta_minus'] = df[
#                 'delta'].abs()  # если убрать модуль, то в разные стороны смотреть будет
#
#             # 2-й этап - отрисовка
#             unique_time = df.index.get_level_values(0).unique().sort_values()
#             unique_price = df.index.get_level_values(1).unique().sort_values()
#
#             spacing = 0.1  # a minimum distance between two consecutive horizontal lines 0.1
#             values1 = (1 - spacing) * df['quantity'] / df[
#                 'quantity'].max()  # relative lengths of horizontal lines - для каждого графика (кол-во сделок, дельты минус, дельты плюс)
#             values2 = (1 - spacing) * df['delta_plus'] / df['quantity'].max()
#             values3 = (1 - spacing) * df['delta_minus'] / df['quantity'].max()
#             base = DataFrame(index=unique_price)  # the widest blank frame with prices
#
#             fig, ax = plt.subplots(figsize=(50, 20))
#
#             xlabels = unique_time.astype(str)
#             ylabels = unique_price.astype(str)
#
#             ax.set_title("   ".join(symbol), fontsize=60)
#             ax.set_xticks(range(len(xlabels)), xlabels, rotation=45)
#             ax.set_yticks(range(len(ylabels)), ylabels)
#             ax.yaxis.set_ticks_position('right')
#             ax.set_xlim([-0.5, len(xlabels)])
#             ax.set_ylim([-1, len(ylabels)])
#
#             for i, t in enumerate(
#                     unique_time):  # три графика по сути накладываются друг на друга - объемы, дельты плюс и дельты минус
#                 pr = base.join(values1.loc[t]).squeeze()
#                 # draw horizontal lines, shifted left by i-th timepoint
#                 ax.barh(ylabels, pr, 0.3, i, color='black')  # 0.3 - толщина линии
#
#                 pr2 = base.join(values2.loc[t]).squeeze()
#                 ax.barh(ylabels, pr2, 0.3, i, color='green')
#
#                 pr3 = base.join(values3.loc[t]).squeeze()
#                 ax.barh(ylabels, pr3, 0.3, i, color='red')
#
#         fig.tight_layout()
#         plt.savefig('Z://OSPanel//domains//localhost//' + str(
#             symbol) + '.png')  # путь для сохранения рисунков winsound.Beep(200, 1000) #чтобы узнать, когда график готов
#     exit()  # выход
#     except Exception as e:
#     print('ошибка: %s' % str(e))
