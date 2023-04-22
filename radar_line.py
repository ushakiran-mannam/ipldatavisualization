import pandas as pd
import plotly.graph_objects as go
import images


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

    # print(batsman_list)
    # print(len(batsman_list))
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

    # Read the CSV file into a pandas dataframe
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Group the dataframe by bowler and sum the is_wicket_delivery column for each bowler
    wickets_by_bowler = df.groupby('bowler')['isWicketDelivery'].sum()

    # Print the number of wickets taken by each bowler
    player_wickets_dict = wickets_by_bowler.to_dict()

    for player in playerlist:
        if player not in player_wickets_dict.keys():
            player_wickets_dict[player] = 0

    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    grouped_data = df.groupby('bowler')

    # Create an empty dictionary to store economy of each bowler
    bowler_economy = {}

    # Iterate over each group
    for name, group in grouped_data:
        total_runs = 0
        legal_deliveries = 0
        
        for index, row in group.iterrows():
            # Check if the delivery was a legal delivery
            if row['extra_type'] not in ['wides', 'noballs']:
                legal_deliveries += 1
                # Check if the delivery was not a bye or leg bye
                if row['extra_type'] not in ['byes', 'legbyes']:
                    total_runs += row['total_run']
        
        # Calculate the number of overs bowled by the bowler
        if legal_deliveries == 0:
            overs_bowled = 0
        else:
            overs_bowled = round(legal_deliveries / 6, 2)

        # Calculate the economy of the bowler
        if overs_bowled == 0:
            economy = 0
        else:
            economy = round(total_runs / overs_bowled, 2)

        # Add the bowler and their overall economy to the dictionary
        bowler = name
        bowler_economy[bowler] = economy
    
    for player in playerlist:
        if player not in bowler_economy.keys():
            bowler_economy[player] = 0


    max_bat_avg = 0
    max_strike_rate = 0
    max_player_awrds = 0
    max_wickets = 0
    max_economy = 0

    for value in batting_average.values():
        if value > max_bat_avg:
            max_bat_avg = value

    for value in batsman_strikerate.values():
        if value > max_strike_rate:
            max_strike_rate = value

    for value in player_of_match_count.values():
        if value > max_player_awrds:
            max_player_awrds = value

    for value in player_wickets_dict.values():
        if value > max_wickets:
            max_wickets = value

    for value in bowler_economy.values():
        if value > max_economy:
            max_economy = value



    return max_bat_avg,max_strike_rate,max_player_awrds,max_wickets,max_economy,batting_average,batsman_strikerate,player_of_match_count,player_wickets_dict,bowler_economy




