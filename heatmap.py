import pandas as pd
import plotly.graph_objects as go

def prepare_heatmap():
    merged_ipl_df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    new_df = merged_ipl_df[['ID','Team1','Team2','WinningTeam']].copy()

    grouped_df = new_df.groupby(new_df.columns.tolist(), sort=False)

    wins = {}

    # Iterate over dataframe
    for group,data in grouped_df:
        team1 = group[1]
        team2 = group[2]
        winner = group[3]

        if (team1,team2) in wins:
            (a,b,sum) = wins[(team1,team2)]
            if(winner == team1):
                wins[(team1,team2)] = (a+1,b,sum+1)
            else:
                wins[(team1,team2)] = (a,b+1,sum+1)
        elif (team2,team1) in wins:
            (a,b,sum) = wins[(team2,team1)]
            if(winner == team1):
                wins[(team2,team1)] = (a,b+1,sum+1)
            else:
                wins[(team2,team1)] = (a+1,b,sum+1)
        else:
            wins[(team1,team2)] = (0,0,0)
            (a,b,sum) = wins[(team1,team2)]
            if(winner == team1):
                wins[(team1,team2)] = (a+1,b,sum+1)
            else:
                wins[(team1,team2)] = (a,b+1,sum+1)


    wins_separated = {}
    for (i,j) in wins.items():
        team1 = i[0]
        team2 = i[1]
        wins_separated[(team1,team2)] = j[0]
        wins_separated[(team2,team1)] = j[1]  # Changed here from 2 to 1 

    count = 0
    for i in wins_separated:
        count = count+1

    unique_teams_list = list(set(merged_ipl_df['Team1']).union(set(merged_ipl_df['Team2'])))
    unique_teams_list.sort()

    matrix = []
    for team1 in unique_teams_list:
        row = []
        for team2 in unique_teams_list:
            if team1 == team2:
                row.append(0)
            else:
                key1 = (team1, team2)
                key2 = (team2, team1)
                if key1 in wins_separated:
                    row.append(wins_separated[key1])
                elif key2 in wins_separated:
                    row.append(wins_separated[key2])
                else:
                    row.append(0)
        matrix.append(row)

    heatmap = go.Heatmap(
        x=unique_teams_list,
        y=unique_teams_list,
        z=matrix,
        colorscale='Viridis',
        colorbar=dict(title='Win Count')
    )

    # Create layout
    layout = go.Layout(
        title={
        'text': 'Head-to-Head Win Count',
        'x': 0.5,  # center title
        'xanchor': 'center',  # center title
        'yanchor': 'top'
    },
        xaxis=dict(title='Team'),
        yaxis=dict(title='Team'),

    )

    fig_data = [heatmap]

    return fig_data,layout


    