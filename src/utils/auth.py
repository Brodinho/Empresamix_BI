import streamlit as st
from src.api.api_connector import APIConnector

def check_authentication():
    """Verifica se o usuário está autenticado e mostra tela de login se necessário"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login()
        return False
    return True

def authenticate_user(username: str, password: str) -> bool:
    """Realiza a autenticação do usuário"""
    try:
        api = APIConnector()
        if api.authenticate(username, password):
            st.session_state.authenticated = True
            return True
        return False
    except Exception as e:
        print(f"Erro na autenticação: {str(e)}")
        return False

def show_login():
    """Mostra a tela de login"""
    # CSS para remover warnings e estilizar o formulário
    st.markdown("""
    <style>
        /* Remove warnings */
        .stWarning, .stAlert, div[data-baseweb="notification"] {
            display: none !important;
        }
        
        /* Remove mensagem padrão do Streamlit */
        [data-testid="stAppViewBlockContainer"] > div:first-child {
            display: none !important;
        }
        
        /* Resto do CSS permanece igual */
        .login-box {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
            background: rgba(17, 25, 40, 0.75);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.125);
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-title {
            font-size: 24px;
            color: white;
            margin-bottom: 0.5rem;
        }
        .input-group {
            margin-bottom: 1rem;
        }
        .input-label {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
            color: rgba(255, 255, 255, 0.8);
        }
        .input-label-icon {
            font-size: 16px;
        }
        .stTextInput input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            color: white !important;
            padding: 0.75rem !important;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(45deg, #3B82F6, #2563EB);
            color: white;
            border: none;
            padding: 0.75rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
        .info-message {
            max-width: 400px;
            margin: 1rem auto;
            padding: 1rem;
            background: #3B82F6;
            border-radius: 8px;
            text-align: center;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # Container centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        
        # Cabeçalho
        st.markdown("""
            <div class="login-header">
                <div style="font-size: 40px;">📊</div>
                <h1 class="login-title">EmpresaMix BI</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Formulário
        with st.form("login_form"):
            # Campo usuário com ícone ao lado do título
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-label">Usuário <span class="input-label-icon">👤</span></div>', unsafe_allow_html=True)
            usuario = st.text_input(
                "Campo de usuário",  # Label para acessibilidade
                value="",
                key="usuario",
                label_visibility="collapsed"  # Oculta o label mas mantém para acessibilidade
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Campo senha com ícone ao lado do título
            st.markdown('<div class="input-group">', unsafe_allow_html=True)
            st.markdown('<div class="input-label">Senha <span class="input-label-icon">🔒</span></div>', unsafe_allow_html=True)
            senha = st.text_input(
                "Campo de senha",  # Label para acessibilidade
                value="",
                type="password",
                key="senha",
                label_visibility="collapsed"  # Oculta o label mas mantém para acessibilidade
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.form_submit_button("Entrar"):
                if authenticate_user(usuario, senha):
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Usuário ou senha inválidos")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mensagem informativa (apenas a versão azul)
    st.markdown("""
        <div class="info-message">
            Por favor, faça login para acessar o dashboard
        </div>
    """, unsafe_allow_html=True)
