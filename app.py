#########Climate App

#####Re-Enter Code From Jupyter Notebook

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt
import time

###Reflect Tables into SQLAlchemy ORM

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#Method to Resolve Thread Issue Found on https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa/51147168
engine = create_engine("sqlite:///C:/Users/bjros/OneDrive/Desktop/KU_Data_Analytics_Boot_Camp/Homework Assignments/Homework Week 10/sqlalchemy-challenge/hawaii.sqlite", connect_args={'check_same_thread': False})

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)
session

###Exploratory Climate Analysis
##Precipitation
# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Display the Data Types
data_types = type(session.query(Measurement).first())

# Display the date of the last data point in the database
dates = session.query(Measurement.date).all()
last_date = dates[-1]

# Calculate the date 1 year ago from the last data point in the database
dates = session.query(Measurement.date).all()
last_date = dates[-1]
last_date1 = pd.to_datetime(last_date)
year_ago = last_date1 - dt.timedelta(days=365)

#Convert the Dates to Timestamps
last_date1 = dt.datetime.strptime('08/23/2017', "%m/%d/%Y")
year_ago = dt.datetime.strptime('08/23/2016', "%m/%d/%Y")

# Perform a query to retrieve the date and precipitation scores
yearly_dates = [row for row in session.query(Measurement.date).filter(func.date(Measurement.date)>=year_ago).filter(func.date(Measurement.date)<=last_date1).all()]
yearly_prcp = [row for row in session.query(Measurement.prcp).filter(func.date(Measurement.date)>=year_ago).filter(func.date(Measurement.date)<=last_date1).all()]

# Save the query results as a Pandas DataFrame and set the index to the date column
#Found method to save query results as Pandas DataFrame from https://stackoverflow.com/questions/35937579/pandas-read-sql-columns-not-working-when-using-index-col-returns-all-columns-i
precipitation_df = pd.DataFrame({'Precipitation':yearly_prcp}, index=yearly_dates)

#Rename the Index Column
#Method Found at https://stackoverflow.com/questions/19851005/rename-pandas-dataframe-index
precipitation_df = precipitation_df.rename_axis("Date")
#Sort the Data and Make the Date Column Accessible
precipitation_df = precipitation_df.sort_index().reset_index()
#Pull Values Out of Tuples in Columns
#Method Found at https://stackoverflow.com/questions/29550414/how-to-split-column-of-tuples-in-pandas-dataframe
precipitation_df['Date'] = pd.DataFrame(precipitation_df['Date'].tolist())
precipitation_df['Precipitation'] = pd.DataFrame(precipitation_df['Precipitation'].tolist())

##Stations 
# Design a query to show how many stations are available in this dataset?
num_stations = session.query(Measurement.station).group_by(Measurement.station).count()
num_stations

# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
stations = [row for row in session.query(Measurement.station).group_by(Measurement.station).all()]
station_counts = [row for row in session.query(func.count(Measurement.station)).group_by(Measurement.station).all()]

#Put the Data in a DataFrame
stations_df = pd.DataFrame({'Station':stations, 'Station Activity':station_counts})
#Take the Values Out of Tuples
#Method to Take Values Out of Tuples Found at https://stackoverflow.com/questions/16296643/convert-tuple-to-list-and-back
stations_df['Station'] = pd.DataFrame(stations_df['Station'].tolist())
stations_df['Station Activity'] = pd.DataFrame(map(list, stations_df['Station Activity']))
#Sort the Values by Station Activity Counts
stations_df = stations_df.sort_values('Station Activity', ascending=False)

##Temperatures
# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
low_temp = session.query(func.min(Measurement.tobs)).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()
high_temp = session.query(func.max(Measurement.tobs)).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()
avg_temp = session.query(func.round(func.avg(Measurement.tobs))).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()

 # Choose the station with the highest number of temperature observations.
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
#Determine the last date
last_date_station = [row for row in session.query(Measurement.date).filter(Measurement.station=='USC00519281').order_by(Measurement.date.desc()).first()]
#Convert to DateTime
last_date_station = pd.to_datetime(last_date_station)
print(last_date_station)

#Calculate the Date from a Year Ago
start_date_station = last_date_station - dt.timedelta(days=365)
print(start_date_station)

#Convert the Dates to Timestamps
last_date_station = dt.datetime.strptime('08/18/2017', "%m/%d/%Y")
start_date_station = dt.datetime.strptime('08/18/2016', "%m/%d/%Y")

#Perform Query
yearly_dates = [row for row in session.query(Measurement.date).filter(Measurement.station=='USC00519281').filter(func.date(Measurement.date)>=start_date_station).filter(func.date(Measurement.date)<=last_date_station).all()]
yearly_temps = [row for row in session.query(Measurement.tobs).filter(Measurement.station=='USC00519281').filter(func.date(Measurement.date)>=start_date_station).filter(func.date(Measurement.date)<=last_date_station).all()]

# Save the query results as a Pandas DataFrame and set the index to the date column
#Found method to save query results as Pandas DataFrame from https://stackoverflow.com/questions/35937579/pandas-read-sql-columns-not-working-when-using-index-col-returns-all-columns-i
temp_df = pd.DataFrame({'Temperature':yearly_temps}, index=yearly_dates)

