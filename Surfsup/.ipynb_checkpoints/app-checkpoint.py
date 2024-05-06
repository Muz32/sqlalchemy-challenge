# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np
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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as a dictionary with date as the key and prcp as the value."""
    # Calculate the date one year from the last date in data set.
    last_date = dt.date(2017, 8, 23)
    query_date = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()

    # Convert the query results to a dictionary with date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in results}

    return jsonify(precipitation_dict)

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
     
if __name__ == "__main__":
    app.run(debug=True)