import requests
import pandas as pd
from utils.constants import API_CONFIG, DATA_CONFIG, COLUNAS_RENAME

def carregar_dados_faturamento():
    """
    Carrega dados de faturamento da API já filtrados para os últimos 5 anos
    """
    try:
        response = requests.get(API_CONFIG["URL"], params=API_CONFIG["PARAMS"])
        response.raise_for_status()
        
        # Converte para DataFrame
        df = pd.DataFrame(response.json())
        
        # Função para converter datas com tratamento de erros
        def converter_data_segura(data_str):
            try:
                return pd.to_datetime(data_str, format='%Y-%m-%d', errors='coerce')
            except:
                return pd.to_datetime(data_str, errors='coerce')
        
        # Converte data com tratamento de erros
        df['data'] = df['data'].apply(converter_data_segura)
        df = df.dropna(subset=['data'])
        
        # Filtra os dados para os últimos 5 anos
        df = df[df['data'] >= DATA_CONFIG["DATA_INICIAL"]]
        
        # Renomeia colunas para padronizar
        df = df.rename(columns=COLUNAS_RENAME)
        
        return df
        
    except Exception as e:
        print(f"Erro ao carregar dados: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return None 