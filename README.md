# sqlalchemy-challenge
Climate App

It was desired to go on vacation in Hawaii, so an exporatory analysis was performed on weather data from Hawaii. After that, a Flask API
was created to return temperature information from a selected date range.


Climate Analysis

-Used the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.

-Chose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.

-Used SQLAlchemy create_engine to connect to your sqlite database.

-Used SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.


Precipitation Analysis

-Designed a query to retrieve the last 12 months of precipitation data.

-Selected only the date and prcp values.

-Loaded the query results into a Pandas DataFrame and set the index to the date column.

-Sorted the DataFrame values by date.

-Used Pandas to print the summary statistics for the precipitation data.


Station Analysis

-Designed a query to calculate the total number of stations.

-Designed a query to find the most active stations.

-Listed the stations and observation counts in descending order.

-Determined which station had the highest number of observations.

-Designed a query to retrieve the last 12 months of temperature observation data (TOBS).

-Filtered by the station with the highest number of observations.

-Ploted the results as a histogram with bins=12.



Climate App

-Used Flask to create the following routes.

/

Home page.

-Lists all routes that are available.


/api/v1.0/precipitation

-Converts the query results to a dictionary using date as the key and prcp as the value.

-Returns the JSON representation of your dictionary.


/api/v1.0/stations

-Returns a JSON list of stations from the dataset.


/api/v1.0/tobs

-Queries the dates and temperature observations of the most active station for the last year of data.

-Return a JSON list of temperature observations (TOBS) for the previous year.


/api/v1.0/<start> and /api/v1.0/<start>/<end>

-Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

-When given the start only, calculates TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

-When given the start and the end dates, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.