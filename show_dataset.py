import pandas as pd
from collections import defaultdict

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1Win"] = dataset["Team1"] > dataset["Team2"]
dataset["Team2Win"] = dataset["Team1"] < dataset["Team2"]

won_last = defaultdict(int)
for index, row in dataset.iterrows():
  home_team = row["Team1"]
  visitor_team = row["Team2"]

  row["Team1LastWin"] = won_last[home_team]
  row["Team2LastWin"] = won_last[visitor_team]
  won_last[home_team] = row["Team1Win"]
  won_last[visitor_team] = row["Team2Win"]

  dataset.ix[index] = row

y_true = [0, 1, 2]

print dataset.ix[:5]
