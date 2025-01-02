import streamlit as st
from src.utils.menu import show_menu
from src.services.api_service import carregar_dados_faturamento
from utils.formatters import formatar_moeda
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboards_comercial.visualizations_vendedores import (
    criar_grafico_top_vendedores,
    criar_treemap_vendas
)

# Configuração inicial da página
st.set_page_config(page_title="Vendedores", page_icon="👥", layout="wide")

# Menu lateral
with st.sidebar:
    show_menu()

def criar_container_kpi(titulo, valor, variacao, cor_variacao="#4CAF50"):
    """Cria um container estilizado para KPI"""
    container = st.container()
    with container:
        st.markdown(f"""
            <div style="
                background-color: #1E1E1E;
                border-radius: 10px;
                padding: 15px 10px;
                height: 120px;
                border: 1px solid #333;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: space-between;
            ">
                <p style="
                    color: #CCC;
                    font-size: 0.9em;
                    margin-bottom: 5px;
                    text-align: center;
                    width: 100%;
                ">{titulo}</p>
                <div style="
                    color: white;
                    font-size: 1.1em;
                    font-weight: bold;
                    margin-bottom: 5px;
                    white-space: nowrap;
                    overflow: hidden;
                    letter-spacing: -0.5px;
                    transform: scale(0.95);
                    text-align: center;
                    width: 100%;
                ">{valor}</div>
                <p style="
                    font-size: 0.8em;
                    color: {cor_variacao};
                    margin-top: auto;
                    text-align: center;
                    width: 100%;
                ">{variacao}</p>
            </div>
        """, unsafe_allow_html=True)

def calcular_metricas_vendedor(df):
    """Calcula métricas principais por vendedor"""
    metricas = pd.DataFrame()
    
    # Faturamento total
    metricas['faturamento_total'] = df.groupby('vendedor')['valor'].sum()
    
    # Ticket médio
    metricas['ticket_medio'] = df.groupby('vendedor')['valor'].mean()
    
    # Quantidade de vendas
    metricas['qtd_vendas'] = df.groupby('vendedor').size()
    
    # Resetar o índice para transformar 'vendedor' em uma coluna
    metricas = metricas.reset_index()
    
    return metricas

def show_vendedores():
    try:
        df = carregar_dados_faturamento()
        if df is None or df.empty:
            st.error("Não foi possível carregar os dados.")
            return

        st.title("Dashboard de Vendedores")
        
        tab1, tab2, tab3 = st.tabs([
            "📊 Performance Geral",
            "🎯 Análise Individual",
            "📈 Tendências e Projeções"
        ])
        
        with tab1:
            # KPIs em linha
            col1, col2, col3, col4 = st.columns([1.1, 1, 1, 1])
            
            with col1:
                criar_container_kpi(
                    "Faturamento Total",
                    formatar_moeda(105037864.50),
                    "↑ 15% vs mês anterior"
                )
            
            with col2:
                criar_container_kpi(
                    "Ticket Médio",
                    formatar_moeda(27614.21),
                    "↑ 5% vs mês anterior"
                )
            
            with col3:
                criar_container_kpi(
                    "Total de Vendas",
                    "2.995",
                    "↑ 8% vs mês anterior"
                )
            
            with col4:
                criar_container_kpi(
                    "Vendedores Ativos",
                    "11",
                    "= Manteve vs mês anterior",
                    cor_variacao="#FFA726"
                )
            
            # Análise de Performance
            st.markdown("### 📈 Análise de Performance")
            
            col1, col2 = st.columns(2)
            
            # Calcular métricas uma única vez
            metricas = calcular_metricas_vendedor(df)
            
            with col1:
                fig_top = criar_grafico_top_vendedores(metricas)
                st.plotly_chart(
                    fig_top, 
                    use_container_width=True,
                    key="grafico_top_vendedores"
                )
            
            with col2:
                fig_dist = criar_treemap_vendas(metricas)
                st.plotly_chart(
                    fig_dist, 
                    use_container_width=True,
                    key="treemap_vendas"
                )
    
    except Exception as e:
        st.error(f"Erro ao carregar o dashboard: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    show_vendedores()
