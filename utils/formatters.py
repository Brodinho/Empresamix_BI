import locale
from typing import Dict, Any

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