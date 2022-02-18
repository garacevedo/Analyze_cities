import pandas as pd
import csv

df = pd.read_csv("muestra_airbnb_nyc.csv", index_col=0)

col_reviews=[]

data_reviews=[]
for i in df.columns.values:
    rev=[]
    if str(i).startswith("review"):
        #print(i)
        col_reviews.append(i)
        data_reviews.append(df[i])
        #avg_reviews.append(df[i].mean())


df["avg_filas"]=df[col_reviews].mean(axis=1)

# Las mejores puntuaciones y los precios
print("Las mejores puntuaciones y sus respectivos precios")
print(df[["avg_filas","price","property_type"]].sort_values(by=[ "avg_filas","price"], ascending=False).head(20))
