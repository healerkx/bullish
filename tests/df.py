


import pandas as pd


df1 = pd.DataFrame({"A":['a', 'b', 'c', 'd'], "B":[5, 7, 6, 8]})

df2 = pd.DataFrame({"A":['a', 'd', 'b', 'c'], "C":[1, 3, 2, 5]})





df1["C"] = [1, 3, 4, 5]
print(df1)

exit()

df = pd.DataFrame({
    "A":[1, 2, 3, 4, 5, 6, 4, 5, 2, 3],
    "B":[3, 2, 3, 2, 3, 2, 2, 1, 1, 2]
})

df2 = pd.DataFrame({
    "A":[1, 2, 3, 4, 5, 6, 4, 5, 2, 3],
    "B":[3, 2, 3, 2, 3, 2, 2, 1, 1, 2]
})

s = pd.Series(df)
print(s)

exit()
s2 = pd.Series(df2)


# NB!
df['L'] = df2['A'].shift() + df2['A'].shift().shift()
print(df)

exit()
df['C'] = df['L'] / df['B']



print(df)


d1 = df.sort('A', ascending=False)
print(d1)
d2 = df.sort('C', ascending=True)
print(d2)