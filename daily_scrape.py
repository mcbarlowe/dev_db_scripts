import requests
import datetime
import logging

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

def main():
    '''
    This script pulls the NHL games played from the day before parses the data
    to calculated individual, on-ice, and relative stats along with team and
    goalie stats and then will insert them into an PostgreSQL Database.

    This will use an NHL scraper built by Harry Shomer using the Hockey-Scraper
    package found at https://github.com/HarryShomer/Hockey-Scraper.
    '''

#setup logger to write out stuff to log file for debugging/warnings
    logging.basicConfig(filename='daily_nhl_scraper.log',
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        level=logging.DEBUG)

#getting yesterday's date and formatting it into the form that the NHL API
#accepts
    date = datetime.datetime.now() - datetime.timedelta(1)
    date = date.strftime('%Y-%m-%d')

    game_ids = get_yest_games(date)

    if game_ids == None:
        logging.info("No games played today")
    else:
        logging.info("Game Ids succesfully scraped")
        logging.info(f"{date} of NHL games: {game_ids}")

if __name__ == '__main__':
    main()
