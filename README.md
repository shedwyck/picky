## references
[nba stats api](https://github.com/swar/nba_api/blob/master/docs/examples/LiveData.ipynb)

### initial progress - 02/25/2026
`stat_parser.py` - fetches individual player stats (PRA) from the games listed in the `game_ids.csv` file generated from `game_id_parser.py`. Currently experiencing issues with parsing multiple games.

`game_id_parser.py` - identifies the game ID of the games of the current week, meaning Monday (Start of Week) until Sunday (End of Week), exports into `game_ids.csv`.