from datetime import datetime, timedelta

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
