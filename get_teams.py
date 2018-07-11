import os
import requests
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def get_teams():
    '''
    This function gets the NHL schedule from the NHL api and
    returns a dictionary

    Inputs:
    start_date - string of the first date to pass to the api url
    end_date - string of the end date for the api url

    Outputs:
    schedule_dict - dictionary created from api JSON
    '''

    api_url = ('https://statsapi.web.nhl.com/api/v1/teams')

    req = requests.get(api_url)
    teams_dict = req.json()

    return teams_dict

def create_team_df(team_dict):
    '''
    This function flatten out the API json into a flat table scructure
    with the relevant stats for the SQL table

    Inputs:
    schedule_dict - dicitonary of the API GET request

    Outputs
    sched_df - pandas dataframe to be inserted into schedule table
    '''

    team_list = []
    for team in team_dict['teams']:
        team_id = team['id']
        name = team['name']
        abbrev = team['abbreviation']
        division = team['division']['name']
        conference = team['conference']['name']
        active = team['active']

        print([team_id, name, abbrev, division,
               conference, active])

        team_list.append([team_id, name, abbrev, division,
                          conference, active])

    team_df_columns = ['team_id', 'name', 'abbrev', 'division',
                       'conference', 'active']

    team_df = pd.DataFrame(team_list, columns=team_df_columns)

    print('Dataframe created')
    return team_df

def team_insert(df):

    print('Inserting DataFrame to the Database')
    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))
    df.to_sql('nhl_teams', schema='nhl_tables', con=engine,
              if_exists='append', index=False)

def main():
    '''
    This script pulls the schedule data of past games and the results
    of each game and inserts them into an Postgres table
    '''

    team_dict = get_teams()

    team_df = create_team_df(team_dict)
    team_insert(team_df)


if __name__ == '__main__':
    main()
