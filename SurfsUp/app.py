# Import the dependencies.

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# 2. Create an app

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB

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
        f"/api/v1.0/start_date/<start><br/>"
        f"/api/v1.0/startend/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
     # Calculated the recent date and using that date calculating the previous 12 months of precipitation data 
    recent_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Performed a query to retrieve the data and precipitation scores
    last_twelve_months = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()

    session.close()


@app.route("/api/v1.0/stations")
def stations():

    # Getting a list of stations
    station_list= session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    session.close()


@app.route("/api/v1.0/tobs")
def tobs():
    
    # Querying the dates and temperature observations of the most-active station for the previous year of data
    max_temp_last_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    
    query_date = dt.date(2017, 8 ,23) - dt.timedelta(days=365)
    
    # calculating tobs and a date from 12 months ago
    results_tobs_date = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= query_date).\
        order_by(Measurement.date.desc()).all()
    
    session.close()

@app.route("/api/v1.0/start_date/<start>")
def start_date(start):
    
    # calculating TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date
    results_start = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start)
    
    session.close()


@app.route("/api/v1.0/startend/<start>/<end>")
def startend(start,end):
    
    # calculating TMIN, TAVG, and TMAX for the dates from the start date to the end date
    results_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    
    return jsonify(t_normals)
if __name__ == '__main__':
    app.run(debug=True)

