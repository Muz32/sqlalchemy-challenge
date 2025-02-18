# Import the dependencies

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<h1><strong>Welcome to the Weather API for Hawaii!</strong></h1><br/><br/>"
        
        f"<strong>Available API Static Routes:</strong><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        
        f"<strong>Available API Dynamic Routes:</strong><br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"  
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/><br/>"
        
        f"<strong>Note:</strong><br/>"
        f"The dynamic routes return minimum, maximum, and average temperatures for inputted dates. " 
        f"The specified dates must be typed in this format DD-MM-YYYY in place of &lt;start&gt; and &lt;end&gt;.<br/>"
        f"Example 1: /api/v1.0/10-05-2015 <br/>Example 2: /api/v1.0/15-07-2010/20-09-2016 <br/>"
        f"The dataset covers the period from 01-01-2010 to 23-08-2017.<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as a dictionary with date as the key and a single dictionary of stations and their precipitation values as the value."""
    # Calculate the date one year from the last date in the data set.
    last_date = session.query(func.max(Measurement.date)).scalar()
    query_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Perform a query to join 'measurement' and 'station' classes with their 'station' attribute (column)
    query_result = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
        join(Station, Measurement.station == Station.station).\
        filter(Measurement.date >= query_date).all()

    # Convert the query results to a dictionary with date as the key and a single dictionary of stations and their precipitation values as the value
    precipitation_dict = {}
    for station, date, prcp in query_result:
        if date not in precipitation_dict:
            precipitation_dict[date] = {'Stations': {}, 'Date': date}
        if station not in precipitation_dict[date]['Stations']:
            precipitation_dict[date]['Stations'][station] = prcp

    # Sort the precipitation_dict by date in descending order
    sorted_precipitation_dict = dict(sorted(precipitation_dict.items(), key=lambda x: x[0]))

    return jsonify(list(sorted_precipitation_dict.values()))


@app.route("/api/v1.0/stations")
def stations():
    """Return all stations and their names"""
    # Query all stations from the 'stations' class
    stations_data = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations_list = []
    for station in stations_data:
        station_dict = {}
        station_dict['station'] = station.station
        station_dict['name'] = station.name
        stations_list.append(station_dict)

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def temperature_observations():
    """Return temperature observations of the most active station for the previous year"""
    # Query to find the most active station and its count of temperature observations
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    if most_active_station:
        most_active_station_id = most_active_station[0]

        # Calculate the date one year from the last date in the dataset
        last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
        last_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d").date()
        query_date = last_date - dt.timedelta(days=365)

        # Query date and temperature observations for the most active station within the last 12 months
        temperature_data = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.station == most_active_station_id).\
            filter(Measurement.date >= query_date).all()

        # Convert the query results to a list of dictionaries
        tobs_list = []
        for date, tobs in temperature_data:
            tobs_dict = {}
            tobs_dict['date'] = date
            tobs_dict['tobs'] = tobs
            tobs_list.append(tobs_dict)
        
        return jsonify({"Most Active Station": most_active_station_id, "Temperature Observations (tobs)": tobs_list})
    else:
        return jsonify({"message": "No data found."}), 404


@app.route("/api/v1.0/<start>")
def temperature_with_start_date(start):
    """Return a JSON list of temperature statistics for all stations within the specified start date range."""

    #Convert the input 'start' date string to a datetime object with format DD-MM-YYYY
    start = dt.datetime.strptime(start, "%d-%m-%Y").date()

    # Query to calculate temperature statistics for all stations within the specified start date range
    temps_query = session.query(Station.name, Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        join(Measurement, Measurement.station == Station.station).\
        filter(Measurement.date >= start).\
        group_by(Station.name, Measurement.station).all()

    # Create a list to hold the temperature statistics for the different stations
    temp_stats_list = []
    for station_name, station_id, min_temp, max_temp, avg_temp in temps_query:
        temp_stats = {'station_name': station_name,
                      'station_id': station_id,
                      'min_temp': min_temp,
                      'max_temp': max_temp,
                      'avg_temp': avg_temp}
        temp_stats_list.append(temp_stats)

    # Convert the start date datetime object back to a string in a desired format when displaying output
    formatted_start = start.strftime("%d %B, %Y")

    #Display output in json format
    return jsonify(f"Specified Start Date is {formatted_start}", temp_stats_list)


@app.route("/api/v1.0/<start>/<end>")
def temperature_stats_with_start_and_end_date(start, end):
    """Return a JSON list of temperature statistics for different stations within the specified start and end dates."""
    
    #Convert the input 'start' and 'end' date strings to datetime objects with format DD-MM-YYYY
    start = dt.datetime.strptime(start, "%d-%m-%Y").date()
    end = dt.datetime.strptime(end, "%d-%m-%Y").date()

    # Query to calculate temperature statistics for the specified start and end dates for all stations
    temps_query = session.query(Station.name, Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        join(Measurement, Measurement.station == Station.station).\
        filter(and_(Measurement.date >= start, Measurement.date <= end)).\
        group_by(Station.name, Measurement.station).all()

    # Create a list to hold the temperature statistics for the different stations
    temp_stats_list = []
    for station_name, station_id, min_temp, max_temp, avg_temp in temps_query:
        temp_stats = {'station_name': station_name,
                      'station_id': station_id,
                      'min_temp': min_temp,
                      'max_temp': max_temp,
                      'avg_temp': avg_temp}
        temp_stats_list.append(temp_stats)
    
    # Convert the start date datetime object back to a string in a desired format when displaying output
    formatted_start = start.strftime("%d %B, %Y")
    formatted_end = end.strftime("%d %B, %Y")
    
    #Display output in json format
    return jsonify(f"Specified Start Date is {formatted_start} and Specified End Date is {formatted_end}",temp_stats_list)


if __name__ == "__main__":
    app.run(debug=True)