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
for index, row in dataset.iterrows():
   home_team = row["Team1"]
   visitor_team = row["Team2"]

   team1_rank = False;
   team2_rank = False;

   if ranking.has_key(home_team):
      team1_rank = ranking.has_key(home_team)

   if ranking.has_key(visitor_team):
      team2_rank = ranking[visitor_team]

   row["Team1LastWin"] = won_last[home_team]
   row["Team2LastWin"] = won_last[visitor_team]
   row["Team1RanksHigher"] = team1_rank > team2_rank
   row["Team2RanksHigher"] = team2_rank > team1_rank

   dataset.ix[index] = row
   won_last[home_team] = row["Team1Win"]
   won_last[visitor_team] = not row["Team1Win"]

print dataset.ix[:5]

y_true = dataset["Team1Win"].values

clf = DecisionTreeClassifier()
X_previouswins = dataset[["Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher"]].values

scores = cross_val_score(clf, X_previouswins, y_true,
scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
