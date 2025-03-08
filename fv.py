import pandas as pd 
from nba_api.stats.endpoints import  TeamYearByYearStats



team_id = 1610612738  
team_stats = TeamYearByYearStats(team_id=team_id).get_data_frames()[0]

print('xyz')
print(team_stats[['YEAR', 'WINS', 'LOSSES', 'WIN_PCT', 'CONF_RANK', 'NBA_FINALS_APPEARANCE', 'PTS_RANK']])
