
import talib
from ..basic import *

PolicyLifetime_Unknown      = 0
PolicyLifetime_Global       = 1
PolicyLifetime_EachCode     = 2
PolicyLifetime_AlwaysNew    = 3

class Policy:
    """
    A policy handles a Context object, returns a Result object.
    Generally speaking, policies take context as input, 
    calculate several stock estimation, including buying and selling threshold 
    for a certain stock, and other information.
    """
    policy_map = dict()

    instance = None

    instance_dict = dict()

    pplicy_lifetime = PolicyLifetime_Unknown

    policy_name = ''

    def handle(self, code, context):
        """
        @param code
        @param context
        """
        pass

    def do_handle(self, code, context):
        return self.handle(code, context)

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

    @classmethod
    def instance_by_code(clz, code):
        if code in clz.instance_dict:
            return clz.instance_dict[code]
        else:
            instance = clz()
            clz.instance_dict[code] = instance
            return instance

    @classmethod
    def get_singleton(clz):
        if clz.instance is None:
            clz.instance = clz()
        return clz.instance



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
