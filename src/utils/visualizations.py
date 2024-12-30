import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from utils.formatters import (
    formatar_moeda,
    MESES_PT,
    MESES_ORDEM,
    COORDENADAS_ESTADOS,
    SIGLAS_ESTADOS,
    MAPEAMENTO_PAISES,
    COORDENADAS_PAISES,
    NOMES_ESTADOS
)
import streamlit as st
import json
from pathlib import Path
import folium
from folium import plugins
from branca.colormap import LinearColormap

def criar_grafico_vendedores(df):
    """
    Cria um gráfico de barras horizontais com os top 5 vendedores por faturamento
    """
    # Agrupar dados por vendedor
    vendedores = df.groupby(['codVendedor', 'vendedor']).agg({
        'valorNota': 'sum',
        'nota': 'count'
    }).reset_index()
    
    # Renomear colunas
    vendedores.columns = ['Código', 'Nome', 'Faturamento', 'Total_Vendas']
    
    # Ordenar e pegar top 5
    top_vendedores = vendedores.nlargest(5, 'Faturamento')
    
    # Calcular o valor máximo para definir o range do eixo x
    max_valor = top_vendedores['Faturamento'].max()
    max_milhoes = math.ceil(max_valor / 1_000_000 / 5) * 5  # Arredonda para cima em intervalos de 5 milhões
    
    # Criar gráfico horizontal
    fig = go.Figure()
    
    # Formatar valores usando formatar_moeda do formatters.py
    valores_formatados = [formatar_moeda(valor) for valor in top_vendedores['Faturamento']]
    
    fig.add_trace(go.Bar(
        x=top_vendedores['Faturamento'],
        y=top_vendedores['Nome'],
        orientation='h',
        text=[f"{valor}<br>{vendas} vendas" 
              for valor, vendas in zip(valores_formatados, 
                                     top_vendedores['Total_Vendas'])],
        textposition='auto',
        marker_color='#4169E1',
        hovertemplate="<b>%{y}</b><br>" +
                     "Faturamento: %{text}<br>" +
                     "<extra></extra>"
    ))
    
    # Criar lista de valores para o eixo x em milhões
    valores_eixo = list(range(0, max_milhoes + 1, 5))
    
    fig.update_layout(
        title='Top 5 Vendedores por Faturamento',
        xaxis=dict(
            title=None,  # Remove o título do eixo x
            ticktext=[f"{x} milhões" if x > 0 else "0" for x in valores_eixo],
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
    # Usar NOMES_ESTADOS para garantir nomes por extenso
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
    
    # Remover registros sem coordenadas
    df_fat_estado = df_fat_estado.dropna(subset=['latitude', 'longitude'])
    
    # Normalizar tamanho das bolhas
    scaler = MinMaxScaler(feature_range=(5, 50))
    df_fat_estado['bubble_size'] = scaler.fit_transform(df_fat_estado[['valorfaturado']])
    
    # Formatar valores para o hover
    df_fat_estado['Faturamento Total'] = df_fat_estado['valorfaturado'].apply(formatar_moeda)
    
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
        )
    )
    
    # Atualizar legendas
    fig.data[0].name = "Estados"
    fig.data[1].name = "Países"
    
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
    
    # Configurar eixo Y
    max_valor = df_mensal['valorNota'].max()
    step = 1000000  # Step de 1 milhão
    num_milhoes = math.ceil(max_valor / step)
    max_escala = num_milhoes * step
    tick_values = [i * step for i in range(num_milhoes + 1)]
    
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        legend=dict(
            title="Ano",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Formatar hover
    for i in range(len(fig.data)):
        ano = fig.data[i].name
        valores = df_mensal[df_mensal['Ano'].astype(str) == ano]['valorNota']
        valores_formatados = [formatar_moeda(valor) for valor in valores]
        fig.data[i].customdata = list(zip([ano] * len(valores), valores_formatados))
        fig.data[i].hovertemplate = (
            "<b>%{x}</b><br>" +
            "Ano: %{customdata[0]}<br>" +
            "Faturamento: %{customdata[1]}" +
            "<extra></extra>"
        )
    
    return fig

def criar_grafico_grupos(df_grupos: pd.DataFrame) -> go.Figure:
    """Cria gráfico de barras para faturamento por grupo"""
    # Criar cópia para não modificar o DataFrame original
    df = df_grupos.copy()
    
    # Formatar valores
    df['valor_formatado'] = df['valorfaturado'].apply(formatar_moeda)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['grupo'],
        y=df['valorfaturado'],
        text=df['valor_formatado'],
        textposition='auto',
        hovertemplate="<b>%{x}</b><br>" +
                     "Faturamento: %{text}<extra></extra>"
    ))
    
    fig.update_layout(
        xaxis_title="Grupo",
        yaxis_title="Faturamento (R$)",
        showlegend=False,
        height=400,
        xaxis=dict(tickangle=45),
        yaxis=dict(showgrid=True),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
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
        hovertemplate="<b>%{y}</b><br>" +
                     "Faturamento: %{text}<extra></extra>"
    ))
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
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
    # Usar NOMES_ESTADOS para obter o nome por extenso
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
        hovertemplate="<b>%{y}</b><br>" +
                     "Faturamento: %{text}<extra></extra>"
    ))
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    
    return fig

