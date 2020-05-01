# Project   : This Flask server will get data from the json and send it to React Frontend
# Author    : Shobhit Gupta
# Date      : 1st May 2020

# importing the libraries
import pandas as pd
import numpy as np 
from flask import Flask
import os
import json
from datetime import datetime
import regex as re
from flask_cors import CORS, cross_origin


# initilising the app
app = Flask(__name__)

# enabling CORS in the application
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# reading the data from the json
df_rows = []
folder = os.fsencode('./data/')
for file in os.listdir(folder):
  filename = os.fsdecode(file)
  if filename.endswith('.json'):
    filename = os.fsdecode(folder)+filename
    with open(os.fsdecode(filename), mode='r') as json_file:
      data = json.load(json_file)
      df_rows.append(data)

# This dataframe contains all the data of the 1000 JSONs
newDF = pd.DataFrame(df_rows)


@app.route("/", methods = ["GET","POST"])
@cross_origin()
def root():

    return "Try the path /get_data to get the data"


@app.route('/get_data', methods = ['GET', 'POST'])
@cross_origin()
def get_data():

    # giving starting and ending year values
    start_year = 2000
    end_year = 2019

    # list of years in the list
    year_list = [year for year in range(start_year,end_year+1)]

    # creating a dictionary with year as keys and count and titles as data elements
    year_data = { year:{'count':0,'titles':[]} for year in year_list}

    # iterating through the wiki data and increasing the count and appending titles
    for i, (row_id, row) in enumerate(newDF.iterrows()):

        year = datetime.strptime(row['time_published'], '%Y-%m-%dT%H:%M:%SZ').year

        # if the current year is present in the year range
        if year in year_data.keys():
            year_data[year]["count"] += 1 #increasing the count
            year_data[year]["titles"].append(row['title'])

    # separating the count and titles to be plotted
    title_counts = [value['count'] for value in year_data.values()]

    titles = [value['titles'] for value in year_data.values()]

    # sending the years and counts for graph plotting
    data = {'labels':year_list, 'counts':title_counts}

    data_json = json.dumps(data)

    return data_json

if __name__ == "__main__":
    app.run(debug = True, port = 2010)
