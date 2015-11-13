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

## Show sample of dataset after normalization

```
python show_dataset.py

       Map     Team1  Team1Pts        Team2  Team2Pts Team1Win Team2Win Team1LastWin Team2LastWin
0    cache   x6tence         4     overGame        16     True    False        False        True
1   mirage  overGame         8      x6tence        16    False     True        True         True
2  inferno     Titan        16  HellRaisers         7     True    False        False        False
3  inferno  FlipSid3        12           SK        16    False     True        True         False
4    train        SK        16     FlipSid3        13     True    False        False        False
5   mirage  FlipSid3        16           SK         7    False     True        False        True
```

## Accuray without any features

```
python accuracy_without_features.py
Accuracy: 56.7%
```
