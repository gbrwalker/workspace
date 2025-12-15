
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('clientes-v3-preparado.csv')


df_corr = df[['salario', 'idade', 'anos_experiencia', 'numero_filhos', 'nivel_educacao_cod', 'area_atuacao_cod', 'estado_cod']].corr()
#Heatmap de correlação
plt.figure(figsize=(10, 8))
sns.heatmap (df_corr, annot=True, fmt=".2f")
plt.title('Mapa de Calor da Correlação entre Variáveis')
plt.show()

#Já usei
#Countplot
sns.countplot(x='estado_civil', data=df)
plt.title('Distribuição do Estado Civil')
plt.xlabel('Estado_Civil')
plt.ylabel('Contagem')
plt.show()

#Countplot com legenda
sns.countplot(x='estado_civil', hue='nivel_educacao', data=df)
plt.title('Distribuição do Estado Civil')
plt.xlabel('Estado Civil')
plt.ylabel('Contagem')
plt.legend(title='Nivel de Educacao')
plt.show()