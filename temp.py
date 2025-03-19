import pandas as pd
import datetime
df=pd.read_csv("transactions.csv")
print(df.loc[df["Type"]=="Credit"])