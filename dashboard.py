import radar_line
import heatmap
import scatter_plot
import team_analysis
import player_venue_analysis
import player_team_analysis
import images
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from flask import Flask

radar_line_chart_batsman_list = radar_line.get_players()
radar_inputs = radar_line.preprocess_radar_chart(radar_line_chart_batsman_list)
hm_data,hm_layout = heatmap.prepare_heatmap()
sp_data,sp_layout = scatter_plot.mesh_grid()
spo_data,spo_layout = scatter_plot.mesh_runs_grid()
heatmap_fig = go.Figure(data=hm_data, layout=hm_layout)
meshgrid_fig = go.Figure(data=sp_data, layout=sp_layout)
meshgrid_runs_fig = go.Figure(data=spo_data, layout=spo_layout)
unique_teams = team_analysis.get_unique_teams()
pv_df = player_venue_analysis.pre_process()
image_elements = images.image_elements


# Create app
server = Flask(__name__)
app = dash.Dash(server=server)

# Define layout
app.layout = html.Div(children=[
    
    html.Link(href='static/app.css', rel='stylesheet'),
    # Navigation bar
    html.Div([    html.H1('IPL DATA VISUALIZATION 2018-2019', style={'textAlign': 'center', 'color': 'white'})], style={'backgroundColor': 'navy', 'padding': '5px'}),
    # Tabs
    dcc.Tabs(id='tabs', value='tab1', children=[
        
        # Tab 1: Radar and line charts
        dcc.Tab(label='Player Comparision', value='tab1', style={'font-weight': 'bold'}, children=[
            
            # Dropdown menu for selecting players
            html.Div([
                html.Label('Select Players: ',style={'paddingLeft': '10px'}),
                dcc.Dropdown(
                    id='player-dropdown',
                    options=[{'label': p, 'value': p} for p in radar_line_chart_batsman_list],
                    value=['MS Dhoni','V Kohli'],
                    multi=True
                )
            ], style={'paddingLeft': '20px','paddingRight': '20px'}),

            html.Div([
                # Other elements in your layout
                html.Div(id='player-images', className='row', style={
                    'display': 'flex',
                    'justify-content': 'center',
                    'overflow-x': 'scroll',
                    'margin-right': '20px',
                    'margin-left': '20px',
                })
            ]),

            html.Div([
                    dcc.Graph(id='radar-chart')
                ],
                style={
                    'width': '80%',   # set width to 80% of container width
                    'height': '500px',  # set height to 500 pixels
                    'margin': 'auto'  # set height to 100% of viewport height
                }),

            html.Div([

                html.Div([
                    dcc.Graph(id='line-chart')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='line-chart-economy')
                ],
                style={'display': 'inline-block', 'width': '50%'})

            ]),
            
        ]),
        
        # Tab 2: Empty
        dcc.Tab(label='Team vs Venue Analysis', value='tab2',style={'font-weight': 'bold'}, children=[
            
            html.Div([
                html.Label('Select Team: ',style={'paddingLeft': '10px'}),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': p, 'value': p} for p in unique_teams],
                    value='Sunrisers Hyderabad'
                )
            ], style={'paddingLeft': '20px','paddingRight': '20px'}),

            html.Div([
                # Other elements in your layout
                html.Div(id='team-images', className='row', style={
                    'display': 'flex',
                    'justify-content': 'center',
                    # 'overflow-x': 'scroll',
                    'margin-right': '10px',
                })
            ]),


            html.Div([
                html.Div([
                    dcc.Graph(id='team-chart-one')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='team-chart-two')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ]),

            html.Div([
                html.Div([
                    dcc.Graph(id='team-chart-three')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='team-chart-four')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ])

            

        ]),
        
        # Tab 3: Empty
        dcc.Tab(label='Head to Head Wins', value='tab3',style={'font-weight': 'bold'}, children=[
            # heat map
            html.Div(
                image_elements,
                className='row',
                style={
                    'display': 'flex',
                    'justify-content': 'center',
                    'white-space': 'nowrap',
                    'margin-left' : '6%',
                    'margin-top' : '4%'
                }
            ),
            html.Div([
                dcc.Graph(id='heat-map',figure=heatmap_fig) 
            ])
        ]),

        # Tab 4: player vs venue
        dcc.Tab(label='Player vs Venue Analysis', value='tab4',style={'font-weight': 'bold'}, children=[
    
            html.Div([
                html.Label('Select Player: ',style={'paddingLeft': '10px'}),
                dcc.Dropdown(
                    id='player-venue-dropdown',
                    options=[{'label': p, 'value': p} for p in radar_line_chart_batsman_list],
                    value='RA Jadeja'
                )
            ], style={'paddingLeft': '20px','paddingRight': '20px'}),

            html.Div([
                # Other elements in your layout
                html.Div(id='player-venue-images', className='row', style={
                    'display': 'flex',
                    'justify-content': 'center',
                    # 'overflow-x': 'scroll',
                    'margin-right': '10px',

                })
            ]),

            html.Div([
                html.Div([
                    dcc.Graph(id='player-venue-one')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='player-venue-two')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ]),

            html.Div([
                html.Div([
                    dcc.Graph(id='player-venue-three')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='player-venue-four')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ])
    
        ]),

        # Tab 5: player vs team
        dcc.Tab(label='Player vs Team Analysis', value='tab5', style={'font-weight': 'bold'}, children=[
    
            html.Div([
                html.Label('Select Player: ',style={'paddingLeft': '10px'}),
                dcc.Dropdown(
                    id='player-team-dropdown',
                    options=[{'label': p, 'value': p} for p in radar_line_chart_batsman_list],
                    value='HH Pandya'
                )
            ], style={'paddingLeft': '20px','paddingRight': '20px'}),

            html.Div([
                # Other elements in your layout
                html.Div(id='player-team-images', className='row', style={
                    'display': 'flex',
                    'justify-content': 'center',
                    # 'overflow-x': 'scroll',
                    'margin-right': '10px',

                })
            ]),

            html.Div([
                html.Div([
                    dcc.Graph(id='player-team-one')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='player-team-two')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ]),

            html.Div([
                html.Div([
                    dcc.Graph(id='player-team-three')
                ],
                style={'display': 'inline-block', 'width': '50%'}),

                html.Div([
                    dcc.Graph(id='player-team-four')
                ],
                style={'display': 'inline-block', 'width': '50%'})
            ])
    
        ]),

        dcc.Tab(label='Overs Data Analysis', value='tab6',style={'font-weight': 'bold'}, children=[
            # heat map

            html.Div([
            html.Div([
                dcc.Graph(id='meshgrid',figure=meshgrid_fig) 
            ],
                style={'display': 'inline-block', 'width': '50%'}),

            html.Div([
                dcc.Graph(id='meshgridruns',figure=meshgrid_runs_fig) 
            ],
                style={'display': 'inline-block', 'width': '50%'})
            ])
        
        
        ])

    ])
])







######################################################

@app.callback(Output('tabs', 'style'),
              Input('tabs', 'value'))
def update_tabs_style(tab):
    return {'backgroundColor': '#f2f2f2',
            'color': '#333333',
            'fontWeight': 'bold',
            'border': '1px solid #d6d6d6',
            'borderRadius': '5px',
            'textAlign': 'center',
            'padding': '10px',
            'boxShadow': '0px 0px 5px 0px rgba(0,0,0,0.1)',
            'zIndex': '1',
            'position': 'relative',
            'top': '0px' if tab == 'tab-1' else '-10px'}

# Callback to update radar chart
@app.callback(Output('radar-chart', 'figure'),
              [Input('player-dropdown', 'value')])
def update_radar_chart(selected_players):
    # data = []
    data,layout = radar_line.create_radar_chart(selected_players,radar_inputs[0],radar_inputs[1],radar_inputs[2],
                                  radar_inputs[3],radar_inputs[4],radar_inputs[5],radar_inputs[6],radar_inputs[7],radar_inputs[8],radar_inputs[9])
    
    return {'data': data, 'layout': layout}

# Callback to update line chart
@app.callback(Output('line-chart', 'figure'),
              [Input('player-dropdown', 'value')])
def update_line_chart(selected_players):
    # data = []
    data,layout = radar_line.create_line_chart(selected_players)
    
    return {'data': data, 'layout': layout}  

# Callback to update line chart
@app.callback(Output('line-chart-economy', 'figure'),
              [Input('player-dropdown', 'value')])
def update_line_chart(selected_players):
    # data = []
    data,layout = radar_line.create_economy_line_chart(selected_players)
    
    return {'data': data, 'layout': layout}

#################################################################

# Callback to update team chart
@app.callback(Output('team-chart-one', 'figure'),
              [Input('team-dropdown', 'value')])
def update_team_chart_one(selected_team):
    # data = []
    data,layout = team_analysis.get_chart_one(selected_team)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('team-chart-two', 'figure'),
              [Input('team-dropdown', 'value')])
def update_team_chart_two(selected_team):
    # data = []
    data,layout = team_analysis.get_chart_two(selected_team)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('team-chart-three', 'figure'),
              [Input('team-dropdown', 'value')])
def update_team_chart_three(selected_team):
    # data = []
    data,layout = team_analysis.get_chart_three(selected_team)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('team-chart-four', 'figure'),
              [Input('team-dropdown', 'value')])
