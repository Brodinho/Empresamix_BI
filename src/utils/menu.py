import streamlit as st

def show_menu():
    """
    Função unificada para mostrar o menu em todas as páginas
    """
    st.markdown("""
        <style>
            /* Remove elementos padrão */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stSidebarNav"] {display: none !important;}
            
            /* Estilo do menu lateral */
            section[data-testid="stSidebar"] {
                background-color: #1a1a1a !important;
                width: 250px !important;
            }
            
            /* Título do Menu */
            .menu-title {
                color: white !important;
                font-size: 24px !important;
                margin-bottom: 20px !important;
            }
            
            /* Botões do menu */
            .menu-button {
                background-color: transparent !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
                border-radius: 4px !important;
                padding: 8px 16px !important;
                margin: 4px 0 !important;
                width: 100% !important;
                text-align: left !important;
                cursor: pointer !important;
                transition: all 0.3s ease !important;
            }
            
            /* Hover dos botões */
            .menu-button:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }
            
            /* Botão ativo */
            .menu-button.active {
                background-color: rgba(255, 255, 255, 0.1) !important;
                border-color: rgba(255, 255, 255, 0.2) !important;
            }
            
            /* Seções do menu */
            .menu-section {
                color: #888888 !important;
                font-size: 12px !important;
                text-transform: uppercase !important;
                margin: 20px 0 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="menu-title">Menu</h1>', unsafe_allow_html=True)
    
    # Botão Home
    st.markdown("""
        <a href="/" style="text-decoration: none;">
            <button class="menu-button">🏠 Home</button>
        </a>
    """, unsafe_allow_html=True)
    
    # Seção Comercial
    st.markdown('<div class="menu-section">📊 Comercial</div>', unsafe_allow_html=True)
    
    # Itens do menu comercial
    menu_items = [
        ('📈', 'Faturamento', '/0_faturamento'),
        ('📊', 'Dataset', '/1_dataset'),
        ('👥', 'Vendedores', '/2_vendedores'),
        ('🏢', 'Clientes', '/3_clientes'),
        ('💰', 'Budget', '/4_budget'),
        ('📈', 'Trends', '/5_trends')
    ]
    
    # Determinar página atual
    current_page = st.session_state.get('current_page', '')
    
    for icon, label, url in menu_items:
        active = 'active' if url in current_page else ''
        st.markdown(f"""
            <a href="{url}" style="text-decoration: none;">
                <button class="menu-button {active}">
                    {icon} {label}
                </button>
            </a>
        """, unsafe_allow_html=True)
    
    # Seção Financeiro
    st.markdown('<div class="menu-section">💰 Financeiro</div>', unsafe_allow_html=True)
