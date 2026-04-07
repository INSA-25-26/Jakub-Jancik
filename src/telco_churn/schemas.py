"""Pydantic request/response models for the prediction API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ChurnPredictionRequest(BaseModel):
    """One customer row (same features as `data/processed/train.csv` without `Churn`)."""

    gender: str = Field(examples=["Female"])
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0)
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


class ChurnPredictionResponse(BaseModel):
    churn_probability: float = Field(ge=0.0, le=1.0)
    churn: bool
    label: str = Field(description='Human-readable churn: "Yes" or "No"')
