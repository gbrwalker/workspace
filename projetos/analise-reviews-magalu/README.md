# Análise de Sentimento de Reviews com LLM (Gemini)

Pipeline que transforma avaliações reais de clientes da **Magalu** (coletadas do Google
Maps) em insights acionáveis, usando a **API do Google Gemini** para classificar
sentimento e identificar categorias relevantes de feedback — como reclamações e menções
ao Procon.

A proposta é mostrar **engenharia aplicada com LLM**: não apenas chamar um modelo, mas
estruturar coleta, *prompting*, processamento em lote e consolidação dos resultados de
forma confiável e em escala.

## Pipeline

1. **Coleta** — avaliações extraídas do Google Maps via [Outscraper](https://outscraper.com/),
   carregadas em um `DataFrame`.
2. **Preparação** — estruturação e limpeza dos textos com pandas.
3. **Classificação com LLM** — cada comentário é enviado ao Gemini com um *prompt* desenhado
   para retornar sentimento e categoria de forma consistente.
4. **Processamento em lote** — varredura da base com controle de *rate limit* (pausas entre
   chamadas) e *parsing* das respostas do modelo.
5. **Consolidação** — os resultados são empilhados para análise agregada dos sentimentos.

## Decisões de engenharia

- **Sem segredo no código.** A chave da API é lida de `GOOGLE_API_KEY` (variável de
  ambiente). Veja [`.env.example`](.env.example).
- **Controle de *rate limit*** com pausas entre chamadas, evitando bloqueios da API.
- **Modelo atual** (`gemini-1.5-flash`), bom equilíbrio entre custo e qualidade para
  classificação em volume.

## Como executar

```bash
pip install -r requirements.txt
export GOOGLE_API_KEY="sua-chave-aqui"   # ou use um arquivo .env
jupyter notebook review_magalu.ipynb
```

> **Dados:** o arquivo `dados_magalu.xlsx` (reviews coletados) **não é versionado**, por
> conter dados extraídos de terceiros. Gere o seu próprio via Outscraper a partir da página
> da loja no Google Maps, ou adapte a etapa de coleta para outra fonte.

## Stack

`pandas` · `numpy` · `google-generativeai` (Gemini 1.5 Flash)
