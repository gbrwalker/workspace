# Gabriel Walker Schulze

**Ciência de Dados · Machine Learning · Engenharia com LLMs**

Construo soluções de dados de ponta a ponta — da coleta e tratamento à modelagem,
avaliação e comunicação dos resultados. Aqui você encontra meus projetos aplicados,
o material da minha formação e minhas certificações, organizados para que dê para
entender rápido o que sei fazer.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-006600)
![Gemini API](https://img.shields.io/badge/Gemini_API-8E75B2?logo=googlegemini&logoColor=white)

---

## 🚀 Projetos em destaque

Cada projeto abaixo tem README próprio com contexto, decisões e resultados.

### 1. Previsão de Quilometragem de Frota (MKM) — autoria própria, uso real
**Modelo que uso na gestão de frota, publicado a partir do núcleo para preservar a privacidade dos sistemas internos.**

Recebe como entrada apenas o trio essencial — **`placa`, `data`, `km`** — e responde
três perguntas práticas do dia a dia da operação: qual a média diária de cada
veículo, qual o km esperado em uma data futura e em quantos dias um veículo bate
em um km alvo (útil para revisão preventiva).

- Estratégia hierárquica por veículo (regressão linear → incrementos → mediana da
  frota) para responder bem em qualquer estágio de histórico.
- Avaliação **temporal**, não aleatória, com erro reportado **por horizonte de previsão**.
- Resultado em frota sintética de 50 veículos: **MAPE 0,49%**, com ~510 km de erro
  médio em previsões de até 30 dias.
- CLI utilitário: `python -m mkm.predict --placa ABC1A23 --data 2027-06-30`.

🔧 `pandas` · `numpy` · `matplotlib` · `pytest`
📁 [`projetos/previsao-km-frota`](projetos/previsao-km-frota)

### 2. Predição de Churn em Telecom
**Engenharia de ML: código modular, testes automatizados e resultados reprodutíveis.**

Modelo que prevê quais clientes vão cancelar o serviço, para o time de retenção agir
antes. Diferente de um notebook, é estruturado como **código de produção**: pacote
modular, **testes (`pytest`)** e treino reprodutível por linha de comando.

- *Pipeline* scikit-learn (sem vazamento de dados), `class_weight='balanced'` e
  *permutation importance* para interpretar o modelo.
- Tratamento de problemas reais de qualidade de dados detectados na base.
- Resultado: **ROC-AUC 0,85**, capturando ~72% dos cancelamentos — com matriz de confusão,
  curva ROC e ranking de variáveis **gerados pelo próprio código**.

🔧 `pandas` · `scikit-learn` · `matplotlib` · `pytest`
📁 [`projetos/predicao-churn-telecom`](projetos/predicao-churn-telecom)

### 3. Detecção de Fraude em Cartão de Crédito
**Classificação com classes extremamente desbalanceadas (0,17% de fraudes).**

Modelei a detecção de fraude sobre a base pública da ULB/Kaggle (284.807 transações,
492 fraudes). O foco foi **maximizar o recall** da classe minoritária sem inflar os
falsos positivos a ponto de inviabilizar a operação.

- Pipeline: limpeza, *split* estratificado, *cross-validation* estratificada e `GridSearch`.
- Comparei **XGBoost** e **SVM (RBF)** com *undersampling* no treino.
- Resultado: o XGBoost entregou **Recall 0,86 / AUC 0,977** com ~300 falsos positivos;
  o SVM chegou a **Recall 0,92**, mas com ~6.000 falsos positivos — uma análise explícita
  do *trade-off* entre sensibilidade e custo operacional.
- Acompanha uma **apresentação executiva** traduzindo o resultado técnico para decisão de negócio.

🔧 `pandas` · `scikit-learn` · `XGBoost` · `matplotlib`
📁 [`projetos/deteccao-fraude-cartao`](projetos/deteccao-fraude-cartao)

### 4. Análise de Sentimento de Reviews com LLM (Gemini)
**Engenharia com LLM aplicada a dados reais de clientes.**

Pipeline que analisa avaliações reais da Magalu coletadas do Google Maps e usa a
**API do Gemini** para classificar sentimento e identificar categorias acionáveis
(reclamação, menção a Procon, etc.), gerando insights para decisão estratégica.

- *Prompt design* para classificação consistente em escala.
- Processamento em lote com controle de *rate limit* e *parsing* das respostas do modelo.
- Chave de API lida de variável de ambiente — nada de segredo no código.

🔧 `pandas` · `google-generativeai` (Gemini 1.5 Flash) · `numpy`
📁 [`projetos/analise-reviews-magalu`](projetos/analise-reviews-magalu)

### 5. Classificação Automática de Notícias (NLP)
**Pipeline de NLP reprodutível, da coleta à avaliação.**

Coleta notícias automaticamente via *feeds* RSS e classifica os textos em categorias
operacionais. Projeto **totalmente reprodutível** — basta rodar o notebook, que ele
coleta os dados ao vivo.

- Normalização textual → vetorização **TF-IDF** (uni + bigramas) → **LinearSVC** (`class_weight='balanced'`).
- Avaliação honesta com *precision/recall/f1* por classe e matriz de confusão.

🔧 `feedparser` · `scikit-learn` · `pandas` · `matplotlib`
📁 [`projetos/classificador-noticias-nlp`](projetos/classificador-noticias-nlp)

---

## 📂 Organização do repositório

```
projetos/        Projetos aplicados (cada um com README, requirements e dados documentados)
estudos/         Material de formação — exercícios e notebooks de curso, mantidos como histórico
certificados/    Comprovantes de cursos e formações
```

- **`projetos/`** é a vitrine: código que resolve um problema de ponta a ponta.
- **`estudos/`** reúne a trilha de aprendizado (formação EBAC em Ciência de Dados e
  práticas de front-end no estilo JavaScript30). Fica separado de propósito, para não
  competir com os projetos aplicados.

---

## 🎓 Certificações

Comprovantes disponíveis em [`certificados/`](certificados):

- **Profissão: Cientista de Dados** — EBAC
- **Inteligência Artificial** — EBAC
- **Introdução à Programação** — EBAC
- **Análise e Desenvolvimento de Sistemas** — UNINASSAU
- JavaScript — freeCodeCamp, Kenzie Academy e Trybe
- Inglês

---

## 🛠️ Stack

**Dados & ML:** Python, pandas, NumPy, scikit-learn, XGBoost, Matplotlib, Seaborn
**LLM:** API do Google Gemini (`google-generativeai`)
**NLP:** TF-IDF, feedparser
**Engenharia & boas práticas:** Pipelines scikit-learn, testes com `pytest`, Git, ambientes reprodutíveis
**BI & SQL:** Power BI, Looker Studio, SQL
**Web:** JavaScript, HTML, CSS

---

## 📫 Contato

- **LinkedIn:** [linkedin.com/in/walker-dev](https://www.linkedin.com/in/walker-dev)
- **E-mail:** gabrielwalker14@gmail.com
