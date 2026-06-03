import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar o arquivo CSV no DataFrame
df = pd.read_csv('ecommerce_preparados.csv')

# Análise detalhada dos dados
# Exibir as primeiras linhas do DataFrame para verificação
print(df.head().to_string())

# Descrição estatística para variáveis numéricas
print(df.describe())

# Gráfico de Histograma (Distribuição das Notas)
plt.figure(figsize=(10, 6))
plt.hist(df['Nota'], bins=10, color='skyblue', edgecolor='black')
plt.title('Distribuição das Notas dos Produtos')
plt.xlabel('Nota')
plt.ylabel('Frequência')
plt.grid(True)
plt.show()

# Gráfico de Dispersão (Relação entre Preço e Marca)
plt.figure(figsize=(10, 6))
plt.scatter(df['Preço'], df['Marca_Cod'], color='green')
plt.title('Dispersão entre Preço e Marca')
plt.xlabel('Preço')
plt.ylabel('Marca_Cod')
plt.grid(True)
plt.show()

# Mapa de Calor (Correlação entre as variáveis numéricas)
corr = df[['Nota', 'N_Avaliações', 'Qtd_Vendidos_Cod', 'Preço']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Mapa de Calor: Correlação entre as Variáveis')
plt.show()

# Gráfico de Barra (Top 20 Marcas)
marca_count = df['Marca'].value_counts()
top_20_marca = marca_count.head(20)
plt.figure(figsize=(12, 6))
top_20_marca.plot(kind='bar', color='lightcoral')
plt.title('Quantidade de Produtos por Marca (Top 20 Marcas)')
plt.xlabel('Marca')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.show()


# Gráfico de Pizza (Distribuição dos Materiais - Exibindo apenas os Top 10 materiais)
material_count = df['Material'].value_counts()
top_10_materiais = material_count.head(10)

plt.figure(figsize=(8, 8))
top_10_materiais.plot(kind='pie', autopct='%1.1f%%', colors=sns.color_palette("Set3", len(top_10_materiais)))
plt.title('Distribuição dos Materiais dos Produtos (Top 10 Materiais)')
plt.ylabel('')
plt.show()

# Gráfico de Densidade (Distribuição das Notas)
plt.figure(figsize=(10, 6))
sns.kdeplot(df['Nota'], fill=True, color='blue')
plt.title('Distribuição de Notas dos Produtos (Densidade)')
plt.xlabel('Nota')
plt.ylabel('Densidade')
plt.grid(True)
plt.show()

# Gráfico de Regressão (Relação entre Preço e Nota)
plt.figure(figsize=(10, 6))
sns.regplot(x='Preço', y='Nota', data=df, scatter_kws={'color':'orange'}, line_kws={'color':'red'})
plt.title('Relação entre Preço e Nota dos Produtos (Regressão)')
plt.xlabel('Preço')
plt.ylabel('Nota')
plt.grid(True)
plt.show()