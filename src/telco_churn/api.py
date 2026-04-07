"""FastAPI service: load fitted pipeline and expose POST /predict."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from telco_churn.config import default_model_path
from telco_churn.prediction_ui import PREDICTION_PAGE_HTML
from telco_churn.schemas import ChurnPredictionRequest, ChurnPredictionResponse


def model_path_from_env() -> Path:
    raw = os.environ.get("TELCO_MODEL_PATH")
    return Path(raw) if raw else default_model_path()


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = model_path_from_env()
    if not path.is_file():
        raise RuntimeError(
            f"Pipeline file not found: {path}. Train first: telco-train or python -m telco_churn.train"
        )
    app.state.pipeline = joblib.load(path)
    yield


app = FastAPI(
    title="Telco Customer Churn",
    description="Binary churn prediction using the trained sklearn pipeline.",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def prediction_ui_page() -> str:
    """Browser UI: form submits to POST /predict via fetch."""
    return PREDICTION_PAGE_HTML


@app.get("/health")
def health(request: Request) -> dict:
    p = getattr(request.app.state, "pipeline", None)
    return {"status": "ok", "model_loaded": p is not None}


@app.post("/predict", response_model=ChurnPredictionResponse)
def predict(request: Request, body: ChurnPredictionRequest) -> ChurnPredictionResponse:
    pipeline = request.app.state.pipeline
    row = pd.DataFrame([body.model_dump()])
    try:
        proba = pipeline.predict_proba(row)[:, 1]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    p = float(proba[0])
    churn = p >= 0.5
    return ChurnPredictionResponse(
        churn_probability=p,
        churn=churn,
        label="Yes" if churn else "No",
    )
