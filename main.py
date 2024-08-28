# from tkinter import * # Listbox widget 
import numpy as np
from fastf1.ergast import Ergast
from DisplayTrack import *

def clear(year: int):
    clear_cache(cache_dir=str(year))

def main():
    ergast = Ergast()
    season_selected = 2023
    type_of_session = 'Race'
    type_result = 'pandas'

    # Circuits, Sessions & Events 
    circuitsId_season_selected = ergast.get_circuits(season=season_selected)["circuitId"].to_numpy()
    num_circuits = 1 # len(circuitsId_season_selected) 
    sessions_season = np.array([ff.get_session(season_selected, i, type_of_session) for i in range(1, num_circuits + 1)])

    # Load all sessions 
    for i in range (num_circuits): sessions_season[i].load()

    events_season = np.array([ff.get_event(season_selected, i) for i in range(1, num_circuits + 1)])
    circuits_season = np.array([sessions_season[i].get_circuit_info() for i in range(num_circuits)])

    # Drivers
    drivers_info = ergast.get_driver_info(season=season_selected, result_type=type_result).values
    num_drivers = len(drivers_info)
    drivers_abr = [drivers_info[i][2] for i in range(num_drivers)]
    drivers_names = [drivers_info[i][5] + " " + drivers_info[i][4] for i in range(num_drivers)]
    drivers_colors = [ff.plotting.driver_color(drivers_abr[i]) for i in range(num_drivers)] 
    driver_to_color = {drivers_names[i]: drivers_colors[i] for i in range (num_drivers)}

    driver_1 = drivers_abr[0]
    driver_2 = drivers_abr[1]

    displayTrack = DisplayTrack(sessions_season[0], circuits_season[0])
    displayTrack.plot()



if __name__ == "__main__":
    main()