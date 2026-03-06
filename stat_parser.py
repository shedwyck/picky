from dataclasses import dataclass
from datetime import timezone
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
import pandas as pd
import time

@dataclass
class Player:
    id: str
    name: str
    pts: int = 0
    reb: int = 0
    ast: int = 0
    stl: int = 0
    blk: int = 0
    pos: str = ""
    team: str = ""

f = "{gameId}: {awayTeam} vs. {homeTeam} @ {gameTimeLTZ}" 
def get_game_stats(game):
    box = boxscore.BoxScore(game)

    team = box.home_team_stats.get_dict()
    print(team['teamName'])
    all_players = box.home_team_player_stats.get_dict() + box.away_team_player_stats.get_dict()
    stats = []
    for player in all_players:
        current_player = Player(
            id=player['personId'],
            name=player['name'],
            pts=player['statistics']['points'],
            reb=player['statistics']['reboundsTotal'],
            ast=player['statistics']['assists'],
            stl = player['statistics']['steals'],
            blk = player['statistics']['blocks']
        )
        stats.append(current_player)
    return stats

def overall_tracker(current, overall):
    for player in current:
        name = player['name']
        if name not in overall:
            overall[name] = {
                # 'team': player['team'],
                # 'pos': player['position'],
                'pts': 0,
                'reb': 0,
                'ast': 0,
                'games': 0
            }

        overall[name]['pts'] += player['points']
        overall[name]['reb'] += player['rebounds']
        overall[name]['ast'] += player['assists']
        overall[name]['stl'] += player['steals']
        overall[name]['blk'] += player['blocks']
        overall[name]['games'] += 1
    
# print(get_game_stats('0022500840'))
# tracker = {}
# overall_tracker(get_game_stats('0022500840'), tracker)
# print(tracker)

df = pd.read_csv('game_ids.csv', dtype=str)
game_ids = df['GAME_ID'].tolist()
game_ids = list(dict.fromkeys(game_ids))

print(get_game_stats(game_ids[0]))