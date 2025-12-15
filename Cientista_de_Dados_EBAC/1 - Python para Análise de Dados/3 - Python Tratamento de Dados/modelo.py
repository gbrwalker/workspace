import seaborn as sn
import matplotlib.pyplot as plt
import pandas as pd
import numpy as ny
import sklearn as sk
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

df = pd.read_csv('CHURN_CREDIT_MOD08_PART3.csv', delimiter=',')

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

# Separar os dados em features (x) e o alvo (y)
x = df.drop('Churn', axis=1)
y = df['Churn']

# Separar os dados em conjuntos de treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=42)
# test_size determina a proporção dos dados que serão separados para teste (25%)
# random_state é usado para garantir que a divisão seja reproduzida

# Verificando o gabarito
print(x_train)
print(x_test)
print(y_train)
print(y_test)

# Outra forma de verificar o gabarito (número de linhas de x e y devem ser iguais)
print(f"Tamanho de x_train: {x_train.shape}")
print(f"Tamanho de x_test: {x_test.shape}")
print(f"Tamanho de y_train: {y_train.shape}")
print(f"Tamanho de y_test: {y_test.shape}")

# Balanceamento

# Primeira etapa é verificar como esta o balanceamento da nossa variavel preditora, Churn
# Caso uma das classes esteja em baixa quantidade nosso modelo futuramente pode ter dificuldade para preves essa classe
churn_counts = df['Churn'].value_counts()
plt.figure(figsize=(10, 8))
churn_counts.plot(kind='bar', color=['blue', 'orange'])
# plt.show()

# Calcular e imprimir as porcentagens dos valores na coluna 'Churn'
print((df['Churn'].value_counts(normalize=True) * 100))

# Criando uma instância do SMOTE
smote = SMOTE(random_state=42)

# Aplicando o SMOTE aos dados de trinamento (x_train, y_train)
x_train_balanced, y_train_balanced = smote.fit_resample(x_train, y_train)

# Verificando a distribuição das classes após o balanceamento
print(f"Distribuição das classes após o balanceamento: {y_train_balanced.value_counts()}")

train_balance = y_train_balanced.value_counts()
print(f"Balanceamento em y_train: {train_balance}")

y_train_balanced.to_csv('y_train_balances.csv', index=False)
x_train_balanced.to_csv('x_train_balances.csv', index=False)
y_test.to_csv('y_test.csv', index=False)
x_test.to_csv('x_test.csv', index=False)