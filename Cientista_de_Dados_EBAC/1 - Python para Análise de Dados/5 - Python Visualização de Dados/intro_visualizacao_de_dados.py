import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('clientes-v3-preparado.csv')

print(df.head().to_string())

# Histograma
plt.hist (df['salario'])
plt.show()

#Histograma - Parâmetros
plt.figure(figsize=(10, 6))
plt.hist(df['salario'], bins=100, color='green', alpha=0.8)
plt.title('Histograma - Distribuição de Salários')
plt.xlabel('Salário')
plt.xticks(ticks=range(0, int(df['salario'].max())+2000, 2000))
plt.ylabel('Frequência')
plt.grid(True)
plt.show()

# Múltiplos gráficos
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1) #2 Linha, 2 Colunas, 1° Gráfico

#Gráfico de Dispersão
plt.scatter(df['salario'], df['salario'])
plt.title('Dispersão - Salario e Salário')
plt.xlabel('Salário')
plt.ylabel('Salário')

plt.subplot(1, 2, 2) # 1 Linha, 2 Colunas, 2° Gráfico
plt.scatter(df['salario'], df['anos_experiencia'], color='#5883a8', alpha=0.6, s=30) # cor hexadecimal online
plt.title('Dispersão Idade e Anos de Experiência')
plt.xlabel('Salário')
plt.ylabel('Anos de Experiência')

#Mapa de Calor
corr=df[['salario', 'anos_experiencia']].corr()
plt.subplot(2, 2, 3) # 1 Linha, 2 Colunas, 1° Gráfico
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlação Salário e Idade')

plt.tight_layout() # Ajustar espaçamentos quando trabalhar com multiplos graficos
plt.show()