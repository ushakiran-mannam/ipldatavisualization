import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Sample data
data = pd.DataFrame({
    'City': ['Delhi', 'Mumbai', 'Chennai', 'Kolkata'],
    'Lat': [28.7041, 19.0760, 13.0827, 22.5726],
    'Lon': [77.1025, 72.8777, 80.2707, 88.3639],
    'Metric': [10, 20, 30, 40]
})

# Define the India map
india_map = px.choropleth_mapbox(
    data_frame=data,
    geojson="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data",
    locations=["City"],
    color="Metric",
    mapbox_style="carto-positron",
    center={"lat": 20.5937, "lon": 78.9629},
    zoom=3,
    opacity=0.5,
    hover_name="City",
    hover_data={"Lat": False, "Lon": False, "Metric": True}
)

# Define the stadium photos and stats
stadiums = {
    'Delhi': {'image': 'https://i.imgur.com/ET8W0PV.jpeg', 'stats': 'Strike rate: 125'},
    'Mumbai': {'image': 'https://i.imgur.com/ATzQk2E.jpeg', 'stats': 'Strike rate: 145'},
    'Chennai': {'image': 'https://i.imgur.com/1E4NShU.jpeg', 'stats': 'Strike rate: 135'},
    'Kolkata': {'image': 'https://i.imgur.com/iViJdMj.jpeg', 'stats': 'Strike rate: 130'}
}

# Define the app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Graph(
        id='india-map',
        figure=india_map
    ),
    html.Div(
        id='stadium-info',
        style={'textAlign': 'center'}
    )
])

# Define the callback to update the stadium information when a location is clicked on the map
@app.callback(
    dash.dependencies.Output('stadium-info', 'children'),
    [dash.dependencies.Input('india-map', 'clickData')])
def update_stadium_info(clickData):
    if clickData is not None:
        location = clickData['points'][0]['location']
        stadium_image = stadiums[location]['image']
        stadium_stats = stadiums[location]['stats']
        return [
            html.Img(src=stadium_image),
            html.H3(location),
            html.H4(stadium_stats)
        ]
    else:
        return []

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
