"""Testes do modelo MKM e de um treino end-to-end (smoke)."""
from datetime import timedelta

import pandas as pd
import pytest

from mkm.data import load_readings, split_temporal
from mkm.evaluate import evaluate
from mkm.model import MKMPredictor
from mkm.synthetic import generate_fleet


def _make_linear_history(placa: str, start: str, rate: float, n: int = 12) -> pd.DataFrame:
    base = pd.Timestamp(start)
    return pd.DataFrame(
        {
            "placa": [placa] * n,
            "data": [base + timedelta(days=30 * i) for i in range(n)],
            "km": [10_000 + rate * 30 * i for i in range(n)],
        }
    )


def test_predictor_recovers_known_daily_rate():
    df = _make_linear_history("ABC1A23", "2024-01-01", rate=120.0)
    model = MKMPredictor().fit(df)
    assert model.daily_rate("ABC1A23") == pytest.approx(120.0, rel=1e-3)


def test_predict_is_linear_in_target_date():
    df = _make_linear_history("ABC1A23", "2024-01-01", rate=100.0)
    model = MKMPredictor().fit(df)
    a = model.predict("ABC1A23", "2025-01-01")
    b = model.predict("ABC1A23", "2025-01-11")
    assert b - a == pytest.approx(1000.0, rel=1e-3)


def test_unknown_plate_raises():
    df = _make_linear_history("ABC1A23", "2024-01-01", rate=80.0)
    model = MKMPredictor().fit(df)
    with pytest.raises(KeyError):
        model.daily_rate("ZZZ9Z99")


def test_days_to_km_zero_when_already_past_target():
    df = _make_linear_history("ABC1A23", "2024-01-01", rate=200.0, n=20)
    model = MKMPredictor().fit(df)
    assert model.days_to_km("ABC1A23", km_alvo=1.0) == 0


def test_falls_back_to_fleet_median_for_single_reading_vehicle():
    rich = _make_linear_history("ABC1A23", "2024-01-01", rate=100.0)
    poor = pd.DataFrame(
        {"placa": ["XYZ9Z99"], "data": [pd.Timestamp("2025-06-01")], "km": [80_000.0]}
    )
    model = MKMPredictor().fit(pd.concat([rich, poor], ignore_index=True))
    assert model.profiles_["XYZ9Z99"].strategy == "fleet_median"
    assert model.daily_rate("XYZ9Z99") == pytest.approx(model.fleet_daily_rate_)


def test_end_to_end_evaluation_is_reasonable_on_synthetic_data():
    raw = generate_fleet(n_vehicles=20, seed=0)
    df = load_readings(raw)
    cutoff = df["data"].quantile(0.7)
    train, test = split_temporal(df, cutoff)
    model = MKMPredictor().fit(train)
    metrics = evaluate(model, train, test)
    assert metrics["mape_pct"] < 8.0    # erro percentual baixo na frota sintetica
    assert metrics["n_amostras"] > 0
