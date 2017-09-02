
from .base_policy import *
import talib
from datetime import datetime
import time
from ..stock_data import *
import numpy as np

# A2和A1的计算结果进行过对比, 数据吻合
# A1和A2最大的实现障碍是有个量比排名，
# 这个属于和其他股票进行横向对比，
# 然而数据结构对单只股票的纵向时间计算比较友好。
# 所以尽量把排序安排到最后。

@Policy.register('O1')
class O1Policy(Policy):
    """
    用于下载daily ticks data into pickle files 
    """

    stock_data = StockData()

    open_dates = []

    def get_tick_data(self, code, context):
        '''
        '''
        current_time = context.get_time()
        current_date = time.localtime(current_time)
        w = int(time.strftime("%w", current_date))
        if w == 0 or w == 6:
            # 周六周日不开盘, 没有数据, 返回False
            return False
        
        if len(O1Policy.open_dates) == 0:
            O1Policy.open_dates = set(self.stock_data.get_open_dates())
            
        date = formatted_date(current_time)

        # 从数据库里面看是否有当日的数据, 没有可能就是节假日.
        if date not in self.open_dates:
            # 当日未开盘(可能是节日)
            return False

        tick_filename = self.stock_data.get_tick_path(code, date)
        if os.path.exists(tick_filename):
            return False

        df = self.stock_data.get_tick_data(code, date)
        return True

    def run_for_code(self, code, context):
        # Get some day tick-data at 9:25, (只有涉及到量比的时候才去取数据)
        return self.get_tick_data(code, context)

    def handle(self, code, context):
        """
        """
        result = self.run_for_code(code, context)
        if result:
            time.sleep(1.2)
        return result

