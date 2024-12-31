import requests
import pandas as pd
from datetime import datetime
import streamlit as st

def carregar_dados_faturamento():
    """
    Carrega dados de faturamento da API
    """
    try:
        url = "http://tecnolife.empresamix.info:8077/POWERBI/"
        params = {
            "CLIENTE": "TECNOLIFE",
            "ID": "XIOPMANA", 
            "VIEW": "CUBO_FATURAMENTO"
        }
        
        # Debug: Mostrar URL completa
        st.write("URL da API:", url)
        st.write("Parâmetros:", params)
        
        response = requests.get(url, params=params)
        st.write("Status da resposta:", response.status_code)
        response.raise_for_status()
        
        # Converte para DataFrame
        df = pd.DataFrame(response.json())
        st.write("DataFrame criado com sucesso")
        st.write("Formato:", df.shape)
        st.write("Colunas:", df.columns.tolist())
        
        # Converter datas com tratamento de erros
        def converter_data(data_str):
            try:
                # Tentar converter a data
                return pd.to_datetime(data_str, format='%Y-%m-%d', errors='coerce')
            except:
                return pd.NaT
        
        # Converter as colunas de data
        df['data'] = df['data'].apply(converter_data)
        df['emissao'] = df['emissao'].apply(converter_data)
        
        # Remover linhas com datas inválidas
        df = df.dropna(subset=['data'])
        
        # Debug: Mostrar range de datas
        st.write("Range de datas:", 
                f"De: {df['data'].min()}", 
                f"Até: {df['data'].max()}")
        
        # Renomear colunas
        colunas = {
            'valorfaturado': 'valor',
            'valorNota': 'valor_nota',
            'grupo': 'grupo',
            'subGrupo': 'categoria',
            'uf': 'estado'
        }
        df = df.rename(columns=colunas)
        
        # Debug: Mostrar algumas estatísticas
        st.write("Total de registros após limpeza:", len(df))
        st.write("Total faturado:", df['valor'].sum())
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        st.write("Traceback completo:", e.__traceback__)
        return None 