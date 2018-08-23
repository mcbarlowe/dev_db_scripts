import pandas as pd
import math

def merge_pbp_and_shifts(line_change_df, pbp_df):
    '''
    function to merge the shift changes and the pbp_df into one data frame
    like Emmanuel Perry's scraper
    '''

#merge pbp_df and line_change_df into one dataframe
    pbp_w_shifts = pd.merge(pbp_df, line_change_df, how='outer',
                            on=['seconds_elapsed', 'event', 'awayplayer1_id',
                                'awayplayer1', 'awayplayer2_id', 'awayplayer2',
                                'awayplayer3', 'awayplayer3_id', 'awayplayer4',
                                'awayplayer4_id', 'awayplayer5', 'awayplayer5_id',
                                'awayplayer6', 'awayplayer6_id', 'homeplayer1_id',
                                'homeplayer1', 'homeplayer2_id', 'homeplayer2',
                                'homeplayer3', 'homeplayer3_id', 'homeplayer4',
                                'homeplayer4_id', 'homeplayer5', 'homeplayer5_id',
                                'homeplayer6', 'homeplayer6_id'])

#sorts the dataframe by elapsed seconds and then index as shift changes often
#take place at the same time by the play by play data
    pbp_w_shifts = pbp_w_shifts.sort_values(['seconds_elapsed','period'],
                                            kind='mergesort',
                                            na_position='first').reset_index(drop=True)

#need to switch PEND so they occur before the shift change on to start the next
#period
    pend_list = pbp_w_shifts[pbp_w_shifts.event == 'PEND'].index.values
    for x in pend_list:
        a, b = pbp_w_shifts.iloc[x, :].copy(), pbp_w_shifts.iloc[x-1, :].copy()
        pbp_w_shifts.iloc[x, :], pbp_w_shifts.iloc[x-1, :] = b, a
#this avoids mislabeling the initial on shift for next period as the period before
        pbp_w_shifts.loc[x, 'period'] = np.ceil(shifts_test.seconds_elapsed/1200) + 1

#cleaning up and the NaNs with appropriate values
    pbp_w_shifts.game_id = pbp_w_shifts.game_id.fillna(pbp_w_shifts.game_id.values[0])
    pbp_w_shifts.date = pbp_w_shifts.date.fillna(pbp_w_shifts.game_id.values[0])
#filling nans with period numbers
    pbp_w_shifts.period = pbp_w_shifts.period.fillna(np.ceil(pbp_w_shifts.seconds_elapsed/1200))

    return pbp_w_shifts

def create_shifts_df(player_matrix, home_team, away_team):
    '''
    function to transform on ice matrix into a shifts dataframe to join
    with the play by play dataframe

    Inputs:
    player_matrix - on ice dictionary
    home_team - home team for this game
    away_team - away team for this game

    Outputs:
    line_change_df - dataframe of just line changes
    '''
    line_change_list = []
    line_change_df_list = []

#loops through player onice matrix and parses the players on and off for each
#second where there is an actual line change i.e. players in the 'Off' part
#of the player_matrix
    for seconds in range(len(player_matrix)):
        if player_matrix[seconds][home_team]['Off'] == {} and player_matrix[seconds][away_team]['Off'] == {}:
            continue
        else:
#pulls out the player name and player id for each team and puts them in a list
#where each entry is either a tuple of player id and name if player was on the
#ice or a tuple of zeros if the team did not have the full compliment of players
#on the ice
            away_off = [(value, key) for key, value
                        in player_matrix[seconds][away_team]['On'].items()
                        if key in player_matrix[seconds-1][away_team]['On'].keys()
                        and player_matrix[seconds][away_team]['On'].keys()]

            away_on = [(value, key) for key, value
                       in player_matrix[seconds][away_team]['On'].items()]

            home_off = [(value, key) for key, value
                        in player_matrix[seconds][home_team]['On'].items()
                        if key in player_matrix[seconds-1][home_team]['On'].keys()
                        and player_matrix[seconds][home_team]['On'].keys()]

            home_on = [(value, key) for key, value
                       in player_matrix[seconds][home_team]['On'].items()]

#checks to see if there were total 6 players on the ice for each team and if not
#pads the lists with (0,0) tuple to form the dataframe
            if len(away_off) < 6:
                away_off.extend([(0,0)] * (6-len(away_off)))

            if len(home_off) < 6:
                home_off.extend([(0,0)] * (6-len(home_off)))

            if len(away_on) < 6:
                away_on.extend([(0,0)] * (6-len(away_on)))

            if len(home_on) < 6:
                home_on.extend([(0, 0)] * (6-len(home_on)))

