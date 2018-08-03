import pandas as pd
import numpy as np
import calc_es_ind_metrics as es_metrics


def calc_pp_faceoffs(pbp_df, pp_skaters_num, pk_skaters_num):
    '''
    calculate the faceoffs won and lost by a player whose team is on the power
    player

    Inputs:
    pbp_df - play by play dataframe
    pp_skaters_num - number of skaters for team on the power play
    pk_skaters_num - number of skaters for team on the penalty kill

    Outputs
    fo_df - dataframe of FOW and FOL for teams on the PP
    '''

    home_5v4_df = pbp_df[(pbp_df.Home_Players == pp_skaters_num) &
                         (pbp_df.Away_Players == pk_skaters_num) &
                         (~pbp_df.Home_Goalie.isna())]

    away_5v4_df = pbp_df[(pbp_df.Home_Players == pk_skaters_num) &
                         (pbp_df.Away_Players == pp_skaters_num) &
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

    fo_5v4 = fo_5v4[['season', 'Game_Id', 'Date', 'player_id',
                             'player_name', 'FOW', 'FOL']]

    fo_5v4.loc[:, ('season', 'Game_Id', 'player_id', 'FOW', 'FOL')] = \
    fo_5v4.loc[:, ('season', 'Game_Id', 'player_id', 'FOW', 'FOL')].astype(int)


    return fo_5v4


def calc_pp_ind_points(pbp_df, pp_skaters_num, pk_skaters_num):
    '''
    This function calculates the individual goals and assists scored while at
    a strength state of 5v4

    Input:
    pbp_df - play by play dataframe

    Output:
    five_v_4_df - play by play dataframe of events taken at 5v4 strength
    '''

    home_pp_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Home_Team) &
                        (pbp_df.Home_Players == pp_skaters_num) &
                        (pbp_df.Away_Players == pk_skaters_num) &
                        (~pbp_df.Home_Goalie.isna())]

    away_pp_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Away_Team) &
                        (pbp_df.Home_Players == pk_skaters_num) &
                        (pbp_df.Away_Players == pp_skaters_num) &
                        (~pbp_df.Home_Goalie.isna())]

    home_pp_points = es_metrics.calc_ind_points(home_pp_df)
    print(home_pp_points)

    away_pp_points = es_metrics.calc_ind_points(away_pp_df)

    print(away_pp_points)
    pts_pp = [home_pp_points, away_pp_points]

    pts_pp_df = pd.concat(pts_pp, sort=False)


    pts_pp_df = pts_pp_df[['season', 'Game_Id', 'Date', 'player_id',
                             'player_name', 'g', 'a1', 'a2']]

    pts_pp_df.loc[:, ('season', 'Game_Id')] = pts_pp_df.loc[:, ('season', 'Game_Id')].astype(int)

    return pts_pp_df

