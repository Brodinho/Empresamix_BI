import locale
from typing import Dict, Any, Tuple
import pandas as pd

# Configurar locale para formatação de moeda em português do Brasil
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def formatar_moeda(valor: float) -> str:
    """Formata um valor numérico para moeda brasileira"""
    try:
        return locale.currency(valor, grouping=True, symbol=True)
    except:
        return f"R$ {valor:,.2f}"

# Constantes para meses em português
MESES_PT = {
    'january': 'Janeiro',
    'february': 'Fevereiro',
    'march': 'Março',
    'april': 'Abril',
    'may': 'Maio',
    'june': 'Junho',
    'july': 'Julho',
    'august': 'Agosto',
    'september': 'Setembro',
    'october': 'Outubro',
    'november': 'Novembro',
    'december': 'Dezembro'
}

MESES_ORDEM = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
               'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Coordenadas dos estados brasileiros
COORDENADAS_ESTADOS = {
    'AC': {'latitude': -9.0238, 'longitude': -70.8120},
    'AL': {'latitude': -9.5713, 'longitude': -36.7820},
    'AM': {'latitude': -3.4168, 'longitude': -65.8561},
    'AP': {'latitude': 1.4102, 'longitude': -51.7703},
    'BA': {'latitude': -12.9718, 'longitude': -38.5011},
    'CE': {'latitude': -3.7172, 'longitude': -38.5433},
    'DF': {'latitude': -15.7975, 'longitude': -47.8919},
    'ES': {'latitude': -20.2976, 'longitude': -40.2958},
    'GO': {'latitude': -16.6864, 'longitude': -49.2643},
    'MA': {'latitude': -2.5297, 'longitude': -44.3028},
    'MG': {'latitude': -19.9167, 'longitude': -43.9345},
    'MS': {'latitude': -20.4428, 'longitude': -54.6460},
    'MT': {'latitude': -15.6014, 'longitude': -56.0979},
    'PA': {'latitude': -1.4558, 'longitude': -48.4902},
    'PB': {'latitude': -7.1195, 'longitude': -34.8450},
    'PE': {'latitude': -8.0476, 'longitude': -34.8770},
    'PI': {'latitude': -5.0892, 'longitude': -42.8019},
    'PR': {'latitude': -25.4195, 'longitude': -49.2646},
    'RJ': {'latitude': -22.9068, 'longitude': -43.1729},
    'RN': {'latitude': -5.7945, 'longitude': -35.2120},
    'RO': {'latitude': -8.7619, 'longitude': -63.9039},
    'RR': {'latitude': 2.8198, 'longitude': -60.6714},
    'RS': {'latitude': -30.0346, 'longitude': -51.2177},
    'SC': {'latitude': -27.5954, 'longitude': -48.5480},
    'SE': {'latitude': -10.9091, 'longitude': -37.0677},
    'SP': {'latitude': -23.5505, 'longitude': -46.6333},
    'TO': {'latitude': -10.2491, 'longitude': -48.3243}
}

# Mapeamento de siglas dos estados
SIGLAS_ESTADOS = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    # ... outros estados ...
}

# Mapeamento de países para suas siglas
MAPEAMENTO_PAISES = {
    'ESTADOS UNIDOS': 'USA',
    'COLOMBIA': 'COL',
    'MEXICO': 'MEX',
    'PARAGUAI': 'PRY',
    'PERU': 'PER',
    'GUATEMALA': 'GTM',
    'EL SALVADOR': 'SLV',
    'BELIZE': 'BLZ',
    'URUGUAY': 'URY',
    'HONDURAS': 'HND',
    'ZIMBABWE': 'ZWE',
    'PANAMA': 'PAN',
    'NICARAGUA': 'NIC',
    'ARGENTINA': 'ARG',
    'COSTA RICA': 'CRI'
}

# Coordenadas dos países
COORDENADAS_PAISES = {
    'USA': {'lat': 37.0902, 'lon': -95.7129},
    'COL': {'lat': 4.5709, 'lon': -74.2973},
    'MEX': {'lat': 23.6345, 'lon': -102.5528},
    'PRY': {'lat': -23.4425, 'lon': -58.4438},
    'PER': {'lat': -9.1900, 'lon': -75.0152},
    'GTM': {'lat': 15.7835, 'lon': -90.2308},
    'SLV': {'lat': 13.7942, 'lon': -88.8965},
    'BLZ': {'lat': 17.1899, 'lon': -88.4976},
    'URY': {'lat': -32.5228, 'lon': -55.7658},
    'HND': {'lat': 15.2000, 'lon': -86.2419},
    'ZWE': {'lat': -19.0154, 'lon': 29.1549},
    'PAN': {'lat': 8.5380, 'lon': -80.7821},
    'NIC': {'lat': 12.8654, 'lon': -85.2072},
    'ARG': {'lat': -38.4161, 'lon': -63.6167},
    'CRI': {'lat': 9.7489, 'lon': -83.7534}
}

# Nomes dos estados por extenso
NOMES_ESTADOS = {
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
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'SE': 'Sergipe',
    'SP': 'São Paulo',
    'TO': 'Tocantins'
}

