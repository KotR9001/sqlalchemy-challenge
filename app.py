###Climate App

#Import Flask & climate_starter notebook
from flask import Flask, jsonify
#import import_ipynb
import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path

find_notebook(climate_starter.ipynb)

#Create App
app = Flask(__name__)

#Create the Precipitation List
prcp_list = []

#Create the Stations List
stations_list = []

#Create the Temperature List for the Most Active Station from the Last Year
temp_list = []

#Define the Start & End Dates
start = 3/18/2012
end = 3/18/2017

#Perform Queries for Minimum, Average, & Maximum Temperature Values where the End Date is not Specified in the URL
low_temp1 = session.query(func.min(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
print(f"The lowest recorded temperature at the most active station was {low_temp1}oC.")
high_temp1 = session.query(func.max(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
print(f"The highest recorded temperature at the most active station was {high_temp1}oC.")
avg_temp1 = session.query(func.round(func.avg(Measurement.tobs))).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
print(f"The average temperature at the most active station was {avg_temp1}oC.")

#Perform Queries for Minimum, Average, & Maximum Temperature Values where the End Date is Specified in the URL
low_temp2 = session.query(func.min(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
print(f"The lowest recorded temperature at the most active station was {low_temp2}oC.")
high_temp2 = session.query(func.max(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
print(f"The highest recorded temperature at the most active station was {high_temp2}oC.")
avg_temp2 = session.query(func.round(func.avg(Measurement.tobs))).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
print(f"The average temperature at the most active station was {avg_temp2}oC.")

#Create the Homepage
app.route("/")
def home():
    print("Here is the homepage.")
    print("---------------------")
    print("Here is the directory of routes.")
    print("--------------------------------")
    print("/api/v1.0/precipitation")
    print("/api/v1.0/stations")
    print("/api/v1.0/tobs")
    print("/api/v1.0/<start>")
    print("/api/v1.0/<start>/<end>")

#Create the Precipitation Page
app.route("/api/v1.0/precipitation")
def precipitation():
    print("Here is the page with precipitation data.")
    for date, prcp in session.query(Measurement.date, Measurement.prcp):
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

#Create the Stations Page
app.route("/api/v1.0/stations")
def stations():
    print("Here is the page with the stations list.")
    for station in session.query(Measurement.station):
        stations_dict = {}
        stations_dict["station"] = station
        stations_list.append(stations_dict)
    return jsonify(stations_list)

#Create the Temperature Page for the Most Active Station from the Last Year
app.route("/api/v1.0/tobs")
def tobs():
    print("Here is the page with the temperature data from the most active station from the previous year.")
    for date, tobs in session.query(Measurement.date, Measurement.tobs):
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["tobs"] = tobs
        prcp_list.append(prcp_dict)
    return jsonify(temp_dict)

#Create the List of Minimum, Average, and Maximum Temperature Values from the Specified Start Date Where the End Date is Not Specified
app.route("/api/v1.0/<start>")
def extremes():
    print("Here is the list of minimum, average, and maximum temperature values from the specified start date to the last available date.")
    return jsonify([f"The minimum temperature in the date range is: {low_temp1}oF.",
                    f"The average temperature in the date range is: {avg_temp1}oF.",
                    f"The maximum temperature in the date range is: {max_temp1}oF."])

#Create the List of Minimum, Average, and Maximum Temperature Values from the Specified Start Date to the Specified End Date
app.route("/api/v1.0/<start>/<end>")
def extremes():
    print("Here is the list of minimum, average, and maximum temperature values from the specified start date to the specified end date.")
    return jsonify([f"The minimum temperature in the date range is: {low_temp2}oF.",
                    f"The average temperature in the date range is: {avg_temp2}oF.",
                    f"The maximum temperature in the date range is: {max_temp2}oF."])

#Create the URL
if __name__ == "__main__":
    app.run(debug=True)