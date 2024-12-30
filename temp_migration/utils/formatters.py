import locale
import pandas as pd
import math
import plotly.express as px
from datetime import datetime

def setup_locale():
    """Configura o locale para formato brasileiro"""
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
        except locale.Error:
            return False
    return True

def formatar_moeda(valor):
    """Formata um valor numérico para o formato de moeda brasileira"""
    if pd.isna(valor):
        return "R$ 0,00"
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def formatar_data_abrev(data_str):
    """
    Formata uma data no formato YYYY-MM para MMM/YYYY
    Exemplo: 2024-01 -> Jan/2024
    """
    try:
        # Converte a string para datetime
        data = datetime.strptime(data_str, '%Y-%m')
        
        # Dicionário de meses em português
        meses = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr',
            5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago',
            9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        
        # Retorna a data formatada
        return f"{meses[data.month]}/{data.year}"
    except:
        return data_str  # Retorna a string original em caso de erro

# Mapeamentos geográficos
COORDENADAS_ESTADOS = {
    'AC': {'latitude': -8.77, 'longitude': -70.55},
    'AL': {'latitude': -9.71, 'longitude': -35.73},
    'AM': {'latitude': -3.07, 'longitude': -61.66},
    'AP': {'latitude': 0.93, 'longitude': -51.22},
    'BA': {'latitude': -12.96, 'longitude': -38.51},
    'CE': {'latitude': -3.73, 'longitude': -38.54},
    'DF': {'latitude': -15.78, 'longitude': -47.93},
    'ES': {'latitude': -19.19, 'longitude': -40.34},
    'GO': {'latitude': -15.98, 'longitude': -49.86},
    'MA': {'latitude': -2.62, 'longitude': -44.28},
    'MG': {'latitude': -18.51, 'longitude': -44.59},
    'MS': {'latitude': -15.56, 'longitude': -56.09},
    'MT': {'latitude': -12.64, 'longitude': -55.42},
    'PA': {'latitude': -3.79, 'longitude': -52.48},
    'PB': {'latitude': -7.11, 'longitude': -35.95},
    'PE': {'latitude': -8.28, 'longitude': -37.67},
    'PI': {'latitude': -8.28, 'longitude': -37.67},
    'PR': {'latitude': -25.42, 'longitude': -49.27},
    'RJ': {'latitude': -22.91, 'longitude': -43.21},
    'RN': {'latitude': -5.22, 'longitude': -36.52},
    'RO': {'latitude': -10.83, 'longitude': -63.95},
    'RR': {'latitude': 1.82, 'longitude': -61.66},
    'RS': {'latitude': -30.01, 'longitude': -51.23},
    'SC': {'latitude': -27.63, 'longitude': -48.67},
    'SE': {'latitude': -10.97, 'longitude': -37.45},
    'SP': {'latitude': -23.55, 'longitude': -46.64},
    'TO': {'latitude': -10.25, 'longitude': -48.26},
}

SIGLAS_ESTADOS = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MG': 'Minas Gerais',
    'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso',
    'PA': 'Pará',
    'PB': 'Paraíba',
}

MAPEAMENTO_PAISES = {
    'ARGENTINA': 'ARG',
    'BELIZE': 'BLZ',
    'BRAZIL': 'BRA',
    'CHILE': 'CHL',
    'COLOMBIA': 'COL',
    'ECUADOR': 'ECU',
    'GUATEMALA': 'GTM',
    'HONDURAS': 'HND',
    'MEXICO': 'MEX',
    'PANAMA': 'PAN',
    'PERU': 'PER',
    'URUGUAY': 'URY',
    'VENEZUELA': 'VEN',
}

COORDENADAS_PAISES = {
    'ARG': {'lat': -38.4161, 'lon': -63.6167},
    'BLZ': {'lat': 17.1899, 'lon': -88.4976},
    'BRA': {'lat': -14.2350, 'lon': -51.9253},
    'CHL': {'lat': -35.6751, 'lon': -71.5430},
    'COL': {'lat': 4.5709, 'lon': -74.2973},
    'ECU': {'lat': -1.8312, 'lon': -78.1834},
    'GTM': {'lat': 15.7835, 'lon': -90.2308},
    'HND': {'lat': 15.1999, 'lon': -86.2419},
    'MEX': {'lat': 23.6345, 'lon': -102.5528},
    'PAN': {'lat': 9.5767, 'lon': -80.7829},
    'PER': {'lat': -9.1899, 'lon': -75.0152},
    'URY': {'lat': -32.5228, 'lon': -55.7658},
    'VEN': {'lat': 6.4238, 'lon': -66.5897},
}

