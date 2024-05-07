# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
from sqlalchemy import and_
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
        "Welcome to the Weather API of Hawaii!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date/2010-01-01<br/>"  
        "/api/v1.0/start_and_end_date/2016-08-10/2017-08-18<br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as a dictionary with date as the key and a single dictionary of stations and their precipitation values as the value."""
    # Calculate the date one year from the last date in the data set.
    last_date = session.query(func.max(Measurement.date)).scalar()
    query_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Perform a query to join 'measurement' and 'station' tables on their 'station' columns
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
@app.route("/api/v1.0/start_date/<start_date>")

def temperature_stats_with_start_date(start_date='2010-01-01'):
    """Return a JSON list of the minimum, average, and maximum temperature for the specified start date and most active station USC00519281"""
    station_id = 'USC00519281'

    # Convert the input start_date string to a datetime object
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()

    # Query to calculate temperature statistics from the specified start date to the last date in the date column
    temps_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(and_(Measurement.station == station_id, Measurement.date >= start_date)).all()

    # Extract the temperature statistics from the query result
    min_temp, max_temp, avg_temp = temps_query[0]

    # Create a dictionary to hold the temperature statistics
    temp_stats = {'start_date': start_date.strftime("%Y-%m-%d"),
                  'station_id': station_id,
                  'min_temp': min_temp,
                  'max_temp': max_temp,
                  'avg_temp': avg_temp}

    return jsonify(temp_stats)


@app.route("/api/v1.0/start_date/<start_date>")
def temperature_with_start_date(start_date='2010-01-01'):
    """Return a JSON list of the minimum, average, and maximum temperature for the specified start date and most active station USC00519281"""
    station_id = 'USC00519281'

    # Convert the input start_date string to a datetime object
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()

    # Query to calculate temperature statistics from the specified start date to the last date in the date column
    temps_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(and_(Measurement.station == station_id, Measurement.date >= start_date)).all()

    # Extract the temperature statistics from the query result
    min_temp, max_temp, avg_temp = temps_query[0]

    # Create a dictionary to hold the temperature statistics
    temp_stats = {'start_date': start_date.strftime("%Y-%m-%d"),
                  'station_id': station_id,
                  'min_temp': min_temp,
                  'max_temp': max_temp,
                  'avg_temp': avg_temp}

    return jsonify(temp_stats)

@app.route("/api/v1.0/start_and_end_date/<start_date>/<end_date>")
def temperature_stats_with_start_and_end_date(start_date='2016-08-10', end_date='2017-08-18'):
    """Return a JSON list of the minimum, average, and maximum temperature for the specified start and end dates and most active station USC00519281"""
    station_id = 'USC00519281'

    # Convert the input start_date and end_date strings to datetime objects
    start_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = dt.datetime.strptime(end_date, "%Y-%m-%d").date()

    # Query to calculate temperature statistics for the specified start and end dates and the most active station
    temps_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(and_(Measurement.station == station_id, Measurement.date >= start_date, Measurement.date <= end_date)).all()

    # Extract the temperature statistics from the query result
    min_temp, max_temp, avg_temp = temps_query[0]

    # Create a dictionary to hold the temperature statistics
    temp_stats = {'start_date': start_date.strftime("%Y-%m-%d"),
                  'end_date': end_date.strftime("%Y-%m-%d"),
                  'station_id': station_id,
                  'min_temp': min_temp,
                  'max_temp': max_temp,
                  'avg_temp': avg_temp}

    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)