#combines the home/away off and on to form one row of a shift change
            off_shift = away_off + home_off
            on_shift = away_on + home_on

#adding the event types showing whether players are coming on or leaving the ice
            off_shift.insert(0, 'OFF')
            on_shift.insert(0, 'ON')

#adding eplased_seconds to help facilitate the join
            off_shift.insert(0, seconds)
            on_shift.insert(0, seconds)

            line_change_list.append(off_shift)
            line_change_list.append(on_shift)

#pulling out the tuples to form a list of lists to create the on ice shift
#dataframe to join to the play by play
    for line in line_change_list:
        shift_line = []
        for x in range(len(line)):
            if type(line[x]) == tuple:
                shift_line.append(line[x][0])
                shift_line.append(line[x][1])
            else:
                shift_line.append(line[x])
        print(shift_line)
        line_change_df_list.append(shift_line)

    columns = ['seconds_elapsed', 'event', 'awayplayer1', 'awayplayer1_id',
               'awayplayer2', 'awayplayer2_id','awayplayer3', 'awayplayer3_id',
               'awayplayer4', 'awayplayer4_id','awayplayer5', 'awayplayer5_id',
               'awayplayer6', 'awayplayer6_id',
               'homeplayer1', 'homeplayer1_id',
               'homeplayer2', 'homeplayer2_id','homeplayer3', 'homeplayer3_id',
               'homeplayer4', 'homeplayer4_id','homeplayer5', 'homeplayer5_id',
               'homeplayer6', 'homeplayer6_id']

    line_change_df = pd.DataFrame(line_change_df_list, columns=columns)

    return line_change_df

def player_onice_matrix(shift_df):
    '''
    This function creates a player on ice matrix showing which players were
    on the ice at the same time from the shift report

    Inputs:
    shift_df - one game shift dataframe with positions added

    Outputs:
    player_matrix - a list of lists breaking down players ice time
    '''

    shift_df.columns = map(str.lower, shift_df.columns)

    teams = list(shift_df.team.unique())
    game = shift_df.game_id.unique()[0]

    player_matrix = get_game_length(shift_df, game, teams)

    for row in range(shift_df.shape[0]):
        player_matrix = add_toi(shift_df.iloc[row, :], player_matrix)

    return player_matrix

def add_toi(row, onice_matrix):
    '''
    function that takes a shift from the shifts_df and applies it to the on
    ice matrix

    Inputs:
    shift_df - dataframe of the shifts of a game
    onice_matrix - empty dict where each index is a second in the game and lists
                   the players moving on and off the ice

    Outputs:
    onice_matrix - list filled with players moving on and off the ice
    '''

    start = row['start']
    end = row['end']
    team = row['team']

    if row['period'] != 1:
        start += (1200 * (row['period'] - 1))
        end += (1200 * (row['period'] - 1))

    for x in range(int(start), int(end) + 1):
        if x == end:
            shift_type = 'Off'
        else:
            shift_type = 'On'

        onice_matrix[x][team][shift_type][str(row.player_id)] = row.player

    return onice_matrix


def get_game_length(game_df, game, teams):
    """
    Gets a list with the length equal to the amount of seconds in that game

    :param game_df: DataFrame with shift info for game
    :param game: game_id
    :param teams: both teams in game

    :return: list
    """
    # Start off with the standard 3 periods (1201 because start at 0)
    seconds = list(range(0, 1201)) * 3

    # If the last shift was an overtime shift, then extend the list of seconds by how fair into OT the game went
    if game_df['period'][game_df.shape[0] - 1] == 4:
        seconds.extend(list(range(0, game_df['end'][game_df.shape[0] - 1] + 1)))

    # For Playoff Games
    # If the game went beyond 4 periods tack that on to
    if int(game) >= 30000:
        # Go from beyond period 4 because done above
        for i in range(game_df['period'][game_df.shape[0] - 1] - 4):
            seconds.extend(list(range(0, 1201)))

        seconds.extend(list(range(0, game_df['end'][game_df.shape[0] - 1] + 1)))

    # Create dict for seconds_list
    # On = Players on Ice at that second
    # Off = Players who got off ice at that second
    for i in range(len(seconds)):
        seconds[i] = {
            teams[0]: {'On': {}, 'Off': {}},
            teams[1]: {'On': {}, 'Off': {}},
        }

    return seconds
