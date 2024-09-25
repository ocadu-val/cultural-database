import pandas as pd

df = pd.read_csv('data.csv')

print(df.head())
# print(df.iloc[1])
print(df['Database Owner'].unique())
print(df['Type of entity'].unique())
