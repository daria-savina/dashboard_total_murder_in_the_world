import pandas as pd

# reading csv files

df1 = pd.read_csv('data.csv', delimiter=';')
df2 = pd.read_csv('iso.csv', delimiter=';')

# join csv files
inner_join = pd.merge(df1,
                      df2,
                      on='country',
                      how='inner')
inner_join.to_csv('result.csv', index=False)
