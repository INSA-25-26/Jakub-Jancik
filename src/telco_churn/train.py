"""CLI: fit pipeline on processed train split and save with joblib."""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from telco_churn.config import (
    default_model_path,
    target_column,
    train_csv_path,
)
from telco_churn.pipeline import build_training_pipeline


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train Telco churn pipeline and save to disk.")
    parser.add_argument(
        "--train-csv",
        type=Path,
        default=None,
        help=f"Default: {train_csv_path()}",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help=f"Default: {default_model_path()}",
    )
    parser.add_argument(
        "--model",
        choices=("mlp", "logistic_regression"),
        default="mlp",
        help="Default mlp matches notebook best test AP model.",
    )
    parser.add_argument(
        "--select-k",
        type=str,
        default=None,
        help="SelectKBest k (integer or 'all'). Defaults: mlp→35, logistic_regression→all.",
    )
    args = parser.parse_args(argv)

    train_path = args.train_csv or train_csv_path()
    out_path = args.output or default_model_path()

    if not train_path.is_file():
        raise SystemExit(f"Train CSV not found: {train_path}")

    sk: int | str
    if args.select_k is None:
        sk = "all" if args.model == "logistic_regression" else 35
    elif args.select_k == "all":
        sk = "all"
    else:
        sk = int(args.select_k)

    df = pd.read_csv(train_path)
    y = df[target_column()].astype(int)
    X = df.drop(columns=[target_column()])

    pipeline = build_training_pipeline(args.model, select_k=sk)
    pipeline.fit(X, y)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, out_path)
    print(f"Saved pipeline to {out_path}")


if __name__ == "__main__":
    main()
