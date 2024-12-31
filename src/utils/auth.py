import streamlit as st
from src.api.api_connector import APIConnector

def check_authentication():
    """Verifica se o usuário está autenticado"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        
    if not st.session_state.authenticated:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            
            if st.form_submit_button("Login"):
                try:
                    api = APIConnector()
                    if api.authenticate(username, password):
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error("Usuário ou senha inválidos")
                except Exception as e:
                    st.error(f"Erro ao autenticar: {str(e)}")
