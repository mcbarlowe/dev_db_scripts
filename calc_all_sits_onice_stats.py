import pandas as pd
import numpy as np

def calc_on_ice_shots(pbp_df):
    '''
    function to calculate on ice shot metrics for all situations

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    on_ice_shots_df - dataframe of on ice shot events while player was on ice
    '''

    home_shots_for_1 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer1_id', 'homePlayer1'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_1 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer1_id', 'homePlayer1'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_for_2 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer2_id', 'homePlayer2'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_2 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer2_id', 'homePlayer2'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_for_3 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer3_id', 'homePlayer3'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_3 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer3_id', 'homePlayer3'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_for_4 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer4_id', 'homePlayer4'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_4 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer4_id', 'homePlayer4'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_for_5 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer5_id', 'homePlayer5'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_5 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer5_id', 'homePlayer5'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_for_6 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer6_id', 'homePlayer6'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    home_shots_against_6 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'homePlayer6_id', 'homePlayer6'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

#refactor this into a for loop and store all the dataframes into a list probably
#can do the same with the code above
    home_shots_for_1.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_1.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    home_onice_1 = home_shots_for_1.merge(home_shots_against_1,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_1 = home_onice_1.fillna(0)

    home_onice_1.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_1\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    home_shots_for_2.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_2.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    home_onice_2 = home_shots_for_2.merge(home_shots_against_2,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_2 = home_onice_2.fillna(0)

    home_onice_2.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_2\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    home_shots_for_3.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_3.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']


    home_onice_3 = home_shots_for_3.merge(home_shots_against_3,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_3 = home_onice_3.fillna(0)

    home_onice_3.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_3\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)
    home_shots_for_4.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_4.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    home_onice_4 = home_shots_for_4.merge(home_shots_against_4,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_4 = home_onice_4.fillna(0)

    home_onice_4.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_4\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    home_shots_for_5.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_5.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    home_onice_5 = home_shots_for_5.merge(home_shots_against_5,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_5 = home_onice_5.fillna(0)

    home_onice_5.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_5\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    home_shots_for_6.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    home_shots_against_6.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    home_onice_6 = home_shots_for_6.merge(home_shots_against_6,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    home_onice_6 = home_onice_6.fillna(0)

    home_onice_6.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = home_onice_6\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    home_onice_list = [home_onice_1, home_onice_2, home_onice_3, home_onice_4,
                       home_onice_5, home_onice_6]

    home_metrics = pd.concat(home_onice_list)

    home_metrics = home_metrics.groupby(['season', 'Game_Id', 'Date',
                                         'player_id', 'player_name'])\
                                ['CF', 'CA', 'FF', 'FA', 'SF', 'SA', 'GF', 'GA'].sum().reset_index()

    away_shots_for_1 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer1_id', 'awayPlayer1'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_1 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer1_id', 'awayPlayer1'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_2 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer2_id', 'awayPlayer2'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_2 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer2_id', 'awayPlayer2'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_3 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer3_id', 'awayPlayer3'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_3 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer3_id', 'awayPlayer3'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_4 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer4_id', 'awayPlayer4'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_4 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer4_id', 'awayPlayer4'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_5 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer5_id', 'awayPlayer5'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_5 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer5_id', 'awayPlayer5'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_6 = pbp_df[pbp_df.is_home == 0]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer6_id', 'awayPlayer6'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_against_6 = pbp_df[pbp_df.is_home == 1]\
                          .groupby(['season', 'Game_Id', 'Date',
                                    'awayPlayer6_id', 'awayPlayer6'])\
                                  ['is_corsi', 'is_fenwick',
                                   'is_shot', 'is_goal'].sum().reset_index()

    away_shots_for_1.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_1.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    away_onice_1 = away_shots_for_1.merge(away_shots_against_1,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_1 = away_onice_1.fillna(0)

    away_onice_1.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_1\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_shots_for_2.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_2.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    away_onice_2 = away_shots_for_2.merge(away_shots_against_2,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_2 = away_onice_2.fillna(0)

    away_onice_2.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_2\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_shots_for_3.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_3.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']


    away_onice_3 = away_shots_for_3.merge(away_shots_against_3,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_3 = away_onice_3.fillna(0)

    away_onice_3.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_3\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_shots_for_4.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_4.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    away_onice_4 = away_shots_for_4.merge(away_shots_against_4,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_4 = away_onice_4.fillna(0)

    away_onice_4.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_4\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_shots_for_5.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_5.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    away_onice_5 = away_shots_for_5.merge(away_shots_against_5,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_5 = away_onice_5.fillna(0)

    away_onice_5.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_5\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_shots_for_6.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                'player_name', 'CF', 'FF', 'SF', 'GF']
    away_shots_against_6.columns = ['season', 'Game_Id', 'Date', 'player_id',
                                    'player_name', 'CA', 'FA', 'SA', 'GA']

    away_onice_6 = away_shots_for_6.merge(away_shots_against_6,
                                          on=['season', 'Game_Id', 'Date',
                                              'player_id', 'player_name'],
                                          how='outer')

    away_onice_6 = away_onice_6.fillna(0)

    away_onice_6.loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                         'GF', 'CA', 'FA', 'SA', 'GA')] = away_onice_6\
                    .loc[:, ('season', 'Game_Id', 'player_id', 'CF', 'FF', 'SF',
                             'GF', 'CA', 'FA', 'SA', 'GA')].astype(int)

    away_onice_list = [away_onice_1, away_onice_2, away_onice_3, away_onice_4,
                       away_onice_5, away_onice_6]

    away_metrics = pd.concat(away_onice_list)

    away_metrics = away_metrics.groupby(['season', 'Game_Id', 'Date',
                                         'player_id', 'player_name'])\
                                ['CF', 'CA', 'FF', 'FA', 'SF', 'SA', 'GF', 'GA'].sum().reset_index()

    away_metrics['team'] = pbp_df.Away_Team
    home_metrics['team'] = pbp_df.Home_Team

    shot_metrics = [away_metrics, home_metrics]

    shot_metrics_df = pd.concat(shot_metrics, sort=False)

    shot_metrics_df = shot_metrics_df[['season', 'Game_Id', 'Date', 'team',
                                       'player_id',
                                       'player_name', 'CF', 'CA', 'FF', 'FA',
                                       'SF', 'SA', 'GF', 'GA']]
    return shot_metrics_df


def main():

    return

if __name__ == '__main__':
    main()
