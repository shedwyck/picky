from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
import re

def normalize_position(pos: str) -> str:
    """
      Normalize the player position string to a standard format (G, F, C, G-F, F-C) or return "Unknown" if it doesn't match known patterns.
    """
    # Normalize key to uppercase and hyphen-separated
    key = (pos or "").replace(" ", "-").upper()
    mapping = {
        # Single-letter
        "G": "G", "F": "F", "C": "C",
        # Hyphenated single-letter combos
        "G-F": "G-F", "F-G": "G-F", "F-C": "F-C", "C-F": "F-C",
        # Full words
        "GUARD": "G", "FORWARD": "F", "CENTER": "C",
        "GUARD-FORWARD": "G-F", "FORWARD-GUARD": "G-F",
        "FORWARD-CENTER": "F-C", "CENTER-FORWARD": "F-C",
    }
    return mapping.get(key, "Unknown")

def get_player_position(player_name: str) -> str:
    """
    Get the position of a player given their first and last name (e.g., "Stephen Curry").

    Args:
        player_name (str): The full name of the player.

    Returns:
        str: The position of the player: G | F | C | G-F | F-C | Unknown
    """
    player_id = None
    try:
        # Search for the player by name
        player_search = players.find_players_by_full_name(player_name)
        if not player_search:
            return "Unknown"
        player_id = player_search[0]['id']
          
        # Fetch the player's info using their ID
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
          
        # Parse the returned dictionary
        details = player_info.get_normalized_dict()['CommonPlayerInfo'][0]
        pos_raw = details.get('POSITION', '') or ''
        # Split on hyphen or slash; trim parts
        parts = [p.strip() for p in re.split(r'[-/]', pos_raw) if p.strip()]
        if len(parts) > 2:
            chosen = parts[-1]  # Pick the latter one when more than 2 positions
        elif len(parts) == 2:
            # Preserve as hyphenated combo (use single-letter if parts are single-letter)
            if all(len(p) == 1 for p in parts):
                chosen = f"{parts[0].upper()}-{parts[1].upper()}"
            else:
                chosen = f"{parts[0].capitalize()}-{parts[1].capitalize()}"
        else:
            chosen = pos_raw.strip()
        return normalize_position(chosen)
    except Exception as e:
        print(f"Error retrieving position for player '{player_name}': {e}")
        return "Unknown"



print(get_player_position("LeBron James"))
# sample input that would return F-C
print(get_player_position("Anthony Davis"))