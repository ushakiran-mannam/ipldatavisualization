import pandas as pd
import plotly.graph_objects as go

def get_players():
    merged_ipl_df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    new_df = merged_ipl_df[['ID','batter','batsman_run']].copy()

    # Group data by matchid and batsman
    grouped_data = new_df.groupby(['ID', 'batter'])

    # Create an empty dictionary to store batsman runs
    # batsman_runs = {}
    batsman_list = []

    # Iterate over each group
    for name, group in grouped_data:
        # Calculate total runs scored by the batsman in the match
        # runs = group['batsman_run'].sum()
        
        # Add the batsman and their total runs to the dictionary
        matchid = name[0]
        batsman = name[1]
        if batsman not in batsman_list:
            batsman_list.append(batsman)
    return batsman_list


def preprocess_radar_chart(playerlist):
    merged_ipl_df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    new_df = merged_ipl_df[['ID','batter','batsman_run']].copy()

    # Group data by matchid and batsman
    grouped_data = new_df.groupby(['ID', 'batter'])

    # Create an empty dictionary to store batsman runs
    batsman_runs = {}

    # Iterate over each group
    for name, group in grouped_data:
        # Calculate total runs scored by the batsman in the match
        runs = group['batsman_run'].sum()
        
        # Add the batsman and their total runs to the dictionary
        matchid = name[0]
        batsman = name[1]
        if matchid not in batsman_runs:
            batsman_runs[matchid] = {}
        batsman_runs[matchid][batsman] = runs

    batsman_totals = {}

    for match_id, match_data in batsman_runs.items():
        for batsman, runs in match_data.items():
            if batsman in batsman_totals:
                batsman_totals[batsman] += runs
            else:
                batsman_totals[batsman] = runs 

    sorted_batsman_runs = dict(sorted(batsman_totals.items(), key=lambda x: x[1], reverse=True))

    iswicket_df = merged_ipl_df[['isWicketDelivery','player_out']].copy()

    out_counts = iswicket_df[iswicket_df['isWicketDelivery'] == 1].groupby('player_out')['isWicketDelivery'].count().reset_index(name='out_count')

    out_counts_dict = {}

    for index, row in out_counts.iterrows():
        player = row['player_out']
        out_count = row['out_count']
        out_counts_dict[player] = out_count

    batting_average = {}
    for batsman in sorted_batsman_runs.keys():
        if batsman in out_counts_dict.keys():
            average = sorted_batsman_runs[batsman]/(out_counts_dict[batsman])
        else:
            average = sorted_batsman_runs[batsman]
        batting_average[batsman] = average

    for player in playerlist:
        if player not in batting_average.keys():
            batting_average[player] = 0

    batsman_deliveries = {}

    # Loop through each ball in the dataset
    for index, row in merged_ipl_df.iterrows():
        batsman = row['batter']
        extra_type = row['extra_type']
        
        # If the delivery is not a wide or no ball, add it to the batsman's count
        if extra_type != 'wides':
            if batsman not in batsman_deliveries:
                batsman_deliveries[batsman] = 1
            else:
                batsman_deliveries[batsman] += 1

    batsman_strikerate = {}
    for batsman in sorted_batsman_runs.keys():
        strike_rate = ((sorted_batsman_runs[batsman])/(batsman_deliveries[batsman]))*100
        batsman_strikerate[batsman] = strike_rate

    for player in playerlist:
        if player not in batsman_strikerate.keys():
            batsman_strikerate[player] = 0    

    player_of_match_count = {}

    df_unique = merged_ipl_df.drop_duplicates(subset=['ID', 'Player_of_Match'])

    # Count number of player of the match awards for each player
    awards_count = df_unique['Player_of_Match'].value_counts()

    player_of_match_count = awards_count.to_dict()

    for player in playerlist:
        if player not in player_of_match_count.keys():
            player_of_match_count[player] = 0

    max_bat_avg = 0
    max_strike_rate = 0
    max_player_awrds = 0 
    for value in batting_average.values():
        if value > max_bat_avg:
            max_bat_avg = value

    for value in batsman_strikerate.values():
        if value > max_strike_rate:
            max_strike_rate = value

    for value in player_of_match_count.values():
        if value > max_player_awrds:
            max_player_awrds = value

    return max_bat_avg,max_strike_rate,max_player_awrds,batting_average,batsman_strikerate,player_of_match_count




def create_radar_chart(selected_players,max_bat_avg,max_strike_rate,max_player_awrds,batting_average,batsman_strikerate,player_of_match_count):
    # player1 = 'JC Buttler'
    # player2 = 'HH Pandya'
    # Define data for radar chart
    data = []
    for player in selected_players:
        # player_df = df[df['player'] == player]
        data.append(go.Scatterpolar(
            r=[(batting_average[player] * 1000 )/max_bat_avg, (batsman_strikerate[player]*1000)/max_strike_rate, (player_of_match_count[player]*1000)/max_player_awrds],
            theta=['Average', 'StrikeRate', 'Player Of Match Count'],
            fill='toself',
            name=player,
            hovertext=[{"Average":batting_average[player]},{"Strike rate":batsman_strikerate[player]},{"Player of match":player_of_match_count[player]}],
            hovertemplate="%{hovertext}<extra></extra>"
        ))

    # Define layout for radar chart
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showline=True,
                showticklabels=False,
                range=[0, 1000]
            )
        ),
        showlegend=True,
        title='Players Performance Radar Chart'
    )

    return data,layout