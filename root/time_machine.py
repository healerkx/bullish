
from .context import *
from .basic import *


class TimeMachine:

    def __init__(self):
        self.agents = []

    def add_agent(self, agent):
        self.agents.append(agent)

    def date_changed(self, begin_time, current_time):
        for code in self.codes:
            data = self.stock_data.get_k_data(code)
            begin = formatted_date(begin_time)
            end = formatted_date(current_time)
            # TODO: Optimized!
            # print(end, ":", end='')
            timed_data = data[data.date < end]
            context = Context()
            context.set_code(code)
            context.set_time(end)
            context.set_data(timed_data)
            for agent in self.agents:
                agent.handle(context)

    def on_date(self, begin_time, current_time):
        begin = formatted_date(begin_time)
        end = formatted_date(current_time)

        context = Context()
        context.set_time(end)
        
        for agent in self.agents:
            agent.handle(context)        
        
    def start(self, begin, end):
        begin_time = unix_time(begin)
        end_time = unix_time(end)

        day_seconds = 3600 * 24
        current_time = begin_time
        while current_time <= end_time:
            # self.date_changed(begin_time, current_time)
            self.on_date(begin_time, current_time)
            current_time += day_seconds
