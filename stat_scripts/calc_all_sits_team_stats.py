import pandas as pd
import numpy as np

def calc_all_sits_team_metrics(pbp_df):
    '''
    This function calculates team metrics for all sits and returns a dataframe
    with the calulated stat dataframe

    Input:
    pbp_df - play by play dataframe

    Output:
    all_sits_team_df - data frame of calculated team stats
    '''

    corsi = ['SHOT', 'BLOCK', 'MISS', 'GOAL']
    fenwick = ['SHOT', 'MISS', 'GOAL']
    shot = ['SHOT', 'GOAL']

    pbp_df['home_corsi'] = np.where((pbp_df['event'].isin(corsi)) &
                                    (pbp_df['is_home'] == 1), 1, 0)
    pbp_df['home_fenwick'] = np.where((pbp_df['event'].isin(fenwick)) &
                                    (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_shot'] = np.where((pbp_df['event'].isin(shot)) &
                                    (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_goal'] = np.where((pbp_df['is_goal'] == 1) &
                                    (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_xg'] = np.where(pbp_df['is_home'] == 1, pbp_df['xg'], 0)

    pbp_df['home_pen'] = np.where((pbp_df['is_penalty'] == 1) &
                                (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_blk'] = np.where((pbp_df['event'] == 'BLOCK') &
                                (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_hits'] = np.where((pbp_df['event'] == 'HIT') &
                                   (pbp_df['is_home'] ==1), 1, 0)

    pbp_df['home_give'] = np.where((pbp_df['event'] == 'GIVE') &
                                   (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_take'] = np.where((pbp_df['event'] == 'TAKE') &
                                   (pbp_df['is_home'] == 1), 1, 0)

    pbp_df['home_face'] = np.where((pbp_df['event'] == 'FAC') &
                                   (pbp_df['ev_team'] == pbp_df['home_team']),
                                   1,0)

    pbp_df['home_xg_adj'] = np.where(pbp_df['is_home'] == 1, pbp_df['xg_adj'], 0)

    pbp_df['home_corsi_adj'] = np.where((pbp_df['event'].isin(corsi)) &
                                    (pbp_df['is_home'] == 1), pbp_df['corsi_adj'], 0)
    pbp_df['home_fenwick_adj'] = np.where((pbp_df['event'].isin(fenwick)) &
                                    (pbp_df['is_home'] == 1), pbp_df['fenwick_adj'], 0)

    pbp_df['away_corsi'] = np.where((pbp_df['event'].isin(corsi)) &
                                    (pbp_df['is_home'] == 0), 1, 0)
    pbp_df['away_fenwick'] = np.where((pbp_df['event'].isin(fenwick)) &
                                    (pbp_df['is_home'] == 0 ), 1, 0)

    pbp_df['away_shot'] = np.where((pbp_df['event'].isin(shot)) &
                                    (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_goal'] = np.where((pbp_df['is_goal'] == 1) &
                                    (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_xg'] = np.where(pbp_df['is_home'] == 1, pbp_df['xg'], 0)

    pbp_df['away_pen'] = np.where((pbp_df['is_penalty'] == 1) &
                                (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_blk'] = np.where((pbp_df['event'] == 'BLOCK') &
                                (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_hits'] = np.where((pbp_df['event'] == 'HIT') &
                                   (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_give'] = np.where((pbp_df['event'] == 'GIVE') &
                                   (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_take'] = np.where((pbp_df['event'] == 'TAKE') &
                                   (pbp_df['is_home'] == 0), 1, 0)

    pbp_df['away_face'] = np.where((pbp_df['event'] == 'FAC') &
                                   (pbp_df['ev_team'] == pbp_df['away_team']),
                                   1,0)

    pbp_df['home_xg_adj'] = np.where(pbp_df['is_home'] == 0, pbp_df['xg_adj'], 0)

    pbp_df['home_corsi_adj'] = np.where((pbp_df['event'].isin(corsi)) &
                                    (pbp_df['is_home'] == 0), pbp_df['corsi_adj'], 0)
    pbp_df['home_fenwick_adj'] = np.where((pbp_df['event'].isin(fenwick)) &
                                    (pbp_df['is_home'] == 0), pbp_df['fenwick_adj'], 0)

    home_stats = pbp_df.groupby(['season', 'game_id', 'date', 'home_team'])\
            ['home_corsi', 'away_corsi', 'home_fenwick', 'away_fenwick',
             'home_shot', 'away_shot', 'home_goal', 'away_goal', 'home_xg',
             'away_xg', 'home_pen', 'away_pen', 'home_hits', 'away_hits',
             'home_blk', 'home_give', 'home_take', 'home_face', 'away_face',
             'home_xg_adj', 'away_xg_adj', 'home_corsi_adj', 'away_corsi_adj',
             'home_fenwick_adj', 'away_fenwick_adj'].sum().reset_index(drop=True)

    away_stats = pbp_df.groupby(['season', 'game_id', 'date', 'away_team'])\
            ['away_corsi', 'home_corsi', 'away_fenwick', 'home_fenwick',
             'away_shot', 'home_shot', 'away_goal', 'home_goal', 'away_xg',
             'home_xg', 'away_pen', 'home_pen', 'away_hits', 'home_hits',
             'away_blk', 'away_give', 'away_take', 'away_face', 'home_face',
             'away_xg_adj', 'home_xg_adj', 'away_corsi_adj', 'home_corsi_adj',
             'away_fenwick_adj', 'home_fenwick_adj'].sum().reset_index(drop=True)


    home_stats.columns = ['cf', 'ca', 'ff', 'fa', 'sf', 'sa', 'gf', 'ga', 'xgf',
                          'xga', 'pend', 'pent', 'hf', 'ha', 'blk', 'give', 'take',
                          'fow', 'fol', 'xgf_adj', 'xga_adj', 'cf_adj', 'ca_adj',
                          'ff_adj', 'fa_adj']

    away_stats.columns = ['cf', 'ca', 'ff', 'fa', 'sf', 'sa', 'gf', 'ga', 'xgf',
                          'xga', 'pend', 'pent', 'hf', 'ha', 'blk', 'give', 'take',
                          'fow', 'fol', 'xgf_adj', 'xga_adj', 'cf_adj', 'ca_adj',
                          'ff_adj', 'fa_adj']

    #need to add in toi here
    team_stats = pd.concat([home_stats, away_stats])

    return team_stats