def update_team_chart_four(selected_team):
    # data = []
    data,layout = team_analysis.get_chart_four(selected_team)
    
    return {'data': data, 'layout': layout}

@app.callback(Output('team-images', 'children'),
              [Input('team-dropdown', 'value')])
def update_team_images(selected_team):
    # Get the image urls for the selected players from your data
    team_image_urls = team_analysis.get_team_urls(selected_team)
    
    # Create a list of html.Img elements for each image url
    image_elements = [html.Img(src=url, style={'margin-right': '10px','height': '100px', 'width': '100px'}) for url in team_image_urls]
    
    # Return the list of html.Img elements
    return image_elements


####################################################################

# Callback to update player venue chart
@app.callback(Output('player-venue-one', 'figure'),
              [Input('player-venue-dropdown', 'value')])
def update_player_venue_one(selected_player):
    # data = []
    data,layout = player_venue_analysis.get_chart_one(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-venue-two', 'figure'),
              [Input('player-venue-dropdown', 'value')])
def update_player_venue_two(selected_player):
    # data = []
    data,layout = player_venue_analysis.get_chart_two(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-venue-three', 'figure'),
              [Input('player-venue-dropdown', 'value')])
def update_player_venue_three(selected_player):
    # data = []
    data,layout = player_venue_analysis.get_chart_three(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-venue-four', 'figure'),
              [Input('player-venue-dropdown', 'value')])
