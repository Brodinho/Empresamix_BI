import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.constants import (
    GRAPH_CONFIG, 
    MESES_PT, 
    UF_TO_ISO, 
    COORDENADAS_ESTADOS
)
from utils.formatters import (
    NOMES_ESTADOS,
    formatar_moeda
)
from src.analysis.faturamento_analysis import preparar_dados_mapa
import math

def criar_grafico_linha_mensal(df_filtrado):
    """
    Cria o gráfico de linha mensal do faturamento
    """
    try:
        # Preparar dados
        df_filtrado['ano'] = df_filtrado['data'].dt.year
        df_filtrado['mes'] = df_filtrado['data'].dt.month
        df_mensal = df_filtrado.groupby(['ano', 'mes'])['valor'].sum().reset_index()
        
        # Criar figura
        fig = go.Figure()
        
        # Adicionar uma linha para cada ano
        for ano in sorted(df_mensal['ano'].unique()):
            dados_ano = df_mensal[df_mensal['ano'] == ano].sort_values('mes')
            
            fig.add_trace(go.Scatter(
                x=dados_ano['mes'],
                y=dados_ano['valor'],
                mode='lines+markers',
                name=str(ano),
                line=dict(width=2),
                hovertemplate=(
                    f'Ano: {ano}<br>' +
                    'Mês: %{x}<br>' +
                    'Valor: R$ %{y:,.2f}<extra></extra>'
                )
            ))
        
        # Configurar layout
        fig.update_layout(
            title=dict(
                text='Evolução do Faturamento Mensal',
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=20)
            ),
            xaxis=dict(
                title='Mês',
                ticktext=['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
                tickvals=list(range(1, 13)),
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True,
                zeroline=True
            ),
            yaxis=dict(
                title='Valor Faturado',
                tickformat='',
                ticksuffix=' Milhões',
                tickvals=list(range(0, 60000000, 10000000)),
                ticktext=[f'{i//1000000}' for i in range(0, 60000000, 10000000)],
                gridcolor='rgba(128,128,128,0.2)',
                showgrid=True,
                zeroline=True
            ),
            **GRAPH_CONFIG['LAYOUT'],
            showlegend=True,
            legend=dict(
                title='Anos',
                yanchor='top',
                y=0.99,
                xanchor='right',
                x=0.99
            ),
            hovermode='x unified'
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico mensal: {str(e)}")
        return None

def criar_mapa_faturamento(df: pd.DataFrame) -> go.Figure:
    """Cria mapa de bolhas para faturamento por estado/país"""
    try:
        # Preparar dados
        df_fat_estado = preparar_dados_mapa(df)
        
        if df_fat_estado.empty:
            # Retornar figura vazia ou mensagem de erro
            fig = go.Figure()
            fig.add_annotation(
                text="Sem dados disponíveis para o mapa",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return fig
        
        # Criar o mapa usando px.scatter_mapbox
        fig = px.scatter_mapbox(
            df_fat_estado,
            lat='latitude',
            lon='longitude',
            size='bubble_size',
            color='is_pais',
            color_discrete_sequence=['blue', 'red'],
            hover_name='Nome_Local',
            hover_data={
                'bubble_size': False,
                'latitude': False,
                'longitude': False,
                'is_pais': False,
                'Faturamento Total': True
            },
            mapbox_style="open-street-map",
            zoom=2
        )
        
        # Atualizar layout
        fig.update_layout(
            height=600,
            showlegend=True,
            legend=dict(
                title="Localização",
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                itemsizing="constant"
            ),
            mapbox=dict(
                center=dict(lat=-15, lon=-55),  # Centralizar no Brasil
                zoom=3  # Ajustar zoom
            )
        )
        
        # Atualizar legendas
        if len(fig.data) > 1:
            fig.data[0].name = "Estados"
            fig.data[1].name = "Países"
        else:
            fig.data[0].name = "Estados"
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar mapa: {str(e)}")
        return None

def criar_grafico_categorias(df_filtrado):
    """
    Cria o gráfico de barras por categoria
    """
    try:
        # Agrupa dados por categoria
        df_categorias = df_filtrado.groupby('categoria')['valor'].sum().reset_index()
        df_categorias = df_categorias.sort_values('valor', ascending=True)
        
        # Criar figura
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=df_categorias['valor'],
            y=df_categorias['categoria'],
            orientation='h',
            marker_color=GRAPH_CONFIG['COLORS']['bar']
        ))
        
        # Configurar layout
        fig.update_layout(
            title=dict(
                text='Faturamento por Categoria',
                x=0.5,
                y=0.95,
                xanchor='center',
                yanchor='top',
                font=dict(size=20)
            ),
            xaxis_title='Valor Faturado (R$)',
            yaxis_title='Categoria',
            xaxis=dict(tickformat=',.2f'),
            **GRAPH_CONFIG['LAYOUT']
        )
        
        return fig
    except Exception as e:
        print(f"Erro ao criar gráfico de categorias: {str(e)}")
        return None

