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
import pandas as pd


def get_all_codes():
    stock_data = StockData()    
    return stock_data.get_codes()

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

    df1 = ts.get_hist_data(code, start=from_date, end=yesterday)
    # Rebuild
    d = {
        'open': df['open'].values, 
        'close': df['close'].values, 
        'high': df['high'].values, 
        'low': df['low'].values, 
        'volume': df['volume'].values 
        }
    df0 = pd.DataFrame(d, columns=['open', 'close', 'high', 'low', 'volume'], index=df.date)    
    df0['turnover'] = df1['turnover']

    return df0

def get_daily_data_ex(db, code):
    """
    """
    from_date = '2014-10-01'
    yesterday = str(datetime.today().date() + timedelta(days=-1))

    print(db, code)
    df = ts.get_hist_data(code)
    return df


#
def insert_code_data(db, code, df):
    """
    DF struct: [open, close, high, low, volume, turnover]
    insert into sk_stock_daily_data 
    (open,  close, high,  low,   volume,    turnover, date,        code,    status, create_time, update_time) values 
    ('4.9', '4.98','4.98','4.87','91300.0', '1.75',   '2017-08-24','000010',1,1503974955,1503974955),
    ('4.97','5.0', '5.03','4.9', '127823.0','2.45',   '2017-08-25','000010',1,1503974955,1503974955),
    ('4.99','5.04','5.06','4.96','78045.0', '1.49',   '2017-08-28','000010',1,1503974955,1503974955);
    """
    lists = []
    ctime = str(int(time.time()))
    
    values = df.values
    dates = df.index
    count = len(values)
    i = 0
    while i < count:
        date = str(dates[i])
        value = values[i]

        v = list(map(lambda x: "'%s'" % x,  value))
        v.append("'%s'" % date)
        v.append("'%s'" % code)
        v.append('1')
        v.append(ctime)
        v.append(ctime)
        s = ",".join(v)
        lists.append("(" + s + ")")

        i += 1
        
    sql = "insert into sk_stock_daily_data (open, close, high, low, volume, turnover, date, code, status, create_time, update_time) values " + ','.join(lists) + ";\n\n"
    print(sql)
    # exit()
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
    """
    基础信息查询
    """
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


def query_data_detail(db):
    pass


def insert_data(db):
    stock_data = StockData()
    for code in stock_data.get_codes():
        res = handle_code_data(db, code)

def get_data_setter(fields, values):
    setter_list = []
    i = 0
    for field in fields:
        setter_list.append("%s='%s'" % (field, values[i]))
        i += 1
    return ','.join(setter_list)

def update_code_data(db, code, df):
    "Turnover only (ts.get_hist_data() 只能拿到*未复权*数据, 故不记录)"
    dates = df.index[::-1]
    values = df.values[::-1]
    count = len(dates)
    insert_values = []
    i = 0
    cursor = db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    ctime = str(int(time.time()))
    while i < count:
        date = dates[i]
        value = values[i]
        
        where = " where code='%s' and date='%s'" % (code, date)
        query = "select * from sk_stock_daily_data " + where
        r = cursor.execute(query)
        if r == 1:
            d = cursor.fetchone()
            if float(d['turnover']) == 0.0:
                sql = "update sk_stock_daily_data set turnover='%s' where code='%s' and date='%s';" % (value[-1], code, date)
                cursor.execute(sql)
                
        i += 1

    db.commit()
    cursor.close()

# Update data
def fetch_and_update_code_data(db, code):
    df = get_daily_data_ex(db, code)
    print(code)
    if df is not None and not df.empty:
        update_code_data(db, code, df)


def update_data(db):
    # update all the codes about ma(x), v_ma(x), turnover...
    stock_data = StockData()
    for code in stock_data.get_codes():
        res = fetch_and_update_code_data(db, code)
       

def bank_data():
    pass

def update_codes_name_to_db(db, df):
    l = len(df.index)
    i = 0
    cursor = db.cursor()
    codes = df.index
    names = df.name.values
    while i < l:
        code = codes[i]
        name = names[i]
        i += 1
        query = "select name from sk_stock_basic_data where code='%s';" % code
        r = cursor.execute(query)
        if r == 1:
            n = cursor.fetchone()
            if n[0] == '' or n[0] != name:
                sql = "update sk_stock_basic_data set name='%s' where code='%s';" % (name, code)
                print(sql)
                cursor.execute(sql)
        else:
            sql = "insert into sk_stock_basic_data (name, code) values ('%s', '%s');" %  (name, code)
            print(sql)
            cursor.execute(sql)

    db.commit()

