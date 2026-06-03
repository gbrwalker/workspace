import pandas as pd

lista_nomes = ['Ana', 'Marcos', 'Carlos']
print('Lista de nomes :\n', lista_nomes)
print('Primeiro elemento da lista :\n', lista_nomes[0])

dicionario_pessoa = {
    'nome': 'Ana',
    'idade': 20,
    'cidade': 'Sao Paulo'
}
print('Dicionario de uma pessoa :\n', dicionario_pessoa)
print('Atributo de um dicionario :\n', dicionario_pessoa.get('nome'))

dados = [
    {'nome': 'Ana', 'idade': 20, 'cidade': 'Sao Paulo'},
    {'nome': 'Marcos', 'idade': 28, 'cidade': 'Belo Horizonte'},
    {'nome': 'Carlos', 'idade': 35, 'cidade': 'Rio de Janeiro'}
]
print('Lista de dicionarios :\n', dados)
print('Selecionando uma pessoa :\n', dados[2].get('nome'))

df = pd.DataFrame(dados)
print('Data frame :\n', df)

print(df['nome'])

print(df[['nome', 'idade']])

print('Primeira linha : \n', df.iloc[0])

df['salario'] = [4100, 3600, 5200]

df.loc[len(df)] = {
    'nome': 'Gabriel',
    'idade': 26,
    'cidade': 'Joinville',
    'salario': 4000
}
print('Data frame atual : \n', df)

df.drop('salario', axis=1, inplace = True)

filtro_idade = df[df['idade'] >= 26]
print('Filtro idade :\n', filtro_idade)

df.to_csv('dados.csv', index=False)