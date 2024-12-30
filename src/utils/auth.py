import streamlit as st
from utils.api_connector import APIConnector
import base64
import os

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/jpg;base64,%s");
        background-size: cover;
        background-position: center;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def check_credentials(username: str, password: str) -> bool:
    return username == 'admin' and password == 'admin'

def login_page():
    # Verificar se o arquivo existe e carregar background
    background_path = 'C:/empresamixBI/assets/bi-background.jpg'
    if not os.path.exists(background_path):
        st.error(f"Arquivo de background não encontrado em: {background_path}")
        return

    with open(background_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    # CSS atualizado
    st.markdown(
        f"""
        <style>
        /* Reset global e background */
        body {{
            margin: 0;
            padding: 0;
            height: 100vh;
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Remove backgrounds indesejados */
        .stApp {{
            background: none !important;
            height: 100vh !important;
        }}
        
        /* Torna o retângulo completamente transparente */
        div[data-testid="stVerticalBlock"] > div:first-child > div:first-child {{
            background-color: rgba(0, 0, 0, 0) !important;
            border: none !important;
            box-shadow: none !important;
        }}
        
        /* Também aplicamos aos elementos que podem estar causando o retângulo */
        .css-1dp5vir, 
        .css-1y4p8pa,
        .css-10trblm,
        .element-container {{
            background-color: rgba(0, 0, 0, 0) !important;
            border: none !important;
            box-shadow: none !important;
        }}
        
        /* Garante que o texto do título fique visível */
        h1 {{
            background: none !important;
            color: white !important;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Criar colunas com proporções ajustadas
    margin_left, form_col, margin_right = st.columns([1.5, 3, 7])

    # Usar a coluna do meio para o formulário
    with form_col:
        # Container do formulário com glass effect
        st.markdown("""
            <div style="
                background: rgba(17, 17, 17, 0);
                backdrop-filter: blur(8px);
                border-radius: 15px;
                padding: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0);
            ">
            <div style="text-align: center; width: 100%;">
                <h1 style="
                    color: white; 
                    font-size: 2.5em; 
                    margin-bottom: 0;
                    text-align: center;
                    text-shadow: -1px -1px 0 #0D47A1, 1px -1px 0 #0D47A1, -1px 1px 0 #0D47A1, 1px 1px 0 #0D47A1, 0 0 8px rgba(13, 71, 161, 0.6);
                ">
                    EmpresaMix
                </h1>
                <p style="
                    color: white; 
                    font-size: 1.2em; 
                    margin-top: 0;
                    margin-bottom: 1em;
                    text-align: center;
                    text-shadow: -1px -1px 0 #0D47A1, 1px -1px 0 #0D47A1, -1px 1px 0 #0D47A1, 1px 1px 0 #0D47A1, 0 0 8px rgba(13, 71, 161, 0.6);
                ">
                    Business Intelligence (BI)
                </p>
                <h2 style="
                    color: white; 
                    margin-bottom: 20px; 
                    font-size: 1.5em;
                    text-align: center;
                    text-shadow: -1px -1px 0 #0D47A1, 1px -1px 0 #0D47A1, -1px 1px 0 #0D47A1, 1px 1px 0 #0D47A1, 0 0 8px rgba(13, 71, 161, 0.6);
                ">
                    Acesso ao Sistema
                </h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Campo de usuário
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.markdown('<div style="font-size: 1.5em; text-align: center;">👤</div>', unsafe_allow_html=True)
        with col2:
            username = st.text_input("", placeholder="Usuário", key='username_input', label_visibility="collapsed")

        # Campo de senha
        col1, col2 = st.columns([0.15, 0.85])
        with col1:
            st.markdown('<div style="font-size: 1.5em; text-align: center;">🔒</div>', unsafe_allow_html=True)
        with col2:
            password = st.text_input("", placeholder="Senha", type='password', key='password_input', label_visibility="collapsed")

        # Botão de login
        clicked = st.button('Acessar', use_container_width=True)
        
        if clicked:
            if check_credentials(username, password):
                st.session_state.authenticated = True
                st.session_state.login_username = username
                st.rerun()
            else:
                st.error('Usuário ou senha inválidos')

        st.markdown('</div>', unsafe_allow_html=True)

def check_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
        
    if not st.session_state['authenticated']:
        login_page()
        st.stop()
    
    return True
