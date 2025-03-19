import pandas as pd
trans=pd.read_csv('transactions.csv')
trans=trans.fillna(value={'Month':9,'Year':2024})
trans.to_csv('transactions.csv',index=False)
