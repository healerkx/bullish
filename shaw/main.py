
import sys, os
project_path = os.path.realpath(os.path.join(__file__, '../../'))
sys.path.append(project_path)

from root import *

def usage():
    return """
policy
    show all the policies
    """


def show_police_list(argv):
    for policy_name, policy_clz in Policy.policy_map.items():
        print(policy_name, policy_clz.__doc__)

if __name__ == '__main__':
    argv = sys.argv[1:]

    if len(argv) == 0:
        print(usage())
        exit()
    
    if argv[0] == 'policy':
        show_police_list(argv)