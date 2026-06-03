"""Pipeline de pré-processamento + modelo.

Todo o pré-processamento vive dentro de um ``Pipeline`` do scikit-learn, o que
evita vazamento de dados (o ``fit`` acontece só no treino) e deixa o objeto
final pronto para serialização e uso em produção.
"""
from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from .data import CATEGORICAL_FEATURES, NUMERIC_FEATURES


def build_preprocessor() -> ColumnTransformer:
    """Imputação + escala para numéricas e imputação + one-hot para categóricas."""
    numeric = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        [
            ("num", numeric, NUMERIC_FEATURES),
            ("cat", categorical, CATEGORICAL_FEATURES),
        ]
    )


def build_pipeline(random_state: int = 42) -> Pipeline:
    """Pipeline completo: pré-processamento + Random Forest balanceado.

    ``class_weight="balanced"`` compensa o desbalanceamento entre clientes que
    permanecem e os que evadem, alinhando o treino ao objetivo de detectar churn.
    """
    return Pipeline(
        [
            ("preprocess", build_preprocessor()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    min_samples_leaf=2,
                    class_weight="balanced",
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )
