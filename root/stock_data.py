
import pytoml as toml
import os
import tushare as ts
import pandas


class StockData:
    """

    """
    def __init__(self):
        data_config = os.path.join(os.path.dirname(__file__), 'config.toml')
        with open(data_config, "rb") as file:
            self.config = toml.load(file)

        if self.config:
            self.k_path = os.path.join(self.config['config']['path'], self.config['config']['k'])

        if not os.path.exists(self.k_path):
            os.mkdir(self.k_path)

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



