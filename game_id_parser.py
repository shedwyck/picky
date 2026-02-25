from nba_api.stats.endpoints import scoreboardv2
from datetime import datetime, timedelta
import pandas as pd

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Microsoft Edge";v="121", "Chromium";v="121", "Not-A.Brand";v="99"',
    'Accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://www.nba.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

def week_days():
    date = datetime.now()
    
    def get_monday(date_obj):
        dates = []
        days_to_subtract = date_obj.weekday()
        mon = date_obj - timedelta(days=days_to_subtract)

        eow = mon + timedelta(days=6)

        print(f"start: {iso_date(mon)}")
        print(f"end: {iso_date(eow)}")

        for i in range(7):
            day = mon + timedelta(days=i)
            dates.append(iso_date(day))

        return dates

    def iso_date(date_obj):
        year = date_obj.strftime("%Y")
        month = date_obj.strftime("%m")
        day = date_obj.strftime("%d")

        date = year + "-" + month + "-" + day
        return date

    return get_monday(date)

def get_game_ids():
    games_week = []
    for date in week_days():
        sb = scoreboardv2.ScoreboardV2(game_date=date, headers=custom_headers, timeout=30)
        df = sb.get_data_frames()[0]
        game_ids = df['GAME_ID'].tolist()
        games_week.extend(game_ids)
    
    return games_week

def export_ids_to_csv():
    game_ids = get_game_ids()
    df = pd.DataFrame(game_ids, columns=['GAME_ID'])
    df.to_csv("game_ids.csv", index=False)

export_ids_to_csv()