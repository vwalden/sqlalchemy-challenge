# Import dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create app
app = Flask(__name__)


# Index route: List all available api routes
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1/tobs<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )


# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query precipitation data & close session
    result_year=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > '2016-08-23').order_by(Measurement.date).all()
    session.close()
    
    # Convert list of tuples into normal list
    prcp_year = list(np.ravel(result_year))
    
    # Return JSON representation
    return jsonify(prcp_year)

    
# Temperature route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query precipitation data & close session
    result_temp=session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23', Measurement.station == 'USC00519281').order_by(Measurement.date).all()
    session.close()
    
    # Convert list of tuples into normal list
    temp_year = list(np.ravel(result_temp))
    
    # Return JSON representation
    return jsonify(temp_year)


# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query precipitation data & close session
    result_list=session.query(Measurement.station).distinct().order_by(Measurement.station).all()
    session.close()
    
    # Convert list of tuples into normal list
    station_list = list(np.ravel(result_list))
    
    # Return JSON representation
    return jsonify(station_list)


# Start route
@app.route("/api/v1.0/start")
def start():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query precipitation data & close session
    result_tmin=session.query(func.min(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').scalar()
    result_tmax=session.query(func.max(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').scalar()
    result_tavg=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-23').scalar()
    session.close()
    
    # Create dictionary of the query data
    summary_temp = {'min': result_tmin, 'max': result_tmax, 'avg': result_tavg}
    
    # Return JSON representation
    return jsonify(summary_temp)


# End route
@app.route("/api/v1.0/start/end")
def end():
     # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query precipitation data & close session
    result_rmin=session.query(func.min(Measurement.tobs)).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').scalar()
    result_rmax=session.query(func.max(Measurement.tobs)).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').scalar()
    result_ravg=session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= '2016-08-23', Measurement.date <= '2017-08-23').scalar()
    session.close()
    
    # Create dictionary of the query data
    summary_rtemp = {'min': result_rmin, 'max': result_rmax, 'avg': result_ravg}
    
        # Return JSON representation
    return jsonify(summary_rtemp)


if __name__ == '__main__':
    app.run(debug=True)