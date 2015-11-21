# CS:GO Match Predictor

RandomForestClassifier is used to make predictions.
This projet was just a demo of RandomForestClassifier usage with sklearn.

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

# Data

## Generate dataset

```
php generate_csv.php
```
