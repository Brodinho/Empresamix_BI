import streamlit as st
import pandas as pd
from utils.comercial.visualizations import (
    criar_grafico_linha_mensal,
    criar_mapa_faturamento,
    criar_grafico_categorias,
    criar_grafico_estados
)
from utils.common.data_processing import (
    formatar_moeda,
    MESES_PT,
    aplicar_filtro_anos
)
import plotly.graph_objects as go

def render_faturamento_dashboard(df_filtrado):
    st.title("Análise de Faturamento")
    
    # Filtro de Anos
    anos_disponiveis = sorted(df_filtrado['data'].dt.year.unique(), reverse=True)
    anos_selecionados = st.multiselect(
        "Selecione o(s) ano(s):",
        anos_disponiveis,
        default=anos_disponiveis[:5]
    )
    
    # Aplicar filtro
    df_anos = aplicar_filtro_anos(df_filtrado, anos_selecionados)
    
    # Configuração dos gráficos
    st.sidebar.markdown("### Configuração dos Gráficos")
    st.sidebar.markdown("Selecione os gráficos que deseja visualizar:")
    
    # Lista para armazenar os gráficos ativos
    graficos_ativos = []
    
    # Checkboxes e criação dos gráficos
    if st.sidebar.checkbox("Mapa de Faturamento por Estado/País", value=True):
        fig_mapa = criar_mapa_faturamento(df_anos)
        graficos_ativos.append(("Distribuição Geográfica do Faturamento", fig_mapa))
    
    if st.sidebar.checkbox("Gráfico de Barras - Top 5 Estados/Países", value=True):
        fig_estados = criar_grafico_estados(df_anos)
        graficos_ativos.append(("Top 5 Estados/Países", fig_estados))
    
    if st.sidebar.checkbox("Gráfico de Linha - Faturamento Mensal", value=True):
        fig_mensal = criar_grafico_linha_mensal(df_anos)
        graficos_ativos.append(("Evolução Mensal do Faturamento", fig_mensal))
    
    if st.sidebar.checkbox("Gráfico de Barras - Top 5 Categorias", value=True):
        fig_categorias = criar_grafico_categorias(df_anos)
        graficos_ativos.append(("Top 5 Categorias", fig_categorias))
    
    # Criar layout dinâmico com os gráficos ativos
    criar_layout_dinamico(graficos_ativos)
    
    # Análise de Frequência
    st.markdown("""
    ### 🔄 Análise de Frequência de Compras
    Entenda os padrões de compra e segmentação dos clientes por frequência.
    """)
    
    with st.expander("ℹ️ Sobre a Análise de Frequência"):
        st.markdown("""
        A análise de frequência de compras é fundamental para:
        
        📊 **Segmentação de Clientes**
        * Identifica diferentes perfis de compradores
        * Permite estratégias personalizadas por segmento
        * Ajuda a entender o ciclo de compras
        """)
        
        # Métricas de frequência
        freq_compras = calcular_metricas_frequencia(df_anos)
        exibir_metricas_frequencia(freq_compras)
        exibir_graficos_frequencia(freq_compras, df_anos)

def criar_layout_dinamico(graficos_ativos):
    """
    Organiza os gráficos dinamicamente baseado nos que estão ativos
    """
    if not graficos_ativos:
        return
    
    # O mapa sempre ocupa largura total quando presente
    mapa = next((g for g in graficos_ativos if "Distribuição Geográfica" in g[0]), None)
    if mapa:
        st.subheader(mapa[0])
        st.plotly_chart(mapa[1], use_container_width=True)
        graficos_ativos = [g for g in graficos_ativos if g != mapa]
    
    # Processa os gráficos restantes em pares
    for i in range(0, len(graficos_ativos), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(graficos_ativos[i][0])
            st.plotly_chart(graficos_ativos[i][1], use_container_width=True)
        
        if i + 1 < len(graficos_ativos):
            with col2:
                st.subheader(graficos_ativos[i + 1][0])
                st.plotly_chart(graficos_ativos[i + 1][1], use_container_width=True)

def calcular_metricas_frequencia(df):
    """Calcula métricas de frequência de compras"""
    freq_compras = df.groupby('razao').agg({
        'nota': 'count',
        'valorNota': 'sum'
    }).reset_index()
    
    freq_compras.columns = ['Cliente', 'Total_Pedidos', 'Valor_Total']
    return freq_compras

# Continua...