# Set up Flask Weather APP
import flask

## Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

## Set up the Database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
## Reflect the DB
Base.prepare(engine, reflect=True)
## Save our references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
## Create session link from Py to our DB
session = Session(engine)

### Set up Flask

### Define flask app
app = Flask(__name__)
### Define welcome route
@app.route("/")
### Create welcome() function then add precip, stations, tobs, and temp routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

#### Create Precipitation Route
@app.route("/api/v1.0/precipitation")
#### Precip function - calculate date one year ago from most recent date in DB - then query the data and precip
#### Then Create a dictionary with the date as a key and precip as the value
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

##### Stations Route
@app.route("/api/v1.0/stations")
##### Create function called stations
def stations():
##### Add query to get all stations in our DB, then unravel our results into a one-dimensional array using np.unravel
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

###### Monthly Temp Route
###### Create route then calculate date one year ago from last date in DB - then query primary station for all temps on prev year
###### Unravel results into 1-D array - then jsonify the list and return results
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

####### Stats route
####### add parameters to our stats function, create a list called SEL for the min, avg and max temps
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)
