import json
import datetime as dt
import time

def open_file():
    with open("water_db.json", "r") as prev_file:
        file = json.load(prev_file)
    return file

def write_file(file):
    with open("water_db.json", "w") as new_file:
        json.dump(file, new_file)

def write_new_day():
    get_now = dt.datetime.today() # grabs today's date and time
    curr_day = str(get_now.date())
    data = {"date": str(curr_day), "litres": 0, "hour": []}
    file = open_file()

    if curr_day == file[-1]["date"]: # checks if the newest day is the same as the current one [-1] just gives the last value of the list
        return None 
    else: # if the values mismatch then a new dict gets added with the new date
        file.append(data)
        write_file(file=file)


def new_litre():
    get_now = dt.datetime.now()
    curr_time = get_now.time().strftime("%H:%M:%S")

    file = open_file()

    file[-1]["litres"] += 1
    file[-1]["hour"].append(curr_time)

    write_file(file=file)

def read_file():
    file = open_file()
    print(f"Today: {file[-1]["date"]} you drank {file[-1]["litres"]}L of water at these times: {file[-1]["hour"]}")
