
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
        self.ring_list = RingList(self.row_iter, 20)
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
        '''
        close_list = [self.get_ring_list_item(nth, 'close') for nth in nth_list]
        close_pair_list = [(nth_close, close) for nth_close in close_list]
        # 8
        close_pair_list.append((abs(close_list[-1] - close) * 10, close))
        # 9 -
        result = [compare_func(close1, close2) for (close1, close2) in close_pair_list]
        return result

    ###########################################################################
    def seek_hammer(self):
        '''
        Ta-lib的CDLHAMMER
        '''
        happen_day_data = self.ring_list.nth(6)
        
        open, close, high, low = self.get_items(happen_day_data[1])
        if (high - close) / (high - low) < 0.03 and (open - low) / (close - open) > 2.0:
            # Found one may be a real hammer
            result = self.compare_close(close, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], SeekCandlestickPolicy.compare_func1)

            print("@", happen_day_data[0])
            print('#', ','.join(result))
            # TODO:


    def seek_hanging_man(self):
        happen_day_data = self.ring_list.nth(6)
        
        open, close, high, low = self.get_items(happen_day_data[1])
        if (high - close) / (high - low) < 0.03 and (close - low) / (open - close) > 2:
            # Found one may be a real hanging_man
            result = self.compare_close(close, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], SeekCandlestickPolicy.compare_func2)

            print("@", happen_day_data[0])
            print('#', ','.join(result))

    def seek_engulfing(self):
        '''
        吞没形态
        '''
        data3 = self.ring_list.nth(3)
        open3, close3, high3, low3 = self.get_items(data3[1])

        data4 = self.ring_list.nth(4)
        open4, close4, high4, low4 = self.get_items(data4[1])

        if (open3 > close3) != (open4 > close4): # 颜色相反
            # 
            if close3 > open3 and open4 > close3 and open3 > close4:
                print("@", data3[0])
                result = self.compare_close(close3, [0, 1, 2, 3, 4, 5, 6, 7], SeekCandlestickPolicy.compare_func1)
                print('D', ','.join(result))
            # 
            elif close3 < open3 and open4 < close3 and open3 < close4:
                print("@", data3[0])
                result = self.compare_close(close3, [0, 1, 2, 3, 4, 5, 6, 7], SeekCandlestickPolicy.compare_func2)
                print('U', ','.join(result))
        


    def seek_3_black_crows(self):
        data = self.ring_list.first()
        print(data[1]['open'])            

'''
对hammer和hanging-man的计算：
从2014年10月到2017年8月，几年的时间内，统计形态发生前后的股票收盘价比较，
计算结果，以hammer为例:
4683.000000, 0.412817 	| 6661.000000, 0.587183
4363.000000, 0.384609 	| 6981.000000, 0.615391
4416.000000, 0.389281 	| 6928.000000, 0.610719
4120.000000, 0.363188 	| 7224.000000, 0.636812
3692.000000, 0.325458 	| 7652.000000, 0.674542
1452.000000, 0.127997 	| 9892.000000, 0.872003
11344.000000, 1.000000 	| 0.000000, 0.000000
6322.000000, 0.557299 	| 5022.000000, 0.442701
5538.000000, 0.488188 	| 5806.000000, 0.511812
5702.000000, 0.502645 	| 5642.000000, 0.497355
5921.000000, 0.521950 	| 5423.000000, 0.478050
6058.000000, 0.534027 	| 5286.000000, 0.465973
6046.000000, 0.532969 	| 5298.000000, 0.467031
6257.000000, 0.551569 	| 5087.000000, 0.448431
6360.000000, 0.560649 	| 4984.000000, 0.439351
6258.000000, 0.551657 	| 5086.000000, 0.448343
6003.000000, 0.529178 	| 5341.000000, 0.470822
5943.000000, 0.523889 	| 5401.000000, 0.476111
6083.000000, 0.536231 	| 5261.000000, 0.463769
6012.000000, 0.529972 	| 5332.000000, 0.470028
4267.000000, 0.376146 	| 7077.000000, 0.623854
在一个观测data window内，第7天（6th）是形态发生日。结果是前面n天和该日close比较，和之后m天的close与之比较的结果。

第一列是大于(hammer, 如果是hanging-man则是’小于‘)的次数，第二列是这个次数占总发生次数的比率。第三列和第四列分别是相反的情况。

而根据hammer的数据显示，出现hammer形态后，之后大约10天内涨的几率几乎是1/2。这样的频率不足以采信hammer形态。

或者说：或许有其他的参数参与，这个形态更有预示意义。
[2017-10-10]
'''