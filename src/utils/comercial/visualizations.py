"""
Módulo de visualizações para o dashboard comercial
"""
import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.utils.formatters import (
    formatar_moeda,
    MESES_PT,
    MESES_ORDEM,
    COORDENADAS_ESTADOS,
    SIGLAS_ESTADOS,
    MAPEAMENTO_PAISES,
    COORDENADAS_PAISES,
    NOMES_ESTADOS
)

def criar_mapa_faturamento(df: pd.DataFrame) -> go.Figure:
    """Cria mapa de bolhas para faturamento por estado/país"""
    # Separar dados do Brasil e do exterior
    df_brasil = df[df["uf"] != "EX"].copy()
    df_exterior = df[df["uf"] == "EX"].copy()
    
    # Processar dados do Brasil
    df_brasil_fat = df_brasil.groupby("uf")["valorfaturado"].sum().reset_index()
    df_brasil_fat["latitude"] = df_brasil_fat["uf"].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get("latitude"))
    df_brasil_fat["longitude"] = df_brasil_fat["uf"].map(lambda x: COORDENADAS_ESTADOS.get(x, {}).get("longitude"))
    df_brasil_fat["is_pais"] = False
    df_brasil_fat["Nome_Local"] = df_brasil_fat["uf"].map(NOMES_ESTADOS)
    
    # Processar dados do exterior
    df_exterior_fat = df_exterior.groupby("pais")["valorfaturado"].sum().reset_index()
    df_exterior_fat["sigla_pais"] = df_exterior_fat["pais"].map(MAPEAMENTO_PAISES)
    df_exterior_fat["latitude"] = df_exterior_fat["sigla_pais"].map(lambda x: COORDENADAS_PAISES.get(x, {}).get("lat"))
    df_exterior_fat["longitude"] = df_exterior_fat["sigla_pais"].map(lambda x: COORDENADAS_PAISES.get(x, {}).get("lon"))
    df_exterior_fat["is_pais"] = True
    df_exterior_fat["Nome_Local"] = df_exterior_fat["pais"]
    
    # Combinar dados
    df_fat_estado = pd.concat([
        df_brasil_fat[["Nome_Local", "valorfaturado", "latitude", "longitude", "is_pais"]],
        df_exterior_fat[["Nome_Local", "valorfaturado", "latitude", "longitude", "is_pais"]]
    ])
    
    # Remover registros sem coordenadas
    df_fat_estado = df_fat_estado.dropna(subset=["latitude", "longitude"])
    
    # Normalizar tamanho das bolhas
    scaler = MinMaxScaler(feature_range=(5, 50))
    df_fat_estado["bubble_size"] = scaler.fit_transform(df_fat_estado[["valorfaturado"]])
    
    # Formatar valores para o hover
    df_fat_estado["Faturamento Total"] = df_fat_estado["valorfaturado"].apply(formatar_moeda)
    
    # Criar o mapa
    fig = px.scatter_mapbox(
        df_fat_estado,
        lat="latitude",
        lon="longitude",
        size="bubble_size",
        color="is_pais",
        color_discrete_sequence=["blue", "red"],
        hover_name="Nome_Local",
        hover_data={
            "bubble_size": False,
            "latitude": False,
            "longitude": False,
            "is_pais": False,
            "Faturamento Total": True
        },
        mapbox_style="open-street-map",
        zoom=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        legend=dict(
            title="Localização",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            itemsizing="constant"
        )
    )
    
    fig.data[0].name = "Estados"
    fig.data[1].name = "Países"
    
    return fig

# ... (outras funções do módulo comercial)
