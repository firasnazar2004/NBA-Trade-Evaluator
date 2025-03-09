from nba_api.stats.static import players

def get_player_id(player_name): 
    all_players = players.get_players()
    for player in all_players: 
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

player_name = 'Luka Dončić'
player_id = get_player_id(player_name)
if player_id: 
    print(f"Player ID for {player_name}: {player_id}")
else:
    print("Player not found.")