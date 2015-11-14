import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict
import csv

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1LastWin"] = 0
dataset["Team2LastWin"] = 0
dataset["Team1RanksHigher"] = 0
dataset["Team2RanksHigher"] = 0
dataset["Team1WonLast"] = 0
dataset["Result"] = 0

ranking = {
   'EnVyUs': 1,
   'Virtus.pro': 2,
   'TSM': 3,
   'fnatic': 4,
   'Natus Vincere': 5,
   'NiP': 6,
   'G2': 7,
   'mousesports': 8,
   'Luminosity': 9,
   'Titan': 10,
   'Cloud9': 11,
   'dignitas': 12,
   'CLG': 13,
   'Liquid': 14,
   'FlipSid3': 15,
   'E-frag.net': 16,
   'Conquest': 17,
   'Renegades': 18,
   'Vexed': 19,
   'CSGL': 20,
}

won_last = defaultdict(int)
last_match_winner = defaultdict(int)

for index, row in dataset.iterrows():
   team1 = row["Team1"]
   team2 = row["Team2"]

   team1_rank = False;
   team2_rank = False;

   if ranking.has_key(team1):
      team1_rank = ranking[team1]

   if ranking.has_key(team2):
      team2_rank = ranking[team2]

   teams = tuple(sorted([team1, team2]))

   result = 0
   if row["Team1Pts"] > row["Team2Pts"]:
      result = 1
   elif row["Team2Pts"] > row["Team1Pts"]:
      result = 2

   row["Team1LastWin"] = int(won_last[team1])
   row["Team2LastWin"] = int(won_last[team2])
   row["Team1RanksHigher"] = int(team1_rank < team2_rank)
   row["Team2RanksHigher"] = int(team2_rank < team1_rank)
   row["Result"] = result
   row["Team1WonLast"] = 1 if last_match_winner[teams] == row["Team1"] else 0

   dataset.ix[index] = row

   won_last[team1] = row["Result"] == 1
   won_last[team2] = row["Result"] == 2

   winner = row["Team1"] if row["Result"] == 1 else row["Team2"]
   last_match_winner[teams] = winner

X_teams_expanded = dataset[["Result", "Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]].values
dataset.to_csv("data/samples.csv")
