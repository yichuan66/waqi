import plotly.graph_objects as go
import csv
from geodesic import GeodesicGrid as gd
from waqi_schema_helper import WaqiSchemaHelper

grid = gd.get_grid(order=3, r=1)

waqi_raw_data = {'id':[], 'lat':[], 'lon':[], 'aqi':[]}
filename = 'data/download/2019-10-08_23_10_04_500/data_downloaded.csv'
with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        if WaqiSchemaHelper.is_valid_row([v for k, v in row.items()]) and count%10 == 0:
            waqi_raw_data['id'].append(row['station_index'])
            waqi_raw_data['lat'].append(float(row['latitude']))
            waqi_raw_data['lon'].append(float(row['longitude']))
            waqi_raw_data['aqi'].append(min(float(row['aqi']), 250))
        count += 1
print(len(waqi_raw_data['id']))

data = {
    'lat' : waqi_raw_data['lat'],
    'lon' : waqi_raw_data['lon'],
    'color' : waqi_raw_data['aqi'],
    'size' : [5 for i in range(len(waqi_raw_data['id']))]
    }

marker = dict(
    size=data['size'],
    color=data['color'],
    showscale=True,
    reversescale=True,
    colorscale='Viridis')

fig = go.Figure(data=go.Scattergeo(
        
        lon=data['lon'],
        lat=data['lat'],
        hovertext=data['color'],
        hoverinfo='text',
        marker=marker))

fig.show()
