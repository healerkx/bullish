import time


def get_path(reletive_path=''):
    pass

def get_open_high_low_close(data, begin=0, end=None):
    close = data.close.values
    opens = data.open.values
    high = data.high.values
    low = data.low.values
    return opens[begin:end], high[begin:end], low[begin:end], close[begin:end]

def unix_time(formatted_time):
    st = time.strptime(formatted_time, '%Y-%m-%d')
    return int(time.mktime(st))

def formatted_time(unixtime):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixtime))

def formatted_date(unixtime):
    return time.strftime('%Y-%m-%d', time.localtime(unixtime))
