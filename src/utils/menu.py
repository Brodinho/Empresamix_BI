import streamlit as st

def show_menu():
    st.markdown("### Menu Principal")
    
    if st.button("📈 Dashboard Comercial", key="comercial", use_container_width=True):
        st.switch_page("pages/1_Comercial.py")
        
    if st.button("💰 Dashboard Financeiro", key="financeiro", use_container_width=True):
        st.switch_page("pages/2_Financeiro.py")
    
    st.markdown("---")
    
    if st.button("🚪 Logout", key="logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.rerun()
