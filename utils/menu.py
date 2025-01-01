import streamlit as st

def configurar_menu():
    """
    Configura o estilo do menu lateral
    """
    # Remove menus padrão do Streamlit
    st.markdown("""
        <style>
            /* Remove elementos padrão */
            #MainMenu {display: none !important;}
            footer {display: none !important;}
            [data-testid="stSidebarNav"] {display: none !important;}
            
            /* Estilo base do menu lateral */
            section[data-testid="stSidebar"] {
                background-color: #1a1a1a !important;
                width: 250px !important;
            }
            
            /* Estilo do título Menu */
            .menu-title {
                color: white !important;
                font-size: 24px !important;
                padding: 15px 0 10px 15px !important;
                margin: 0 !important;
                font-weight: 600 !important;
            }
            
            /* Container dos itens do menu */
            .menu-container {
                padding: 0 10px !important;
            }
            
            /* Links do menu */
            .menu-item {
                display: block !important;
                text-decoration: none !important;
                color: white !important;
                padding: 8px 12px !important;
                margin: 4px 0 !important;
                border-radius: 4px !important;
                background-color: transparent !important;
                transition: all 0.3s !important;
            }
            
            /* Hover nos links do menu */
            .menu-item:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
                text-decoration: none !important;
            }
            
            /* Item ativo do menu */
            .menu-item.active {
                background-color: #2d2d2d !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Estilo para os títulos das seções */
            .section-title {
                color: #888888 !important;
                font-size: 12px !important;
                padding: 20px 15px 10px !important;
                margin: 0 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.5px !important;
            }
            
            /* Estilo para os ícones */
            .menu-icon {
                margin-right: 10px !important;
                opacity: 0.9 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Criar estrutura do menu
    with st.sidebar:
        # Título do Menu
        st.markdown('<h1 class="menu-title">Menu</h1>', unsafe_allow_html=True)
        
        # Container dos itens
        st.markdown('<div class="menu-container">', unsafe_allow_html=True)
        
        # Botão Home com link
        st.markdown(
            '<a href="/" class="menu-item">'
            '<span class="menu-icon">🏠</span> Home'
            '</a>', 
            unsafe_allow_html=True
        )
        
        # Seção Comercial
        st.markdown('<h2 class="section-title">📊 Comercial</h2>', unsafe_allow_html=True)
        
        # Itens da seção Comercial com links
        menu_items = [
            ('📈', 'Faturamento', '/0_faturamento', True),
            ('📊', 'Dataset', '/1_dataset', False),
            ('👥', 'Vendedores', '/2_vendedores', False),
            ('🏢', 'Clientes', '/3_clientes', False),
            ('💰', 'Budget', '/4_budget', False),
            ('📈', 'Trends', '/5_trends', False)
        ]
        
        for icon, label, url, is_active in menu_items:
            active_class = 'active' if is_active else ''
            st.markdown(
                f'<a href="{url}" class="menu-item {active_class}">'
                f'<span class="menu-icon">{icon}</span> {label}'
                f'</a>',
                unsafe_allow_html=True
            )
        
        # Seção Financeiro
        st.markdown('<h2 class="section-title">💰 Financeiro</h2>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) 