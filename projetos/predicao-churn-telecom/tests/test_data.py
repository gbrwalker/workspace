"""Testes da camada de dados."""
from churn.data import TARGET, clean, load_dataset, load_raw


def test_load_raw_has_target_and_enough_rows():
    df = load_raw()
    assert TARGET in df.columns
    assert len(df) > 1000


def test_clean_binarizes_target():
    df = clean(load_raw())
    assert set(df[TARGET].unique()) <= {0, 1}


def test_clean_coerces_total_pago_to_float():
    df = clean(load_raw())
    assert str(df["Total_Pago"].dtype).startswith("float")


def test_clean_drops_id_column():
    df = clean(load_raw())
    assert "customerID" not in df.columns


def test_clean_normalizes_genero():
    df = clean(load_raw())
    assert set(df["Genero"].dropna().unique()) <= {"Male", "Female"}


def test_clean_normalizes_internet_service():
    df = clean(load_raw())
    assert "dsl" not in set(df["Servico_Internet"].dropna().unique())


def test_load_dataset_separates_features_and_target():
    X, y = load_dataset()
    assert len(X) == len(y)
    assert TARGET not in X.columns