# Mapeamento de meses para português
MESES_PT = {
    'January': 'Janeiro',
    'February': 'Fevereiro',
    'March': 'Março',
    'April': 'Abril',
    'May': 'Maio',
    'June': 'Junho',
    'July': 'Julho',
    'August': 'Agosto',
    'September': 'Setembro',
    'October': 'Outubro',
    'November': 'Novembro',
    'December': 'Dezembro'
}

# Lista de meses em ordem
MESES_ORDEM = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

NOMES_ESTADOS = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

# Mapeamento de colunas do dataset
MAPEAMENTO_COLUNAS_DATASET = {
    'data': 'Data',
    'sequencial': 'Sequencial',
    'os': 'Ordem de Serviço',
    'nota': 'Nota Fiscal',
    'emissao': 'Data Emissão',
    'codGrupo': 'Código Grupo',
    'grupo': 'Grupo',
    'codVendedor': 'Código Vendedor',
    'vendedor': 'Vendedor',
    'codcli': 'Código Cliente',
    'cliente': 'Cliente',
    'estado': 'Estado',
    'valorfaturado': 'Valor Faturado',
    'valoripi': 'Valor IPI',
    'valoricms': 'Valor ICMS',
    'valoriss': 'Valor ISS',
    'valorSubs': 'Valor Substituição',
    'valorFrete': 'Valor Frete',
    'valorNota': 'Valor Nota',
    'valorContabil': 'Valor Contábil',
    'valorCusto': 'Valor Custo',
    'valorDesconto': 'Valor Desconto',
    'categoria': 'Categoria'
}

# Lista de colunas que devem ser formatadas como inteiros
COLUNAS_INTEIRAS = ['sequencial', 'os', 'codGrupo', 'codVendedor', 'codcli', 'nota']

# Lista de colunas que devem ser formatadas como data
COLUNAS_DATA = ['data', 'emissao']

# Lista de colunas que devem ser formatadas como moeda
COLUNAS_MOEDA = [
    'valorfaturado', 'valoripi', 'valoricms', 'valoriss', 
    'valorSubs', 'valorFrete', 'valorNota', 'valorContabil',
    'valorCusto', 'valorDesconto'
]

def formatar_coluna_dataset(valor, tipo_coluna):
    """Formata o valor de uma coluna do dataset de acordo com seu tipo"""
    if pd.isna(valor):
        return ""
    
    if tipo_coluna == 'inteiro':
        return str(int(float(valor))) if pd.notnull(valor) else ""
    
    elif tipo_coluna == 'data':
        return pd.to_datetime(valor).strftime('%d-%m-%Y')
    
    elif tipo_coluna == 'moeda':
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    return str(valor)

def calcular_metricas_vendedores(df_vendedores):
    """Calcula métricas por vendedor"""
    metricas = df_vendedores.groupby('vendedor').agg({
        'valorfaturado': 'sum',
        'os': 'count'
    }).reset_index()
    
    metricas['ticket_medio'] = metricas['valorfaturado'] / metricas['os']
    
    # Formatação dos valores
    metricas['valorfaturado_fmt'] = metricas['valorfaturado'].apply(formatar_moeda)
    metricas['ticket_medio_fmt'] = metricas['ticket_medio'].apply(formatar_moeda)
    
    return metricas

def criar_dataframe_exibicao_vendedores(metricas):
    """Cria DataFrame formatado para exibição"""
    df_exibir = pd.DataFrame({
        'Vendedor': metricas['vendedor'],
        'Total Faturado': metricas['valorfaturado_fmt'],
        'Quantidade de Pedidos': metricas['os'],
        'Ticket Médio': metricas['ticket_medio_fmt']
    })
    return df_exibir.sort_values('Quantidade de Pedidos', ascending=False)

def configurar_grafico_barras_vendedores(df_graph):
    """Configura o gráfico de barras dos vendedores"""
    fig = px.bar(
        df_graph,
        y='vendedor',
        x='valor',
        title='Análise Gráfica',
        orientation='h'
    )
    
    max_valor = df_graph['valor'].max()
    step = 3000000  # Step de 3 milhões
    num_steps = math.ceil(max_valor / step)
    max_escala = num_steps * step
    tick_values = [i * step for i in range(num_steps + 1)]
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(
            tickmode="array",
            tickvals=tick_values,
            ticktext=[formatar_moeda(val) for val in tick_values],
            range=[0, max_escala],
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)'
        )
    )
    
    fig.update_traces(
        text=[formatar_moeda(val) for val in df_graph['valor']],
        textposition='outside',
        texttemplate='%{text}',
        textangle=0
    )
    
    return fig

