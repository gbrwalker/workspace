import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('CHURN_CREDIT_MOD14.csv', delimiter=';')

print(df.head(10))

print(df.dtypes)
print(df.info())

df['Salario_Anual'] = df['Salario_Anual'].str.replace('.','', regex=False)
df['Salario_Anual'] = df['Salario_Anual'].astype(float)
print(df.dtypes)

print(df.isnull().values.any()) # Irá retornar true caso tenha algum valor nulo no dataframe

print(df.isnull().sum())

print((df.isnull().sum() / len(df)) * 100) # Obtendo as porcentagens dos valores nulos de cada coluna

# Coluna genero
remove_genero_null = df[df['Genero'].isnull()] 
print(remove_genero_null) # Mostrando os resultados que pussem valores nulos

remove_genero_null = df.dropna(subset=['Genero'], inplace=True) # Excluindo os valores nulos
print(df['Genero'].isnull().sum())

# Coluna idade
remove_genero_null = df[df['Idade'].isnull()] 
print(remove_genero_null) # Mostrando os resultados que pussem valores nulos

remove_genero_null = df.dropna(subset=['Idade'], inplace=True) # Excluindo os valores nulos
print(df['Idade'].isnull().sum())

# Coluna salário

# Média do salário anual
print(df['Salario_Anual'].mean()) # Média anual é de 10.2 milhões

# Mediana do salário anual
print(df['Salario_Anual'].median()) # Mediana anual é de 10.7 milhões

sns.set_style('whitegrid') # Setando estilo estético dos gráficos produzidos por Seaborn.

plt.figure(figsize=(8, 6)) # Criando um gráfico de Box Plot
sns.boxplot(data=df,
            y='Salario_Anual',
            color='skyblue')
plt.title('Boxplot da Coluna Salário')
plt.ylabel('Salario_Anual')
# plt.show()

sns.set_style('darkgrid')

plt.figure(figsize=(8, 6))
sns.histplot(data=df,
             x='Salario_Anual',
             bins=20,
             kde=True,
             color='skyblue')
plt.title('Histograma da Coluna de Salário')
plt.xlabel('Salario_Anual')
plt.ylabel('Contagem')
# plt.show()

# Trazendo a mediana dos salários removendo salários acima de 2 milhões
salarios_abaixo_2milhoes = df[df['Salario_Anual'] < 20000000]
print(salarios_abaixo_2milhoes['Salario_Anual'].mean())

mediana_salario_abaixo_2milhoes = df[df['Salario_Anual'] < 20000000]['Salario_Anual'].median()

# df['Salario_Anual'].fillna(mediana_salario_abaixo_2milhoes, inplace=True)
# For example, when doing 'df[col].method(value, inplace=True)', 
# try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.

df.fillna({'Salario_Anual': mediana_salario_abaixo_2milhoes}, inplace=True) # Substituindo os valores nulos pela mediana

print(df['Salario_Anual'].isnull().sum())

print(df['Salario_Anual'].median())

plt.figure(figsize=(10, 6))
sns.histplot(data=df,
             x='Churn',
             bins=20,
             kde=True,
             color='skyblue')
# plt.show()

print(df['Churn'].value_counts(normalize=True) * 100) # Cálculando a porcentagem de churn e não churn

# Vamos tentar buscar um padrão para os churn nulos
print(df[df['Churn'].isnull()])

df_churn_nulo = df[df['Churn'].isnull()]

# Plotando a distribuição dos paises
plt.figure(figsize=(10, 6))
sns.countplot(data=df_churn_nulo,
              x='Pais')
plt.title('Distribuição da coluna "Pais"para Churn Nulo')
plt.xlabel('Pais')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
# plt.show() # Verificamos que a maioria é da Espanha

plt.figure(figsize=(10, 6))
sns.countplot(data=df,
              x='Pais')
plt.title('Distribuição da coluna "Pais" para Churn Nulo')
plt.xlabel('Pais')
plt.ylabel('Contagem')
plt.xticks(rotation=45)
# plt.show() # Verificando todos os paises, a maioria é da frança

# Como a porcentagem da Espanha é pequena, iremos remover os dados nulos
df.dropna(subset=['Churn'], inplace=True)
print(df['Churn'].isnull().sum())

print(df.isnull().sum())

df['Churn'] = df['Churn'].astype(int)

# Alterando nome da coluna para seguir o padrão
df.rename(columns={'Balance': 'Balanco'}, inplace=True)
print(df.head())

print(df['Pais'].unique()) # Verificamos os nomes dentro da coluna pais

df['Pais'] = df['Pais'].str.upper() # Transformando os nomes no formato de texto caixa alta
print(df['Pais'].unique())

# Corrigindo o Germani para Germany
df['Pais'] = df['Pais'].replace('GERMANI', 'GERMANY')
print(df['Pais'].unique())

# Removendo colunas que não são importantes para não correr o risco de haver algum vies
df.drop(columns=['Sobrenome'], inplace=True)
df.drop(columns=['CustomerId'], inplace=True)