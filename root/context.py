

class Context:
    """
    """

    def __init__(self):
        self.codes = []
        self.code = ""
        self.data = None
        self.time = None

    def get_codes(self):
        return self.codes

    def set_codes(self, codes):
        self.codes = codes

    def get_code(self):
        return self.code

    def set_code(self, code):
        self.code = code

    def get_data(self):
        """
        """
        return self.data

    def set_data(self, data):
        self.data = data

    def get_time(self):
        """
        :return:
        """
        return self.time

    def set_time(self, time):
        self.time = time
