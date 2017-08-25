
from .base_policy import *
import talib
from datetime import datetime
from ..stock_data import *

# A2和A1的计算结果进行过对比, 数据吻合

@Policy.register('A2')
class A2Policy(Policy):
    """
    一般选股策略A2(A1的优化版本)
    """
    k_data = None

 
    def get_last_5_days_volume_data(self, context, code):
        """
        Days means workday!
        """
        k_data = self.prepare_code_data(code)
        date = datetime.fromtimestamp(context.get_time()).date()
        print(date)
        the_k_data = k_data.loc[k_data.index == date]
        return the_k_data


    def get_tick_data_at_0925(self, context, code):
        df = context.get_tick_data(code)
        tick_data_0925 = df.iloc[-1]
        print(tick_data_0925['time'])
        return tick_data_0925


    def eval_stock_code(self, context, code):
        k_data = self.get_last_5_days_volume_data(context, code)
        print("@", k_data)
        # Get some day tick-data at 9:25, 
        tick_data_0925 = self.get_tick_data_at_0925(context, code)
        print("#", tick_data_0925)
        # TODO: Perform the policy to calc 'volume_ratio'


    def pick_stock_codes(self, context):
        code_results = []
        codes = context.get_codes()
        for code in codes:
            code_result = self.eval_stock_code(context, code)
            code_results.append(code_result)

        #exit()
        return None

        ######################################################
        ######################################################
        ######################################################

        # TODO: Perform the policy to calc 'volume_ratio'
        pd = context.get_profile_data(formatted_date(time))
        if pd is None:
            raise Exception("Today all data is empty")

        num = 0
        vol_list = []
        for i in pd.index:
            code = pd.loc[i]['code']
            vol_list.append(self.get_volume_avg(code, d1, d2, d3, d4, d5))
            num += 1
            
        pd['avm5d'] = vol_list

        open_minutes_today = 5
        pd['volume_ratio'] = pd['volume'] / open_minutes_today / pd['avm5d']

        p1 = pd.loc[pd.changepercent > 4.0][pd.volume_ratio > 1]
        
        # 1. 竞价结束后, 对量比进行排行, 看前30名, 涨幅在4%以下的
        p1 = p1.sort_values('volume_ratio', ascending=False)


        # 2. 选择流通股本数量较小的, 最好在3亿以下, 中小板尤佳
        basics = context.get_stock_basics()
        basics = basics.loc[basics.outstanding > 0.0]
        basics = basics.sort_values('outstanding')
        # Why some stock's outstanding is 0???
        # print(basics[:20])
        
        # 3. 选择之前换手率连续多日在3%以下或连续几日平均换手率在3%以下的个股

        # 4. 选择之前多日成交量较为均衡或有涨停未放量现象的个股（之前一直无量涨停的个股除外）
        
        r = p1[['code', 'volume', 'avm5d', 'volume_ratio', 'changepercent']]

        r = r[0:20]
        print(r)
        return r

    def prepare_code_data(self, code):
        # TODO: 让优化的工作隐藏到context和 stock_data obj 层去, Policy尽量做到对未来数据不可见
        if self.k_data is not None:
            return self.k_data
        print("Prepare")
        stock_data = StockData()
        k_data = stock_data.get_k_data(code)
        # 
        k_data1 = k_data.shift()
        k_data2 = k_data1.shift()
        k_data3 = k_data2.shift()
        k_data4 = k_data3.shift()
        k_data5 = k_data4.shift()

        k_data['volume_sum5d'] = k_data1['volume'] + k_data2['volume'] + k_data3['volume'] + k_data4['volume'] + k_data5['volume']
        
        self.k_data = k_data
        return self.k_data
    
    def setup(self, context):
        """
        Setup some context
        """
        pass

    def handle(self, context):
        """
        """
        print("#" * 30)
        result = self.pick_stock_codes(context)

        return result

