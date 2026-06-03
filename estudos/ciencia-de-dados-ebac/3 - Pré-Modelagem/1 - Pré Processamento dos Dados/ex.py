import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import skew

df = pd.read_csv('CHURN_TELECON_MOD08_TAREFA.csv', delimiter=';')

print(df.head(20))

print(df.dtypes)

print(df.isnull().sum()) # Trazendo os valores nulos por coluna
print((df.isnull().sum()/ len(df)) * 100) # Trazendo a porcentagem de valores nulos por coluna

remove_gen_null = df[df['Genero'].isnull()]
print(remove_gen_null) # Mostrando os resultados que pussem valores nulos
remove_gen_null = df.dropna(subset=['Genero'], inplace=True) # Excluindo valores nulos na coluna Genero
print(remove_gen_null)

# Churn: A porcentagem de valores nulos são pequenas (0.20)
remove_churn_null = df[df['Churn'].isnull()]
print(remove_churn_null)
remove_churn_null = df.dropna(subset=['Churn'], inplace=True)
print(remove_churn_null)

# Pagamento Mensal
print(df['Pagamento_Mensal'].mean()) # Media 65.60756321839081
print(df['Pagamento_Mensal'].median()) # mediana 71.45

# Verificando a assimetria, assimetria leve é indicado preencher os dados nulos com a média
assimetria = skew(df['Pagamento_Mensal'].dropna()) 
print(assimetria)

media_pagamento_mensal = df['Pagamento_Mensal'].mean()

df.fillna({'Pagamento_Mensal': media_pagamento_mensal}, inplace=True)
print(df['Pagamento_Mensal'].isnull().sum())

plt.figure(figsize=(10, 6))
sns.boxplot(data=df,
            y='Pagamento_Mensal',
            color='skyblue')
plt.title('BoxPlot para Pagamentos Mensais')
plt.ylabel('Pagamento_Mensal')
# plt.show() # não foi identificado outlier

plt.figure(figsize=(10, 6))
sns.histplot(df['Pagamento_Mensal'].dropna(),
             kde=True,
             bins=30,
             color='skyblue')
# plt.show()

# PhoneService boxplot
phoneservice_null = df[df['PhoneService'].isnull()]
print(phoneservice_null)
print(df['PhoneService'].value_counts())

plt.figure(figsize=(10, 6))
sns.histplot(data=df,
             x='PhoneService',
             bins=20,
             kde=True,
             color='skyblue')
# plt.show()

print(df['Genero'].unique())
df['Genero'] = df['Genero'].replace(('F', 'f'), 'Female')
df['Genero'] = df['Genero'].replace('M', 'Male')
df['Genero'] = df['Genero'].str.upper()
print(df['Genero'].unique())

df.rename(columns={'Genero': 'Gender', 'Idoso': 'elderly', 'Casado': 'Married', 'Tempo_como_Cliente': 'Client_Hour', 'Suporte_Tecnico': 'Tecnical_Suport',
                   'Tipo_Contrato': 'Contract_Type', 'Pagamento_Mensal': 'Payment_Month', 'Total_Pago': 'Full_Payment'}, inplace=True)
df.columns = df.columns.str.upper()
print(df.head())

df.to_csv('arquivo_analise_telecon.csv', index=False)