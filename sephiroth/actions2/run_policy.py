
from actions import *
import time
import sys
# TODO:
project_path = os.path.realpath(os.path.join(__file__, '../../../'))
sys.path.append(project_path)
from root import *

@Actions.register("run_policy")
class RunPolicyAction(BaseAction):

    def __init__(self):
        pass

    def execute(self, context):
        action_config = self.get_action_config()
        policy_name_list = action_config['policy_list']

        ag = Agent()
        for policy_name in policy_name_list:
            policy = {'name': policy_name, 'params':None}
            ag.add_policy(policy)

        action_context = Context()
        current_time = context.get_time()
        action_context.set_time(current_time)
        result = ag.handle(action_context)


        