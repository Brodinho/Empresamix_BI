import streamlit as st
from utils.api_connector import APIConnector
from utils.theme_config import COLORS, PLOT_CONFIG
from utils.menu import show_sidebar
from datetime import datetime

# CSS para ocultar elementos padrão do Streamlit
css = """
<style>
    /* Oculta elementos padrão */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Oculta navegação padrão do Streamlit */
    div[data-testid="stSidebarNav"] {display: none !important;}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# Mostra o menu personalizado
show_sidebar()

# Resto do código do dashboard financeiro...