def configurar_grafico_linha_vendedores(evolucao_mensal):
    """Configura o gráfico de linha da evolução mensal"""
    fig = px.line(
        evolucao_mensal,
        x='mes_abrev',
        y='valorfaturado',
        title='Evolução Mensal do Faturamento'
    )
    
    max_valor = evolucao_mensal['valorfaturado'].max()
    
    if max_valor <= 500_000:
        intervalo = 50_000
    elif max_valor <= 1_000_000:
        intervalo = 100_000
    else:
        intervalo = 200_000
    
    y_ticks = list(range(0, int(max_valor * 1.1), intervalo))
    
    fig.update_layout(
        xaxis_title=None,
        yaxis_title=None,
        yaxis=dict(
            tickmode='array',
            ticktext=[formatar_moeda(val) for val in y_ticks],
            tickvals=y_ticks,
            range=[0, max_valor * 1.1],
            tickfont=dict(size=10)
        )
    )
    
    return fig

def calcular_metricas_clientes(df_clientes):
    """Calcula métricas por cliente"""
    metricas = df_clientes.groupby('razao').agg({
        'valorfaturado': 'sum',
        'os': 'count'
    }).reset_index()
    
    metricas['ticket_medio'] = metricas['valorfaturado'] / metricas['os']
    
    # Formatação dos valores
    metricas['valorfaturado_fmt'] = metricas['valorfaturado'].apply(formatar_moeda)
    metricas['ticket_medio_fmt'] = metricas['ticket_medio'].apply(formatar_moeda)
    
    return metricas

def criar_dataframe_exibicao_clientes(metricas):
    """Cria DataFrame formatado para exibição de clientes"""
    df_exibir = pd.DataFrame({
        'Cliente': metricas['razao'],
        'Total Faturado': metricas['valorfaturado_fmt'],
        'Quantidade de Pedidos': metricas['os'],
        'Ticket Médio': metricas['ticket_medio_fmt']
    })
    return df_exibir.sort_values('Quantidade de Pedidos', ascending=False)

def configurar_grafico_barras_clientes(df_graph):
    """Configura o gráfico de barras para análise de clientes"""
    fig = px.bar(
        df_graph,
        y='cliente',
        x='valor',
        orientation='h',
        title='Top 5 Clientes'
    )
    
    # Configurar formato brasileiro para os valores
    max_valor = df_graph['valor'].max()
    step = 3000000  # Step de 3 milhões
    num_steps = math.ceil(max_valor / step)
    max_escala = num_steps * step
    tick_values = [i * step for i in range(num_steps + 1)]
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(
            tickmode="array",
            tickvals=tick_values,
            ticktext=[formatar_moeda(val) for val in tick_values],
            range=[0, max_escala],
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)'
        )
    )
    
    fig.update_traces(
        text=[formatar_moeda(val) for val in df_graph['valor']],
        textposition='outside',
        texttemplate='%{text}',
        textangle=0
    )
    
    return fig

def configurar_grafico_linha_clientes(df_evolucao):
    """Configura o gráfico de linha para evolução mensal"""
    fig = px.line(
        df_evolucao,
        x='mes_abrev',
        y='valorfaturado',
        title='Evolução Mensal do Faturamento'
    )
    
    # Calcular valores para o eixo Y em milhões
    max_valor = df_evolucao['valorfaturado'].max()
    step = 1_000_000  # 1 milhão
    num_steps = math.ceil(max_valor / step)
    max_escala = num_steps * step
    tick_values = [i * step for i in range(num_steps + 1)]
    
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis=dict(
            tickmode='array',
            tickvals=tick_values,
            ticktext=[formatar_moeda(val) for val in tick_values],
            gridcolor='rgba(128, 128, 128, 0.2)',
            showgrid=True
        ),
        xaxis=dict(
            tickangle=45,
            gridcolor='rgba(128, 128, 128, 0.2)',
            showgrid=True
        )
    )
    
    # Configurar o hover
    fig.update_traces(
        hovertemplate="Data: %{x}<br>" +
                     "Faturamento: " + 
                     df_evolucao['valorfaturado'].apply(formatar_moeda) +
                     "<extra></extra>"
    )
    
    return fig