def criar_grafico_budget(dados_atual, meta_mensal, meta_total, ano_atual):
    """Cria o gráfico de análise de budget vs realizado"""
    from utils.formatters import formatar_moeda
    
    # Preparar dados
    meses = pd.date_range(start=f'{ano_atual}-01-01', periods=12, freq='M')
    mes_ultimo_realizado = int(max(dados_atual.index)) if not dados_atual.empty else 0
    
    # Criar figura
    fig = go.Figure()
    
    # Linha da Meta
    fig.add_trace(go.Scatter(
        x=meses.strftime('%b').str.lower(),
        y=[meta_mensal] * 12,
        name='Meta',
        line=dict(color='gray', width=1),
        hoverinfo='skip'
    ))
    
    # Preparar dados do realizado
    valores_realizados = [dados_atual.get(m.strftime('%m'), 0) for m in meses[:mes_ultimo_realizado]]
    realizado_acumulado = [sum(valores_realizados[:i+1]) for i in range(len(valores_realizados))]
    
    # Preparar dados do hover
    hover_data = []
    for i, m in enumerate(meses[:mes_ultimo_realizado]):
        mes_nome = formatters.MESES_PT.get(m.strftime('%B').lower(), m.strftime('%B'))
        valor_realizado = valores_realizados[i]
        valor_acumulado = realizado_acumulado[i]
        valor_forecast = meta_total - valor_acumulado
        
        hover_text = (
            f'Mês: {mes_nome}<br>' +
            f'Realizado no mês: {formatters.formatar_moeda(valor_realizado)}<br>' +
            f'Budget: {formatters.formatar_moeda(meta_total)}<br>' +
            f'Forecast: {formatters.formatar_moeda(valor_forecast)}'
        )
        hover_data.append(hover_text)
    
    # Linha do Realizado
    fig.add_trace(go.Scatter(
        x=meses[:mes_ultimo_realizado].strftime('%b').str.lower(),
        y=valores_realizados,
        name='Realizado',
        line=dict(color='blue', width=2),
        text=hover_data,
        hovertemplate='%{text}<extra></extra>',
        hoverinfo='text'
    ))
    
    # Configurar layout
    fig.update_layout(
        title=f'Análise de Meta vs Realizado {ano_atual}',
        xaxis_title=None,
        yaxis=dict(
            tickformat=",.2f",
            tickprefix="R$ ",
            separatethousands=True,
            title=None
        ),
        legend_title=None,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        font=dict(color="white")
    )
    
    # Adicionar anotação sobre o forecast em dezembro
    if mes_ultimo_realizado < 12:
        fig.add_annotation(
            x=meses[-1].strftime('%b').lower(),
            y=meta_mensal,
            text=f'Necessário em Dezembro: {formatters.formatar_moeda(meta_total - sum(valores_realizados))}',
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            font=dict(color="white")
        )
    
    return fig

