import pandas as pd
import numpy as np
from sklearn.grid_search import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

dataset = pd.read_csv('../data/samples.csv')

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

y_true = dataset["Result"].values
X_teams_expanded = dataset[["Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "TeamHigher", "Team1WonLast"]].values

clf = DecisionTreeClassifier(min_samples_leaf=6, min_samples_split=2)
scores = cross_val_score(clf, X_teams_expanded, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))

parameter_space = {
 "max_features": [3, 7, 'auto'],
 "n_estimators": [1000,],
 "criterion": ["gini", "entropy"],
 "min_samples_leaf": [3, 4, 5, 6, 7, 8, 9, 10],
}
clf = RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_samples_leaf=10, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=1000, n_jobs=2,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False)
scores = cross_val_score(clf, X_teams_expanded, y_true, scoring='accuracy')
print("Accuracy: {0:.1f}%".format(np.mean(scores) * 100))

grid = GridSearchCV(clf, parameter_space)
grid.fit(X_teams_expanded, y_true)
print("Accuracy: {0:.1f}%".format(grid.best_score_ * 100))
print(grid.best_estimator_)
