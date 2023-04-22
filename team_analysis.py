import pandas as pd
import plotly.graph_objs as go
import images

def get_unique_teams():
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Get all unique teams
    teams = df['BattingTeam'].unique()

    return teams

def get_chart_one(selected_team):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Filter the data for Mumbai Indians batting
    mi_df = df[df['BattingTeam'] == selected_team]

    # Calculate the total runs scored by Mumbai Indians at each venue
    venue_runs_df = mi_df.groupby('Venue').agg({'total_run': 'sum', 'ID': 'nunique'}).reset_index()
    venue_runs_df['avg_runs'] = venue_runs_df['total_run'] / venue_runs_df['ID']


    trace = go.Bar(x=venue_runs_df['Venue'], y=venue_runs_df['avg_runs'],marker=dict(color=venue_runs_df['avg_runs'], colorscale='Viridis'))
    # Create the layout for the bar chart
    layout = go.Layout(title=f'{selected_team} Average Runs Scored by Venue', xaxis=dict(title='Venue'), yaxis=dict(title='average runs'))

    fig_data = [trace]

    return fig_data,layout

def get_chart_two(selected_team):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    mi_df = df[df['BattingTeam'] == selected_team]

    # Calculate the total matches played by Mumbai Indians at each venue
    matches_df = mi_df.groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    matches_df = matches_df.rename(columns={'ID': 'TotalMatches'})
    
    # Calculate the total wins by Mumbai Indians at each venue
    wins_df = mi_df[mi_df['WinningTeam'] == selected_team].groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    wins_df = wins_df.rename(columns={'ID': 'TotalWins'})
    
    # Replace NaN values in 'TotalWins' column with 0
    wins_df['TotalWins'].fillna(0, inplace=True)
    
    # Calculate the win percentage by Mumbai Indians at each venue
    win_perc_df = pd.merge(matches_df, wins_df, on='Venue', how='outer')
    
    # Replace NaN values in 'TotalWins' column with 0
    win_perc_df['TotalWins'].fillna(0, inplace=True)
    
    win_perc_df['WinPercentage'] = (win_perc_df['TotalWins'] / win_perc_df['TotalMatches']) * 100
    win_perc_df['WinPercentage'] = win_perc_df['WinPercentage'].round(2).fillna(0)
    
    #print(win_perc_df)
    
    
    
    trace = go.Bar(x=win_perc_df['Venue'], y=win_perc_df['WinPercentage'],marker=dict(color=win_perc_df['WinPercentage'], colorscale='Viridis'))
    layout = go.Layout(title=f' {selected_team} Win Percentage by Venue', xaxis=dict(title='Venue'), yaxis=dict(title='WinPercentage'))
    fig_data=[trace]
    return fig_data,layout


def get_chart_three(selected_team):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    mi_df = df[df['BattingTeam'] == selected_team]
    mi_bat_first_df = mi_df[(mi_df['innings'] == 1) & (mi_df['BattingTeam'] == selected_team)]
    
    #print(mi_bat_first_df)
    
    # Calculate the total matches played by Mumbai Indians when batting first at each venue
    matches_bat_first_df = mi_bat_first_df.groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    matches_bat_first_df = matches_bat_first_df.rename(columns={'ID': 'TotalMatchesBatFirst'})
    #print(matches_bat_first_df)
    
    # Calculate the total wins by Mumbai Indians when batting first at each venue
    wins_bat_first_df = mi_bat_first_df[mi_bat_first_df['WinningTeam'] == selected_team].groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    wins_bat_first_df = wins_bat_first_df.rename(columns={'ID': 'TotalWinsBatFirst'})
    
    # Calculate the win percentage by Mumbai Indians when batting first at each venue
    win_perc_bat_first_df = pd.merge(matches_bat_first_df, wins_bat_first_df, on='Venue', how='outer')
    win_perc_bat_first_df['WinPercentageBatFirst'] = (win_perc_bat_first_df['TotalWinsBatFirst'] / win_perc_bat_first_df['TotalMatchesBatFirst']) * 100
    
    
    trace = go.Bar(x=win_perc_bat_first_df['Venue'], y=win_perc_bat_first_df['WinPercentageBatFirst'],marker=dict(color=win_perc_bat_first_df['WinPercentageBatFirst'], colorscale='Viridis'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title=f'{selected_team} Win perecentage when Batting First by Venue', xaxis=dict(title='Venue'), yaxis=dict(title='Win Percentage'))
    fig_data=[trace]
    return fig_data,layout

def get_chart_four(selected_team):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    
    
    mi_df = df[df['BattingTeam'] == selected_team]

    # Filter the data for Mumbai Indians matches where they batted first
    mi_bat_second_df = mi_df[(mi_df['innings'] == 2) & (mi_df['BattingTeam'] == selected_team)]
    
    #print(mi_bat_second_df)
    
    # Calculate the total matches played by Mumbai Indians when batting first at each venue
    matches_bat_second_df = mi_bat_second_df.groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    matches_bat_second_df = matches_bat_second_df.rename(columns={'ID': 'TotalMatchesBatFirst'})
    #print(matches_bat_second_df)
    
    # Calculate the total wins by Mumbai Indians when batting first at each venue
    wins_bat_second_df = mi_bat_second_df[mi_bat_second_df['WinningTeam'] == selected_team].groupby('Venue').agg({'ID': 'nunique'}).reset_index()
    wins_bat_second_df = wins_bat_second_df.rename(columns={'ID': 'TotalWinsBatFirst'})
    
    # Calculate the win percentage by Mumbai Indians when batting first at each venue
    win_perc_bat_second_df = pd.merge(matches_bat_second_df, wins_bat_second_df, on='Venue', how='outer')
    win_perc_bat_second_df['WinPercentageBatSecond'] = (win_perc_bat_second_df['TotalWinsBatFirst'] / win_perc_bat_second_df['TotalMatchesBatFirst']) * 100
    
    
    trace = go.Bar(x=win_perc_bat_second_df['Venue'], y=win_perc_bat_second_df['WinPercentageBatSecond'],marker=dict(color=win_perc_bat_second_df['WinPercentageBatSecond'], colorscale='Viridis'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title=f'{selected_team} Win Percentage When Batting Second By Venue', xaxis=dict(title='Venue'), yaxis=dict(title='Win Percetage'))
    
    fig_data=[trace]
    return fig_data,layout


def get_team_urls(selected_team):
    links = []
    
    links.append(images.team_images[selected_team])

    return links