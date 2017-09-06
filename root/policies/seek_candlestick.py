
from .base_policy import *
import talib
from datetime import datetime
import time
from ..stock_data import *
from ..ring_list import *
import numpy as np


@Policy.register('SeekCandle', PolicyLifetime_EachCode)
class SeekCandlestickPolicy(Policy):
    """
    Seek Hammer, Hanging-man.
    """
    k_data = None

    def initialize(self, **args):
        if 'code' not in args:
            raise Exception('Code not provided')
        
        self.load_data(args['code'])
        k_data = self.k_data[self.k_data.index >= datetime.strptime('2017-01-02', '%Y-%m-%d').date()]
        self.dates = set(map(lambda x: str(x), k_data.index))
        self.row_iter = k_data.iterrows()
        self.ring_list = RingList(self.row_iter, 10)

    #
    def load_data(self, code):
        if self.k_data is not None:
            return self.k_data
        
        stock_data = StockData()
        self.k_data = stock_data.get_k_data(code)
        return self.k_data

    def seek_candle_pattern(self, code, context):
        data = self.ring_list.first()
        print(data[1]['open'])
        self.ring_list.forward()
        return True

    def handle(self, code, context):
        """
        """
        date = formatted_date(context.get_time())
        
        if date not in self.dates:
            return None
        result = self.seek_candle_pattern(code, context)
        
        return result

    