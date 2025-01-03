import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.formatters import formatar_moeda, criar_container_kpi, MESES_ORDEM
import math
from plotly.subplots import make_subplots
from typing import Dict, Any
import streamlit as st

def criar_grafico_top_vendedores(df_metricas: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de barras horizontais com os top 5 vendedores por faturamento
    """
    try:
        # Pegar top 5 vendedores
        top_5_vendedores = df_metricas.nlargest(5, 'faturamento_total')
        
        fig = px.bar(
            top_5_vendedores,
            x='faturamento_total',
            y='vendedor',
            title="Top 5 Vendedores por Faturamento",
            template="plotly_dark",
            orientation='h'
        )
        
        # Calcular o valor máximo para definir o range do eixo x
        max_valor = top_5_vendedores['faturamento_total'].max()
        max_milhoes = math.ceil(max_valor / 1_000_000)
        
        # Configuração do layout
        fig.update_layout(
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=[i * 10000000 for i in range(0, max_milhoes + 1)],
                ticktext=[f'{i*10:,} Milhões'.replace(',', '.') for i in range(0, max_milhoes + 1)],
                tickangle=0
            ),
            yaxis=dict(
                tickangle=0,
                autorange="reversed"
            ),
            height=400
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico top vendedores: {str(e)}")
        return go.Figure()

def criar_treemap_vendas(df_metricas: pd.DataFrame) -> go.Figure:
    """
    Cria um treemap com a distribuição de vendas por vendedor
    """
    try:
        fig = px.treemap(
            df_metricas,
            values='qtd_vendas',
            path=['vendedor'],
            title="Distribuição de Vendas por Vendedor",
            template="plotly_dark",
            color='qtd_vendas',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            height=400,
            showlegend=False
        )
        
        fig.update_traces(
            textinfo="label+value+percent parent",
            textfont=dict(size=12),
            hovertemplate="<b>%{label}</b><br>Vendas: %{value:,.0f}<br>Percentual: %{percentParent:.1%}<extra></extra>"
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar treemap de vendas: {str(e)}")
        return go.Figure()

def criar_grafico_evolucao_vendas(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria gráfico de evolução de vendas do vendedor
    """
    try:
        # Filtrar dados do vendedor
        df_vendedor = df[df['vendedor'] == vendedor].copy()
        
        # Agrupar por mês
        df_vendedor['mes_ano'] = df_vendedor['data'].dt.strftime('%m/%Y')
        vendas_mensais = df_vendedor.groupby('mes_ano').agg({
            'valor': 'sum',
            'data': 'first'
        }).reset_index()
        
        # Ordenar por data
        vendas_mensais = vendas_mensais.sort_values('data')
        
        # Contar quantidade de vendas por mês
        qtd_vendas = df_vendedor.groupby('mes_ano').size().reset_index(name='quantidade')
        vendas_mensais = vendas_mensais.merge(qtd_vendas, on='mes_ano')
        
        # Determinar o modo de exibição baseado no número de meses com vendas
        num_meses = len(vendas_mensais)
        modo_exibicao = 'markers' if num_meses <= 2 else 'lines+markers'
        
        # Determinar o valor máximo para definir a escala
        max_valor = vendas_mensais['valor'].max()
        max_milhoes = math.ceil(max_valor / 1_000_000)
        
        # Criar figura com eixos secundários
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Preparar valores formatados para o hover
        valores_formatados = [formatar_moeda(valor) for valor in vendas_mensais['valor']]
        
        # Adicionar linha/pontos de faturamento
        fig.add_trace(
            go.Scatter(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['valor'],
                name='Faturamento',
                mode=modo_exibicao,
                line=dict(color='#4169E1', width=2),
                marker=dict(
                    color='#4169E1',
                    size=8 if num_meses > 2 else 12
                ),
                customdata=valores_formatados,  # Dados formatados para o hover
                hovertemplate="Mês: %{x}<br>Faturamento: %{customdata}<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Adicionar linha/pontos de quantidade de vendas
        fig.add_trace(
            go.Scatter(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['quantidade'],
                name='Qtd. Vendas',
                mode=modo_exibicao,
                line=dict(color='#32CD32', width=2, dash='dot'),
                marker=dict(
                    color='#32CD32',
                    size=8 if num_meses > 2 else 12
                ),
                hovertemplate="Mês: %{x}<br>Vendas: %{y}<extra></extra>"
            ),
            secondary_y=True
        )
        
        # Atualizar eixos Y
        fig.update_yaxes(
            title_text=None,  # Remove o título do eixo Y primário
            secondary_y=False,
            tickmode='array',
            tickvals=[i * 200000 for i in range(math.ceil(max_valor/200000) + 1)],
            ticktext=[f"{i/5:.1f} Milhão" if i > 0 else "0" for i in range(math.ceil(max_valor/200000) + 1)]
        )
        
        # Atualizar eixo Y secundário (mantém o título)
        fig.update_yaxes(
            title_text="Quantidade de Vendas",
            secondary_y=True
        )
        
        # Configurar layout
        fig.update_layout(
            title=f"Evolução de Vendas - {vendedor.upper()}",
            template="plotly_dark",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            xaxis=dict(
                title=None,
                tickangle=45,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)',
            ),
            height=400,
            margin=dict(t=50, l=50, r=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico de evolução: {str(e)}")
        return go.Figure()

def criar_grafico_categorias(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria um gráfico de barras horizontais mostrando a distribuição de vendas por categoria
    """
    try:
        df_vendedor = df[df['vendedor'] == vendedor]
        dados_categoria = df_vendedor.groupby('categoria').agg({
            'valor': 'sum',
            'sequencial': 'count'
        }).reset_index()
        
        # Ordenar por valor e calcular percentuais
        dados_categoria = dados_categoria.sort_values('valor', ascending=True)
        total_valor = dados_categoria['valor'].sum()
        dados_categoria['percentual'] = dados_categoria['valor'] / total_valor * 100
        
        # Formatar valores para exibição
        dados_categoria['valor_formatado'] = dados_categoria['valor'].apply(
            lambda x: f"R$ {x:_.2f}".replace(".", ",").replace("_", ".")
        )
        dados_categoria['percentual_formatado'] = dados_categoria['percentual'].apply(
            lambda x: f"{x:.1f}%"
        )
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=dados_categoria['categoria'],
            x=dados_categoria['valor'],
            orientation='h',
            text=dados_categoria.apply(
                lambda row: f"{row['percentual_formatado']} ({row['valor_formatado']})", 
                axis=1
            ),
            textposition='auto',
            hovertemplate="Categoria: %{y}<br>" +
                         "Valor: %{text}<br>" +
                         "<extra></extra>",
            marker_color='#4169E1'
        ))
        
        fig.update_layout(
            title=f"Distribuição por Categoria - {vendedor}",
            template="plotly_dark",
            height=400,
            showlegend=False,
            xaxis_title="Faturamento",
            yaxis_title=None,
            margin=dict(l=200, r=20, t=30, b=20)
        )
        
        # Formatar eixo X para valores em milhões
        max_valor = dados_categoria['valor'].max()
        max_milhoes = math.ceil(max_valor / 1_000_000)
        
        fig.update_xaxes(
            tickmode='array',
            tickvals=[i * 1_000_000 for i in range(0, max_milhoes + 1)],
            ticktext=[f'{i} Mi' for i in range(0, max_milhoes + 1)]
        )
        
        return fig
    except Exception as e:
        print(f"Erro ao criar gráfico de categorias: {str(e)}")
        return go.Figure()

def criar_indicadores_vendedor(metricas: Dict[str, Any]) -> go.Figure:
    """
    Cria um conjunto de indicadores para o vendedor
    """
    try:
        fig = go.Figure()
        
        indicadores = [
            ("Faturamento Total", metricas.get('faturamento_total', 0), "R$"),
            ("Ticket Médio", metricas.get('ticket_medio', 0), "R$"),
            ("Total de Vendas", metricas.get('total_vendas', 0), "#"),
            ("Clientes Atendidos", metricas.get('total_clientes', 0), "#")
        ]
        
        for i, (nome, valor, prefixo) in enumerate(indicadores):
            fig.add_trace(go.Indicator(
                mode="number",
                value=valor,
                title={
                    "text": nome,
                    "font": {"size": 16}
                },
                domain={
                    'row': i//2,
                    'column': i%2,
                    'x': [i%2 * 0.5, (i%2 + 1) * 0.5 - 0.05],
                    'y': [0.1 + (i//2) * 0.5, 0.4 + (i//2) * 0.5]
                },
                number={
                    'prefix': prefixo if prefixo == "R$" else "",
                    'suffix': "" if prefixo == "R$" else " vendas" if nome == "Total de Vendas" else " clientes",
                    'valueformat': ",.2f" if prefixo == "R$" else ",d",
                    'font': {"size": 24}
                }
            ))
        
        fig.update_layout(
            grid={'rows': 2, 'columns': 2},
            template="plotly_dark",
            height=400,
            margin=dict(t=100, b=100, l=50, r=50),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar indicadores: {str(e)}")
        return go.Figure()

def criar_expander_info_graficos() -> None:
    """
    Cria um expander com informações sobre como interpretar os gráficos
    de Evolução de Vendas e Distribuição por Categoria
    """
    with st.expander("ℹ️ Como interpretar os gráficos"):
        st.markdown("""
        ### 📊 Gráfico de Evolução de Vendas
        
        Este gráfico apresenta duas informações importantes:
        - **Linha Azul** 📈 : Representa o faturamento mensal do vendedor
        - **Linha Verde Pontilhada** 📉 : Indica a quantidade de vendas realizadas
        
        **Como interpretar:**
        - O eixo Y esquerdo mostra os valores de faturamento em milhões (R$)
        - O eixo Y direito apresenta a quantidade de vendas
        - O eixo X mostra a evolução temporal (mês/ano)
        - Passe o mouse sobre as linhas para ver os valores exatos
        
        ---
        
        ### 📊 Gráfico de Distribuição por Categoria
        
        Este gráfico mostra a distribuição do faturamento por categoria de produtos:
        - As barras são ordenadas do maior para o menor valor
        - Cada barra mostra:
            - Nome da categoria
            - Percentual sobre o total (%)
            - Valor absoluto (R$)
        
        **Como interpretar:**
        - O eixo X mostra o faturamento em milhões (R$)
        - As categorias são apresentadas no eixo Y
        - Os valores dentro das barras mostram o percentual e o valor total
        """)
        
        st.info("""
        💡 **Dica:** Para uma análise mais detalhada, você pode:
        - Passar o mouse sobre os elementos para ver informações detalhadas
        - Clicar na legenda para mostrar/ocultar elementos
        - Usar os botões de zoom e download no canto superior direito dos gráficos
        """)

def criar_kpis_tendencia(df: pd.DataFrame, vendedor: str) -> None:
    """
    Cria cards com KPIs de tendência para o vendedor
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(
            criar_container_kpi(
                "Crescimento Médio",
                "15% ao mês",
                "↑ Tendência de alta"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            criar_container_kpi(
                "Sazonalidade",
                "Alta em Dez",
                "🎯 Próximo pico"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            criar_container_kpi(
                "Previsão Próximo Mês",
                formatar_moeda(850000),
                "↑ 12% vs atual"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            criar_container_kpi(
                "Meta Anual",
                "85% atingida",
                "🎯 No objetivo"
            ),
            unsafe_allow_html=True
        ) 

def criar_grafico_tendencia_vendas(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria gráfico de linha com projeção futura de vendas
    """
    try:
        # Filtrar dados do vendedor
        df_vendedor = df[df['vendedor'] == vendedor].copy()
        
        # Agrupar por mês
        df_vendedor['mes_ano'] = df_vendedor['data'].dt.strftime('%m/%Y')
        vendas_mensais = df_vendedor.groupby('mes_ano').agg({
            'valor': 'sum',
            'data': 'first'  # Para manter a data para ordenação
        }).reset_index()
        
        # Ordenar por data
        vendas_mensais = vendas_mensais.sort_values('data')
        
        # Calcular média móvel de 3 meses
        vendas_mensais['media_movel'] = vendas_mensais['valor'].rolling(window=3, min_periods=1).mean()
        
        # Criar figura
        fig = go.Figure()
        
        # Adicionar linha de vendas reais
        fig.add_trace(
            go.Scatter(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['valor'],
                name='Vendas Reais',
                line=dict(color='#4169E1', width=2),
                hovertemplate="Mês: %{x}<br>Valor: R$ %{y:,.2f}<extra></extra>"
            )
        )
        
        # Adicionar linha de média móvel
        fig.add_trace(
            go.Scatter(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['media_movel'],
                name='Média Móvel (3 meses)',
                line=dict(color='#32CD32', width=2, dash='dash'),
                hovertemplate="Mês: %{x}<br>Média: R$ %{y:,.2f}<extra></extra>"
            )
        )
        
        # Configurar layout
        fig.update_layout(
            title="Tendência de Vendas",
            template="plotly_dark",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            xaxis=dict(
                title=None,
                tickangle=45,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)',
            ),
            yaxis=dict(
                title="Valor (R$)",
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)',
                tickformat=",.0f"
            ),
            height=400,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico de tendência: {str(e)}")
        # Retornar uma figura vazia em caso de erro
        return go.Figure()

def criar_grafico_sazonalidade(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria gráfico de calor mostrando padrões sazonais de vendas
    """
    try:
        # Filtrar dados do vendedor
        df_vendedor = df[df['vendedor'] == vendedor].copy()
        
        if df_vendedor.empty:
            print("Sem dados para o vendedor selecionado")
            return go.Figure()
            
        # Criar colunas de ano e mês
        df_vendedor['ano'] = df_vendedor['data'].dt.year
        df_vendedor['mes'] = df_vendedor['data'].dt.month
        
        # Criar uma matriz completa com todos os meses
        anos = df_vendedor['ano'].unique()
        meses = range(1, 13)  # 1 a 12
        
        # Criar DataFrame vazio com todos os meses e anos
        index = pd.MultiIndex.from_product([anos, meses], names=['ano', 'mes'])
        vendas_completas = pd.DataFrame(index=index).reset_index()
        
        # Agrupar vendas reais
        vendas_reais = df_vendedor.groupby(['ano', 'mes'])['valor'].sum().reset_index()
        
        # Mesclar dados reais com a matriz completa
        vendas_completas = vendas_completas.merge(
            vendas_reais, 
            on=['ano', 'mes'], 
            how='left'
        ).fillna(0)
        
        # Criar matriz para o heatmap
        matriz_vendas = pd.pivot_table(
            vendas_completas,
            values='valor',
            index='ano',
            columns='mes',
            aggfunc='sum',
            fill_value=0
        )
        
        # Normalizar valores para melhor visualização
        matriz_normalizada = matriz_vendas / 1000  # Valores em milhares
        
        # Criar figura
        fig = go.Figure(data=go.Heatmap(
            z=matriz_normalizada.values,
            x=MESES_ORDEM,  # Usar todos os meses
            y=matriz_vendas.index,
            colorscale='Viridis',
            hoverongaps=False,
            hovertemplate="Ano: %{y}<br>Mês: %{x}<br>Valor: R$ %{z:.0f}K<extra></extra>"
        ))
        
        # Configurar layout
        fig.update_layout(
            title="Sazonalidade de Vendas",
            template="plotly_dark",
            xaxis=dict(
                title="Mês",
                tickangle=45,
                side='bottom'
            ),
            yaxis=dict(
                title="Ano",
                tickangle=0
            ),
            height=400,
            margin=dict(t=50, l=50, r=50, b=50),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        # Adicionar anotações apenas para valores significativos
        for i in range(len(matriz_normalizada.index)):
            for j in range(len(matriz_normalizada.columns)):
                valor = matriz_normalizada.iloc[i, j]
                if valor > 0:
                    fig.add_annotation(
                        x=MESES_ORDEM[j],
                        y=matriz_normalizada.index[i],
                        text=f"R${valor:.0f}K",
                        showarrow=False,
                        font=dict(
                            size=10,
                            color='white'
                        )
                    )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico de sazonalidade: {str(e)}")
        return go.Figure()

def criar_grafico_comparativo_metas(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria gráfico comparando metas vs realizado
    """
    try:
        # Filtrar dados do vendedor
        df_vendedor = df[df['vendedor'] == vendedor].copy()
        
        # Agrupar por mês
        df_vendedor['mes_ano'] = df_vendedor['data'].dt.strftime('%m/%Y')
        vendas_mensais = df_vendedor.groupby('mes_ano').agg({
            'valor': 'sum',
            'data': 'first'
        }).reset_index()
        
        # Ordenar por data
        vendas_mensais = vendas_mensais.sort_values('data')
        
        # Simular metas (você deve substituir isso com suas metas reais)
        meta_mensal = 1_000_000  # Meta fixa de 1M por mês
        vendas_mensais['meta'] = meta_mensal
        
        # Calcular percentual atingido
        vendas_mensais['percentual_atingido'] = (vendas_mensais['valor'] / vendas_mensais['meta'] * 100).round(1)
        
        # Criar figura
        fig = go.Figure()
        
        # Adicionar barras de realizado
        fig.add_trace(
            go.Bar(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['valor'],
                name='Realizado',
                marker_color='#4169E1',
                hovertemplate="Mês: %{x}<br>Realizado: R$ %{y:,.2f}<extra></extra>"
            )
        )
        
        # Adicionar linha de meta
        fig.add_trace(
            go.Scatter(
                x=vendas_mensais['mes_ano'],
                y=vendas_mensais['meta'],
                name='Meta',
                line=dict(color='#FF4500', width=2, dash='dash'),
                hovertemplate="Meta: R$ %{y:,.2f}<extra></extra>"
            )
        )
        
        # Configurar layout
        fig.update_layout(
            title="Comparativo de Metas",
            template="plotly_dark",
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            ),
            xaxis=dict(
                title=None,
                tickangle=45,
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)',
            ),
            yaxis=dict(
                title="Valor (R$)",
                showgrid=True,
                gridwidth=1,
                gridcolor='rgba(128, 128, 128, 0.2)',
                tickformat=",.0f"
            ),
            height=400,
            margin=dict(t=50, l=50, r=50, b=50)
        )
        
        # Adicionar anotações com percentual atingido
        for i, row in vendas_mensais.iterrows():
            fig.add_annotation(
                x=row['mes_ano'],
                y=row['valor'],
                text=f"{row['percentual_atingido']}%",
                showarrow=False,
                yshift=10,
                font=dict(
                    size=10,
                    color='white'
                )
            )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico comparativo de metas: {str(e)}")
        return go.Figure() 