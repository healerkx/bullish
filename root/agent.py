
from .policy import *

class Agent:

    def __init__(self):
        self.policy_list = []
        self.capital = 10000
        self.repo = dict()
        self.last_diff = 0
        self.highest = 0

    def add_policy(self, policy_name):
        policy = Seek3BlackCrows_Policy() #DMA_Policy() # TODO: Create policy by name
        self.policy_list.append(policy)

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

    def buy(self, code, close):
        exist = self.get_repo_count(code)

        count = self.capital // close
        self.repo[code] = count + exist
        print("BUY:", code, count, close, count * close)
        
        self.capital -= count * close
        self.print_capital(code, close)

    def sell(self, code, close):
        exist = self.get_repo_count(code)
        if exist == 0:
            return

        count = exist
        self.repo[code] = exist - count
        print("SEL:", code, count, close, count * close)
        
        self.capital += count * close
        self.print_capital(code, close)

    def handle(self, context):
        """
        An agent can compose multi policies for a DataFrame
        """
        for policy in self.policy_list:
            data = context.get_data()
            result = policy.handle(context)

            if sum(result) > 0:
                print(code, date)
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