def calcular_metricas_individuais(df: pd.DataFrame, vendedor: str) -> Dict[str, Any]:
    """Calcula métricas individuais para um vendedor específico"""
    try:
        dados_vendedor = df[df['vendedor'] == vendedor]
        
        metricas = {
            'total_vendas': len(dados_vendedor),
            'faturamento_total': dados_vendedor['valor'].sum(),
            'ticket_medio': dados_vendedor['valor'].mean(),
            'maior_venda': dados_vendedor['valor'].max(),
            'menor_venda': dados_vendedor['valor'].min(),
            'total_clientes': dados_vendedor['codcli'].nunique(),  # Usando código do cliente
            'total_categorias': dados_vendedor['categoria'].nunique() if 'categoria' in dados_vendedor.columns else 0
        }
        
        return metricas
        
    except Exception as e:
        print(f"Erro ao calcular métricas: {str(e)}")
        return {
            'total_vendas': 0,
            'faturamento_total': 0,
            'ticket_medio': 0,
            'maior_venda': 0,
            'menor_venda': 0,
            'total_clientes': 0,
            'total_categorias': 0
        }

def calcular_tendencia(valores: pd.Series) -> str:
    """Calcula a tendência de uma série temporal"""
    if len(valores) < 2:
        return "neutro"
    
    primeira_metade = valores[:len(valores)//2].mean()
    segunda_metade = valores[len(valores)//2:].mean()
    
    if segunda_metade > primeira_metade * 1.05:
        return "crescimento"
    elif segunda_metade < primeira_metade * 0.95:
        return "queda"
    else:
        return "estavel" 

def criar_container_kpi(titulo: str, valor: str, variacao: str) -> str:
    """
    Cria um container HTML estilizado para KPI
    
    Args:
        titulo (str): Título do indicador
        valor (str): Valor principal do indicador
        variacao (str): Texto de variação (ex: "↑ 15% vs mês anterior")
    
    Returns:
        str: String HTML formatada do container
    """
    # Definição das cores com base na variação
    cor_variacao = '#4CAF50' if '↑' in variacao else \
                   '#FF5252' if '↓' in variacao else \
                   '#FFA500'  # Cor laranja para valores que se mantiveram
    
    return f"""
        <div style="
            background-color: #1E1E1E;
            border-radius: 12px;
            padding: 20px;
            height: 140px;
            border: 1px solid #444;
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.4),
                       inset 0 -1px 1px rgba(255, 255, 255, 0.1),
                       inset 0 1px 1px rgba(0, 0, 0, 0.2);
            margin: 5px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            text-align: center;
            transform: translateY(0);
            transition: all 0.2s ease;
        ">
            <div style="
                color: #FFF;
                font-size: 1.1em;
                font-weight: 500;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            ">{titulo}</div>
            <div style="
                color: white;
                font-size: 1.8em;
                font-weight: bold;
                margin-bottom: 12px;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            ">{valor}</div>
            <div style="
                font-size: 0.9em;
                color: {cor_variacao};
                font-weight: 500;
            ">{variacao}</div>
        </div>
    """ 

def calcular_variacao_periodo(
    df: pd.DataFrame,
    vendedor: str,
    metrica: str,
    data_atual: pd.Timestamp
) -> Tuple[float, str]:
    """
    Calcula a variação percentual de uma métrica entre o período atual e o anterior
    
    Args:
        df: DataFrame com os dados
        vendedor: Nome do vendedor
        metrica: Nome da métrica ('valor', 'qtd_vendas', 'clientes')
        data_atual: Data de referência para o cálculo
        
    Returns:
        Tuple[float, str]: (variação percentual, texto formatado para exibição)
    """
    try:
        # Filtrar dados do vendedor
        dados_vendedor = df[df['vendedor'] == vendedor].copy()
        
        # Determinar período atual e anterior
        mes_atual = data_atual.month
        ano_atual = data_atual.year
        
        # Calcular data do mês anterior
        if mes_atual == 1:
            mes_anterior = 12
            ano_anterior = ano_atual - 1
        else:
            mes_anterior = mes_atual - 1
            ano_anterior = ano_atual
            
        # Filtrar dados por período
        dados_mes_atual = dados_vendedor[
            (dados_vendedor['data'].dt.month == mes_atual) & 
            (dados_vendedor['data'].dt.year == ano_atual)
        ]
        
        dados_mes_anterior = dados_vendedor[
            (dados_vendedor['data'].dt.month == mes_anterior) & 
            (dados_vendedor['data'].dt.year == ano_anterior)
        ]
        
        # Calcular valores conforme a métrica
        if metrica == 'valor':
            valor_atual = dados_mes_atual['valor'].sum()
            valor_anterior = dados_mes_anterior['valor'].sum()
        elif metrica == 'qtd_vendas':
            valor_atual = len(dados_mes_atual)
            valor_anterior = len(dados_mes_anterior)
        elif metrica == 'ticket_medio':
            valor_atual = dados_mes_atual['valor'].mean()
            valor_anterior = dados_mes_anterior['valor'].mean()
        elif metrica == 'clientes':
            valor_atual = dados_mes_atual['codcli'].nunique()
            valor_anterior = dados_mes_anterior['codcli'].nunique()
        else:
            return 0.0, "Sem variação"
            
        # Calcular variação percentual
        if valor_anterior == 0:
            if valor_atual > 0:
                return 100.0, "↑ Novo"
            return 0.0, "Sem variação"
            
        variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
        
        # Formatar texto de retorno
        if variacao > 0:
            texto = f"↑ {abs(variacao):.1f}% vs mês anterior"
        elif variacao < 0:
            texto = f"↓ {abs(variacao):.1f}% vs mês anterior"
        else:
            texto = "Mesma quantidade mês anterior"
            
        return variacao, texto
        
    except Exception as e:
        print(f"Erro ao calcular variação: {str(e)}")
        return 0.0, "Sem variação" 