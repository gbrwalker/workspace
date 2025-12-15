import requests

def enviar_arquivos():
    # Caminho do arquivo para upload
    caminho = 'C:/Users/gwalk/workspace/projects/Python/produtos_informatica.xlsx'

    # Enviar o arquivo
    requisicao = requests.post('https://file.io', files={'file': open(caminho, 'rb')})
    saida_requisicao = requisicao.json()

    print(saida_requisicao)
    url = saida_requisicao['link']
    print("Arquivo enviado. Link :", url)


def receber_arquivos(file_url):
    # Receber o arquivo
    requisicao = requests.get(file_url)

    # Salvar o arquivo
    if requisicao.ok:
        with open('arquivo_baixado.xlsx', 'wb') as file:
            file.write(requisicao.content)
        print('Arquivo baixado com sucesso !')
    else:
        print('Erro :', requisicao.json())




# enviar_arquivos()
receber_arquivos('https://file.io/avoc0WBJJYq5')

