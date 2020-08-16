#Flask dependencies
from flask import Flask, jsonify, render_template

#Other dependencies
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
#data and date manipulation libraries
import numpy as np
import pandas as pd
import datetime as dt

#connection_string
connection_string = "postgres:postgres@localhost:5432/ETL_Rental_DB"

def postgres_create_session(connection_string):
    #####This functions create all the background functions for a successful connections to the db
    #####and returns a session class, mapped classes
    #Create an engine to the hawaii.sqlite database
    engine = create_engine(f'postgresql://{connection_string}', echo=True)
    # reflect an existing database into a new model; reflect the tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Save references to each table
    Rental = Base.classes.Rental
    Income = Base.classes.Income
    Crime = Base.classes.Crime
    Community_Assets = Base.classes.Community_Assets
    Bridge_Rental_Crime = Base.classes.Bridge_Rental_Crime

    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    return session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime
    #####This functions create all the background functions for a successful connections to the db
    #####and returns a session class, mapped classes
    #Create an engine to the hawaii.sqlite database
    engine = create_engine(f'postgresql://{connection_string}', echo=True)
    # reflect an existing database into a new model; reflect the tables
    Base = automap_base()
    Base.prepare(engine, reflect=True)

    # Save references to each table
    Rental = Base.classes.Rental
    Income = Base.classes.Income
    Crime = Base.classes.Crime
    Community_Assets = Base.classes.Community_Assets
    Bridge_Rental_Crime = Base.classes.Bridge_Rental_Crime

    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
    return session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime 

def listings(session,Rental, count=100):
    ####This function retrieves the "count" of listings upto 100 of data from the Measurement class
    ####Returns a dictionary with key as 1, 2,3 etc and value as another dictionary with limited rental details 
    

    ### Design a query to retrieve the "count" no of listings
    rental_listing = session.query(Rental.id, Rental.title, Rental.price, Rental.image, Rental.url, Rental.bedrooms, Rental.rental_type, Rental.source, Rental.sqft).filter().order_by(Rental.post_published_date).limit(count)
    rental_listing_DF = pd.DataFrame(rental_listing)

    #Convert the DF to a dictionary
    rental_listing_dict = rental_listing_DF.T.to_dict()
    return rental_listing_dict    

def comm_services(session,Community_Assets, count=100):
    ####This function retrieves the "count" of comm_services upto 100 of data from the Community_Assets class
    ####Returns a dictionary with key as 1, 2,3 etc and value as another dictionary with limited rental details 
    
    #limit count to 100
    count = 100 if count>100 else max(count,1)
    ### Design a query to retrieve the "count" no of services
    service_listing = session.query(Community_Assets.id, Community_Assets.agency_name, Community_Assets.e_mail, Community_Assets.fees, Community_Assets.hours, Community_Assets.application,  Community_Assets.category, Community_Assets.address, Community_Assets.crisis_phone).limit(count)
    servicel_listing_DF = pd.DataFrame(service_listing)

    #Convert the DF to a dictionary
    servicel_listing_dict = servicel_listing_DF.T.to_dict()
    return servicel_listing_dict   

def crime_details(session,Crime, Type="Assault"):
    ####This function retrieves all the crime data in the last year based on type
    #["assault", "auto theft", "break and enter", "robbery" ,'Homicide', and "theft over"]
  
    Type = "Assault" if Type not in ['Assault', 'Auto Theft', 'Break and Enter', 'Theft Over','Robbery', 'Homicide'] else Type
    

    ### Design a query to retrieve all the crime data based on type
    crime_listing = session.query(Crime.MCI, Crime.occurrencedate, Crime.reporteddate, Crime.offence, Crime.neighbourhood).filter(Crime.MCI==Type).order_by(Crime.occurrencedate)
    crime_listing_DF = pd.DataFrame(crime_listing)

    #Convert the DF to a dictionary
    crime_listing_dict = crime_listing_DF.T.to_dict()
    return crime_listing_dict


def income_details(session,Income):
    ####This function retrieves the income details for all FSA in Toronto
    

    ### Design a query to retrieve all the income data for all FSA in Toronto
    fsa_income = session.query(Income.FSA, Income.avg_income)
    fsa_income_DF = pd.DataFrame(fsa_income)

    #Convert the DF to a dictionary
    fsa_income_dict = fsa_income_DF.T.to_dict()
    return fsa_income_dict   

    

#Create app
app = Flask(__name__)

#Create routes
@app.route('/')
def home_page():
    return render_template('index.html', name='home_page')

@app.route('/rental/<count>')
def rental(count):
    print("GET request at rental")
    
    try:
        #limit count to 100
        count = int(count)
        #limit count to 100
        count = 100 if count>100 else max(count,1)
    except:
        print("Enter a number; We limit the listing as 100")
        return "Server is not able to respond. Please try after some time", 404

    try:
        session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime = postgres_create_session(connection_string)
        rental_listing_dict = listings(session,Rental, count)
        ### Close the session
        session.close()
    except:
        ### Close the session
        session.close()
        return "Server is not able to respond. Please try after some time", 404
    return jsonify(rental_listing_dict)

@app.route('/community/<count>')
def community(count):
    print("GET request at community")
    try:
        #limit count to 100
        count = int(count)
        #limit count to 100
        count = 100 if count>100 else max(count,1)
    except:
        print("Enter a number; We limit the listing as 100")
        return "Server is not able to respond. Please try after some time", 404
    try:
        #limit count to 100
        count = int(count)
        #limit count to 100
        count = 100 if count>100 else max(count,1)
    except:
        print("Enter a number; We limit the listing as 100")

    try:
        session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime = postgres_create_session(connection_string)
        servicel_listing_dict  = comm_services(session,Community_Assets, count)
        ### Close the session
        session.close()
    except:
        ### Close the session
        session.close()
        return "Server is not able to respond. Please try after some time", 404
    return jsonify(servicel_listing_dict)

@app.route('/crime/<type>')
def crime(type):
    print("GET request at crime")
    try:
        type=type.capitalize()
        assert type in ['Assault', 'Auto Theft', 'Break and Enter', 'Theft Over',
       'Robbery', 'Homicide']
    except:
        print("Enter a type as 'Assault', 'Auto Theft', 'Break and Enter', 'Theft Over','Robbery', 'Homicide'")
        print("We are showing results of Assault")

    try:
        session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime = postgres_create_session(connection_string)
        crime_listing_dict = crime_details(session,Crime, type)
        ### Close the session
        session.close()
    except:
        ### Close the session
        session.close()
        return "Server is not able to respond. Please try after some time", 404
    return jsonify(crime_listing_dict)

@app.route('/income/')
def income():
    print(f"GET request at income")
    try:
        session, Rental, Income, Crime, Community_Assets, Bridge_Rental_Crime = postgres_create_session(connection_string)
        fsa_income_dict = income_details(session,Income)
        ### Close the session
        session.close()
    except:
        ### Close the session
        session.close()
        return "Server is not able to respond. Please try after some time", 404
    return jsonify(fsa_income_dict)

if __name__== "__main__":
    #app.run(threaded=True, debug=True, port=5000)
    app.run(debug=True, threaded=True, port=5000)
