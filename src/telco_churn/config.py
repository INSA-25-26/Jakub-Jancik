"""Project paths and metadata loaded from `data/processed/metadata.json`."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


def project_root() -> Path:
    """Repository root (parent of `src/`)."""
    return Path(__file__).resolve().parents[2]


def processed_dir() -> Path:
    return project_root() / "data" / "processed"


def raw_csv_path() -> Path:
    return project_root() / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"


def train_csv_path() -> Path:
    return processed_dir() / "train.csv"


def metadata_path() -> Path:
    return processed_dir() / "metadata.json"


def default_model_path() -> Path:
    return project_root() / "models" / "churn_pipeline.joblib"


@lru_cache
def load_metadata() -> dict[str, Any]:
    path = metadata_path()
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {path}. Run notebook 01 (or preprocessing) to generate processed data."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def feature_columns() -> list[str]:
    meta = load_metadata()
    return list(meta["numeric_features"]) + list(meta["categorical_features"])


def target_column() -> str:
    return str(load_metadata()["target_column"])


def random_state() -> int:
    return int(load_metadata().get("random_state", 42))
