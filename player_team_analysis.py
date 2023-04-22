import pandas as pd
import plotly.graph_objs as go
import plotly.colors as cl
import images


def calculateBatsmanAverage(playerName):

    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Derive the opponent team for each match
    df['opponent'] = df.apply(lambda x: x['Team1'] if x['BattingTeam'] == x['Team2'] else x['Team2'], axis=1)

    # Group the data by matchid, batter, and opponent
    grouped_data = df.groupby(['batter', 'opponent'])

    # Create an empty dictionary to store batsman runs against each opponent
    batsman_runs = {}

    # Iterate over each group
    for name, group in grouped_data:
        # Calculate total runs scored by the batsman against the opponent in the match
        runs = group['batsman_run'].sum()
        
        # Add the batsman and their total runs against the opponent to the dictionary
        batsman = name[0]
        opponent = name[1]
        if batsman not in batsman_runs:
            batsman_runs[batsman] = {}
        batsman_runs[batsman][opponent] = runs

    iswicket_df = df[['isWicketDelivery','player_out','opponent']].copy()
    out_counts = iswicket_df[iswicket_df['isWicketDelivery'] == 1].groupby('player_out')['isWicketDelivery'].count().reset_index(name='out_count')
    opponent_counts = df.groupby(['player_out', 'opponent']).count()['isWicketDelivery']
    outs_against_each_opponent = opponent_counts.reset_index().groupby('player_out').apply(lambda x: x.set_index('opponent').to_dict()['isWicketDelivery']).to_dict()

    # Create a new dictionary to store the total runs and total outs for each batsman against each opponent
    totals = {}
    for batsman in batsman_runs:
        for opponent in batsman_runs[batsman]:
            if batsman in outs_against_each_opponent and opponent in outs_against_each_opponent[batsman]:
                runs = batsman_runs[batsman][opponent]
                outs = outs_against_each_opponent[batsman][opponent]
                if batsman not in totals:
                    totals[batsman] = {}
                if opponent not in totals[batsman]:
                    totals[batsman][opponent] = {'runs': 0, 'outs': 0}
                totals[batsman][opponent]['runs'] += runs
                totals[batsman][opponent]['outs'] += outs

    # Calculate the average runs for each batsman against each opponent
    averages = {}
    for batsman in totals:
        averages[batsman] = {}
        for opponent in totals[batsman]:
            runs = totals[batsman][opponent]['runs']
            outs = totals[batsman][opponent]['outs']
            if outs >= 0:
                averages[batsman][opponent] = runs / max(outs, 1)


    

    # Define the batsman for whom you want to plot the average
    batsman = playerName

    if batsman in averages:
        
        # Get the data for the given batsman
        batsman_data = averages[batsman]

        # Create a list of dictionaries containing the opponent and the average against that opponent
        opponent_averages = [{'Opponent team': opponent, 'Average': average} for opponent, average in batsman_data.items()]

        # Create a DataFrame from the averages
        df = pd.DataFrame(opponent_averages)
    else:
        
        df = pd.DataFrame(columns = ['Opponent team', 'Average'], index=[0])
        df.iloc[0,:] = 0

    # Create the trace for the bar chart
    trace = go.Bar(x=df['Opponent team'], y=df['Average'], marker=dict(color=df['Average'], colorscale='Viridis'))

    # Create the layout for the bar chart
    layout = go.Layout(title='{} IPL Average against each Opponent'.format(batsman), xaxis=dict(title='Opponent team'), yaxis=dict(title='Average'))

    fig_data = [trace]

    return fig_data, layout


def calculateBatsmanStrikeRate(playerName):


    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Derive the opponent team for each match
    df['opponent'] = df.apply(lambda x: x['Team1'] if x['BattingTeam'] == x['Team2'] else x['Team2'], axis=1)

    # Group the data by matchid, batter, and opponent
    grouped_data = df.groupby(['batter', 'opponent'])


    # Create an empty dictionary to store batsman runs and balls faced against each opponent
    batsman_stats = {}

    # Iterate over each group
    for name, group in grouped_data:
        # Calculate total runs scored by the batsman against the opponent in the match
        runs = group['batsman_run'].sum()
        
        # Calculate total balls faced by the batsman against the opponent in the match
        balls_faced = len(group)
        
        # Add the batsman, their total runs and balls faced against the opponent to the dictionary
        batsman = name[0]
        opponent = name[1]
        if batsman not in batsman_stats:
            batsman_stats[batsman] = {}
        batsman_stats[batsman][opponent] = {'runs': runs, 'balls_faced': balls_faced}


    # Define the player for whom you want to plot the strike rate
    batsman = playerName
        
        
    if batsman in batsman_stats:
    
        # Get the data for the given player
        player_data = batsman_stats[batsman]

        # Iterate through the opponent teams and calculate the strike rate
        opponent_strike_rates = []
        for opponent, runs_balls in player_data.items():
            runs = runs_balls['runs']
            balls = runs_balls['balls_faced']
            if balls > 0:
                strike_rate = runs / balls * 100
            else:
                strike_rate = 0
            opponent_strike_rates.append({'Opponent team': opponent, 'Strike rate': strike_rate})

        # Create a DataFrame from the strike rates
        df = pd.DataFrame(opponent_strike_rates)
    else:
        
        df = pd.DataFrame(columns = ['Opponent team', 'Strike rate'], index=[0])
        df.iloc[0,:] = 0

    # Create the trace for the bar chart
    trace = go.Bar(x=df['Opponent team'], y=df['Strike rate'], marker=dict(color=df['Strike rate'], colorscale='RdYlGn'))

    # Create the layout for the bar chart
    layout = go.Layout(title='{} IPL Strike Rate against each Opponent'.format(batsman), xaxis=dict(title='Opponent team'), yaxis=dict(title='Strike rate'))

    fig_data = [trace]

    return fig_data, layout


