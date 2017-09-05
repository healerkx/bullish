
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
        if 'code' in args:
            self.data = self.load_data(args['code'])
        print("#", args['code'])
        exit()
    
    def load_data(self, code):
        print("#", code)
        return None

    def get_dataframe_window(self, from_date, dates_count):
        pass

    def seek_hh(self, code, context):
        return True

    def handle(self, code, context):
        """
        """
        result = self.seek_hh(code, context)
        
        return result

    