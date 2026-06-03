import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

# Dados de investimento
dados = {
    'Investimento_Publicidade': [100, 140, 150, 390, 350, 155, 200],
    'Acessos_Site': [200, 260, 300, 760, 700, 320, 400]
}

df = pd.DataFrame(dados)

# Calculando a correlação

print(df['Investimento_Publicidade'].corr(df['Acessos_Site']))

# Passo 1 - Separar a narável dependente da independente

x = df[['Investimento_Publicidade']] # Variável independendte (característica)
y = df['Acessos_Site'] # Variável dependente (rótulo)

# Criando um objeto do tipo LinearRegression(), que será usado para representar nosso modelo de regressão linear.
regressa_acessos_site = LinearRegression()

regressa_acessos_site.fit(x, y)
# O modelo aprende a relação entre as variáveis independetes (x) e a variável dependente (y)
# Após a execução desta linha, o modela estará pronto para fazer previsões

# Atributo do objeto de regressão linear que representa o coeficiente linear da equação
print(regressa_acessos_site.intercept_)

# Atributo do objeto de regressão linear que representa os coeficientes das variáveis independentes na equação
print(regressa_acessos_site.coef_)

# SQR = SOMA DOS QUADRADOS TOTAIS
# SQM = SOMA DOS QUADRADOS DO MODELO
# SQE = SOME DOS QUADRADOS DOS ERROS

# SQT = SQM + SQE
# R2 = SQM / SQT
# R2 = 1 - (SQE/SQT)

print(regressa_acessos_site.score(x, y))

# Plotando os dados originais
plt.scatter(x, y, color='blue', label='Dados Originais')

# Plotar a linha de regressão
plt.plot(x, regressa_acessos_site.predict(x), color='red', label='Linha de Regressão')
plt.legend()
# plt.show()

# Realizando previsões

previsoes = regressa_acessos_site.predict(x)
print(previsoes)
print(y)

investimento = [[500]]
previsao_acessos = regressa_acessos_site.predict(investimento)
print(previsao_acessos)

dados_novo = {
    'Investimento_Publicidade': [100, 140, 160, 390, 380, 245, 250, 140, 360],
    'Impressao_Publicidade': [2050, 2500, 3350, 7500, 7120, 3650, 1985, 2150, 2100],
    'Alcance_Publicidade': [1500, 2350, 2950, 7200, 6885, 2050, 1185, 1930, 1985 ],
    'Curtidas_Publicidade': [200, 20, 100, 120, 125, 125, 90, 50, 55 ],
    'Comentarios_Publicidade': [50, 15, 10, 45, 56, 60, 2, 15, 32],
    'Acessos_Site': [200, 260, 320, 780, 700, 340, 425, 180, 200]
}

df_new = pd.DataFrame(dados_novo)

print(df_new)

# Passo 1: Matriz de Correlação

# Calculando a matriz de correlação
correlacao = df_new.corr()

# Gráfico:
plt.figure(figsize=(10, 6))
sns.heatmap(correlacao, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Gráfico de correlação')
# plt.show()

# Passo 2

# Separar as variáveis independentes da variável dependente
x_new = df_new[['Investimento_Publicidade', 'Impressao_Publicidade', 'Alcance_Publicidade', 'Curtidas_Publicidade', 'Comentarios_Publicidade']] # variável independente
y_new = df_new['Acessos_Site'] # variável dependente (rótulo)

# Passo 3

# Regressão Linear Múltipla
regressao_multipla = LinearRegression()
regressao_multipla.fit(x_new, y_new)

print(regressao_multipla.intercept_)
print(regressao_multipla.coef_)

# Passo 4

# Avaliação do modelo
print(regressao_multipla.score(x_new, y_new))

# Exemplo 1

# Iremos rodar o modelo apenas com as variáveis de menor correlação

x = df_new[['Curtidas_Publicidade', 'Comentarios_Publicidade']] # Variáveis independentes
y = df_new['Acessos_Site'] # variável dependente

regressao_exemplo1 = LinearRegression()
regressao_exemplo1.fit(x, y)

print(regressao_exemplo1.score(x, y))

# Exemplo 2

# Iremos rodar o modelo apenas com as variáveis de maior correlção
x = df_new[['Investimento_Publicidade', 'Impressao_Publicidade', 'Alcance_Publicidade']]
y = df_new['Acessos_Site']

regressao_exemplo2 = LinearRegression()
regressao_exemplo2.fit(x, y)

print(regressao_exemplo2.score(x, y))

# Separando as variáveis independentes da variável dependente
x_new = df_new[['Investimento_Publicidade', 'Impressao_Publicidade', 'Alcance_Publicidade', 'Curtidas_Publicidade', 'Comentarios_Publicidade']] # variável independente
y_new = df_new['Acessos_Site'] # variável dependente (rótulo)

# Adicionando uma constante ao conjunto de dados para estimar o termo de interceptação
x = sm.add_constant(x_new)

# Criando o modelo de regressão linear múltipla
modelo_stats = sm.OLS(y_new, x_new)

# Ajustando o modelo aos dados
resultado_stats = modelo_stats.fit()

# Exibindo os resultados da regressão
print(resultado_stats.summary())

# Separando as variáveis independentes da variável dependente
x_1 = df_new[['Investimento_Publicidade', 'Impressao_Publicidade', 'Alcance_Publicidade']] # variável independente
y_1 = df_new['Acessos_Site'] # variável dependente (rótulo)

x_1 = sm.add_constant(x_1)
modelo_stats_x1 = sm.OLS(y_1, x_1)
resultado_stats_ex1 = modelo_stats_x1.fit()
print(resultado_stats_ex1.summary())