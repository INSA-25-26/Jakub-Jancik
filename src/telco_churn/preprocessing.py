"""Custom processors and sklearn preprocessing used in the training pipeline."""

from __future__ import annotations

from typing import Any

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeatureColumnSelector(TransformerMixin, BaseEstimator):
    """
    Stateless: keeps only the configured columns in a fixed order.
    No statistics are estimated from training data in `fit`.
    """

    def __init__(self, columns: list[str] | None = None):
        self.columns = columns

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        cols = self.columns
        if cols is None:
            raise ValueError("columns must be set")
        df = X if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        missing = set(cols) - set(df.columns)
        if missing:
            raise ValueError(f"Missing feature columns: {sorted(missing)}")
        return df[cols].copy()


def make_column_preprocessor(
    numeric_features: list[str],
    categorical_features: list[str],
    *,
    scale_numeric: bool = True,
) -> ColumnTransformer:
    num_steps: list[tuple[str, Any]] = [("imputer", SimpleImputer(strategy="median"))]
    if scale_numeric:
        num_steps.append(("scaler", StandardScaler()))

    return ColumnTransformer(
        transformers=[
            ("num", Pipeline(steps=num_steps), numeric_features),
            (
                "cat",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="most_frequent")),
                        (
                            "onehot",
                            OneHotEncoder(handle_unknown="ignore", sparse_output=False),
                        ),
                    ]
                ),
                categorical_features,
            ),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
