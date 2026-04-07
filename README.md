# INSA zadanie - Telco Customer Churn

Projekt pokryva celu cast zadania:

- data s ciselnycmi aj kategorickymi atributmi
- osetrenie chybajucich hodnot
- vyber relevantnych atributov
- viacero modelov: logisticka regresia, kNN, neuronna siet (MLP), rozhodovaci strom
- optimalizacia nastaveni pomocou krizovej validacie
- finalne testovanie na testovacej mnozine s metrikami:
  - accuracy
  - precision
  - recall
  - F1
  - precision-recall krivka + average precision

## Struktura

- `data/raw/` - povodny dataset
- `data/processed/` - vycistene data, split, metadata, feature scores
- `notebooks/01_preprocessing_and_feature_selection.ipynb`
- `notebooks/02_modeling_and_evaluation.ipynb`
- `reports/` - csv prehlady metrik a PR krivka
- `models/best_model.joblib` - export z notebooku 02 (najlepsi podla test AP)
- `pyproject.toml` - balik `telco-churn` (cast II + III)
- `src/telco_churn/` - pipeline, skript trenovania, FastAPI
- `tests/` - jednotkove, diferenčne (joblib roundtrip) a integracne testy API

## Spustenie

1. Nainstaluj zavislosti:

Pre notebooky staci:

```bash
python -m pip install -r requirements.txt
```

Pre produkcny kod (cast II/III), odporucane ako editovatelna instalacia s testami:

```bash
python -m pip install -e ".[dev]"
```

2. Notebooky sa da spustat v poradi:

- `notebooks/01_preprocessing_and_feature_selection.ipynb`
- `notebooks/02_modeling_and_evaluation.ipynb`

3. Alebo ich vykonaj z CLI:

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/01_preprocessing_and_feature_selection.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/02_modeling_and_evaluation.ipynb
```

Poznamka pre obmedzene Windows prostredia:

```powershell
$env:JUPYTER_ALLOW_INSECURE_WRITES = "true"
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/01_preprocessing_and_feature_selection.ipynb
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/02_modeling_and_evaluation.ipynb
```

## Cast II — trenovanie pipeline a ulozenie modelu

Vyzaduje vygenerovane `data/processed/train.csv` a `metadata.json` (notebook 01).

```bash
python -m telco_churn.train --output models/churn_pipeline.joblib
```

Predvoleny model je **MLP** s parametrami z najlepsieho modelu podla test AP v notebooku 02. Logisticka regresia:

```bash
python -m telco_churn.train --model logistic_regression -o models/lr_pipeline.joblib
```

Alternativa cez entry point (po instalacii balika): `telco-train`.

## Cast II — testy

```bash
python -m pytest
```

## Cast III — webova sluzba (FastAPI)

Najprv natrenuj pipeline (subor `models/churn_pipeline.joblib`), alebo nastav cestu:

```powershell
$env:TELCO_MODEL_PATH = "C:\cesta\k\churn_pipeline.joblib"
```

Spustenie servera:

```bash
python -m uvicorn telco_churn.api:app --reload --host 127.0.0.1 --port 8000
```

- Webové rozhranie predikcie (formulár v prehliadači): http://127.0.0.1:8000/
- Interaktívne API (Swagger): http://127.0.0.1:8000/docs — „Try it out“ na `POST /predict`
- Alternatívna dokumentácia: http://127.0.0.1:8000/redoc
- Zdravie: `GET /health`
- Predikcia: `POST /predict` (JSON podla `ChurnPredictionRequest` v `src/telco_churn/schemas.py`). Samotné `GET /predict` v prehliadači vráti 405 (povolená je len metóda POST).

## Zdroj dat

- Telco Customer Churn (CSV): `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`
