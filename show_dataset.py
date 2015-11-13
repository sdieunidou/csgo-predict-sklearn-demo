import pandas as pd
from collections import defaultdict

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Visitor Team", "VisitorPts", "Home Team", "HomePts"]
dataset["HomeWin"] = dataset["VisitorPts"] < dataset["HomePts"]
dataset["VisitorWin"] = dataset["VisitorPts"] > dataset["HomePts"]

won_last = defaultdict(int)
for index, row in dataset.iterrows():
  home_team = row["Home Team"]
  visitor_team = row["Visitor Team"]

  row["HomeLastWin"] = won_last[home_team]
  row["VisitorLastWin"] = won_last[visitor_team]
  won_last[home_team] = row["HomeWin"]
  won_last[visitor_team] = row["VisitorWin"]

  dataset.ix[index] = row

y_true = [0, 1, 2]

print dataset.ix[:5]
