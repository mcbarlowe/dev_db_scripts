import pandas as pd
import numpy as np

score_venue_adj_dic = {-3: {'home_weight': .850, 'away_weight': 1.214},
                       -2: {'home_weight': .882, 'away_weight': 1.154},
                       -1: {'home_weight': .915, 'away_weight': 1.103},
                       0: {'home_weight': .970, 'away_weight': 1.032},
                       1: {'home_weight': 1.026, 'away_weight': .975},
                       2: {'home_weight': 1.074, 'away_weight': .936},
                       3: {'home_weight': 1.132, 'away_weight': .895}}

wght_shots_goals = {-3: {'home_weight': .943, 'away_weight': 1.057},
                    -2: {'home_weight': .976, 'away_weight': 1.024},
                    -1: {'home_weight': .936, 'away_weight': 1.064},
                    0: {'home_weight': .942, 'away_weight': 1.058},
                    1: {'home_weight': .995, 'away_weight': 1.005},
                    2: {'home_weight': 1.01, 'away_weight': .990},
                    3: {'home_weight': 1.017, 'away_weight': .983}}

wght_shots_shot = {-3: {'home_weight': .163, 'away_weight': .237},
                   -2: {'home_weight': .171, 'away_weight': .229},
                   -1: {'home_weight': .180, 'away_weight': .220},
                   0: {'home_weight': .196, 'away_weight': .204},
                   1: {'home_weight': .213, 'away_weight': .187},
                   2: {'home_weight': .221, 'away_weight': .179},
                   3: {'home_weight': .227, 'away_weight': .173}}

def switch_block_shots(pbp_df):
    '''
    This function switches the p1 and p2 of blocked shots because Harry's
    scraper lists p1 as the blocker instead of the shooter

    Inputs:
    pbp_df - dataframe of play by play to be cleaned

    Outputs:
    pbp_df - cleaned dataframe
    '''

    print(pbp_df.loc[:, ('p1_name', 'p1_ID', 'p2_name', 'p2_ID')].head(15))
#creating new columns where I switch the players around for blocked shots
    pbp_df.loc[:, ('new_p1_name')] = np.where(pbp_df.Event == 'BLOCK',
                                              pbp_df.p2_name, pbp_df.p1_name)
    pbp_df.loc[:, ('new_p2_name')] = np.where(pbp_df.Event == 'BLOCK',
                                              pbp_df.p1_name, pbp_df.p2_name)
    pbp_df.loc[:, ('new_p1_ID')] = np.where(pbp_df.Event == 'BLOCK',
                                            pbp_df.p2_ID, pbp_df.p1_ID)
    pbp_df.loc[:, ('new_p2_ID')] = np.where(pbp_df.Event == 'BLOCK',
                                            pbp_df.p1_ID, pbp_df.p2_ID)

    print(pbp_df.iloc[:, -5:].head(20))
#saving the new columns as the old ones
    pbp_df.loc[:, ('p1_name')] = pbp_df['new_p1_name']
    pbp_df.loc[:, ('p2_name')] = pbp_df['new_p2_name']
    pbp_df.loc[:, ('p1_ID')] = pbp_df['new_p1_ID']
    pbp_df.loc[:, ('p2_ID')] = pbp_df['new_p2_ID']

#drop unused new columns
    pbp_df = pbp_df.drop(['new_p1_name', 'new_p2_name',
                          'new_p1_ID', 'new_p2_ID'], axis=1)

    return pbp_df

def calc_distance(pbp_df):
    '''
    This function calculates the distance from the coordinate given for the
    event to the center of the goal

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with distance calculated
    '''
    pbp_df.loc[:, ('distance')] = np.sqrt((87.95-abs(pbp_df.xC))**2
                                          + pbp_df.yC**2)

    return pbp_df

