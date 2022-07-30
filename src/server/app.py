from datetime import time
from flask import Flask
import flask
from schedule import Scheduler
from stretchable_clock import StretcheableClock

app = Flask(__name__)


HIDE_SECONDS = True
NUMBER_OF_HOURS_PER_DAY = 12
START_TIME = time(1, 0)
DAY_DURATION_IN_MINUTES = 45
SCHEDULE = [
    (3, "Réveil / café"),
    (8, "Horoscope"),
    (16, "Shift de travail"),
    (5, "Repas"),
    (3, "Nuit de sommeil"),
]

clock = StretcheableClock(START_TIME, DAY_DURATION_IN_MINUTES / NUMBER_OF_HOURS_PER_DAY)
scheduler = Scheduler(SCHEDULE, NUMBER_OF_HOURS_PER_DAY)

@app.route("/get_data")
def get_time():
    time = clock.get_time()
    schedule = scheduler.get_list_of_tasks(time)

    response = flask.jsonify(
        {'time': time.isoformat(), "schedule": schedule, "hide_seconds": HIDE_SECONDS}
    )
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response