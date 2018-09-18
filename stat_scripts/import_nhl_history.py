import pandas as pd
import os
import numpy as np
import xg_prepare as xg
import merge_shift_and_pbp as oi_matrix
import clean_pbp
import calc_adjusted_stats
from calc_all_sits_ind_stats import calc_ind_metrics, calc_adj_ind_metrics
from calc_all_sits_onice_stats import calc_onice_stats, calc_adj_onice_stats
from calc_pppkes_ind_stats import calc_ppespk_ind_metrics, calc_adj_ppespk_ind_metrics
from calc_pppkes_onice_stats import calc_onice_str_stats, calc_adj_onice_str_stats
from sqlalchemy import create_engine

def sched_insert(df, table_name):

    print('Inserting DataFrame to the Database')
    engine = create_engine(os.environ.get('DEV_DB_CONNECT'))
    df.to_sql(table_name, schema='nhl_tables', con=engine,
              if_exists='append', index=False)

seasons = ['20102011', '20112012', '20122013', '20132014',
           '20142015', '20152016', '20162017', '20172018']
for season in seasons:
    print(f'Loading {season} season')
    pbp_df = pd.read_csv(f'../scraped_files/nhl_pbp{season}.csv')
    shifts_df = pd.read_csv(f'../scraped_files/nhl_shifts{season}.csv')

    pbp_df.columns = map(str.lower, pbp_df.columns)
    shifts_df.columns = map(str.lower, shifts_df.columns)

    if season == '20172018':
        games = list(range(20001, 21272))
    else:
        games = list(range(20001, 21231))

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

        print(f'Calculating {game} stats')
        as_ind_stats = calc_ind_metrics(new_pbp_df)
        as_onice_stats = calc_onice_stats(new_pbp_df)
        as_adj_ind_stats = calc_adj_ind_metrics(new_pbp_df)
        as_adj_onice_stats = calc_adj_onice_stats(new_pbp_df)

        ind_stats_5v5 = calc_ppespk_ind_metrics(new_pbp_df, 6, 6)
        onice_stats_5v5 = calc_onice_str_stats(new_pbp_df, 6, 6)
        ind_stats_5v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 6)
        onice_stats_5v5_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 6)

        try:
            ind_stats_4v4 = calc_ppespk_ind_metrics(new_pbp_df, 5, 5)
            onice_stats_4v4 = calc_onice_str_stats(new_pbp_df, 5, 5)
            ind_stats_4v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 5)
            onice_stats_4v4_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 5)
        except ValueError:
            ind_stats_4v4 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v4 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_4v4_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v4_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        try:
            ind_stats_3v3 = calc_ppespk_ind_metrics(new_pbp_df, 4, 4)
            onice_stats_3v3 = calc_onice_str_stats(new_pbp_df, 4, 4)
            ind_stats_3v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 4)
            onice_stats_3v3_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 4)
        except ValueError:
            ind_stats_3v3 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v3 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_3v3_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v3_adj = pd.DataFrame(columns=list(as_onice_stats.columns))


        try:
            ind_stats_5v4 = calc_ppespk_ind_metrics(new_pbp_df, 6, 5)
            onice_stats_5v4 = calc_onice_str_stats(new_pbp_df, 6, 5)
            ind_stats_5v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 5)
            onice_stats_5v4_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 5)
        except ValueError:
            ind_stats_5v4 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_5v4 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_5v4_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_5v4_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        try:
            ind_stats_4v5 = calc_ppespk_ind_metrics(new_pbp_df, 5, 6)
            onice_stats_4v5 = calc_onice_str_stats(new_pbp_df, 5, 6)
            ind_stats_4v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 6)
            onice_stats_4v5_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 6)
        except ValueError:
            ind_stats_4v5 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v5 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_4v5_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v5_adj = pd.DataFrame(columns=list(as_onice_stats.columns))


        try:
            ind_stats_4v3 = calc_ppespk_ind_metrics(new_pbp_df, 5, 4)
            onice_stats_4v3 = calc_onice_str_stats(new_pbp_df, 5, 4)
            ind_stats_4v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 4)
            onice_stats_4v3_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 4)
        except ValueError:
            ind_stats_4v3 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v3 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_4v3_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_4v3_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        try:
            ind_stats_3v4 = calc_ppespk_ind_metrics(new_pbp_df, 4, 5)
            onice_stats_3v4 = calc_onice_str_stats(new_pbp_df, 4, 5)
            ind_stats_3v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 5)
            onice_stats_3v4_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 5)
        except ValueError:
            ind_stats_3v4 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v4 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_3v4_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v4_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        try:
            ind_stats_5v3 = calc_ppespk_ind_metrics(new_pbp_df, 6, 4)
            onice_stats_5v3 = calc_onice_str_stats(new_pbp_df, 6, 4)
            ind_stats_5v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 4)
            onice_stats_5v3_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 4)
        except ValueError:
            ind_stats_5v3 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_5v3 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_5v3_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_5v3_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        try:
            ind_stats_3v5 = calc_ppespk_ind_metrics(new_pbp_df, 4, 6)
            onice_stats_3v5 = calc_onice_str_stats(new_pbp_df, 4, 6)
            ind_stats_3v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 6)
            onice_stats_3v5_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 6)
        except ValueError:
            ind_stats_3v5 = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v5 = pd.DataFrame(columns=list(as_onice_stats.columns))
            ind_stats_3v5_adj = pd.DataFrame(columns=list(as_ind_stats.columns))
            onice_stats_3v5_adj = pd.DataFrame(columns=list(as_onice_stats.columns))

        as_stats = as_onice_stats.merge(as_ind_stats,
                                        on=['season', 'game_id', 'date',
                                            'player_id', 'player_name'],
                                        how='left')
        as_stats = as_stats.fillna(0)

        as_stats_adj = as_adj_onice_stats.merge(as_adj_ind_stats,
                                               on=['season', 'game_id', 'date',
                                                   'player_id', 'player_name'],
                                               how='left')
        as_stats_adj = as_stats_adj.fillna(0)

        stats_5v5 = onice_stats_5v5.merge(ind_stats_5v5,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_5v5 = stats_5v5.fillna(0)

        stats_5v5_adj = onice_stats_5v5_adj.merge(ind_stats_5v5_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_5v5_adj = stats_5v5_adj.fillna(0)

        stats_4v4 = onice_stats_4v4.merge(ind_stats_4v4,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_4v4 = stats_4v4.fillna(0)

        stats_4v4_adj = onice_stats_4v4_adj.merge(ind_stats_4v4_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_4v4_adj = stats_4v4_adj.fillna(0)

        stats_4v3 = onice_stats_4v3.merge(ind_stats_4v3,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_4v3 = stats_4v3.fillna(0)

        stats_4v3_adj = onice_stats_4v3_adj.merge(ind_stats_4v3_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_4v3_adj = stats_4v3_adj.fillna(0)

        stats_3v4 = onice_stats_3v4.merge(ind_stats_3v4,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_3v4 = stats_3v4.fillna(0)

        stats_3v4_adj = onice_stats_3v4_adj.merge(ind_stats_3v4_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_3v4_adj = stats_3v4_adj.fillna(0)

        stats_3v3 = onice_stats_3v3.merge(ind_stats_3v3,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_3v3 = stats_3v3.fillna(0)

        stats_3v3_adj = onice_stats_3v3_adj.merge(ind_stats_3v3_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_3v3_adj = stats_3v3_adj.fillna(0)

        stats_5v4 = onice_stats_5v4.merge(ind_stats_5v4,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_5v4 = stats_5v4.fillna(0)

        stats_5v4_adj = onice_stats_5v4_adj.merge(ind_stats_5v4_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_5v4_adj = stats_5v4_adj.fillna(0)

        stats_4v5 = onice_stats_4v5.merge(ind_stats_4v5,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_4v5 = stats_4v5.fillna(0)

        stats_4v5_adj = onice_stats_4v5_adj.merge(ind_stats_4v5_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')

        stats_4v5_adj = stats_4v5_adj.fillna(0)

        stats_5v3 = onice_stats_5v3.merge(ind_stats_5v3,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_5v3 = stats_5v3.fillna(0)

        stats_5v3_adj = onice_stats_5v3_adj.merge(ind_stats_5v3_adj,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_5v3_adj = stats_5v3_adj.fillna(0)

        stats_3v5 = onice_stats_3v5.merge(ind_stats_3v5,
                                          on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_3v5 = stats_3v5.fillna(0)

        stats_3v5_adj = onice_stats_3v5_adj.merge(ind_stats_3v5_adj,
                 on=['season', 'game_id', 'date',
                                              'player_id', 'player_name'],
                                          how='left')
        stats_3v5_adj = stats_3v5_adj.fillna(0)

        tables = ['player_3v3', 'player_3v3_adj', 'player_3v4', 'player_3v4_adj',
                  'player_3v5', 'player_3v5_adj', 'player_4v3', 'player_4v3_adj',
                  'player_4v4', 'player_4v4_adj', 'player_4v5', 'player_4v5_adj',
                  'player_5v3', 'player_5v3_adj', 'player_5v4', 'player_5v4_adj',
                  'player_5v5', 'player_5v5_adj', 'player_allsits',
                  'player_allsits_adj']

        data = [stats_3v3, stats_3v3_adj, stats_3v4, stats_3v4_adj, stats_3v5,
                stats_3v5_adj, stats_4v3, stats_4v3_adj, stats_4v4, stats_4v4_adj,
                stats_4v5, stats_4v5_adj, stats_5v3, stats_5v3_adj, stats_5v4,
                stats_5v4_adj, stats_5v5, stats_5v5_adj, as_stats, as_stats_adj]

        for df, table in zip(data, tables):
            if df.toi.sum() > 0:
                print(f'Inserting data into {table}')
                print(df[df.toi >0].head())
                df.columns = list(map(str.lower, df.columns))
                sched_insert(df[df.toi > 0], table)



'''
    print('all sits stats')
    print(as_stats)
    print(as_stats_adj)
    print(as_stats.columns)
    print(as_stats_adj.columns)
    print('5v5 stats')
    print(stats_5v5)
    print(stats_5v5_adj)
    if (stats_4v4.toi.sum() > 0):
        print('4v4 stats')
        print(stats_4v4)
        print(stats_4v4_adj)
    if (stats_3v3.toi.sum() > 0):
        print('3v3 stats')
        print(stats_3v3)
        print(stats_3v3_adj)
    if stats_5v4.toi.sum() > 0:
        print('5v4 stats')
        print(stats_5v4)
        print(stats_5v4_adj)
    if stats_4v5.toi.sum() > 0:
        print('4v5 stats')
        print(stats_4v5)
        print(stats_4v5_adj)
    if stats_4v3.toi.sum() > 0:
        print('4v3 stats')
        print(stats_4v3)
        print(stats_4v3_adj)
    if stats_3v4.toi.sum() > 0:
        print('3v4 stats')
        print(stats_3v4)
        print(stats_3v4_adj)
    if stats_5v3.toi.sum() > 0:
        print('5v3 stats')
        print(stats_5v3)
        print(stats_5v3_adj)
    if stats_3v5.toi.sum() > 0:
        print('3v5 stats')
        print(stats_3v5)
        print(stats_3v5_adj)
'''
