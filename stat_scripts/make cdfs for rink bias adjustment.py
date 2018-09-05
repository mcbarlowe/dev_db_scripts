# -*- coding: utf-8 -*-
"""
Created on Sun Mar 05 18:34:37 2017

@author: Ganesh
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import thinkbayes as tb


class RinkAdjust(object):

    def __init__( self ):
        self.teamxcdf, self.teamycdf, self.otherxcdf, self.otherycdf  = {}, {}, {}, {}


    def addCDFs( self, team, this_x_cdf, this_y_cdf, other_x_cdf, other_y_cdf ):
        self.teamxcdf[team] = this_x_cdf
        self.teamycdf[team] = this_y_cdf
        self.otherxcdf[team] = other_x_cdf
        self.otherycdf[team] = other_y_cdf


    def addTeam( self, team, this_team, rest_of_league ):
        this_x_cdf = tb.MakeCdfFromPmf( tb.MakePmfFromList( this_team.X ) )
        this_y_cdf = tb.MakeCdfFromPmf( tb.MakePmfFromList( this_team.Y ) )
        other_x_cdf = tb.MakeCdfFromPmf( tb.MakePmfFromList( rest_of_league.X ) )
        other_y_cdf = tb.MakeCdfFromPmf( tb.MakePmfFromList( rest_of_league.Y ) )
        self.addCDFs( team, this_x_cdf, this_y_cdf, other_x_cdf, other_y_cdf )


    def PlotTeamCDFs( self, team, savefig=False ):
        this_x_cdf = self.teamxcdf[team]
        this_y_cdf = self.teamycdf[team]
        other_x_cdf = self.otherxcdf[team]
        other_y_cdf = self.otherycdf[team]

        f, axx = plt.subplots( 1, 2, sharey='col' )
        f.set_size_inches( 14, 8 )

        xx1, yx1 = this_x_cdf.Render()
        xx2, yx2 = other_x_cdf.Render()

        axx[0].plot( xx1, yx1, color='blue', label='@%s' % team )
        axx[0].plot( xx2, yx2, color='brown', label='@Rest of League' )
        axx[0].set_xlabel( 'CDF of X' )
        axx[0].legend()

        xy1, yy1 = this_y_cdf.Render()
        xy2, yy2 = other_y_cdf.Render()

        axx[1].plot( xy1, yy1, color='blue', label='@%s' % team )
        axx[1].plot( xy2, yy2, color='brown', label='@Rest of League' )
        axx[1].set_xlabel( 'CDF of Y' )
        axx[1].legend()

        f.suptitle( 'Cumulative Density Function for Shot Location Rink Bias Adjustment' )

        plt.show()

        if savefig:
            #f.set_tight_layout( True )
            plt.savefig( 'Rink bias CDF chart %s.png' % team )


    def rink_bias_adjust( self, x, y, team ):
        """ this method implements the actual location conversion from biased to "unbiased" shot location

         the way it works for rink bias adjustment is that for a given shot location in a specific rink,
         you find the cumulative probabilities for that x and y in that rink. Then you calculate the league
         equivalent x and y that have the same probabilities as the one measured in the specific rink

         The equivalency CDFs are calculated using only visiting teams, which ensures that both single rink and
         league wide rinks have as wide a sample of teams as possible but avoid any possible home team bias.
         All of which lets us assume that they are then unbiased enough to be representative (at least enough
         for standardization purposes)

         This is (my adaption of my understanding of) Shuckers' method for rink bias adjustment as described in Appendix A here:
         http://www.sloansportsconference.com/wp-content/uploads/2013/Total%20Hockey%20Rating%20(THoR)%20A%20comprehensive%20statistical%20rating%20of%20National%20Hockey%20League%20forwards%20and%20defensemen%20based%20upon%20all%20on-ice%20events.pdf

         for example, if a shot x coordinate is measured as xmeas in a rink

             xprob = this_x_cdf.Prob( xmeas )  # cum prob of seeing xmeas in this rink
             xadj = other_x_cdf.Value( xprob ) # value associated with same prob in rest of league

        analogous process for y

        The code for Cdf/Pmf creation and manipulation is taken directly from Allan Downey's code for "Think Bayes"
        """

        xprob = self.teamxcdf[team].Prob( x )
        newx = self.otherxcdf[team].Value( xprob )

        yprob = self.teamycdf[team].Prob( y )
        newy = self.otherycdf[team].Value( yprob )

        return newx, newy


# Read the raw data

print 'Read shots'
csvfile = 'all teams away shots generated 2017-3-5-21-5-6.csv'
shots = pd.read_csv( csvfile )

# Replace every occurrence of PHX with ARI

print 'Fix team labels'
shots['Home'] = shots.apply( lambda x: x.Home if x.Home !='PHX' else 'ARI', axis=1 )
shots['Away'] = shots.apply( lambda x: x.Away if x.Away !='PHX' else 'ARI', axis=1 )

# add a 'Direction' column to indicate the primary direction for shots. The heuristic to determine
# direction is the sign of the median of the X coordinate of shots in each period. This then lets us filter
# out shots that originate from back in the defensive zone when the signs don't match

print 'Determine shot directions for filtering rink-length shots'

gp_groups = shots.groupby( by=[ 'GameId', 'Period' ] )
meanies = gp_groups.transform(np.median)  # will give us game/period median for X and Y for every data point
shots['Direction'] = np.sign( meanies['X'] )

valid_shots = shots[ np.sign(shots.X) == shots.Direction ].copy()   # copy so we can manipulate freely

# Normalize the shots by flipping the signs on shots with negative X coordinates so they all point in the same direction

print 'Normalize shot directions'

# should actually write this to a CSV as up to here is the performance intensive part

valid_shots['X'], valid_shots['Y'] = zip( *valid_shots.apply( lambda x: (x.X, x.Y) if x.X > 0 else (-x.X,-x.Y), axis=1 ) )

# Now rip through each team and create a CDF for that team and for the other 29 teams in the league

print 'Create RinkAdjust object and generate CDF plots'

adjuster = RinkAdjust()

for team in sorted(valid_shots.Home.unique()):
#for team in [ 'EDM' ]:

    this_team = valid_shots[ valid_shots.Home == team ]
    rest_of_league = valid_shots[ valid_shots.Home != team ]

    adjuster.addTeam( team, this_team, rest_of_league )

    # if an adjustment is needed, use this routine
    # newx, newy = adjuster.rink_bias_adjust( x, y, team )

    # in the meantime, we'll just visualize the results

    adjuster.PlotTeamCDFs( team, savefig=True )
