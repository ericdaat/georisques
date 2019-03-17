import flask
import json
from scrapping import get_risks_from_coordinates


bp = flask.Blueprint("home", __name__)


@bp.route("/")
def risks():
    redis_store = flask.current_app.extensions["redis"]
    risks = redis_store.get("foo")

    if risks:
        risks = eval(risks)
    else:
        risks = get_risks_from_coordinates(lat=48.88711, lon=2.34525)
        redis_store.set("foo", json.dumps(risks))

    return flask.render_template("home/risks.html", risks=risks)
