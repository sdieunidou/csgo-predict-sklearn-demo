import pandas as pd
from collections import defaultdict

dataset = pd.read_csv('data/raw/dataset.csv', parse_dates=["Date"])
dataset.columns = ["Date", "Map", "Team1", "Team1Pts", "Team2", "Team2Pts"]
dataset["Team1LastWin"] = 0
dataset["Team2LastWin"] = 0
dataset["TeamHigher"] = 0
dataset["Team1WonLast"] = 0
dataset["Result"] = 0

ranking = {
   'EnVyUs': 20,
   'Virtus.pro': 29,
   'TSM': 18,
   'fnatic': 17,
   'Natus Vincere': 16,
   'NiP': 15,
   'G2': 14,
   'mousesports': 13,
   'Luminosity': 12,
   'Titan': 11,
   'Cloud9': 10,
   'dignitas': 9,
   'CLG': 8,
   'Liquid': 7,
   'FlipSid3': 6,
   'E-frag.net': 5,
   'Conquest': 4,
   'Renegades': 3,
   'Vexed': 2,
   'CSGL': 1,
}

won_last = defaultdict(int)
last_match_winner = defaultdict(int)

for index, row in dataset.sort("Date").iterrows():
   team1 = row["Team1"]
   team2 = row["Team2"]

   team1_rank = 0;
   team2_rank = 0;

   if ranking.has_key(team1):
      team1_rank = ranking[team1]

   if ranking.has_key(team2):
      team2_rank = ranking[team2]

   team_higher = 0
   if team1_rank > 0 and team1_rank > team2_rank:
      team_higher = 1
   elif team2_rank > 0 and not team1_rank > team2_rank:
      team_higher = 2

   teams = tuple(sorted([team1, team2]))

   result = 0
   if row["Team1Pts"] > row["Team2Pts"]:
      result = 1
   elif row["Team2Pts"] > row["Team1Pts"]:
      result = 2

   row["Team1LastWin"] = int(won_last[team1])
   row["Team2LastWin"] = int(won_last[team2])
   row["TeamHigher"] = int(team_higher)
   row["Result"] = result
   row["Team1WonLast"] = 1 if last_match_winner[teams] == row["Team1"] else 0

   dataset.ix[index] = row

   won_last[team1] = row["Result"] == 1
   won_last[team2] = row["Result"] == 2

   winner = row["Team1"] if row["Result"] == 1 else row["Team2"]
   last_match_winner[teams] = winner

X_teams_expanded = dataset[["Result", "Date", "Team1", "Team2", "Map", "Team1LastWin", "Team2LastWin", "TeamHigher", "Team1WonLast"]].values
dataset.to_csv("data/samples.csv")
