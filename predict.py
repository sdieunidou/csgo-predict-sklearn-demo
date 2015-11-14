import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

dataset = pd.read_csv('data/samples.csv')

teams = np.concatenate([dataset["Team1"].values, dataset["Team2"].values]).T
encoding = LabelEncoder()
encoding.fit(teams)

maps = dataset["Map"].values
encodingMaps = LabelEncoder()
encodingMaps.fit(maps)

for index, row in dataset.iterrows():
   row["Team1"] = encoding.transform([row["Team1"]])[0]
   row["Team2"] = encoding.transform([row["Team2"]])[0]
   row["Map"] = encodingMaps.transform([row["Map"]])[0]

   dataset.ix[index] = row

y_true = dataset["Team1Win"].values
X_teams_expanded = dataset[["Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]].values

clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features=5, max_leaf_nodes=None,
            min_samples_leaf=6, min_samples_split=3,
            min_weight_fraction_leaf=0.0, n_estimators=1000, n_jobs=2,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False)

clf.fit(X_teams_expanded, y_true)

dataset = pd.read_csv("data/submission.csv")
dataset.columns = ["Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]

for index, row in dataset.iterrows():
   team1 = row["Team1"]
   team2 = row["Team2"]
   row["Team1"] = encoding.transform([team1])[0]
   row["Team2"] = encoding.transform([team2])[0]
   row["Map"] = encodingMaps.transform([row["Map"]])[0]

   dataset.ix[index] = row

X_submission = dataset[["Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "Team1RanksHigher", "Team2RanksHigher", "Team1WonLast"]].values

print clf.predict(X_submission)
