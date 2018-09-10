import datetime
import os
import requests


def get_today_sched(date):
    '''
    this function gets the schedule of games that are set to be played on the
    date pased to it in the NHL

    Input:
    date - date to get schedule

    Ouput:
    games - dictionary of games to be played
    '''

    url = f'https://statsapi.web.nhl.com/api/v1/schedule?date={date}'

    req = requests.get(url)
    schedule_dict = req.json()

    today_games = {}

    for x in schedule_dict['dates']:
        for game in x['games']:
            today_games[game['gamePk']] = {}
            today_games[game['gamePk']]['date'] = date
            today_games[game['gamePk']]['home_team'] = game['teams']['home']['team']['name']
            today_games[game['gamePk']]['home_team_id'] = game['teams']['home']['team']['id']
            today_games[game['gamePk']]['away_team'] = game['teams']['away']['team']['name']
            today_games[game['gamePk']]['away_team_id'] = game['teams']['away']['team']['id']

    return today_games

def main():
    get_today_sched('2018-10-04')

if __name__ == '__main__':
    main()
