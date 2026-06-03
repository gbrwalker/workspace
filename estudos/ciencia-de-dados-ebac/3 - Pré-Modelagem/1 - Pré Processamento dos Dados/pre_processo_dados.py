import seaborn as sns
import pandas as pd 
import matplotlib.pyplot as plt

# Criando um dataframe com algumas idades
dados = {
    'idade': [25, 30, 35, 400, 45, 50, 554, 60, 60, 24, 233, 70, 26],
    'cidade': ['São Paulo', 'Salvador', 'Curitiba', 'São Paulo', 'salvador', 'Curtiba', 'São Paulo', 'Salvador', 'curitiba', 'são Paulo', 'Salvador', 'Curitiba', 'São Paulo'],
    'salario': ['1200,0', '0', '4000,0', '0', '5000,0', '1500,0', '0', '0', '0', '3000,0', '2500,0', '3000,0', '0']
}

df = pd.DataFrame(dados)
print(df)

media = df['idade'].mean()
print(media)

df = df.groupby('cidade')['idade'].mean().reset_index()
print(df)