
from actions import *
import time
import sys
# TODO:
project_path = os.path.realpath(os.path.join(__file__, '../../../'))
sys.path.append(project_path)
from root import *

@Actions.register("dump_tick")
class DumpTickAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        today = formatted_date(time.time())
        stock_data = StockData()
        d = stock_data.get_stock_basics(today)
        print(d)
