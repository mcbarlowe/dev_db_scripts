'''
This model will predict the probabilites of winners in NHL games by using the
poisson distirbution and monte carlo sampling
'''
import os
import datetime
import multiprocessing as mp
from get_today_schedule import get_today_sched
import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def get_avg_df(df):
    '''
    This is to create an average of the time frame of the past results. This
    was only implemented because of Vegas who had no past results as an expansion
    team. I'm hoping to use this most likely with the new Seatle expansion team
    in the next couple years.

    Inputs:
    df - dataframe of past results

    Outputs:
    avg_df - a dataframe of avg results for games with no OT, OT and no Shootout,
             and games that goto shootout
    '''

#creates three different dataframes based on whether the game went to OT, SO,
#or ended in regulation
    reg = df[df.ot_flag != 1]
    ot = df[(df.ot_flag == 1) & (df.shootout_flag != 1)]
    shootout = df[df.shootout_flag == 1]

#creates averages for the results of the three dataframes which reduces them to
#one row
    reg_avg = reg[['home_score', 'away_score','seconds_in_ot']].mean()
    ot_avg = ot[['home_score', 'away_score', 'seconds_in_ot']].mean()
    shootout_avg = shootout[['home_score', 'away_score', 'seconds_in_ot']].mean()

#creates the ot_flag and shootout_flag that is in the table the data is pulled
#from. Will be neccesary for future calculations
    reg_avg['ot_flag'] = 0
    ot_avg['ot_flag'] = 1
    shootout_avg['ot_flag'] = 1

    reg_avg['shootout_flag'] = 0
    ot_avg['shootout_flag'] = 0
    shootout_avg['shootout_flag'] = 1

#combines the three series from average the three dataframes of the three types
#of game outcomes: Regulation, Overtime, Shootout
    avg_df = pd.concat([reg_avg, ot_avg, shootout_avg], axis=1).T

    #rename avg_df columns
    avg_df.columns = ['goals_for', 'goals_against', 'seconds_in_ot', 'ot_flag', 'shootout_flag']

#create columsn for ot and non ot_goals which will be used in the monte carlo
#simulations
    avg_df['non_ot_goals_for'] = np.where(((avg_df.shootout_flag == 1) | (avg_df.ot_flag == 1)) &
                                              (avg_df.goals_for > avg_df.goals_against), avg_df.goals_for - 1,
                                              avg_df.goals_for)
    avg_df['non_ot_goals_against'] = np.where(((avg_df.shootout_flag == 1) | (avg_df.ot_flag == 1)) &
                                              (avg_df.goals_for < avg_df.goals_against), avg_df.goals_against - 1,
                                              avg_df.goals_against)
    avg_df['ot_goals'] = np.where(avg_df.shootout_flag == 0,
                                          avg_df.goals_for - avg_df.non_ot_goals_for, 0)
    avg_df['ot_goals_against'] = np.where((avg_df.ot_flag == 1) & (avg_df.shootout_flag != 1), 1, 0)

    return avg_df

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
            #print(row)
            new_row = row[['game_id', 'game_type', 'season', 'game_date', 'home_team_id', 'home_team',
                           'home_score', 'away_score', 'ot_flag', 'shootout_flag', 'seconds_in_ot']]

            #print(new_row)
            new_row.index = ['game_id', 'game_type', 'season', 'game_date', 'team_id', 'team',
                           'goals_for', 'goals_against', 'ot_flag', 'shootout_flag', 'seconds_in_ot']

            new_row['is_home'] = 1

            cleaned_results.append(new_row)

        elif row.away_team == team:
            #print(row)
            new_row = row[['game_id', 'game_type', 'season', 'game_date', 'away_team_id', 'away_team',
                           'away_score', 'home_score', 'ot_flag', 'shootout_flag', 'seconds_in_ot']]
            #print(new_row)
            new_row.index = ['game_id', 'game_type', 'season', 'game_date', 'team_id', 'team',
                           'goals_for', 'goals_against', 'ot_flag', 'shootout_flag', 'seconds_in_ot']

            new_row['is_home'] = 0

            #print(new_row)
            cleaned_results.append(new_row)

    cleaned_df = pd.concat(cleaned_results, axis=1).T

    #calculating non ot goals by seeing if the game went to ot or shootout and if so whether the team won or not.
    #if they did then they score one less goals than their final total if not then they scored their same goals for
    #amount
    cleaned_df['non_ot_goals_for'] = np.where(((cleaned_df.shootout_flag == 1) | (cleaned_df.ot_flag == 1)) &
                                          (cleaned_df.goals_for > cleaned_df.goals_against), cleaned_df.goals_for - 1,
                                          cleaned_df.goals_for)
    cleaned_df['non_ot_goals_against'] = np.where(((cleaned_df.shootout_flag == 1) | (cleaned_df.ot_flag == 1)) &
                                          (cleaned_df.goals_for < cleaned_df.goals_against), cleaned_df.goals_against - 1,
                                          cleaned_df.goals_against)
    cleaned_df['ot_goals'] = np.where(cleaned_df.shootout_flag == 0,
                                      cleaned_df.goals_for - cleaned_df.non_ot_goals_for, 0)
    cleaned_df['ot_goals_against'] = np.where(cleaned_df.shootout_flag == 0,
                                              cleaned_df.goals_against - cleaned_df.non_ot_goals_against,0)

    cleaned_df = cleaned_df.reset_index(drop=True)

    #only return the last two seasons of games
    cleaned_df = cleaned_df.sort_values(by=['game_date'], ascending=False).iloc[:83, :]

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

#if schedule is empty exit program
    if not daily_sched:
        return

#Query the results database to return past results

    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))
    sql_query = 'SELECT * from nhl_tables.nhl_schedule'
    df = pd.read_sql(sql_query, con=engine,
                     parse_dates = {'game_date': '%Y-%m-%d'})

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

