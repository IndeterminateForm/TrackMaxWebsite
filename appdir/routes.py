from appdir import app
from flask import request, render_template, redirect, url_for, jsonify
import matplotlib
import matplotlib.pyplot as plt
import csv
import json
from geojson import MultiPoint, Point, LineString, FeatureCollection, Feature


@app.route('/')
@app.route('/index')
def index():
    return render_template('home.html')


@app.route('/stats')
def stats():
    return render_template('stats.html', title='Stats')


@app.route('/upload')
def upload():
    return render_template('upload.html')

# If the method is POST, the user submitted data


@app.route("/upload", methods=['POST'])
def get_csv_path():
    csv_path = request.form['text']
    return redirect(url_for("plot_data", csv_path=csv_path, _external=False))


@app.route("/plot")
def plot_data():
    csv_path = request.args.get("csv_path")
    lat, long, time, alt, speed = [], [], [], [], []

    # Read the data
    with open(csv_path, "r") as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            lat.append(row[0])
            long.append(row[1])
            time.append(row[3]/1000)
            alt.append(row[2])
            speed.append(row[4])

    coords = []
    latindex = 0
    while latindex < len(lat):
        temptuple = (lat[latindex], long[latindex])
        coords.append(temptuple)
        latindex += 1

    # Create the plot and save it as an image
    # Saving the plot for "data.csv" as "data_fig.png"
    length = len(csv_path)
    plot_path = "./appdir/static/" + csv_path[2:length - 4] + "_fig1.png"
    matplotlib.use('Agg')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(time, alt)
    ax.set_title("Altitude")
    ax.set_xlabel("Time (Seconds)")
    ax.set_ylabel("Altitude (Meters)")
    fig.savefig(plot_path)
    plt.close(fig)

    length = len(csv_path)
    plot_path = "./appdir/static/" + csv_path[2:length - 4] + "_fig2.png"
    matplotlib.use('Agg')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.plot(time, speed)
    ax.set_title("Speed")
    ax.set_xlabel("Time (Seconds)")
    ax.set_ylabel("Speed (mph)")
    fig.savefig(plot_path)
    plt.close(fig)

    # Pass the path to the saved image to your HTML with "figure1" tag
    return render_template("plot.html", csv_path=csv_path, figure1="./static/" + csv_path[2:length-4] + "_fig1.png", figure2="./static/" + csv_path[2:length-4] + "_fig2.png")


@app.route('/map')
def mapfunction():
    csv_path = request.args.get("csv_path")
    lat, long, time, alt, speed = [], [], [], [], []

    # Read the data
    with open(csv_path, "r") as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            lat.append(row[0])
            long.append(row[1])
            time.append(row[3]/1000)
            alt.append(row[2])
            speed.append(row[4])

    coords = []
    latindex = 0
    while latindex < len(lat):
        temptuple = (lat[latindex], long[latindex])
        coords.append(temptuple)
        latindex += 1

    jsoncoords = MultiPoint(coords)
    stringcoords = str(jsoncoords)

    #f = open('./appdir/static/coordinates.json', 'w')
    #f.write("{\"type\": \"FeatureCollection\",\n\"features\": [{\n\t\"type\": \"Feature\",\n\t\"geometry\": {\n\t\t\"type\": \"LineString\",\n\t\t\"coordinates\": [[125.6, 10.1],[40,-105]]\n\t},\n\t\"properties\": {\n\t\"stroke\": \"#555555\",\"stroke-width\": 2, \"stroke-opacity\": 1}\n}\n]\n}")
    #f.close()

    return render_template("map.html")


@app.route('/coordinates')
def mapfunction1():
    csv_path = request.args.get("csv_path")
    lat, long, time, alt, speed = [], [], [], [], []

    # Read the data
    with open(csv_path, "r") as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader:
            lat.append(row[0])
            long.append(row[1])
            time.append(row[3]/1000)
            alt.append(row[2])
            speed.append(row[4])

    coords = []
    coordindex = 0
    while coordindex < len(lat):
        temptuple = (long[coordindex], lat[coordindex])
        coords.append(temptuple)
        coordindex += 1

    jsoncoords = LineString(coords)
    feature = Feature(geometry=jsoncoords)
    featurecollection = FeatureCollection([feature])

    return featurecollection


app.run(port=8080, debug=False)