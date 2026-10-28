import flask
import main

app = flask.Flask(__name__)

@app.route("/drink")
def litre_drink():
    main.new_litre()

main.read_file()
