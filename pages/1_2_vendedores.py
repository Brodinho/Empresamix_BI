import streamlit as st
from src.utils.menu import show_menu
from src.services.api_service import carregar_dados_faturamento
from utils.formatters import (
    formatar_moeda,
    calcular_metricas_individuais,
    calcular_tendencia,
    criar_container_kpi,
    calcular_variacao_periodo,
    gerar_insights_vendedor
)
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dashboards_comercial.visualizations_vendedores import (
    criar_grafico_top_vendedores,
    criar_treemap_vendas,
    criar_grafico_evolucao_vendas,
    criar_grafico_categorias,
    criar_indicadores_vendedor,
    criar_grafico_sazonalidade_geral,
    criar_grafico_tendencia_vendas,
    criar_grafico_comparativo_metas,
    criar_expander_info_graficos,
    criar_expander_info_tendencias,
    criar_kpis_tendencia
)

# Configuração inicial da página
st.set_page_config(page_title="Vendedores", page_icon="👥", layout="wide")

# Menu lateral
with st.sidebar:
    show_menu()

def calcular_metricas_vendedor(df):
    """Calcula métricas principais por vendedor"""
    metricas = pd.DataFrame()
    
    # Faturamento total
    metricas['faturamento_total'] = df.groupby('vendedor')['valor'].sum()
    
    # Ticket médio
    metricas['ticket_medio'] = df.groupby('vendedor')['valor'].mean()
    
    # Quantidade de vendas
    metricas['qtd_vendas'] = df.groupby('vendedor').size()
    
    # Resetar o índice
    metricas = metricas.reset_index()
    
    return metricas

def calcular_valores_cards(df_filtrado):
    """Calcula os valores para os cards com comparação ao período anterior"""
    # Implementar lógica de comparação com período anterior aqui
    # ... código para cálculo dos valores dos cards ...
    pass

