import sqlite3
from datetime import datetime as dt
from flask import Flask, render_template, g

# con = sqlite3.connect("water_data.db")
# cur = con.cursor()
# cur.execute("CREATE TABLE data(id INTEGER PRIMARY KEY AUTOINCREMENT, date, litre, hour)")
# con.commit()

app = Flask(__name__)

def get_db(): # g is a temporary "storage unit" provided by Flask, it can store connections and other things as long as the flask server is on. G stays alive along with it's connection to the database as long as the server is on
    if "connection" not in g:
        g.conn = sqlite3.connect("water_data.db") # if no connection in g exists it creates one, if one does it simply returns it
    return g.conn # the goal of this was to reduce unnecessary power opening and closing connections in every function

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop("connection", None)
    if db is not None:
        db.close()

def add_new_row():
    get_now = dt.now()
    curr_day = str(get_now.date())
    curr_time = str(get_now.time().strftime("%H:%M:%S"))

    con = get_db()
    cur = con.cursor()
    
    data_format = [None, curr_day, 1, curr_time]
    cur.execute("INSERT INTO data VALUES (?,?,?,?)", data_format)

    con.commit()

def read_day(): 
    get_now = dt.now()
    curr_day = get_now.date()

    con = get_db()
    cur = con.cursor()

    cur.execute("""SELECT hour FROM data WHERE date="{date}" """.format(date=curr_day))
    hours_list = [row[0] for row in cur] # these things save in tuples so ou have to grab the first object and iterate from there
    res = cur.execute("""SELECT SUM(litre) FROM data WHERE date="{date}" """.format(date=curr_day))
    litres_int = int(res.fetchone()[0]) # was a tuple like (3,) so I grabbed the first (and only) element and turned it into an integer

    return str(curr_day), litres_int, hours_list # returns a tuple, first being the num of litres and another a list of hours

def read_file():
    con = get_db()
    cur = con.cursor()
    res = cur.execute("SELECT * FROM data")

    return res.fetchall()

def del_row():
    con = get_db()
    cur = con.cursor()
    cur.execute("DELETE FROM data")
    con.commit()


"""
Additional note, I think I added too many variables. Clean up code.
"""

@app.route("/drink")
def litre_drink():
    add_new_row()
    return "You drank another litre!"

@app.route("/stats")
def show_stats():
    return render_template("text.html", display_date=read_day()[0], total_litres=read_day()[1], drinking_times=read_day()[2])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")