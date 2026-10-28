import json
import datetime as dt

get_now = dt.datetime.now() # grabs today's date and time
curr_day = get_now.date()
curr_time = get_now.time().strftime("%H:%M:%S")

def write_new_day(data):
    with open("water_db.json", "r") as prev_file:
        file = json.load(prev_file)

    file.append(data)

    with open("water_db.json", "w", encoding="utf-8") as new_file:
        json.dump(file, new_file)

data = {"date": str(curr_day), "litres": 0, "hour": []}
write_new_day(data=data)
