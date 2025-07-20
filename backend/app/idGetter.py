from nba_api.stats.static import players, teams
from thefuzz import process 


def get_player_id(player_name, threshold=80): 
    all_players = players.get_players()
    player_names= {player['full_name']: player['id'] for player in all_players}    
    
    best_match , score = process.extractOne(player_name, player_names.keys())

    if score>= threshold:
        print(f"Input: {player_name}")
        print(f"Best match: {best_match} with score {score}")
        return player_names[best_match]
        
    else:
        return None

    
def get_team_id(team_name, threshold=80): 
    all_teams = teams.get_teams()
    team_names = {team['full_name']: team['id'] for team in all_teams}
    
    best_match , score = process.extractOne(team_name, team_names.keys())
    if score>= threshold:
        return team_names[best_match]
    else:
        return None

# team_name = input("Enter Team Name: ")
# print(f"The team id for the {team_name} is: {get_team_id(team_name)}")

# player_name = 'Lebron  '
# player_id = get_player_id(player_name)
# if player_id: 
#     print(f"Player ID for {player_name}: {player_id}")
# else:
#     print("Player not found.")