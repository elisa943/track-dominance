import fastf1 as ff
import streamlit as st
from fastf1.ergast import Ergast
from datetime import datetime
import time

"""
# Sélection d'un pilote
pilot = st.selectbox('Choisis un pilote', ['Hamilton', 'Verstappen', 'Leclerc'])
st.write(f'Vous avez choisi : {pilot}')
"""

class App():
    def __init__(self): 
        # Titre de la page
        st.title('Track Dominance')
        st.sidebar.header("F1 Track Dominance")
    
    def which_year(self):
        current_year = datetime.now().year
        years = list(range(1950, current_year + 1))
        st.session_state.selected_date = st.selectbox(
            "Which season?", 
            options=years,
            index=None
        )
        return st.session_state.selected_date
    
    def which_circuit(self, circuits):
        st.session_state.circuit = st.selectbox(
            "Which circuit?", 
            circuits,
            index=None
        )
        return st.session_state.circuit 

    def load_data(self, season_selected, circuit_selected, type_of_session):
        with st.spinner('Loading data...'):
            session_selected = ff.get_session(season_selected, circuit_selected, type_of_session)
            session_selected.load()
            time.sleep(5)
            return session_selected

