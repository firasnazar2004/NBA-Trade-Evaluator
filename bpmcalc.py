import pandas as pd 
import numpy as np
from nba_api.stats.endpoints import PlayerCareerStats



#Simplified coefficients from ChatGpt that are based on historical BPM models
a = 0.25
b= 0.3 
c= 0.35 
d= 1
e = 0.9
f = 0.7

def calculate_bpm(points, rebounds , assists, steals, blocks, turnovers, minutes):
    if minutes == 0:
        return 0
    bpm = (a * points + 
           b * rebounds + 
           c * assists + 
           d* steals +
           e * blocks - 
           0.7 * turnovers) / minutes *36
    return round(bpm,2)

player_stats = PlayerCareerStats