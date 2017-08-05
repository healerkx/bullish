
from .base_policy import *
import talib

@Policy.register('C1')
class C1Policy(Policy):

    """
    一般选股策略C1
    """

    def find_stock_codes(self, data):
        # 1. 竞价结束后, 对量比进行排行, 看前30名, 涨幅在4%以下的

        # 2. 选择流通股本数量较小的, 最好在3亿以下, 中小板尤佳

        # 3. 选择之前换手率连续多日在3%以下或连续几日平均换手率在3%以下的个股

        # 4. 选择之前多日成交量较为均衡或有涨停未放量现象的个股（之前一直无量涨停的个股除外）

        


    def handle(self, context):
        """
        """