def calc_angle(pbp_df):
    '''
    This function calculates the angle of the shooter from center ice with the
    vertex of the angle being located at the center of the goal

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with shooter angle calculated
    '''

    pbp_df.loc[:, ('angle')] = (np.arcsin(abs(pbp_df.yC)/np.sqrt((87.95-abs(pbp_df.xC))**2 + pbp_df.yC**2)) * 180) / 3.14

    pbp_df.loc[:, ('angle')] = np.where((pbp_df.xC > 88) | (pbp_df.xC < -88), 90 + (180-(90 + pbp_df.angle)), pbp_df.angle)

    return pbp_df

def calc_time_diff(pbp_df):
    '''
    This function calculates the time difference between events

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with time difference calculated
    '''

    pbp_df.loc[:, ('time_diff')] = pbp_df.Seconds_Elapsed -\
                                   pbp_df.Seconds_Elapsed.shift(1)

    pbp_df.loc[:, ('time_diff')] = np.where(pbp_df.time_diff == -1200, 0, pbp_df.time_diff)

    return pbp_df

def calc_rebound(pbp_df):
    '''
    This function calculates whether the corsi event was generated off of a
    goalie rebound by looking at the time difference between the current event
    and the last event and checking that last even was a shot as well

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with rebound calculated
    '''

    pbp_df.loc[:, ('is_rebound')] = np.where((pbp_df.time_diff < 4) &
                                             ((pbp_df.Event.isin(['SHOT', 'GOAL'])) &
                                              (pbp_df.Event.shift(1) == 'SHOT') &
                                              (pbp_df.Ev_Team == pbp_df.Ev_Team.shift(1))),
                                             1, 0)

    return pbp_df

def calc_rush_shot(pbp_df):
    '''
    This function calculates whether the corsi event was generated off the rush
    by looking at the time difference between the last even and whether the last
    event occured in the neutral zone

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with is_rush calculated
    '''

    pbp_df.loc[:, ('is_rush')] = np.where((pbp_df.time_diff < 4) &
                                          (pbp_df.Event.isin(['SHOT', 'MISS', 'BLOCK', 'GOAL'])) &
                                          (abs(pbp_df.xC.shift(1)) < 26),
                                          1, 0)

    return pbp_df

def calc_shooter_strength(pbp_df):
    '''
    Function calculates the team strength of the shooter such as 5v5, 5v4,
    etc. This is done by subtracting the home and away skaters based on who is
    shooting the puck.

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe with shooter strength calculated
    '''

#calculates shooter strength based on who's shooting
    pbp_df.loc[:, ('shooter_strength')] = \
            np.where((pbp_df.Ev_Team == pbp_df.Home_Team),
                     pbp_df.Home_Players - pbp_df.Away_Players,
                     pbp_df.Away_Players - pbp_df.Home_Players)

#handle empty net situations this time for the home team
    pbp_df.loc[:, ('shooter_strength')] = \
            np.where((pbp_df.Ev_Team == pbp_df.Home_Team) &
                     (pbp_df.Home_Goalie.isnull()),
                     pbp_df['shooter_strength'] + 1,
                     pbp_df['shooter_strength'])

#away team empty net situations
    pbp_df.loc[:, ('shooter_strength')] = \
            np.where((pbp_df.Ev_Team == pbp_df.Away_Team) &
                     (pbp_df.Away_Goalie.isnull()),
                     pbp_df['shooter_strength'] + 1,
                     pbp_df['shooter_strength'])

    return pbp_df

def calc_rebound_angle(pbp_df):
    '''
    Function calculates the angle between two shots if the second shot
    is flagged as a rebound else the value is zero

    Input:
    pbp_df - play by play dataframe

    Output:
    pbp_df - play by play dataframe
    '''
    pbp_df.loc[:, ('rebound_angle')] = \
            np.where(pbp_df.is_rebound == 1,
                     pbp_df.angle + pbp_df.angle.shift(1), 0)

    return pbp_df


def calc_is_goal(pbp_df):
    '''
    Function calculates if shot is a goal or not and denotes by a 1 and zero
    repsectively

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    pbp_df - play by play dataframe
    '''

    pbp_df.loc[:, ('is_goal')] = np.where(pbp_df.Event == 'GOAL', 1, 0)

    return pbp_df

