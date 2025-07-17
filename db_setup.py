import sqlite3
import kagglehub
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import teamyearbyyearstats    
from idGetter import get_player_id, get_team_id
import os 
import pandas as pd 

conference_map = {
    1610612737: 'East',   # Atlanta Hawks
    1610612738: 'East',   # Boston Celtics
    1610612751: 'East',   # Brooklyn Nets
    1610612766: 'East',   # Charlotte Hornets
    1610612741: 'East',   # Chicago Bulls
    1610612739: 'East',   # Cleveland Cavaliers
    1610612742: 'West',   # Dallas Mavericks
    1610612743: 'West',   # Denver Nuggets
    1610612765: 'East',   # Detroit Pistons
    1610612744: 'West',   # Golden State Warriors
    1610612745: 'West',   # Houston Rockets
    1610612754: 'East',   # Indiana Pacers
    1610612746: 'West',   # LA Clippers
    1610612747: 'West',   # Los Angeles Lakers
    1610612763: 'West',   # Memphis Grizzlies
    1610612748: 'East',   # Miami Heat
    1610612749: 'East',   # Milwaukee Bucks
    1610612750: 'West',   # Minnesota Timberwolves
    1610612740: 'West',   # New Orleans Pelicans
    1610612752: 'East',   # New York Knicks
    1610612760: 'West',   # Oklahoma City Thunder
    1610612753: 'East',   # Orlando Magic
    1610612755: 'East',   # Philadelphia 76ers
    1610612756: 'West',   # Phoenix Suns
    1610612757: 'West',   # Portland Trail Blazers
    1610612758: 'West',   # Sacramento Kings
    1610612759: 'West',   # San Antonio Spurs
    1610612761: 'East',   # Toronto Raptors
    1610612762: 'West',   # Utah Jazz
    1610612764: 'East',   # Washington Wizards
}


path = kagglehub.dataset_download("ratin21/nba-player-stats-and-salaries-2010-2025")
dataset_files = os.listdir(path)
print("Files downloaded from KaggleHub:", dataset_files)



all_players = players.get_players()


nba_teams = teams.get_teams()
team_data = [(team['id'], team['full_name'], team['abbreviation'], conference_map.get(team['id'], 'Unknown')) for team in nba_teams]



conn = sqlite3.connect("nba_players.db")
cur = conn.cursor()  



#players db
cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        full_name TEXT NOT NULL,
        is_active BOOLEAN,
        team_id INTEGER
    );
""")



#player_stats db
cur.execute("""
    CREATE TABLE IF NOT EXISTS player_stats (
        player_id INTEGER,
        season TEXT,
        points REAL,
        rebounds REAL,
        assists REAL,
        steals REAL,
        blocks REAL,
        turnovers REAL,
        minutes REAL,
        "FG%" REAL, 
        "3P%" REAL,
        PRIMARY KEY (player_id, season)
    )
""")

#teams db 
cur.execute("""
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY,
        team_name TEXT,
        team_abbreviation TEXT,
        conference TEXT
    )
""")

#team_stats
cur.execute("""
    CREATE TABLE IF NOT EXISTS team_stats (
        team_id INTEGER,
        season TEXT,
        wins INTEGER,
        losses INTEGER,
        win_pct REAL,
        playoff_wins INTEGER,
        playoff_losses INTEGER,
        salary_cap REAL,
        power_ranking INTEGER,
        championship_years_ago INTEGER,
        PRIMARY KEY (team_id, season)
    )
""")

#contracts db
cur.execute("""
    CREATE TABLE IF NOT EXISTS contracts (
        player_id INTEGER,
        season TEXT,
        salary INTEGER,
        years_remaining INTEGER,
        is_restricted BOOLEAN,
        is_max_contract BOOLEAN,
        PRIMARY KEY (player_id, season)
    )
""")

# cur.executemany("""
#  INSERT OR IGNORE INTO teams (team_id, team_name, team_abbreviation, conference)
#  VALUES (?, ?, ?, ?)
# """, team_data)

# for p in all_players:
#     cur.execute("""
#         INSERT OR REPLACE INTO players (id, full_name, is_active, team_id)
#         VALUES (?, ?, ?, ?)
#     """, (p['id'], p['full_name'], p['is_active'], p.get('team_id')))
def year_to_season(year):
    return f"{year - 1}-{str(year)[-2:]}"


stats_df = pd.read_csv(os.path.join(path, 'NBA Player Stats and Salaries_2010-2025.csv'))
contracts_df= pd.read_csv(os.path.join(path, 'NBA Player Stats and Salaries_2010-2025.csv'))

player_id_map = {}



cur.execute("SELECT id, full_name FROM players")
for row in cur.fetchall():
    player_id_map[row[1]] = row[0]

stats_df['Season'] = stats_df['Year'].apply(year_to_season)
stats_df = stats_df[['Player' , 'Season' , 'PTS' , 'TRB' , 'AST','STL' , 'BLK' ,'TOV' ,'MP', 'FG%', '3P%']]
stats_df= stats_df.dropna()
stats_data = []

for _,row in stats_df.iterrows():
    name = row['Player']
    
    if name not in player_id_map: 
        continue
    
    player_id = player_id_map[name]
    stats_data.append((
    player_id, 
        row["Season"], 
        row["PTS"],
        row["TRB"],
        row["AST"],
        row['STL'],              
        row["BLK"],
        row["TOV"],
        row["MP"],        
        row["FG%"],       
        row["3P%"]        
))
    

cur.executemany("""
                INSERT OR REPLACE INTO player_stats(player_id, season, points,
                 rebounds, assists, steals, blocks, turnovers, minutes, "FG%", "3P%")
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
                """ ,stats_data)


contracts_df['salary'] = (
    contracts_df['salary']
    .replace('[\$,]', '', regex=True)  
    .astype(float)
    .fillna(0)                         
    .astype(int)
)
contracts_df = contracts_df[['player_id' , 'season' , 'salary']].dropna()


conn.commit()
conn.close()

print("Dataset path:'" , dataset_files)