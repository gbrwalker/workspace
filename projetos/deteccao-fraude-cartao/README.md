# Detecção de Fraude em Cartão de Crédito

Classificação de transações fraudulentas em um cenário de **desbalanceamento extremo**:
apenas **492 fraudes em 284.807 transações (0,17%)**. Em problemas assim, acurácia não
diz nada — um modelo que prevê "tudo legítimo" acerta 99,8%. O objetivo real é
**maximizar o recall da fraude** sem gerar tantos falsos positivos a ponto de inviabilizar
a operação antifraude.

## Dataset

Base pública **Credit Card Fraud Detection** (Machine Learning Group – ULB), disponível no
Kaggle. As variáveis `V1`–`V28` já vêm anonimizadas por **PCA**; além delas, há `Time`,
`Amount` e o alvo `Class` (0 = legítima, 1 = fraude).

> **Os dados não são versionados** (arquivo grande). Para reproduzir:
> 1. Baixe em <https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud>
> 2. Coloque o `creditcard.csv` em `data/` (ou ajuste o caminho na primeira célula do notebook).

## Metodologia

1. **Análise inicial** — confirmação do desbalanceamento, ausência de nulos e do efeito do PCA.
2. **Limpeza** — remoção de 1.081 duplicatas; garantia do tipo do alvo.
3. **Divisão estratificada** — 212.794 amostras de treino / 70.932 de teste, preservando a
   proporção de fraudes em ambos.
4. **Modelagem e tuning** — *cross-validation* estratificada e `GridSearch` para busca de
   hiperparâmetros, com a métrica de seleção voltada ao recall da classe minoritária.
5. **Avaliação** — comparação por matriz de confusão, curva **ROC** e curva **Precision–Recall**.

## Modelos comparados

| Modelo | Estratégia | Recall (fraude) | Falsos positivos | AUC |
|---|---|---|---|---|
| **XGBoost** | `scale_pos_weight`, *subsample* e *colsample* ajustados | 0,864 | ~300 | **0,977** |
| **SVM (RBF)** | *undersampling* no treino + `class_weight='balanced'` | **0,915** | ~6.000 | ~0,96 |

## Conclusão

Não existe "melhor modelo" universal aqui — existe um **trade-off**:

- O **SVM** é o mais sensível (maior recall), mas gera ~6.000 falsos positivos, o que
  significa muito alerta para revisão manual.
- O **XGBoost** perde um pouco de recall, mas reduz os falsos positivos para ~300 e tem
  AUC superior (0,977) — entregando um fluxo de alertas muito mais limpo e operacionalmente viável.

Para um contexto antifraude real, o XGBoost tende a ser a escolha mais equilibrada; o SVM
faz sentido quando o custo de uma fraude não detectada supera de longe o custo da revisão.

📄 A **apresentação executiva** (`Apresentação Modelo de Detecção de Fraudes.docx`) traduz
essa análise técnica em recomendação de negócio.

## Como executar

```bash
pip install -r requirements.txt
jupyter notebook Projeto_Final_Creditcard_Fraud_ML.ipynb
```

## Stack

`pandas` · `numpy` · `scikit-learn` · `XGBoost` · `matplotlib`
