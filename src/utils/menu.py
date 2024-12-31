import streamlit as st

def show_menu():
    """Exibe o menu lateral"""
    st.sidebar.title("Menu")
    
    # Home
    if st.sidebar.button("🏠 Home"):
        st.switch_page("Home.py")
    
    # Seção Comercial
    st.sidebar.markdown("### 📊 Comercial")
    if st.sidebar.button("📈 Faturamento", key="btn_faturamento"):
        st.switch_page("pages/1_0_faturamento.py")
    if st.sidebar.button("📊 Dataset", key="btn_dataset"):
        st.switch_page("pages/1_1_dataset.py")
    if st.sidebar.button("👥 Vendedores", key="btn_vendedores"):
        st.switch_page("pages/1_2_vendedores.py")
    if st.sidebar.button("🏢 Clientes", key="btn_clientes"):
        st.switch_page("pages/1_3_clientes.py")
    if st.sidebar.button("💰 Budget", key="btn_budget"):
        st.switch_page("pages/1_4_budget.py")
    if st.sidebar.button("📉 Trends", key="btn_trends"):
        st.switch_page("pages/1_5_trends.py")
    
    # Seção Financeira
    st.sidebar.markdown("### 💰 Financeiro")
    if st.sidebar.button("📊 Dashboard Financeiro", key="btn_financeiro"):
        st.switch_page("pages/2_financeiro.py")
    
    # Logout
    st.sidebar.markdown("---")
    if st.sidebar.button("❌ Logout", key="btn_logout"):
        st.session_state.authenticated = False
        st.rerun()
