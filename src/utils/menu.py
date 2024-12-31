import streamlit as st

def show_menu():
    """Exibe o menu lateral"""
    st.sidebar.title("Menu")
    
    # Links diretos para as páginas
    if st.sidebar.button("🏠 Home"):
        st.switch_page("Home.py")
        
    if st.sidebar.button("📊 Dashboard Comercial"):
        st.switch_page("pages/1_comercial.py")
        
    if st.sidebar.button("💰 Dashboard Financeiro"):
        st.switch_page("pages/2_financeiro.py")
        
    if st.sidebar.button("❌ Logout"):
        st.session_state.authenticated = False
        st.rerun()
