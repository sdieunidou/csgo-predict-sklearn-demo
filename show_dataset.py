import pandas as pd

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Visitor Team", "VisitorPts", "Home Team", "HomePts"]

print dataset.ix[:5]
