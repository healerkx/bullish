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


def query_data_detail(db):
    pass


def insert_data(db):
    codes = get_all_codes()
    for code in codes:
        res = handle_code_data(db, code)
        if res:
            time.sleep(0)

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
