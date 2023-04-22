import pandas as pd
import plotly.graph_objs as go
import images

def pre_process():
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    
    # Compute the batting statistics
    batting_df = df.groupby(['batter', 'Venue']).agg({'batsman_run': 'sum', 'ballnumber': 'count', 'isWicketDelivery': 'sum'}).reset_index()
    batting_df.rename(columns={'batsman_run': 'runs_scored', 'ballnumber': 'balls_faced', 'isWicketDelivery': 'times_out'}, inplace=True)
    batting_df['batting_average'] = batting_df['runs_scored'] / batting_df['times_out']
    batting_df['batting_strike_rate'] = batting_df['runs_scored'] / batting_df['balls_faced']
    
    # Compute the bowling statistics
    bowling_df = df.groupby(['bowler', 'Venue']).agg({'isWicketDelivery': 'sum', 'total_run': 'sum', 'ballnumber': 'count'}).reset_index()
    bowling_df.rename(columns={'isWicketDelivery': 'wickets_taken', 'total_run': 'runs_conceded', 'ballnumber': 'balls_bowled'}, inplace=True)
    bowling_df['bowling_average'] = bowling_df['runs_conceded'] / bowling_df['wickets_taken']
    bowling_df['bowling_strike_rate'] = bowling_df['balls_bowled'] / bowling_df['wickets_taken']
    
    # Merge the batting and bowling dataframes
    merged_df = pd.merge(batting_df, bowling_df, left_on=['batter', 'Venue'], right_on=['bowler', 'Venue'], how='outer')
    merged_df['player'] = merged_df['batter'].fillna(merged_df['bowler']).fillna('Unknown')
    
    
    # Create a final dataframe that combines the batting and bowling stats for each player at each venue
    final_df = pd.DataFrame(columns=['player', 'venue', 'runs scored at that venue', 'batting average at that venue', 'batting strike rate at that venue', 'wickets taken at that venue', 'bowling average at that venue', 'bowling strike rate at that venue'])
    
    final_df['player'] = merged_df['batter']
    final_df['venue'] = merged_df['Venue']
    final_df['runs scored at that venue'] = merged_df['runs_scored']
    final_df['batting average at that venue'] = merged_df['batting_average']
    final_df['batting strike rate at that venue'] = merged_df['batting_strike_rate']
    final_df['wickets taken at that venue'] = merged_df['wickets_taken']
    final_df['bowling average at that venue'] = merged_df['bowling_average']
    final_df['bowling strike rate at that venue'] = merged_df['bowling_strike_rate']
    
    final_df.drop_duplicates(inplace=True)
    #print(final_df)
    final_dict = final_df.to_dict('records')
    #print(final_dict)
    final_dict = {index: row for index, row in final_df.iterrows() if not pd.isna(row['player'])}
    #print(final_dict)
    return final_df


def get_chart_five(selected_player,final_df):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    selected_batsman=selected_player
    if selected_batsman in final_df['player'].unique():
        player_df = final_df[(final_df['player'] == selected_batsman)]
        player_df = player_df.reset_index()  
        player_df= player_df.rename(columns={0: 'battingaverage'})      
    else:   
        player_df = pd.DataFrame(columns=['venue','runs scored at that venue','batting average at that venue','batting strike rate at that venue'], index=[0])
        player_df.iloc[0,:] = 0
    
    trace = go.Bar(x=player_df['venue'], y=player_df['runs scored at that venue'],marker=dict(color=player_df['runs scored at that venue'], colorscale='Viridis'))
    
        # Create the layout for the bar chart
    layout = go.Layout(title= f'Runs Scored By {selected_player} at that Venue', xaxis=dict(title='Venue'), yaxis=dict(title=''))
    fig_data = [trace]
    return fig_data,layout

