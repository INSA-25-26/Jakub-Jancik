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
- `models/best_model.joblib` - najlepsi model podla test AP

## Spustenie

1. Nainstaluj zavislosti:

```bash
python -m pip install -r requirements.txt
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

## Zdroj dat

- Telco Customer Churn (CSV): `data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv`
