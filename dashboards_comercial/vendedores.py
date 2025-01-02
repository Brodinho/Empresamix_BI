import streamlit as st
from utils.common.imports import *
from utils.common.data_processing import processar_datas
from utils.visualizations import criar_grafico_vendedores

def render_vendedores_dashboard(df_filtrado):
    """
    Renderiza o dashboard de vendedores
    """
    st.title("Análise de Vendedores")
    
    # Filtros de anos e meses
    # ... código dos filtros ...

    # Botões de navegação
    st.write("📊 Performance Geral    🎯 Análise Individual    📈 Tendências e Projeções")

    # Conteúdo da Análise Individual
    st.header("🎯 Análise Individual do Vendedor")
    
    # Seleção do vendedor
    vendedor = st.selectbox("Selecione um vendedor:", lista_vendedores)
    
    # Cards com métricas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        mostrar_card_faturamento(metricas)
    with col2:
        mostrar_card_ticket_medio(metricas)
    with col3:
        mostrar_card_total_vendas(metricas)
    with col4:
        mostrar_card_total_clientes(metricas)
        
    # Expander com informações sobre os gráficos
    criar_expander_info_graficos()
    
    # Gráficos
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        st.plotly_chart(criar_grafico_evolucao_vendas(df_anos, vendedor))
    with col_graf2:
        st.plotly_chart(criar_grafico_categorias(df_anos, vendedor)) 