def create_radar_chart(selected_players,max_bat_avg,max_strike_rate,max_player_awrds,max_wickets,max_economy,batting_average,batsman_strikerate,player_of_match_count,player_wickets_dict,bowler_economy):
    # player1 = 'JC Buttler'
    # player2 = 'HH Pandya'
    # Define data for radar chart
    data = []
    for player in selected_players:
        # player_df = df[df['player'] == player]
        data.append(go.Scatterpolar(
            r=[(batting_average[player] * 1000 )/max_bat_avg, (batsman_strikerate[player]*1000)/max_strike_rate, (player_of_match_count[player]*1000)/max_player_awrds, (player_wickets_dict[player]*1000)/max_wickets, (bowler_economy[player]*1000)/max_economy],
            theta=['Batting Average', 'Batting StrikeRate', 'Player Of Match Count', 'Wickets taken', 'Bowling Economy'],
            fill='toself',
            name=player,
            hovertext=[{"Average":batting_average[player]},{"Strike rate":batsman_strikerate[player]},{"Player of match":player_of_match_count[player]},{"Wickets Taken":player_wickets_dict[player]},{"Economy":bowler_economy[player]}],
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
        title='Players Performance Radar Chart',
        height=450 # set height to 600 pixels
    )

    return data,layout

def create_line_chart(selected_players):
    figure_data = []
    data = pd.read_csv("data/2018_and_2019_ipl_ball_by_ball.csv")
    for player in selected_players:
        selected_batsman = player
        if selected_batsman in data['batter'].unique():

            # filter the data to only include the selected batsman
            selected_batsman_data = data[data['batter'] == selected_batsman]

            # group the data by match id and calculate the total runs and balls faced for the selected batsman in each match
            match_batsman_data = selected_batsman_data.groupby('ID')['batsman_run'].agg(['sum', 'count']).reset_index()
            match_batsman_data.columns = ['ID', 'runs', 'balls_faced']

            # calculate the strike rate for the selected batsman in each match
            match_batsman_data['strike_rate'] = (match_batsman_data['runs'] / match_batsman_data['balls_faced']) * 100

            # create a dictionary that maps the actual match id to sequential numbers
            match_id_map = {match_id: i+1 for i, match_id in enumerate(match_batsman_data['ID'].unique())}

            # create a new column in the match_batsman_data dataframe that maps the actual match id to sequential numbers
            match_batsman_data['match_num'] = match_batsman_data['ID'].map(match_id_map)

        else:
            match_batsman_data = pd.DataFrame(columns=['ID', 'runs', 'balls_faced','strike_rate','match_num'], index=[0])
            match_batsman_data.iloc[0,:] = 0

        figure_data.append(go.Scatter(
            x=match_batsman_data['match_num'], y=match_batsman_data['strike_rate'], mode='lines',name=player))
    
    layout = go.Layout(xaxis=dict(title='Match Number'), yaxis=dict(title='Strike Rate'), title='Batting Strike Rate by Match')

    return figure_data,layout

def create_economy_line_chart(selected_players):

    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Group the data by bowler and match ID
   

    

    # Create an empty dictionary to store bowler economy in each match
    bowler_economy = {}

    fig_data = []

    for bowlerName in selected_players:
        if bowlerName in df['bowler'].unique():
            grouped_data = df.groupby(['bowler', 'ID'])
            
            # Iterate over each group
            for (bowler, match_id), group in grouped_data:
                if(bowler!=bowlerName):
                    continue
                else:
                    total_runs = 0
                    legal_deliveries = 0

                    for index, row in group.iterrows():
                        # Check if the delivery was a legal delivery
                        if row['extra_type'] not in ['wides', 'noballs']:
                            legal_deliveries += 1
                            # Check if the delivery was not a bye or leg bye
                            if row['extra_type'] not in ['byes', 'legbyes']:
                                total_runs += row['total_run']

                    # Calculate the number of overs bowled by the bowler in the match
                    if legal_deliveries == 0:
                        overs_bowled = 0
                    else:
                        overs_bowled = round(legal_deliveries / 6, 2)

                    # Calculate the economy of the bowler in the match
                    if overs_bowled == 0:
                        economy = 0
                    else:
                        economy = round(total_runs / overs_bowled, 2)

                    # Add the bowler, match number, and their economy to the dictionary
                    if bowler not in bowler_economy:
                        bowler_economy[bowler] = {}
                    match_num = list(bowler_economy[bowler].keys())[-1] + 1 if len(bowler_economy[bowler]) > 0 else 1
                    bowler_economy[bowler][match_num] = economy

            match_num_list = []
            economy_list = []

            for match_num, economy in bowler_economy[bowlerName].items():
                match_num_list.append(match_num)
                economy_list.append(economy)

            edf = pd.DataFrame({
                'Match Number': match_num_list,
                'Economy': economy_list
            })
            fig_data.append(go.Scatter(
                    x=edf['Match Number'], y=edf['Economy'], mode='lines',name=bowlerName))
        else:
            edf = pd.DataFrame(columns=['Match Number', 'Economy'], index=[0])
            edf.iloc[0,:] = 0
            fig_data.append(go.Scatter(
                    x=edf['Match Number'], y=edf['Economy'], mode='lines',name=bowlerName))
            
    layout = go.Layout(xaxis=dict(title='Match Number'), yaxis=dict(title='Economy'), title='Bowling Economy by Match')
    return fig_data,layout





def get_player_urls(selected_players):
    links = []
    for player in selected_players:
        links.append(images.player_img_dict[player])

    return links
