
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
        k_data = k_data[k_data.index >= datetime.strptime('2017-01-02', '%Y-%m-%d').date()]
        self.dates = set(map(lambda x: str(x), k_data.index))
        self.row_iter = k_data.iterrows()
        self.ring_list = RingList(self.row_iter, 7)
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

    def get_items(self, data):
        return data['open'], data['close'], data['high'], data['low']

    ###########################################################################
    def seek_hammer(self):
        '''
        Ta-lib的CDLHAMMER
        '''
        data3 = self.ring_list.nth(3)
        
        open3, close3, high3, low3 = self.get_items(data3[1])
        if (high3 - close3) / (high3 - low3) < 0.03 and (open3 - low3) / (close3 - open3) > 2:
            # Found one may be a real hammer
            data2 = self.ring_list.nth(2)
            data1 = self.ring_list.nth(1)
            data0 = self.ring_list.nth(0)

            data4 = self.ring_list.nth(4)
            data5 = self.ring_list.nth(5)
            data6 = self.ring_list.nth(6)

            print("#", data3[0], open3, close3, high3, low3)
            # TODO:


    def seek_hanging_man(self):
        data3 = self.ring_list.nth(3)
        
        open3, close3, high3, low3 = self.get_items(data3[1])
        if (high3 - close3) / (high3 - low3) < 0.03 and (close3 - low3) / (open3 - close3) > 2:
            print("#", open3, close3, high3, low3)
            data2 = self.ring_list.nth(2)


    def seek_engulfing(self):
        data = self.ring_list.first()
        print(data[1]['open'])      

    def seek_3_black_crows(self):
        data = self.ring_list.first()
        print(data[1]['open'])            
