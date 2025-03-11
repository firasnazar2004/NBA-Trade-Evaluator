import pandas as pd 
from nba_api.stats.endpoints import PlayerCareerStats
from bpmcalc import get_bpm

'''
Star Value Calculation 

SV=BPM × f(Age,Percentile)

Percentile refers to the player's percentile ranking in terms of BPM
'''