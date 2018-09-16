'''
this function calculates the on ice stats of players at any given strength state
'''
import pandas as pd
import numpy as np

def calc_toi(pbp_df, first_skater_num, second_skater_num):
    '''
    This will calculate a players TOI for all situations in the game

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    toi_df - dataframe with each players TOI calculated
    '''

    home_str_df = pbp_df[(pbp_df.home_players == first_skater_num) &
                         (pbp_df.away_players == second_skater_num) &
                         (~pbp_df.home_goalie.isna())]

    away_str_df = pbp_df[(pbp_df.home_players == first_skater_num) &
                         (pbp_df.away_players == second_skater_num) &
                         (~pbp_df.away_goalie.isna())]
#compiling toi for each player column in the pbp_df to make sure that every
#player is accounted for as the player columns are not any set position
    home_1 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer1_id',
                             'homeplayer1'])['event_length'].sum().reset_index()
    home_2 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer2_id',
                             'homeplayer2'])['event_length'].sum().reset_index()
    home_3 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer3_id',
                             'homeplayer3'])['event_length'].sum().reset_index()
    home_4 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer4_id',
                             'homeplayer4'])['event_length'].sum().reset_index()
    home_5 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer5_id',
                             'homeplayer5'])['event_length'].sum().reset_index()
    home_6 = home_str_df.groupby(['season', 'game_id', 'date', 'homeplayer6_id',
                             'homeplayer6'])['event_length'].sum().reset_index()

    away_1 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer1_id',
                             'awayplayer1'])['event_length'].sum().reset_index()
    away_2 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer2_id',
                             'awayplayer2'])['event_length'].sum().reset_index()
    away_3 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer3_id',
                             'awayplayer3'])['event_length'].sum().reset_index()
    away_4 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer4_id',
                             'awayplayer4'])['event_length'].sum().reset_index()
    away_5 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer5_id',
                             'awayplayer5'])['event_length'].sum().reset_index()
    away_6 = away_str_df.groupby(['season', 'game_id', 'date', 'awayplayer6_id',
                             'awayplayer6'])['event_length'].sum().reset_index()

    print(home_1.head())
#making all the dataframes the same to that I can concat them
    home_1.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    home_2.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    home_3.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    home_4.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    home_5.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    home_6.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']

    away_1.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    away_2.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    away_3.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    away_4.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    away_5.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']
    away_6.columns = ['season', 'game_id', 'date', 'player_id', 'player_name', 'toi']

#joining all the seperate toi dataframes into one big dataframe that I will
#group by and sum their TOI
    home_toi = pd.concat([home_1, home_2, home_3, home_4, home_5, home_6])

    print(home_toi.dtypes)
    away_toi = pd.concat([away_1, away_2, away_3, away_4, away_5, away_6])
    print(away_toi.dtypes)
    away_toi = away_toi.groupby(['season', 'game_id', 'date', 'player_id', 'player_name'])['toi'].sum().reset_index()
    home_toi = home_toi.groupby(['season', 'game_id', 'date', 'player_id', 'player_name'])['toi'].sum().reset_index()

    toi_df = pd.concat([home_toi, away_toi])

    toi_df = toi_df.groupby(['player_id', 'player_name'])['toi'].sum().reset_index()

    return toi_df

