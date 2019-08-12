import os

from datetime import datetime, timedelta

import pandas as pd

from dateutil.parser import parse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def StringWeek(x):
    if x == 'Mon':
        y = 0
    elif x == 'Tue':
        y = 1
    elif x == 'Wed':
        y = 2
    elif x == 'Thu':
        y = 3
    elif x == 'Fri':
        y = 4
    elif x == 'Sat':
        y = 5
    elif x == 'Sun':
        y = 6
    else:
        y = None
    return y


def clean_table(df):

    date_time = []
    home_team = []
    away_team = []

    for row in enumerate(df['Teams']):
        # Get info on which rows have datetime and store
        # parse() will return an error for unrecognized date formats
        try:
            parse(row[1])
            date = row[1]
        except:
            teams = row[1].split(' v ')
            home_team.append(''.join([x for x in teams[0] if not x.isdigit()]).strip())
            away_team.append(''.join([x for x in teams[1] if not x.isdigit()]).strip())
            pass
        # Get today's date
        today = datetime.today().date()
        # Get the weekday
        current_day = today.weekday()
        # Get the weekday of the fixture
        game_day = StringWeek(date.split(' ')[0])
        # Calculate the date given the above
        if game_day is None:
            days_from = 0
        else:
            days_from = game_day - current_day
        match_date = today + timedelta(days = days_from)
        # if the datetime value is smaller than last, add one week
        while row[0] > 0 and match_date < max(date_time):
            match_date = match_date + timedelta(weeks = 1)
        # Store values in a list
        date_time.append(match_date)
    # Add datetime as a dataframe column
    df['datetime'] = date_time
    # Remove NaN rows
    df = df.dropna()
    return df, home_team, away_team, df['datetime']


def str_odds_to_prob(fraction_str):
    split_str = fraction_str.split('/')
    return (float(split_str[1]) / (float(split_str[1]) + float(split_str[0])))


def normalise_probs(odds, total):
    return odds / total


def df_str_to_float(df, h_team, a_team, date):

    home_win = []
    draw = []
    away_win = []
        
    # Transform odds string into floats
    for row in range(len(df)):
        h_prob = str_odds_to_prob(df.iloc[row,1].split(' ')[0])
        d_prob = str_odds_to_prob(df.iloc[row,2].split(' ')[0])
        a_prob = str_odds_to_prob(df.iloc[row,3].split(' ')[0])
        total = h_prob + d_prob + a_prob
        
        home_win.append(normalise_probs(h_prob, total))
        draw.append(normalise_probs(d_prob, total))
        away_win.append(normalise_probs(a_prob, total))
    
    cleaned_pl_data = pd.DataFrame({'home_team':h_team,'away_team':a_team,
                                    'home_win':home_win,'draw':draw,
                                    'away_win':away_win,'date_time':date})
    
    return cleaned_pl_data[[
            'home_team','away_team','home_win','draw','away_win','date_time'
            ]]


def get_sb_odds():
    
    fixtures_url = 'https://m.skybet.com/football/competitions'
    driver.get(fixtures_url)
    
    pl = 'table.market-table.competitions-premier-league.competitions-premier-league-matches'
    tbl = driver.find_element_by_css_selector(pl).get_attribute('outerHTML')
    premier_league_data = pd.read_html(tbl)[0]
    
    data = clean_table(premier_league_data)
    df = df_str_to_float(data[0], data[1], data[2], data[3])
    
    # Create a new file with the date
    date = str(datetime.now()).split(' ')[0].replace('-','_')
    path = f'{os.path.dirname(os.getcwd())}\\data\\SkyBet\\\PL_Odds_{date}.csv'
    df.to_csv(path, index = 0, sep = ',')



if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    delay = 3
    get_sb_odds()

