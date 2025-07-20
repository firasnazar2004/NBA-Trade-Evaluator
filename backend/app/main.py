import sys
# import pandas as pd
sys.path.append("/Users/firasnazar/Main Library/Coding/Projects/NbaTradeEvaluator/NBA-Trade-Evaluator/nba_env/lib/python3.13/site-packages")
from sportsipy.nba.roster import Player
from basketball_reference_scraper.players import get_stats
import kagglehub
from kagglehub import KaggleDatasetAdapter
from nba_api.stats.endpoints import LeagueStandings, TeamYearByYearStats
import requests
url = "https://stats.nba.com/stats/scoreboard/?GameDate=02/10/2025"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
print(response.status_code)







team_history = TeamYearByYearStats(team_id="1610612738").get_data_frames()[0]  # Example: Boston Celtics
print("Team History Columns:", team_history.columns)

# salaries_ds = pd.read_csv(r"C:\Users\FIRAS\.cache\kagglehub\datasets\jamiewelsh2\nba-player-salaries-2022-23-season\versions\2\nba_salaries.csv")