def calc_zone(pbp_df):
    '''
    Function parses event description to determine zone of the event

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    pbp_df same df but with zone column calculated.
    '''

    pbp_df.loc[:, ('zone')] = np.where(pbp_df.Description.str\
                                       .contains('neu. zone', case=False)
                                       , 'neu', 0)

    pbp_df.loc[:, ('zone')] = np.where(pbp_df.Description.str\
                                       .contains('off. zone', case=False),
                                       'off', pbp_df.zone)

    pbp_df.loc[:, ('zone')] = np.where(pbp_df.Description.str\
                                       .contains('def. zone', case=False),
                                       'def', pbp_df.zone)

    pbp_df.loc[:, ('zone')] = np.where((pbp_df.zone == 'def')
                                       & (pbp_df.Event == 'BLOCK'), 'off',
                                       pbp_df.zone)

    pbp_df.loc[:, ('zone')] = np.where((pbp_df.Event.\
                                       isin(['SHOT', 'MISS',
                                             'BLOCK', 'GOAL'])) &
                                       (pbp_df.zone == 'def') &
                                       (pbp_df.distance <= 64),
                                       'off', pbp_df.zone)

    return pbp_df

def calc_shot_metrics(pbp_df):
    '''
    function to calculate whether an event is a corsi or fenwick event

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    pbp_df - play by play dataframe with corsi and fenwick columns calculated
    '''

    corsi = ['SHOT', 'BLOCK', 'MISS', 'GOAL']
    fenwick = ['SHOT', 'MISS', 'GOAL']
    shot = ['SHOT', 'GOAL']

    pbp_df.loc[:, ('is_corsi')] = np.where(pbp_df.Event.isin(corsi), 1, 0)
    pbp_df.loc[:, ('is_fenwick')] = np.where(pbp_df.Event.isin(fenwick), 1, 0)
    pbp_df.loc[:, ('is_shot')] = np.where(pbp_df.Event.isin(shot), 1, 0)

    return pbp_df

def calc_is_home(pbp_df):
    '''
    Function determines whether event was taken by the home team or not

    Inputs:
    pbp_df - play by play dataframe

    Outputs:
    pbp_df - play by play dataframe
    '''

    pbp_df.loc[:, ('is_home')] = np.where(pbp_df.Ev_Team == pbp_df.Home_Team,
                                          1, 0)

def calc_score_diff(pbp_df):
    '''
    Function to calculate score differential for score adjustment caps at
    +/- 3 due to Micah Blake McCurdy's (@Ineffectivemath on Twitter) adjustment
    method.

    Input:
    pbp_df - play by play df

    Output:
    pbp_df - play by play df with score diff calculated
    '''

    pbp_df.loc[:, ('score_diff')] = pbp_df.Home_Score - pbp_df.Away_Score

    pbp_df.loc[:, ('score_diff')] = np.where(pbp_df.score_diff < -3, -3,
                                             pbp_df.score_diff)

    pbp_df.loc[:, ('score_diff')] = np.where(pbp_df.score_diff > 3, 3,
                                             pbp_df.score_diff)

    return pbp_df

def calc_is_penalty(pbp_df):
    '''
    calculates whether an event is a penalty

    Input:
    pbp_df - play by play df

    Output:
    pbp_df - play by play df with is_penalty column created
    '''


