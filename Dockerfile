FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY models/churn_pipeline.joblib ./models/churn_pipeline.joblib

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

ENV TELCO_MODEL_PATH=/app/models/churn_pipeline.joblib
EXPOSE 8000

CMD ["uvicorn", "telco_churn.api:app", "--host", "0.0.0.0", "--port", "8000"]
