import requests
import datetime
import logging
import hockey_scraper
import process_players
import xg_prepare as xg
import merge_shift_and_pbp as oi_matrix
import clean_pbp
import calc_adjusted_stats
from calc_all_sits_ind_stats import calc_ind_metrics, calc_adj_ind_metrics
from calc_all_sits_onice_stats import calc_onice_stats, calc_adj_onice_stats
from calc_pppkes_ind_stats import calc_ppespk_ind_metrics, calc_adj_ppespk_ind_metrics
from calc_pppkes_onice_stats import calc_onice_str_stats, calc_adj_onice_str_stats

def get_yest_games(date):
    '''
    This function will return a list of game ids of NHL games played on the
    date given

    Input:
    date - the date on which the nhl games returned was played

    Output:
    game_ids - a list of NHL game ids played on the date given
    '''

    game_ids = []

    api_url = ('https://statsapi.web.nhl.com/api/v1/schedule?'
               'date={}').format(date)

    req = requests.get(api_url)
    schedule_dict = req.json()

#tests to see if any games were played and if not returns None to let the main
#script know that there where no games played and to stop running
    if schedule_dict['totalGames'] == 0:
        return None

    for date in schedule_dict['dates']:
        for game in date['games']:
            game_ids.append(game['gamePk'])

    return game_ids

def scrape_daily_games(game_id_list):
    '''
    this function scrapes the game ids provided in the list and returns a dict
    with all the pbp and shift data for each game with game_id serving as the
    key. It will also return a error_games list of the game where an error
    occured in the scraping

    Inputs:
    game_id_list - a list of game ids to scrape

    Outputs:
    game_dict - dictionary containing shift and pbp data for each game
    error_games - a list of game_ids where the scraper encountered errors
    '''

#setup games dictionary to store the pbp of the games scraped from the day
#before
    games_dict = {}

#create list to add games that errored out to write to file
    error_games = []

    for game in game_id_list:
        scraped_data = hockey_scraper.scrape_games([game],
                                                   True, data_format='Pandas')

#pull pbp, and shifts from the scraped data and write errors to the log
        games_dict[str(game)] = {}
        games_dict[str(game)]['pbp'] = scraped_data['pbp']
        games_dict[str(game)]['shifts'] = scraped_data['shifts']

#if an error occurs from scraping the game, log the errors and save the game id
#to rescrape latter. Delete the key from the dictionary so the data is not
#mistakenly added to the database
        if scraped_data['errors']:
            error_games.append(game)
            logging.debug(f"Errors are {scraped_data['errors']}")
            del games_dict[str(game)]

    logging.info("All games scrapped")
    logging.debug(games_dict.keys())

    return games_dict, error_games

def main():
    '''
    This script pulls the NHL games played from the day before parses the data
    to calculated individual, on-ice, and relative stats along with team and
    goalie stats and then will insert them into an PostgreSQL Database.

    This will use an NHL scraper built by Harry Shomer using the Hockey-Scraper
    package found at https://github.com/HarryShomer/Hockey-Scraper.
    '''


#setup logger to write out stuff to log file for debugging/warnings
#TODO changing logging level to info once script is ready
    logging.basicConfig(filename='daily_nhl_scraper.log',
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        level=logging.DEBUG)

#getting yesterday's date and formatting it into the form that the NHL API
#accepts
    date = datetime.datetime.now() - datetime.timedelta(1)
    date = date.strftime('%Y-%m-%d')

#TODO remove test date once script is fully functional
    #test_date = "2018-01-09"
    game_ids = get_yest_games(date)

    #game_ids = [2017020001]
    if game_ids == None:
        logging.info("No games played today")
        return
    else:
        logging.info("Game Ids succesfully scraped")
        logging.info(f"{date} NHL games: {game_ids}")

    games_dict, error_games = scrape_daily_games(game_ids)


    for key, value in games_dict.items():
        process_players.process_players(value['shifts'])

    for key, value in games_dict.items():

#TODO insert code to insert raw pbp into a rawpbptable in the database to create
#CDF for rink coordinates for the rink adjustment functions if i have time

#pulling pbp and shifts data for each game out of the dictionary
        pbp_df = value['pbp']
        shifts_df = value['shifts']

#change all columns to lower case
        pbp_df.columns = map(str.lower, pbp_df.columns)
        shifts_df.columns = map(str.lower, shifts_df.columns)

