import requests
from bs4 import BeautifulSoup

url = 'https://wiki.python.org.br/AprendaMais'
requisicao = requests.get(url)
extracao = BeautifulSoup(requisicao.text,'html.parser')

# Exibir o Texto
#print(extracao)

# Desafio
contador_p = 0
contador_h2 = 0

for linha_texto in extracao.find_all('h2'):
   contador_h2 += 1

for linha_texto in extracao.find_all('p'):
   contador_p += 1

print('paragrafos :', contador_p)
print('titulos :', contador_h2)