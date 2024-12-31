"""
Visualizações específicas para o dashboard de faturamento
"""
import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.utils.formatters import (
    formatar_moeda,
    MESES_PT,
    MESES_ORDEM,
    COORDENADAS_ESTADOS,
    MAPEAMENTO_PAISES,
    COORDENADAS_PAISES,
    NOMES_ESTADOS
)

def criar_mapa_faturamento(df: pd.DataFrame) -> go.Figure:
    """Cria mapa de bolhas para faturamento por estado/país"""
    # Separar dados do Brasil e do exterior
    df_brasil = df[df['uf'] != 'EX'].copy()
    df_exterior = df[df['uf'] == 'EX'].copy()
    
    # Processar dados do Brasil
    df_brasil_fat = df_brasil.groupby('uf')['valorfaturado'].sum().reset_index()
    df_brasil_fat['latitude'] = df_brasil_fat['uf'].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get('latitude'))
    df_brasil_fat['longitude'] = df_brasil_fat['uf'].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get('longitude'))
    df_brasil_fat['is_pais'] = False
    df_brasil_fat['Nome_Local'] = df_brasil_fat['uf'].map(NOMES_ESTADOS)
    
    # Processar dados do exterior
    df_exterior_fat = df_exterior.groupby('pais')['valorfaturado'].sum().reset_index()
    df_exterior_fat['sigla_pais'] = df_exterior_fat['pais'].map(MAPEAMENTO_PAISES)
    df_exterior_fat['latitude'] = df_exterior_fat['sigla_pais'].map(lambda x: COORDENADAS_PAISES.get(x, {}).get('lat'))
    df_exterior_fat['longitude'] = df_exterior_fat['sigla_pais'].map(lambda x: COORDENADAS_PAISES.get(x, {}).get('lon'))
    df_exterior_fat['is_pais'] = True
    df_exterior_fat['Nome_Local'] = df_exterior_fat['pais']
    
    # Combinar dados
    df_fat_estado = pd.concat([
        df_brasil_fat[['Nome_Local', 'valorfaturado', 'latitude', 'longitude', 'is_pais']],
        df_exterior_fat[['Nome_Local', 'valorfaturado', 'latitude', 'longitude', 'is_pais']]
    ])
    
    df_fat_estado = df_fat_estado.dropna(subset=['latitude', 'longitude'])
    
    scaler = MinMaxScaler(feature_range=(5, 50))
    df_fat_estado['bubble_size'] = scaler.fit_transform(df_fat_estado[['valorfaturado']])
    df_fat_estado['Faturamento Total'] = df_fat_estado['valorfaturado'].apply(formatar_moeda)
    
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
        mapbox_style='open-street-map',
        zoom=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            title='Localização',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01,
            itemsizing='constant'
        )
    )
    
    fig.data[0].name = 'Estados'
    fig.data[1].name = 'Países'
    
    return fig