def criar_grafico_faturamento_estado(df: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de barras horizontais com os top 5 estados/países por faturamento
    """
    try:
        # Separar dados do Brasil e exterior
        df_brasil = df[df['estado'] != 'EX'].copy()
        df_exterior = df[df['estado'] == 'EX'].copy()
        
        # Processar dados do Brasil
        df_brasil_fat = df_brasil.groupby('estado')['valor'].sum().reset_index()
        df_brasil_fat['Nome_Local'] = df_brasil_fat['estado'].map(NOMES_ESTADOS)
        
        # Processar dados do exterior
        if not df_exterior.empty:
            df_exterior_fat = df_exterior.groupby('pais')['valor'].sum().reset_index()
            df_exterior_fat['Nome_Local'] = df_exterior_fat['pais']
            
            # Combinar dados
            df_fat_total = pd.concat([
                df_brasil_fat[['Nome_Local', 'valor']],
                df_exterior_fat[['Nome_Local', 'valor']]
            ])
        else:
            df_fat_total = df_brasil_fat[['Nome_Local', 'valor']]
        
        # Pegar top 5
        top_5 = df_fat_total.nlargest(5, 'valor')
        
        # Criar gráfico
        fig = go.Figure()
        
        # Formatar valores usando formatar_moeda
        valores_formatados = [formatar_moeda(valor) for valor in top_5['valor']]
        
        fig.add_trace(go.Bar(
            x=top_5['valor'],
            y=top_5['Nome_Local'],
            orientation='h',
            text=valores_formatados,
            textposition='auto',
            marker_color='#4169E1',
            hovertemplate="<b>%{y}</b><br>" +
                         "Faturamento: %{text}<br>" +
                         "<extra></extra>"
        ))
        
        # Calcular o valor máximo para definir o range do eixo x
        max_valor = top_5['valor'].max()
        max_milhoes = math.ceil(max_valor / 1_000_000)
        
        # Criar lista de valores para o eixo x
        valores_eixo = list(range(0, max_milhoes + 1, max(1, max_milhoes // 5)))
        
        fig.update_layout(
            title=dict(
                text='Faturamento por Estado',
                font=dict(color="white", size=20),
                y=0.9,  # ajusta a posição vertical do título
                x=0.5,  # centraliza o título
                xanchor='center',
                yanchor='top'
            ),
            xaxis=dict(
                title=None,
                ticktext=[formatar_moeda(x * 1_000_000) for x in valores_eixo],
                tickvals=[x * 1_000_000 for x in valores_eixo],
                tickmode='array'
            ),
            yaxis=dict(
                title='',
                autorange="reversed"  # Inverte a ordem para o maior valor aparecer no topo
            ),
            hovermode='x unified',
            hoverlabel=dict(
                bgcolor="rgba(0,0,0,0.8)",
                font_size=14
            ),
            showlegend=False,
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
        
        return fig
        
    except Exception as e:
        print(f"Erro ao criar gráfico de faturamento por estado: {str(e)}")
        return go.Figure()

# Aqui viriam as outras funções de gráficos específicos do dashboard de faturamento 