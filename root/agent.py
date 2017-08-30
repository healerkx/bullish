
from .policies import *


class Agent:

    def __init__(self):
        self.policy_list = []
        self.capital = 10000
        self.repo = dict()
        self.last_diff = 0
        self.highest = 0
        self.concerned_codes = []

    def add_concerned_code(self, code):
        self.concerned_codes.append(code)

    def get_concerned_codes(self):
        return self.concerned_codes

    def add_policy(self, policy_name):
        policy_clz = Policy.get_policy_clz(policy_name)
        self.policy_list.append(policy_clz())

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

    def setup(self, context):
        for policy in self.policy_list:
            policy.setup(context)
    
    def handle(self, code, context):
        """
        An agent can compose multi policies for a code's DataFrame object
        """
        # context.set_codes(self.get_concerned_codes())
        pr = PolicyResult()
        
        for policy in self.policy_list:
            print(context.get_time())
            result = policy.handle(code, context)
            continue
            
            if sum(result) > 0:
                print(result)

            continue

            diff, close = result
            if self.last_diff * diff < 0:
                if diff > 0:
                    print(date, end=' ')
                    self.buy(code, close)
                elif diff < 0:
                    print(date, end=' ')
                    self.sell(code, close)

            self.last_diff = diff

            total = self.get_total(code, close)
            if total > self.highest:
                print('HIGH!', date)
                self.highest = total
                self.print_capital(code, close)

        return pr

    