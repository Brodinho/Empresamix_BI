import pandas as pd
from datetime import datetime

def aplicar_filtro_anos(df, anos_selecionados):
    """
    Filtra o DataFrame pelos anos selecionados, considerando sempre desde 01/01
    """
    if not anos_selecionados:
        return df
    
    # Criar máscara para os anos selecionados
    mascara = df['data'].dt.year.isin(anos_selecionados)
    
    return df[mascara].copy() 