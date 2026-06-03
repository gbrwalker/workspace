"""Testes do pipeline e de um treino end-to-end (smoke test)."""
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from churn.data import load_dataset
from churn.pipeline import build_pipeline


def test_build_pipeline_returns_pipeline():
    assert isinstance(build_pipeline(), Pipeline)


def test_pipeline_predicts_valid_probabilities():
    X, y = load_dataset()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=0
    )
    pipe = build_pipeline(random_state=0).fit(X_tr, y_tr)
    proba = pipe.predict_proba(X_te)[:, 1]
    assert proba.min() >= 0.0
    assert proba.max() <= 1.0


def test_pipeline_beats_random_baseline():
    X, y = load_dataset()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=0
    )
    pipe = build_pipeline(random_state=0).fit(X_tr, y_tr)
    auc = roc_auc_score(y_te, pipe.predict_proba(X_te)[:, 1])
    assert auc > 0.7  # claramente acima do acaso (0.5)
