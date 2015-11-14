# Data

## Crawler

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

## Generate transformed CSV

```
python create_model.py
```


## Predict submissions

Predictor use submissions contain in `data/submission.csv` file.

```
python predict.py
```
