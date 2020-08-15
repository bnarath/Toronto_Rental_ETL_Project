import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime, timedelta

from flask import Flask, jsonify

#database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the database 
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save table references 
measurement_table = Base.classes.measurement
station_table = Base.classes.station

# Flask Setup
app = Flask(__name__)

#Flask routes

     #base route
@app.route("/")
def welcome():
    print("request for welcome page")

    # Calculate the date 1 year ago from the last data point in the database

    session = Session(engine)

    newestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.desc()).first()

    newest_date = datetime.strptime(newestdate_query[0], "%Y-%m-%d").date()

    edge_date = newest_date - timedelta(days=365)

    session.close()   

    return (
        f"""
        <head>
            <meta charset = "UTF-8"> 
            <title> Climate API </title>
        </head>
        <body>
            <H1> Welcome to the Climate API </H1>
            <hr>
            <H2>Available Routes</H2>
            <ul> 
                <li> <b> Precipitation data for previous year ({edge_date} to {newest_date}): </b> /api/v1.0/precipitation </li> <br/>
                <li> <b> Stations list: </b> /api/v1.0/stations </li> <br/>
                <li> <b> Most active station's temperature observations(TOBS) for previous year ({edge_date} to {newest_date}): </b> /api/v1.0/tobs </li type="circle"> <br/>
                <li> <b> Max, min and avg temperature observations based on specified dates: </b> </li>
                <li type="square"> specify start date(yyyy-mm-dd):  /api/v1.0/&lt;startdate&gt <br/>  </li type="square"> 
                <li type="square"> specify date range(yyyy-mm-dd/yyyy-mm-dd):  /api/v1.0/&lt;startdate&gt/&lt;enddate&gt </li type="square"> 
            </ul> 
        </body>
        """
    )


      #prec route
@app.route("/api/v1.0/precipitation")
def prec():
    print("request for precipitation data")

    # Create session 
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database

    newestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.desc()).first()

    newest_date = datetime.strptime(newestdate_query[0], "%Y-%m-%d").date()

    edge_date = newest_date - timedelta(days=365)

    """Return a list of dates and associated precipitation obs for last year"""
    # Query the last 12 months of precipitation data. 
    results_prec = session.query(measurement_table.date, measurement_table.prcp).\
                      filter(measurement_table.date>=edge_date).\
                      all()

    session.close()

    # Create a dictionary from the row data and append to a list of rows
    prec_data= []
    for row in results_prec:
        prep_dict = {row[0]:row[1]}
        prec_data.append(prep_dict)
    
    return jsonify(prec_data)


      #stat route
@app.route("/api/v1.0/stations")
def stat():
    print("request for station list")

    # Create session 
    session = Session(engine)
    
    """Return a list of stations and associated data"""
    # Query the stations 
    results_stat = session.query(station_table.station).all()

    session.close()

    # convert into list
    stat_data= list(np.ravel(results_stat))
    
    return jsonify(stat_data)

#tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    print("request for temp data by date for most active station")

    # Create session 
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database

    newestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.desc()).first()

    newest_date = datetime.strptime(newestdate_query[0], "%Y-%m-%d").date()

    edge_date = newest_date - timedelta(days=365)


    #identify most active station
    most_active = session.query(measurement_table.station,
                          func.count(measurement_table.station)).\
                          group_by(measurement_table.station).\
                          order_by((func.count(measurement_table.station).desc())).\
                          first()

    """Return a list of dates and associated temp obs for last year"""
    # Query the last 12 months of temp data by date for most active station 
    results_tobs = session.query(measurement_table.date, measurement_table.tobs).\
                      filter(measurement_table.station == most_active[0]).\
                      filter(measurement_table.date>=edge_date).\
                      all()

    session.close()

    # Create a dictionary from the row data and append to list
    tobs_data= []

    for row in results_tobs:
        tobs_dict = {}
        tobs_dict["date"] = row[0]
        tobs_dict["temperature"] = row[1]
        tobs_data.append(tobs_dict)
    
    return jsonify(tobs_data)


#route - sum temp data based on start date 
@app.route("/api/v1.0/<startdate>")
def start_date_sum_temp(startdate):
    print("request for summary temp data based on specified start date")

    # Create session 
    session = Session(engine)

    # Identify earliest date in dataset

    earliestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.asc()).first()

    earliest_date = datetime.strptime(earliestdate_query[0], "%Y-%m-%d")

    #evaluate whether dates provided in correct format/convert from string to date
    try:
        start_date = datetime.strptime(startdate, "%Y-%m-%d")
    except:
        return ("error: required date format is /api/v1.0/yyyy-mm-dd")

    if start_date < earliest_date:
        return (f"error: earliest date in dataset is {earliest_date}")
    
    #run query
    else:
        results_sum_temp = session.query(func.min(measurement_table.tobs),
                        func.max(measurement_table.tobs),
                        func.avg(measurement_table.tobs)).\
                        filter(measurement_table.date >= start_date).all()  
    
         # convert into list
        temp_sum_data= list(np.ravel(results_sum_temp))
    
        return jsonify(temp_sum_data)

    session.close()

#route - sum temp data based on start and end dates 
@app.route("/api/v1.0/<startdate>/<enddate>")
def start_and_end_date_sum_temp(startdate, enddate):
    print("request for summary temp data based on specified start and end date")

    # Create session 
    session = Session(engine)

    # Identify earliest date in dataset

    earliestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.asc()).first()

    earliest_date = datetime.strptime(earliestdate_query[0], "%Y-%m-%d")

    # Identify earliest date in dataset

    latestdate_query = session.query(measurement_table.date).\
                                 order_by(measurement_table.date.desc()).first()

    latest_date = datetime.strptime(latestdate_query[0], "%Y-%m-%d")

    #evaluate whether dates provided in correct format/convert from string to date

        #start date
    try:
        start_date = datetime.strptime(startdate, "%Y-%m-%d")
    except:
        return ("error: required date format is /api/v1.0/yyyy-mm-dd")
    
        #end date
    try:
        end_date = datetime.strptime(enddate, "%Y-%m-%d")
    except:
        return ("error: required date format is /api/v1.0/yyyy-mm-dd")

    #evaluate whether dates provided within interval available in database

    if start_date < earliest_date:
        return (f"error: earliest date in dataset is {earliest_date}")

    elif end_date > latest_date:
        return (f"error: latest date in dataset is {latest_date}")
    
    #run query
    else:
        results_sum_temp = session.query(func.min(measurement_table.tobs),
                        func.max(measurement_table.tobs),
                        func.avg(measurement_table.tobs)).\
                        filter(measurement_table.date.between (start_date, end_date)).all()  
    
         # convert into list
        temp_sum_data= list(np.ravel(results_sum_temp))
    
        return jsonify(temp_sum_data)

    session.close()

if __name__ == "__main__":
    app.run(debug=True)
