import numpy as np
import pandas as pd

# Replace the file path with your existing CSV file
file_path = "C:\\Users\\Acer\\Downloads\\Recipes\\csv\\output.csv"

# Read your CSV file into a Pandas DataFrame
df1 = pd.read_csv(file_path)
df1['split'] = np.random.randn(df1.shape[0], 1)

# Split ratio for training set
msk = np.random.rand(len(df1)) <= 0.8
train = df1[msk]
inter = df1[~msk]

# Save training set to "train.csv" in the same file path
train.to_csv('C:\\Users\\Acer\\Downloads\\Recipes\\csv\\train.csv', index=False)

# Save intermediate set to "intermediate.csv" in the same file path
inter.to_csv('C:\\Users\\Acer\\Downloads\\Recipes\\csv\\intermediate.csv', index=False)

# Read the intermediate CSV file into a new DataFrame
df2 = pd.read_csv('C:\\Users\\Acer\\Downloads\\Recipes\\csv\\intermediate.csv')
df2['split'] = np.random.randn(df2.shape[0], 1)

# Split ratio for dev and test
msk = np.random.rand(len(df2)) <= 0.5
dev = df2[msk]
test = df2[~msk]

# Save development set to "dev.csv" in the same file path
dev.to_csv('C:\\Users\\Acer\\Downloads\\Recipes\\csv\\dev.csv', index=False)

# Save test set to "test.csv" in the same file path
test.to_csv('C:\\Users\\Acer\\Downloads\\Recipes\\csv\\test.csv', index=False)
