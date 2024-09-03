# from tkinter import * # Listbox widget 
import numpy as np
import os
from fastf1.ergast import Ergast
from DisplayTrack import *
from datetime import datetime

def clear(year: int):
    clear_cache(cache_dir=str(year))

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_season(season_selected: int):
    current_year = datetime.now().year
    return season_selected >= 1950 and season_selected <= current_year

def check_circuit(circuit_selected: int, circuitsId_season_selected):
    return 0 <= circuit_selected < len(circuitsId_season_selected)

def check_driver(driver: str, drivers_names, drivers_abr):
    return driver.lower() in drivers_names or driver.upper() in drivers_abr

def display_drivers_list(circuitsId_season_selected):
    for i in range(len(circuitsId_season_selected)):
        print(i, circuitsId_season_selected[i])

def main():
    clear_terminal()
    ergast = Ergast()
    type_of_session = 'Race'
    type_result = 'pandas'

    # Pick season
    season_selected = int(input("Which season ? "))
    if not check_season(season_selected): 
        print("Pick a year between 1950 and the current year.")
        return
    
    # Get all circuits from season selected by user  
    circuitsId_season_selected = ergast.get_circuits(season=season_selected, result_type=type_result)["circuitId"].tolist()
    
    # Pick circuit
    clear_terminal()
    display_drivers_list(circuitsId_season_selected)
    circuit_selected = int(input("Which circuit (enter number) ? "))
    if not check_circuit(circuit_selected, circuitsId_season_selected):
        print("Pick a circuit from the season.")
        return 
    circuit_selected = circuitsId_season_selected[circuit_selected]

    session_selected = ff.get_session(season_selected, circuit_selected, type_of_session)
    session_selected.load()
    
    event = ff.get_event(season_selected, circuit_selected)
    circuit = session_selected.get_circuit_info()
    
    # Drivers who raced that weekend
    drivers_info = ergast.get_driver_info(season=season_selected, circuit=circuit_selected, result_type=type_result).to_numpy()
    num_drivers = len(drivers_info)
    drivers_abr = [drivers_info[i][2] for i in range(num_drivers)]
    drivers_names = [drivers_info[i][4] + " " + drivers_info[i][5] for i in range(num_drivers)]
    abr_to_name = {drivers_abr[i]: drivers_names[i] for i in range(num_drivers)}
    drivers_colors = [ff.plotting.driver_color(drivers_abr[i]) for i in range(num_drivers)] 
    driver_to_color = {drivers_abr[i]: drivers_colors[i] for i in range (num_drivers)}

    clear_terminal()
    print(drivers_abr)
    driver_selected_1 = input("Pick a driver : ")
    driver_selected_2 = input("Pick a second driver : ")
    if not check_driver(driver_selected_1, drivers_names, drivers_abr) or not check_driver(driver_selected_2, drivers_names, drivers_abr):
        print("Pick a driver from the list")
        return 
    
    displayTrack_driver_1 = DisplayTrack(session_selected, circuit, driver_to_color[driver_selected_1], abr_to_name[driver_selected_1])
    displayTrack_driver_2 = DisplayTrack(session_selected, circuit, driver_to_color[driver_selected_2], abr_to_name[driver_selected_2])

    displayTrack_driver_1.plot()
    displayTrack_driver_2.plot()

if __name__ == "__main__":
    main()