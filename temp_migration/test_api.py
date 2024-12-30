from utils.api_connector import APIConnector
import json
import os
from dotenv import load_dotenv

def test_api_connection():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Mostra configurações (sem senhas)
    print('Configurações:')
    print(f"API_URL: {os.getenv('API_URL')}")
    print(f"API_CLIENT: {os.getenv('API_CLIENT')}")
    print(f"API_VIEW: {os.getenv('API_VIEW')}\n")
    
    # Inicializa o conector
    api = APIConnector()
    
    print('Testando conexão com a API...')
    
    try:
        # Testa conexão básica
        if api.check_connection():
            print('✓ Conexão básica OK')
        else:
            print('✗ Erro na conexão básica')
            return
            
        # Testa obtenção dos dados
        print('\nTentando obter dados de faturamento...')
        data = api.get_faturamento_data()
        
        if data:
            print('✓ Dados obtidos com sucesso!')
            print('\nPrimeiros 5 registros:')
            print(json.dumps(data[:5], indent=2))
            print(f'\nTotal de registros: {len(data)}')
        else:
            print('✗ Erro ao obter dados')
    except Exception as e:
        print(f'\nErro detalhado: {str(e)}')

if __name__ == '__main__':
    test_api_connection()
