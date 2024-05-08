# sqlalchemy challenge

In this assignment challenge, I use SQLAlchemy to connect to a SQLite database containing climate data to perform various analyses. Additionally, I designed a Flask API to return various queries from the SQLite database. This assignment challenge is divided into two parts:

## Part 1: Analyzing and Exploring the Climate Data
I analyzed weather data for precipitation (prcp) and temperature observations (tobs) across different stations. The analysis involved converting queried results from the ORM (Object Relational Mapper) to pandas dataframes and plotting the results. This part was completed using Jupyter Notebook, and the code is contained in the file named 'climate.ipynb'.

## Part 2: Designing a Climate App
In this part, a Flask API was designed to handle both static and dynamic routes for queried climate data. The code for the app design is contained in the 'app.py' file.

For static routes, the following endpoints were created:

- **Precipitation Route**: Returns JSON-formatted data with the date as the key and the precipitation value for the last 12 months.
- **Stations Route**: Provides data for all weather stations in the database.
- **TOBs Route**: Retrieves data for the most active station over the last 12 months.

For dynamic routes, the following endpoints were implemented:

- **Start Route**: Accepts the start date as a parameter from the URL and calculates the minimum, maximum, and average temperatures from the given start date to the end of the dataset.
- **Start/End Route**: Accepts both the start and end dates as parameters from the URL and calculates the minimum, maximum, and average temperatures from the given start date to the given end date.

**Please note**: For dynamic routes, the specified dates must be typed in this format DD-MM-YYYY in place of &lt;start&gt; and &lt;end&gt;
- Example 1: `/api/v1.0/10-05-2015`
- Example 2: `/api/v1.0/15-07-2010/20-09-2016`

## Source of Data
The data for this assignment challenge was provided by EdX LLC. The dataset covers the period from 01-01-2010 to 23-08-2017. All data files are contained in the 'Resources' folder inside the 'Surfsup' directory.

## Folders and Files
- `Surfsup`
  - `climate.ipynb`
  - `app.py`
  - `Resources`
    - `hawaii.sqlite`
    - `hawaii_measurements.csv`
    - `hawaii_stations.csv`
