import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('CHURN_CREDIT_MOD14.csv', delimiter=';')

# Passo 1: Estatistica Descritiva: Calcule estatisticas descritivas básicas para resumir a distribuição da variável.
# Devolve as variáveis númericas
print(df.describe())

df.rename(columns={'Balance': 'Balanco'}, inplace=True) # Trocando o nome da coluna para padronizar

# Verificando o total de linhas com o dado igual a zero
print((df['Balanco'] == 0).sum())

# Calculando a porcentagem dos valores nulos
print(((df['Balanco'] == 0).mean()) * 100)

df.boxplot(column='Balanco')
plt.title('Box Plot Balanço')
plt.ylabel('Valores')
# plt.show()

# Vamos retirar os valores diferentes de (0) zero para identificair outliers
df_not_zero = df[df['Balanco'] != 0]
df_not_zero.boxplot(column='Balanco')
plt.title('Box Plot Balanço com valores diferentes de zero')
plt.ylabel('Valores')
# plt.show()

# Vamos analisar a coluna de quatidade de produto, a média está um pouco mais distante dos 50%
df.boxplot(column='Qtd_Produtos')
plt.title('Box Plot Quantidade de Produtos')
plt.ylabel('Quantidade de Produtos')
# plt.show()

# Analisaremos a variável tempo de crédito, a média esta quase igual aos 50%
df.boxplot(column='Tempo_Credito')
plt.title('Box Plot para tempo de crédito')
plt.ylabel('Valores')
# plt.show()

# Analisando as variáveis booleanas 
count_card = df['Possui_Cartao'].value_counts() # Contagem dos valores da coluna Possui Cartão
print(count_card)

# Calculando a porcentagem para que seja possível criar o gráfico
porcent_card = (count_card / count_card.sum()) * 100
ax = porcent_card.plot(kind='bar')
plt.title('Gráfico de barras para a variável possui_cartao')
plt.xlabel('Possui Cartão')
plt.ylabel('Frequência')
# plt.show()

# Membro ativo
count_member = df['Membro_Ativo'].value_counts() # Contagem dos valores da coluna Membro Ativo
print(count_member)

# Calculando a porcentagem dos membros ativos
porcent_member = (count_member / count_member.sum()) * 100
ax = porcent_member.plot(kind='bar')
plt.title('Gráfico de barras para a variável membro ativo')
plt.xlabel('Membro Ativo')
plt.ylabel('Frequência')
# plt.show()

# Analisando o Churn
count_churn = df['Churn'].value_counts()
print(count_churn)

# Calculando a porcentagem de churn's
porcent_churn = (count_churn / count_churn.sum()) * 100
ax = porcent_churn.plot(kind='bar')
plt.title('Gráfico de barras para a varável churn')
plt.xlabel('Churn')
plt.ylabel('Frequência')
# plt.show()

# Analisando as variáveis categóricas 

df['Pais'] = df['Pais'].replace('Germani', 'Germany')
print(df['Pais'].unique())
df['Pais'] = df['Pais'].str.upper()

# Calculando a porcentagem
coun_contry = df['Pais'].value_counts()
porcent_contry = (coun_contry / coun_contry.sum()) * 100

ax = coun_contry.plot(kind='bar')
# Adicionando as porcentagens nas barras
for i, v in enumerate(coun_contry):
    ax.text(i, v + 1, f'{porcent_contry[i]:.2f}%', ha='center')
plt.title('Gráfico de barras para a variável pais')
plt.xlabel('Pais')
plt.ylabel('Frequência')
# plt.show()

count_gender = df['Genero'].value_counts()
porcent_gender = (count_gender / count_gender.sum()) * 100

ax = count_gender.plot(kind='bar')
for i, v in enumerate(count_gender):
    ax.text(i, v + 1, f'{porcent_gender[i]:.2f}%', ha='center')
plt.title('Gráfico de barras para a variável genero')
plt.xlabel('Genero')
plt.ylabel('Frequência')
# plt.show()

# Verificar se outliers são casos isolados, se são possíveis erros de digitação e se devem ser removidos ou não
df_not_zero = df[df['Balanco'] != 0]
fig = px.box(df_not_zero,
             y='Balanco',
             title='Box Plot do Balanço com valores diferentes de zero (0)',
             labels={'Balanco': 'Valores'})
# # fig.show()

# Visualizando onde a ocorrência é maior de 180000
print(df[df['Balanco'] > 180000])

# Verificando a porcentagem dos outlier's
outliers_up_180000 = len(df[df['Balanco'] > 180000]) / len(df) * 100
print(f"Porcentagem de outliers a cima de 180000 {outliers_up_180000:.2f}%")

# Caso opte por remover ou substituir os valores outliers (sem afetar os valores 0)

# Inicia fazendo uma cópia do df pois não iremos trabalhar com os dados alterados:
df_novo = df.copy()

# Criar os quatis do boxplot, para remover aqueles que estão nos quartis desejados
Q1 = df_novo['Balanco'].quantile(0.25)
Q3 = df_novo['Balanco'].quantile(0.75)

IQR = Q3 - Q1

lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR

df_sem_outliers = df_novo[(df['Balanco'] >= lim_inf) & (df['Balanco'] <= lim_sup)]

# Calculando a mediana dos dados sem os valores maiores que 186000
mediana_sem_outlier = df_sem_outliers['Balanco'].median()

# Substituindo os valores maiores que 186000 pela mediana no novo dataframe
df_novo.loc[df['Balanco'] > 186000, 'Balanco'] = mediana_sem_outlier

# Outlier para a coluna de quantidade de produtos
fig = px.box(df,
             y='Qtd_Produtos',
             title='Box Plot da quantidade de produtos',
             labels={'Qtd_Produtos': 'Valores'})
# # fig.show()

# Verificando a distribuição das categorias
print(df['Qtd_Produtos'].value_counts(normalize=True) * 100)