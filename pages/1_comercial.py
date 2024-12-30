import streamlit as st
from dashboards_comercial.faturamento import render_faturamento_dashboard
from dashboards_comercial.vendedores import render_vendedores_dashboard

# Configuração da página
st.set_page_config(page_title="Dashboard Comercial", layout="wide")

# Seleção do dashboard no menu lateral
pagina = st.sidebar.radio(
    "Selecione a página:",
    ["📊 Faturamento", "📈 Dataset", "👥 Vendedores", "🏢 Clientes", "💰 Budget", "📉 Trends"]
)

# Renderizar apenas o dashboard selecionado
if pagina == "📊 Faturamento":
    if "df_filtrado" in st.session_state:
        render_faturamento_dashboard(st.session_state.df_filtrado)
    else:
        st.error("Dados não carregados. Por favor, carregue os dados primeiro.")
elif pagina == "👥 Vendedores":
    render_vendedores_dashboard(st.session_state.df_filtrado)
# ... outros dashboards serão adicionados aqui
