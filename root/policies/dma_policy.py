
from .base_policy import *
import talib


@Policy.register('DMA')
class DMAPolicy(Policy):
    """
    双均线策略
    """

    def handle(self, context):
        data = context.get_data()
        ma5 = talib.MA(data.close.values, timeperiod=5)
        ma60 = talib.MA(data.close.values, timeperiod=10)

        diff = ma5[-1] - ma60[-1]
        close = data.close.values[-1]
        # print(diff)

        return diff, close
