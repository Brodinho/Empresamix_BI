import streamlit as st

def setup_page():
    """Configura o layout padrão da página"""
    # Configuração da página
    st.set_page_config(
        page_title="EmpresaMix Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None  # Desabilita o menu padrão
    )
    
    # Remover elementos indesejados via JavaScript
    st.markdown("""
        <script>
            // Função para remover elementos
            function removeElements() {
                // Remover elementos de navegação
                const elements = document.querySelectorAll('[data-testid="stSidebarNav"], .css-1d391kg, .css-1vencpc');
                elements.forEach(el => el.remove());
            }
            
            // Executar após o carregamento da página
            window.addEventListener('load', removeElements);
            // Executar periodicamente para garantir
            setInterval(removeElements, 100);
        </script>
        
        <style>
            /* Ocultar elementos padrão */
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            [data-testid="stSidebarNav"] {display: none !important;}
            .css-1d391kg {display: none !important;}
            .css-1vencpc {display: none !important;}
            
            /* Estilo para a sidebar */
            section[data-testid="stSidebar"] {
                background-color: #1E1E1E;
                width: 250px !important;
            }
            
            /* Estilo para os botões do menu */
            .stButton > button {
                width: 100%;
                background-color: transparent;
                color: white;
                border: 1px solid rgba(255,255,255,0.1);
                padding: 0.5rem;
                margin-bottom: 0.5rem;
                text-align: left;
                font-size: 1rem;
            }
            
            .stButton > button:hover {
                background-color: rgba(255,255,255,0.1);
                border-color: rgba(255,255,255,0.2);
            }
        </style>
    """, unsafe_allow_html=True)

def sidebar_menu():
    """Cria o menu lateral padronizado"""
    with st.sidebar:
        # Limpar a sidebar antes de adicionar nosso menu
        st.markdown("""
            <style>
                section[data-testid="stSidebar"] > div:first-child {
                    padding-top: 0 !important;
                }
                section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
                    display: none !important;
                }
            </style>
        """, unsafe_allow_html=True)
        
        # Adicionar nosso menu
        st.markdown("### Menu Principal")
        
        # Dashboard Comercial
        if st.button("📈 Dashboard Comercial", key="btn_comercial"):
            st.switch_page("pages/1_comercial.py")
        
        # Dashboard Financeiro
        if st.button("💰 Dashboard Financeiro", key="btn_financeiro"):
            st.switch_page("pages/2_financeiro.py")
        
        st.markdown("---")
        
        # Logout
        if st.button("🚪 Logout", key="btn_logout"):
            st.session_state.authenticated = False
            st.switch_page("Home.py")