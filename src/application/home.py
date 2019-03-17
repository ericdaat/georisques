from flask import Blueprint, request, current_app, render_template
import json
from scrapping import get_risks_from_coordinates


bp = Blueprint("home", __name__)


@bp.route("/", methods=("GET", "POST"))
def risks():
    """ URL for displaying the risks given lat and long.

    This method calls `scrapping.get_risks_from_coordinate` and if it
    returns valid results, stores the results in cache for 3600 seconds to
    avoid scrapping the website again if we reload the page.

    Note: so far we use the latitude & longitude as cache key. This works
    but could end up storing a lot of similar communes in cache. A better
    way would be to get the commune from the lat & lon first, and use that
    as cache key.

    Returns:
        Flask template -- HTML template
    """

    risks = None

    if request.method == "POST":
        # Get lat & lon from POST form
        form = request.form.to_dict()
        lat = form["lat"]
        lon = form["lon"]

        # Cache key is computed from lat & lon
        # (see docstring for more details)
        cache_key = "coord:{lat}_{lon}".format(lat=lat, lon=lon)

        # Check if the results are in cache
        redis_store = current_app.extensions["redis"]
        risks = redis_store.get(cache_key)

        if risks:
            # If the results are cached, eval them as dict
            risks = eval(risks)
        else:
            # If not, scrap the website
            risks, has_found_results = get_risks_from_coordinates(
                lat=lat,
                lon=lon
            )
            if has_found_results:
                # If the scrapping returned something store the results
                # in cache for 3600 seconds
                redis_store.set(cache_key, json.dumps(risks), ex=3600)

    return render_template("home/risks.html", risks=risks)
