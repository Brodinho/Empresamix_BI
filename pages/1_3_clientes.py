import streamlit as st
from src.utils.theme_config import COLORS
from src.utils.menu import show_menu
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="EmpresaMix - Clientes",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para ocultar elementos padrão do Streamlit
css = '''
<style>
    #MainMenu {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    div[data-testid="stSidebarNav"] {display: none !important;}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# Menu lateral
with st.sidebar:
    show_menu()

# Título
st.title("Clientes")

# Verificar autenticação
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.warning("Por favor, faça login para acessar o dashboard.")
    st.stop()

# Conteúdo específico da página
if st.session_state.df_filtrado is not None:
    # TODO: Implementar visualizações específicas
    st.info("Dashboard em desenvolvimento")
else:
    st.error("Dados não carregados. Por favor, carregue os dados primeiro.")