def update_player_venue_four(selected_player):
    # data = []
    data,layout = player_venue_analysis.get_chart_four(selected_player)
    
    return {'data': data, 'layout': layout}

@app.callback(Output('player-venue-images', 'children'),
              [Input('player-venue-dropdown', 'value')])
def update_player_venue_images(selected_player):
    # Get the image urls for the selected players from your data
    player_image_urls = player_venue_analysis.get_player_urls(selected_player)
    
    # Create a list of html.Img elements for each image url
    image_elements = [html.Img(src=url, style={'margin-right': '10px'}) for url in player_image_urls]
    
    # Return the list of html.Img elements
    return image_elements

############################################################################

# Callback to update player venue chart
@app.callback(Output('player-team-one', 'figure'),
              [Input('player-team-dropdown', 'value')])
def update_player_team_one(selected_player):
    # data = []
    data,layout = player_team_analysis.calculateBatsmanAverage(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-team-two', 'figure'),
              [Input('player-team-dropdown', 'value')])
def update_player_team_two(selected_player):
    # data = []
    data,layout = player_team_analysis.calculateBatsmanStrikeRate(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-team-three', 'figure'),
              [Input('player-team-dropdown', 'value')])
def update_player_team_three(selected_player):
    # data = []
    data,layout = player_team_analysis.calculateBowlerEconomy(selected_player)
    
    return {'data': data, 'layout': layout}

# Callback to update team chart
@app.callback(Output('player-team-four', 'figure'),
              [Input('player-team-dropdown', 'value')])
def update_player_team_four(selected_player):
    # data = []
    data,layout = player_team_analysis.calculateBowlerWickets(selected_player)
    
    return {'data': data, 'layout': layout}

@app.callback(Output('player-team-images', 'children'),
              [Input('player-team-dropdown', 'value')])
def update_player_team_images(selected_player):
    # Get the image urls for the selected players from your data
    player_image_urls = player_team_analysis.get_player_urls(selected_player)
    
    # Create a list of html.Img elements for each image url
    image_elements = [html.Img(src=url, style={'margin-right': '10px'}) for url in player_image_urls]
    
    # Return the list of html.Img elements
    return image_elements


##############################################################################

@app.callback(Output('player-images', 'children'),
              [Input('player-dropdown', 'value')])
def update_player_images(selected_players):
    # Get the image urls for the selected players from your data
    player_image_urls = radar_line.get_player_urls(selected_players)
    
    # Create a list of html.Img elements for each image url
    image_elements = [html.Img(src=url, style={'margin-right': '10px'}) for url in player_image_urls]
    
    # Return the list of html.Img elements
    return image_elements


if __name__ == '__main__':
    app.run_server(debug=True)

