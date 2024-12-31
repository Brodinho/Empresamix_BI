import os
from dotenv import load_dotenv
import pandas as pd
import requests
import json

class APIConnector:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("API_URL")
        self.token = None

    def authenticate(self, username: str, password: str) -> bool:
        """Autentica o usuário"""
        # Por enquanto, vamos usar uma autenticação simples
        return username == "admin" and password == "admin"

    def get_dados(self):
        """Obtém dados da API"""
        # Implementação temporária
        return pd.DataFrame({
            "data": ["2024-01-01", "2024-01-02"],
            "valor": [1000, 2000]
        })
