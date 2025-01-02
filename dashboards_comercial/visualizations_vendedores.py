import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.formatters import formatar_moeda
import math
from plotly.subplots import make_subplots
from typing import Dict, Any

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
    Cria um gráfico de linha mostrando a evolução das vendas do vendedor
    """
    try:
        # Agrupar dados por mês
        df_vendedor = df[df['vendedor'] == vendedor].copy()
        df_vendedor['mes_ano'] = df_vendedor['data'].dt.strftime('%Y-%m')
        dados_mensais = df_vendedor.groupby('mes_ano').agg({
            'valor': 'sum',
            'data': 'count'
        }).reset_index()
        
        # Criar figura com dois eixos Y
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Adicionar linha de faturamento
        fig.add_trace(
            go.Scatter(
                x=dados_mensais['mes_ano'],
                y=dados_mensais['valor'],
                name="Faturamento",
                line=dict(color="#4169E1", width=3),
                hovertemplate="Faturamento: %{y:,.2f}<br>Mês: %{x}<extra></extra>"
            ),
            secondary_y=False
        )
        
        # Adicionar linha de quantidade de vendas
        fig.add_trace(
            go.Scatter(
                x=dados_mensais['mes_ano'],
                y=dados_mensais['data'],
                name="Qtd. Vendas",
                line=dict(color="#32CD32", width=3, dash='dot'),
                hovertemplate="Vendas: %{y}<br>Mês: %{x}<extra></extra>"
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title=f"Evolução de Vendas - {vendedor}",
            template="plotly_dark",
            height=400,
            hovermode="x unified"
        )
        
        return fig
    except Exception as e:
        print(f"Erro ao criar gráfico de evolução: {str(e)}")
        return go.Figure()

def criar_grafico_categorias(df: pd.DataFrame, vendedor: str) -> go.Figure:
    """
    Cria um gráfico de rosca mostrando a distribuição de vendas por categoria
    """
    try:
        df_vendedor = df[df['vendedor'] == vendedor]
        dados_categoria = df_vendedor.groupby('categoria').agg({
            'valor': 'sum',
            'id_venda': 'count'
        }).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=dados_categoria['categoria'],
            values=dados_categoria['valor'],
            hole=0.6,
            textinfo='label+percent',
            hovertemplate="Categoria: %{label}<br>" +
                         "Valor: " + formatar_moeda("%{value:,.2f}") + "<br>" +
                         "Percentual: %{percent}<extra></extra>"
        ))
        
        fig.update_layout(
            title="Distribuição por Categoria",
            template="plotly_dark",
            height=400
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