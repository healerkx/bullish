
import sys, os
project_path = os.path.realpath(os.path.join(__file__, '../../'))
sys.path.append(project_path)

import pytoml as toml
from root import *

def travel(config):
    print(config)
    ag = Agent()
    if 'policy' not in config:
        return

    for tab_name in config['policy']:
        policy = config['policy'][tab_name]
        ag.add_policy(policy['name'])
        # TODO: add policy args within a dict
    # ag.add_concerned_code(code)

    tm = TimeMachine()
    tm.add_agent(ag)

    tm.start(config['config']['date_begin'], config['config']['date_end'])


if __name__ == '__main__':
    if len(sys.argv) == 1:
        exit()

    file = os.path.join(os.path.dirname(__file__), 'conf', sys.argv[1])
    with open(file) as f:
        config = toml.load(f)
        travel(config)