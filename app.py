import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement= Base.classes.measurements
Station= Base.classes.stations
session= Session(engine)

app= Flask(__name__)

@app.route("/")
def home():
    return(
        f"Home page"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/measurements<br/>"
        f"/api/v1.0/stations"
    )

@app.route("/api/v1.0/precipitation")
def precipitaion():
    result= session.query(Measurement.date, Measurement.prcp).all()
"""Dictionary"""
    precip = []
    for date, prcp in result:
        precip_dict= {}
        precip_dict["date"]= date
        precip_dict["prcp"]= prcp
        all_precip.append(precip_dict)
    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Satation.name).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    results= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()
    return jsonify(results)

@app.route("/api/v1.0/<start>")
def tobs():
    return jsonify(results)

@app.route("api/v1.0/<start>/<end>")
def tobs():
    return jsonify(results)

if__name__== "__main__":
    app.run(debug=True)
