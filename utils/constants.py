# utils/constants.py
from datetime import datetime

# Constantes de API
API_CONFIG = {
    "URL": "http://tecnolife.empresamix.info:8077/POWERBI/",
    "PARAMS": {
        "CLIENTE": "TECNOLIFE",
        "ID": "XIOPMANA",
        "VIEW": "CUBO_FATURAMENTO"
    }
}

# Configurações de Data
DATA_CONFIG = {
    "ANOS_DEFAULT": 5,
    "DATA_INICIAL": datetime(datetime.now().year - 4, 1, 1)
}

# Mapeamento de colunas
COLUNAS_RENAME = {
    'valorfaturado': 'valor',
    'valorNota': 'valor_nota',
    'grupo': 'grupo',
    'subGrupo': 'categoria',
    'uf': 'estado'
}

# Dicionário para tradução dos meses
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

# Configurações de Gráficos
GRAPH_CONFIG = {
    'COLORS': {
        'line': '#00FF00',
        'bar': '#4169E1',
        'grid': 'rgba(128,128,128,0.2)'
    },
    'LAYOUT': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font_color': 'white'
    }
}

# Dicionário de conversão UF para código ISO
UF_TO_ISO = {
    'AC': 'BRA-AC', 'AL': 'BRA-AL', 'AP': 'BRA-AP', 'AM': 'BRA-AM',
    'BA': 'BRA-BA', 'CE': 'BRA-CE', 'DF': 'BRA-DF', 'ES': 'BRA-ES',
    'GO': 'BRA-GO', 'MA': 'BRA-MA', 'MT': 'BRA-MT', 'MS': 'BRA-MS',
    'MG': 'BRA-MG', 'PA': 'BRA-PA', 'PB': 'BRA-PB', 'PR': 'BRA-PR',
    'PE': 'BRA-PE', 'PI': 'BRA-PI', 'RJ': 'BRA-RJ', 'RN': 'BRA-RN',
    'RS': 'BRA-RS', 'RO': 'BRA-RO', 'RR': 'BRA-RR', 'SC': 'BRA-SC',
    'SP': 'BRA-SP', 'SE': 'BRA-SE', 'TO': 'BRA-TO'
}

# Coordenadas dos estados brasileiros
COORDENADAS_ESTADOS = {
    'AC': {'latitude': -8.77, 'longitude': -70.55},
    'AL': {'latitude': -9.71, 'longitude': -35.73},
    # ... resto das coordenadas dos estados
}

# Coordenadas dos países
COORDENADAS_PAISES = {
    'EUA': {'lat': 37.0902, 'lon': -95.7129},
    'COL': {'lat': 4.5709, 'lon': -74.2973},
    # ... resto das coordenadas dos países
}

# Mapeamento de siglas para nomes completos
SIGLAS_ESTADOS = {
    "AC": "Acre",
    "AL": "Alagoas",
    # ... resto das siglas
}

# Mapeamento de países para suas siglas
MAPEAMENTO_PAISES = {
    'COLOMBIA': 'COL',
    'PERU': 'PER',
    # ... resto do mapeamento
}
