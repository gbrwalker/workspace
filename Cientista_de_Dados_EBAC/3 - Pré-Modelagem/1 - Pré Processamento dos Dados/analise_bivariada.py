import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('CHURN_CREDIT_MOD14.csv', delimiter=';')

print(df.head())

# Perguntas a serem respondidas?
#   Mulheres estão mais propensas a churn que homens?
#   Os clientes franceses costuma contratar mais produtos que os demais?
#   Em qual pais temos tido maior % de churn?
#   Qual idade tendemos a ter mais churn?

fig = px.histogram(df,
                   x='Churn',
                   color='Genero',
                   barmode='stack')
# Layout
fig.update_layout(title='Re;ação entre Churn e Genêro',
           xaxis_title='Churn',
           yaxis_title='Contagem',
           legend_title='Genêro')
# fig.show()

# Calculando a porcentagem de cada categoria
df_group = df.groupby(['Churn', 'Genero']).size().reset_index(name='count')
total_churn = df_group.groupby('Churn')['count'].transform('sum')
df_group['percent'] = (df_group['count'] / total_churn) * 100

# Criando gráfico de barras empilhados
fig = px.bar(df_group,
             x='Churn',
             y='percent',
             color='Genero',
             barmode='stack',
             labels={'Churn': 'Churn', 'percent': 'Porcentagem', 'Genero': 'Gênero'})
# Layout
fig.update_layout(title='Relação entre Churt e Gênero',
                  yaxis_title='Porcentagem',
                  legend_title='Gênero')
# fig.show()

# Analisando Pais x Churn
df['Pais'] = df['Pais'].replace('Germani', 'Germany')
df['Pais'] = df['Pais'].str.upper()

# Calculando a porcentagem de cada categoria
df_group_pais = df.groupby(['Churn', 'Pais']).size().reset_index(name='count')
total_churn_pais = df_group_pais.groupby('Churn')['count'].transform('sum')
df_group_pais['percent'] = (df_group_pais['count'] / total_churn_pais) * 100

# Criando gráfico de barras empilhados
fig = px.bar(df_group_pais,
             x='Churn',
             y='percent',
             color='Pais',
             barmode='stack',
             labels={'Churn': 'Churn', 'percent': 'Porcentagem', 'Pais': 'pais'})
# Layout
fig.update_layout(title='Relação entre Chunr e Pais',
                  yaxis_title='Porcentagem',
                  legend_title='Pais')
# fig.show()

# Analisano Pais x Quantidade de Produtos

# Calcular a mediana de produtos por pais
mediana_produtos_pais = df.groupby('Pais')['Qtd_Produtos'].median().reset_index()

# Criando gráfico de barras
fig = px.bar(mediana_produtos_pais, 
             x='Pais',
             y='Qtd_Produtos',
             title='Média de Produtos por Pais',
             labels={'Qtd_Produtos': 'Média de Produtos', 'Pais': 'País'})
# fig.show()

# Analisando Churn x Idade

# Calculando a mediana de churn por idade
mediana_churn_idade = df.groupby('Churn')['Idade'].median().reset_index()

# Criando gráfico de barras
fig = px.bar(mediana_churn_idade,
             x='Churn',
             y='Idade',
             title='Média Idade Churn')
# fig.show()

# Analisando membro ativo x churn
fig = px.histogram(df,
                   x='Churn',
                   color='Membro_Ativo',
                   barmode='stack')
# Layout
fig.update_layout(title='Relação entre Churn e Membro Ativo',
                  xaxis_title='Churn',
                  yaxis_title='Contagem',
                  legend_title='Membro_Ativo')
# fig.show()

# Mediana do Salário x Churn

# Tranformando o salario anula em tipo float
df['Salario_Anual'] = df['Salario_Anual'].str.replace('.', '', regex=False)
df['Salario_Anual'] = df['Salario_Anual'].astype(float)

mediana_churn_salario = df.groupby('Churn')['Salario_Anual'].median().reset_index()

# Criando gráfico de barras
fig = px.bar(mediana_churn_salario,
             x='Churn',
             y='Salario_Anual',
             title='Média Salario Anula Churn')
# fig.show()

# Mediana salário anula x pais

# Trocando os valores nulos por salários abaixo de 2 milhões
mediana_salario_abaixo_2milhoes = df[df['Salario_Anual'] < 20000000]['Salario_Anual'].median()
df.fillna({'Salario_Anual': mediana_salario_abaixo_2milhoes}, inplace=True)

mediana_pais_salario = df.groupby('Pais')['Salario_Anual'].median().reset_index()

# Criando gráfico de barras
fig = px.bar(mediana_pais_salario,
             x='Pais',
             y='Salario_Anual',
             title='Média Salários Anual Pais')
# fig.show()

# Mediana do Salário x Idade
mediana_salario_idade = df.groupby('Idade')['Salario_Anual'].median().reset_index()

# Criando gráfico de linha
fig = px.line(mediana_salario_idade,
              x='Idade',
              y='Salario_Anual',
              title='Relação entre Idade e Média de Salário',
              labels={'Idade': 'Idade', 'Salario_Anual': 'Média de Salário'})
fig.show()