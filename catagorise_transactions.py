import database
import sklearn
import pandas as pd

data = database.getTransactionData()
df = pd.DataFrame(data)
print(df)