def calc_ind_metrics(pbp_df):
    '''
    this function calculates the individual metrics of each players
    contribution during the game

    Input:
    pbp_df - play by play df

    Output:
    player_df - individual player stats df
    '''

    def calc_ind_points(pbp_df):
        '''
        function calculates individual points for each player in the data
        frame and returns a dataframe with those stats

        Inputs:
        pbp_df - play by play dataframe

        Outputs:
        points_df - dataframe with individual points of players
        '''

        goal_df = pbp_df[pbp_df.Event == 'GOAL']\
                  .groupby(['Game_Id', 'Date', 'Ev_Team',
                            'p1_ID', 'p1_name'])['is_goal'].sum().reset_index()

        a1_df = pbp_df[pbp_df.Event == 'GOAL']\
                .groupby(['Game_Id', 'Date', 'Ev_Team',
                          'p2_ID', 'p2_name'])['is_goal'].sum().reset_index()


        a2_df = pbp_df[pbp_df.Event == 'GOAL']\
                .groupby(['Game_Id', 'Date', 'Ev_Team',
                          'p3_ID', 'p3_name'])['is_goal'].sum().reset_index()



        goal_df.columns = ['Game_Id', 'Date', 'Ev_Team', 'player_id',
                           'player_name', 'goals']

        a1_df.columns = ['Game_Id', 'Date', 'Ev_Team',
                         'player_id', 'player_name', 'a1']

        a2_df.columns = ['Game_Id', 'Date', 'Ev_Team',
                         'player_id', 'player_name', 'a2']

        points_df = goal_df.merge(a1_df, on=['Game_Id', 'Date', 'Ev_Team',
                                             'player_id', 'player_name'],
                                  how='outer')

        points_df = points_df.merge(a2_df, on=['Game_Id', 'Date', 'Ev_Team',
                                               'player_id', 'player_name'],
                                    how='outer')

        points_df = points_df.fillna(0)

        points_df.loc[:, ('player_id', 'goals', 'a1', 'a2')] = \
            points_df.loc[:, ('player_id', 'goals', 'a1', 'a2')].astype(int)


        return points_df

    def calc_ind_shot_metrics(pbp_df):
        '''
        function to calculate individual shot metrics and return a data
        frame with them

        Inputs:
        pbp_df - play by play dataframe

        Ouputs:
        ind_shots_df - df with calculated iSF, iCF, iFF need to add ixG to
                       this later once xg model is finished
        '''

        corsi = ['SHOT', 'BLOCK', 'MISS', 'GOAL']
        fenwick = ['SHOT', 'MISS', 'GOAL']

        corsi_df = pbp_df[pbp_df.Event.isin(corsi)]\
                  .groupby(['Game_Id', 'Date', 'Ev_Team',
                            'p1_ID', 'p1_name'])['is_corsi'].sum().reset_index()

        fenwick_df = pbp_df[pbp_df.Event.isin(fenwick)]\
                     .groupby(['Game_Id', 'Date', 'Ev_Team',
                               'p1_ID', 'p1_name'])['is_fenwick'].sum().reset_index()

        shot_df = pbp_df[pbp_df.Event.isin(fenwick)]\
                     .groupby(['Game_Id', 'Date', 'Ev_Team',
                               'p1_ID', 'p1_name'])['is_shot'].sum().reset_index()

        corsi_df.columns = ['Game_Id', 'Date', 'Ev_Team', 'player_id',
                            'player_name', 'iCF']

        fenwick_df.columns = ['Game_Id', 'Date', 'Ev_Team',
                         'player_id', 'player_name', 'iFF']

        shot_df.columns = ['Game_Id', 'Date', 'Ev_Team',
                         'player_id', 'player_name', 'iSF']

        metrics_df = corsi_df.merge(fenwick_df,
                                    on=['Game_Id', 'Date', 'Ev_Team',
                                        'player_id', 'player_name'],
                                    how='outer')

        metrics_df = metrics_df.merge(shot_df,
                                      on=['Game_Id', 'Date', 'Ev_Team',
                                          'player_id', 'player_name'],
                                    how='outer')

        metrics_df = metrics_df.fillna(0)

        metrics_df.loc[:, ('player_id', 'iCF', 'iFF', 'iSF')] = \
            metrics_df.loc[:, ('player_id', 'iCF', 'iFF', 'iSF')].astype(int)

        print(metrics_df)

        return metrics_df



    points_df = calc_ind_points(pbp_df)
    metrics_df = calc_ind_shot_metrics(pbp_df)

    ind_stats_df = metrics_df.merge(points_df,
                                      on=['Game_Id', 'Date', 'Ev_Team',
                                          'player_id', 'player_name'],
                                    how='outer')

    return ind_stats_df

def main():

    return

if __name__ == '__main__':
    main()
