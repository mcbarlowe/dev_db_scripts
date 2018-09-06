'''
This model will predict the probabilites of winners in NHL games by using the
poisson distirbution and monte carlo sampling
'''
import os
import datetime
from get_today_schedule import get_today_sched
import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def clean_results(results_df, team, date):
    '''
    this function cleans the results dataframe and just strips out the wanted
    team results and creates a column for OT goals as well
    '''
    results_df = results_df[results_df.game_date < date]
    cleaned_results = []
    #looping through the results_df to pull out only the games the team variable played in.
    for index, row in results_df.iterrows():
        if row.home_team == team:
            new_row = row[['game_id', 'game_type', 'season', 'game_date', 'home_team_id', 'home_team',
                           'home_score', 'away_score', 'ot_flag', 'shootout_flag', 'seconds_in_ot']]

            new_row.index = ['game_id', 'game_type', 'season', 'game_date', 'team_id', 'team',
                           'goals_for', 'goals_against', 'ot_flag', 'shootout_flag', 'seconds_in_ot']

            new_row['is_home'] = 1

            cleaned_results.append(new_row)

        elif row.away_team == team:
            new_row = row[['game_id', 'game_type', 'season', 'game_date', 'away_team_id', 'away_team',
                           'away_score', 'home_score', 'ot_flag', 'shootout_flag', 'seconds_in_ot']]

            new_row.index = ['game_id', 'game_type', 'season', 'game_date', 'team_id', 'team',
                           'goals_for', 'goals_against', 'ot_flag', 'shootout_flag', 'seconds_in_ot']

            new_row['is_home'] = 0

            cleaned_results.append(new_row)

    cleaned_df = pd.concat(cleaned_results, axis=1).T

    #calculating non ot goals by seeing if the game went to ot or shootout and if so whether the team won or not.
    #if they did then they score one less goals than their final total if not then they scored their same goals for
    #amount
    cleaned_df['non_ot_goals'] = np.where(((cleaned_df.shootout_flag == 1) | (cleaned_df.ot_flag == 1)) &
                                          (cleaned_df.goals_for > cleaned_df.goals_against), cleaned_df.goals_for - 1,
                                          cleaned_df.goals_for)

    cleaned_df['ot_goals'] = cleaned_df.goals_for - cleaned_df.non_ot_goals

    cleaned_df = cleaned_df.reset_index(drop=True)

    #only return the last two seasons of games
    cleaned_df = cleaned_df.iloc[:164, :]

    return cleaned_df

def test_monte_carlo():
    '''
    This function will run the simulations on a test data set to see how they
    perform on last seasons data.
    '''

    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))

    sql_query = 'SELECT * from nhl_tables.nhl_schedule'
    df = pd.read_sql(sql_query, con=engine,
                     parse_dates = {'game_date': '%Y-%m-%d'})




def main():

#gets todays date
    date = datetime.datetime.now().strftime('%Y-%m-%d')

#get daily schedule
    daily_sched = get_today_sched(date)

#TODO write code to query the results database to return the past two years
#of results for each team in each game

#TODO sort the data and adjust scoring for non OT and get OT and shootout win
#% for each team

#TODO run simulation using each teams distribution of goals scored in regulation
#for ties determine probability of both teams not scoring in OT from their OT
#poisson goal distributions. USe that p and (1-p) as a bernoulli trial to
#determine if game was decided in OT. If it is decided in OT use Bradley-Terry
#model to determine probability of home team winning with another Bernoulli trial.
#If the game is not decided in OT use another Bradley-Terry model with SO win %'s
#to determine probability of home team winning shootout.

    return

if __name__ == '__main__':
    main()

