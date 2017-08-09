
import pytoml as toml
import os
import tushare as ts
import pandas
from .basic import *
from .cache import *


class StockDataStorage:

    def __init__(self):
        data_config = os.path.join(os.path.dirname(__file__), 'config.toml')
        with open(data_config, "rb") as file:
            self.config = toml.load(file)

        if self.config:
            self.path = self.config['config']['path']
            self.k_path = os.path.join(self.path, self.config['config']['k'])
            self.profile_path = os.path.join(self.path, self.config['config']['profile'])
            self.basics_path = os.path.join(self.path, self.config['config']['basics'])

        if not os.path.exists(self.k_path):
            os.mkdir(self.k_path)

        if not os.path.exists(self.profile_path):
            os.mkdir(self.profile_path)

        if not os.path.exists(self.basics_path):
            os.mkdir(self.basics_path)

    def get_cached_value(self, options, args):
        filename_f = options['filename']
        if not filename_f:
            raise Exception("No cache arg:filename")
        
        filename = os.path.join(self.path, options['path'], filename_f(args))
        if not os.path.exists(filename):
            return None
        read_f = options['read']
        if read_f:
            data = read_f(filename)
            return data
        return None
    
    def set_cached_value(self, options, args, value):
        filename_f = options['filename']
        if not filename_f:
            raise Exception("No cache arg:filename")
        
        filename = os.path.join(self.path, options['path'], filename_f(args))
        write_f = options['write']
        if write_f:
            write_f(value, filename)        

# Global
stock_data_storage = StockDataStorage()


class StockData:
    """

    """
    def __init__(self):
        data_config = os.path.join(os.path.dirname(__file__), 'config.toml')
        with open(data_config, "rb") as file:
            self.config = toml.load(file)

        if self.config:
            self.k_path = os.path.join(self.config['config']['path'], self.config['config']['k'])
            self.profile_path = os.path.join(self.config['config']['path'], self.config['config']['profile'])

        if not os.path.exists(self.k_path):
            os.mkdir(self.k_path)

        if not os.path.exists(self.profile_path):
            os.mkdir(self.profile_path)

    def get_k_path(self):
        if self.k_path:
            return self.k_path
        return ''

    def get_local_k_data(self, code):
        k_data_file = os.path.join(self.k_path, code)
        if os.path.exists(k_data_file):
            return pandas.read_pickle(k_data_file)
        else:
            return None

    def set_local_k_data(self, code, k_data):
        k_data_file = os.path.join(self.k_path, code)
        pandas.to_pickle(k_data, k_data_file)

    def get_k_data(self, code, **params):
        """
        :param code:
        :param params:
        :return:
        """
        k_data = self.get_local_k_data(code)
        if k_data is not None:
            return k_data

        k_data = ts.get_k_data(code, **params)

        # TODO: Merge DataFrame, using df1.append(df2).drop_duplicates()
        self.set_local_k_data(code, k_data)
        return k_data

    def get_local_profile_data(self, date):
        profile_data_file = os.path.join(self.profile_path, date)
        if os.path.exists(profile_data_file):
            return pandas.read_pickle(profile_data_file)
        else:
            return None

    def set_local_profile_data(self, date, profile_data):
        profile_data_file = os.path.join(self.profile_path, date)
        pandas.to_pickle(profile_data, profile_data_file)

    def get_profile_data(self, date=None):
        """
        TuShare
        ts.get_today_all() + cache
        :param date:
        :return:
        """
        today = formatted_date(time.time())
        if not date:
            date = today
        profile_data = self.get_local_profile_data(date)
        if profile_data is not None:
            return profile_data
        elif date != today:
            return None

        # TODO: 当天的Profile数据, 应该是变化的, 收盘前存入可能不太合适, 收盘后应该写入的才能用于历史数据分析
        profile_data = ts.get_today_all()

        self.set_local_profile_data(date, profile_data)

        return profile_data

    @cache(storage=stock_data_storage, 
            path='basics', filename=lambda x: x[-1],
            read=pandas.read_pickle, write=pandas.to_pickle)
    def get_stock_basics(self, date):
        return ts.get_stock_basics()