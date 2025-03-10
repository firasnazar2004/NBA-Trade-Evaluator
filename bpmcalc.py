import pandas as pd 
import numpy as np
from nba_api.stats.endpoints import PlayerCareerStats , PlayerGameLog
from idGetter import get_player_id


#Simplified coefficients from ChatGpt that are based on historical BPM models
a = 0.25
b= 0.3 
c= 0.35 
d= 1
e = 0.9
f = 0.7

def calculate_bpm(points, rebounds , assists, steals, blocks, turnovers, minutes):
    if minutes == 0:
        return 0
    
    bpm = (a * points + 
           b * rebounds + 
           c * assists + 
           d* steals +
           e * blocks - 
           f * turnovers) / minutes *36
    return round(bpm,2)


# playerName = input("Enter player Name: ")
def get_bpm(playerName):
    player_id = get_player_id(playerName)
    current_season = '2024-25'
    if player_id:
        # print(f"Player ID for {playerName}: {player_id}")
        try:
            player_stats = PlayerGameLog(player_id=player_id , season=current_season).get_data_frames()[0]
            points = player_stats['PTS'].sum()
            rebounds= player_stats['REB'].sum()
            assists= player_stats['AST'].sum()
            steals= player_stats['STL'].sum()
            blocks= player_stats['REB'].sum()
            turnovers= player_stats['TOV'].sum()
            minutes= player_stats['MIN'].sum()
            bpm = calculate_bpm(points,rebounds,assists,steals,blocks,turnovers,minutes)
            return bpm
        # print(f"BPM for {playerName} in the {current_season} season is = {bpm}")
        except Exception as e:
            print(f"Error fetching player stats: {e}")
    else:
        print("Player not found.")