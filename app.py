from flask import Flask, render_template
import urllib.request, json

import os

app = Flask(__name__)


@app.route("/")
def test():
    # Configure API request
    url = "https://developer.nps.gov/api/v1/parks?stateCode=WI&api_key={}".format(os.environ.get("NPS_KEY"))
    print(os.environ.get("NPS_KEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    # print(dict)
    return render_template ("index.html", parks=dict["data"])

@app.route("/grte")
def get_grte():
    # Configure API request
    url = "https://developer.nps.gov/api/v1/parks?parkCode=grte&api_key={}".format(os.environ.get("NPS_KEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    parks = []
    # print(dict)
    for park in dict["data"]:
        park = {
            "Park Name": park["fullName"],
            "Description": park["description"],
            "State": park["states"],
            "Image": park["images"][0]['url']
        }
        parks.append(park)

    return {"results": parks}