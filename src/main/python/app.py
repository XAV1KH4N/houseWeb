from datetime import date
from flask import Flask, render_template, request

import Bin
import View

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', views=getViews(), bins=getBins())


@app.route('/addViewing/', methods=['POST', 'GET'])
def addViewing():
    view = View.View()
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["appt"]
        view.addViewing(date, time)
    view.close()
    return render_template('index.html', views=getViews(), bins=getBins())


@app.route('/deleteViewing/<int:id>', methods=['POST', 'GET'])
def deleteViewing(id):
    view = View.View()
    view.deleteViewing(id)
    view.close()
    return render_template('index.html', views=getViews(), bins=getBins())


def getBins():
    bin = Bin.Bin()
    data = bin.nextBins()
    for bin in data:
        if data[bin] == 0:
            data[bin] = "Today"
        elif data[bin] == 1:
            data[bin] = "Tomorrow"
    return data


def getViews():
    view = View.View()
    views = []
    for item in view.getViewings():
        time = countDown(item[1])
        if time == 0:
            time = "Today"
        elif time == 1:
            time = "Tomorrow"
        dt = formatDate(item[1])
        views.append([item[0], dt, item[2], time])
    view.close()
    return views


def formatDate(dt):
    year, month, day = dt.split("-")
    return day + " / " + month + " / " + year


def countDown(dt):
    year, month, day = dt.split("-")
    viewing = date(int(year), int(month), int(day))
    now = date.today()
    delta = viewing - now
    return delta.days


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
