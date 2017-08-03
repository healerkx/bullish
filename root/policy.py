
import talib
from .basic import *

class Policy:

    def handle(self, context):
        """
        """
        pass


class DMA_Policy(Policy):
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


class Seek3BlackCrows_Policy(Policy):
    """
    寻找三只黑乌鸦测试
    :return Result
    """
    def handle(self, context):
        data = context.get_data()
        a = talib.CDL3BLACKCROWS(*get_open_high_low_close(data))

        # print(diff)
        return a
