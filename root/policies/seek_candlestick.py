
from .base_policy import *
import talib
from datetime import datetime
import time
from ..stock_data import *
import numpy as np


@Policy.register('SeekCandle', PolicyLifetime_EachCode)
class SeekCandlestickPolicy(Policy):
    """
    Seek Hammer, Hanging-man.
    """
    def initialize(self, **args):
        if 'code' not in args:
            raise Exception('Code not provided')
        
        self.load_data(args['code'])
        self.row_iter = self.k_data.iterrows()

        self.window_size = 10 # TODO: 参数化
        self.window_current = 0
        self.window_tail = 0
        self.window_slides = []
        # Fill all the window_slides
        for i in range(0, self.window_size):
            self.window_slides.append(next(self.row_iter))
            self.window_tail += 1

    #
    def load_data(self, code):
        if self.k_data is not None:
            return self.k_data
        
        stock_data = StockData()
        self.k_data = stock_data.get_k_data(code)
        return self.k_data

    def move_window_slide(self):
        row = next(self.row_iter)
        self.window_tail += 1
        self.window_tail = self.window_tail % self.window_size
        self.window_slides[self.window_tail] = row
        self.window_current += 1


    def get_dataframe_window(self, from_date, dates_count):
        pass

    def seek_hh(self, code, context):
        return True

    def handle(self, code, context):
        """
        """
        result = self.seek_hh(code, context)
        
        return result

    