def criar_grafico_top5_clientes(df_original):
    """
    Cria o gráfico dos Top 5 Clientes usando o DataFrame original,
    independente dos filtros aplicados
    """
    # Agrupa por cliente e soma o faturamento
    df_top5 = df_original.groupby('razao')['valorNota'].sum().reset_index()
    
    # Seleciona apenas os top 5
    df_top5 = df_top5.nlargest(5, 'valorNota')
    df_top5 = df_top5.sort_values('valorNota', ascending=True)
    
    # Cria o gráfico
    fig = px.bar(
        df_top5,
        y='razao',
        x='valorNota',
        orientation='h',
        title='Top 5 Clientes'
    )
    
    # Configurações do layout
    fig.update_layout(
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    
    # Formatação dos valores
    fig.update_traces(
        text=[formatar_moeda(val) for val in df_top5['valorNota']],
        textposition='outside',
        texttemplate='%{text}',
        textangle=0
    )
    
    return fig

ESTADO_PARA_ISO = {
    'Acre': 'BRA-AC',
    'Alagoas': 'BRA-AL',
    # ... (resto do mapeamento)
}

PERIODOS_TRENDS = {
    'Última semana': 'now 7-d',
    'Último mês': 'today 1-m',
    'Últimos 3 meses': 'today 3-m',
    'Último ano': 'today 12-m',
    'Últimos 5 anos': 'today 5-y'
}

# Mapeamento de nomes de estados para códigos ISO
ESTADO_TO_ISO = {
    'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 'Amazonas': 'AM',
    'Bahia': 'BA', 'Ceará': 'CE', 'Distrito Federal': 'DF',
    'Espírito Santo': 'ES', 'Goiás': 'GO', 'Maranhão': 'MA',
    'Mato Grosso': 'MT', 'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG',
    'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 'Pernambuco': 'PE',
    'Piauí': 'PI', 'Rio de Janeiro': 'RJ', 'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS', 'Rondônia': 'RO', 'Roraima': 'RR',
    'Santa Catarina': 'SC', 'São Paulo': 'SP', 'Sergipe': 'SE',
    'Tocantins': 'TO'
}

# Ordem dos dias da semana
ORDEM_DIAS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
NOMES_DIAS = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']

# Ordem dos meses
ORDEM_MESES = range(1, 13)
NOMES_MESES = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Faixas de valor para análise de clientes
ORDEM_FAIXAS_VALOR = [
    'Até R$ 1.000',
    'R$ 1.001 a R$ 5.000',
    'R$ 5.001 a R$ 10.000',
    'R$ 10.001 a R$ 50.000',
    'Acima de R$ 50.000'
]

def definir_faixa_valor(valor):
    if valor <= 1000:
        return 'Até R$ 1.000'
    elif valor <= 5000:
        return 'R$ 1.001 a R$ 5.000'
    elif valor <= 10000:
        return 'R$ 5.001 a R$ 10.000'
    elif valor <= 50000:
        return 'R$ 10.001 a R$ 50.000'
    else:
        return 'Acima de R$ 50.000'

def calcular_metricas_valor(df):
    valor_clientes = df.groupby('razao').agg({
        'valorNota': ['sum', 'mean', 'count']
    }).reset_index()
    
    valor_clientes.columns = ['Cliente', 'Valor_Total', 'Ticket_Medio', 'Num_Compras']
    valor_clientes['LTV'] = valor_clientes['Valor_Total']
    
    return valor_clientes

def identificar_novos_clientes(df):
    df_sorted = df.sort_values(['razao', 'data'])
    primeira_compra = df_sorted.groupby('razao')['data'].transform('min')
    df_sorted['novo_cliente'] = df_sorted['data'] == primeira_compra
    return df_sorted

def calcular_taxa_conversao(df):
    status_mensal = []
    
    for data in pd.date_range(df['data'].min(), df['data'].max(), freq='M'):
        df_ate_mes = df[df['data'] <= data]
        recencia = df_ate_mes.groupby('razao')['data'].max().apply(
            lambda x: (data - x).days
        )
        inativos_anterior = set(recencia[recencia > 180].index)
        mes_seguinte = data + pd.DateOffset(months=1)
        df_mes_seguinte = df[
            (df['data'] > data) & 
            (df['data'] <= mes_seguinte)
        ]
        reativados = len(set(df_mes_seguinte['razao']) & inativos_anterior)
        
        status_mensal.append({
            'data': data,
            'inativos': len(inativos_anterior),
            'reativados': reativados
        })
    
    df_status = pd.DataFrame(status_mensal)
    df_status['taxa_conversao'] = (df_status['reativados'] / df_status['inativos'] * 100)
    return df_status