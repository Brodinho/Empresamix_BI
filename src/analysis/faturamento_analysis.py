import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from utils.formatters import (
    formatar_moeda,
    COORDENADAS_ESTADOS,
    MAPEAMENTO_PAISES,
    COORDENADAS_PAISES,
    NOMES_ESTADOS
)

def preparar_dados_mapa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepara os dados para o mapa de faturamento, separando dados do Brasil e exterior
    """
    try:
        # Debug: verificar dados de exportação
        print("Total de registros de exportação:", len(df[df['estado'] == 'EX']))
        if len(df[df['estado'] == 'EX']) > 0:
            print("Países nas exportações:", df[df['estado'] == 'EX']['pais'].unique())
            print("Códigos de países:", df[df['estado'] == 'EX']['codPais'].unique())
        
        # Separar dados do Brasil e do exterior
        df_brasil = df[df['estado'] != 'EX'].copy()
        df_exterior = df[df['estado'] == 'EX'].copy()
        
        # Processar dados do Brasil
        df_brasil_fat = df_brasil.groupby('estado')['valor'].sum().reset_index()
        df_brasil_fat['latitude'] = df_brasil_fat['estado'].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get('latitude'))
        df_brasil_fat['longitude'] = df_brasil_fat['estado'].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get('longitude'))
        df_brasil_fat['is_pais'] = False
        df_brasil_fat['Nome_Local'] = df_brasil_fat['estado'].map(NOMES_ESTADOS)
        
        # Processar dados do exterior
        if not df_exterior.empty:
            df_exterior_fat = df_exterior.groupby('pais')['valor'].sum().reset_index()
            df_exterior_fat['sigla_pais'] = df_exterior_fat['pais'].map(MAPEAMENTO_PAISES)
            df_exterior_fat['latitude'] = df_exterior_fat['sigla_pais'].map(lambda x: COORDENADAS_PAISES.get(x, {}).get('lat'))
            df_exterior_fat['longitude'] = df_exterior_fat['sigla_pais'].map(lambda x: COORDENADAS_PAISES.get(x, {}).get('lon'))
            df_exterior_fat['is_pais'] = True
            df_exterior_fat['Nome_Local'] = df_exterior_fat['pais']
            
            # Debug: verificar mapeamento
            print("Mapeamento de países:")
            for _, row in df_exterior_fat.iterrows():
                print(f"{row['pais']} -> {row['sigla_pais']} -> ({row['latitude']}, {row['longitude']})")
            
            # Combinar dados
            df_fat_estado = pd.concat([
                df_brasil_fat[['Nome_Local', 'valor', 'latitude', 'longitude', 'is_pais']],
                df_exterior_fat[['Nome_Local', 'valor', 'latitude', 'longitude', 'is_pais']]
            ])
        else:
            df_fat_estado = df_brasil_fat[['Nome_Local', 'valor', 'latitude', 'longitude', 'is_pais']]
        
        # Remover registros sem coordenadas
        df_fat_estado = df_fat_estado.dropna(subset=['latitude', 'longitude'])
        
        # Normalizar tamanho das bolhas
        scaler = MinMaxScaler(feature_range=(5, 50))
        df_fat_estado['bubble_size'] = scaler.fit_transform(df_fat_estado[['valor']])
        
        # Formatar valores para o hover
        df_fat_estado['Faturamento Total'] = df_fat_estado['valor'].apply(formatar_moeda)
        
        return df_fat_estado
        
    except Exception as e:
        print(f"Erro ao preparar dados do mapa: {str(e)}")
        return pd.DataFrame() 