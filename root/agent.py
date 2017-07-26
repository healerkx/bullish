
from .policy import *

class Agent:

    def __init__(self):
        self.policy_list = []

    def add_policy(self, policy_name):
        policy = DMA_Policy() # TODO: Create policy by name
        self.policy_list.append(policy)

    def handle(self, data):
        """
        An agent can compose multi policies for a DataFrame
        """

        for policy in self.policy_list:
            policy.handle(data)

