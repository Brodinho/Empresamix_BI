import requests
import pandas as pd
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import logging
import streamlit as st
from datetime import datetime

# Configurar logging
logging.basicConfig(level=logging.INFO)

class APIConnector:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv('API_URL')
        self.client = os.getenv('API_CLIENT')
        self.api_id = os.getenv('API_ID')
        self.view = os.getenv('API_VIEW')
        
        if not all([self.base_url, self.client, self.api_id, self.view]):
            raise ValueError("Configurações da API incompletas. Verifique o arquivo .env")

    def _converter_data(self, data_str):
        """Converte string de data para datetime de forma segura"""
        try:
            # Tentar diferentes formatos de data
            for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']:
                try:
                    return pd.to_datetime(data_str, format=fmt)
                except:
                    continue
            
            # Se nenhum formato funcionar, usar parser automático com validação
            dt = pd.to_datetime(data_str)
            
            # Validar se a data está em um intervalo razoável (1900-2100)
            if dt.year < 1900 or dt.year > 2100:
                return pd.NaT
            
            return dt
            
        except Exception as e:
            logging.warning(f"Erro ao converter data '{data_str}': {str(e)}")
            return pd.NaT

    @st.cache_data(ttl=3600)  # Cache por 1 hora
    def get_dados(_self) -> pd.DataFrame:
        """Obtém e processa os dados da API com cache"""
        try:
            dados_raw = _self.get_faturamento_data()
            if not dados_raw:
                raise Exception("Não foi possível obter dados da API")
            
            # Converter lista JSON diretamente para DataFrame
            df = pd.DataFrame(dados_raw)
            
            # Converter coluna 'data' para datetime com tratamento de erros
            df['data'] = df['data'].apply(_self._converter_data)
            
            # Remover linhas com datas inválidas
            df = df.dropna(subset=['data'])
            
            # Log para debug
            logging.info(f"Colunas do DataFrame: {df.columns.tolist()}")
            logging.info(f"Número de registros: {len(df)}")
            logging.info(f"Range de datas: {df['data'].min()} até {df['data'].max()}")
            
            return df
            
        except Exception as e:
            logging.error(f"Erro ao processar dados: {str(e)}")
            raise

    def get_faturamento_data(self) -> List[Dict]:
        params = {
            'CLIENTE': self.client,
            'ID': self.api_id,
            'VIEW': self.view
        }
        
        try:
            logging.info(f"Tentando acessar: {self.base_url}")
            logging.info(f"Parâmetros: {params}")
            
            response = requests.get(
                self.base_url,
                params=params,
                timeout=10
            )
            
            logging.info(f"Status code: {response.status_code}")
            response.raise_for_status()
            
            dados = response.json()
            logging.info(f"Tipo de dados recebidos: {type(dados)}")
            logging.info(f"Tamanho dos dados: {len(dados) if isinstance(dados, list) else 'N/A'}")
            
            return dados
            
        except Exception as e:
            logging.error(f"Erro ao acessar a API: {str(e)}")
            return []

    def check_connection(self) -> bool:
        try:
            response = requests.get(self.base_url, timeout=5)
            return response.status_code == 200
        except:
            return False