def update_codes_to_db(db, df):
    import numpy as np
    cursor = db.cursor()
    for v in df.values:
        industry = '' if pd.isnull(v[1]) else v[2]
        area = '' if pd.isnull(v[1]) else v[3]
        sme = 0 if pd.isnull(v[4]) else 1
        gem = 0 if pd.isnull(v[5]) else 1
        st = 0 if pd.isnull(v[6]) else 1
        code = v[0]
        
        sql = "update sk_stock_basic_data set industry='%s', area='%s', is_sme=%d, is_gem=%d, is_st=%d where code='%s';" % (industry, area, sme, gem, st, code)
        # print(sql)
        cursor.execute(sql)
    db.commit()


def update_codes(db):
    # update names
    df0 = ts.get_stock_basics()
    update_codes_name_to_db(db, df0)

    if os.path.exists('codes-info.pickle'):
        print('Refresh the basic info, please rm codes-info.pickle in advance.')
        df = pd.read_pickle('codes-info.pickle')
        update_codes_to_db(db, df)
        return

    # 行业
    df1 = ts.get_industry_classified()
    # df1 MUST have name column, otherwise the list'index would be changed

    #df2 = ts.get_concept_classified()
    #df2.drop('name', axis=1, inplace=True)
    #df1.merge(df2, left_on='code', right_on='code', how='outer')

    # 地域
    df3 = ts.get_area_classified()
    df3.drop('name', axis=1, inplace=True)
    df1 = df1.merge(df3, left_on='code', right_on='code', how='outer')
    
    # 中小板
    df4 = ts.get_sme_classified()
    df4.drop('name', axis=1, inplace=True)
    df4['sme'] = 1
    df1 = df1.merge(df4, left_on='code', right_on='code', how='outer')
    
    # 创业板
    df5 = ts.get_gem_classified()
    df5.drop('name', axis=1, inplace=True)
    df5['gem'] = 1
    df1 = df1.merge(df5, left_on='code', right_on='code', how='outer')
    
    # *ST
    df6 = ts.get_st_classified()
    df6.drop('name', axis=1, inplace=True)
    df6['st'] = 1
    df1 = df1.merge(df6, left_on='code', right_on='code', how='outer')
    
    pd.to_pickle(df1, 'codes-info.pickle')
    update_codes_to_db(db, df1)


def print_dataframe(db, code, filename=None):
    import time
    a = time.time()
    sql = "select date, open, close, high, low, volume from sk_stock_daily_data where code='%s'" % code
    with db.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        r = cursor.execute(sql)
        if r == 0:
            print("None data")
            return
        dataset = cursor.fetchall()

    dates = [d['date'] for d in dataset]
    df = pd.DataFrame(list(dataset), columns=['open', 'close', 'high', 'low', 'volume'], index=dates)
    
    if filename:
        pd.to_pickle(df, filename)

    b = time.time()
    print('use', b - a, 'seconds')
    return df


def main(argv):
    conv = MySQLdb.converters.conversions.copy()
    conv[12] = str
    config = {'db': 'fregata', 'user': 'root', 'passwd': 'root', 'host': '127.0.0.1', 'port': 3306}
    print('DB config:', config)
    db = MySQLdb.connect(**config, conv=conv)

    if len(argv) == 0:
        insert_data(db)
    elif argv[0] == 'insert':
        insert_data(db)
    elif argv[0] == 'update-values':
        update_data(db)        
    elif argv[0] == 'update-codes':
        update_codes(db)        
    elif argv[0] == 'query':
        query_data_info(db)
    elif argv[0] == 'detail':
        query_data_detail(db)
    elif argv[0] == 'bank':
        bank_data(db)
    else:
        filename = argv[1] if len(argv) > 1 else None
        print_dataframe(db, argv[0], filename)


if __name__ == '__main__':
    main(sys.argv[1:])
