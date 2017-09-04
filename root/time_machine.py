
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
        self.agent.log("[%s]" % end)
        policy_result = self.agent.handle(self.code, context)

    def start_daily(self, begin, end, skip_weekends=True):
        '''
        on_date invoked daily, each policy consumes context data.
        '''
        begin_time = unix_time(begin)
        end_time = unix_time(end)
        
        day_seconds = 3600 * 24
        current_time = begin_time
        context = Context(self)
        context.set_codes(self.agent.get_concerned_codes())

        self.agent.log("#%s" % self.code)

        while current_time <= end_time:
            if skip_weekends:
                current_date = time.localtime(current_time)
                weekday = int(time.strftime("%w", current_date))
                if weekday == 0 or weekday == 6:
                    current_time += day_seconds
                    # 周六周日不开盘, 没有数据, 返回False
                    continue
            # 
            self.on_date(context, begin_time, current_time)
            current_time += day_seconds

    def start_fulltime(self, begin, end):
        '''
        on_date invoked once, Policy executed once with full-time data.
        '''
        begin_time = unix_time(begin)
        end_time = unix_time(end)
        
        context = Context(self)
        context.set_codes(self.agent.get_concerned_codes())

        self.agent.log("#%s" % self.code)
        self.on_date(context, begin_time, end_time) 

    # Entry for TimeMachine
    def start(self, begin, end, **options):
        if 'mode' in options:
            if options['mode'] == 'daily':
                skip_weekends = True  # TODO: options
                self.start_daily(begin, end, skip_weekends)
            if options['mode'] == 'fulltime':
                self.start_fulltime(begin, end)
        else:
            self.start_daily(begin, end)

