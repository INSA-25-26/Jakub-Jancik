from __future__ import annotations

import joblib
import numpy as np
import pandas as pd
import pytest

from telco_churn.config import target_column, train_csv_path
from telco_churn.pipeline import build_training_pipeline


@pytest.fixture
def fitted_logistic_pipeline(train_csv_exists):
    df = pd.read_csv(train_csv_path()).head(200)
    y = df[target_column()].astype(int)
    X = df.drop(columns=[target_column()])
    pipe = build_training_pipeline("logistic_regression")
    pipe.fit(X, y)
    return pipe, X


def test_pipeline_has_expected_steps():
    pipe = build_training_pipeline("logistic_regression")
    assert [name for name, _ in pipe.steps] == [
        "select_columns",
        "preprocess",
        "select",
        "model",
    ]


def test_pipeline_predict_proba_shape(fitted_logistic_pipeline):
    pipe, X = fitted_logistic_pipeline
    proba = pipe.predict_proba(X.iloc[:10])
    assert proba.shape == (10, 2)
    assert np.allclose(proba.sum(axis=1), 1.0)


def test_pipeline_inference_is_deterministic(fitted_logistic_pipeline):
    pipe, X = fitted_logistic_pipeline
    a = pipe.predict_proba(X.iloc[:7])
    b = pipe.predict_proba(X.iloc[:7])
    np.testing.assert_array_equal(a, b)


def test_pipeline_joblib_roundtrip_matches_proba(tmp_path, fitted_logistic_pipeline):
    """Differential guard: serialize/deserialize must not change predictions."""
    pipe, X = fitted_logistic_pipeline
    path = tmp_path / "pipe.joblib"
    joblib.dump(pipe, path)
    loaded = joblib.load(path)
    before = pipe.predict_proba(X.iloc[:20])
    after = loaded.predict_proba(X.iloc[:20])
    np.testing.assert_allclose(before, after, rtol=0.0, atol=0.0)
