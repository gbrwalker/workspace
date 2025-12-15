# Classificação Automática de Notícias com Processamento de Linguagem Natural

## Descrição do Projeto

Este projeto tem como objetivo desenvolver um pipeline de dados capaz de coletar notícias automaticamente, realizar o pré-processamento textual e aplicar técnicas de Processamento de Linguagem Natural (PLN) para classificar textos jornalísticos em categorias relevantes.

A proposta é demonstrar, de forma prática e acadêmica, a aplicação de modelos supervisionados de aprendizado de máquina em dados reais e não estruturados, contemplando todas as etapas clássicas de um projeto de ciência de dados: coleta, preparação, modelagem, avaliação e interpretação dos resultados.

---

## Objetivo

Construir um fluxo completo que permita:

- Coletar notícias automaticamente a partir de fontes RSS
- Preparar e normalizar textos para análise
- Treinar um modelo de classificação de textos
- Avaliar o desempenho do modelo de forma adequada
- Visualizar e interpretar os resultados obtidos

---

## Estrutura do Projeto

O projeto está organizado de forma sequencial em um notebook, seguindo as etapas abaixo:

1. Coleta de dados  
2. Pré-processamento dos textos  
3. Construção do dataset de treinamento  
4. Treinamento do modelo de classificação  
5. Avaliação do modelo  
6. Visualização dos resultados  
7. Conclusões e insights finais  

---

## Coleta de Dados

A coleta de dados é realizada por meio de feeds RSS de portais de notícias, permitindo a obtenção automática de títulos, descrições, fonte da notícia e data de coleta.

Essa abordagem garante acesso a dados reais, atualizados e não estruturados, sem a necessidade de scraping pesado ou dependência de APIs complexas.

---

## Pré-processamento dos Textos

Os textos coletados passam por uma etapa de normalização, que inclui:

- Conversão para letras minúsculas
- Remoção de caracteres especiais
- Padronização de espaços em branco
- Junção de título e descrição em um único campo textual

O objetivo dessa etapa é reduzir ruído e facilitar a extração de padrões relevantes pelo modelo de aprendizado de máquina.

---

## Dataset de Treinamento

Foi construído um dataset de treinamento supervisionado contendo exemplos representativos de cada classe definida no projeto. As categorias finais utilizadas foram:

- evento_critico: acidentes, interdições e incêndios
- clima: eventos climáticos com impacto operacional
- outro: eventos institucionais, culturais ou informativos

A redução consciente do número de classes permitiu diminuir a ambiguidade semântica e melhorar a capacidade de generalização do modelo.

---

## Modelagem

O modelo de classificação foi construído utilizando:

- Vetorização TF-IDF para representação dos textos
- Classificador Linear Support Vector Machine (LinearSVC)

Essa combinação foi escolhida por apresentar bom desempenho em problemas de classificação textual, além de ser interpretável e adequada para projetos acadêmicos.

O conjunto de dados foi dividido em treino e teste utilizando `train_test_split` com estratificação, garantindo uma avaliação justa do modelo.

---

## Avaliação do Modelo

O desempenho do modelo foi avaliado com base em:

- Acurácia
- Precision, recall e f1-score por classe
- Matriz de confusão

Os resultados obtidos refletem um cenário realista para bases de dados reduzidas e textos curtos, demonstrando aprendizado efetivo sem sobreajuste.

Os erros observados ocorreram majoritariamente entre classes semanticamente próximas, o que é esperado em dados jornalísticos.

---

## Visualização dos Resultados

Foram geradas visualizações para facilitar a interpretação dos resultados, incluindo:

- Distribuição das classes no conjunto de teste
- Distribuição das classes preditas pelo modelo

Essas visualizações auxiliam na compreensão do comportamento do classificador e evidenciam tendências na classificação dos textos.

---

## Conclusões

O projeto demonstrou que é possível estruturar um pipeline completo de classificação de textos utilizando técnicas acessíveis de Processamento de Linguagem Natural. A abordagem adotada mostrou-se adequada ao objetivo acadêmico proposto, com resultados interpretáveis e metodologicamente corretos.

Apesar das limitações relacionadas ao tamanho do dataset e à construção manual da base de treinamento, os resultados confirmam a viabilidade da solução e estabelecem uma base sólida para evoluções futuras.

---

## Possíveis Evoluções

Como continuidade do projeto, podem ser exploradas as seguintes melhorias:

- Expansão do dataset com exemplos reais rotulados
- Aplicação de validação cruzada
- Análise dos termos mais relevantes por classe
- Implementação de classificação hierárquica
- Integração com dashboards interativos

---

## Tecnologias Utilizadas

- Python
- Pandas
- Scikit-learn
- Feedparser
- Matplotlib

---

## Observações Finais

Este projeto foi desenvolvido com foco acadêmico, priorizando clareza metodológica, avaliação honesta e interpretação crítica dos resultados, atendendo plenamente aos requisitos da atividade proposta.
