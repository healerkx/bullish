
import talib
from ..basic import *


class Policy:

    policy_map = dict()

    def handle(self, context):
        """
        """
        pass

    @staticmethod
    def register(policy_name):
        def handler(clz):
            Policy.policy_map[policy_name] = clz
            return clz

        return handler

    @staticmethod
    def get_policy_clz(policy_name):
        return Policy.policy_map[policy_name]




class Seek3BlackCrowsPolicy(Policy):
    """
    寻找三只黑乌鸦测试
    :return Result
    """
    def handle(self, context):
        data = context.get_data()
        a = talib.CDL3BLACKCROWS(*get_open_high_low_close(data))

        # print(diff)
        return a
