
import os
import pytoml as toml

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
