"""

ts.get_stock_basics => codes
foreach code in codes 
    ts.get_k_data(code)
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


stock_data = StockData()

def get_all_codes():
    global stock_data
    basics = stock_data.get_stock_basics('2017-08-16')
    return basics.index

def get_daily_data(code):
    global stock_data
    return stock_data.get_k_data(code)

def insert_data(db, code, df):
    values = []
    ctime = str(int(time.time()))
    if df.empty:
        return
    for entry in df.values:
        v = list(map(lambda x: "'%s'" % x,  entry))
        v.append('1')
        v.append(ctime)
        v.append(ctime)
        s = ",".join(v)
        values.append("(" + s + ")")

    sql = "insert into sk_stock_daily_data (date, open, close, high, low, volume, code, status, create_time, update_time) values " + ','.join(values) + ";\n\n"
    print(sql)
    #return
    with db.cursor() as cursor:
        r = cursor.execute(sql)
        db.commit()
        
        
def main(argv):
    conv = MySQLdb.converters.conversions.copy()
    conv[12] = str
    config = {'db':'fregata', 'user':'root', 'passwd':'root', 'host':'127.0.0.1', 'port':3306}
    db = MySQLdb.connect(**config)
    codes = get_all_codes()
    # 603976 603813
    
    for code in codes:
        df = get_daily_data(code)
        if df is None:
            continue
        insert_data(db, code, df)
        time.sleep(2)



if __name__ == '__main__':
    main(sys.argv)