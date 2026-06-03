import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as ny
import sklearn as sk
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv('CHURN_CREDIT_MOD08_PART3.csv', delimiter=',')

print(df.head(10))

# Matriz Correlação
print(df.select_dtypes(include=['number']).corr())

# Cluster Map
correlation_matrix = df.select_dtypes(include='number').corr()

# Plotar o mapa de calor da matriz de correlação
plt.figure(figsize=(10, 8))
sn.heatmap(correlation_matrix,
           annot=True,
           cmap='coolwarm',
           fmt=".2f",
           annot_kws={"size": 10})
plt.title('Matriz de Correlação')
# plt.show()

# Criando uma instância do Label Encoder
label_encoder = LabelEncoder()

# Aplicando o Label Encoder para a coluna "Genero"- ideal
df['Genero_encoded'] = label_encoder.fit_transform(df['Genero'])

# Aplicar o One Hor para a coluna "Pais" - nesse caso não criamos instância

# Essa função transforma a coluna "Pais" em várias colunas binárias
df = pd.get_dummies(df,
                    columns=['Pais'],
                    prefix='Pais',
                    drop_first=True) 

print(df)

print(df.dtypes)

# Alterar os dados booleanos para numéricos
for column in df.columns:
    if df[column].dtype == 'bool':
        df[column] = df[column].astype(int)

print(df)

# Dropar as colunas com os atributos categóricos
df = df.drop(['Genero'], axis=1)
print(df)

# Agora é possível fazer a correlação das categorias categóricas
print(df.corr())