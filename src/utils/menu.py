import streamlit as st

def show_menu():
    """Exibe o menu lateral"""
    st.sidebar.title("Menu")
    
    if st.sidebar.button("Dashboard Comercial"):
        st.session_state.current_page = "comercial"
        st.experimental_set_query_params(page="comercial")
        st.rerun()
        
    if st.sidebar.button("Dashboard Financeiro"):
        st.session_state.current_page = "financeiro"
        st.experimental_set_query_params(page="financeiro")
        st.rerun()
        
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
