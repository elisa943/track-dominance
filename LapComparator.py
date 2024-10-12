import fastf1 as ff
from fastf1.plotting import *
import numpy as np
from matplotlib import pyplot as plt
from SubTrack import * 

class LapComparator(): # https://docs.fastf1.dev/time_explanation.html#lap-timing
    def __init__(self, driver_abbr, session, fastest_lap=(True, True), num_lap=(0, 0)):
        self.driver_abbr = driver_abbr # Couple of int 
        self.session = session 
        self.fastest_lap = fastest_lap # Couple of bool
        self.num_lap = num_lap
        self.FREQUENCY = 1000 # Frequency of telemetry 
    
    def laps(self):
        lap = [None, None]
        
        # Retrieve laps
        for i in range(2):
            if self.fastest_lap[i]:
                lap[i] = self.session.laps.pick_driver(self.driver_abbr[i]).pick_fastest()
            else:
                lap[i] = self.session.laps.pick_laps(self.num_lap[i]).pick_driver(self.driver_abbr[i])
        
        # Add 'Distance' column
        # lap[0] = lap[0].get_telemetry().add_distance()
        # lap[1] = lap[1].get_telemetry().add_distance()

        print(lap[0]['Time'])
        print(lap[0]['LapStartTime'])
        print(lap[0].get_pos_data().loc[:, ('X', 'Y')].to_numpy())


        return lap