def plot_related_queries(queries):
    """Plota as consultas relacionadas"""
    if not isinstance(queries, dict):
        st.info("Formato de dados inválido para consultas relacionadas.")
        return
    
    has_data = False
    
    # Verificar e exibir consultas mais populares
    if isinstance(queries.get('top'), pd.DataFrame) and not queries['top'].empty:
        has_data = True
        st.subheader("Consultas mais populares")
        st.dataframe(
            queries['top'].style.background_gradient(cmap='Blues'),
            use_container_width=True
        )
    
    # Verificar e exibir consultas em ascensão
    if isinstance(queries.get('rising'), pd.DataFrame) and not queries['rising'].empty:
        has_data = True
        st.subheader("Consultas em ascensão")
        st.dataframe(
            queries['rising'].style.background_gradient(cmap='Greens'),
            use_container_width=True
        )
    
    if not has_data:
        st.info("Não há consultas relacionadas disponíveis para este termo.")

def plot_related_topics(topics):
    """Plota os tópicos relacionados"""
    if not isinstance(topics, dict):
        st.info("Formato de dados inválido para tópicos relacionados.")
        return
    
    has_data = False
    
    # Verificar e exibir tópicos mais populares
    if isinstance(topics.get('top'), pd.DataFrame) and not topics['top'].empty:
        has_data = True
        st.subheader("Tópicos mais populares")
        st.dataframe(
            topics['top'].style.background_gradient(cmap='Blues'),
            use_container_width=True
        )
    
    # Verificar e exibir tópicos em ascensão
    if isinstance(topics.get('rising'), pd.DataFrame) and not topics['rising'].empty:
        has_data = True
        st.subheader("Tópicos em ascensão")
        st.dataframe(
            topics['rising'].style.background_gradient(cmap='Greens'),
            use_container_width=True
        )
    
    if not has_data:
        st.info("Não há tópicos relacionados disponíveis para este termo.")

def plot_trends_data(df):
    """Plota o gráfico de tendências temporais"""
    if df is None or df.empty:
        st.info("Não há dados temporais disponíveis.")
        return
    
    try:
        # Converter índice para datetime se necessário
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        
        # Criar gráfico de linha
        fig = go.Figure()
        
        # Adicionar linha de tendência
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[df.columns[0]],
            mode='lines+markers',
            name='Interesse',
            line=dict(color='#1f77b4')
        ))
        
        # Configurar layout
        fig.update_layout(
            title="Interesse ao longo do tempo",
            xaxis_title="Data",
            yaxis_title="Interesse relativo",
            showlegend=True,
            height=400,
            hovermode='x unified'
        )
        
        # Exibir gráfico
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception:
        st.info("Não foi possível criar o gráfico de tendências temporais.")

