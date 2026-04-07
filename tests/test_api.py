from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from telco_churn.api import app


def test_root_serves_prediction_form(monkeypatch, small_fitted_pipeline_path):
    monkeypatch.setenv("TELCO_MODEL_PATH", str(small_fitted_pipeline_path))
    with TestClient(app) as client:
        r = client.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "")
    assert 'id="churn-form"' in r.text
    assert "/predict" in r.text


def test_health(monkeypatch, small_fitted_pipeline_path):
    monkeypatch.setenv("TELCO_MODEL_PATH", str(small_fitted_pipeline_path))
    with TestClient(app) as client:
        r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data.get("model_loaded") is True


def test_predict_returns_valid_response(monkeypatch, small_fitted_pipeline_path, sample_request_row):
    monkeypatch.setenv("TELCO_MODEL_PATH", str(small_fitted_pipeline_path))
    with TestClient(app) as client:
        r = client.post("/predict", json=sample_request_row)
    assert r.status_code == 200
    body = r.json()
    assert "churn_probability" in body
    assert "churn" in body
    assert body["label"] in ("Yes", "No")
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert body["churn"] == (body["churn_probability"] >= 0.5)


def test_predict_validation_error_on_missing_field(monkeypatch, small_fitted_pipeline_path, sample_request_row):
    monkeypatch.setenv("TELCO_MODEL_PATH", str(small_fitted_pipeline_path))
    bad = {k: v for k, v in sample_request_row.items() if k != "tenure"}
    with TestClient(app) as client:
        r = client.post("/predict", json=bad)
    assert r.status_code == 422
