import pandas as pd

df_csv = pd.read_csv('Consulta.csv')

print(df_csv['Valor (R$)'].mean())
