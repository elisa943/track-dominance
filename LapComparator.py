import fastf1 as ff
from fastf1.plotting import *
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from SubTrack import * 

class LapComparator(): # https://docs.fastf1.dev/time_explanation.html#lap-timing
    def __init__(self, driver_abbr, session, driver_color, fastest_lap=(True, True), num_lap=(0, 0)):
        self.driver_abbr = driver_abbr # Couple of int 
        self.session = session
        self.driver_color = driver_color 
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
        
        car_data = [None, None]
        car_data[0] = lap[0].get_car_data().add_distance()
        car_data[1] = lap[1].get_car_data().add_distance()

        lap[0] = lap[0].get_telemetry()
        lap[1] = lap[1].get_telemetry()

        return lap, car_data

    def speeds(self, lap):
        speed = [None, None]
        timestamps = [None, None]
        
        speed[0] = lap[0]['Speed'].to_numpy()
        speed[1] = lap[1]['Speed'].to_numpy()

        timestamps[0] = lap[0]['Time'].dt.total_seconds().to_numpy()  # Time in seconds
        timestamps[1] = lap[1]['Time'].dt.total_seconds().to_numpy()  # Time in seconds

        return speed, timestamps

    def interpolate_data(self, speeds, timestamps):
        # Create DataFrame
        df = pd.DataFrame({'timestamp': timestamps, 'speed': speeds})

        # Set index to timestamp
        df.set_index('timestamp', inplace=True)

        # Interpolate speed values
        df['speed'] = df['speed'].interpolate(method='linear')

        # Resample to create uniform timestamps
        uniform_timestamps = np.linspace(df.index.min(), df.index.max(), num=1000)  # 1000 points between min and max
        uniform_speeds = np.interp(uniform_timestamps, df.index, df['speed'])

        return uniform_timestamps, uniform_speeds

    def get_uniform_time_speed(self):
        laps, car_data = self.laps()
        speeds, timestamps = self.speeds(laps)

        # Interpolate both drivers' speeds and timestamps
        uniform_timestamps = []
        uniform_speeds = []

        for i in range(2):
            ut, us = self.interpolate_data(speeds[i], timestamps[i])
            uniform_timestamps.append(ut)
            uniform_speeds.append(us)

        return uniform_timestamps, uniform_speeds

    def plot_streamlit(self): # Uniform speed isn't the best option : ex : HAM and ZHO

        uniform_timestamps, uniform_speeds = self.get_uniform_time_speed()

        st.title(f"Speed Profile for {self.driver_abbr[0]} and {self.driver_abbr[0]}")

        # Create a matplotlib figure
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plotting
        ax.plot(uniform_timestamps[0], uniform_speeds[0], label=f"{self.driver_abbr[0]}", color=self.driver_color[0])
        ax.plot(uniform_timestamps[1], uniform_speeds[1], label=f"{self.driver_abbr[1]}", color=self.driver_color[1])
        
        ax.set_title(f"Speed Profile for {self.driver_abbr[0]} and {self.driver_abbr[1]}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Speed (m/s)")
        ax.legend()
        ax.grid()

        # Use Streamlit to display the plot
        st.pyplot(fig)
