
# 蜡烛图形态分析
# 目前用于锤子线等几个形态TF出现概率的分析
import sys, os
import pickle
from numpy import *;

def analyze(m):
    t = m.T
    rows_count = len(t)
    print(rows_count)
    for i in range(0, rows_count):
        r = t[i,:].flatten().tolist()[0]
        count = len(r)
        print('%f, %f \t| %f, %f' % (r.count('T'), r.count('T') / count, r.count('F'), r.count('F') / count))


def parse(file, prefix='#'):
    rows = []
    for line in file:
        if line.startswith('@'):
            pass
        elif line.startswith(prefix):
            c = line[1:].strip()
            row = c.split(',')
            rows.append(row)
    return rows


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()
    filename = sys.argv[1]
    if not os.path.exists(filename):
        exit()
    
    with open(filename) as file:
        prefix = '#'
        if len(sys.argv) > 2:
            prefix = sys.argv[2]
        rows = parse(file, prefix)
        m = mat(rows)

        if len(sys.argv) > 3:
            f = open(sys.argv[3], 'wb')
            pickle.dump(m, f)
        
        rows = analyze(m)
