import pandas as pd
from utils.formatters import formatar_moeda
from utils.constants import MESES_PT

def processar_metricas_vendedor(df_filtrado):
    """Processa os dados para criar métricas por vendedor"""
    try:
        df_metricas = df_filtrado.groupby('vendedor', as_index=False).agg({
            'nota': 'count',
            'valorNota': ['sum', 'mean']
        })
        df_metricas.columns = ['Vendedor', 'Pedidos', 'Valor Total', 'Ticket Médio']
        df_metricas = df_metricas.sort_values('Pedidos', ascending=False)
        df_metricas.index = range(1, len(df_metricas) + 1)
        df_metricas['Valor Total'] = df_metricas['Valor Total'].apply(formatar_moeda)
        df_metricas['Ticket Médio'] = df_metricas['Ticket Médio'].apply(formatar_moeda)
        return df_metricas
    except Exception as e:
        raise Exception(f"Erro ao processar métricas por vendedor: {str(e)}")

def processar_dados_geograficos(df):
    """Processa dados para visualização no mapa"""
    pass

def processar_dados_mensais(df_filtrado):
    """Processa dados para análise mensal"""
    try:
        # Remover linhas com datas nulas
        df_filtrado = df_filtrado.dropna(subset=['data'])
        
        # Criar DataFrame com as informações necessárias
        df_mensal = df_filtrado.assign(
            Ano=df_filtrado['data'].dt.year,
            Mês=df_filtrado['data'].dt.month_name().map(MESES_PT),
            Num_Mês=df_filtrado['data'].dt.month
        )
        
        # Agrupar os dados
        df_mensal = df_mensal.groupby(
            ['Mês', 'Ano', 'Num_Mês']
        )['valorNota'].sum().reset_index()
        
        # Ordenar por ano e mês
        df_mensal = df_mensal.sort_values(['Ano', 'Num_Mês'])
        
        return df_mensal
    except Exception as e:
        raise Exception(f"Erro ao processar dados mensais: {str(e)}")

def processar_dados_categoria(df):
    """Processa dados por categoria"""
    pass
