import fastf1 as ff
import streamlit as st
from fastf1.ergast import Ergast
from datetime import datetime
import time

class App():
    def __init__(self): 
        # Titre de la page
        st.title('Track Dominance')
        st.sidebar.header("F1 Track Dominance")
    
    def which_year(self):
        """ Creates selection box to select a year """
        current_year = datetime.now().year
        years = list(range(2000, current_year + 1))
        selected_date = st.selectbox(
            "Which season?", 
            options=years,
            index=None
        )
        return selected_date
    
    def which_circuit(self, circuits):
        """ Creates selection box to select a track """
        circuit = st.selectbox(
            "Which circuit?", 
            circuits,
            index=None
        )
        return circuit 

    def which_drivers(self, drivers_name):
        """ Creates selection boxes to select 2 drivers """
        driver_1 = st.selectbox(
            "First driver?", 
            drivers_name,
            index=None
        )
        driver_2 = st.selectbox(
            "Second driver?", 
            drivers_name,
            index=None
        )
        return driver_1, driver_2

    @staticmethod
    def load_data(session_selected):
        with st.spinner('Loading data...'):
            try:
                session_selected.load(weather=False, messages=False)
                return session_selected
            except Exception as e:
                return None
