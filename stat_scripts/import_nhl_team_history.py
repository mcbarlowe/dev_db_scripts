import pandas as pd
import os
import numpy as np
import xg_prepare as xg
import merge_shift_and_pbp as oi_matrix
import clean_pbp
import calc_adjusted_stats
from calc_pppkes_ind_stats import calc_ppespk_ind_metrics, calc_adj_ppespk_ind_metrics
from calc_pppkes_onice_stats import calc_onice_str_stats, calc_adj_onice_str_stats
from sqlalchemy import create_engine
from calc_team_stats import calc_team_metrics

def sched_insert(df, table_name):

    print('Inserting DataFrame to the Database')
    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))
    df.to_sql(table_name, schema='nhl_tables', con=engine,
              if_exists='append', index=False)


#seasons = ['20092010', '20102011', '20112012', '20122013', '20132014',
#           '20142015', '20152016', '20162017', '20172018']

seasons = ['20092010']
error_list = []
for season in seasons:
    print(f'Loading {season} season')
    pbp_df = pd.read_csv(f'../scraped_files/nhl_pbp{season}.csv')
    shifts_df = pd.read_csv(f'../scraped_files/nhl_shifts{season}.csv')

    pbp_df.columns = map(str.lower, pbp_df.columns)
    shifts_df.columns = map(str.lower, shifts_df.columns)

    '''
    if season == '20172018':
        games = list(range(20001, 21272))
    else:
        games = list(range(20001, 21231))
    '''
    games = [20107]
    for game in games:
        print(f'Parsing {game} in {season} season')
        game1_df = pbp_df[pbp_df.game_id == game].reset_index(drop=True)
        game1_shifts_df = shifts_df[shifts_df.game_id == game].reset_index(drop=True)

        game1_df = xg.fixed_seconds_elapsed(game1_df)

        new_pbp_df = oi_matrix.return_pbp_w_shifts(game1_df, game1_shifts_df)

        new_pbp_df = clean_pbp.clean_pbp(new_pbp_df)

        new_pbp_df = xg.create_stat_features(new_pbp_df)

        new_pbp_df = new_pbp_df.apply(calc_adjusted_stats.calc_adjusted_columns,
                                              axis=1)
        new_pbp_df = clean_pbp.final_pbp_clean(new_pbp_df)

        team_allsits = calc_team_metrics(new_pbp_df, [6,5,4,3], [6,5,4,3])
        team_5v5 = calc_team_metrics(new_pbp_df, [6], [6])
        team_4v4 = calc_team_metrics(new_pbp_df, [5], [5])
        team_3v3 = calc_team_metrics(new_pbp_df, [4], [4])
        team_5v4 = calc_team_metrics(new_pbp_df, [6], [5])
        team_4v5 = calc_team_metrics(new_pbp_df, [5], [6])
        team_5v3 = calc_team_metrics(new_pbp_df, [6], [4])
        team_3v5 = calc_team_metrics(new_pbp_df, [4], [6])
        team_4v3 = calc_team_metrics(new_pbp_df, [5], [4])
        team_3v4 = calc_team_metrics(new_pbp_df, [4], [5])

        tables = ['team_3v3', 'team_3v4',
                  'team_3v5', 'team_4v3',
                  'team_4v4', 'team_4v5',
                  'team_5v3', 'team_5v4',
                  'team_5v5',  'team_allsits']

        data = [team_3v3, team_3v4,
                  team_3v5, team_4v3,
                  team_4v4, team_4v5,
                  team_5v3, team_5v4,
                  team_5v5,  team_allsits]

        print(team_allsits.head())

        '''
        for df, table in zip(data, tables):
            if df.toi.sum() > 0:
                print(f'Inserting data into {table}')
                print(df[df.toi >0].head())
                df.columns = list(map(str.lower, df.columns))
                sched_insert(df[df.toi > 0], table)
                '''

        '''
        except Exception as e:
            print(f'{season}{game} Error: {e}')
            error_list.append(f'{season}{game} Error: {e}')

with open('team_error_log.txt', 'w') as f:
    for error in error_list:
        f.write(error)
        '''