def calc_pp_penalties(pbp_df, pp_skaters_num, pk_skaters_num):
    '''
    function to calculate penalties drawn and taken for teams on the
    '''

    home_pp_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Home_Team) &
                        (pbp_df.Home_Players == pp_skaters_num) &
                        (pbp_df.Away_Players == pk_skaters_num) &
                        (pbp_df.is_penalty > 0) &
                        (~pbp_df.Home_Goalie.isna())]

    away_pp_df = pbp_df[(pbp_df.Ev_Team == pbp_df.Away_Team) &
                        (pbp_df.Home_Players == pk_skaters_num) &
                        (pbp_df.Away_Players == pp_skaters_num) &
                        (pbp_df.is_penalty > 0) &
                        (~pbp_df.Home_Goalie.isna())]

    home_pent = home_pp_df[(home_pp_df.Event == 'PENL') &
                    ((home_pp_df.p1_ID == home_pp_df.homePlayer1_id) |
                     (home_pp_df.p1_ID == home_pp_df.homePlayer2_id) |
                     (home_pp_df.p1_ID == home_pp_df.homePlayer3_id) |
                     (home_pp_df.p1_ID == home_pp_df.homePlayer4_id) |
                     (home_pp_df.p1_ID == home_pp_df.homePlayer5_id) |
                     (home_pp_df.p1_ID == home_pp_df.homePlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p1_ID', 'p1_name'])['is_penalty'].sum().\
                 reset_index()

    home_pent.columns = ['season', 'Game_Id', 'Date',
                         'player_id', 'player_name', 'PENT']

    home_pend = home_pp_df[(home_pp_df.Event == 'PENL') &
                    ((home_pp_df.p2_ID == home_pp_df.homePlayer1_id) |
                     (home_pp_df.p2_ID == home_pp_df.homePlayer2_id) |
                     (home_pp_df.p2_ID == home_pp_df.homePlayer3_id) |
                     (home_pp_df.p2_ID == home_pp_df.homePlayer4_id) |
                     (home_pp_df.p2_ID == home_pp_df.homePlayer5_id) |
                     (home_pp_df.p2_ID == home_pp_df.homePlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p2_ID', 'p2_name'])['is_penalty'].sum().\
                 reset_index()

    home_pend.columns = ['season', 'Game_Id', 'Date',
                         'player_id', 'player_name', 'PEND']

    home_pp_penl = home_pent.merge(home_pend,
                                       on=['season', 'Game_Id', 'Date',
                                           'player_id', 'player_name'],
                                       how='outer')

    away_pent = away_pp_df[(away_pp_df.Event == 'PENL') &
                    ((away_pp_df.p1_ID == away_pp_df.awayPlayer1_id) |
                     (away_pp_df.p1_ID == away_pp_df.awayPlayer2_id) |
                     (away_pp_df.p1_ID == away_pp_df.awayPlayer3_id) |
                     (away_pp_df.p1_ID == away_pp_df.awayPlayer4_id) |
                     (away_pp_df.p1_ID == away_pp_df.awayPlayer5_id) |
                     (away_pp_df.p1_ID == away_pp_df.awayPlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p1_ID', 'p1_name'])['is_penalty'].sum().\
                 reset_index()

    away_pent.columns = ['season', 'Game_Id', 'Date',
                         'player_id', 'player_name', 'PENT']

    away_pend = away_pp_df[(away_pp_df.Event == 'PENL') &
                    ((away_pp_df.p2_ID == away_pp_df.awayPlayer1_id) |
                     (away_pp_df.p2_ID == away_pp_df.awayPlayer2_id) |
                     (away_pp_df.p2_ID == away_pp_df.awayPlayer3_id) |
                     (away_pp_df.p2_ID == away_pp_df.awayPlayer4_id) |
                     (away_pp_df.p2_ID == away_pp_df.awayPlayer5_id) |
                     (away_pp_df.p2_ID == away_pp_df.awayPlayer6_id))].\
                 groupby(['season', 'Game_Id', 'Date',
                          'p2_ID', 'p2_name'])['is_penalty'].sum().\
                 reset_index()

    away_pend.columns = ['season', 'Game_Id', 'Date',
                         'player_id', 'player_name', 'PEND']

    away_pp_penl = away_pent.merge(away_pend, on=['season', 'Game_Id', 'Date',
                                                  'player_id', 'player_name'],
                                   how='outer')

    penl_dfs = [home_pp_penl, away_pp_penl]

    pp_penl_dfs = pd.concat(penl_dfs, sort=True)

    pp_penl_dfs = pp_penl_dfs.fillna(0)

    pp_penl_dfs = pp_penl_dfs[['season', 'Game_Id', 'Date', 'player_id',
                               'player_name', 'PENT', 'PEND']]

    pp_penl_dfs.loc[:, ('season', 'Game_Id', 'player_id', 'PENT', 'PEND')] = \
    pp_penl_dfs.loc[:, ('season', 'Game_Id', 'player_id', 'PENT', 'PEND')].astype(int)

    return pp_penl_dfs
