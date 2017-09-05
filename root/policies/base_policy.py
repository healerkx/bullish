
import talib
from ..basic import *

# 
PolicyLifetime_Unknown      = 0
# If you need a Policy single instance, set PolicyLifetime_Global.
PolicyLifetime_Global       = 1
# Most of the time, A policy instance containing data against a certain code, 
# set this value to class member policy_lifetime.
PolicyLifetime_EachCode     = 2  
# For each date or each code, create a brand new instance always.
PolicyLifetime_AlwaysNew    = 3


class Policy:
    """
    A policy handles a Context object, returns a Result object.
    Generally speaking, policies take context as input, 
    calculate several stock estimation, including buying and selling threshold 
    for a certain stock, and other information.
    """
    policy_map = dict()

    policy_lifetime = PolicyLifetime_Unknown

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
    def register(policy_name, policy_lifetime=PolicyLifetime_EachCode):
        def handler(clz):
            clz.policy_name = policy_name
            clz.policy_lifetime = policy_lifetime
            if policy_lifetime == PolicyLifetime_Global:
                clz.__instance = None
            elif policy_lifetime == PolicyLifetime_EachCode:
                clz.__instance_dict = dict()
            elif policy_lifetime == PolicyLifetime_AlwaysNew:
                pass
            elif policy_lifetime == PolicyLifetime_Unknown:
                raise Exception('A policy MUST set a valid Policy Lifetime')
            else:
                raise Exception('A policy MUST set a valid Policy Lifetime')

            Policy.policy_map[policy_name] = clz
            return clz

        return handler

    @staticmethod
    def get_policy_clz(policy_name):
        return Policy.policy_map[policy_name]

    # TODO: GC for unused code
    @classmethod
    def instance_by_code(clz, code):
        if code in clz.__instance_dict:
            return clz.__instance_dict[code]
        else:
            instance = clz()
            clz.__instance_dict[code] = instance
            return instance

    @classmethod
    def get_singleton(clz):
        if clz.__instance is None:
            clz.__instance = clz()
        return clz.__instance



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
