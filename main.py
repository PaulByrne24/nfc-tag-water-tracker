import json
import datetime as dt

get_date = str(dt.date.today()) # grabs today's date and turns it to string, as json doesn't accept dataype "datetime" uses

def write_new_day(data):
    with open("water_db.json", "w", encoding="utf-8") as file:
        json.dump(data, file)

# data = {"date": get_date, "litres": 0, "hour": []}
# write(data)
