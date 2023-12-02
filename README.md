# sqlalchemy-challenge
Climate App

Performed an exporatory analysis on weather data from Hawaii, because it was desired to go on vacation in Hawaii. After that, created a Flask API
to return temperature information from a selected date range.<br />
<br />
<b>Climate Analysis</b><br />
-Used the provided starter notebook and hawaii.sqlite files to complete a climate analysis and data exploration.<br />
-Chose a start date and end date for the trip. Make sure that the selected vacation range is approximately 3-15 days total.<br />
-Used SQLAlchemy create_engine to connect to your sqlite database.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/32b1e281-346c-4328-89ef-af4c3f1bef22)<br />
-Used SQLAlchemy automap_base() to reflect database tables into classes and save a reference to those classes called Station and Measurement.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/7bccb5d8-c223-4e72-8418-76e6c2dfad60)<br />
<br />
<b>Precipitation Analysis</b><br />
-Designed a query to retrieve the last 12 months of precipitation data.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/874c74f9-11de-49b7-ab1e-73028d2db484)<br />
-Selected only the date and prcp values.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/6da79e61-3815-40c4-b32d-1075e685505f)<br />
-Loaded the query results into a Pandas DataFrame and set the index to the date column.<br />
-Plotted the precipitation over time for the last 12 months of precipitation data.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/99830bfc-f33d-4346-a84d-6ee37f8b7bd4)<br />
-Sorted the DataFrame values by date.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/145efab6-ed1d-418a-9b37-35e95513a836)<br />
-Used Pandas to print the summary statistics for the precipitation data.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/a914ac61-dcd8-4d4c-b070-3b234e27a1a5)<br />
<br />
<b>Station Analysis</b><br />
-Designed a query to calculate the total number of stations.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/5b143176-71aa-409f-84ad-aee9ac7c3058)<br />
-Designed a query to find the most active stations.<br />
-Listed the stations and observation counts in descending order.<br />
-Determined which station had the highest number of observations.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/46dd093c-ea85-4a1b-988b-7aaaf4059d6e)<br />
-Designed a query to retrieve the last 12 months of temperature observation data (TOBS).<br />
-Filtered by the station with the highest number of observations.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/8f952870-9ac4-434f-9de5-94524585d327)<br />
-Ploted the results as a histogram with bins=12.<br />
![image](https://github.com/KotR9001/sqlalchemy-challenge/assets/57807780/5575b2c0-c809-4697-a2f3-af608064615d)<br />
<br />
<b>Climate App</b><br />
-Used Flask to create the following routes.<br />
/<br />
Home page.<br />
-Lists all routes that are available.<br />
/api/v1.0/precipitation<br />
-Converts the query results to a dictionary using date as the key and prcp as the value.<br />
-Returns the JSON representation of your dictionary.<br />
/api/v1.0/stations<br />
-Returns a JSON list of stations from the dataset.<br />
/api/v1.0/tobs<br />
-Queries the dates and temperature observations of the most active station for the last year of data.<br />
-Return a JSON list of temperature observations (TOBS) for the previous year.<br />
/api/v1.0/<start> and /api/v1.0/<start>/<end><br/>
-Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.<br />
-When given the start only, calculates TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.<br />
-When given the start and the end dates, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.<br />
