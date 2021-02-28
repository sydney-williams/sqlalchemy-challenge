import numpy as np
import pandas as pd

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurements = base.classes.measurement
stations = base.classes.station

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
    "List all available api routes."
    test = (
        f"Welcome to the Honolulu, Hawaii climate and weather exploration and analysis page!<br/>"
        f"Available Routes:<br/>"
        f"Precipitation/api/v1.0/precipitation<br/>"
        f"List of stations/api/v1.0/stations<br/"
        f"Temperature/api/v1.0/tobs<br/"
        f"Temperature Start and End/api/v1.0/temp/start/end")
    return (test)

#precipitation information 
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session (link) from Python to the DB
    # session = Session(engine)
    ##return the precipitation data for the last year
    ##calculate the date 1 yr ago from the last yr
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    #create a query of the precipitation data and dates
    precipitation = session.query(measurements.date, measurements.prcp).\
        filter(measurements.date >= prev_year).all()

    ##calculate the date 1 yr ago from the last yr
    #create a precipitation dictionary
    for date, prcp in precipitation:
        precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#stations information
@app.route("/api/v1.0/stations")
def stations():
    #create session (link) from Python to the DB
    # session = Session(engine)
    ##return a list of stations
    #create a query of the stations 
    results = session.query(stations.station).all()

    ##unravel stations into a 1D array and convert to a list
    stations_all = list(np.ravel(results))

    return jsonify(stations_all = stations)
