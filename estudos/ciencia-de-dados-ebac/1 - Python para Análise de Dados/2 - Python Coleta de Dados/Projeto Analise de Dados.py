import requests
from bs4 import BeautifulSoup
import pandas

#print('Request :')

response = requests.get('https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/historico/')
#print(response.text[:600])

#print('BeautifulSoup')

soup = BeautifulSoup(response.text,'html.parser')
#print(soup.prettify()[:1000])

#print('Pandas :')
url_dados = pandas.read_html('https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/historico/')
print(url_dados[0].head(15))