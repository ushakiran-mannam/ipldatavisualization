import radar_line
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from flask import Flask

radar_line_chart_batsman_list = radar_line.get_players()
radar_inputs = radar_line.preprocess_radar_chart(radar_line_chart_batsman_list)


# Create app
server = Flask(__name__)
app = dash.Dash(server=server)


# Define layout
app.layout = html.Div([
    
    # Tabs
    dcc.Tabs(id='tabs', value='tab1', children=[
        
        # Tab 1: Radar and line charts
        dcc.Tab(label='Charts', value='tab1', children=[
            
            # Dropdown menu for selecting players
            html.Div([
                html.Label('Select Players: '),
                dcc.Dropdown(
                    id='player-dropdown',
                    options=[{'label': p, 'value': p} for p in radar_line_chart_batsman_list],
                    value=['MS Dhoni','V Kohli'],
                    multi=True
                )
            ]),
            
            # Radar chart
            html.Div([
                dcc.Graph(id='radar-chart')
            ]),
            
            # # Line chart
            # html.Div([
            #     html.Label('Select Player for Line Chart: '),
            #     dcc.Dropdown(
            #         id='line-player-dropdown',
            #         options=[{'label': v, 'value': k} for k, v in players.items()],
            #         value='player1'
            #     ),
            #     dcc.Graph(id='line-chart')
            # ]),
            
            # # Toggle for selecting player 2 for line chart
            # html.Div([
            #     html.Label('Select Player 2: '),
            #     dcc.RadioItems(
            #         id='line-player2-toggle',
            #         options=[{'label': v, 'value': k} for k, v in players.items()],
            #         value=None
            #     )
            # ])
        ]),
        
        # Tab 2: Empty
        dcc.Tab(label='Tab 2', value='tab2', children=[
            html.Div([
                html.H3('Player performance analysis')
            ])
        ]),
        
        # Tab 3: Empty
        dcc.Tab(label='Tab 3', value='tab3', children=[
            html.Div([
                html.H3('Team Performance analysis')
            ])
        ])
    ])
])

# Callback to update radar chart
@app.callback(Output('radar-chart', 'figure'),
              [Input('player-dropdown', 'value')])
def update_radar_chart(selected_players):
    # data = []
    data,layout = radar_line.create_radar_chart(selected_players,radar_inputs[0],radar_inputs[1],radar_inputs[2],
                                  radar_inputs[3],radar_inputs[4],radar_inputs[5])
    
    return {'data': data, 'layout': layout}

if __name__ == '__main__':
    app.run_server(debug=True)

