from flask import Blueprint, request, current_app, render_template
import json
from scrapping import get_risks_from_coordinates


bp = Blueprint("home", __name__)


@bp.route("/", methods=("GET", "POST"))
def risks():
    risks = None

    if request.method == "POST":
        form = request.form.to_dict()
        lat = form["lat"]
        lon = form["lon"]

        cache_key = "coord:{lat}_{lon}".format(lat=lat, lon=lon)

        redis_store = current_app.extensions["redis"]
        risks = redis_store.get(cache_key)

        if risks:
            risks = eval(risks)
        else:
            risks = get_risks_from_coordinates(lat=lat, lon=lon)
            if risks:
                redis_store.set(cache_key, json.dumps(risks))

    return render_template("home/risks.html", risks=risks)
