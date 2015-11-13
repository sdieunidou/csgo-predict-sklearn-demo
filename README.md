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

       Map     Team1  Team1Pts        Team2  Team2Pts Team1Win Team2Win
0    cache   x6tence         4     overGame        16     True    False
1   mirage  overGame         8      x6tence        16    False     True
2  inferno     Titan        16  HellRaisers         7     True    False
3  inferno  FlipSid3        12           SK        16    False     True
4    train        SK        16     FlipSid3        13     True    False
5   mirage  FlipSid3        16           SK         7    False     True
```
