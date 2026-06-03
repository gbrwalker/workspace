"""Predição de churn (evasão de clientes) para uma operadora de telecom.

Pacote organizado em módulos com responsabilidade única:

- ``data``      : carregamento e limpeza da base.
- ``pipeline``  : pré-processamento + modelo (scikit-learn ``Pipeline``).
- ``train``     : treino, avaliação e exportação de modelo e relatórios.
- ``plots``     : geração das figuras de avaliação.
"""
