# sqlalchemy-challenge
In this assignemnt challenge I use sql alchemy to connect to a sqlite database on climate data to undertake various analysis. I also designed a flask API to return various quiries from the sqlite database. This assignment challenge is divided into two parts:

## Part 1 Analysing and Exploring the Climate Data
I analysed weather data for precipitation (prcp) and temperature observations (tobs) for different stations. The analysis included converting queried results from the ORM (Object Relational Mapper) to pandas dataframes and plotting of results. The analysis in this part was done using jupyter notebook. The jupyter notebook file is contained in the folder'Surfsup'with the file name 'climate.ipynb'. 

## Part 2 Part 2: Design Your Climate App
In this part, a Flask API was designed to handle both static and dynamic routes for queried climate data.

For static routes, the following endpoints were created:

- **Precipitation Route**: Returns JSON data with the date as the key and the precipitation value for the last 12 months.

- **Stations Route**: Provides data for all weather stations in the database.

- **TOBs Route**: Retrieves data for the most active station in the last 12 months.

For dynamic routes, the following endpoints were implemented:

- **Start Route**: Accepts the start date as a parameter from the URL and calculates the minimum, maximum, and average temperatures from the given start date to the end of the dataset.

- **Start/End Route**: Accepts both the start and end dates as parameters from the URL calculates the minimum, maximum, and average temperatures from the given start date to the given end date.

**Please note** For dynamic routes, the specified dates must be typed in this format DD-MM-YYYY.
        -Example 1: /api/v1.0/start_date/10-05-2015.
        -Example 2: /api/v1.0/start_date_and_end_date/15-07-2010/20-09-2016.
    
## Source of data
The data for this assignemnt challenge was provided by EdX LLC. The dataset covers the period from 01-01-2010 to 23-08-2017. All data files are contained in the Resources folder inside the 'Surfup' folder. 

## Folders and Files
- `Surfsup`
  - `climate.ipynb`
  - `app.py`
   - `Resources`
     - `hawaii.sqlite`
     - `hawaii_measurements.csv`
     - `hawaii_stations.csv`
    
