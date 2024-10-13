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
                    if 'data_loaded' not in st.session_state:
                        st.session_state.session_selected = App.load_data(session_selected)
                    if st.session_state.session_selected != None: # data is loaded
                        circuit = st.session_state.session_selected.get_circuit_info()
                        
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
                        st.session_state.data_loaded = True 

                        st.session_state.driver_1, st.session_state.driver_2 = app.which_drivers(drivers_names)
                        if st.session_state.driver_1 != None and st.session_state.driver_2 != None:
                            drivers_colors = (driver_to_color[name_to_abr[st.session_state.driver_1]], driver_to_color[name_to_abr[st.session_state.driver_2]])
                            
                            lap_compare = LapComparator((name_to_abr[st.session_state.driver_1], name_to_abr[st.session_state.driver_2]), st.session_state.session_selected, drivers_colors, fastest_lap=(False, False), num_lap=(1, 1))
                            lap_compare.plot_streamlit()
                            
                            # To be removed 
                            displayTrack_driver_1 = DisplayTrack(st.session_state.session_selected, circuit, drivers_colors[0], st.session_state.driver_1)
                            displayTrack_driver_2 = DisplayTrack(st.session_state.session_selected, circuit, drivers_colors[1], st.session_state.driver_2)
                            displayTrack_driver_1.plot_streamlit()
                            displayTrack_driver_2.plot_streamlit()


if __name__ == "__main__":
    main()