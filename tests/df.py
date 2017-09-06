
import pandas as pd
import os, sys

dates = ['2017-08-01', '2017-08-02', '2017-08-03', '2017-08-04', '2017-08-05', '2017-08-06', '2017-08-07', '2017-08-08']

d = {
    'a': [1, 2, 3, 4, 5, 6, 7, 8],
    'b': [11, 12, 13, 14, 15, 16, 17, 18],
    'c': ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd']
}

df = pd.DataFrame(d, index=dates, columns=['a', 'b', 'c'])


project_path = os.path.realpath(os.path.join(__file__, '../../'))
print(project_path)
sys.path.append(project_path)

from root import *


l = RingList(df.iterrows(), 3)

print(list(map(lambda x: x[0], l.items())))

l.forward()
print(list(map(lambda x: x[0], l.items())))

l.forward(2)
print(list(map(lambda x: x[0], l.items())))

l.forward(2)
print(list(map(lambda x: x[0], l.items())))

l.forward()
print(list(map(lambda x: x[0], l.items())))