def plot_regional_data(df, termo):
    """Plota o gráfico de interesse por região"""
    if df is None or df.empty:
        st.info("Não há dados regionais disponíveis.")
        return
    
    try:
        # Criar DataFrame com os dados formatados
        df_map = df.reset_index()
        df_map.columns = ['estado', 'interesse']
        
        # Mapear estados para suas siglas
        estado_to_sigla = {v: k for k, v in formatters.NOMES_ESTADOS.items()}
        df_map['sigla'] = df_map['estado'].map(estado_to_sigla)
        
        # Criar mapa centralizado no Brasil
        m = folium.Map(
            location=[-15.7801, -47.9292],
            zoom_start=4,
            tiles='cartodbpositron',
            control_scale=True
        )
        
        # Adicionar controle de tela cheia
        plugins.Fullscreen(
            position='topleft',
            title='Tela cheia',
            title_cancel='Sair da tela cheia',
            force_separate_button=True
        ).add_to(m)
        
        # Criar escala de cores
        colormap = LinearColormap(
            colors=['#f7fbff', '#08519c'],
            vmin=0,
            vmax=100,
            caption='Interesse (%)'
        )
        
        # Carregar o GeoJSON do Brasil
        geojson_path = Path(__file__).parent / 'brazil-states.json'
        with open(geojson_path, 'r', encoding='utf-8') as f:
            brazil_states = json.load(f)
            
        # Adicionar camada do GeoJSON com tooltip melhorado
        folium.GeoJson(
            brazil_states,
            style_function=lambda feature: {
                'fillColor': colormap(
                    df_map[df_map['sigla'] == feature['properties']['sigla']]['interesse'].values[0]
                    if feature['properties']['sigla'] in df_map['sigla'].values else 0
                ),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            },
            tooltip=folium.GeoJsonTooltip(
                fields=['name'],
                aliases=[''],
                style=('background-color: white; color: black; font-family: courier new; font-size: 12px; padding: 10px;'),
                sticky=True  # Mantém o tooltip visível
            )
        ).add_to(m)
        
        # Adicionar círculos preenchidos nas capitais
        for idx, row in df_map.iterrows():
            coords = formatters.COORDENADAS_ESTADOS.get(row['sigla'], {})
            if coords:
                # Calcular o tamanho do círculo baseado no interesse (min 5, max 15)
                radius = 5 + (row['interesse'] / 100 * 10)
                
                folium.CircleMarker(
                    location=[coords['latitude'], coords['longitude']],
                    radius=radius,  # Tamanho variável baseado no interesse
                    color='white',  # Borda branca
                    weight=1,
                    fill=True,
                    fill_color='#1f77b4',  # Cor azul similar ao gráfico de barras
                    fill_opacity=0.7,
                    popup=None,
                    tooltip=f"{row['estado']}: {row['interesse']:.0f}%"
                ).add_to(m)
        
        # Adicionar legenda
        colormap.add_to(m)
        
        # Criar gráfico de barras
        fig_bars = go.Figure()
        fig_bars.add_trace(go.Bar(
            x=df_map['interesse'],
            y=df_map['estado'],
            orientation='h',
            marker_color='#1f77b4',
            text=df_map['interesse'].apply(lambda x: f'{x:.0f}%'),
            textposition='auto',
        ))
        
        fig_bars.update_layout(
            title="Interesse relativo por região",
            height=600,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=False,
            xaxis_title="Interesse (%)",
            yaxis_title="Estado"
        )
        
        # Criar duas colunas para os gráficos
        col1, col2 = st.columns(2)
        
        # Exibir gráficos nas colunas
        with col1:
            st.write(f"Distribuição geográfica do interesse: {termo}")
            folium_html = folium.Figure().add_child(m)._repr_html_()
            st.components.v1.html(folium_html, height=600)
        
        with col2:
            st.plotly_chart(fig_bars, use_container_width=True)
        
        # Exibir dados em formato de tabela
        st.subheader("Dados detalhados por região")
        st.dataframe(
            df_map[['estado', 'interesse']].style.background_gradient(cmap='Blues', subset=['interesse']),
            use_container_width=True
        )
        
    except Exception as e:
        st.info(f"Não foi possível criar os gráficos de interesse por região: {str(e)}")

