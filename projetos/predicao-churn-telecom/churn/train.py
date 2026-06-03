"""Treina, avalia e exporta o modelo de churn.

Executa o fluxo completo e grava os artefatos em ``reports/``:
modelo serializado, métricas em JSON e figuras de avaliação.

Uso:
    python -m churn.train
"""
from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.inspection import permutation_importance
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split

from . import plots
from .data import load_dataset
from .pipeline import build_pipeline

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
FIGURES = REPORTS / "figures"


def _clean_feature_names(pipeline) -> list[str]:
    """Remove os prefixos (``num__``/``cat__``) dos nomes gerados pelo ColumnTransformer."""
    raw = pipeline.named_steps["preprocess"].get_feature_names_out()
    return [name.split("__", 1)[-1] for name in raw]


def main(random_state: int = 42) -> dict:
    FIGURES.mkdir(parents=True, exist_ok=True)

    X, y = load_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state
    )

    pipeline = build_pipeline(random_state)
    pipeline.fit(X_train, y_train)

    proba = pipeline.predict_proba(X_test)[:, 1]
    preds = pipeline.predict(X_test)
    report = classification_report(
        y_test, preds, output_dict=True, target_names=["Permanece", "Churn"]
    )
    auc = roc_auc_score(y_test, proba)

    # Figuras de avaliação
    plots.save_confusion_matrix(pipeline, X_test, y_test, FIGURES / "matriz_confusao.png")
    plots.save_roc_curve(pipeline, X_test, y_test, FIGURES / "curva_roc.png")
    perm = permutation_importance(
        pipeline, X_test, y_test, scoring="roc_auc", n_repeats=10,
        random_state=random_state, n_jobs=-1,
    )
    plots.save_feature_importance(
        _clean_feature_names(pipeline), perm.importances_mean,
        FIGURES / "importancia_variaveis.png",
    )

    metrics = {
        "n_total": int(len(y)),
        "churn_rate": round(float(y.mean()), 4),
        "test_size": int(len(y_test)),
        "roc_auc": round(float(auc), 4),
        "accuracy": round(float(report["accuracy"]), 4),
        "recall_churn": round(float(report["Churn"]["recall"]), 4),
        "precision_churn": round(float(report["Churn"]["precision"]), 4),
        "f1_churn": round(float(report["Churn"]["f1-score"]), 4),
    }

    REPORTS.mkdir(parents=True, exist_ok=True)
    (REPORTS / "metrics.json").write_text(
        json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    joblib.dump(pipeline, REPORTS / "modelo_churn.joblib")

    print(json.dumps(metrics, indent=2, ensure_ascii=False))
    return metrics


if __name__ == "__main__":
    main()
