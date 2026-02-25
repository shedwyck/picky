import requests
import time
import random
from bs4 import BeautifulSoup

games = []
season = 87

for i in range(1,63):
    url = f"https://uaap.livestats.ph/tournaments/uaap-season-{season}-men-s-basketball?game_id={i}"

    wait_time = random.uniform(2, 5)
    time.sleep(wait_time)

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming 'soup' is already defined from your requests.get()
    tables = soup.find_all('table', class_='box-score')

    all_game_stats = {}
    team_names = []
    for table in tables:
        team_name = table.find_previous('div', class_='team_code').get_text(strip=True)
        team_names.append(team_name)

    print(f"\nGAME {i} - {team_names[0]} vs {team_names[1]}")
    for table in tables:
        team_name = table.find_previous('div', class_='team_code').get_text(strip=True)
    
        all_game_stats[team_name] = []
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            if 'bsheader_type' in row.get('class', []):
                continue
                
            cells = row.find_all('td')
            if len(cells) > 10:
                player_data = {
                    "Team": team_name,
                    "No": cells[0].get_text(strip=True),
                    "Name": cells[1].get_text(strip=True),
                    "PTS": cells[4].get_text(strip=True),
                    "REB": cells[15].get_text(strip=True),
                    "AST": cells[16].get_text(strip=True),
                    "STL": cells[18].get_text(strip=True)
                }
                all_game_stats[team_name].append(player_data)
                print(f"{team_name:<8} | #{player_data['No']:<3} | {player_data['Name']:<20} | {player_data['PTS']:<4} | {player_data['REB']:<4} | {player_data['AST']:<4}")
        
    games.append(all_game_stats)

def get_all_player_averages(game_data):
    stats_tracker = {}

    for game in game_data:
        for team_name, players in game.items():
            for p in players:
                name = p['Name']
                # Calculate PRA for this instance
                current_pra = int(p['PTS']) + int(p['REB']) + int(p['AST'])
                
                if name not in stats_tracker:
                    stats_tracker[name] = {
                        "total_pra": current_pra, 
                        "games": 1, 
                        "team": team_name
                    }
                else:
                    stats_tracker[name]["total_pra"] += current_pra
                    stats_tracker[name]["games"] += 1

    # Now calculate the averages and put them in a sortable list
    leaderboard = []
    for name, data in stats_tracker.items():
        avg_pra = data["total_pra"] / data["games"]
        leaderboard.append({
            "Name": name,
            "Team": data["team"],
            "Avg_PRA": avg_pra,
            "GP": data["games"]
        })

    # Sort by Avg_PRA descending
    return sorted(leaderboard, key=lambda x: x['Avg_PRA'], reverse=True)

# --- Execute and Print ---
full_leaderboard = get_all_player_averages(games)

print(f"{'TEAM':<10} | {'PLAYER':<20} | {'GP':<3} | {'AVG PRA':<8}")
print("-" * 50)
for entry in full_leaderboard:
    # Only show players who actually scored/played (optional filter)
    if entry['Avg_PRA'] > 0:
        print(f"{entry['Team']:<10} | {entry['Name']:<20} | {entry['GP']:<3} | {entry['Avg_PRA']:>7.2f}")