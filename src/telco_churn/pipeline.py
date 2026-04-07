"""Full sklearn `Pipeline` factory (matches notebook 02 — best test AP: MLP)."""

from __future__ import annotations

from typing import Literal

from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline

from telco_churn.config import load_metadata, random_state
from telco_churn.preprocessing import FeatureColumnSelector, make_column_preprocessor

ModelName = Literal["mlp", "logistic_regression"]


def build_training_pipeline(
    model: ModelName = "mlp",
    *,
    select_k: int | str = 35,
    scale_numeric: bool | None = None,
) -> Pipeline:
    """
    Build an unfitted pipeline.

    Default hyperparameters reproduce the notebook's best **test** average precision
    model (`mlp` with tuned params from `reports/tuning_summary.csv`).
    """
    meta = load_metadata()
    numeric = list(meta["numeric_features"])
    categorical = list(meta["categorical_features"])
    feature_cols = numeric + categorical
    rs = random_state()

    if scale_numeric is None:
        scale_numeric = True

    preprocess = make_column_preprocessor(
        numeric, categorical, scale_numeric=bool(scale_numeric)
    )

    if model == "mlp":
        clf = MLPClassifier(
            random_state=rs,
            max_iter=400,
            early_stopping=True,
            n_iter_no_change=15,
            hidden_layer_sizes=(32,),
            alpha=1e-4,
            learning_rate_init=1e-3,
            batch_size=64,
        )
    elif model == "logistic_regression":
        clf = LogisticRegression(max_iter=2000, random_state=rs, C=1.0)
    else:
        raise ValueError(f"Unknown model: {model}")

    return Pipeline(
        steps=[
            ("select_columns", FeatureColumnSelector(columns=feature_cols)),
            ("preprocess", preprocess),
            ("select", SelectKBest(score_func=mutual_info_classif, k=select_k)),
            ("model", clf),
        ]
    )
