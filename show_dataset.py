import pandas as pd

dataset = pd.read_csv('data/raw/dataset.csv');
print dataset.ix[:5]
