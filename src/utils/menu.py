import streamlit as st
import os

def get_current_page():
    """
    Determina a página atual baseado na URL
    """
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        ctx = get_script_run_ctx()
        if ctx is None:
            return None
        return os.path.basename(ctx.script_path) if ctx.script_path else None
    except:
        return None

def show_menu():
    """
    Função unificada para mostrar o menu em todas as páginas
    """
    # CSS para remover menu padrão e estilizar botões
    st.markdown("""
        <style>
            /* Remove elementos padrão do Streamlit */
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}
            
            /* Remove completamente o menu de navegação padrão */
            [data-testid="stSidebarNav"] {display: none !important;}
            section[data-testid="stSidebarNav"] {display: none !important;}
            div[data-testid="collapsedControl"] {display: none !important;}
            
            /* Estilos do menu personalizado */
            .stButton > button {
                width: 100%;
                background-color: transparent;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                padding: 8px 16px;
                margin: 4px 0;
                text-align: left;
            }
            
            .stButton > button:hover {
                border: 1px solid rgba(255, 255, 255, 0.2);
                background-color: rgba(255, 255, 255, 0.1);
            }
            
            .stButton > button:disabled {
                color: rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.05);
                background-color: transparent;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("# Menu")
    
    # Botão Home
    current_page = get_current_page()
    is_home = current_page == "Home.py"
    
    if st.button("🏠 Home", 
                key="home_btn", 
                disabled=is_home,
                use_container_width=True):
        st.switch_page("Home.py")
    
    # Seção Comercial
    st.markdown("### 📊 Comercial")
    
    # Menu items com caminhos corretos
    menu_items = [
        ('📈', 'Faturamento', '1_0_faturamento.py'),
        ('📊', 'Dataset', '1_1_dataset.py'),
        ('👥', 'Vendedores', '1_2_vendedores.py'),
        ('🏢', 'Clientes', '1_3_clientes.py'),
        ('💰', 'Budget', '1_4_budget.py'),
        ('📈', 'Trends', '1_5_trends.py')
    ]
    
    # Criar botões do menu
    for icon, label, page_file in menu_items:
        button_key = f"btn_{label.lower()}"
        is_current = current_page == page_file
        
        if st.button(
            f"{icon} {label}",
            key=button_key,
            disabled=is_current,
            use_container_width=True
        ):
            st.switch_page(f"pages/{page_file}")
    
    # Seção Financeiro
    st.markdown("### 💰 Financeiro")
