from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from sklearn.impute import SimpleImputer

from telco_churn.config import feature_columns, load_metadata
from telco_churn.preprocessing import FeatureColumnSelector, make_column_preprocessor


def test_feature_column_selector_is_stateless_order():
    cols = ["a", "b"]
    df = pd.DataFrame({"b": [2, 3], "a": [1, 4], "z": [9, 9]})
    tr = FeatureColumnSelector(columns=cols)
    tr.fit(df, None)
    out1 = tr.transform(df)
    tr.fit(pd.DataFrame({"a": [0], "b": [0]}), None)
    out2 = tr.transform(df)
    pd.testing.assert_frame_equal(out1.reset_index(drop=True), out2.reset_index(drop=True))
    assert list(out1.columns) == cols


def test_feature_column_selector_missing_column_raises():
    tr = FeatureColumnSelector(columns=["a", "b"])
    df = pd.DataFrame({"a": [1]})
    tr.fit(df)
    with pytest.raises(ValueError, match="Missing"):
        tr.transform(df)


def test_simple_imputer_learns_state_from_training_data():
    train = pd.DataFrame({"x": [1.0, np.nan, 3.0]})
    test = pd.DataFrame({"x": [np.nan]})
    imp = SimpleImputer(strategy="mean")
    imp.fit(train)
    assert imp.statistics_[0] == pytest.approx(2.0)
    out = imp.transform(test)
    assert out[0, 0] == pytest.approx(2.0)


def test_column_preprocessor_fit_transform(train_csv_exists):
    meta = load_metadata()
    numeric = list(meta["numeric_features"])
    categorical = list(meta["categorical_features"])
    df = pd.read_csv(train_csv_exists).head(50)
    X = df[feature_columns()]
    pre = make_column_preprocessor(numeric, categorical, scale_numeric=True)
    Xt = pre.fit_transform(X)
    assert Xt.shape[0] == 50
    assert Xt.shape[1] > 0
