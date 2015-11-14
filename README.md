# Data

## Crawler

The crawler retrieve data of past 3 months from hltv.org.

```
cd crawler/
composer install -o
php crawler.php
```

## Generate dataset

```
cd data/
php generate_csv.php
```

# Predictor

RandomForestClassifier is used to make predictions.

## Generate transformed CSV

```
python create_model.py
```

## Predict submissions

Predictor use submissions contain in `data/submission.csv` file.

```
python predict.py
```
