import pandas as pd
from moexalgo import Market

# Выделяют 3 уровня листинга:
#
# Первый уровень (listlevel=1) – самые ликвидные и надежные ценные бумаги крупнейших и инвестиционно-привлекательных
#                                эмитентов. Для включения есть жесткие требования.
# Второй уровень (listlevel=2) – бумаги компаний поменьше по капитализации и ликвидности. Требования мягче.
# Третий уровень (listlevel=3) – как правило, акции компаний малой капитализации и более высокого риска.
#                                Требования слабее.

stocks = Market("stocks")
all_stocks = pd.DataFrame(stocks.tickers())
print(all_stocks.columns.tolist())
listlevels = sorted(all_stocks["LISTLEVEL"].unique())
with open("stock_listing.txt", "w", encoding="utf-8") as file:
    print(f"Всего в Алгопаке доступны данные по {all_stocks.shape[0]} акциям Мосбиржи")
    print(
        f"Всего в Алгопаке доступны данные по {all_stocks.shape[0]} акциям Мосбиржи",
        file=file,
    )
    for level in listlevels:
        stocks_level = all_stocks[all_stocks["LISTLEVEL"] == level]
        print(f"Для {level} уровня листинга отобрано {stocks_level.shape[0]} акций:")
        print(
            f"Для {level} уровня листинга отобрано {stocks_level.shape[0]} акций:",
            file=file,
        )
        list_tickers = stocks_level["SECID"].tolist()
        list_shortnames = stocks_level["SHORTNAME"].tolist()
        for ticker, shortname in zip(list_tickers, list_shortnames):
            print(f"{ticker} - {shortname}")
            print(f"{ticker} - {shortname}", file=file)
        print("_" * 70)
        print("_" * 70, file=file)