import fastf1 as ff
from fastf1.plotting import *
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from SubTrack import * 
from DisplayTrack import DisplayTrack

class LapComparator(): # https://docs.fastf1.dev/time_explanation.html#lap-timing
    def __init__(self, driver_abbr, session, driver_color, circuit, fastest_lap=(True, True), num_lap=(0, 0)):
        self.driver_abbr = driver_abbr # Couple of int 
        self.session = session
        self.driver_color = driver_color 
        self.circuit = circuit
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

        return lap

    def speeds(self, lap):
        speed = [None, None]
        timestamps = [None, None]
        
        speed[0] = lap[0]['Speed'].to_numpy()
        speed[1] = lap[1]['Speed'].to_numpy()

        timestamps[0] = lap[0]['Time'].dt.total_seconds().to_numpy()  # Time in seconds
        timestamps[1] = lap[1]['Time'].dt.total_seconds().to_numpy()  # Time in seconds

        return speed, timestamps

    def interpolate_data(self, speeds, timestamps): 
        """ Interpolate both distance and time of two trajectories """ 
        # Create DataFrame
        df = pd.DataFrame({'timestamp': timestamps, 'speed': speeds})

        # Set index to timestamp
        df.set_index('timestamp', inplace=True)

        # Interpolate speed values
        df['speed'] = df['speed'].interpolate(method='linear')

        # Resample to create uniform timestamps
        uniform_timestamps = np.linspace(df.index.min(), df.index.max(), num=1000)
        uniform_speeds = np.interp(uniform_timestamps, df.index, df['speed'])

        return uniform_timestamps, uniform_speeds

    def get_uniform_time_speed(self):
        laps = self.laps()
        speeds, timestamps = self.speeds(laps)

        # Interpolate both drivers' speeds and timestamps
        uniform_timestamps = []
        uniform_speeds = []

        for i in range(2):
            ut, us = self.interpolate_data(speeds[i], timestamps[i])
            uniform_timestamps.append(ut)
            uniform_speeds.append(us)

        return uniform_timestamps, uniform_speeds

    """
    def select_fastest(self): 
        # Selects the fastest portions of the track by each driver
        uniform_timestamps, uniform_speeds = self.get_uniform_time_speed()
        pass
    """ 
    def plot_streamlit(self):
        uniform_timestamps, uniform_speeds = self.get_uniform_time_speed()
        st.title(f"Speed Profile for {self.driver_abbr[0]} and {self.driver_abbr[1]}")
        
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
    
    def plot_distances(self):
        distances = self.get_distances()
        _, timestamps = self.speeds(self.laps())

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(timestamps[0], distances[0], label=f"{self.driver_abbr[0]}", color=self.driver_color[0])
        ax.plot(timestamps[1], distances[1], label=f"{self.driver_abbr[1]}", color=self.driver_color[1])
        ax.set_ylabel("Distance (m)")
        ax.set_xlabel("Time (s)")
        ax.legend()
        ax.grid()

        st.pyplot(fig)

    def get_distances(self):
        laps = self.laps()
        distances = [None, None]
        distances[0] = laps[0]['Distance'].to_numpy()
        distances[1] = laps[1]['Distance'].to_numpy()
        return distances
    """
    def get_telemetry_laps(self):
        laps = self.laps()
        laps[0] = get_telemetry(laps[0])
        laps[1] = get_telemetry(laps[1])
        return laps 
    
    def add_relative_distances(self, laps):
        laps[0].add_relative_distance() 
        laps[1].add_relative_distance() 
    """
    @staticmethod
    def weighted_middle(speed1, speed2, coef1, coef2):
        """ Middle value between two values weighted by coefficients """
        return coef1 * speed1 + coef2 * speed2

    def interpolation(self, speed1, speed2, timestamp1, timestamp2, inverse=False):
        """ Linear interpolation of speed and timestamps """
        if len(speed1) != len(timestamp1) or len(speed2) != len(timestamp2): 
            raise ValueError("Length of positions and timestamps must be equal")

        if len(speed1) > len(speed2): 
            return self.interpolation(speed2, speed1, timestamp2, timestamp1, True)
        elif len(speed1) == len(speed2): 
            return speed1, speed2, timestamp1, timestamp2
        else: 
            # Interpolation of positions
            new_timestamp2 = np.linspace(timestamp2[0], timestamp2[-1], num=len(timestamp1))
            new_speed2 = np.zeros((len(timestamp1), 1))
            previous_timestamp = 0
            for i in range(len(new_speed2)):
                if timestamp2[previous_timestamp] <= new_timestamp2[i] < timestamp2[previous_timestamp+1]:
                    coef1 = (new_timestamp2[i] - timestamp2[previous_timestamp])/len(timestamp1)
                    coef2 = (timestamp2[previous_timestamp + 1] - new_timestamp2[i])/len(timestamp1)
                    new_speed2[i] = self.weighted_middle(speed2[previous_timestamp], speed2[previous_timestamp+1], coef1, coef2)
                else: 
                    previous_timestamp += 1
                    i -= 1
            if inverse:
                return new_speed2, speed1, new_timestamp2, timestamp1
            return speed1, new_speed2, timestamp1, new_timestamp2
    
    def selects_fastest_portions(self, speed1, speed2):
        """ Returns a list of values (1 or 2) indicating which driver was the fastest in each portion """
        if len(speed1) != len(speed2):
            raise ValueError("Speed length is incorrect")
        return [1 if speed1[i] > speed2[i] else 2 for i in range(len(speed1))]
    
    def get_speed_timestamps(self):
        laps = self.laps()
        speeds, timestamps = self.speeds(laps)
        return speeds[0], speeds[1], timestamps[0], timestamps[1]
    
    def interpolation_track(self, track, size):
        # Create an array of indices for the original track
        original_indices = np.linspace(0, len(track) - 1, num=len(track))
        
        # Create an array of indices for the new track
        new_indices = np.linspace(0, len(track) - 1, num=size)
        
        # Interpolate the track to match the length of the speed list
        new_track = np.zeros((size, track.shape[1]))
        for i in range(track.shape[1]):
            new_track[:, i] = np.interp(new_indices, original_indices, track[:, i])
        
        return new_track

    def plot_streamlit_dominance(self):
        speed1, speed2, timestamp1, timestamp2 = self.get_speed_timestamps()
        speed1, speed2, timestamp1, timestamp2 = self.interpolation(speed1, speed2, timestamp1, timestamp2)
        portions = self.selects_fastest_portions(speed1, speed2)
        
        selected_portions = [] # Time during which driverID is faster than the other driver
        driverID = portions[0]
        driverIndex = 0
        for i in range(1, len(portions)):
            if portions[i] != driverID:
                selected_portions.append((driverID - 1, i - driverIndex))
                driverID = portions[i]
                driverIndex = i 
        selected_portions.append((driverID - 1, len(portions) - driverIndex))
        print(selected_portions)
        
        # Creates figure
        fig, ax = plt.subplots()
        
        fastest_lap = self.session.laps.pick_fastest()
        pos = fastest_lap.get_pos_data()
        
        # Get an array of shape [n, 2] where n is the number of points and the second axis is x and y.
        track = pos.loc[:, ('X', 'Y')].to_numpy()

        # Convert the rotation angle from degrees to radian.
        track_angle = self.circuit.rotation / 180 * np.pi

        # Rotate and plot the track map.
        rotated_track = DisplayTrack.rotate(track, angle=track_angle)
        rotated_track_interp = self.interpolation_track(rotated_track, len(speed1))

        #ax.plot(rotated_track_interp[:, 0], rotated_track_interp[:, 1], color='black')
        # for i in range(len(portions)):
        #     ax.plot(rotated_track_interp[i, 0], rotated_track_interp[i, 1], marker='o', color=self.driver_color[portions[i] - 1])

        index = 0
        for i in range(len(selected_portions)):
            driverID = selected_portions[i][0]
            num_index = selected_portions[i][1]
            ax.plot(rotated_track_interp[index:num_index, 0], rotated_track_interp[index:num_index, 1], color=self.driver_color[driverID])
            index += num_index

        # Add plot details
        ax.legend()
        ax.set_title(f"Track dominance between {self.driver_abbr[0]} and {self.driver_abbr[1]}")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_aspect('equal')

        # Display the plot in Streamlit
        st.pyplot(fig)

