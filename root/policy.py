
import talib

class Policy:

    def handle(self, data):
        pass


class DMA_Policy(Policy):
    """
    双均线策略
    """
    def handle(self, data):
        ma5 = talib.MA(data.close.values, timeperiod=5)
        ma60 = talib.MA(data.close.values, timeperiod=60)

        diff = ma5[-1] - ma60[-1]
        print(diff)
        return diff