import streamlit as st
from src.api.api_connector import APIConnector
from src.utils.theme_config import COLORS
from src.utils.auth import check_authentication   
import os
from dotenv import load_dotenv
from src.utils.menu import show_menu
import pandas as pd

# Carrega variáveis de ambiente
load_dotenv()

# Inicialização do session_state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'df_filtrado' not in st.session_state:
    st.session_state.df_filtrado = None

# Configuração da página
st.set_page_config(
    page_title="EmpresaMix - BI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para controlar a visibilidade dos elementos
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

# MANTENHA APENAS ESTE BLOCO DE LOGIN
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form(key="login_form_unique"):
            st.text_input("Usuário", key="username")
            st.text_input("Senha", type="password", key="password")
            submit = st.form_submit_button("Entrar")
            
            if submit:
                username = st.session_state.username
                password = st.session_state.password
                
                # Debug: mostrar valores recebidos
                st.write(f"Username digitado: {username}")
                st.write(f"Password digitado: {password}")
                
                # Validação mais explícita
                if username.strip() == "admin" and password.strip() == "admin":
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error(f"Usuário ou senha inválidos! Verifique suas credenciais.")
                    st.error(f"Esperado: admin/admin")
                    st.error(f"Recebido: {username}/{password}")

def carregar_dados():
    """Função para carregar/atualizar dados"""
    with st.spinner("Carregando dados..."):
        try:
            api = APIConnector()
            st.session_state.df_filtrado = api.get_dados()
            st.success("Dados atualizados com sucesso!")
        except Exception as e:
            st.error(f"Erro ao carregar dados: {str(e)}")

# Interface principal (após login)
if st.session_state.authenticated:
    st.title("EmpresaMix - Dashboard")

    # Botão para atualização manual dos dados
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Atualizar Dados"):
            # Limpar cache antes de recarregar
            st.cache_data.clear()
            carregar_dados()

    # Carregar dados iniciais se necessário
    if st.session_state.df_filtrado is None:
        carregar_dados()

    # Mostrar informações sobre os dados
    if st.session_state.df_filtrado is not None:
        with col1:
            st.info(f"Última atualização: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Menu lateral personalizado
    with st.sidebar:
        show_menu()

    # Cards informativos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style="background-color: {COLORS["card"]}; padding: 20px; border-radius: 10px; margin: 10px;">
                <h2 style="color: {COLORS["blue"]};">Comercial</h2>     
                <p style="color: #FAFAFA;">Indicadores comerciais e vendas</p>
                <ul style="color: #FAFAFA;">
                    <li>Faturamento</li>
                    <li>Vendas por Período</li>
                    <li>Top Clientes e Produtos</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background-color: {COLORS["card"]}; padding: 20px; border-radius: 10px; margin: 10px;">
                <h2 style="color: {COLORS["orange"]};">Financeiro</h2>  
                <p style="color: #FAFAFA;">Indicadores financeiros e fluxo de caixa</p>
                <ul style="color: #FAFAFA;">
                    <li>Receita, Custos e Margem</li>
                    <li>Análise Mensal Financeira</li>
                    <li>Distribuição de Custos</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )