# Import Deps
import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px 

# Data source https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv

def extract_subarea(place):
    return place[0]

def extract_area(place):
    return place[1]

# Fetch data and clean
def fetch_eq_data(period='daily', region='Worldwide', min_mag=1 ):
    # Where data is from
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.csv'

    if period == 'weekly':
        new_url = url.format('all_week')
    elif period == 'monthly':
        new_url = url.format('all_month')
    else:
        new_url = url.format('all_day')

    #Fetch data and extract relevant data
    df_earthquake = pd.read_csv(new_url)
    df_earthquake = df_earthquake(['time', 'lattitude', 'longitude', 'mag', 'place'])

    #Extract sub-area in place columns
    place_list = df_earthquake['place'].str.split(', ')
    df_earthquake['sub_area'] = place_list.apply(extract_subarea)
    df_earthquake['area'] = place_list.apply(extract_area)
    df_earthquake = df_earthquake.drop(columns=['place'], axis=1)

    #Filter data based on min. threshold
    if isinstance(min_mag, int) and min_mag > 0:
        df_earthquake = df_earthquake[df_earthquake['mag']>= min_mag]
    else:
        df_earthquake = df_earthquake[df_earthquake['mag']>0]

    # Convert 'time' to pd datetime
    df_earthquake['time'] = pd.to_datetime(df_earthquake['time'])

    # Set lat and long to a default if not found
    if region in df_earthquake['area'].to_list():
        df_earthquake = df_earthquake[df_earthquake['area'] == region]
        max_mag = df_earthquake['mag'].max()
        center_lat = df_earthquake[df_earthquake['mag']== max_mag]['latitude'].values[0]
        center_long = df_earthquake[df_earthquake['mag']== max_mag]['longitude'].values[0]
    else:
        center_lat, center_long = [54, 15]

    



# Create visualizer