#Rename the Index Column
#Method Found at https://stackoverflow.com/questions/19851005/rename-pandas-dataframe-index
temp_df = temp_df.rename_axis("Date")
#Sort the Data and Make the Date Column Accessible
temp_df = temp_df.sort_index().reset_index()
#Pull Values Out of Tuples in Columns
#Method Found at https://stackoverflow.com/questions/29550414/how-to-split-column-of-tuples-in-pandas-dataframe
temp_df['Date'] = pd.DataFrame(temp_df['Date'].tolist())
temp_df['Temperature'] = pd.DataFrame(temp_df['Temperature'].tolist())

#Close All Existing Sessions
#Method Found at https://docs.sqlalchemy.org/en/13/orm/session_api.html
#session.close_all()

###Create New Code for the Climate App
#Import Flask & climate_starter notebook
#Method to Allow Import of Python Files Found at https://stackoverflow.com/questions/4142151/how-to-import-the-class-within-the-same-directory-or-sub-directory
from flask import Flask, jsonify, Response

#Create App
app = Flask(__name__)

#Define the Start & End Dates
start = dt.datetime.strptime('3/18/2012', '%m/%d/%Y')
end = dt.datetime.strptime('3/18/2013', '%m/%d/%Y')

#Create the Homepage
@app.route("/")
def home():
    return(
        f"Here is the homepage</br>."
        f"---------------------------------</br>"
        f"Here is the directory of routes</br>."
        f"-----------------------------------------</br>"
        f"Here is the page with precipitation data</br>"
        f"/api/v1.0/precipitation</br>"
        f"----------------------------------------</br>"
        f"Here is the page with the stations list</br>" 
        f"/api/v1.0/stations</br>"
        f"-----------------------------------------------------------------------------------------------</br>"
        f"Here is the page with the temperature data from the most active station from the previous year</br>"
        f"/api/v1.0/tobs</br>"
        f"------------------------------------------------------------------------------------------------------------------------------</br>"
        f"Here is the list of minimum, average, and maximum temperature values from the specified start date to the last available date</br>"
        f"/api/v1.0/start</br>"
        f"------------------------------------------------------------------------------------------------------------------------------</br>"
        f"Here is the list of minimum, average, and maximum temperature values from the specified start date to the specified end date</br>"
        f"/api/v1.0/start/end"
    )

#Create the Precipitation Page
@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create the Precipitation List
    prcp_list = []
    #session = Session(engine)
    for date, prcp in session.query(Measurement.date, Measurement.prcp).all():
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    #session.close()
    return jsonify(prcp_list)
        

#Create the Stations Page
@app.route("/api/v1.0/stations")
def station():
    #Create the Stations List
    stations_list = []
    #session = Session(engine)
    for station in session.query(Measurement.station).group_by(Measurement.station).all():
        stations_dict = {}
        stations_dict["station"] = station
        stations_list.append(stations_dict)
    #session.close()
    return jsonify(stations_list)
    

#Create the Temperature Page for the Most Active Station from the Last Year
@app.route("/api/v1.0/tobs")
def tobs():
    #Create the Temperature List for the Most Active Station from the Last Year
    temp_list = []
    #session = Session(engine)
    for date, tobs in session.query(Measurement.date, Measurement.tobs).all():
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)
    #session.close()
    return jsonify(temp_list)

#Create the List of Minimum, Average, and Maximum Temperature Values from the Specified Start Date Where the End Date is Not Specified
@app.route("/api/v1.0/start")
def extremes1():
    #session = Session(engine)
    #Perform Queries for Minimum, Average, & Maximum Temperature Values where the End Date is not Specified in the URL
    low_temp1 = session.query(func.min(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
    print(f"The lowest recorded temperature at the most active station was {low_temp1}oC.")
    high_temp1 = session.query(func.max(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
    print(f"The highest recorded temperature at the most active station was {high_temp1}oC.")
    avg_temp1 = session.query(func.round(func.avg(Measurement.tobs))).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=last_date1).all()
    print(f"The average temperature at the most active station was {avg_temp1}oC.")
    #session.close()
    return(f"The minimum temperature in the date range is: {low_temp1}oF.</br>"
           f"The average temperature in the date range is: {avg_temp1}oF.</br>"
           f"The maximum temperature in the date range is: {high_temp1}oF.</br>")

#Create the List of Minimum, Average, and Maximum Temperature Values from the Specified Start Date to the Specified End Date
@app.route("/api/v1.0/start/end")
def extremes2():
    #session = Session(engine)
    #Perform Queries for Minimum, Average, & Maximum Temperature Values where the End Date is Specified in the URL
    low_temp2 = session.query(func.min(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
    print(f"The lowest recorded temperature at the most active station was {low_temp2}oC.")
    high_temp2 = session.query(func.max(Measurement.tobs)).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
    print(f"The highest recorded temperature at the most active station was {high_temp2}oC.")
    avg_temp2 = session.query(func.round(func.avg(Measurement.tobs))).filter(func.date(Measurement.date)>=start).filter(func.date(Measurement.date)<=end).all()
    print(f"The average temperature at the most active station was {avg_temp2}oC.")
    #session.close()
    return (f"The minimum temperature in the date range is: {low_temp2}oF.</br>"
            f"The average temperature in the date range is: {avg_temp2}oF.</br>"
            f"The maximum temperature in the date range is: {high_temp2}oF.</br>")

#Create the URL
if __name__ == "__main__":
    app.run(debug=True)