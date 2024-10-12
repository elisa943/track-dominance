import numpy as np
from fastf1.ergast import Ergast
from DisplayTrack import *
from LapComparator import *
from App import *
from datetime import datetime

def clear(year: int):
    clear_cache(cache_dir=str(year))

def check_driver(driver: str, drivers_names, drivers_abr):
    return driver.lower() in drivers_names or driver.upper() in drivers_abr

def main():
    ergast = Ergast()  # streamlit run main.py
    app = App()
    type_of_session = 'Race'
    type_result = 'pandas'

    # Pick season
    st.session_state.season_selected = app.which_year()

    # Get all circuits from season selected by user  
    if 'season_selected' in st.session_state:
        if st.session_state.season_selected is not None:
            circuitsId_season_selected = ergast.get_circuits(season=st.session_state.season_selected, result_type=type_result)["circuitId"].tolist()
        
            # Pick circuit
            st.session_state.circuit_selected = app.which_circuit(circuitsId_season_selected)
        
            if 'circuit_selected' in st.session_state:
                if st.session_state.circuit_selected is not None:
                    st.session_state.session_selected = app.load_data(st.session_state.season_selected, st.session_state.circuit_selected, type_of_session)
                    event = ff.get_event(st.session_state.season_selected, st.session_state.circuit_selected)
                    circuit = st.session_state.session_selected.get_circuit_info()
                    st.write('Data loaded')


    #session_selected = ff.get_session(season_selected, circuit_selected, type_of_session)
    #session_selected.load()
    #event = ff.get_event(season_selected, circuit_selected)
    #circuit = session_selected.get_circuit_info()
    """
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
    

    lap_compare = LapComparator((driver_selected_1, driver_selected_2), session_selected, fastest_lap=(False, False), num_lap=(1, 1))
    laps = lap_compare.laps()

    input()

    # Display each driver's fastest laps
    displayTrack_driver_1 = DisplayTrack(session_selected, circuit, driver_to_color[driver_selected_1], abr_to_name[driver_selected_1])
    displayTrack_driver_2 = DisplayTrack(session_selected, circuit, driver_to_color[driver_selected_2], abr_to_name[driver_selected_2])
    
    displayTrack_driver_1.plot()
    displayTrack_driver_2.plot()
    """

if __name__ == "__main__":
    main()