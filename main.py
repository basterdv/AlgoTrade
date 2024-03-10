from moexalgo import Ticker, Market
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field
from typing import TypeVar
from pydantic import BaseModel

# ticker – торговый код (тикер) инструмента, его уникальный идентификатор. Например, SBER.
# shortname – краткое название инструмента, может содержать аббревиатуру эмитента. К примеру, Сбербанк.
# lotsize – минимальный объем одной заявки на покупку/продажу в лотах.
# decimals – количество знаков после запятой при отображении цены инструмента.
# minstep – минимальный шаг изменения цены при торговле данным инструментом.
# issuesize – объем выпуска данного инструмента согласно проспекту эмиссии.
# isin – международный идентификационный код ценной бумаги (ISIN).
# regnumber – регистрационный номер выпуска ценной бумаги в ЦБ РФ.
# listlevel – уровень листинга инструмента, соответствует котировальному списку на Мосбирже.
# И остановимся на последнем параметре. На Московской бирже параметр listlevel обозначает уровень листинга,
# то есть котировальный список, в который включены ценные бумаги (акции, облигации).

# выбираем акции Сбера
sber = Ticker('SBER')

# все акции
stocks = Market('stocks')


# Вызоваем метод tickers() на экземпляре класса Market
class All_stocks:

    def get_table(self):
        all_stocks = pd.DataFrame(stocks.tickers())
        stocks_list = all_stocks.to_dict()
        return stocks_list

# class BaseTable(BaseModel):
#     a: pd.DataFrame(stocks.tickers())
#
#     class Config:
#         arbitrary_types_allowed = True

# a = All_stocks()
# st = a.get_table()
# table = st['SECID']
# print(table[0])

# print(st['SECID'])
# all_stocks = stocks.tickers()
# print(type(all_stocks))

# stocks = Market("shares/TQBR")

# получим дневные свечи с 2020 года
# cand = pd.DataFrame(sber.candles(date='2020-01-01', till_date='2023-11-01', period='D'))
# print(cand)
