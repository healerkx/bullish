# Main
import os, sys, time, datetime

project_path = os.path.realpath(os.path.join(__file__, '../../'))
sys.path.append(project_path)

from root import *


def run_for_code(code, agent, config):
    tm = TimeMachine()
    tm.set_code(code)
    tm.set_agent(agent)
    begin = config['config']['date_begin']
    end = config['config']['date_end']
    print('On code =', code)
    tm.start(begin, end)


def run_for_all_codes(config):
    stock_data = StockData()
    agent = Agent()

    for policy_name in config['policy']:
        policy = config['policy'][policy_name]
        agent.add_policy(policy['name'])

    for code in stock_data.get_codes():
        run_for_code(code, agent, config)


def main(argv):
    file = os.path.join(os.path.dirname(__file__), 'conf', argv[0])
    with open(file) as f:
        config = toml.load(f)
        run_for_all_codes(config)

if __name__ == '__main__':
    main(sys.argv[1:])