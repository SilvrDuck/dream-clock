from datetime import time
from flask import Flask
import flask
from schedule import Scheduler
from stretchable_clock import StretcheableClock

app = Flask(__name__)


START_TIME = time(0, 0)
HOUR_DURATION_IN_MINUTES = 45
SCHEDULE = [
    (3, "Réveil / café"),
    (8, "Récupération de carte de pointage"),
    (16, "Shift de travail"),
    (5, "Repas"),
    (3, "Nuit de sommeil"),
]

clock = StretcheableClock(START_TIME, HOUR_DURATION_IN_MINUTES)
scheduler = Scheduler(SCHEDULE)

@app.route("/get_data")
def get_time():
    time = clock.get_time()
    schedule = scheduler.get_list_of_tasks(time)

    response = flask.jsonify({'time': time.isoformat(), "schedule": schedule})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response