def calculateBowlerWickets(playerName):

    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Derive the opponent team for each match
    df['opponent'] = df.apply(lambda x: x['Team2'] if x['BattingTeam'] == x['Team2'] else x['Team1'], axis=1)

    # Group the data by bowler and opponent
    grouped_data = df.groupby(['bowler', 'opponent'])

    # Create an empty dictionary to store bowler wickets against each opponent
    bowler_wickets = {}

    # Iterate over each group
    for name, group in grouped_data:
        # Extract the bowler and opponent names from the group name
        bowler = name[0]
        opponent = name[1]
        
        # Initialize the wicket count to zero
        wickets = 0
        
        # Iterate over each row in the group
        for index, row in group.iterrows():
            is_wicket = row['isWicketDelivery']
            kind = row['kind']
            
            # Skip rows where isWicket is not True
            if not is_wicket:
                continue
                
            # If the kind of out is "runout", skip this row
            if kind == 'run out':
                continue
            
            # Increment the wicket count
            wickets += 1
        
        # Add the bowler and their wicket against the opponent to the dictionary
        if bowler not in bowler_wickets:
            bowler_wickets[bowler] = {}
        bowler_wickets[bowler][opponent] = wickets


    if playerName in bowler_wickets:
        
        # Define the player for whom you want to plot the wickets
        bowler = playerName
        # Get the data for the given player
        player_data = bowler_wickets[bowler]

        # Create a list of dictionaries containing the opponent and the number of wickets against that opponent
        opponent_wickets = [{'Opponent team': opponent, 'Wickets': wickets} for opponent, wickets in player_data.items()]

        # Create a DataFrame from the wickets
        df = pd.DataFrame(opponent_wickets)
    else:
        
        df = pd.DataFrame(columns = ['Opponent team', 'Wickets'], index=[0])
        df.iloc[0,:] = 0

    # Create the trace for the bar chart
    trace = go.Bar(x=df['Opponent team'], y=df['Wickets'], marker=dict(color=df['Wickets'], colorscale='Viridis'))

    # Create the layout for the bar chart
    layout = go.Layout(title='{} IPL Wickets against each Opponent'.format(playerName), xaxis=dict(title='Opponent team'), yaxis=dict(title='Wickets'))

    fig_data = [trace]

    return fig_data, layout


def calculateBowlerEconomy(playerName):

    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')

    # Derive the opponent team for each match
    df['opponent'] = df.apply(lambda x: x['Team2'] if x['BattingTeam'] == x['Team2'] else x['Team1'], axis=1)

    # Group the data by bowler and opponent
    grouped_data = df.groupby(['bowler', 'opponent'])

    # Create an empty dictionary to store economy of each bowler against each opponent
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
        
        # Calculate the number of overs bowled by the bowler against the opponent in the match
        if legal_deliveries == 0:
            overs_bowled = 0
        else:
            overs_bowled = round(legal_deliveries / 6, 2)

        # Calculate the economy of the bowler against the opponent in the match
        if overs_bowled == 0:
            economy = 0
        else:
            economy = round(total_runs / overs_bowled, 2)

        # Add the bowler and their economy against the opponent to the dictionary
        bowler = name[0]
        opponent = name[1]
        if bowler not in bowler_economy:
            bowler_economy[bowler] = {}
        bowler_economy[bowler][opponent] = economy


    # Define the bowler for whom you want to plot the economy rate
    bowler = playerName
    
    if bowler in bowler_economy:
    
        # Get the data for the given bowler
        bowler_data = bowler_economy[bowler]

        # Create a list of dictionaries containing the opponent and the economy rate against that opponent
        opponent_economy = [{'Opponent team': opponent, 'Economy rate': economy} for opponent, economy in bowler_data.items()]

        # Create a DataFrame from the economy rates
        df = pd.DataFrame(opponent_economy)
    else:
        
        df = pd.DataFrame(columns = ['Opponent team', 'Economy rate'], index=[0])
        df.iloc[0,:] = 0

    # Define the colors for the bar chart
    num_opponents = len(df['Opponent team'])
    color_scale = cl.qualitative.Alphabet
    colors = color_scale[:num_opponents]

    # Create the trace for the bar chart
    trace = go.Bar(x=df['Opponent team'], y=df['Economy rate'], marker=dict(color=colors, colorscale=color_scale))

    # Create the layout for the bar chart
    layout = go.Layout(title='{} IPL Economy Rate against each Opponent'.format(bowler), xaxis=dict(title='Opponent team'), yaxis=dict(title='Economy rate'))

    fig_data = [trace]

    return fig_data, layout


def get_player_urls(selected_player):
    links = []
    
    links.append(images.player_img_dict[selected_player])

    return links

