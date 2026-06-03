"""Gráficos de avaliação (PNG, headless)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from .model import MKMPredictor  # noqa: E402


def save_error_histogram(detail: pd.DataFrame, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(detail["erro_km"], bins=40, color="#2a7ab9", edgecolor="white")
    ax.axvline(0, color="#333", linestyle="--", linewidth=1)
    ax.set_title("Distribuicao do erro de previsao (km)")
    ax.set_xlabel("Erro = km_previsto - km_real")
    ax.set_ylabel("Leituras")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_horizon_mae(metrics: dict, path: Path) -> None:
    per = metrics["por_horizonte"]
    labels = list(per.keys())
    values = [per[k]["mae_km"] for k in labels]
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(labels, values, color="#2a7ab9")
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.0f} km", ha="center", va="bottom")
    ax.set_title("Erro medio absoluto por horizonte de previsao")
    ax.set_ylabel("MAE (km)")
    ax.set_xlabel("Distancia entre ultima leitura de treino e leitura prevista")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_vehicle_examples(
    df: pd.DataFrame, model: MKMPredictor, path: Path, n: int = 4, seed: int = 0
) -> None:
    """Plota série real e linha prevista para alguns veículos representativos."""
    rng = np.random.default_rng(seed)
    placas = list(model.profiles_.keys())
    eligiveis = [p for p in placas if (df["placa"] == p).sum() >= 6]
    sample = rng.choice(eligiveis, size=min(n, len(eligiveis)), replace=False)

    fig, axes = plt.subplots(2, 2, figsize=(11, 7), sharex=False)
    for ax, placa in zip(axes.flat, sample):
        g = df[df["placa"] == placa].sort_values("data")
        ax.scatter(g["data"], g["km"], color="#2a7ab9", s=20, label="leituras reais")
        xs = pd.date_range(g["data"].min(), g["data"].max(), periods=50)
        ys = [model.predict(placa, x) for x in xs]
        ax.plot(xs, ys, color="#c0392b", linewidth=1.6, label="modelo")
        ax.set_title(f"{placa}  ({model.profiles_[placa].daily_rate:.0f} km/dia)")
        ax.tick_params(axis="x", rotation=20)
        ax.legend(loc="upper left", fontsize=8)
    fig.suptitle("Modelo ajustado a veiculos da amostra")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
