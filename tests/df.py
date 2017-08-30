
import pandas as pd

dates = ['2017-08-01', '2017-08-02', '2017-08-03', '2017-08-04']

d = {
    'a': [1, 2, 3, 4],
    'b': [11, 12, 13, 14],
    'c': ['a', 'b', 'c', 'd']
}

df = pd.DataFrame(d, index=dates, columns=['a', 'b', 'c'])

v = df.get_value('2017-08-02', 'a')
print(v)