from flask import Flask, render_template, request
import urllib.request, json

import os

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
@app.route("/index.html", methods = ['POST', 'GET'])
def home():
    # check if post or get
    if request.method == "GET":
        # Configure API request
        url = "https://developer.nps.gov/api/v1/parks?&api_key={}".format(os.environ.get("NPS_KEY"))
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        parks = []
        # make park data readable to template
        for park in dict["data"]:
            if park and len(park["images"])>0:
                park = {
                    "name": park["fullName"],
                    "image": park["images"][0]['url'],
                    "code": park["parkCode"]
                }
                parks.append(park)
        return render_template ("index.html", parks=parks)
    else:
        # post- read form data
        state = request.form['state']
        query = request.form['query']
        query = query.replace(' ', '%20')
        # configure request
        if query != "":
            url =  "https://developer.nps.gov/api/v1/parks?stateCode={}&q={}&api_key={}".format(state,query, os.environ.get("NPS_KEY"))
        else:
            url =  "https://developer.nps.gov/api/v1/parks?stateCode={}&api_key={}".format(state, os.environ.get("NPS_KEY"))
        response = urllib.request.urlopen(url)
        data = response.read()
        dict = json.loads(data)
        parks = []
        for park in dict["data"]:
            if park and len(park["images"])>0:
                park = {
                    "name": park["fullName"],
                    "image": park["images"][0]['url'],
                    "code": park["parkCode"]
                }
                parks.append(park)
        # list to keep track of past form values
        formInfo = [state, abbrev_to_us_state[state], query.replace('%20',' ')]
        return render_template ("index.html", parks=parks, formInfo = formInfo)

#path for each specific park
@app.route('/generic.html/<path:code>')
def get_specific(code):
    # Configure API request
    url = "https://developer.nps.gov/api/v1/parks?parkCode={}&api_key={}".format(code, os.environ.get("NPS_KEY"))
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)
    # get necessary park data
    for park in dict["data"]:
        park = {
            "name": park["fullName"],
            "description": park["description"],
            "states": park["states"],
            "images": park["images"],
            "weather": park["weatherInfo"],
            "topics": park["topics"],
            "url": park["url"],
            "address": park["addresses"][0],
            "activities": park["activities"]
        }
    return render_template ("generic.html", park = park)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
    "All 50": ""
}
    
# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))