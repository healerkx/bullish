


import pandas as pd

df = pd.read_pickle('/Users/healer/a.p')

df['a'] = df.shift()['volume'] +  df.shift().shift()['volume']


print(df)