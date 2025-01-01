import streamlit as st
from src.utils.menu import show_menu

# Configuração inicial da página
st.set_page_config(
    page_title="Faturamento",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir página atual
st.session_state['current_page'] = '/0_faturamento'

# Mostrar menu
with st.sidebar:
    show_menu()

# Depois importamos o resto
from dashboards_comercial.visualizations_faturamento import (
    criar_grafico_linha_mensal,
    criar_mapa_faturamento,
    criar_grafico_faturamento_estado,
    criar_grafico_faturamento_categoria
)
from src.services.api_service import carregar_dados_faturamento

# Remover padding padrão do Streamlit
st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem;
            padding-right: 1rem;
            padding-left: 1rem;
            padding-bottom: 1rem;
        }
        .element-container {
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

def show_faturamento():
    # Carregar dados
    df_completo = carregar_dados_faturamento()
    
    # Criar filtro de anos
    anos_disponiveis = sorted(df_completo['data'].dt.year.unique())
    anos_selecionados = st.multiselect(
        "Selecione os anos:",
        anos_disponiveis,
        default=anos_disponiveis[-4:] if len(anos_disponiveis) > 4 else anos_disponiveis
    )
    
    # Aplicar filtro de anos
    if anos_selecionados:
        df_filtrado = df_completo[df_completo['data'].dt.year.isin(anos_selecionados)]
    else:
        df_filtrado = df_completo
    
    # Título do mapa
    st.markdown("<h3 style='text-align: center; color: white;'>Distribuição Geográfica do Faturamento</h3>", unsafe_allow_html=True)
    
    # Mapa de faturamento
    fig_mapa = criar_mapa_faturamento(df_filtrado)
    st.plotly_chart(fig_mapa, use_container_width=True)

    # Layout dos gráficos usando colunas
    col1, col2 = st.columns([1, 1])

    with col1:
        fig_evolucao = criar_grafico_linha_mensal(df_filtrado)
        st.plotly_chart(fig_evolucao, use_container_width=True)

    with col2:
        fig_categorias = criar_grafico_faturamento_categoria(df_filtrado)
        st.plotly_chart(fig_categorias, use_container_width=True)

    # Gráfico de Estados
    fig_estados = criar_grafico_faturamento_estado(df_filtrado)
    st.plotly_chart(fig_estados, use_container_width=True)

if __name__ == "__main__":
    show_faturamento()
