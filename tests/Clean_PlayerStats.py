import pickle
from tqdm import tqdm
import pandas as pd

# Read in the datasets
# Player statistics data
path = open(r'C:\Users\charl\Desktop\FantasyFootball\Players\player_stats.pk', 'rb')
player_stats = pickle.load(path)
# results data for name mapping
path = open(r'C:\Users\charl\Desktop\FantasyFootball\Results\results_stats.pk', 'rb')
result_stats = pickle.load(path)

# Rename teams to match results_stats dictionary
team_name_map = {}
# sort both by alphabetical order so that they can be mapped in a loop
teams_1 = list(set([v['details']['club'] for k,v in player_stats.items()]))
teams_1.sort()
teams_2 = [k for k,v in result_stats.items()]
teams_2.sort()
for team in enumerate(teams_1):
    team_name_map[team[1]] = teams_2[team[0]]

# Clean the dataframes for each player
for name, stats in tqdm(player_stats.items()):
    # clean the history dataframe
    temp_df = player_stats[name]['history']
    try:
        temp_df['Season'] = [x.split('/')[0] for x in temp_df['Season']]
        temp_df['£'] = [float(x.split('£')[1]) for x in temp_df['£']]
        player_stats[name]['history'] = temp_df
    except KeyError:
        player_stats[name]['history'] = None
    
    # clean the stats dataframe
    temp_df = player_stats[name]['stats']
    try:
        drop_row = temp_df.loc[temp_df['OPP'] == [x for x in temp_df['OPP'] if len(x.split(' ')) < 5][0]].index[0]
        temp_df = temp_df.drop([drop_row])
    except IndexError:
        pass
    # Create new columns using the strings in the opposition column
    temp_df['home_team'] = [x.split(' ')[0] if '(A)' in x else player_stats[name]['details']['club']  for x in temp_df['OPP']]
    temp_df['away_team'] = [x.split(' ')[0] if '(H)' in x else player_stats[name]['details']['club']  for x in temp_df['OPP']]
    temp_df['home_score'] = [x.split(' ')[2] for x in temp_df['OPP']]
    temp_df['away_score'] = [x.split(' ')[4] for x in temp_df['OPP']]
    temp_df['£'] = [float(x.split('£')[1]) for x in temp_df['£']]
    
    # Delete the opposition column
    del temp_df['OPP']
    
    # Rename the columns
    temp_df.columns = ['GameWeek','Points','MinutesPlayed','GoalsScored','Assists',
                       'CleanSheets','GoalsConceded','OwnGoals',
                       'PenaltySaves','PenaltyMisses','YellowCards',
                       'RedCards','Saves','Bonus','BonusPointSystem',
                       'Influence','Creativity','Threat','IctIndex',
                       'NetTransfers', 'SelectedBy', '£', 'home_team',
                       'away_team', 'home_goals', 'away_goals']
    # Reorder columns
    player_stats[name]['stats'] = temp_df[['GameWeek','home_team','away_team','home_goals',
                        'away_goals','Points','MinutesPlayed','GoalsScored','Assists',
                       'CleanSheets','GoalsConceded','OwnGoals',
                       'PenaltySaves','PenaltyMisses','YellowCards',
                       'RedCards','Saves','Bonus','BonusPointSystem',
                       'Influence','Creativity','Threat','IctIndex',
                       'NetTransfers', 'SelectedBy', '£']]
    
    # Map full names onto club names
    player_stats[name]['details']['club'] = team_name_map[player_stats[name]['details']['club']]

# Save dictionary to path as pickle file
path = open(r'C:\Users\charl\Desktop\FantasyFootball\Players\player_stats_cleaned.pk', 'wb')
pickle.dump(player_stats, path)        
