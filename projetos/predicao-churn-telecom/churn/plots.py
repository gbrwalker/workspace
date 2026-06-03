"""Geração das figuras de avaliação (salvas como PNG)."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")  # backend headless — não exige display

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay  # noqa: E402


def save_confusion_matrix(model, X_test, y_test, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(4.5, 4))
    ConfusionMatrixDisplay.from_estimator(
        model,
        X_test,
        y_test,
        display_labels=["Permanece", "Churn"],
        cmap="Blues",
        colorbar=False,
        ax=ax,
    )
    ax.set_title("Matriz de Confusão")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_roc_curve(model, X_test, y_test, path: Path) -> None:
    fig, ax = plt.subplots(figsize=(5, 4))
    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax, name="Random Forest")
    ax.plot([0, 1], [0, 1], "--", color="grey", linewidth=1, label="Aleatório")
    ax.set_title("Curva ROC")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def save_feature_importance(
    names: Sequence[str], importances: Sequence[float], path: Path, top: int = 12
) -> None:
    order = np.argsort(importances)[-top:]
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.barh([names[i] for i in order], [importances[i] for i in order], color="#2a7ab9")
    ax.set_title(f"Top {top} variáveis (importância por permutação)")
    ax.set_xlabel("Queda média no ROC-AUC ao embaralhar a variável")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
