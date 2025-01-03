import streamlit as st
from src.utils.auth import authenticate_user

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Login - EmpresaMix BI",
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # CSS customizado
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        
        .login-container {
            max-width: 400px;
            margin: 2rem auto;
            padding: 2rem;
            background: rgba(17, 25, 40, 0.75);
            border-radius: 12px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.125);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .login-logo {
            font-size: 40px;
            margin-bottom: 1rem;
        }
        
        .login-title {
            font-size: 24px;
            font-weight: 600;
            color: #ffffff;
            margin: 0.5rem 0;
        }
        
        .login-subtitle {
            color: #9CA3AF;
            font-size: 14px;
        }
        
        .input-container {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 0.5rem;
            margin-bottom: 1rem;
        }
        
        .stTextInput input {
            background: transparent !important;
            border: none !important;
            padding: 0.5rem !important;
            color: white !important;
            height: 40px !important;
        }
        
        .stTextInput input:focus {
            box-shadow: none !important;
        }
        
        .stButton button {
            width: 100%;
            background: linear-gradient(45deg, #3B82F6, #2563EB) !important;
            color: white !important;
            border: none !important;
            padding: 0.75rem !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            margin-top: 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: linear-gradient(45deg, #2563EB, #1D4ED8) !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
            transform: translateY(-1px);
        }
        
        .error-msg {
            color: #EF4444;
            font-size: 14px;
            margin-top: 0.5rem;
            text-align: center;
        }
        
        /* Remove Streamlit branding */
        #MainMenu, footer, header {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True)

    # Layout do login
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Cabeçalho com logo
    st.markdown("""
        <div class="login-header">
            <div class="login-logo">📊</div>
            <h1 class="login-title">EmpresaMix BI</h1>
            <p class="login-subtitle">Faça login para acessar o dashboard</p>
        </div>
    """, unsafe_allow_html=True)

    # Formulário de login
    with st.form("login_form"):
        # Campo de usuário
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        usuario = st.text_input("", placeholder="Usuário", key="usuario")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Campo de senha
        st.markdown('<div class="input-container">', unsafe_allow_html=True)
        senha = st.text_input("", placeholder="Senha", type="password", key="senha")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botão de login
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            if authenticate_user(usuario, senha):
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.markdown("""
                    <div class="error-msg">
                        ❌ Usuário ou senha inválidos
                    </div>
                """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 