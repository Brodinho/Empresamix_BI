from pytrends.request import TrendReq
import pandas as pd
import streamlit as st

def init_pytrends():
    """Inicializa a conexão com o Google Trends"""
    try:
        pytrends = TrendReq(hl='pt-BR', tz=360)
        return pytrends
    except Exception as e:
        return None

def get_trends_data(keyword, timeframe, geo):
    """Obtém dados do Google Trends"""
    # Inicializar variáveis
    interest_over_time = None
    interest_by_region = None
    related_queries = {'top': None, 'rising': None}
    related_topics = {'top': None, 'rising': None}
    
    try:
        pytrends = init_pytrends()
        if not pytrends:
            return None, None, None, None
            
        # Construir payload
        try:
            pytrends.build_payload(
                kw_list=[keyword.strip()],
                cat=0,
                timeframe=timeframe,
                geo=geo
            )
        except Exception as e:
            return None, None, None, None
            
        # Dados temporais
        try:
            interest_over_time = pytrends.interest_over_time()
            if not interest_over_time.empty:
                interest_over_time = interest_over_time.drop('isPartial', axis=1) if 'isPartial' in interest_over_time.columns else interest_over_time
        except Exception:
            interest_over_time = pd.DataFrame()
            
        # Dados regionais
        try:
            interest_by_region = pytrends.interest_by_region(resolution='REGION', inc_low_vol=True)
        except Exception:
            interest_by_region = pd.DataFrame()
            
        # Consultas relacionadas
        try:
            queries = pytrends.related_queries()
            if queries and keyword.strip() in queries:
                related_queries = queries[keyword.strip()]
        except Exception:
            pass
            
        # Tópicos relacionados
        try:
            topics = pytrends.related_topics()
            if topics and keyword.strip() in topics:
                related_topics = topics[keyword.strip()]
        except Exception:
            pass
            
        # Verificar se temos pelo menos alguns dados
        if interest_over_time is not None and not interest_over_time.empty:
            return interest_over_time, interest_by_region, related_queries, related_topics
        else:
            st.warning("""
                Não foi possível obter dados do Google Trends.
                
                Sugestões:
                - Tente um termo mais genérico
                - Selecione um período diferente
                - Aguarde alguns minutos e tente novamente
            """)
            return None, None, None, None
            
    except Exception:
        return None, None, None, None 