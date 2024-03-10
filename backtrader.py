import backtrader as bt

if __name__ == "__main__":
    cerebro = bt.Cerebro()
    print("Начальный капитал: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("Конечный капитал: %.2f" % cerebro.broker.getvalue())
