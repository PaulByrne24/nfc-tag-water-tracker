import sqlite3
import datetime as dt
import flask

# con = sqlite3.connect("water_data.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, date, litre, hour)")
# con.commit()

def add_new_row():
    get_now = dt.datetime.now()
    curr_day = str(get_now.date())
    curr_time = str(get_now.time().strftime("%H:%M:%S"))

    con = sqlite3.connect("water_data.db")
    cur = con.cursor()
    
    data = [None, curr_day, 1, curr_time]
    cur.execute("INSERT INTO data VALUES (?,?,?,?)",data)

    con.commit()
    con.close()

def read_day(): 
    get_now = dt.datetime.now()
    curr_day = get_now.date()

    con = sqlite3.connect("water_data.db")
    cur = con.cursor()
    cur.execute("""SELECT hour FROM data WHERE date="{date}" """.format(date=curr_day))
    ret_hours = [row[0] for row in cur] # these things save in tuples so ou have to grab the first object and iterate from there

    res = cur.execute("""SELECT SUM(litre) FROM data WHERE date="{date}" """.format(date=curr_day))
    tmp = int(res.fetchone()[0]) # was a tuple like (3,) so I grabbed the first (and only) element and turned it into an integer
    con.close()
    return str(curr_day), tmp, ret_hours # returns a tuple, first being the num of litres and another a list of hours

def read_file():
    con = sqlite3.connect("water_data.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM data")
    ret = res.fetchall()
    con.close()
    return ret

def del_row():
    con = sqlite3.connect("water_data.db")
    cur = con.cursor()
    cur.execute("DELETE FROM data")
    con.commit()
    con.close()

# changing the database and trying to implement sqllite. Currently a struggle but I see a way, every tap will save a row with the day
# 1 litre and the time. Then with SELECT and the sum command I'll add the total litres in a day and the hours will appear one after another
# on the flask website. There's no need to condense an entire day into one row
# This also means that the function that adds the "taps" can be condensed into one function and there's no need for checks that the day
# already exists. I have to make another function though, one that collects and shows the data to the user
# Additional note, I think I added too many variables

app = flask.Flask(__name__)

@app.route("/drink")
def litre_drink():
    add_new_row()
    return "You drank another litre!"

@app.route("/stats")
def show_stats():
    return flask.render_template("text.html", display_date=read_day()[0], total_litres=read_day()[1], drinking_times=read_day()[2])