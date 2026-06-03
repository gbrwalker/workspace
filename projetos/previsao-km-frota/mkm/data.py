"""Carregamento e validação do trio de entrada ``(placa, data, km)``.

A entrada do modelo é **deliberadamente simples** — qualquer pipeline de
telemetria interno pode produzir esse formato, o que torna o modelo
independente das fontes de origem.
"""
from __future__ import annotations

from pathlib import Path
from typing import IO, Union

import pandas as pd

REQUIRED_COLUMNS = ("placa", "data", "km")


def load_readings(source: Union[str, Path, IO, pd.DataFrame]) -> pd.DataFrame:
    """Carrega leituras de odômetro a partir de CSV/Parquet ou DataFrame.

    Parameters
    ----------
    source : caminho para arquivo ``.csv``/``.parquet``, *file-like* ou
        ``DataFrame`` pronto.

    Returns
    -------
    DataFrame com as colunas ``placa`` (str), ``data`` (datetime) e ``km`` (float),
    ordenado por ``(placa, data)`` e sem duplicatas.
    """
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    elif isinstance(source, (str, Path)):
        path = Path(source)
        if path.suffix.lower() == ".parquet":
            df = pd.read_parquet(path)
        else:
            df = pd.read_csv(path)
    else:
        # file-like (BytesIO/StringIO)
        df = pd.read_csv(source)

    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(
            f"colunas obrigatorias ausentes: {sorted(missing)}. "
            f"esperado: {REQUIRED_COLUMNS}"
        )

    df["placa"] = df["placa"].astype(str).str.strip().str.upper()
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df["km"] = pd.to_numeric(df["km"], errors="coerce")

    return _clean(df)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Remove inconsistências comuns em telemetria de frota.

    - Linhas com ``data`` ou ``km`` ausentes/inválidos.
    - Quilometragem negativa (impossível por construção do hodômetro).
    - Duplicatas de ``(placa, data)`` — mantém o maior km (mais recente do dia).
    - Leituras decrescentes dentro do mesmo veículo (sinal de troca ou erro);
      mantemos a primeira ocorrência e descartamos a regressão.
    """
    df = df.dropna(subset=["data", "km"])
    df = df[df["km"] >= 0]

    df = (
        df.sort_values(["placa", "data", "km"])
        .drop_duplicates(subset=["placa", "data"], keep="last")
        .reset_index(drop=True)
    )

    running_max = df.groupby("placa")["km"].cummax()
    df = df[df["km"] >= running_max - 1e-6].reset_index(drop=True)
    return df


def split_temporal(
    df: pd.DataFrame, cutoff: Union[str, pd.Timestamp]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Divide os dados em treino/teste por uma data de corte.

    Modelar séries temporais com *split* aleatório vaza informação do futuro
    para o treino. O recorte temporal é o único correto.
    """
    cutoff = pd.Timestamp(cutoff)
    train = df[df["data"] <= cutoff].reset_index(drop=True)
    test = df[df["data"] > cutoff].reset_index(drop=True)
    return train, test
