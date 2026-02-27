import pandas as pd
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Load your single stats CSV
df_stats = pd.read_csv('player_stats.csv')

def normalize_position(pos: str) -> str:
    """
    Normalize the player position string to a standard format (G, F, C, G-F, F-C) 
    or return "Unknown" if it doesn't match known patterns.
    """
    key = (pos or "").replace(" ", "-").upper()
    mapping = {
        "G": "G", "F": "F", "C": "C",
        "G-F": "G-F", "F-G": "G-F", "F-C": "F-C", "C-F": "F-C",
        "GUARD": "G", "FORWARD": "F", "CENTER": "C",
        "GUARD-FORWARD": "G-F", "FORWARD-GUARD": "G-F",
        "FORWARD-CENTER": "F-C", "CENTER-FORWARD": "F-C",
    }
    return mapping.get(key, "Unknown")

def get_position_by_name(player_name: str) -> str:
    """
    Searches the NBA API by player_name to get their official NBA ID, 
    then fetches their position safely.
    """
    if not isinstance(player_name, str) or not player_name.strip():
        return "Unknown"
        
    try:
        # 1. Search the static dictionary by name (this is local and lightning fast)
        player_search = players.find_players_by_full_name(player_name)
        
        if not player_search:
            print(f"  -> Player not found in NBA database: {player_name}")
            return "Unknown"
            
        # Grab the official NBA ID from the first search result
        official_nba_id = player_search[0]['id']
        
        # 2. Guardrail: Pause for 0.6 seconds so the NBA API doesn't ban our IP
        time.sleep(0.6)
        
        # 3. Fetch info using the official NBA ID
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=official_nba_id)
        details = player_info.get_normalized_dict()['CommonPlayerInfo'][0]
        pos_raw = details.get('POSITION', '')
        
        return normalize_position(pos_raw)
        
    except Exception as e:
        print(f"  -> Error retrieving position for '{player_name}': {e}")
        return "Unknown"

def rewrite_player_stats(df):
    """
    Applies the name lookup to the dataframe and saves the updated CSV.
    """
    if 'player_name' not in df.columns:
        print("Critical Error: 'player_name' column missing from CSV!")
        return df

    print("Fetching positions from NBA API using names... this might take a moment.")
    
    # Apply the fetch function to the player_name column
    df['position'] = df['player_name'].apply(get_position_by_name)
    
    # Save the result to a new CSV
    df.to_csv('player_stats_updated.csv', index=False)
    print("\nSuccess! Data saved to 'player_stats_updated.csv'.")
    
    return df

if __name__ == "__main__":
    # Run the main script on your single CSV
    updated_dataframe = rewrite_player_stats(df_stats)
    
    # Print the first few rows to verify it worked
    print("\nPreview of updated data:")
    print(updated_dataframe[['player_name', 'position']].head())