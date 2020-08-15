import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from datetime import datetime, timedelta

from flask import Flask, jsonify

#database setup
engine = create_engine("REF")

# reflect the database 
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save table references 
Rental = Base.classes.Rental
Community_Asset = Base.classes.Community_Assets
Crime = Base.classes.Crime
Income = Base.classes.Income

# Flask Setup
app = Flask(__name__)

#Flask routes

     #base route
@app.route("/")
def welcome():
    print("request for welcome page")

    return (
        f"""
        <head>
            <meta charset = "UTF-8"> 
            <title> Rental API </title>
        </head>
        <body>
            <H1> Welcome to the Toronto Rental API </H1>
            <hr>
            <H2>Available Routes</H2>
            <ul> 
                <li> <b> Community Services: </b> /api/v1.0/community_assets/<first three digits of postal code> </li> <br/> 
                <li> <b> Average Incomes: </b> /api/v1.0/average_income/<first three digits of postal code> </li> <br/> 
            </ul> 
        </body>
        """
    )


      #community asset route
@app.route("/api/v1.0/community_assets/<Forward_Sortation_area>")
def CA():
    print("request for community asset data by FSA")

    # Create session 
    session = Session(engine)

    fsa_community_asset_query = session.query(Community_Assets).filter(Community_Assets.fsa == 'Forward_Sortation_area').all()

    session.close()

    # Create a dictionary from the row data and append to a list of rows

    fsa_community_asset = 
    
    return jsonify(fsa_community_asset)

     #community asset route
@app.route("/api/v1.0/average_income/<Forward_Sortation_area>")
def AI():
    print("request for average income data by FSA")

    # Create session 
    session = Session(engine)

    try:
        fsa_average_income_query = session.query(Income).filter(Income.fsa == 'Forward_Sortation_area').all()

    except:
        return ("error: required date format is /api/v1.0/xxx where xxx is the first three digits of teh postal code")

    session.close()

    # Create a dictionary from the row data and append to a list of rows
    
    fsa_average_income = 

    return jsonify(fsa_average_income)


      #rental listings route
@app.route("/api/v1.0/rental_listings/<Forward_Sortation_area>")
def RL():
    print("request for rental listing data by FSA")

    # Create session 
    session = Session(engine)

    fsa_rental_listings_query = session.query(Rental).filter(Rental.fsa == 'Forward_Sortation_area').all()

    session.close()

        # Create a dictionary from the row data and append to a list of rows
    
    fsa_rental_listings = 

    return jsonify(fsa_rental_listings)


if __name__ == "__main__":
    app.run(debug=True)
