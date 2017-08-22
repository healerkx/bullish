


import pandas as pd
import time
a = time.time()
df = pd.read_pickle('/Users/healer/a.p')

df['a'] = df.shift()['volume'] +  df.shift().shift()['volume']
b = time.time()

print(b - a)