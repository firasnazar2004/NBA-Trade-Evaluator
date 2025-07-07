import requests
import time

# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Connection": "keep-alive",
#     "Host": "stats.nba.com"
# }
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.15; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.nba.com",
    "Referer": "https://www.nba.com/",
    "Connection": "keep-alive"
}
def get_player_stats(player_id, season="2024-25", retries=3):
    url = f"https://stats.nba.com/stats/playergamelog?PlayerID={player_id}&Season={season}&SeasonType=Regular%20Season"
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=30)  # Increased timeout
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(5)  # Wait 5 seconds before retrying

    print("All attempts failed. Could not fetch player stats.")
    return None

# Test with LeBron James' Player ID (2544)
stats = get_player_stats(2544, "2023-24")
print(stats if stats else "No stats retrieved.")
