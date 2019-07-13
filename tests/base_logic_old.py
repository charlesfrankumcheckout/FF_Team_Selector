import pickle
import pandas as pd
from datetime import datetime 
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

## Read in the datasets
# Player statistics data
path = open(r'C:\Users\charl\Desktop\FantasyFootball\Players\player_stats_cleaned.pk', 'rb')
player_stats = pickle.load(path)

# Fixture Gameweeks data
gameweeks = pd.read_csv(r'C:\Users\charl\Desktop\FantasyFootball\Fixtures\fixtures.csv')

# Team info data
team_path = open(r'C:\Users\charl\Desktop\FantasyFootball\Team\team_info.pk', 'rb')
team_info = pickle.load(team_path)

# =============================================================================
# # Latest Skybet odds data
# filename = '\PL_Odds_'+str(datetime.now()).split(' ')[0].replace('-','_')
# game_odds = pd.read_csv(r'C:\Users\charl\Desktop\FantasyFootball\SkyBet'+filename+'.csv')
# =============================================================================

# Convert date column to datetime
gameweeks['datetime'] = pd.to_datetime(gameweeks['datetime'])
# Separate into future, past and current gameweeks
future_games = gameweeks[gameweeks['datetime'] >= datetime.today().date()]
past_games = gameweeks[gameweeks['datetime'] < datetime.today().date()]
current_gameweek = gameweeks[gameweeks['gameweek'] == min(future_games['gameweek'])]

# identify whether we are in a transfer period
if len(future_games.loc[future_games['gameweek'] == int(current_gameweek.iloc[0]['gameweek'])]) < len(current_gameweek):
    next_gameweek = current_gameweek.iloc[0]['gameweek'] + 1
else:
    next_gameweek = current_gameweek
    
# grab the next set of fixtures
next_gameweek_df = gameweeks[gameweeks['gameweek'] == next_gameweek]

# Generate scores for every player based on how valuable they are historically/currently

# Look at player points and value over time - get the top x for each position for last n weeks
def top_x_points(position, period, x):
    score_dict = {}
    for k,v in player_stats.items():
        if player_stats[k]['details']['position'] == position:
            stats_table = player_stats[k]['stats']
            score = sum(stats_table[stats_table['GameWeek'] > (max(stats_table['GameWeek']) - period)]['Points'])
            if len(score_dict) < x:
                score_dict[k] = score
            elif score > min(score_dict.values()):
                score_dict.pop([k for k,v in score_dict.items() if v == min(score_dict.values())][0], None)
                score_dict[k] = score
    return score_dict

goalie_points_dict = top_x_points('Goalkeeper', 4, 5)
defender_points_dict = top_x_points('Defender', 4, 5)
midfielder_points_dict = top_x_points('Midfielder', 4, 5)
striker_points_dict = top_x_points('Forward', 4, 5)

def top_x_value(position, period, x):
    score_dict = {}
    for k,v in player_stats.items():
        if player_stats[k]['details']['position'] == position:
            stats_table = player_stats[k]['stats']
            stats_table['value'] = stats_table['Points']/stats_table['£'] 
            player_stats[k]['stats'] = stats_table
            # Use the sum of the last 4 weeks of value and select players to be graphed based on this
            score = sum(stats_table[stats_table['GameWeek'] > (max(stats_table['GameWeek']) - period)]['value'])
            if len(score_dict) < x:
                score_dict[k] = score
            elif score > min(score_dict.values()):
                score_dict.pop([k for k,v in score_dict.items() if v == min(score_dict.values())][0], None)
                score_dict[k] = score
    return score_dict
        
goalie_value_dict = top_x_value('Goalkeeper', 4, 5)
defender_value_dict = top_x_value('Defender', 4, 5)
midfielder_value_dict = top_x_value('Midfielder', 4, 5)
striker_value_dict = top_x_value('Forward', 4, 5)

def plot_performance(players_dict, metric):
    plt.figure()
    ax = plt.subplot()

    for k,v in players_dict.items():
        
        ax.plot(player_stats[k]['stats']['GameWeek'],player_stats[k]['stats'][str(metric)], label = k)
        
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel('GameWeek')
    plt.ylabel(player_stats[k]['details']['position'] + ' - ' +str(metric))
    plt.show()
    
plot_performance(goalie_points_dict, 'Points')
plot_performance(defender_points_dict, 'Points')
plot_performance(midfielder_points_dict, 'Points')
plot_performance(striker_points_dict, 'Points')
    
plot_performance(goalie_value_dict, 'value')
plot_performance(defender_value_dict, 'value')
plot_performance(midfielder_value_dict, 'value')
plot_performance(striker_value_dict, 'value')

# Apply linear regression on the full player list

# Need to apply data imputing so that all player data is of equal size - use auto encoding combined with nn maybe?
# Simple linear regression on player value vs points
values = [v['stats']['value'] for k,v in player_stats.items()]
points = [v['stats']['Points'] for k,v in player_stats.items()]

for k,v in player_stats.items()
  LinearRegression().fit(x,y)



# Use betting sites to identify which teams are likely to win the next gameweek(s) and adjust scores
# Add weights based on injuries or absence = 0
# Use these scores to identify how well my players are doing
# Set a threshold on whether to use a free transfer / bonus cards
# Set a threshold on whether it is worth it to spend 4 points on a transfer
# Give captain/vice captain to players with highest scores on team









