"""Carregamento e limpeza da base de churn.

A base de origem usa nomes de colunas mistos (PT/EN) — eles são preservados
como vieram para manter rastreabilidade com o dado bruto.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "telco_churn.csv"

TARGET = "Churn"
ID_COL = "customerID"

NUMERIC_FEATURES = ["Tempo_como_Cliente", "Pagamento_Mensal", "Total_Pago"]
CATEGORICAL_FEATURES = [
    "Genero",
    "Idoso",
    "Casado",
    "Dependents",
    "PhoneService",
    "Servico_Internet",
    "Servico_Seguranca",
    "Suporte_Tecnico",
    "StreamingTV",
    "Tipo_Contrato",
    "PaymentMethod",
]


def load_raw(path: Path | str = DATA_PATH) -> pd.DataFrame:
    """Lê o CSV bruto (delimitado por ``;`` e com BOM)."""
    return pd.read_csv(path, sep=";", encoding="utf-8-sig")


def _normalize_genero(s: pd.Series) -> pd.Series:
    """Consolida encodings inconsistentes (``M``/``f``/``F``) em ``{Male, Female}``.

    Mantém ``NaN`` onde o valor é ausente, para ser imputado no pipeline.
    """
    return s.str[0].str.upper().map({"M": "Male", "F": "Female"})


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica a limpeza necessária para a modelagem.

    - Remove o identificador do cliente (não é preditor).
    - ``Total_Pago`` chega com strings vazias em clientes recém-chegados;
      coagimos para numérico (vira ``NaN``, imputado no pipeline).
    - ``Idoso`` é um indicador 0/1 — tratado como categórico.
    - Corrige inconsistências de encoding encontradas na base bruta:
      ``Genero`` (``M``/``f``/``F`` → ``Male``/``Female``) e
      ``Servico_Internet`` (``dsl`` → ``DSL``).
    - ``Churn`` (``Yes``/``No``) é convertido para 0/1.
    """
    df = df.copy()
    df = df.drop(columns=[c for c in (ID_COL,) if c in df.columns])
    df["Total_Pago"] = pd.to_numeric(df["Total_Pago"], errors="coerce")
    df["Idoso"] = df["Idoso"].astype(str)
    df["Genero"] = _normalize_genero(df["Genero"])
    df["Servico_Internet"] = df["Servico_Internet"].replace({"dsl": "DSL"})
    df[TARGET] = (df[TARGET].astype(str).str.strip().str.lower() == "yes").astype(int)
    return df


def load_dataset(path: Path | str = DATA_PATH) -> tuple[pd.DataFrame, pd.Series]:
    """Retorna ``(X, y)`` prontos para alimentar o pipeline."""
    df = clean(load_raw(path))
    y = df[TARGET]
    X = df.drop(columns=[TARGET])
    return X, y
