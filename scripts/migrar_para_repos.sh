#!/usr/bin/env bash
#
# Migra cada projeto de projetos/ para um repositório PÚBLICO próprio no GitHub,
# preservando o histórico de cada um (via git subtree split).
#
# Pré-requisitos (na sua máquina):
#   - gh CLI instalado e autenticado:  gh auth login
#   - rodar a partir do repositório workspace, na branch que tem os projetos
#     (ex.: claude/kind-mccarthy-GvUBs ou main, após o merge do PR #1)
#
# Uso:
#   bash scripts/migrar_para_repos.sh
#   DRY_RUN=1 bash scripts/migrar_para_repos.sh   # apenas mostra o que faria
#
set -euo pipefail

OWNER="gbrwalker"
DRY_RUN="${DRY_RUN:-0}"

# pasta em projetos/  |  nome do repo  |  descrição
PROJECTS=(
  "previsao-km-frota|previsao-km-frota|Modelo de previsao de quilometragem de frota (MKM): recebe (placa, data, km) e preve km diario, km futuro e dias ate revisao. Python, pandas, pytest."
  "predicao-churn-telecom|predicao-churn-telecom|Predicao de churn em telecom com scikit-learn: pipeline modular, testes e avaliacao honesta (ROC-AUC 0,85)."
  "deteccao-fraude-cartao|deteccao-fraude-cartao|Deteccao de fraude em cartao de credito com classes desbalanceadas: XGBoost x SVM, foco em recall."
  "analise-reviews-magalu|analise-reviews-magalu|Analise de sentimento de reviews com a API do Google Gemini (engenharia com LLM)."
  "classificador-noticias-nlp|classificador-noticias-nlp|Classificacao automatica de noticias (NLP): coleta RSS + TF-IDF + LinearSVC."
)

run() {
  if [ "$DRY_RUN" = "1" ]; then
    printf '  [dry-run]'; printf ' %q' "$@"; printf '\n'
  else
    "$@"
  fi
}

# --- checagens de ambiente -------------------------------------------------
command -v gh >/dev/null || { echo "ERRO: gh CLI nao encontrado. Instale: https://cli.github.com/"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "ERRO: gh nao autenticado. Rode: gh auth login"; exit 1; }
ROOT="$(git rev-parse --show-toplevel)" || { echo "ERRO: rode dentro do repositorio git."; exit 1; }
cd "$ROOT"

# garante que o git use as credenciais do gh para push via https
run gh auth setup-git

# --- migração --------------------------------------------------------------
for entry in "${PROJECTS[@]}"; do
  IFS="|" read -r path repo desc <<< "$entry"
  prefix="projetos/$path"

  echo ""
  echo "=== $repo ==="
  if [ ! -d "$prefix" ]; then
    echo "  AVISO: $prefix nao existe nesta branch — pulando."
    continue
  fi

  # 1) cria o repositorio (vazio) se ainda nao existir
  if gh repo view "$OWNER/$repo" >/dev/null 2>&1; then
    echo "  repo $OWNER/$repo ja existe — reaproveitando."
  else
    run gh repo create "$OWNER/$repo" --public -d "$desc"
  fi

  # 2) extrai o subdiretorio com seu historico para uma branch temporaria
  branch="export-$repo"
  git branch -D "$branch" >/dev/null 2>&1 || true
  echo "  extraindo historico de $prefix ..."
  run git subtree split --prefix="$prefix" -b "$branch"

  # 3) envia para a branch main do novo repo
  echo "  enviando para $OWNER/$repo ..."
  run git push "https://github.com/$OWNER/$repo.git" "$branch:main"

  git branch -D "$branch" >/dev/null 2>&1 || true
  echo "  OK -> https://github.com/$OWNER/$repo"
done

# --- resumo final ----------------------------------------------------------
echo ""
echo "================================================================"
echo "Repositorios:"
for entry in "${PROJECTS[@]}"; do
  IFS="|" read -r path repo desc <<< "$entry"
  echo "  https://github.com/$OWNER/$repo"
done
cat <<'EOF'

Para FIXAR no perfil (somente o dono, pela interface):
  1. Acesse https://github.com/gbrwalker
  2. Clique em "Customize your pins"
  3. Marque os projetos acima (ate 6) e salve.
EOF
