
import pytoml as toml
import os
import tushare as ts
import pandas
from .basic import *
from .cache import *
import pandas as pd
import MySQLdb

from .stock_data_storage import StockDataStorage

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
            self.tick_path = os.path.join(self.config['config']['path'], self.config['config']['tick'])

        if not os.path.exists(self.k_path):
            os.mkdir(self.k_path)

        if not os.path.exists(self.profile_path):
            os.mkdir(self.profile_path)

        if not os.path.exists(self.tick_path):
            os.mkdir(self.tick_path)
        #
        config = {'db':'fregata', 'user':'root', 'passwd':'root', 'host':'127.0.0.1', 'port':3306}
        db = MySQLdb.connect(**config)
        self.db = db

    def get_k_path(self):
        if self.k_path:
            return self.k_path
        return ''

    def get_k_data_from_file(self, code):
        k_data_file = os.path.join(self.k_path, code)
        if os.path.exists(k_data_file):
            return pandas.read_pickle(k_data_file)
        else:
            return None

    def get_k_data_from_db(self, code, db):
        sql = "select date, open, close, high, low, volume, turnover from sk_stock_daily_data where code='%s' and status=1;" % code
        with db.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            r = cursor.execute(sql)
            if r == 0:
                return None
            dataset = cursor.fetchall()

        dates = [d['date'] for d in dataset]
        df = pd.DataFrame(list(dataset), columns=['open', 'close', 'high', 'low', 'volume', 'turnover'], index=dates)
        return df

    def set_k_data_to_file(self, code, k_data):
        k_data_file = os.path.join(self.k_path, code)
        pandas.to_pickle(k_data, k_data_file)

    @staticmethod
    def convert_k_data(df):
        """
        Convert k_data into DataFrame obj with date index
        """
        d = {
            'open':     df['open'].values,
            'close':    df['close'].values, 
            'high':     df['high'].values, 
            'low':      df['low'].values, 
            'volume':   df['volume'].values 
            }
        k_data = pd.DataFrame(d, index=df['date'].values, columns=['open', 'close', 'high', 'low', 'volume'])
        return k_data 
        
    def get_k_data(self, code):
        """
        Try load data from file cache first,
        Try load data from MySQL, the update the pickle file
        Call remote API to fetch K data if MySQL-don't have data
        :param code:
        :param params:
        :return:
        """
        k_data = self.get_k_data_from_file(code)
        if k_data is not None:
            return k_data

        k_data = self.get_k_data_from_db(code, self.db)
        if k_data is not None:
            self.set_k_data_to_file(code, k_data)
            return k_data
        
        k_data = ts.get_k_data(code)
        if k_data is None or k_data.empty:
            return None

        k_data = StockData.convert_k_data(k_data)
        hist_data = ts.get_hist_data(code)
        k_data['turnover'] = hist_data['turnover']
        self.set_k_data_to_file(code, k_data)
        return k_data


    ########################################################
    def get_tick_data(self, code, date):
        """
        """
        tick_data = self.get_tick_data_from_file(code, date)
        if tick_data is not None:
            return tick_data

        df = ts.get_tick_data(code, date=date)
        if df is None or df.empty:
            return None
        if len(df['time'][0]) > 10:
            print(df['time'][0])
            return None
        
        self.set_tick_data_to_file(code, date, df)
        return df

    def get_tick_data_from_file(self, code, date):
        tick_filename = self.get_tick_path(code, date)
        if not os.path.exists(tick_filename):
            return None
        return pandas.read_pickle(tick_filename)

    def set_tick_data_to_file(self, code, date, df):
        tick_filename = self.get_tick_path(code, date)
        pandas.to_pickle(df, tick_filename)

    def get_tick_path(self, code, date):
        path = os.path.join(self.tick_path, code)
        if not os.path.exists(path):
            os.mkdir(path)        
        return os.path.join(path, date)

    @staticmethod
    def get_option(options, option_name):
        if option_name in options:
            return options[option_name]
        else:
            return None

    ########################################################
    def get_codes(self, **options):
        sql = "select code from sk_stock_basic_data"
        where_clause = []
        if StockData.get_option(options, 'sme'):
            where_clause.append('is_sme = 1')

        if len(where_clause) > 0:
            sql += ' where ' + ' AND '.join(where_clause)

        with self.db.cursor() as cursor:
            print(sql)
            r = cursor.execute(sql)
            if r == 0:
                return None
            codes = cursor.fetchall()
            return list(map(lambda x: x[0], codes))
        return []
        



    ########################################################
    # Profile!
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

