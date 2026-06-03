import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('arquivo_analise_telecon.csv', delimiter=',')

print(df.head(10))

# Utilizando o describe para visualizar as estatisticas descritivas 
print(df.describe())

# Analysis Churn
count_churn = df['CHURN'].value_counts()
print(count_churn)

# Calculate Churn Percentage
percent_churn = (count_churn / count_churn.sum()) * 100
print(percent_churn)

ax = count_churn.plot(kind='bar')
# Add percentage to graph
for i, v in enumerate(count_churn):
    ax.text(i, v + 1, f'{percent_churn[i]:.2f}%', ha='center')
plt.title('Gráfico de barras para churn')
plt.xlabel('Churn')
plt.ylabel('Frequência')
plt.xticks(rotation=1)
plt.savefig('imagens/calculate_churn_percentage.png')
# plt.show()

# Analysis Dependents
df['DEPENDENTS'].hist(bins=20)
plt.title('Histograma dos dependentes')
plt.xlabel('Dependentes')
plt.ylabel('Frequência')
plt.savefig('imagens/analysis_dependents.png')

# plt.show()

# Analysis Contract type
df['CONTRACT_TYPE'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Gráfico de Pizza para Visualizar os Tipos de Contratos')
plt.savefig('imagens/analysis_contract_type.jpg')

# plt.show()

# Analysis Streaming TV
count_stramingtv = df['STREAMINGTV'].value_counts()

# Calculate Streaming TV Percentage
percent_streamingtv = (count_stramingtv / count_stramingtv.sum()) * 100

ax = count_stramingtv.plot(kind='bar')

# Add percentage to graph
for i, v in enumerate(count_stramingtv):
    ax.text(i, v + 1, f'{percent_streamingtv[i]:.2f}%', ha='center')
plt.title('Gráfico de Barras para Streaming TV')
plt.xlabel('Streaming')
plt.ylabel('Frequência')
plt.xticks(rotation=1)
plt.savefig('imagens/analysis_streaming_tv.png')

# plt.show()

# Verify Booleans Elderly
count_elderly = df['ELDERLY'].value_counts()
percent_elderly = (count_elderly / count_elderly.sum()) * 100

print(count_elderly)
print(percent_elderly, '%')

# Verify Booleans Married
count_married = df['MARRIED'].value_counts()
percent_married = (count_married / count_married.sum()) * 100

print(count_married)
print(percent_married, '%')

# Verify Booleans Dependents
count_dependents = df['DEPENDENTS'].value_counts()
percent_dependents = (count_dependents / count_dependents.sum()) * 100

print(count_dependents)
print(percent_dependents, '%')

# Search Outlier Client Hour
fig = px.box(df,
             y='CLIENT_HOUR',
             title='BoxPlot do Tempo de Atendimento',
             labels={'CLIENT_HOUR': 'Tempo'})
fig.write_image('imagens/search_outliers_client_hour.png')
# fig.show()

# Search Outlier Payment Month
fig = px.box(df,
             y='PAYMENT_MONTH',
             title='BoxPlot de Pagamento Mensal',
             labels={'PAYMENT_MONTH': 'Mensalidade'})
fig.write_image('imagens/search_outliers_payment_mounth.png')
# fig.show()

# Search Outlier Full Payment
fig = px.box(df,
             y='FULL_PAYMENT',
             title='BoxPlot de Pagamento Total',
             labels={'FULL_PAYMENT': 'Pagamento Total'})
fig.write_image('imagens/search_outliers_full_payment.png')
# fig.show()

# Biv Analysis

# Percentage Married x Churn
df_group_married = df.groupby(['CHURN', 'MARRIED']).size().reset_index(name='count')
total_churn = df_group_married.groupby('CHURN')['count'].transform('sum')
df_group_married['percent'] = (df_group_married['count'] / total_churn) * 100

fig = px.bar(df_group_married,
             x='CHURN',
             y='percent',
             color='MARRIED',
             barmode='stack',
             labels={'CHURN': 'Churn', 'percent': 'Porcentagem', 'MARRIED': 'Casado(a)'})
# Layout
fig.update_layout(title='Releção entre Churn e Casado(a)',
                  yaxis_title='Porcentagem',
                  legend_title='Casado(a)')
fig.write_image('imagens/percent_married_churn.png')
# fig.show()

# Percentage Contract Type x Churn
df_group_contract_type = df.groupby(['CHURN', 'CONTRACT_TYPE']).size().reset_index(name='count')
df_group_contract_type['percent'] = (df_group_contract_type['count'] / total_churn) * 100

fig = px.bar(df_group_contract_type,
             x='CHURN',
             y='percent',
             color='CONTRACT_TYPE',
             barmode='stack',
             labels={'CHURN': 'Churn', 'percent': 'Porcentagem', 'CONTRACT_TYPE': 'Tipo de Contrato'})
# Layout
fig.update_layout(title='Relação entre Churn e Tipo de Contrato',
                  yaxis_title='Porcentagem',
                  legend_title='Tipo de Contrato')
fig.write_image('imagens/percent_contract_type_churn.png')
# fig.show()

# Percentage Dependents x Churn
df_group_dependents = df.groupby(['CHURN', 'DEPENDENTS']).size().reset_index(name='count')
df_group_dependents['percent'] = (df_group_dependents['count'] / total_churn) * 100

fig = px.bar(df_group_dependents,
             x='CHURN',
             y='percent',
             color='DEPENDENTS',
             barmode='stack',
             labels={'CHURN': 'Churn', 'percent': 'Porcentagem', 'DEPENDENTS': 'Dependentes'})
# Layout
fig.update_layout(title='Relação entre Churn e Dependentes',
                  yaxis_title='Porcentagem',
                  legend_title='Dependentes')
fig.write_image('imagens/percent_dependents_churn.png')
# fig.show()

# Percentage Gender x Churn
df_group_gender = df.groupby(['CHURN', 'GENDER']).size().reset_index(name='count')
df_group_gender['percent'] = (df_group_gender['count'] / total_churn) * 100

fig = px.bar(df_group_gender,
             x='CHURN',
             y='percent',
             color='GENDER',
             barmode='stack',
             labels={'CHURN': 'Churn', 'percent': 'Porcentagem', 'GENDER': 'Gênero'}
             )
# Layout
fig.update_layout(title='Relação entre Gênero e Churn',
                  yaxis_title='Porcentagem',
                  legend_title='Gênero')
fig.write_image('imagens/percent_gender_churn.png')
# fig.show()

# Percentage Elderly x Churn
fig = px.histogram(df,
                   x='CHURN',
                   color='ELDERLY',
                   barmode='stack',
                   labels={'CHURN': 'Churn', 'ELDERLY': 'Idoso'})
# Layout
fig.update_layout(title='Relação entre Idosos e Churn',
                  xaxis_title='CHURN',
                  yaxis_title='Contagem',
                  legend_title='Idoso')
fig.write_image('imagens/percent_elderly_churn.png')
# fig.show()