def criar_grafico_recencia(df_recencia):
    fig = go.Figure(data=[
        go.Pie(
            labels=df_recencia.index,
            values=df_recencia.values,
            hole=.3,
            marker=dict(
                colors=['#00FF00', '#FFA500', '#FF4500', '#FF0000']
            )
        )
    ])
    
    fig.update_layout(
        title='Distribuição de Recência dos Clientes',
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    total = df_recencia.sum()
    for i, value in enumerate(df_recencia.values):
        percentage = (value / total) * 100
        fig.add_annotation(
            text=f'{percentage:.1f}%',
            x=df_recencia.index[i],
            y=value,
            showarrow=False,
            font=dict(size=12, color='white')
        )
    
    return fig

def criar_grafico_conversao(df_conversao):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_conversao['data'],
        y=df_conversao['inativos'],
        name='Clientes Inativos',
        marker_color='#FF4B4B',
        yaxis='y2'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_conversao['data'],
        y=df_conversao['taxa_conversao'],
        name='Taxa de Conversão',
        line=dict(color='#00FF00', width=2),
        yaxis='y'
    ))
    
    fig.update_layout(
        title='Taxa de Conversão de Clientes Inativos',
        yaxis=dict(
            title='Taxa de Conversão (%)',
            titlefont=dict(color='#00FF00'),
            tickfont=dict(color='#00FF00')
        ),
        yaxis2=dict(
            title='Número de Inativos',
            titlefont=dict(color='#FF4B4B'),
            tickfont=dict(color='#FF4B4B'),
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def criar_grafico_valor_cliente(valor_clientes, ordem_faixas):
    # Criar Series com a ordem correta
    dist_valor = pd.Series(
        index=ordem_faixas,
        data=[len(valor_clientes[valor_clientes['faixa_valor'] == faixa]) for faixa in ordem_faixas]
    )

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dist_valor.index,
        y=dist_valor.values,
        text=dist_valor.values,
        textposition='auto',
        marker_color='#32CD32',
        hovertemplate='Quantidade de Clientes: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title='Distribuição de Clientes por Faixa de Valor (LTV)',
        xaxis_title='Faixa de Valor',
        yaxis_title='Número de Clientes',
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

def criar_grafico_dispersao_clientes(valor_clientes):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=valor_clientes['Num_Compras'],
        y=valor_clientes['LTV'],
        mode='markers',
        marker=dict(
            size=8,
            color=valor_clientes['Ticket_Medio'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Ticket Médio')
        ),
        hovertemplate="""
        Número de Compras: %{x}<br>
        LTV: R$ %{y:,.2f}<br>
        Ticket Médio: R$ %{marker.color:,.2f}
        <extra></extra>"""
    ))

    fig.update_layout(
        title='Relação entre Frequência de Compras e Valor Total (LTV)',
        xaxis_title='Número de Compras',
        yaxis_title='Valor Total (R$)',
        hovermode='closest',
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    
    return fig

def criar_grafico_dia_semana(dia_semana_stats):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dia_semana_stats.index,
        y=dia_semana_stats['nota'],
        name='Número de Pedidos',
        marker_color='#4169E1',
        yaxis='y'
    ))

    fig.add_trace(go.Scatter(
        x=dia_semana_stats.index,
        y=dia_semana_stats['valorNota'],
        name='Ticket Médio',
        line=dict(color='#32CD32', width=2),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Atividade por Dia da Semana',
        yaxis=dict(
            title='Número de Pedidos',
            titlefont=dict(color='#4169E1'),
            tickfont=dict(color='#4169E1')
        ),
        yaxis2=dict(
            title='Ticket Médio (R$)',
            titlefont=dict(color='#32CD32'),
            tickfont=dict(color='#32CD32'),
            overlaying='y',
            side='right',
            tickformat='R$ ,.2f'
        ),
        hovermode='x unified',
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def criar_grafico_sazonalidade_mensal(mes_stats):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=mes_stats.index,
        y=mes_stats['razao'],
        name='Número de Clientes',
        marker_color='#4169E1'
    ))

    fig.add_trace(go.Scatter(
        x=mes_stats.index,
        y=mes_stats['valorNota'],
        name='Valor Total',
        line=dict(color='#32CD32', width=2),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Sazonalidade Mensal',
        yaxis=dict(
            title='Número de Clientes',
            titlefont=dict(color='#4169E1'),
            tickfont=dict(color='#4169E1')
        ),
        yaxis2=dict(
            title='Valor Total (R$)',
            titlefont=dict(color='#32CD32'),
            tickfont=dict(color='#32CD32'),
            overlaying='y',
            side='right',
            tickformat='R$ ,.2f'
        ),
        hovermode='x unified',
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig
