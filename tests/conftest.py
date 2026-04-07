from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import pytest

from telco_churn.config import target_column, train_csv_path
from telco_churn.pipeline import build_training_pipeline


@pytest.fixture
def train_csv_exists() -> Path:
    p = train_csv_path()
    if not p.is_file():
        pytest.skip(f"Missing processed train split: {p}")
    return p


@pytest.fixture
def small_fitted_pipeline_path(tmp_path: Path, train_csv_exists: Path) -> Path:
    df = pd.read_csv(train_csv_exists).head(150)
    y = df[target_column()].astype(int)
    X = df.drop(columns=[target_column()])
    pipe = build_training_pipeline("logistic_regression")
    pipe.fit(X, y)
    out = tmp_path / "pipeline.joblib"
    joblib.dump(pipe, out)
    return out


@pytest.fixture
def sample_request_row(train_csv_exists: Path) -> dict:
    rec = pd.read_csv(train_csv_exists).iloc[0].drop(labels=[target_column()])
    return json.loads(rec.to_json())

