import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('MODULO7_PROJETOFINAL_BASE_SUPERMERCADO - MODULO7_PROJETOFINAL_BASE_SUPERMERCADO (1).csv.csv', delimiter=',')

print(df.head(10))


# Média dos preços por categoria de produto
med_precos_categoria = df.groupby('Categoria')['Preco_Normal'].mean().sort_values(ascending=False)
print(f"\n Média por {med_precos_categoria}")

# Mediana dos preços por categoria de produto
mediana_precos_categoria = df.groupby('Categoria')['Preco_Normal'].median().sort_values(ascending=False)
print(f"\nMedia por {mediana_precos_categoria}")

# Desvio padrão por categoria
desvio_padrao_por_categoria = df.groupby('Categoria')['Preco_Normal'].std().reset_index()
print(f"\n Desvio padrão: \n{desvio_padrao_por_categoria}")

# Consolidar média, mediana e desvio padrão criando um DataFrame
mmd_por_categoria = df.groupby('Categoria')['Preco_Normal'].agg(
    median = 'mean',
    mediana = 'median',
    desvio_padrao = 'std'
).reset_index()

# Buscando os top devios
top_desvio = mmd_por_categoria.sort_values(by='desvio_padrao', ascending=False)
print(top_desvio)

# Boxplot do preço normal com a categoria que tem o maior desvio_padrao
lacteos = df[df['Categoria'] == 'lacteos']['Preco_Normal']
plt.figure(figsize=(12, 6))
plt.boxplot(lacteos, label=['Lacteos'])
plt.title('Boxplot do preco_normal para a categoria lacteos', fontsize=16)
plt.ylabel('Preço Normal')
plt.tight_layout()
plt.savefig('imagens/Boxplot_categoria_lacteos.png')
plt.show()


# Gráfico de barras para apresentar o desconto por categoria
plt.figure(figsize=(12, 6))
desconto_categoria = df.groupby('Categoria')['Desconto'].mean() # Agrupando os dados por categoria e calculando a média de descontos por categoria
plt.bar(desconto_categoria.index, desconto_categoria, color='skyblue')
plt.title('Distribuição de descontos por categoria')
plt.xlabel('Categoria')
plt.ylabel('Desconto')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('imagens/Barras_desconto_categoria.png')
plt.show()



# Gráfico de mapa interativo agrupando os dados por categoria, marca, e trazendo a média de desconto
desconto_categoria_marca = df.groupby(['Categoria', 'Marca'])['Desconto'].mean().reset_index() # Agrupando os dados do DataFrame por categoria, marca e calculando a média de desconto para cada categoria e marca

#Criando o gráfico treemap
fig = px.treemap(desconto_categoria_marca,
                 path=['Categoria', 'Marca'],
                 values='Desconto',
                 title='Desconto por categoria e marca',
                 color='Marca'
                 )
fig.show()

fig.write_image('imagens/Treemap_Desconto.png', engine="kaleido")



