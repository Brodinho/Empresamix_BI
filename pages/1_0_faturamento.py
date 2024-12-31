import streamlit as st
from src.services.api_service import carregar_dados_faturamento
from dashboards_comercial.visualizations_faturamento import (
    criar_grafico_linha_mensal,
    criar_mapa_faturamento,
    criar_grafico_categorias,
    criar_grafico_estados
)

def show_faturamento():
    st.title("Dashboard de Faturamento")
    
    # Carrega dados
    df = carregar_dados_faturamento()
    
    if df is not None:
        # Filtro de Anos
        anos_disponiveis = sorted(df['data'].dt.year.unique(), reverse=True)
        anos_selecionados = st.multiselect(
            "Selecione o(s) ano(s):",
            anos_disponiveis,
            default=anos_disponiveis
        )
        
        if not anos_selecionados:
            st.warning("Por favor, selecione pelo menos um ano.")
            return
            
        # Filtrar dados pelos anos selecionados
        df_filtrado = df[df['data'].dt.year.isin(anos_selecionados)]
        
        # Mapa (ocupando toda a largura)
        st.subheader("Distribuição Geográfica do Faturamento")
        fig_map = criar_mapa_faturamento(df_filtrado)
        if fig_map:
            st.plotly_chart(fig_map, use_container_width=True)
        
        # Criar duas colunas para os demais gráficos
        col1, col2 = st.columns(2)
        
        # Gráfico de linha na primeira coluna
        with col1:
            st.subheader("Evolução Mensal do Faturamento")
            fig_line = criar_grafico_linha_mensal(df_filtrado)
            if fig_line:
                st.plotly_chart(fig_line, use_container_width=True)
        
        # Gráfico de categorias na segunda coluna
        with col2:
            st.subheader("Faturamento por Categoria")
            fig_cat = criar_grafico_categorias(df_filtrado)
            if fig_cat:
                st.plotly_chart(fig_cat, use_container_width=True)
        
        # Gráfico de estados
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Faturamento por Estado")
            fig_estados = criar_grafico_estados(df_filtrado)
            if fig_estados:
                st.plotly_chart(fig_estados, use_container_width=True)

# Executar o dashboard
show_faturamento()
