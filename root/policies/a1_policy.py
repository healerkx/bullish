
from .base_policy import *
import talib

@Policy.register('A1', PolicyLifetime_Global)
class A1Policy(Policy):
    """
    一般选股策略A1
    (要有每天缓存的Profile data才能计算, ts.get_profile_data() )
    """

    def dataframe_to_code_volume_dict(self, df):
        d = dict()
        if df is None: 
            return d
        for v in df.values:
            d[v[0]] = v[8]  # 0 is for code, 8 is for volume
        return d

    def get_last_work_day(self, current_time, workday_offset):
        '''
        Calculate date by workdays offset
        '''
        if workday_offset == 0:
            return time.strftime('%Y-%m-%d', time.localtime(current_time))
        day_seconds = 24 * 3600
        today = time.localtime(current_time)
        w = int(time.strftime("%w", today))
        workday_offset_abs = abs(workday_offset)
        day_offset = abs(workday_offset)
        step = int(workday_offset / abs(workday_offset))
        i = 0
        while i < workday_offset_abs:
            w += step
            if w > 6:
                w = 0
            elif w < 0:
                w = 6

            if w != 6 and w != 0:
                i += 1
            else:
                day_offset += 1
            
        return time.strftime('%Y-%m-%d', time.localtime(current_time + step * day_offset * day_seconds))

    def get_code_volume_dict_by_date(self, context, current_time, workday_offset):
        day_seconds = 24 * 3600
        date = self.get_last_work_day(current_time, workday_offset)
        
        pd = context.get_profile_data(date)
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
        
        r = p1[['code', 'volume', 'avm5d', 'volume_ratio', 'changepercent']]

        r = r[0:20]
        print(r)
        return r


    def handle(self, context):
        """
        """
        result = self.find_stock_codes(context)

        return result

