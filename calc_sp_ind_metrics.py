import pandas as pd
import numpy as np
import calc_es_ind_metrics as es_metrics


def calc_5v4_faceoffs(pbp_df):
    '''
    calculate the faceoffs won and lost by a player whose team is on the power
    player at 5v4 strength

    Inputs:
    pbp_df - play by play dataframe

    Outputs - dataframe of FOW and FOL at 5v4 strength
    '''

    home_5v4_df = pbp_df[(pbp_df.Home_Players == 6) &
                         (pbp_df.Away_Players == 5) &
                         (~pbp_df.Home_Goalie.isna())]

    away_5v4_df = pbp_df[(pbp_df.Home_Players == 5) &
                         (pbp_df.Away_Players == 6) &
                         (~pbp_df.Away_Goalie.isna())]

    home_fo_won = home_5v4_df[(home_5v4_df.Event == 'FAC') &
                    ((home_5v4_df.p1_ID == home_5v4_df.homePlayer1_id) |
                     (home_5v4_df.p1_ID == home_5v4_df.homePlayer2_id) |
                     (home_5v4_df.p1_ID == home_5v4_df.homePlayer3_id) |
                     (home_5v4_df.p1_ID == home_5v4_df.homePlayer4_id) |
                     (home_5v4_df.p1_ID == home_5v4_df.homePlayer5_id) |
                     (home_5v4_df.p1_ID == home_5v4_df.homePlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p1_ID', 'p1_name']).size().\
                 reset_index()

    home_fo_won.columns = ['season', 'Game_Id', 'Date',
                      'player_id', 'player_name', 'FOW']

    home_fo_lost = home_5v4_df[(home_5v4_df.Event == 'FAC') &
                    ((home_5v4_df.p2_ID == home_5v4_df.homePlayer1_id) |
                     (home_5v4_df.p2_ID == home_5v4_df.homePlayer2_id) |
                     (home_5v4_df.p2_ID == home_5v4_df.homePlayer3_id) |
                     (home_5v4_df.p2_ID == home_5v4_df.homePlayer4_id) |
                     (home_5v4_df.p2_ID == home_5v4_df.homePlayer5_id) |
                     (home_5v4_df.p2_ID == home_5v4_df.homePlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p2_ID', 'p2_name']).size().\
                 reset_index()

    home_fo_lost.columns = ['season', 'Game_Id', 'Date',
                      'player_id', 'player_name', 'FOL']

    home_5v4_fo_df = home_fo_won.merge(home_fo_lost,
                                       on=['season', 'Game_Id', 'Date',
                                           'player_id', 'player_name'],
                                       how='outer')

    away_fo_won = away_5v4_df[(away_5v4_df.Event == 'FAC') &
                    ((away_5v4_df.p1_ID == away_5v4_df.awayPlayer1_id) |
                     (away_5v4_df.p1_ID == away_5v4_df.awayPlayer2_id) |
                     (away_5v4_df.p1_ID == away_5v4_df.awayPlayer3_id) |
                     (away_5v4_df.p1_ID == away_5v4_df.awayPlayer4_id) |
                     (away_5v4_df.p1_ID == away_5v4_df.awayPlayer5_id) |
                     (away_5v4_df.p1_ID == away_5v4_df.awayPlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p1_ID', 'p1_name']).size().\
                 reset_index()

    away_fo_won.columns = ['season', 'Game_Id', 'Date',
                      'player_id', 'player_name', 'FOW']

    away_fo_lost = away_5v4_df[(away_5v4_df.Event == 'FAC') &
                    ((away_5v4_df.p2_ID == away_5v4_df.awayPlayer1_id) |
                     (away_5v4_df.p2_ID == away_5v4_df.awayPlayer2_id) |
                     (away_5v4_df.p2_ID == away_5v4_df.awayPlayer3_id) |
                     (away_5v4_df.p2_ID == away_5v4_df.awayPlayer4_id) |
                     (away_5v4_df.p2_ID == away_5v4_df.awayPlayer5_id) |
                     (away_5v4_df.p2_ID == away_5v4_df.awayPlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p2_ID', 'p2_name']).size().\
                 reset_index()

    away_fo_lost.columns = ['season', 'Game_Id', 'Date',
                      'player_id', 'player_name', 'FOL']

    away_5v4_fo_df = away_fo_won.merge(away_fo_lost,
                                       on=['season', 'Game_Id', 'Date',
                                           'player_id', 'player_name'],
                                       how='outer')

    fo_dfs = [home_5v4_fo_df, away_5v4_fo_df]

    fo_5v4 = pd.concat(fo_dfs)

    fo_5v4 = fo_5v4.fillna(0)


    return fo_5v4


def calc_5v4_ind_points(pbp_df):
    '''
    This function calculates the individual goals and assists scored while at
    a strength state of 5v4

    Input:
    pbp_df - play by play dataframe

    Output:
    five_v_4_df - play by play dataframe of events taken at 5v4 strength
    '''

    home_5v4_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Home_Team) &
                         (pbp_df.Home_Players == 6) &
                         (pbp_df.Away_Players == 5) &
                         (~pbp_df.Home_Goalie.isna())]

    away_5v4_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Away_Team) &
                         (pbp_df.Home_Players == 5) &
                         (pbp_df.Away_Players == 6) &
                         (~pbp_df.Home_Goalie.isna())]

    home_5v4_points = es_metrics.calc_ind_points(home_5v4_df)
    print(home_5v4_points)

    away_5v4_points = es_metrics.calc_ind_points(away_5v4_df)

    print(away_5v4_points)
    pts_5v4 = [home_5v4_points, away_5v4_points]

    pts_5v4_df = pd.concat(pts_5v4, sort=False)


    pts_5v4_df = pts_5v4_df[['season', 'Game_Id', 'Date', 'player_id',
                             'player_name', 'g', 'a1', 'a2']]

    pts_5v4_df.loc[:, ('season', 'Game_Id')] = pts_5v4_df.loc[:, ('season', 'Game_Id')].astype(int)
    return pts_5v4_df
