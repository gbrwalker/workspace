import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

df = pd.read_csv("ALUGUEL_MOD12.csv", delimiter=';')

df.head(10)

# A) Verifique os tipos de dados.

print(df.dtypes)

# B) Verifique os dados faltantes, se houver dados faltantes faça a substituição ou remoção justificando sua escolha.
print(df.isnull().sum())

# 2 - Realize a segunda etapa de pré processamento dos dados.

# A) Utilize a função describe para identificarmos outliers e verificarmos a distribuição dos dados.
print(df.describe())

# B) Caso note uma variável que te pareça conter outliers realiza a análise e tratamento desses dados, justificando a escolha do método utilizado.

# Utilizando o método Box Plot para verificar se existe outliers para os valores dos aluguéis
plt.figure(figsize=(10, 6))
sns.boxplot(data=df,
            y='Valor_Aluguel',
            color='skyblue')
plt.title('Box Plot para valor de alugueis')
plt.ylabel('Valor_Aluguel')
# plt.show()()


# Utilizando o método Box Plot para verificar se existe outliers para os valores dos condominios
# A principio há condiminios com os valores zerados
plt.figure(figsize=(10, 6))
sns.boxplot(data=df,
            y='Valor_Condominio',
            color='skyblue')
plt.title('Box Plot para valor dos condiminios')
plt.ylabel('Valor_Condominio')
# plt.show()()


# Utilizando o método Box Plot para verificar se existe outliers para a metragem
plt.figure(figsize=(10, 6))
sns.boxplot(data=df,
            y='Metragem',
            color='skyblue')
plt.title('Box Plot para metragem')
plt.ylabel('Metragem')
# plt.show()()

# Verificando valores dos condominios
count_val_cond = df['Valor_Condominio'].value_counts() # Contagem dos valores da coluna do valor_condominio
# Calculando a porcentagem de valores de condominio
percent_val_cond = (count_val_cond / count_val_cond.sum()) * 100
# Buscando a porcentagem de valores zeros
percent_zero = percent_val_cond.get(0, 0) # Vai retornar (0) zero se não encontrar nada
print(f"Porcentagem de registros com valor zero: {percent_zero:.2f}%")
# Foi encontrado apenas 8.86% de valores com o codomínio igual a zero, neste caso vou utilizar como premissa
# que podem ser casas e não apartamentos.

# C) Realize a análise bivariada dos dados. Faça uso de pelo menos 3 gráficos e traga insights acerca do analisado.

# Buscar as correlações mais fortes
correlacao = df.corr()

# Gráfico da correlação
plt.figure(figsize=(10, 6))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Gráfico de correlação')
# plt.show()()

# Metragem x Valor do condomínio
mediana_metragem_valor_condominio = df.groupby('Metragem')['Valor_Condominio'].median().reset_index()

fig = px.bar(mediana_metragem_valor_condominio,
             x='Metragem',
             y='Valor_Condominio',
             title='Média de metragem por valor do condomínio',
             labels={'Metragem': 'Metragem', 'Valor_Condominio': 'Valor do Condomínio'})
# fig.show()()

# Metragem x Número de vagas
mediana_metragem_n_vagas = df.groupby('Metragem')['N_Vagas'].median().reset_index()

fig = px.bar(mediana_metragem_n_vagas,
             x='Metragem',
             y='N_Vagas',
             title='Média de metragem por número de vagas',
             labels={'Metragem': 'Metragem', 'N_Vagas': 'Número de vagas'})
# fig.show()()


# N_banheiros x N_suites
mediana_nbanheiro_nsuites = df.groupby('N_banheiros')['N_Suites'].median().reset_index()

fig = px.bar(mediana_nbanheiro_nsuites,
             x='N_banheiros',
             y='N_Suites',
             title='Média da quantidade de banheiros por suítes',
             labels={'N_banheiros': 'Número de Banheiros', 'N_Suites': 'Número de Suítes'})
# fig.show()()

X = df.drop('Valor_Aluguel', axis=1) # Separando X - Todas variáveis exceto valor_aluguel
y = df['Valor_Aluguel'] # Separando Y (Apenas variavel valor_aluguel)

# Separando os dados em conjunto de treino e teste
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Verificando o gabarito
print(f"Tamanho de x_train: {x_train.shape}")
print(f"Tamanho de x_test: {x_test.shape}")
print(f"Tamanho de y_train: {y_train.shape}")
print(f"Tamanho de y_test: {y_test.shape}")

X = x_train[['Metragem']]  # Variável independente (características)
y = y_train  # Variável dependente (rótulo)

regressao_metragem = LinearRegression()
regressao_metragem.fit(X, y)

print(regressao_metragem.intercept_)
print(regressao_metragem.coef_)

a = regressao_metragem.intercept_
b = regressao_metragem.coef_[0]

print(f"Equação da reta: y = {b:.2f} * Metragem + {a:.2f}")

# Avaliação do modelo
print(regressao_metragem.score(X, y))

# Plotando a reta de regressão
plt.plot(X, regressao_metragem.predict(X), color='red', label='Linha de Regressão')
plt.legend()
# plt.show()()

X_test = x_test[['Metragem']]  # Variável independente (características)
y_test = y_test  # Variável dependente (rótulo)

# Usando o modelo treinado para fazer previsões sobre os dados de teste
previsoes = regressao_metragem.predict(X_test)

# Avaliando o desempenho do modelo usando métricas como o R²
r2 = regressao_metragem.score(X_test, y_test)

print("Coeficiente de Determinação (R²) nos Dados de Teste:", r2)

# Regressão Linear Multipla

# Separar as variáveis independentes da variável dependente (Trazendo as colunas exceto o valor do aluguel)

X = df.drop('Valor_Aluguel', axis=1)
y = df['Valor_Aluguel']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

regressao_multipla = LinearRegression()
regressao_multipla.fit(X_train, y_train)

r2 = regressao_multipla.score(X, y)

print("Coeficiente de Determinação (R²) nos Dados de Treino:", r2)


regressao_multipla = LinearRegression()
regressao_multipla.fit(X_test, y_test)

r2 = regressao_multipla.score(X_test, y_test)
print("Coeficiente de Determinação (R²) nos Dados de Teste:", r2)