import pandas as pd 
import numpy as np
from nba_api.stats.endpoints import PlayerCareerStats , PlayerGameLog
from nba_api.stats.static import players
from idGetter import get_player_id
import time


#Simplified coefficients from ChatGpt that are based on historical BPM models
a = 0.22
b= 0.28 
c= 0.32 
d= 1
e = 0.85
f = 0.7
g = 10
h = 7
def get_all_bpm():
    all_players = players.get_active_players()
    players_bpm_list = []
    
    for player in all_players[:500]:
        player_name = player['full_name']
        print(f"Checking BPM for: {player_name}")
        bpm = get_bpm(player_name)
        if bpm is not None:
            players_bpm_list.append((player_name,bpm))
            time.sleep(2)
            print(f"Collected BPMs for {len(players_bpm_list)}")
    return pd.DataFrame(players_bpm_list, columns=['Player','BPM'])


def get_percentile_ranking(player_name,bpm_df):
    bpm_df = bpm_df.sort_values(by='BPM' , ascending=False).reset_index(drop=True)
    bpm_df['Rank'] = bpm_df.index + 1 
    bpm_df['Percentile'] =bpm_df['Rank'] / len(bpm_df) * 100 
    player_row = bpm_df[bpm_df['Player']==player_name]
    
    if player_row.empty:
        return None,None
    
    player_rank = int(player_row['Rank'].values[0])
    player_percentile = float(player_row['Percentile'].values[0])

    return player_rank, player_percentile

def calculate_bpm(points, rebounds , assists, steals, blocks, turnovers, minutes, fg_pct, three_pct):
    if minutes == 0:
        return 0
    
    bpm = (a * points + 
           b * rebounds + 
           c * assists + 
           d* steals +
           e * blocks - 
           f * turnovers + 
           g * fg_pct + 
           h * three_pct
           
           ) / minutes *36
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

bpm_df = get_all_bpm()
player_name = 'lebron'
rank, percentile = get_percentile_ranking(player_name, bpm_df)