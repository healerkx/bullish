
from .stock_data import *
from datetime import datetime
import time


class Context:
    """
    """

    def __init__(self, time_machine):
        self.codes = []
        self.code = ""
        self.data = None
        self.time = None
        self.time_machine = time_machine
        self.stock_data = StockData()

    def get_codes(self):
        return self.codes

    def set_codes(self, codes):
        self.codes = codes

    def get_k_data(self, code):
        """
        Get K data by code
        """
        k_data = self.stock_data.get_k_data(code)
        if self.time:
            end_date = datetime.fromtimestamp(self.time).date()
            return k_data.loc[k_data.index <= end_date]
        else:
            return k_data

    def get_tick_data(self, code, date=None):
        """
        Get tick data by params code and date(or context date)
        """
        if not date:
            date = str(datetime.fromtimestamp(self.time).date())        
        tick_data = self.stock_data.get_tick_data(code, date)
        return tick_data

    def get_profile_data(self, date=None):
        if not date:
            date = self.time
        profile_data = self.stock_data.get_profile_data(date)
        return profile_data

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

    def get_stock_basics(self):
        today = formatted_date(self.get_time())
        return self.stock_data.get_stock_basics(today)