def show_vendedores():
    # Estilo CSS para os cards
    st.markdown("""
        <style>
        /* Estilo base para os cards */
        div[data-testid="metric-container"] {
            background-color: rgba(28, 31, 34, 0.9);
            border: 1px solid rgba(128, 128, 128, 0.3);
            border-radius: 8px;
            padding: 15px 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Título do card */
        div[data-testid="metric-container"] label {
            font-size: 16px !important;
            color: rgb(180, 180, 180) !important;
            font-weight: 500 !important;
        }
        
        /* Valor principal */
        div[data-testid="metric-container"] div[data-testid="metric-value"] {
            font-size: 28px !important;
            font-weight: 600 !important;
            color: white !important;
            line-height: 1.4 !important;
        }
        
        /* Valor da variação (delta) */
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            font-size: 14px !important;
            line-height: 1.4 !important;
        }
        
        /* Espaçamento entre os cards */
        div.stHorizontalBlock {
            gap: 16px;
            padding: 10px 0px;
        }
        
        /* Ajuste do tamanho do container dos cards */
        div.stHorizontalBlock > div[data-testid="column"] {
            min-width: 200px;
            flex: 1;
        }
        
        /* Hover effect nos cards */
        div[data-testid="metric-container"]:hover {
            border-color: rgba(128, 128, 128, 0.5);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        </style>
    """, unsafe_allow_html=True)

    try:
        df = carregar_dados_faturamento()
        if df is None or df.empty:
            st.error("Não foi possível carregar os dados.")
            return

        st.title("Dashboard de Vendedores")
        
        # Criar filtros de data
        col_filtros1, col_filtros2 = st.columns(2)
        
        with col_filtros1:
            # Extrair anos únicos do DataFrame
            anos_disponiveis = sorted(df['data'].dt.year.unique())
            opcao_todos_anos = "Todos os Anos"
            
            anos_opcoes = [opcao_todos_anos] + anos_disponiveis
            anos_selecionados = st.selectbox(
                "Selecione o(s) ano(s):",
                options=anos_opcoes,
                index=0  # "Todos os Anos" como padrão
            )
            
            # Converter seleção para lista de anos
            anos_para_filtro = anos_disponiveis if anos_selecionados == opcao_todos_anos else [anos_selecionados]
        
        with col_filtros2:
            # Lista de meses em português
            meses = {
                0: 'Todos os Meses',
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março',
                4: 'Abril', 5: 'Maio', 6: 'Junho',
                7: 'Julho', 8: 'Agosto', 9: 'Setembro',
                10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }
            
            mes_selecionado = st.selectbox(
                "Selecione o(s) mês(es):",
                options=list(meses.keys()),
                format_func=lambda x: meses[x],
                index=0  # "Todos os Meses" como padrão
            )
            
            # Converter seleção para lista de meses
            meses_para_filtro = list(range(1, 13)) if mes_selecionado == 0 else [mes_selecionado]
        
        # Aplicar filtros
        mask = (df['data'].dt.year.isin(anos_para_filtro)) & \
               (df['data'].dt.month.isin(meses_para_filtro))
        df_filtrado = df[mask]
        
        if df_filtrado.empty:
            st.warning("Nenhum dado encontrado para os filtros selecionados.")
            return
            
        # Calcular métricas com dados filtrados
        metricas = calcular_metricas_vendedor(df_filtrado)
        
        tab1, tab2, tab3 = st.tabs([
            "📊 Performance Geral",
            "🎯 Análise Individual",
            "📈 Tendências e Projeções"
        ])
        
        with tab1:
            # KPIs em linha
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(
                    criar_container_kpi(
                        "Faturamento Total",
                        formatar_moeda(105037864.50),
                        "↑ 15% vs mês anterior"
                    ),
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    criar_container_kpi(
                        "Ticket Médio",
                        formatar_moeda(27614.21),
                        "↑ 5% vs mês anterior"
                    ),
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    criar_container_kpi(
                        "Total de Vendas",
                        f"{2995:,}",
                        "↑ 8% vs mês anterior"
                    ),
                    unsafe_allow_html=True
                )
            
            with col4:
                st.markdown(
                    criar_container_kpi(
                        "Vendedores Ativos",
                        "11",
                        "Mesma quantidade mês anterior"
                    ),
                    unsafe_allow_html=True
                )
            
            # Análise de Performance
            st.markdown("### 📈 Análise de Performance")
            
            col1, col2 = st.columns(2)
            
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
    
        with tab2:  # Análise Individual
            st.markdown("### 🎯 Análise Individual do Vendedor")
            
            if df_filtrado is None or df_filtrado.empty:
                st.warning("Nenhum dado disponível para o período selecionado.")
                return
            
            # Remover valores None e ordenar vendedores
            vendedores_disponiveis = df_filtrado['vendedor'].dropna().unique().tolist()
            try:
                vendedores_disponiveis = sorted([v for v in vendedores_disponiveis if v is not None])
            except TypeError as e:
                st.error(f"Erro ao processar lista de vendedores: {str(e)}")
                return
                
            if not vendedores_disponiveis:
                st.warning("Nenhum vendedor encontrado para o período selecionado.")
                return
                
            vendedor_selecionado = st.selectbox(
                "Selecione um vendedor:",
                options=vendedores_disponiveis,
                key="select_vendedor"
            )
            
            if vendedor_selecionado:
                try:
                    # Calcular métricas do vendedor
                    metricas_vendedor = calcular_metricas_individuais(df_filtrado, vendedor_selecionado)
                    
                    # Obter data mais recente do período
                    data_atual = df_filtrado['data'].max()
                    
                    # Calcular variações
                    _, var_faturamento = calcular_variacao_periodo(df_filtrado, vendedor_selecionado, 'valor', data_atual)
                    _, var_ticket = calcular_variacao_periodo(df_filtrado, vendedor_selecionado, 'ticket_medio', data_atual)
                    _, var_vendas = calcular_variacao_periodo(df_filtrado, vendedor_selecionado, 'qtd_vendas', data_atual)
                    _, var_clientes = calcular_variacao_periodo(df_filtrado, vendedor_selecionado, 'clientes', data_atual)
                    
                    # Criar linha de indicadores
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(
                            criar_container_kpi(
                                "Faturamento Total",
                                formatar_moeda(metricas_vendedor['faturamento_total']),
                                var_faturamento
                            ),
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.markdown(
                            criar_container_kpi(
                                "Ticket Médio",
                                formatar_moeda(metricas_vendedor['ticket_medio']),
                                var_ticket
                            ),
                            unsafe_allow_html=True
                        )
                    
                    with col3:
                        st.markdown(
                            criar_container_kpi(
                                "Total de Vendas",
                                f"{metricas_vendedor['total_vendas']:,}",
                                var_vendas
                            ),
                            unsafe_allow_html=True
                        )
                    
                    with col4:
                        st.markdown(
                            criar_container_kpi(
                                "Total de Clientes",
                                f"{metricas_vendedor['total_clientes']:,}",
                                var_clientes
                            ),
                            unsafe_allow_html=True
                        )
                    
                    # Espaço entre os indicadores e o expander
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Expander com informações sobre os gráficos
                    criar_expander_info_graficos()
                    
                    # Espaço entre o expander e os gráficos
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Gráficos em duas colunas
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.plotly_chart(
                            criar_grafico_evolucao_vendas(df_filtrado, vendedor_selecionado),
                            use_container_width=True,
                            key="evolucao_vendas"
                        )
                    
                    with col2:
                        st.plotly_chart(
                            criar_grafico_categorias(df_filtrado, vendedor_selecionado),
                            use_container_width=True,
                            key="categorias_vendedor"
                        )
                
                except Exception as e:
                    st.error(f"Erro ao processar dados do vendedor: {str(e)}")
    
        with tab3:  # Tendências e Projeções
            st.markdown("### 📈 Tendências e Projeções")
            
            # KPIs de Tendência primeiro
            criar_kpis_tendencia(df_filtrado, vendedor_selecionado)
            
            # Espaço entre os KPIs e o expander
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Agora o expander com informações
            criar_expander_info_tendencias()
            
            # Espaço entre o expander e os gráficos
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Gráficos em duas colunas
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(
                    criar_grafico_tendencia_vendas(df_filtrado, vendedor_selecionado),
                    use_container_width=True
                )
                
                st.plotly_chart(
                    criar_grafico_comparativo_metas(df_filtrado, vendedor_selecionado),
                    use_container_width=True
                )
            
            with col2:
                st.plotly_chart(
                    criar_grafico_sazonalidade_geral(df_filtrado),
                    use_container_width=True
                )
            
            # Insights automáticos
            with st.expander("💡 Insights e Recomendações"):
                insights = gerar_insights_vendedor(df_filtrado, vendedor_selecionado)
                for insight in insights:
                    st.markdown(f"• {insight}")
    
    except Exception as e:
        st.error(f"Erro ao carregar o dashboard: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    show_vendedores()
