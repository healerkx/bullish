
from actions import *

@Actions.register("dump_pickle")
class DumpPickleAction(BaseAction):

    def __init__(self):
        pass

        
    def execute(self, context):
        print("Executed!!!!!", context)