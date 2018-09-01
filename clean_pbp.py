'''
This script will be used to clean up the resultant dataframe from merging the
shifts df and the pbp df such as filling NaN values and calculating proper
strength states and whether goalies where on the ice
'''
import pandas as pd
import numpy as np

def clean_pbp(new_pbp):
    '''
    this function cleans the new_pbp and gets it ready for xg and stat
    calculation
    '''
#fills na values in the coordinate with zeros
    new_pbp.loc[:, ('xc')] = new_pbp.loc[:, ('xc')].fillna(0)
    new_pbp.loc[:, ('yc')] = new_pbp.loc[:, ('yc')].fillna(0)
#fills na values with the names of the appropriate coaches
    new_pbp.loc[:, ('away_coach')] = new_pbp.loc[:, ('away_coach')].fillna(new_pbp.away_coach.unique()[0])
    new_pbp.loc[:, ('home_coach')] = new_pbp.loc[:, ('home_coach')].fillna(new_pbp.home_coach.unique()[0])
#fills na values with the names of the appropriate teams
    new_pbp.loc[:, ('away_team')] = new_pbp.loc[:, ('away_team')].fillna(new_pbp.away_team.unique()[0])
    new_pbp.loc[:, ('home_team')] = new_pbp.loc[:, ('home_team')].fillna(new_pbp.home_team.unique()[0])
#calculates new running scores to fill in the NaNs
    new_pbp.loc[:, ('away_score')] = np.where((new_pbp.event == 'GOAL') & (new_pbp.ev_team == new_pbp.away_team.unique()[0]), 1, 0).cumsum()
    new_pbp.loc[:, ('home_score')] = np.where((new_pbp.event == 'GOAL') & (new_pbp.ev_team == new_pbp.home_team.unique()[0]), 1, 0).cumsum()

    #clean home and away goalies
    new_pbp = new_pbp.apply(clean_goalie,
                            args=(new_pbp.away_goalie.unique(),
                                  new_pbp.away_goalie_id.unique(),
                                  new_pbp.home_goalie.unique(),
                                  new_pbp.home_goalie_id.unique()),
                            axis=1)

    #clean home and away skaters
    new_pbp = new_pbp.apply(clean_skaters, axis=1)

    return new_pbp

def main():
    return

def clean_goalie(row, away_goalie, away_goalie_id, home_goalie, home_goalie_id):
    '''
    This checks to make sure the goalie for each team is on the ice and if so
    fills the NaN's from the shift/pbp merge with the goalie's name/id and if
    not leave it NaN

    Input:
    row - row of the new_pbp_df
    away_goalie    - list of away goalies in the game
    away_goalie_id - list of away goalie's player ids
    home_goalie    - same as away but for the home team
    home_goalie_id - see above

    Output:
    row - row with Goalie on ice calculated
    '''

    away_goalie = away_goalie[~pd.isnull(away_goalie)]
    away_goalie_id = away_goalie_id[~pd.isnull(away_goalie_id)]
    home_goalie = home_goalie[~pd.isnull(home_goalie)]
    home_goalie_id = home_goalie_id[~pd.isnull(home_goalie_id)]

    for goalie, goalie_id in zip(away_goalie, away_goalie_id):
        if np.where(row[['awayplayer1', 'awayplayer2', 'awayplayer3', 'awayplayer4', 'awayplayer5', 'awayplayer6']].isin([goalie]), 1, 0).sum() > 0:
            row.loc[('away_goalie', 'away_goalie_id')] = goalie, goalie_id

    for goalie, goalie_id in zip(home_goalie, home_goalie_id):
        if np.where(row[['homeplayer1', 'homeplayer2', 'homeplayer3', 'homeplayer4', 'homeplayer5', 'homeplayer6']].isin([goalie]), 1, 0).sum() > 0:
            row.loc[('home_goalie', 'home_goalie_id')] = goalie, goalie_id

    return row

def clean_skaters(row):
    '''
    this function looks at the number of players that are on the ice and counts
    them to return the number of skaters for each team for each event in the
    pbp.

    Inputs:
    row - one row of the pbp dataframe

    Outputs:
    row - row with amount of skaters for each team calculated
    '''
    away_players = row[['awayplayer1', 'awayplayer2', 'awayplayer3',
                        'awayplayer4', 'awayplayer5', 'awayplayer6']]

    home_players = row[['homeplayer1', 'homeplayer2', 'homeplayer3',
                        'homeplayer4', 'homeplayer5', 'homeplayer6']]

    row.away_players = len(away_players[away_players.nonzero()[0]])
    row.home_players = len(home_players[home_players.nonzero()[0]])

    return row

if __name__ == '__main__':
    main()
