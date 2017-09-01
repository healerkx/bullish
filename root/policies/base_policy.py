
import talib
from ..basic import *


class Policy:
    """
    A policy handles a Context object, returns a Result object.
    Generally speaking, policies take context as input, 
    calculate several stock estimation, including buying and selling threshold 
    for a certain stock, and other information.
    """
    policy_map = dict()

    policy_name = ''

    def handle(self, context):
        """
        @param context
        """
        pass

    @staticmethod
    def register(policy_name):
        def handler(clz):
            clz.policy_name = policy_name
            Policy.policy_map[policy_name] = clz
            return clz

        return handler

    @staticmethod
    def get_policy_clz(policy_name):
        return Policy.policy_map[policy_name]



class PolicyResult:
    def __init__(self):
        pass

#
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
