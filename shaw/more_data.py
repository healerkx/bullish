"""

ts.get_stock_basics => codes
foreach code in codes 
    ts.get_k_data(code) from last_save_date to yesterday
    => insert DataFrame into table
FIRST WRITE 2017-08-17
"""
import tushare as ts
import sys, os

import MySQLdb
import MySQLdb.cursors
import MySQLdb.converters

project_path = os.path.realpath(os.path.join(__file__, '../../'))
sys.path.append(project_path)

import pytoml as toml
from root import *
from datetime import datetime, date
from datetime import timedelta

stock_data = StockData()

def get_all_codes():
    global stock_data
    basics = stock_data.get_stock_basics('2017-08-16')
    return basics.index

#
def get_daily_data(db, code):
    """
    """
    from_date = '2014-10-01'
    yesterday = str(datetime.today().date() + timedelta(days=-1))

    with db.cursor() as cursor:
        cursor.execute('select max(date) from sk_stock_daily_data where code=\'%s\'' % code)
        result = cursor.fetchall()
        max_date = result[0][0]
        
        if max_date is not None:
            if str(max_date) == yesterday:  # Data already saved to yesterday
                return None
            from_date = str(max_date + timedelta(days=1))
    
    df = ts.get_k_data(code, start=from_date, end=yesterday)
    if from_date == yesterday and df.empty:
        print(code, 'suspension?')
    return df

#
def insert_code_data(db, code, df):
    """
    """
    values = []
    ctime = str(int(time.time()))

    for entry in df.values:
        v = list(map(lambda x: "'%s'" % x,  entry))
        v.append('1')
        v.append(ctime)
        v.append(ctime)
        s = ",".join(v)
        values.append("(" + s + ")")

    sql = "insert into sk_stock_daily_data (date, open, close, high, low, volume, code, status, create_time, update_time) values " + ','.join(values) + ";\n\n"
    print(sql)
    
    with db.cursor() as cursor:
        r = cursor.execute(sql)
        db.commit()
    return True

#
def handle_code_data(db, code):
    df = get_daily_data(db, code)
    if df is None or df.empty:
        return False

    return insert_code_data(db, code, df)


def query_data_info(db):
    cursor = db.cursor()
    # count how many codes
    sql = "select count(distinct(code)) from sk_stock_daily_data;"
    r = cursor.execute(sql)
    if r == 1:
        count = cursor.fetchall()
        print("Contains (%d) codes by now" % count[0][0])
        print()
    
    # max history date
    sql = "select max(date) from sk_stock_daily_data;"
    r = cursor.execute(sql)
    date = '1970-01-01'
    if r == 1:
        date = cursor.fetchall()[0][0]
        print("The latest date is (%s)" % date)
        print()

    # count how many code date=max-history-date?
    sql = "select count(distinct(code)) from sk_stock_daily_data where date = '%s';" % date
    r = cursor.execute(sql)
    if r == 1:
        count = cursor.fetchall()
        print("Contains (%d) codes in the latest date (%s)" % (count[0][0], date))
        print()

    cursor.close()


def insert_data(db):
    codes = get_all_codes()
    for code in codes:
        res = handle_code_data(db, code)
        if res:
            time.sleep(0)  

def bank_data():
    pass

def print_dataframe(db, code, filename=None):
    sql = "select date, open, close, high, low, volume from sk_stock_daily_data where code='%s'" % code
    with db.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:

        r = cursor.execute(sql)
        if r == 0:
            print("None data")
            return
        dataset = cursor.fetchall()

    dates = [d['date'] for d in dataset]

    import pandas as pd
    df = pd.DataFrame(list(dataset), columns=['open', 'close', 'high', 'low', 'volume'], index=dates)
    
    if filename:
        pd.to_pickle(df, filename)
    print(df[:10])
    return df

def main(argv):
    conv = MySQLdb.converters.conversions.copy()
    conv[12] = str
    config = {'db':'fregata', 'user':'root', 'passwd':'root', 'host':'127.0.0.1', 'port':3306}
    print('DB config:', config)
    db = MySQLdb.connect(**config, conv=conv)

    if len(argv) == 0:
        insert_data(db)
    if argv[0] == 'insert':
        insert_data(db)
    elif argv[0] == 'query':
        query_data_info(db)
    elif argv[0] == 'detail':
        query_data_detail(db)     
    elif argv[0] == 'bank':
        bank_data(db)
    else:
        filename = None
        if len(argv) > 1:
            filename = argv[1]
        print_dataframe(db, argv[0], filename)


if __name__ == '__main__':
    main(sys.argv[1:])
