import pandas as pd 
from nba_api.stats.endpoints import  TeamYearByYearStats , CommonTeamRoster, PlayerCareerStats



team_id = 1610612738  
team_stats = TeamYearByYearStats(team_id=team_id).get_data_frames()[0]
team_roster = CommonTeamRoster(team_id=team_id).get_data_frames()[0]
player_stats = PlayerCareerStats(player_id=2544).get_data_frames()

print(player_stats)
