import sys
import os
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def get_schedule(date):
    '''
    This function gets the NHL schedule from the NHL api and
    returns a dictionary

    Inputs:
    start_date - string of the first date to pass to the api url
    end_date - string of the end date for the api url

    Outputs:
    schedule_dict - dictionary created from api JSON
    '''

    api_url = ('https://statsapi.web.nhl.com/api/v1/schedule?'
               'startDate={}').format(date)

    req = requests.get(api_url)
    schedule_dict = req.json()

    return schedule_dict

def create_sched_df(schedule_dict):
    '''
    This function flatten out the API json into a flat table scructure
    with the relevant stats for the SQL table

    Inputs:
    schedule_dict - dicitonary of the API GET request

    Outputs
    sched_df - pandas dataframe to be inserted into schedule table
    '''

    master_sched = []
    for item in schedule_dict['dates']:
        games = item['games']

        game_date = item['date']
        for game in games:
            game_id = game['gamePk']
            game_type = game['gameType']
            season = game['season']
            home_id = game['teams']['home']['team']['id']
            home_team = game['teams']['home']['team']['name']
            home_score = game['teams']['home']['score']
            away_id = game['teams']['away']['team']['id']
            away_team = game['teams']['away']['team']['name']
            away_score = game['teams']['away']['score']

            master_sched.append([game_id, game_type, season, game_date,
                          home_id, home_team, home_score, away_id,
                          away_team, away_score])

    sched_df_columns = ['game_id', 'game_type', 'season', 'game_date',
                        'home_team_id', 'home_team', 'home_score',
                        'away_team_id',
                        'away_team', 'away_score']
    sched_df = pd.DataFrame(master_sched, columns=sched_df_columns)

    print('Dataframe created')
    return sched_df

def sched_insert(df):

    print('Inserting DataFrame to the Database')
    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))
    df.to_sql('nhl_schedule', schema='nhl_tables', con=engine,
              if_exists='append', index=False)

def main():
    '''
    This script pulls the schedule data of past games and the results
    of each game and inserts them into an Postgres table
    '''
    date = sys.argv[1]

    schedule_dict = get_schedule(date)

    if schedule_dict['totalItems'] == 0:
        print("No Games Today")
        return
    else:
        sched_df = create_sched_df(schedule_dict)
        sched_insert(sched_df)


if __name__ == '__main__':
    main()
