'''
This model will predict the probabilites of winners in NHL games by using the
poisson distirbution and monte carlo sampling
'''
import os
import datetime
from get_today_schedule import get_today_sched
import numpy as np
import pandas as pd
import psycopg2

def main():

#gets todays date
    date = datetime.datetime.now().strftime('%Y-%m-%d')

#get daily schedule
    daily_sched = get_today_sched(date)

#TODO write code to query the results database to return the past two years
#of results for each team in each game

#TODO sort the data and adjust scoring for non OT and get OT and shootout win
#% for each team

#TODO run simulation using each teams distribution of goals scored in regulation
#for ties determine probability of both teams not scoring in OT from their OT
#poisson goal distributions. USe that p and (1-p) as a bernoulli trial to
#determine if game was decided in OT. If it is decided in OT use Bradley-Terry
#model to determine probability of home team winning with another Bernoulli trial.
#If the game is not decided in OT use another Bradley-Terry model with SO win %'s
#to determine probability of home team winning shootout.

    return

if __name__ == '__main__':
    main()

