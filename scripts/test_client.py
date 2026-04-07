from __future__ import annotations

import argparse
import json

import requests


SAMPLE_PAYLOAD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "Yes",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 85.5,
    "TotalCharges": 1020.0,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple API test client for churn service.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="Base URL of API service.")
    args = parser.parse_args()

    predict_url = f"{args.base_url.rstrip('/')}/predict"
    health_url = f"{args.base_url.rstrip('/')}/health"

    health_resp = requests.get(health_url, timeout=10)
    health_resp.raise_for_status()
    print("Health:", health_resp.json())

    response = requests.post(predict_url, json=SAMPLE_PAYLOAD, timeout=10)
    response.raise_for_status()
    print("Predict response:")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    main()
