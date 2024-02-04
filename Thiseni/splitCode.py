import numpy as np
import pandas as pd

file = "output.csv"

df1 = pd.read_csv(file)
df1['split'] = np.random.randn(df1.shape[0], 1)
# Split ratio for training set
msk = np.random.rand(len(df1)) <= 0.8
train = df1[msk]
inter = df1[~msk]
train.to_csv('train.csv', index=False)
inter.to_csv('intermediate.csv', index=False)

df2 = pd.read_csv('intermediate.csv')
df2['split'] = np.random.randn(df2.shape[0], 1)
# Split ratio for dev and test
msk = np.random.rand(len(df2)) <= 0.5
dev = df2[msk]
test = df2[~msk]
dev.to_csv('dev.csv', index=False)
test.to_csv('test.csv', index=False)