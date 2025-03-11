import pandas as pd 
from nba_api.stats.endpoints import  TeamYearByYearStats , CommonTeamRoster, PlayerCareerStats
from bpmcalc import  get_bpm
from idGetter import get_team_id

#def calculate_fv():


# def get_fv():    

def calculate_roster_strength(teamName):
    roster_strength = 0 
    team_id = get_team_id(teamName)
    roster = CommonTeamRoster(team_id=team_id).get_data_frames()[0]
    for _, player in roster.iterrows(): 
        player_name = player['PLAYER']
        roster_strength +=  get_bpm(player_name)

team_name = input("Enter team name: ")
# team_id = get_team_id(team_name)
# roster = CommonTeamRoster(team_id=team_id).get_data_frames()[0]
# print(roster)
print(calculate_roster_strength(team_name))
