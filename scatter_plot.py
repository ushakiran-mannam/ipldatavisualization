import pandas as pd
import plotly.graph_objs as go

def mesh_grid():

    # Load the data
    ipl_data = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    wicket_count = ipl_data.groupby(['overs', 'ballnumber'])['isWicketDelivery'].sum().reset_index()
    # Define the data trace
    data = go.Mesh3d(x=wicket_count['overs'],
                    y=wicket_count['ballnumber'],
                    z=wicket_count['isWicketDelivery'],
                    intensity=wicket_count['isWicketDelivery'],
                    color='cyan',
                    colorbar=dict(
                        len=0.5,  # set the length of the colorbar to 50% of the default size
                        tickfont=dict(size=10)
                    ),
                    opacity=0.8)

    # Define the layout
    layout = go.Layout(
        title={
        'text': 'Wickets in all overs analysis',
        'x': 0.47,  # center title
        'xanchor': 'center',  # center title
        
        'y': 0.9
    },
    scene=dict(
        xaxis=dict(
            title='Overs',
            nticks=10,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title='Ball Number',
            nticks=10,
            tickfont=dict(size=10)
        ),
        zaxis=dict(
            title='Is Wicket',
            nticks=5,
            tickfont=dict(size=10)
        ),
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(
            eye=dict(x=1.8, y=-1.8, z=0.9)
        ),
        dragmode='turntable',
        bgcolor='white'
    ),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    height=600
    ) 

    fig_data = [data]

    return fig_data,layout


def mesh_runs_grid():

    # Load the data
    ipl_data = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    wicket_count = ipl_data.groupby(['overs', 'ballnumber'])['total_run'].sum().reset_index()
    # Define the data trace
    data = go.Mesh3d(x=wicket_count['overs'],
                    y=wicket_count['ballnumber'],
                    z=wicket_count['total_run'],
                    intensity=wicket_count['total_run'],
                    color='cyan',
                    colorbar=dict(
                        len=0.5,  # set the length of the colorbar to 50% of the default size
                        tickfont=dict(size=10)
                    ),
                    opacity=0.8)

    # Define the layout
    layout = go.Layout(
        title={
        'text': 'Runs in all overs analysis',
        'x': 0.47,  # center title
        'xanchor': 'center',  # center title
        
        'y': 0.9
    },
    scene=dict(
        xaxis=dict(
            title='Overs',
            nticks=10,
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            title='Ball Number',
            nticks=10,
            tickfont=dict(size=10)
        ),
        zaxis=dict(
            title='Runs',
            nticks=5,
            tickfont=dict(size=10)
        ),
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(
            eye=dict(x=1.8, y=-1.8, z=0.9)
        ),
        dragmode='turntable',
        bgcolor='white'
    ),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
        pad=0
    ),
    height=600
    ) 

    fig_data = [data]

    return fig_data,layout
