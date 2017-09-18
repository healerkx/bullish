
from .base_policy import *
import talib
from datetime import datetime
import time
from ..stock_data import *
from ..ring_list import *
import numpy as np

# 使用RingList对要处理的DataFrame切片(slice)进行抽象
# 避免了反复使用index date进行查找, 并且使用切片copy数据片段的做法

@Policy.register('SeekCandle', PolicyLifetime_EachCode)
class SeekCandlestickPolicy(Policy):
    """
    Seek Hammer, Hanging-man.
    """
    k_data = None

    dates = None

    def initialize(self, **args):
        if 'code' not in args:
            raise Exception('Code not provided')

        k_data = self.load_data(args['code'])
        if k_data is None:
            return False
        k_data = k_data[k_data.index >= datetime.strptime('2014-01-01', '%Y-%m-%d').date()]
        self.dates = set(map(lambda x: str(x), k_data.index))
        self.row_iter = k_data.iterrows()
        self.ring_list = RingList(self.row_iter, 8)
        return True
    #
    def load_data(self, code):
        if self.k_data is not None:
            return self.k_data
        
        stock_data = StockData()
        self.k_data = stock_data.get_k_data(code)
        
        return self.k_data

    def seek_candle_pattern(self, code, context):
        '''
        '''
        if 'candle_pattern' not in self.params:
            return

        candle_pattern = self.params['candle_pattern']
        func_name = 'seek_%s' % candle_pattern
        if not hasattr(self, func_name):
            raise Exception('No function for this pattern seeking')

        func = getattr(self, func_name)
        func()

        # Forward to next date
        self.ring_list.forward()
        return True

    def handle(self, code, context):
        """
        """
        if self.dates is None:  # 初始化失败
            return None
        date = formatted_date(context.get_time())
        if date not in self.dates:
            return None
        result = self.seek_candle_pattern(code, context)
        return result

    @staticmethod
    def compare_func1(close1, close2):
        return 'T' if close1 >= close2 else 'F'

    @staticmethod
    def compare_func2(close1, close2):
        return 'T' if close1 < close2 else 'F'

    def get_items(self, data):
        return data['open'], data['close'], data['high'], data['low']

    def get_ring_list_item(self, nth, key):
        data = self.ring_list.nth(nth)
        return data[1][key]

    def compare_close(self, close, nth_list, compare_func):
        '''
        0. close 0 compare with close 3
        1. close 1 compare with close 3
        2. close 2 compare with close 3
        3. close 3 compare with close 3 (No meanings)
        4. close 4 compare with close 3
        5. close 5 compare with close 3
        6. close 6 compare with close 3
        7. close 7 compare with close 3
        8. abs(close 7 - close 3) / close 3 > 10%
        9. close 5 compare with close 4
        10. close 6 compare with close 5
        11. close 7 compare with close 6
        '''
        close_list = [self.get_ring_list_item(nth, 'close') for nth in nth_list]
        close_pair_list = [(nth_close, close) for nth_close in close_list]
        # 8
        close_pair_list.append((abs(close_list[7] - close) * 10, close))
        # 9
        close_pair_list.append((close_list[5], close_list[4]))
        close_pair_list.append((close_list[6], close_list[5]))
        close_pair_list.append((close_list[7], close_list[6]))

        result = [compare_func(close1, close2) for (close1, close2) in close_pair_list]
        return result

    ###########################################################################
    def seek_hammer(self):
        '''
        Ta-lib的CDLHAMMER
        '''
        data3 = self.ring_list.nth(3)
        
        open3, close3, high3, low3 = self.get_items(data3[1])
        if (high3 - close3) / (high3 - low3) < 0.03 and (open3 - low3) / (close3 - open3) > 2:
            # Found one may be a real hammer
            result = self.compare_close(close3, [0, 1, 2, 3, 4, 5, 6, 7], SeekCandlestickPolicy.compare_func1)

            print("#", data3[0], open3, close3, high3, low3)
            print('*', ','.join(result))
            # TODO:


    def seek_hanging_man(self):
        data3 = self.ring_list.nth(3)
        
        open3, close3, high3, low3 = self.get_items(data3[1])
        if (high3 - close3) / (high3 - low3) < 0.03 and (close3 - low3) / (open3 - close3) > 2:
            # Found one may be a real hanging_man
            result = self.compare_close(close3, [0, 1, 2, 3, 4, 5, 6, 7], SeekCandlestickPolicy.compare_func2)

            print("#", data3[0], open3, close3, high3, low3)
            print('*', ','.join(result))


    def seek_engulfing(self):
        '''
        吞没模式
        '''
        data3 = self.ring_list.nth(3)
        data4 = self.ring_list.nth(4)
        


    def seek_3_black_crows(self):
        data = self.ring_list.first()
        print(data[1]['open'])            
