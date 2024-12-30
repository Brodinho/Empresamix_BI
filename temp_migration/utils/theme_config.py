# Configurações de tema e cores para os dashboards
COLORS = {
    'blue': '#00B4D8',
    'orange': '#FF9F1C',
    'red': '#FF4B4B',
    'yellow': '#FFD93D',
    'gray': '#4F4F4F',
    'background': '#0E1117',
    'card': '#1B1B1B'
}

# Configuração padrão para gráficos Plotly
PLOT_CONFIG = {
    'template': 'plotly_dark',
    'paper_bgcolor': COLORS['background'],
    'plot_bgcolor': COLORS['background'],
    'font': {'color': '#FFFFFF'},
    'margin': {'t': 30, 'l': 10, 'r': 10, 'b': 10}
}