def get_chart_one(selected_player):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    selected_batsman=selected_player
    if selected_batsman in df['batter'].unique():
        battingavg_df = df[df['batter'] == selected_batsman]
    
            # Calculate the batting average at each venue for Yuvraj Singh
        batting_avg_df = battingavg_df.groupby(['Venue'])['batsman_run'].sum() / battingavg_df.groupby(['Venue'])['player_out'].count()
    
        batting_avg_df = batting_avg_df.reset_index()
    
    
        batting_avg_df = batting_avg_df.rename(columns={0: 'battingaverage'})
    #     print(batting_avg_df)
    
        
    else:
        batting_avg_df = pd.DataFrame(columns=['Venue','battingaverage'], index=[0])
        batting_avg_df.iloc[0,:] = 0
            
    
    #print(batting_avg_df)
    
    trace = go.Bar(x=batting_avg_df['Venue'], y=batting_avg_df['battingaverage'],marker=dict(color=batting_avg_df['battingaverage'], colorscale='Viridis'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title=f'{selected_player} Batting Average at the venue', xaxis=dict(title='Venue'), yaxis=dict(title=''))
    fig_data = [trace]
    return fig_data,layout

def get_chart_two(selected_player):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    selected_batsman=selected_player
    if selected_batsman in df['batter'].unique():
    # Filter the data for Yuvraj Singh only
        sr_df = df[df['batter'] == selected_batsman]
    
        # Calculate the batting strike rate at each venue for Yuvraj Singh
        balls_faced = sr_df.groupby(['Venue'])['batter'].count()
        runs_scored = sr_df.groupby(['Venue'])['batsman_run'].sum()
        batting_sr_df = (runs_scored / balls_faced) * 100
    
        batting_sr_df = batting_sr_df.reset_index()
    
        #print(batting_avg_df)
        #print(batting_sr_df)
    
    
        batting_sr_df = batting_sr_df.rename(columns={0: 'battingstrikerate'})
    
    #print(batting_sr_df)
    else:
        batting_sr_df = pd.DataFrame(columns=['Venue','battingstrikerate'], index=[0])
        batting_sr_df.iloc[0,:] = 0
        
    trace = go.Bar(x=batting_sr_df['Venue'], y=batting_sr_df['battingstrikerate'],marker=dict(color=batting_sr_df['battingstrikerate'], colorscale='Viridis'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title= f'{selected_player} Strike rate at that venue', xaxis=dict(title='Venue'), yaxis=dict(title=''))
    fig_data = [trace]
    return fig_data,layout

def get_chart_three(selected_player):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    selected_bowler=selected_player
    if selected_bowler in df['bowler'].unique():
        # Filter the data for Imran Tahir only
        #print("hi")
        eco_df = df[df['bowler'] == selected_bowler]
    
        # Calculate the economy rate at each venue for Imran Tahir
        economy_rate_df = eco_df.groupby(['Venue'])['total_run'].sum() / (eco_df.groupby(['Venue'])['overs'].sum() // 60)
        # print(economy_rate_df)
    
    
        economy_rate_df = economy_rate_df.reset_index()
        economy_rate_df = economy_rate_df.rename(columns={0: 'economy'})
        
    else:
        #print("hello")
        economy_rate_df = pd.DataFrame(columns=['Venue','economy'], index=[0])
        economy_rate_df.iloc[0,:] = 0
        
    
    # print(economy_rate_df)
    
    trace = go.Bar(x=economy_rate_df['Venue'], y=economy_rate_df['economy'],marker=dict(color=economy_rate_df['economy'], colorscale='Viridis'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title= f'{selected_player} Economy at Each Venue', xaxis=dict(title='Venue'), yaxis=dict(title=''))
    fig_data = [trace]
    return fig_data,layout
                         
def get_chart_four(selected_player):
    df = pd.read_csv('data/2018_and_2019_ipl_ball_by_ball.csv')
    selected_bowler=selected_player
    if selected_bowler in df['bowler'].unique():
    
    #Filter the data for Imran Tahir only
        wickets_org_df = df[df['bowler'] == 'Imran Tahir']
    
        #Count the number of wickets taken by Imran Tahir at each venue
        wickets_df = wickets_org_df.groupby(['Venue'])['player_out'].count()
    
        wickets_df = wickets_df.reset_index()
        #print(batting_avg_df)
        #print(batting_sr_df)
    
    
        wickets_df = wickets_df.rename(columns={0: 'wicketstaken'})
        
    else:
        wickets_df = pd.DataFrame(columns=['Venue','player_out'], index=[0])
        wickets_df.iloc[0,:] = 0
        
        
    
    trace = go.Bar(x=wickets_df['Venue'], y=wickets_df['player_out'],marker=dict(color=wickets_df['player_out'], colorscale='Inferno'))
    
    # Create the layout for the bar chart
    layout = go.Layout(title= f'{selected_player} Wickets taken at that Venue', xaxis=dict(title='Venue'), yaxis=dict(title=''))
    fig_data = [trace]
    return fig_data,layout

def get_player_urls(selected_player):
    links = []
    
    links.append(images.player_img_dict[selected_player])

    return links
        