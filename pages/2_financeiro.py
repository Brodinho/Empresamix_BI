import streamlit as st
from src.utils.theme_config import COLORS
from src.utils.menu import show_menu
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="EmpresaMix - Financeiro",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

# Menu lateral
with st.sidebar:
    show_menu()

# Título
st.title("Dashboard Financeiro")

# Exemplo de conteúdo
st.markdown(
    f"""
    <div style="background-color: {COLORS["card"]}; padding: 20px; border-radius: 10px; margin: 10px;">
        <h2 style="color: {COLORS["orange"]};">Indicadores Financeiros</h2>
        <p style="color: #FAFAFA;">Visão geral das métricas financeiras</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Placeholder para gráficos
col1, col2 = st.columns(2)
with col1:
    st.metric("Receita", "R$ 250.000", "10%")
with col2:
    st.metric("Margem", "25%", "-2%")
