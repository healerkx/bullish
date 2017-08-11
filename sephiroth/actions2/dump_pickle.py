
from actions import *
import time
import sys
sys.path.append('/Users/healer/Projects/fregata')
from root import *

@Actions.register("dump_pickle")
class DumpPickleAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        today = formatted_date(time.time())
        stock_data = StockData()
        d = stock_data.get_stock_basics(today)
        print(d)
