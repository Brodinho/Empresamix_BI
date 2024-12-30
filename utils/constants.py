# utils/constants.py

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
