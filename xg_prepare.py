import pandas as pd
import numpy as np

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
    pbp_df.loc[:, ('new_p1_name')] = np.where(pbp_df.Event == 'BLOCK', pbp_df.p2_name, pbp_df.p1_name)
    pbp_df.loc[:, ('new_p2_name')] = np.where(pbp_df.Event == 'BLOCK', pbp_df.p1_name, pbp_df.p2_name)
    pbp_df.loc[:, ('new_p1_ID')] = np.where(pbp_df.Event == 'BLOCK', pbp_df.p2_ID, pbp_df.p1_ID)
    pbp_df.loc[:, ('new_p2_ID')] = np.where(pbp_df.Event == 'BLOCK', pbp_df.p1_ID, pbp_df.p2_ID)

    print(pbp_df.iloc[:, -5:].head(20))
#saving the new columns as the old ones
    pbp_df.loc[:,('p1_name')] = pbp_df['new_p1_name']
    pbp_df.loc[:,('p2_name')] = pbp_df['new_p2_name']
    pbp_df.loc[:,('p1_ID')] = pbp_df['new_p1_ID']
    pbp_df.loc[:,('p2_ID')] = pbp_df['new_p2_ID']

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
    pbp_df.loc[:,('distance')] = np.sqrt((87.95-abs(pbp_df.xC))**2 + pbp_df.yC**2)

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

    pbp_df.loc[:, ('time_diff')] = pbp_df.Seconds_Elapsed - pbp_df.Seconds_Elapsed.shift(1)

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

def main():

    return

if __name__ == '__main__':
    main()
