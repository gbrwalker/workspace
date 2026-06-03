"""Testes da camada de carregamento e limpeza."""
from io import StringIO

import pandas as pd
import pytest

from mkm.data import load_readings, split_temporal


def _csv(rows: list[tuple[str, str, float]]) -> StringIO:
    text = "placa,data,km\n" + "\n".join(f"{p},{d},{k}" for p, d, k in rows)
    return StringIO(text)


def test_load_normalizes_plate_case_and_types():
    df = load_readings(_csv([("abc1a23", "2025-01-10", 1000), ("abc1a23", "2025-02-10", 2500)]))
    assert df["placa"].iloc[0] == "ABC1A23"
    assert str(df["data"].dtype).startswith("datetime64")
    assert df["km"].dtype.kind in {"f", "i"}


def test_load_raises_when_columns_missing():
    with pytest.raises(ValueError, match="colunas obrigatorias"):
        load_readings(pd.DataFrame({"placa": ["A"], "km": [10]}))


def test_clean_drops_decreasing_readings():
    df = load_readings(_csv([
        ("ABC1A23", "2025-01-01", 1000),
        ("ABC1A23", "2025-02-01", 1500),
        ("ABC1A23", "2025-03-01", 900),    # km decresceu — erro/troca
        ("ABC1A23", "2025-04-01", 1800),
    ]))
    assert list(df["km"]) == [1000.0, 1500.0, 1800.0]


def test_clean_collapses_same_day_duplicates_keeping_largest():
    df = load_readings(_csv([
        ("ABC1A23", "2025-01-01", 1000),
        ("ABC1A23", "2025-01-01", 1200),   # leitura mais tarde no mesmo dia
        ("ABC1A23", "2025-02-01", 2000),
    ]))
    jan = df[df["data"] == "2025-01-01"]
    assert len(jan) == 1
    assert jan["km"].iloc[0] == 1200


def test_split_temporal_respects_cutoff():
    df = load_readings(_csv([
        ("ABC1A23", "2025-01-01", 100),
        ("ABC1A23", "2025-06-01", 5000),
        ("ABC1A23", "2025-12-01", 12000),
    ]))
    train, test = split_temporal(df, "2025-06-01")
    assert len(train) == 2 and len(test) == 1
    assert train["data"].max() <= pd.Timestamp("2025-06-01")
    assert test["data"].min() > pd.Timestamp("2025-06-01")
