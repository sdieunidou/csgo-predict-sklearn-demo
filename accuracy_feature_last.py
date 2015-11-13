import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from collections import defaultdict

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1Win"] = dataset["Team1Pts"] > dataset["Team2Pts"]
dataset["Team1LastWin"] = False;
dataset["Team2LastWin"] = False;
dataset["Team1RanksHigher"] = False;
dataset["Team2RanksHigher"] = False;
dataset["Team1WonLast"] = False;

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

   row["Team1LastWin"] = won_last[team1]
   row["Team2LastWin"] = won_last[team2]
   row["Team1RanksHigher"] = team1_rank > team2_rank
   row["Team2RanksHigher"] = team2_rank > team1_rank
   row["Team1WonLast"] = 1 if last_match_winner[teams] == row["Team1"] else 0

   dataset.ix[index] = row

   won_last[team1] = row["Team1Win"]
   won_last[team2] = not row["Team1Win"]

   winner = row["Team1"] if row["Team1Win"] else row["Team2"]
   last_match_winner[teams] = winner

print dataset.ix[:5]

y_true = dataset["Team1Win"].values

clf = DecisionTreeClassifier()
X_lastwinner = dataset[["Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]].values

scores = cross_val_score(clf, X_lastwinner, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
