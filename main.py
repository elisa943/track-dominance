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
                    # Get event 
                    event = ff.get_event(st.session_state.season_selected, st.session_state.circuit_selected)

                    # Get session (Race)
                    session_selected = ff.get_session(st.session_state.season_selected, st.session_state.circuit_selected, type_of_session)
                    st.session_state.session_selected = app.load_data(session_selected)
                    if st.session_state.session_selected != None:
                        circuit = session_selected.get_circuit_info()
                        
                        # Get drivers
                        drivers_info = ergast.get_driver_info(
                            season=st.session_state.season_selected, 
                            circuit=st.session_state.circuit_selected, 
                            result_type=type_result
                        )
                        drivers_info = drivers_info.to_numpy()
                        num_drivers = len(drivers_info)
                        drivers_names = [drivers_info[i][4] + " " + drivers_info[i][5] for i in range(num_drivers)]
                        drivers_abr = [drivers_info[i][2] for i in range(num_drivers)]
                        abr_to_name = {drivers_abr[i]: drivers_names[i] for i in range(num_drivers)}
                        name_to_abr = {drivers_names[i]: drivers_abr[i] for i in range(num_drivers)}
                        driver_to_color = ff.plotting.get_driver_color_mapping(session_selected)

                        st.session_state.driver_1, st.session_state.driver_2 = app.which_drivers(drivers_names)
                        if st.session_state.driver_1 != None and st.session_state.driver_2 != None:
                            displayTrack_driver_1 = DisplayTrack(session_selected, circuit, driver_to_color[name_to_abr[st.session_state.driver_1]], st.session_state.driver_1)
                            displayTrack_driver_2 = DisplayTrack(session_selected, circuit, driver_to_color[name_to_abr[st.session_state.driver_2]], st.session_state.driver_2)
                            displayTrack_driver_1.plot_streamlit()
                            displayTrack_driver_2.plot_streamlit()

    
    #lap_compare = LapComparator((driver_selected_1, driver_selected_2), session_selected, fastest_lap=(False, False), num_lap=(1, 1))
    #laps = lap_compare.laps()

if __name__ == "__main__":
    main()