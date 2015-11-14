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

## Features implemented

* Team has win this lasted match played
* Team1 has win this lasted match against Team2
* Team1 is ranked better than Team2 (use HLTV ranking)

## Generate transformed CSV

```
python create_model.py
```

## Predict submissions

Predictor use submissions contain in `data/submission.csv` file.

```
python predict.py
```
