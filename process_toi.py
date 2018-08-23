'''
This will update the nhl_players table as it computes TOI from the player
shifts file/dataframe produced by the scraper
'''

import player_info
import process_players
import compile_toi
import pandas as pd
import player_onice_matrix

def main():

    col_types = {'Unnamed: 0': int,  'Game_Id': int, 'Period': int,
                 'Team': str, 'Player': str, 'Player_Id': int,
                 'Start': int, 'End': int, 'Duration': int,
                 'Date': object}

    shifts_df = pd.read_csv('scraped_files/nhl_shifts20172018.csv', dtype=col_types)

    print(shifts_df.columns)
    shifts_df = player_info.fill_shifts_with_positions(shifts_df)

    player_toi_df, team_toi_df = compile_toi.process_games(shifts_df)

    player_toi_df = pd.DataFrame(player_toi_df)
    team_toi_df = pd.DataFrame(team_toi_df)
    pd.DataFrame.to_csv(player_toi_df, 'test_player_toi.csv')
    pd.DataFrame.to_csv(team_toi_df, 'test_team_toi.csv')

if __name__ == '__main__':
    main()