def criar_grafico_linha_mensal(df_evolucao: pd.DataFrame) -> go.Figure:
    """Cria gráfico de linha para evolução mensal do faturamento"""
    # Remover linhas com datas nulas
    df_filtrado = df_evolucao.dropna(subset=['data'])
    
    # Criar DataFrame com as informações necessárias
    df_mensal = df_filtrado.assign(
        Ano=df_filtrado['data'].dt.year,
        Mês=df_filtrado['data'].dt.month_name().map(MESES_PT),
        Num_Mês=df_filtrado['data'].dt.month
    )
    
    # Agrupar os dados usando valorNota
    df_mensal = df_mensal.groupby(['Mês', 'Ano', 'Num_Mês'])['valorNota'].sum().reset_index()
    df_mensal = df_mensal.sort_values(['Ano', 'Num_Mês'])
    
    # Criar gráfico
    fig = px.line(
        df_mensal,
        x='Mês',
        y='valorNota',
        color=df_mensal['Ano'].astype(str),
        markers=True,
        category_orders={'Mês': MESES_ORDEM}
    )
    
    # Atualizar layout
    fig.update_layout(
        showlegend=True,
        height=400,
        xaxis=dict(
            showgrid=True,
            title=None
        ),
        yaxis=dict(
            showgrid=True,
            tickformat='R$ ,.2f',
            title=None
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        legend=dict(
            title='Ano',
            yanchor='top',
            y=0.99,
            xanchor='left',
            x=0.01
        )
    )
    
    return fig

def criar_grafico_grupos(df_grupos: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras para faturamento por grupo"""
    # Criar cópia para não modificar o DataFrame original
    df = df_grupos.copy()
    
    # Agrupar por grupo e somar o faturamento
    df_agrupado = df.groupby('grupo')['valorfaturado'].sum().reset_index()
    
    # Formatar valores
    df_agrupado['valor_formatado'] = df_agrupado['valorfaturado'].apply(formatar_moeda)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_agrupado['grupo'],
        y=df_agrupado['valorfaturado'],
        text=df_agrupado['valor_formatado'],
        textposition='auto',
        hovertemplate='<b>%{x}</b><br>' +
                     'Faturamento: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='Grupo',
        yaxis_title='Faturamento (R$)',
        showlegend=False,
        height=400,
        xaxis=dict(tickangle=45),
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def criar_grafico_categorias(df_categorias: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras para faturamento por categoria"""
    # Criar cópia para não modificar o DataFrame original
    df = df_categorias.copy()
    
    # Agrupar por código e descrição do subgrupo e somar o faturamento
    df_agrupado = df.groupby(['codSubGrupo', 'subGrupo'])['valorfaturado'].sum().reset_index()
    
    # Formatar valores
    df_agrupado['valor_formatado'] = df_agrupado['valorfaturado'].apply(formatar_moeda)
    
    # Criar rótulo combinando código e descrição
    df_agrupado['categoria'] = df_agrupado.apply(
        lambda x: f"{x['codSubGrupo']} - {x['subGrupo']}", axis=1
    )
    
    # Ordenar por valor decrescente e pegar top 5
    df_agrupado = df_agrupado.sort_values('valorfaturado', ascending=True).tail(5)
    
    # Calcular os ticks do eixo X
    max_valor = df_agrupado['valorfaturado'].max()
    step = 10000000  # Step de 10 milhões
    num_dezenas = math.ceil(max_valor / step)
    max_escala = num_dezenas * step
    tick_values = [i * step for i in range(num_dezenas + 1)]
    tick_text = ['0' if x == 0 else f"{int(x/1000000)} Milhões" for x in tick_values]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_agrupado['valorfaturado'],
        y=df_agrupado['categoria'],
        orientation='h',
        text=df_agrupado['valor_formatado'],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>' +
                     'Faturamento: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        showlegend=False,
        height=400,
        xaxis=dict(
            showgrid=True,
            tickmode='array',
            tickvals=tick_values,
            ticktext=tick_text,
            range=[0, max_escala]
        ),
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig

def criar_grafico_estados(df_estados: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras para faturamento por estado/país"""
    # Criar cópia para não modificar o DataFrame original
    df = df_estados.copy()
    
    # Separar dados do Brasil e exterior
    df_brasil = df[df['uf'] != 'EX'].copy()
    df_exterior = df[df['uf'] == 'EX'].copy()
    
    # Agrupar dados do Brasil por UF
    df_brasil_agrupado = df_brasil.groupby('uf')['valorfaturado'].sum().reset_index()
    df_brasil_agrupado['local'] = df_brasil_agrupado['uf'].map(NOMES_ESTADOS)
    
    # Agrupar dados do exterior por país
    df_exterior_agrupado = df_exterior.groupby('pais')['valorfaturado'].sum().reset_index()
    df_exterior_agrupado['local'] = df_exterior_agrupado['pais']
    
    # Combinar os resultados
    df_agrupado = pd.concat([
        df_brasil_agrupado[['local', 'valorfaturado']],
        df_exterior_agrupado[['local', 'valorfaturado']]
    ])
    
    # Formatar valores
    df_agrupado['valor_formatado'] = df_agrupado['valorfaturado'].apply(formatar_moeda)
    
    # Ordenar por valor decrescente e pegar top 5
    df_agrupado = df_agrupado.sort_values('valorfaturado', ascending=True).tail(5)
    
    # Calcular os ticks do eixo X
    max_valor = df_agrupado['valorfaturado'].max()
    step = 10000000  # Step de 10 milhões
    num_dezenas = math.ceil(max_valor / step)
    max_escala = num_dezenas * step
    tick_values = [i * step for i in range(num_dezenas + 1)]
    tick_text = [f"{int(x/1000000)} Milhões" for x in tick_values]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_agrupado['valorfaturado'],
        y=df_agrupado['local'],
        orientation='h',
        text=df_agrupado['valor_formatado'],
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>' +
                     'Faturamento: %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        xaxis_title='',
        yaxis_title='',
        showlegend=False,
        height=400,
        xaxis=dict(
            showgrid=True,
            tickmode='array',
            tickvals=tick_values,
            ticktext=tick_text,
            range=[0, max_escala]
        ),
        yaxis=dict(showgrid=True),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    return fig