#fixing the seconds elapsed column
        pbp_df = xg.fixed_seconds_elapsed(pbp_df)

#merging the shifts and pbp dataframes
        new_pbp_df = oi_matrix.return_pbp_w_shifts(pbp_df, shifts_df)

    #clean the pbp and fix block shots and calc columns to be used to calc
    #other stats
        new_pbp_df = clean_pbp.clean_pbp(new_pbp_df)

    #TODO adjust the coordinates of shots to adjust for rink bias add this later
    # if i have time

    #calc xg features and xg values for each fenwick envent
        new_pbp_df = xg.create_stat_features(new_pbp_df)

    #calc all adjusted stat columns for corsi, fenwick and xg
        new_pbp_df = new_pbp_df.apply(calc_adjusted_stats.calc_adjusted_columns,
                                      axis=1)

    #TODO calc all player individual, on-ice, and relative stats for all strengths
    #both adjusted and unadjusted
        as_ind_stats = calc_ind_metrics(new_pbp_df)
        as_onice_stats = calc_onice_stats(new_pbp_df)
        as_adj_ind_stats = calc_adj_ind_metrics(new_pbp_df)
        as_adj_onice_stats = calc_adj_onice_stats(new_pbp_df)

        ind_stats_5v5 = calc_ppespk_ind_metrics(new_pbp_df, 6, 6)
        onice_stats_5v5 = calc_onice_str_stats(new_pbp_df, 6, 6)
        ind_stats_5v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 6)
        onice_stats_5v5_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 6)

        ind_stats_4v4 = calc_ppespk_ind_metrics(new_pbp_df, 5, 5)
        onice_stats_4v4 = calc_onice_str_stats(new_pbp_df, 5, 5)
        ind_stats_4v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 5)
        onice_stats_4v4_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 5)

        ind_stats_3v3 = calc_ppespk_ind_metrics(new_pbp_df, 4, 4)
        onice_stats_3v3 = calc_onice_str_stats(new_pbp_df, 4, 4)
        ind_stats_3v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 4)
        onice_stats_3v3_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 4)

        ind_stats_5v4 = calc_ppespk_ind_metrics(new_pbp_df, 6, 5)
        onice_stats_5v4 = calc_onice_str_stats(new_pbp_df, 6, 5)
        ind_stats_5v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 5)
        onice_stats_5v4_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 5)

        ind_stats_4v5 = calc_ppespk_ind_metrics(new_pbp_df, 5, 6)
        onice_stats_4v5 = calc_onice_str_stats(new_pbp_df, 5, 6)
        ind_stats_4v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 6)
        onice_stats_4v5_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 6)

        ind_stats_4v3 = calc_ppespk_ind_metrics(new_pbp_df, 5, 4)
        onice_stats_4v3 = calc_onice_str_stats(new_pbp_df, 5, 4)
        ind_stats_4v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 5, 4)
        onice_stats_4v3_adj = calc_adj_onice_str_stats(new_pbp_df, 5, 4)

        ind_stats_3v4 = calc_ppespk_ind_metrics(new_pbp_df, 4, 5)
        onice_stats_3v4 = calc_onice_str_stats(new_pbp_df, 4, 5)
        ind_stats_3v4_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 5)
        onice_stats_3v4_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 5)

        ind_stats_5v3 = calc_ppespk_ind_metrics(new_pbp_df, 6, 4)
        onice_stats_5v3 = calc_onice_str_stats(new_pbp_df, 6, 4)
        ind_stats_5v3_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 6, 4)
        onice_stats_5v3_adj = calc_adj_onice_str_stats(new_pbp_df, 6, 4)

        ind_stats_3v5 = calc_ppespk_ind_metrics(new_pbp_df, 4, 6)
        onice_stats_3v5 = calc_onice_str_stats(new_pbp_df, 4, 6)
        ind_stats_3v5_adj = calc_adj_ppespk_ind_metrics(new_pbp_df, 4, 6)
        onice_stats_3v5_adj = calc_adj_onice_str_stats(new_pbp_df, 4, 6)

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

    #TODO calc team stats for all strengths adjusted/unadjusted

    #TODO calc goalie stats for all strengths adjusted/unadjusted and xg

    #TODO Insert all stats to the appropriate database tables

    #TODO write code to write all the games with erros to a file that another
    #script will rescrape periodically until all data is clean
    return new_pbp_df


if __name__ == '__main__':
    main()
