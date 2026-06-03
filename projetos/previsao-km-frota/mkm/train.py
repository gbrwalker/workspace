"""Orquestrador: gera dados sintéticos, treina, avalia e exporta artefatos.

Uso:
    python -m mkm.train
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib

from . import plots
from .data import load_readings, split_temporal
from .evaluate import evaluate
from .model import MKMPredictor
from .synthetic import generate_fleet

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"


def main(seed: int = 42) -> dict:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    raw = generate_fleet(n_vehicles=50, seed=seed)
    raw_path = DATA / "frota_sintetica.csv"
    raw.to_csv(raw_path, index=False)

    df = load_readings(raw_path)

    cutoff = df["data"].quantile(0.7)
    train, test = split_temporal(df, cutoff)

    model = MKMPredictor().fit(train)
    metrics = evaluate(model, train, test)

    plots.save_error_histogram(metrics["detalhe"], FIGURES / "histograma_erros.png")
    plots.save_horizon_mae(metrics, FIGURES / "mae_por_horizonte.png")
    plots.save_vehicle_examples(df, model, FIGURES / "exemplos_veiculos.png")

    summary = {
        "veiculos": int(df["placa"].nunique()),
        "leituras": int(len(df)),
        "data_corte_treino": str(cutoff.date()),
        "leituras_treino": int(len(train)),
        "leituras_teste": int(len(test)),
        "metricas": {k: v for k, v in metrics.items() if k != "detalhe"},
    }
    (REPORTS / "metrics.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    joblib.dump(model, REPORTS / "mkm_model.joblib")

    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    return summary


if __name__ == "__main__":
    main()
