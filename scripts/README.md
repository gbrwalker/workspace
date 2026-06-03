# scripts/

## `migrar_para_repos.sh`

Publica cada projeto de [`../projetos`](../projetos) como um **repositório público
próprio** no GitHub, preservando o histórico de cada um (via `git subtree split`).

Foi criado porque a publicação não pôde ser feita pelo ambiente automatizado
(o token da integração não tem permissão para criar repositórios). Rodando na sua
máquina, com o `gh` autenticado, resolve tudo de uma vez.

### Pré-requisitos
- [`gh` CLI](https://cli.github.com/) instalado e autenticado (`gh auth login`).
- Executar a partir da raiz deste repositório.

### Uso
```bash
# pré-visualização (não cria nem envia nada):
DRY_RUN=1 bash scripts/migrar_para_repos.sh

# execução real:
bash scripts/migrar_para_repos.sh
```

Ao final, o script imprime os links dos repositórios e as instruções para
**fixar (pin)** os projetos no perfil — passo que só o dono faz, pela interface
do GitHub.
