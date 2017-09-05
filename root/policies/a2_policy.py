
from .base_policy import *
import talib
from datetime import datetime
from ..stock_data import *
import numpy as np

# A2和A1的计算结果进行过对比, 数据吻合
# A1和A2最大的实现障碍是有个量比排名，
# 这个属于和其他股票进行横向对比，
# 然而数据结构对单只股票的纵向时间计算比较友好。
# 所以尽量把排序安排到最后。

@Policy.register('A2', PolicyLifetime_EachCode)
class A2Policy(Policy):
    """
    一般选股策略A2(A1的优化版本)
    第一步、9:25竞价结束后，对量比进行排行，看前30名，涨幅在4%以下的;
    第二步、选择流通股本数量较小的，最好在3亿以下，中小板尤佳;√
    第三步、选择之前换手率连续多日在3%以下或连续几日平均换手率在3%以下的个股;√
    第四步、选择之前多日成交量较为均衡（）或有涨停未放量现象的个股(之前一直无量涨停的个股除外);
    第五步、最好选择个人曾经操作过的、相对比较熟悉的个股进行介入操作。
    考虑到优化执行速度,对上述执行顺序进行了*调整*:
    1. 选择中小板的codes, 作为第一个筛选条件(股本在3亿以下, 可以最后作为权值处理)
    2. 以前4日平均换手率作为筛选条件
    3. 
    """

    k_data = None

    def get_recent_days_data(self, code, context):
        """
        'Days' means workday!
        """
        k_data = self.prepare_code_data(code)
        date = datetime.fromtimestamp(context.get_time()).date()
        the_k_data = k_data.loc[k_data.index == date]
        
        return the_k_data

    def get_tick_data_at_0925(self, code, context):
        '''
        通过ts.get_tick_data()获取每天09:25的price的方式消耗太大
        1. 3000+股票 * N年交易日 次获取API，200w次的HTTP调用 + File Cache
        2. File Cache这些日tick data, 数量非常庞大 (约200G+)

        通过观察, 利用历史数据, 每日0925的price, 就是每日的开盘价open
        SO, 暂时不用, 真实数据的时候, 可以改成当日数据ts.get_today_ticks()!!!
        '''
        df = context.get_tick_data(code)
        if df is not None:
            tick_data_0925 = df.iloc[-1]
            # print(tick_data_0925['time'])
            return tick_data_0925
        return None

    def get_volume_std_diff(self, the_k_data):
        d = the_k_data
        na = np.array([d['volume_b1d'], d['volume_b2d'], d['volume_b3d'], d['volume_b4d'], d['volume_b5d']])
        
        std = np.std(na)
        avg = np.average(na)
        return std / avg


    def run_for_code(self, code, context):
        # 1. code 已经是满足 sme=1 的筛选
        k_data = self.get_recent_days_data(code, context)
        if k_data is None or k_data.empty:
            print('没有数据, 不考虑')
            return None

        # 2. 换手率连续多日在3%以下...
        turnover_avg = k_data['turnover_avg']
        if turnover_avg is None or turnover_avg.empty:
            print('没有换手率, 不考虑')
            return None

        if turnover_avg.values[0] > 3.0:
            print("turnover avg > 3.0")
            return None
        
        volume_sum5d = k_data['volume_sum5d']

        # 通过观察, 利用历史数据, 每日0925的price, 就是每日的开盘价open
        # 优化!, 可能不需要要0925的日数据, 免去HTTP/LOCAL-IO
        price_at_0925 = k_data['open'].values[0]
        if p_change(price_at_0925, k_data['last_close'].values[0]) > 4.0:
            # TODO:
            print('涨跌幅 > 4.0')
            return None

        std_diff = self.get_volume_std_diff(k_data)
        if std_diff > 0.30: # 目前设置 标准差/平均值 的阈值 是3.0, 大于阈值表示volume变动大
            print('成交量波动大 > 0.3')
            return None

        # Get some day tick-data at 9:25, (只有涉及到量比的时候才去取数据)
        tick_data_0925 = self.get_tick_data_at_0925(code, context)
        if tick_data_0925 is None:
            return None

        volume_ratio = tick_data_0925['volume'] / volume_sum5d.values[0] / 5 * 60 * 4 * 5
        print('Volume-Ratio is', volume_ratio)
        # TODO: 设置量比阈值

        return (True, volume_ratio)


    def prepare_code_data(self, code):
        if self.k_data is not None:
            return self.k_data
        
        print("Loading data for", code)
        stock_data = StockData()
        k_data = stock_data.get_k_data(code)

        # 
        k_data1 = k_data.shift()
        k_data2 = k_data1.shift()
        k_data3 = k_data2.shift()
        k_data4 = k_data3.shift()
        k_data5 = k_data4.shift()

        k_data['volume_b1d'] = k_data1['volume']
        k_data['volume_b2d'] = k_data2['volume']
        k_data['volume_b3d'] = k_data3['volume']
        k_data['volume_b4d'] = k_data4['volume']
        k_data['volume_b5d'] = k_data5['volume']

        k_data['volume_sum5d'] = k_data1['volume'] + k_data2['volume'] + k_data3['volume'] + k_data4['volume'] + k_data5['volume']
        k_data['turnover_avg'] = (k_data1['turnover'] + k_data2['turnover'] + k_data3['turnover'] + k_data4['turnover']) / 4
        k_data['last_close'] = k_data1['close']
        
        self.k_data = k_data
        return k_data
    

    def handle(self, code, context):
        """
        """
        result = self.run_for_code(code, context)
        print(result)
        return result

