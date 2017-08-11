
from .base_policy import *
import talib

@Policy.register('C1')
class C1Policy(Policy):
    """
    一般选股策略C1
    """

    def dataframe_to_code_volume_dict(self, df):
        d = dict()
        if df is None: 
            return d
        for v in df.values:
            d[v[0]] = v[8]  # 0 is for code, 8 is for volume
        return d

    def get_code_volume_dict_by_date(self, context, current_time, day_offset):
        day_seconds = 24 * 3600
        pd = context.get_profile_data(formatted_date(current_time + day_offset * day_seconds))
        return self.dataframe_to_code_volume_dict(pd)

    def get_volume_avg(self, code, *ds):
        volume = 0
        minutes = 0
        for d in ds:
            if d and code in d:
                volume += d[code]
                minutes += 4 * 60
        if minutes > 0:
            return volume / minutes
        return float("inf")

    def find_stock_codes(self, context):
        time = context.get_time()
        day_seconds = 24 * 3600

        d5 = self.get_code_volume_dict_by_date(context, time, -5)
        d4 = self.get_code_volume_dict_by_date(context, time, -4)
        d3 = self.get_code_volume_dict_by_date(context, time, -3)
        d2 = self.get_code_volume_dict_by_date(context, time, -2)
        d1 = self.get_code_volume_dict_by_date(context, time, -1)

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
        
        print(p1[['code', 'volume', 'avm5d', 'volume_ratio', 'changepercent']])


    def handle(self, context):
        """
        """
        self.find_stock_codes(context)

