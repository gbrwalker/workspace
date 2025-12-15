Análise de Churn em uma Empresa de Telecomunicações

Este repositório contém um script em Python para analisar dados de churn em uma empresa de telecomunicações. Ele realiza análises estatísticas, univariadas e bivariadas, além de identificar outliers e salvar gráficos como imagens para facilitar a visualização.

## Requisitos

Certifique-se de ter as seguintes bibliotecas instaladas:

- pandas
- seaborn
- matplotlib
- plotly

Você pode instalá-las usando:
```bash
pip install pandas seaborn matplotlib plotly
```


Descrição do Script

O script realiza as seguintes etapas:



## Carregamento dos Dados

- Lê o arquivo arquivo_analise_telecon.csv para um DataFrame.

- Exibe as 10 primeiras linhas e estatísticas descritivas usando describe().



## Análise Univariada

Distribuição de Churn

![imagens/calculate_churn_percentage.png](imagens/calculate_churn_percentage.png)


Distribuição de Dependentes

![- Histograma para visualizar a quantidade de dependentes por cliente.](imagens/analysis_dependents.png)



## Identificação de Outliers

- Utiliza gráficos do tipo boxplot para identificar outliers nas seguintes variáveis:

Tempo de Atendimento

![alt text](imagens/search_outliers_client_hour.png)


Pagamento Mensal

![alt text](imagens/search_outliers_payment_mounth.png)

Pagamento Total

![alt text](imagens/search_outliers_full_payment.png)



## Análise Bivariada

Churn x Casado(a)

![imagens/percent_married_churn.png |](imagens/percent_married_churn.png)

Churn x Tipo de Contrato

![alt text](imagens/percent_contract_type_churn.png)

Churn x Dependentes

![- Gráfico de barras empilhadas mostrando a relação entre churn e número de dependentes.](imagens/percent_dependents_churn.png)

Churn x Gênero

![- Gráfico de barras empilhadas mostrando a relação entre churn e gênero.](imagens/percent_gender_churn.png)

Churn x Idosos

![- Gráfico de barras empilhadas mostrando a relação entre churn e se o cliente é idoso.](imagens/percent_elderly_churn.png)