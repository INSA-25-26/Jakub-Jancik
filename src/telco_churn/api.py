"""FastAPI service: load fitted pipeline and expose POST /predict."""

from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

from telco_churn.config import default_model_path
from telco_churn.prediction_ui import PREDICTION_PAGE_HTML
from telco_churn.schemas import ChurnPredictionRequest, ChurnPredictionResponse

logger = logging.getLogger("telco_churn.api")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

PREDICT_REQUESTS_TOTAL = Counter(
    "telco_predict_requests_total",
    "Number of prediction requests.",
)
PREDICT_FAILURES_TOTAL = Counter(
    "telco_predict_failures_total",
    "Number of failed prediction requests.",
)
PREDICT_LATENCY_SECONDS = Histogram(
    "telco_predict_latency_seconds",
    "Latency of prediction endpoint in seconds.",
)


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


@app.get("/metrics", include_in_schema=False)
def metrics() -> Response:
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=ChurnPredictionResponse)
def predict(request: Request, body: ChurnPredictionRequest) -> ChurnPredictionResponse:
    pipeline = request.app.state.pipeline
    row = pd.DataFrame([body.model_dump()])
    started = time.perf_counter()
    PREDICT_REQUESTS_TOTAL.inc()
    try:
        proba = pipeline.predict_proba(row)[:, 1]
    except Exception as e:
        PREDICT_FAILURES_TOTAL.inc()
        logger.exception("Prediction failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    finally:
        PREDICT_LATENCY_SECONDS.observe(time.perf_counter() - started)
    p = float(proba[0])
    churn = p >= 0.5
    logger.info("Prediction successful, churn_probability=%.6f, churn=%s", p, churn)
    return ChurnPredictionResponse(
        churn_probability=p,
        churn=churn,
        label="Yes" if churn else "No",
    )
