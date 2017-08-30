
from .context import *
from .basic import *


class TimeMachine:
    """
    A time machine can take one agent travelling in history (data).
    """
    def __init__(self):
        self.agent = None
        self.code = None

    def set_agent(self, agent):
        self.agent = agent

    def set_code(self, code):
        self.code = code

    def on_date(self, context, begin_time, current_time):
        begin = formatted_date(begin_time)
        end = formatted_date(current_time)
        print('[%s]' % end)

        context.set_time(current_time)
        policy_result = self.agent.handle(self.code, context)

        #TODO: yield policy result
        
    def start(self, begin, end):
        begin_time = unix_time(begin)
        end_time = unix_time(end)
        
        day_seconds = 3600 * 24
        current_time = begin_time
        context = Context(self)
        context.set_codes(self.agent.get_concerned_codes())

        self.agent.setup(context)

        while current_time <= end_time:
            # self.date_changed(begin_time, current_time)
            self.on_date(context, begin_time, current_time)
            current_time += day_seconds
