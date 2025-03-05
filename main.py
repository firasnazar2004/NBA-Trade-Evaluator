import sys
import pandas as pd
sys.path.append(r"E:\Firas Main Library\Projects\NBA-TRADE-EVAULATOR\nba_env\Lib\site-packages")
from sportsipy.nba.roster import Player
from basketball_reference_scraper.players import get_stats
import kagglehub
from kagglehub import KaggleDatasetAdapter
from nba_api.stats.endpoints import LeagueStandings, TeamYearByYearStats

file_path = "database_24_25.csv"

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "eduardopalmieri/nba-player-stats-season-2425",
  file_path)
path = kagglehub.dataset_download("jamiewelsh2/nba-player-salaries-2022-23-season")







team_history = TeamYearByYearStats(team_id="1610612738").get_data_frames()[0]  # Example: Boston Celtics
print("Team History Columns:", team_history.columns)

# salaries_ds = pd.read_csv(r"C:\Users\FIRAS\.cache\kagglehub\datasets\jamiewelsh2\nba-player-salaries-2022-23-season\versions\2\nba_salaries.csv")
