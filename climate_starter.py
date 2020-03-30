#!/usr/bin/env python
# coding: utf-8

# In[1]:


from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt


# In[2]:


import numpy as np
import pandas as pd


# In[3]:


import datetime as dt
import time


# In[4]:


###Reflect Tables into SQLAlchemy ORM


# In[5]:


# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# In[6]:


engine = create_engine("sqlite:///C:/Users/bjros/OneDrive/Desktop/KU_Data_Analytics_Boot_Camp/Homework Assignments/Homework Week 10/sqlalchemy-challenge/hawaii.sqlite")


# In[7]:


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)


# In[8]:


# We can view all of the classes that automap found
Base.classes.keys()


# In[9]:


# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[10]:


# Create our session (link) from Python to the DB
session = Session(engine)
session


# In[11]:


###Exploratory Climate Analysis


# In[12]:


# Design a query to retrieve the last 12 months of precipitation data and plot the results
# Display the Data Types
data_types = type(session.query(Measurement).first())
print(data_types.__dict__)


# In[13]:


# Display the date of the last data point in the database
dates = session.query(Measurement.date).all()
last_date = dates[-1]
last_date


# In[14]:


# Calculate the date 1 year ago from the last data point in the database
dates = session.query(Measurement.date).all()
last_date = dates[-1]
last_date1 = pd.to_datetime(last_date)
year_ago = last_date1 - dt.timedelta(days=365)
year_ago


# In[15]:


#Convert the Dates to Timestamps
last_date1 = dt.datetime.strptime('08/23/2017', "%m/%d/%Y")
year_ago = dt.datetime.strptime('08/23/2016', "%m/%d/%Y")


# In[16]:


# Perform a query to retrieve the date and precipitation scores
yearly_dates = [row for row in session.query(Measurement.date).filter(func.date(Measurement.date)>=year_ago).filter(func.date(Measurement.date)<=last_date1).all()]
print(yearly_dates)
yearly_prcp = [row for row in session.query(Measurement.prcp).filter(func.date(Measurement.date)>=year_ago).filter(func.date(Measurement.date)<=last_date1).all()]
print(yearly_prcp)


# In[17]:


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
#Show the Precipitation Data
precipitation_df


# In[18]:


# Use Pandas Plotting with Matplotlib to plot the data
#Pandas Plot
precipitation_df.plot(x="Date", y="Precipitation", kind="bar", color="blue", grid = True)
plt.title("Precipitation Over Time")
plt.xlabel("Date")
plt.ylabel("Precipitation (Inches)")
plt.xticks(np.arange(0, 12, step=1), precipitation_df['Date'], rotation=90)
plt.show()

#Save the Figure
plt.savefig("Precipitation.png")


# In[19]:


# Use Pandas to calculate the summary statistics for the precipitation data
precipitation_df['Precipitation'].describe()


# In[20]:


# Design a query to show how many stations are available in this dataset?
num_stations = session.query(Measurement.station).group_by(Measurement.station).count()
num_stations


# In[21]:


# What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
stations = [row for row in session.query(Measurement.station).group_by(Measurement.station).all()]
print(stations)
station_counts = [row for row in session.query(func.count(Measurement.station)).group_by(Measurement.station).all()]
print(station_counts)
print("-"*120)
print("USC00519281 is the most active station.")

#Put the Data in a DataFrame
stations_df = pd.DataFrame({'Station':stations, 'Station Activity':station_counts})
#Take the Values Out of Tuples
#Method to Take Values Out of Tuples Found at https://stackoverflow.com/questions/16296643/convert-tuple-to-list-and-back
stations_df['Station'] = pd.DataFrame(stations_df['Station'].tolist())
stations_df['Station Activity'] = pd.DataFrame(map(list, stations_df['Station Activity']))
#Sort the Values by Station Activity Counts
stations_df = stations_df.sort_values('Station Activity', ascending=False)
#Show the Station Data
stations_df


# In[22]:


# Using the station id from the previous query, calculate the lowest temperature recorded, 
# highest temperature recorded, and average temperature of the most active station?
low_temp = session.query(func.min(Measurement.tobs)).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()
print(f"The lowest recorded temperature at the most active station was {low_temp}oF.")
high_temp = session.query(func.max(Measurement.tobs)).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()
print(f"The lowest recorded temperature at the most active station was {high_temp}oF.")
avg_temp = session.query(func.round(func.avg(Measurement.tobs))).group_by(Measurement.station).filter(Measurement.station=='USC00519281').all()
print(f"The lowest recorded temperature at the most active station was {avg_temp}oF.")


# In[23]:


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
#Show the Precipitation Data
temp_df


# In[24]:


#Create the Bins & Groups
bins = [53, 56, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86]
groups = ['53-56', '56-59', '59-62', '62-65', '65-68', '68-71', '71-74', '74-77', '77-80', '80-83', '83-86']

#Assign the Temperature Values to Groups
temp_df['Temperature Groups'] = pd.cut(temp_df['Temperature'], bins, labels=groups)

#Create the Plot
temp_df.hist(bins=12)
plt.title('Temperature Distribution')
plt.xlabel('Temperature')
plt.ylabel('Frequency')

#Show the Plot
plt.show()

#Save the Figure
plt.savefig("Temperature_Distribution.png")


# In[25]:


###Bonus Challenge Assignment


# In[26]:


# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# function usage example
print(calc_temps('2012-02-28', '2012-03-05'))


# In[27]:


# Use your previous function `calc_temps` to calculate the tmin, tavg, and tmax 
# for your trip using the previous year's data for those same dates.


# In[28]:


# Plot the results from your previous query as a bar chart. 
# Use "Trip Avg Temp" as your Title
# Use the average temperature for the y value
# Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr)


# In[29]:


# Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
# Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation


# In[30]:


# Create a query that will calculate the daily normals 
# (i.e. the averages for tmin, tmax, and tavg for all historic data matching a specific month and day)

def daily_normals(date):
   """Daily Normals.
   
   Args:
       date (str): A date string in the format '%m-%d'
       
   Returns:
       A list of tuples containing the daily normals, tmin, tavg, and tmax
   
   """
   
   sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
   return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()
   
daily_normals("01-01")


# In[31]:


# calculate the daily normals for your trip
# push each tuple of calculations into a list called `normals`

# Set the start and end date of the trip

# Use the start and end date to create a range of dates

# Stip off the year and save a list of %m-%d strings

# Loop through the list of %m-%d strings and calculate the normals for each date


# In[32]:


# Load the previous query results into a Pandas DataFrame and add the `trip_dates` range as the `date` index


# In[33]:


# Plot the daily normals as an area plot with `stacked=False`


# In[ ]:




