import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from collections import defaultdict

dataset = pd.read_csv('../data/raw/dataset.csv')
dataset.columns = ["Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1Win"] = dataset["Team1Pts"] > dataset["Team2Pts"]
dataset["Team1LastWin"] = False;
dataset["Team2LastWin"] = False;

won_last = defaultdict(int)
for index, row in dataset.iterrows():
   home_team = row["Team1"]
   visitor_team = row["Team2"]
   row["Team1LastWin"] = won_last[home_team]
   row["Team2LastWin"] = won_last[visitor_team]
   dataset.ix[index] = row
   won_last[home_team] = row["Team1Win"]
   won_last[visitor_team] = not row["Team1Win"]

print dataset.ix[:5]

y_true = dataset["Team1Win"].values

clf = DecisionTreeClassifier()
X_previouswins = dataset[["Team1LastWin", "Team2LastWin"]].values

scores = cross_val_score(clf, X_previouswins, y_true,
scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))
