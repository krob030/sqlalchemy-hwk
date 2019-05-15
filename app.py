import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement= Base.classes.measurement
Station= Base.classes.station
session= Session(engine)

app= Flask(__name__)

@app.route("/")
def home():
    return(
        f"Home page"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    results= session.query(Measurement.date, Measurement.prcp).all()
    all_precip= []
    for date, prcp in results:
        precip_dict= {}
        precip_dict["date"]= date
        precip_dict["prcp"]= prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    station_list= list(np.ravel(results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results= session.query(Measurement.tobs).filter(Measurement.date >= prev_year).all()
    date_tobs= list(np.ravel(results))
    return jsonify(date_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    calc_startend= list(np.ravel(results))
    return jsonify(calc_startend)

if __name__== "__main__":
    app.run(debug=True)