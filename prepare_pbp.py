'''
This script takes the shifts data frame and the play by play dataframe returned
from Harry Shomer's scraper and returns a merged play by play dataframe with
shift data included and certain variables calculated for the calculating of
shot metrics, xG, and TOI. Will also process players in the game and add them
to the players table if they are not already present.
'''
import player_onice_matrix #this creates shift events in pbp

import xg_prepare          #this module has functions to create xg and shot vars

import process_players     #this module parses players and adds to players table
                           #if not present
