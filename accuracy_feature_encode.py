import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelEncoder
from collections import defaultdict

dataset = pd.read_csv('data/raw/dataset.csv')
dataset.columns = ["Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1Win"] = 0
dataset["Team1LastWin"] = 0
dataset["Team2LastWin"] = 0
dataset["Team1RanksHigher"] = 0
dataset["Team2RanksHigher"] = 0
dataset["Team1WonLast"] = 0

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

teams = np.concatenate([dataset["Team1"].values, dataset["Team2"].values]).T
encoding = LabelEncoder()
encoding.fit(teams)

maps = dataset["Map"].values
encodingMaps = LabelEncoder()
encodingMaps.fit(maps)

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

   row["Team1LastWin"] = int(won_last[team1])
   row["Team2LastWin"] = int(won_last[team2])
   row["Team1RanksHigher"] = int(team1_rank > team2_rank)
   row["Team2RanksHigher"] = int(team2_rank > team1_rank)
   row["Team1Win"] = int(row["Team1Pts"] > row["Team2Pts"])
   row["Team1WonLast"] = 1 if last_match_winner[teams] == row["Team1"] else 0
   row["Team1"] = encoding.transform([team1])[0]
   row["Team2"] = encoding.transform([team2])[0]
   row["Map"] = encodingMaps.transform([row["Map"]])[0]

   dataset.ix[index] = row

   won_last[team1] = row["Team1Win"]
   won_last[team2] = not row["Team1Win"]

   winner = row["Team1"] if row["Team1Win"] else row["Team2"]
   last_match_winner[teams] = winner

print dataset.ix[:5]

y_true = dataset["Team1Win"].values

X_teams_expanded = dataset[["Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]].values

clf = DecisionTreeClassifier()
scores = cross_val_score(clf, X_teams_expanded, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
