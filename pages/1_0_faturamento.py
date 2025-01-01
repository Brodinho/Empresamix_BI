import streamlit as st
from src.services.api_service import carregar_dados_faturamento
from dashboards_comercial.visualizations_faturamento import (
    criar_grafico_linha_mensal,
    criar_mapa_faturamento,
    criar_grafico_categorias,
    criar_grafico_faturamento_estado,
    criar_grafico_faturamento_categoria
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
        
        # Layout dos gráficos usando colunas
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de Evolução Mensal
            fig_evolucao = criar_grafico_linha_mensal(df_filtrado)
            st.plotly_chart(fig_evolucao, use_container_width=True)
        
        with col2:
            # Gráfico de Categorias - usando a abordagem que remove o título extra
            _, subcol, _ = st.columns([1, 8, 1])
            with subcol:
                fig_categorias = criar_grafico_faturamento_categoria(df_filtrado)
                st.plotly_chart(fig_categorias, use_container_width=True)
        
        # Gráfico de Estados - já ajustado anteriormente
        _, col_estados, _ = st.columns([1, 8, 1])
        with col_estados:
            fig_estados = criar_grafico_faturamento_estado(df_filtrado)
            st.plotly_chart(fig_estados, use_container_width=True)

# Executar o dashboard
show_faturamento()
