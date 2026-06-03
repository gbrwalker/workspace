"""Avaliação temporal honesta: treina com passado, mede no futuro.

Para cada leitura de teste, perguntamos ao modelo "qual o km esperado nessa
data?" e comparamos com a leitura real. Reportamos:

- **MAE** absoluto (km de erro).
- **MAPE** relativo (% sobre o km real).
- Erros por **horizonte de previsão** (faixas de dias entre a última leitura
  de treino e a leitura de teste) — porque previsão de 30 dias e de 6 meses
  têm cobrança bem diferente.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .model import MKMPredictor


def _last_train_date_per_vehicle(train: pd.DataFrame) -> dict[str, pd.Timestamp]:
    return train.groupby("placa")["data"].max().to_dict()


def evaluate(model: MKMPredictor, train: pd.DataFrame, test: pd.DataFrame) -> dict:
    """Calcula métricas de erro do modelo em uma base de teste."""
    if test.empty:
        raise ValueError("base de teste vazia")

    last_seen = _last_train_date_per_vehicle(train)

    rows = []
    for _, r in test.iterrows():
        placa = r["placa"]
        if placa not in model.profiles_:
            continue
        prediction = model.predict(placa, r["data"])
        actual = float(r["km"])
        rows.append(
            {
                "placa": placa,
                "data": r["data"],
                "horizonte_dias": (r["data"] - last_seen.get(placa, r["data"])).days,
                "km_real": actual,
                "km_previsto": prediction,
                "erro_km": prediction - actual,
                "erro_pct": (prediction - actual) / actual if actual > 0 else np.nan,
            }
        )

    if not rows:
        raise ValueError("nenhuma placa do teste foi vista no treino")

    df = pd.DataFrame(rows)
    abs_err = df["erro_km"].abs()
    abs_pct = df["erro_pct"].abs().dropna()

    bins = [-1, 30, 90, 180, np.inf]
    labels = ["<=30d", "31-90d", "91-180d", ">180d"]
    df["bucket"] = pd.cut(df["horizonte_dias"], bins=bins, labels=labels)
    per_horizon = (
        df.groupby("bucket", observed=True)
        .apply(
            lambda g: pd.Series(
                {
                    "n": len(g),
                    "mae_km": float(g["erro_km"].abs().mean()),
                    "mape_pct": float((g["erro_pct"].abs() * 100).mean()),
                }
            ),
            include_groups=False,
        )
        .to_dict(orient="index")
    )

    return {
        "n_amostras": int(len(df)),
        "mae_km": round(float(abs_err.mean()), 1),
        "mape_pct": round(float(abs_pct.mean() * 100), 2),
        "mediana_erro_km": round(float(abs_err.median()), 1),
        "p90_erro_km": round(float(abs_err.quantile(0.9)), 1),
        "por_horizonte": {
            k: {kk: round(vv, 2) if isinstance(vv, float) else int(vv) for kk, vv in v.items()}
            for k, v in per_horizon.items()
        },
        "detalhe": df,
    }
