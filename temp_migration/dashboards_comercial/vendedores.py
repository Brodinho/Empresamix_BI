import streamlit as st
from utils.common.imports import *
from utils.common.data_processing import processar_datas
from utils.visualizations import criar_grafico_vendedores

def render_vendedores_dashboard(df_filtrado):
    """
    Renderiza o dashboard de vendedores
    """
    st.title("Análise de Vendedores")
    
    # Filtro de Anos
    anos_disponiveis = sorted(df_filtrado['data'].dt.year.unique(), reverse=True)
    anos_selecionados = st.multiselect(
        "Selecione o(s) ano(s):",
        anos_disponiveis,
        default=anos_disponiveis[:5],
        key="vendedores_anos_select"
    )
    
    # Aplicar filtro de anos
    df_anos = df_filtrado[df_filtrado['data'].dt.year.isin(anos_selecionados)]
    
    # Criação das abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Visão Geral", 
        "👤 Performance Individual", 
        "📈 Análise Temporal",
        "🗺️ Análise Geográfica",
        "🏷️ Produtos e Categorias"
    ])
    
    # Conteúdo das abas
    with tab1:
        st.header("Visão Geral")
        # Criar gráfico de Top 5 Vendedores
        fig_vendedores = criar_grafico_vendedores(df_anos)
        st.plotly_chart(fig_vendedores, use_container_width=True, key="plot_vendedores")
    
    with tab2:
        st.header("Performance Individual")
        st.info("Em desenvolvimento: Métricas individuais dos vendedores")
    
    with tab3:
        st.header("Análise Temporal")
        st.info("Em desenvolvimento: Análise de tendências e sazonalidade")
    
    with tab4:
        st.header("Análise Geográfica")
        st.info("Em desenvolvimento: Distribuição geográfica das vendas")
    
    with tab5:
        st.header("Produtos e Categorias")
        st.info("Em desenvolvimento: Análise de produtos e categorias") 