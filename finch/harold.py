# Main
import os, sys, time, datetime

project_path = os.path.realpath(os.path.join(__file__, '../../'))
sys.path.append(project_path)

from root import *


def is_bad_code(code):
    """
    个别股票被长期排除在外
    """
    return False


def run_for_code(code, agent, config):
    '''
    '''
    tm = TimeMachine()
    tm.set_code(code)
    tm.set_agent(agent)
    begin = config['config']['date_begin']
    end = config['config']['date_end']
    print('On code =', code)
    # daily is for default TimeMachine option
    mode = config['config']['mode'] if 'mode' in config['config'] else 'daily'
    tm.start(begin, end, mode='daily')


def run_for_all_codes(config):
    '''
    '''
    stock_data = StockData()
    agent = Agent(config)

    for policy_name in config['policy']:
        policy = config['policy'][policy_name]
        agent.add_policy(policy['name'])

    for code in stock_data.get_codes():
        if is_bad_code(code):
            continue
        run_for_code(code, agent, config)


def main(argv):
    filename = argv[0]
    filepath = os.path.join(os.path.dirname(__file__), 'conf', argv[0])
    with open(filepath) as file:
        config = toml.load(file)
        config['__file__'] = os.path.basename(filename)
        run_for_all_codes(config)


if __name__ == '__main__':
    """
    for code in all codes: # 所有股票codes
        #code -> LOG
        for date in dates: # 历史数据回归时间区域
            [date] -> LOG

            # 考虑基础的策略, 可能直接过滤（以后考虑放到Policy里面）
            continue if is_bad_code(*code*)
            
            for policy_class in agent.policy_classes:
                policy = policy_class[singleton / instance-by-code / always-new]
                policy.handle() -> [policy result] -> LOG

            #---------------------

            
            # End of this [date]
        #---------------------

        
        # End of this [code]


    # End of this Program
    """
    main(sys.argv[1:])


