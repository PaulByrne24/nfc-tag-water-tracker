import sqlite3
import datetime as dt
import flask

get_now = dt.datetime.today() # grabs today's date and time
curr_day = str(get_now.date())
curr_time = str(get_now.time().strftime("%H:%M:%S"))

con = sqlite3.connect("water_data.db")
cur = con.cursor()
data = [None, curr_day, 0, curr_time]
# cur.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, date, litre, hour)")
cur.execute("INSERT INTO data VALUES (?,?,?,?)",data)
# cur.execute("DELETE FROM data")
con.commit()
res = cur.execute("SELECT * FROM data")
print(res.fetchall())


def new_litre():
    get_now = dt.datetime.now()
    curr_day = str(get_now.date())
    curr_time = str(get_now.time().strftime("%H:%M:%S"))

    file = open_file()

    file[-1]["litres"] += 1
    file[-1]["hour"].append(curr_time)

    write_file(file=file)

def get_avg_l():
    pass

def read_file():
    file = open_file()
    return f"Today: {file[-1]["date"]} you drank {file[-1]["litres"]}L of water at these times: {file[-1]["hour"]}"

# changing the database and trying to implement sqllite. Currently a struggle but I see a way, every tap will save a row with the day
# 1 litre and the time. Then with SELECT and the sum command I'll add the total litres in a day and the hours will appear one after another
# on the flask website. There's no need to condense an entire day into one row
# This also means that the function that adds the "taps" can be condensed into one function and there's no need for checks that the day
# already exists. I have to make another function though, one that collects and shows the data to the user

app = flask.Flask(__name__)

@app.route("/drink")
def litre_drink():
    write_new_day()
    new_litre()
    return read_file()