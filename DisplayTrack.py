import fastf1 as ff
from fastf1.plotting import *
import numpy as np
from matplotlib import pyplot as plt
from Track import *

class DisplayTrack(Track):
    def __init__(self, session, circuit, driver_color, driver_name=None):
        self.session = session
        self.circuit = circuit 
        self.driver_name = driver_name
        self.driver_color = driver_color # RGB value 
        
    def plot(self):
        # New figure 
        plt.figure()
        
        # Plot circuit (with fastest lap) https://docs.fastf1.dev/gen_modules/examples_gallery/plot_annotate_corners.html#sphx-glr-gen-modules-examples-gallery-plot-annotate-corners-py
        fastest_lap = self.session.laps.pick_fastest()
        
        if self.driver_name != None: 
            fastest_lap = self.session.laps.pick_driver(ff.plotting.get_driver_abbreviation(self.driver_name, self.session)).pick_fastest()
        
        tel = fastest_lap.get_telemetry()
        pos = fastest_lap.get_pos_data()

        # Get an array of shape [n, 2] where n is the number of points and the second
        # axis is x and y.
        track = pos.loc[:, ('X', 'Y')].to_numpy()

        # Convert the rotation angle from degrees to radian.
        track_angle = self.circuit.rotation / 180 * np.pi

        # Rotate and plot the track map.
        rotated_track = DisplayTrack.rotate(self, track, angle=track_angle)
        plt.plot(rotated_track[:, 0], rotated_track[:, 1], color=self.driver_color)

        # Plot
        plt.legend([self.driver_name])
        plt.title(self.session.event['Location'])
        plt.xticks([])
        plt.yticks([])
        plt.axis('equal')
        plt.show()
    
    def rotate(self, xy, *, angle):
        rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                            [-np.sin(angle), np.cos(angle)]])
        return np.matmul(xy, rot_mat)
