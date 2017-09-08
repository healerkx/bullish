
from .policies import *
import sys


class Agent:
    """
    An agent perform as global entity traveling in time machine,
    using several policies, buying, selling or watching some stock.
    """

    def __init__(self, config):
        self.policy_list = []
        self.policy_clz_list = []
        self.capital = 10000
        self.repo = dict()
        self.last_diff = 0
        self.highest = 0
        self.concerned_codes = []
        self.config = config
        
        self.file = sys.stdout
        if 'log' in self.config:
            log_path = self.config['log']['path']
            log_name = self.config['__file__'] + '.log'
            log_file = os.path.join(log_path, log_name)
            self.file = open(log_file, mode='w', encoding='utf8')

    #
    def add_concerned_code(self, code):
        self.concerned_codes.append(code)

    def get_concerned_codes(self):
        return self.concerned_codes

    def add_policy(self, policy):
        '''
        @param policy should be a mapping object, contains keys: 'name', 'params'
        '''
        policy_name = policy['name']
        policy_clz = Policy.get_policy_clz(policy_name)
        if 'params' in policy:
            policy_clz.params = policy['params']
        
        self.policy_clz_list.append(policy_clz)

    #
    def get_repo_count(self, code):
        if code in self.repo:
            return self.repo[code]
        else:
            self.repo[code] = 0
            return 0

    def get_total(self, code, close):
        hold = self.get_repo_count(code)
        total = self.capital + hold * close
        return total

    def print_capital(self, code, close):
        hold = self.get_repo_count(code)
        total = self.capital + hold * close
        print('%.2f = (%.2f) + %d * %.2f' % (total, self.capital, hold, close))

    def buy(self, code, price, count=None):
        exist = self.get_repo_count(code)

        if not count:
            count = self.capital // price
        self.repo[code] = count + exist
        print("BUY:", code, count, price, count * price)
        
        self.capital -= count * price
        self.print_capital(code, price)

    def sell(self, code, price, count=None):
        exist = self.get_repo_count(code)
        if exist == 0:
            return
        if count and count > exist:
            # Not so much
            return

        count = exist if count is None else count
        self.repo[code] = exist - count
        print("SEL:", code, count, price, count * price)

        self.capital += count * price
        self.print_capital(code, price)

    #
    def log(self, content):
        self.file.write(content + "\n")

    def set_result(self, code, date, policy_name, result):
        """
        Dump result into file in format "#{PolicyName}: #{PolicyResult}"
        """
        self.log("%s: %s" % (policy_name, result))

    #
    def handle(self, code, context):
        """
        An agent can compose multi policies for a code's DataFrame object
        """
        # context.set_codes(self.get_concerned_codes())
        date = str(datetime.fromtimestamp(context.get_time()).date())
        for policy_clz in self.policy_clz_list:
            if policy_clz.policy_lifetime == PolicyLifetime_Global:
                policy = policy_clz.get_singleton()
            elif policy_clz.policy_lifetime == PolicyLifetime_EachCode:
                policy = policy_clz.instance_by_code(code)
            elif policy_clz.policy_lifetime == PolicyLifetime_AlwaysNew:
                policy = policy_clz()
                policy.initialize(code=code, date=date)
            elif policy_clz.policy_lifetime == PolicyLifetime_Unknown:
                raise Exception('A policy MUST set a valid Policy Lifetime')
            else:
                raise Exception('A policy MUST set a valid Policy Lifetime')

            result = policy.do_handle(code, context)

            self.set_result(code, date, policy.policy_name, result)


